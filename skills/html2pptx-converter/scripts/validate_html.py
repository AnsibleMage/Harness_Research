#!/usr/bin/env python3
"""
validate_html.py - Validate HTML files against html2pptx conversion rules.

Usage:
    python scripts/validate_html.py <html_file_or_directory> [--output <json_path>] [--mode wireframe]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

# Windows encoding fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_BODY_DIMENSIONS = [
    ("720pt", "405pt"),   # 16:9
    ("720pt", "540pt"),   # 4:3
    ("720pt", "450pt"),   # 16:10
]

WEB_SAFE_FONTS = {
    "arial", "helvetica", "times new roman", "georgia",
    "courier new", "verdana", "tahoma", "trebuchet ms",
    "impact", "comic sans ms",
    "sans-serif", "serif", "monospace",
}

MANUAL_BULLET_CHARS = {"•", "‣", "▸", "▹", "-", "*", "◦", "●", "○"}

TEXT_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li"}
TEXT_TAG_SET = TEXT_TAGS

SHAPE_CSS_PROPS = {"background", "background-color", "border", "box-shadow"}
SPAN_DISALLOWED_PROPS = {"margin", "padding",
                         "margin-top", "margin-bottom", "margin-left", "margin-right",
                         "padding-top", "padding-bottom", "padding-left", "padding-right"}

WIREFRAME_ALLOWED_COLORS = {"#000000", "#808080", "#e0e0e0", "#ffffff"}

SEVERITY_ERROR = "error"
SEVERITY_WARNING = "warning"


# ---------------------------------------------------------------------------
# CSS Utility
# ---------------------------------------------------------------------------

def parse_inline_style(style_str: str) -> dict:
    """Parse an inline style string into a {property: value} dict."""
    result = {}
    if not style_str:
        return result
    for declaration in style_str.split(";"):
        declaration = declaration.strip()
        if ":" not in declaration:
            continue
        prop, _, val = declaration.partition(":")
        result[prop.strip().lower()] = val.strip().lower()
    return result


def extract_css_blocks(html: str) -> list:
    """Extract raw CSS text from <style> blocks."""
    return re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL | re.IGNORECASE)


def parse_css_block(css_text: str) -> list:
    """
    Parse CSS block into list of (selector, {property: value}) tuples.
    Very lightweight parser — handles simple single-level rules.
    """
    rules = []
    # Remove comments
    css_text = re.sub(r"/\*.*?\*/", "", css_text, flags=re.DOTALL)
    for match in re.finditer(r"([^{]+)\{([^}]*)\}", css_text):
        selector = match.group(1).strip().lower()
        declarations = match.group(2)
        props = {}
        for decl in declarations.split(";"):
            decl = decl.strip()
            if ":" not in decl:
                continue
            prop, _, val = decl.partition(":")
            props[prop.strip().lower()] = val.strip().lower()
        if props:
            rules.append((selector, props))
    return rules


def get_effective_styles_for_tag(tag: str, css_rules: list, inline_style: str) -> dict:
    """
    Merge CSS rules matching the tag with its inline style.
    Inline style wins over CSS (higher specificity).
    """
    merged = {}
    for selector, props in css_rules:
        # Accept if selector is exactly the tag name or ends with the tag (e.g. "body", "div > body")
        selector_parts = re.split(r"[\s>+~,]", selector)
        selector_parts = [s.strip() for s in selector_parts if s.strip()]
        if selector_parts and selector_parts[-1] == tag:
            merged.update(props)
    merged.update(parse_inline_style(inline_style))
    return merged


# ---------------------------------------------------------------------------
# HTML Validation Parser
# ---------------------------------------------------------------------------

class HtmlValidationParser(HTMLParser):
    """
    Single-pass HTML parser that collects all information needed for validation.
    """

    def __init__(self, html_source: str):
        super().__init__()
        self.html_source = html_source
        self.lines = html_source.splitlines()

        # Tag tracking
        self._tag_stack: list = []          # list of (tag, attrs_dict)
        self._in_body = False

        # Collected data for validation
        self.body_attrs: dict = {}
        self.body_line: int = 0

        # list of (tag, attrs, line, parent_text_tag_or_none)
        self.text_tag_entries: list = []

        # list of (tag, attrs, line)  — tags that should NOT have shape styling
        self.non_div_styled_entries: list = []

        # list of (tag, attrs, line) for <span>
        self.span_entries: list = []

        # list of (text, line, parent_tag)
        self.p_text_entries: list = []

        # current text-parent tag
        self._current_text_tag: str | None = None
        self._current_line_offset: int = 0

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_line(self) -> int:
        """Approximate current line number via getpos()."""
        line, _ = self.getpos()
        return line

    @staticmethod
    def _attrs_to_dict(attrs) -> dict:
        return {k.lower(): (v or "") for k, v in attrs}

    # ------------------------------------------------------------------
    # HTMLParser overrides
    # ------------------------------------------------------------------

    def handle_starttag(self, tag: str, attrs):
        tag = tag.lower()
        attrs_dict = self._attrs_to_dict(attrs)
        line = self._get_line()

        self._tag_stack.append((tag, attrs_dict))

        if tag == "body":
            self._in_body = True
            self.body_attrs = attrs_dict
            self.body_line = line

        if tag in TEXT_TAG_SET:
            self._current_text_tag = tag
            self.text_tag_entries.append((tag, attrs_dict, line))

        if tag in ("p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol") and tag != "div":
            self.non_div_styled_entries.append((tag, attrs_dict, line))

        if tag == "span":
            self.span_entries.append((tag, attrs_dict, line))

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        # Pop stack
        for i in range(len(self._tag_stack) - 1, -1, -1):
            if self._tag_stack[i][0] == tag:
                self._tag_stack.pop(i)
                break
        if tag == self._current_text_tag:
            self._current_text_tag = None
        if tag == "body":
            self._in_body = False

    def handle_data(self, data: str):
        if not self._in_body:
            return
        text = data.strip()
        if not text:
            return
        line = self._get_line()
        # Determine innermost tag
        innermost = self._tag_stack[-1][0] if self._tag_stack else None
        self.p_text_entries.append((text, line, innermost))


# ---------------------------------------------------------------------------
# Validation Rules
# ---------------------------------------------------------------------------

class ValidationResult:
    def __init__(self, filepath: str):
        self.file = filepath
        self.errors: list = []
        self.warnings: list = []

    def add_error(self, rule: str, message: str, line: int):
        self.errors.append({"rule": rule, "message": message, "line": line, "severity": SEVERITY_ERROR})

    def add_warning(self, rule: str, message: str, line: int):
        self.warnings.append({"rule": rule, "message": message, "line": line, "severity": SEVERITY_WARNING})

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "errors": self.errors,
            "warnings": self.warnings,
        }


PT_PATTERN = re.compile(r"^(\d+(?:\.\d+)?)pt$")


def rule_body_dimensions(result: ValidationResult, body_attrs: dict, css_rules: list, body_line: int, strict: bool = False):
    """body must have width and height in pt units.

    strict=True: only the 3 standard pairs are allowed (full_design compat).
    strict=False: any positive pt value is accepted; non-standard emits warning.
    """
    styles = get_effective_styles_for_tag("body", css_rules, body_attrs.get("style", ""))

    width = styles.get("width", "").strip().lower()
    height = styles.get("height", "").strip().lower()

    if not width and not height:
        result.add_error("body_dimensions",
                         "body 태그에 width/height 인라인 스타일이 없습니다", body_line)
        return

    if strict:
        matched = any(width == w and height == h for w, h in VALID_BODY_DIMENSIONS)
        if not matched:
            result.add_error(
                "body_dimensions",
                f"body 태그의 크기가 올바르지 않습니다 (현재: width={width}, height={height}). "
                "허용값: 720pt×405pt (16:9), 720pt×540pt (4:3), 720pt×450pt (16:10)",
                body_line,
            )
    else:
        # Flexible mode: accept any positive pt value
        w_match = PT_PATTERN.match(width)
        h_match = PT_PATTERN.match(height)

        if not w_match or float(w_match.group(1)) <= 0:
            result.add_error(
                "body_dimensions",
                f"body width가 유효한 pt 값이 아닙니다 (현재: {width}). 양수 pt 값이어야 합니다.",
                body_line,
            )
        if not h_match or float(h_match.group(1)) <= 0:
            result.add_error(
                "body_dimensions",
                f"body height가 유효한 pt 값이 아닙니다 (현재: {height}). 양수 pt 값이어야 합니다.",
                body_line,
            )

        # Warn if non-standard
        if w_match and h_match:
            is_standard = any(width == w and height == h for w, h in VALID_BODY_DIMENSIONS)
            if not is_standard:
                result.add_warning(
                    "body_dimensions",
                    f"비표준 body 크기입니다 (현재: {width}×{height}). "
                    "CUSTOM defineLayout이 필요할 수 있습니다.",
                    body_line,
                )


def rule_display_flex(result: ValidationResult, body_attrs: dict, css_rules: list, body_line: int):
    """body must have display: flex."""
    styles = get_effective_styles_for_tag("body", css_rules, body_attrs.get("style", ""))
    display = styles.get("display", "").strip().lower()
    if display != "flex":
        result.add_error(
            "display_flex",
            f"body 태그에 display: flex 스타일이 없습니다 (현재: display={display or '없음'})",
            body_line,
        )


def rule_text_in_proper_tags(result: ValidationResult, p_text_entries: list):
    """Text must not appear directly in <div> or <span> without a proper text ancestor."""
    DISALLOWED_DIRECT_PARENTS = {"div", "span", "section", "article", "aside", "main",
                                 "header", "footer", "nav", "figure", "figcaption"}
    for text, line, parent in p_text_entries:
        if parent in DISALLOWED_DIRECT_PARENTS:
            result.add_error(
                "text_in_proper_tags",
                f"텍스트 '{text[:30]}...' 가 <{parent}> 태그에 직접 포함되어 있습니다. "
                "<p> 또는 <h1>~<h6> 태그로 감싸야 합니다.",
                line,
            )


def rule_no_css_gradient(result: ValidationResult, html: str, css_rules: list):
    """No CSS gradients allowed."""
    # Check inline styles in HTML
    for match in re.finditer(r'style\s*=\s*["\']([^"\']*(?:linear-gradient|radial-gradient)[^"\']*)["\']',
                              html, re.IGNORECASE):
        line_num = html[:match.start()].count("\n") + 1
        result.add_error(
            "no_css_gradient",
            "인라인 스타일에 CSS 그라디언트(linear-gradient/radial-gradient)가 사용되었습니다",
            line_num,
        )
    # Check <style> blocks
    for selector, props in css_rules:
        for prop, val in props.items():
            if "linear-gradient" in val or "radial-gradient" in val:
                result.add_error(
                    "no_css_gradient",
                    f"<style> 블록의 '{selector}' 규칙에 CSS 그라디언트가 사용되었습니다",
                    0,
                )


def rule_web_safe_fonts(result: ValidationResult, html: str, css_rules: list):
    """Only web-safe fonts allowed."""
    def check_font_family(value: str, line: int, context: str):
        # Split font stack
        fonts = [f.strip().strip("'\"").lower() for f in value.split(",")]
        for font in fonts:
            if font and font not in WEB_SAFE_FONTS:
                result.add_error(
                    "web_safe_fonts",
                    f"{context}에 웹 안전 폰트가 아닌 '{font}' 폰트가 사용되었습니다",
                    line,
                )

    # Check inline styles
    for match in re.finditer(r'style\s*=\s*["\']([^"\']*)["\']', html, re.IGNORECASE):
        inline = match.group(1)
        fm = re.search(r'font-family\s*:\s*([^;]+)', inline, re.IGNORECASE)
        if fm:
            line_num = html[:match.start()].count("\n") + 1
            check_font_family(fm.group(1), line_num, "인라인 스타일")

    # Check CSS rules
    for selector, props in css_rules:
        ff = props.get("font-family", "")
        if ff:
            check_font_family(ff, 0, f"CSS 규칙 '{selector}'")


def rule_no_manual_bullets(result: ValidationResult, p_text_entries: list):
    """No manual bullet characters at start of <p> text."""
    for text, line, parent in p_text_entries:
        if parent == "p" and text:
            first_char = text[0]
            if first_char in MANUAL_BULLET_CHARS:
                result.add_error(
                    "no_manual_bullets",
                    f"<p> 태그에 수동 불릿 문자 '{first_char}'가 사용되었습니다. "
                    "<ul>/<li> 태그를 사용하세요.",
                    line,
                )


def rule_shape_styling_on_div_only(result: ValidationResult, non_div_entries: list, css_rules: list):
    """background, border, box-shadow should only be on div elements."""
    for tag, attrs, line in non_div_entries:
        styles = parse_inline_style(attrs.get("style", ""))
        for prop in SHAPE_CSS_PROPS:
            if prop in styles:
                result.add_warning(
                    "shape_styling_on_div_only",
                    f"<{tag}> 태그에 '{prop}' 스타일이 적용되어 있습니다. "
                    "배경/테두리 스타일은 <div> 태그에만 사용하는 것을 권장합니다.",
                    line,
                )

    # Also check CSS rules targeting non-div text tags
    text_tags_no_div = TEXT_TAG_SET - {"div"}
    for selector, props in css_rules:
        selector_parts = re.split(r"[\s>+~,]", selector)
        selector_parts = [s.strip() for s in selector_parts if s.strip()]
        if not selector_parts:
            continue
        last = selector_parts[-1]
        # Strip pseudo-classes/elements and attribute selectors
        tag_only = re.split(r"[:.#\[]", last)[0]
        if tag_only in text_tags_no_div:
            for prop in SHAPE_CSS_PROPS:
                if prop in props:
                    result.add_warning(
                        "shape_styling_on_div_only",
                        f"CSS 규칙 '{selector}'에서 <{tag_only}> 태그에 '{prop}' 스타일이 적용되어 있습니다",
                        0,
                    )


def rule_span_style_limits(result: ValidationResult, span_entries: list):
    """span elements should only use font-weight, font-style, text-decoration, color."""
    for tag, attrs, line in span_entries:
        styles = parse_inline_style(attrs.get("style", ""))
        for prop in styles:
            if prop in SPAN_DISALLOWED_PROPS:
                result.add_warning(
                    "span_style_limits",
                    f"<span> 태그에 '{prop}' 스타일이 사용되었습니다. "
                    "<span>에는 font-weight, font-style, text-decoration, color만 사용하세요.",
                    line,
                )


def rule_badge_ordering(result: ValidationResult, html: str):
    """Wireframe mode: badge/overlay elements must be in the last portion of <body>.

    html2pptx renders elements in DOM order — earlier = below, later = above.
    Badges/markers placed before content sections will be covered and invisible.
    """
    body_match = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL | re.IGNORECASE)
    if not body_match:
        return
    body_content = body_match.group(1)
    body_len = len(body_content)
    if body_len == 0:
        return

    # Find all badge class elements
    badge_positions = [m.start() for m in re.finditer(r'class\s*=\s*["\']badge["\']', body_content, re.IGNORECASE)]
    if not badge_positions:
        return

    # Badges should be in the last 30% of body content
    threshold = body_len * 0.7
    for pos in badge_positions:
        if pos < threshold:
            line_num = html[:html.index(body_content) + pos].count("\n") + 1
            result.add_warning(
                "badge_ordering",
                "배지(badge) 요소가 body의 앞부분에 위치합니다. "
                "다른 요소에 덮일 수 있으므로 body의 마지막에 배치하세요.",
                line_num,
            )


def rule_badge_uniqueness(result: ValidationResult, html: str):
    """Wireframe mode: each badge must have a unique (left, top) coordinate pair.

    Duplicate coordinates cause one badge to cover another, making it invisible.
    """
    badge_pattern = re.compile(
        r'class\s*=\s*["\']badge["\'][^>]*style\s*=\s*["\']([^"\']*)["\']',
        re.IGNORECASE,
    )
    positions = []
    for match in badge_pattern.finditer(html):
        style = match.group(1)
        left_m = re.search(r'left\s*:\s*([\d.]+pt)', style)
        top_m = re.search(r'top\s*:\s*([\d.]+pt)', style)
        if left_m and top_m:
            coord = (left_m.group(1), top_m.group(1))
            line_num = html[:match.start()].count("\n") + 1
            positions.append((coord, line_num))

    seen = {}
    for coord, line in positions:
        if coord in seen:
            result.add_warning(
                "badge_uniqueness",
                f"배지 좌표 ({coord[0]}, {coord[1]})가 중복됩니다 "
                f"(이전 발견: line {seen[coord]}). 각 배지는 고유한 위치를 가져야 합니다.",
                line,
            )
        else:
            seen[coord] = line


def rule_wireframe_colors(result: ValidationResult, html: str, css_rules: list):
    """Wireframe mode: only #000000, #808080, #E0E0E0, #FFFFFF colors allowed.

    Non-wireframe colors emit warnings (not errors) to account for edge cases.
    Active only when --mode wireframe is specified.
    """
    COLOR_CSS_PROPS = {"color", "background-color", "background", "border-color",
                       "border", "border-top", "border-bottom", "border-left", "border-right"}

    hex_pattern = re.compile(r"#([0-9a-fA-F]{6})\b")

    def check_color_value(value: str, line: int, context: str):
        for match in hex_pattern.finditer(value):
            found_color = f"#{match.group(1).lower()}"
            if found_color not in WIREFRAME_ALLOWED_COLORS:
                result.add_warning(
                    "wireframe_colors",
                    f"{context}에 와이어프레임 비허용 색상 '{found_color}'이 사용되었습니다. "
                    f"허용: {', '.join(sorted(WIREFRAME_ALLOWED_COLORS))}",
                    line,
                )

    # Check inline styles in HTML
    for match in re.finditer(r'style\s*=\s*["\']([^"\']*)["\']', html, re.IGNORECASE):
        inline = match.group(1)
        line_num = html[:match.start()].count("\n") + 1
        for prop_name in COLOR_CSS_PROPS:
            prop_match = re.search(rf'{prop_name}\s*:\s*([^;]+)', inline, re.IGNORECASE)
            if prop_match:
                check_color_value(prop_match.group(1), line_num, f"인라인 스타일 '{prop_name}'")

    # Check <style> blocks
    for selector, props in css_rules:
        for prop_name in COLOR_CSS_PROPS:
            val = props.get(prop_name, "")
            if val:
                check_color_value(val, 0, f"CSS 규칙 '{selector}' → '{prop_name}'")


# ---------------------------------------------------------------------------
# Core Validation Function
# ---------------------------------------------------------------------------

def validate_file(filepath: str, mode: str = "full_design") -> ValidationResult:
    """Run all validation rules on a single HTML file.

    mode: "full_design" (strict body dimensions) or "wireframe" (flexible body + color check).
    """
    result = ValidationResult(filepath)

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            html = fh.read()
    except FileNotFoundError:
        result.add_error("file_read", f"파일을 찾을 수 없습니다: {filepath}", 0)
        return result
    except OSError as exc:
        result.add_error("file_read", f"파일 읽기 오류: {exc}", 0)
        return result

    # Parse CSS blocks
    css_text_blocks = extract_css_blocks(html)
    css_rules: list = []
    for block in css_text_blocks:
        css_rules.extend(parse_css_block(block))

    # Parse HTML structure
    parser = HtmlValidationParser(html)
    try:
        parser.feed(html)
    except Exception as exc:  # noqa: BLE001
        result.add_error("html_parse", f"HTML 파싱 오류: {exc}", 0)
        return result

    # Determine strict mode for body dimensions
    strict_dimensions = (mode != "wireframe")

    # Run rules
    if not parser.body_attrs and parser.body_line == 0:
        result.add_error("body_dimensions", "<body> 태그를 찾을 수 없습니다", 1)
        result.add_error("display_flex", "<body> 태그를 찾을 수 없습니다", 1)
    else:
        rule_body_dimensions(result, parser.body_attrs, css_rules, parser.body_line, strict=strict_dimensions)
        rule_display_flex(result, parser.body_attrs, css_rules, parser.body_line)

    rule_text_in_proper_tags(result, parser.p_text_entries)
    rule_no_css_gradient(result, html, css_rules)
    rule_web_safe_fonts(result, html, css_rules)
    rule_no_manual_bullets(result, parser.p_text_entries)
    rule_shape_styling_on_div_only(result, parser.non_div_styled_entries, css_rules)
    rule_span_style_limits(result, parser.span_entries)

    # Wireframe-specific rules
    if mode == "wireframe":
        rule_wireframe_colors(result, html, css_rules)
        rule_badge_ordering(result, html)
        rule_badge_uniqueness(result, html)

    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def collect_html_files(target: str) -> list:
    """Return list of .html file paths from a file or directory."""
    path = Path(target)
    if path.is_file():
        if path.suffix.lower() != ".html":
            print(f"경고: '{target}'는 .html 파일이 아닙니다. 그대로 처리합니다.")
        return [str(path)]
    if path.is_dir():
        files = sorted(path.glob("**/*.html"))
        return [str(f) for f in files]
    return []


def determine_output_path(input_target: str, output_arg: str | None) -> str:
    if output_arg:
        return output_arg
    input_path = Path(input_target)
    if input_path.is_file():
        return str(input_path.parent / "html_validation.json")
    return str(input_path / "html_validation.json")


def build_output(results: list, start_time: datetime, mode: str) -> dict:
    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)
    return {
        "validated_at": start_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": mode,
        "files_checked": len(results),
        "results": [r.to_dict() for r in results],
        "summary": {
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "pass": total_errors == 0,
        },
    }


def print_summary(output: dict):
    summary = output["summary"]
    print(f"\n{'='*60}")
    print(f"HTML 유효성 검사 결과 (모드: {output.get('mode', 'full_design')})")
    print(f"{'='*60}")
    print(f"검사 파일 수  : {output['files_checked']}")
    print(f"총 오류       : {summary['total_errors']}")
    print(f"총 경고       : {summary['total_warnings']}")
    status = "PASS" if summary["pass"] else "FAIL"
    print(f"결과          : {status}")
    print(f"{'='*60}")

    for file_result in output["results"]:
        if file_result["errors"] or file_result["warnings"]:
            print(f"\n파일: {file_result['file']}")
            for item in file_result["errors"]:
                print(f"  [ERROR] (line {item['line']}) [{item['rule']}] {item['message']}")
            for item in file_result["warnings"]:
                print(f"  [WARN]  (line {item['line']}) [{item['rule']}] {item['message']}")


def main():
    parser = argparse.ArgumentParser(
        description="html2pptx 변환 규칙에 따라 HTML 파일을 검증합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python scripts/validate_html.py slides/slide_00.html
  python scripts/validate_html.py slides/
  python scripts/validate_html.py slides/ --output results/validation.json
  python scripts/validate_html.py slides/ --mode wireframe
        """,
    )
    parser.add_argument(
        "target",
        metavar="html_file_or_directory",
        help="검증할 HTML 파일 또는 디렉터리 경로",
    )
    parser.add_argument(
        "--output",
        metavar="json_path",
        help="결과 JSON 파일 저장 경로 (기본값: 입력 경로와 같은 위치의 html_validation.json)",
        default=None,
    )
    parser.add_argument(
        "--mode",
        choices=["full_design", "wireframe"],
        default="full_design",
        help="검증 모드: full_design(기본, 고정 body 크기) 또는 wireframe(유연 body 크기 + 색상 검증)",
    )
    args = parser.parse_args()

    # Collect files
    files = collect_html_files(args.target)
    if not files:
        print(f"오류: '{args.target}'에서 HTML 파일을 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)

    start_time = datetime.now(timezone.utc)
    results = [validate_file(f, mode=args.mode) for f in files]

    output = build_output(results, start_time, args.mode)
    print_summary(output)

    # Write JSON
    output_path = determine_output_path(args.target, args.output)
    try:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(output, fh, ensure_ascii=False, indent=2)
        print(f"\n상세 결과 저장됨: {output_path}")
    except OSError as exc:
        print(f"경고: JSON 파일 저장 실패: {exc}", file=sys.stderr)

    sys.exit(0 if output["summary"]["pass"] else 1)


if __name__ == "__main__":
    main()
