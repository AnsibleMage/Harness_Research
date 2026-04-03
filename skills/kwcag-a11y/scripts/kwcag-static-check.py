#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KWCAG 2.2 Tier 1 정적 HTML 접근성 검사기
=========================================
한국형 웹 콘텐츠 접근성 지침 2.2 기반 정적 분석 도구.

사용법:
    python kwcag-static-check.py <path> [--format json|md] [--severity critical|major|minor|all]

의존성: Python 3 표준 라이브러리만 사용 (외부 패키지 없음)
"""

import argparse
import datetime
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser
from typing import Optional


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_ARIA_ROLES = frozenset({
    "alert", "alertdialog", "application", "article", "banner", "button",
    "cell", "checkbox", "columnheader", "combobox", "complementary",
    "contentinfo", "definition", "dialog", "directory", "document", "feed",
    "figure", "form", "grid", "gridcell", "group", "heading", "img", "link",
    "list", "listbox", "listitem", "log", "main", "marquee", "math", "menu",
    "menubar", "menuitem", "menuitemcheckbox", "menuitemradio", "navigation",
    "none", "note", "option", "presentation", "progressbar", "radio",
    "radiogroup", "region", "row", "rowgroup", "rowheader", "search",
    "searchbox", "separator", "slider", "spinbutton", "status", "switch",
    "tab", "table", "tablist", "tabpanel", "term", "textbox", "timer",
    "toolbar", "tooltip", "tree", "treegrid", "treeitem",
})

VALID_LANG_CODES = frozenset({
    "aa", "ab", "af", "ak", "am", "an", "ar", "as", "av", "ay", "az",
    "ba", "be", "bg", "bh", "bi", "bm", "bn", "bo", "br", "bs",
    "ca", "ce", "ch", "co", "cr", "cs", "cu", "cv", "cy",
    "da", "de", "dv", "dz",
    "ee", "el", "en", "eo", "es", "et", "eu",
    "fa", "ff", "fi", "fj", "fo", "fr", "fy",
    "ga", "gd", "gl", "gn", "gu", "gv",
    "ha", "he", "hi", "ho", "hr", "ht", "hu", "hy", "hz",
    "ia", "id", "ie", "ig", "ii", "ik", "in", "io", "is", "it", "iu",
    "ja", "jv", "jw",
    "ka", "kg", "ki", "kj", "kk", "kl", "km", "kn", "ko", "kr", "ks",
    "ku", "kv", "kw", "ky",
    "la", "lb", "lg", "li", "ln", "lo", "lt", "lu", "lv",
    "mg", "mh", "mi", "mk", "ml", "mn", "mo", "mr", "ms", "mt", "my",
    "na", "nb", "nd", "ne", "ng", "nl", "nn", "no", "nr", "nv", "ny",
    "oc", "oj", "om", "or", "os",
    "pa", "pi", "pl", "ps", "pt",
    "qu",
    "rm", "rn", "ro", "ru", "rw",
    "sa", "sc", "sd", "se", "sg", "sh", "si", "sk", "sl", "sm", "sn",
    "so", "sq", "sr", "ss", "st", "su", "sv", "sw",
    "ta", "te", "tg", "th", "ti", "tk", "tl", "tn", "to", "tr", "ts",
    "tt", "tw", "ty",
    "ug", "uk", "ur", "uz",
    "ve", "vi", "vo",
    "wa", "wo",
    "xh",
    "yi", "yo",
    "za", "zh", "zu",
})

INTERACTIVE_ELEMENTS = frozenset({
    "a", "button", "input", "select", "textarea", "summary", "details",
})

NON_INTERACTIVE_ELEMENTS = frozenset({
    "div", "span", "p", "li", "td", "section", "article", "header",
    "footer", "nav", "aside", "main", "figure", "figcaption",
})

VAGUE_LINK_TEXTS = frozenset({
    "여기", "클릭", "더보기", "more", "click here", "read more",
    "click", "here", "자세히", "바로가기", "링크",
})

FOCUSABLE_ELEMENTS = frozenset({
    "a", "button", "input", "select", "textarea", "iframe", "area",
    "summary",
})

KWCAG_PRINCIPLES = {
    "5.1": "인식의 용이성",
    "5.2": "인식의 용이성",
    "5.3": "인식의 용이성",
    "5.4": "인식의 용이성",
    "6.1": "운용의 용이성",
    "6.4": "운용의 용이성",
    "6.5": "운용의 용이성",
    "7.1": "이해의 용이성",
    "7.2": "이해의 용이성",
    "7.3": "이해의 용이성",
    "8.1": "견고성",
    "8.2": "견고성",
}

REQUIREMENT_NAMES = {
    "5.1.1": "적절한 대체 텍스트 제공",
    "5.2.1": "자막 제공",
    "5.3.1": "표의 구성",
    "5.3.2": "콘텐츠의 선형구조",
    "5.4.2": "자동 재생 금지",
    "6.1.1": "키보드 사용 보장",
    "6.1.2": "초점 이동과 표시",
    "6.1.4": "문자 단축키",
    "6.4.1": "반복 영역 건너뛰기",
    "6.4.2": "제목 제공",
    "6.4.3": "적절한 링크 텍스트",
    "6.5.3": "레이블과 네임",
    "7.1.1": "기본 언어 표시",
    "7.2.1": "사용자 요구에 따른 실행",
    "7.3.2": "레이블 제공",
    "7.3.3": "접근 가능한 인증",
    "8.1.1": "마크업 오류 방지",
    "8.2.1": "웹 애플리케이션 접근성 준수",
}


def _get_principle(req_id: str) -> str:
    """검사항목 ID에서 원칙 카테고리를 반환한다."""
    prefix = ".".join(req_id.split(".")[:2])
    return KWCAG_PRINCIPLES.get(prefix, "기타")


def _reconstruct_tag(tag: str, attrs: list[tuple[str, Optional[str]]]) -> str:
    """태그와 속성 목록으로 원본 HTML 태그 문자열을 재구성한다."""
    parts = [tag]
    for name, value in attrs:
        if value is None:
            parts.append(name)
        else:
            parts.append(f'{name}="{value}"')
    result = "<" + " ".join(parts) + ">"
    if len(result) > 120:
        result = result[:117] + "..."
    return result


# ---------------------------------------------------------------------------
# HTML Parser
# ---------------------------------------------------------------------------

class HTMLAccessibilityParser(HTMLParser):
    """
    HTMLParser 기반 접근성 분석용 파서.
    모든 요소, 속성, 텍스트 노드를 라인 번호와 함께 수집한다.
    """

    def __init__(self):
        super().__init__()
        # 수집된 모든 요소 (시작 태그) 목록
        self.elements: list[dict] = []
        # 현재 열린 요소 스택 (중첩 추적)
        self.element_stack: list[dict] = []
        # 모든 ID 수집 (중복 검사용)
        self.all_ids: list[tuple[str, int, str]] = []  # (id, line, tag)
        # 제목 태그 추적
        self.headings: list[dict] = []
        # style 태그 내용 수집
        self.style_contents: list[tuple[str, int]] = []  # (content, line)
        # 현재 수집 중인 텍스트
        self._current_text_parts: list[str] = []
        # 현재 a 태그 정보 (링크 텍스트 수집용)
        self._in_a: Optional[dict] = None
        self._a_text_parts: list[str] = []
        self._a_has_img: bool = False
        self._a_img_has_alt: bool = False
        # 현재 label 태그 정보
        self._in_label: Optional[dict] = None
        # 현재 style 태그 내부 여부
        self._in_style: bool = False
        self._style_line: int = 0
        self._style_parts: list[str] = []
        # 현재 title 태그 내부 여부
        self._in_title: bool = False
        self._title_parts: list[str] = []
        self.title_text: str = ""
        self.title_line: int = 0
        # 현재 heading 태그 내부 여부
        self._in_heading: Optional[dict] = None
        self._heading_text_parts: list[str] = []
        # 현재 svg 태그 내부 여부
        self._in_svg: bool = False
        self._svg_element: Optional[dict] = None
        self._svg_has_title: bool = False
        # iframe 수집
        self.iframes: list[dict] = []
        # label 수집 (for 속성 매핑)
        self.labels: list[dict] = []
        # select 수집 (onchange 검사용)
        self.selects: list[dict] = []
        # a 태그 중첩 감지
        self._a_depth: int = 0
        # button 태그 중첩 감지
        self._button_depth: int = 0
        # 중첩 위반 기록
        self.nesting_violations: list[dict] = []
        # html 태그 정보
        self.html_element: Optional[dict] = None
        # video/audio 태그
        self.media_elements: list[dict] = []
        self._in_media: Optional[dict] = None
        self._media_has_track_captions: bool = False
        # table 관련
        self.tables: list[dict] = []
        self._in_table: Optional[dict] = None
        self._table_has_th: bool = False
        self._table_has_td: bool = False
        self._th_elements: list[dict] = []
        # main/skip-link 존재 여부
        self.has_main_element: bool = False
        self.has_role_main: bool = False
        self.has_skip_link: bool = False
        # h1 존재 여부
        self.has_h1: bool = False
        # submit 버튼 라인 번호 목록
        self.submit_button_lines: list[int] = []
        # 완료된 링크 목록
        self.completed_links: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]):
        tag_lower = tag.lower()
        line = self.getpos()[0]
        attrs_dict = {k.lower(): v for k, v in attrs}
        element = {
            "tag": tag_lower,
            "attrs": attrs_dict,
            "attrs_list": attrs,
            "line": line,
            "raw": _reconstruct_tag(tag, attrs),
        }
        self.elements.append(element)
        self.element_stack.append(element)

        # ID 수집
        if "id" in attrs_dict and attrs_dict["id"]:
            self.all_ids.append((attrs_dict["id"], line, tag_lower))

        # html 태그
        if tag_lower == "html":
            self.html_element = element

        # heading 태그
        if tag_lower in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag_lower[1])
            element["level"] = level
            self._in_heading = element
            self._heading_text_parts = []
            if level == 1:
                self.has_h1 = True

        # a 태그
        if tag_lower == "a":
            self._a_depth += 1
            if self._a_depth > 1:
                self.nesting_violations.append({
                    "type": "a_in_a",
                    "line": line,
                    "raw": element["raw"],
                })
            self._in_a = element
            self._a_text_parts = []
            self._a_has_img = False
            self._a_img_has_alt = False
            # skip link 검사
            href = attrs_dict.get("href", "")
            if href and (href.startswith("#main") or href.startswith("#content")):
                self.has_skip_link = True

        # button 태그
        if tag_lower == "button":
            self._button_depth += 1
            if self._button_depth > 1:
                self.nesting_violations.append({
                    "type": "button_in_button",
                    "line": line,
                    "raw": element["raw"],
                })

        # img 내부 a 태그 처리
        if tag_lower == "img" and self._in_a is not None:
            self._a_has_img = True
            alt = attrs_dict.get("alt")
            if alt is not None and alt.strip():
                self._a_img_has_alt = True

        # label 태그
        if tag_lower == "label":
            self._in_label = element
            self.labels.append(element)

        # style 태그
        if tag_lower == "style":
            self._in_style = True
            self._style_line = line
            self._style_parts = []

        # title 태그
        if tag_lower == "title":
            self._in_title = True
            self._title_parts = []
            self.title_line = line

        # svg 태그
        if tag_lower == "svg":
            self._in_svg = True
            self._svg_element = element
            self._svg_has_title = False

        if self._in_svg and tag_lower == "title":
            self._svg_has_title = True

        # iframe 태그
        if tag_lower == "iframe":
            self.iframes.append(element)

        # select 태그
        if tag_lower == "select":
            self.selects.append(element)

        # video/audio 태그
        if tag_lower in ("video", "audio"):
            self._in_media = element
            self._media_has_track_captions = False
            self.media_elements.append(element)

        # track 태그 (media 내부)
        if tag_lower == "track" and self._in_media is not None:
            kind = attrs_dict.get("kind", "")
            if kind and kind.lower() in ("captions", "subtitles"):
                self._media_has_track_captions = True

        # table 태그
        if tag_lower == "table":
            self._in_table = element
            self._table_has_th = False
            self._table_has_td = False
            self._th_elements = []

        if tag_lower == "th" and self._in_table is not None:
            self._table_has_th = True
            self._th_elements.append(element)

        if tag_lower == "td" and self._in_table is not None:
            self._table_has_td = True

        # main 요소 또는 role=main
        if tag_lower == "main":
            self.has_main_element = True
        if attrs_dict.get("role", "").lower() == "main":
            self.has_role_main = True

        # submit 버튼
        if tag_lower == "button":
            btn_type = attrs_dict.get("type", "submit").lower()
            if btn_type == "submit":
                self.submit_button_lines.append(line)
        if tag_lower == "input":
            input_type = attrs_dict.get("type", "").lower()
            if input_type == "submit":
                self.submit_button_lines.append(line)

    def handle_endtag(self, tag: str):
        tag_lower = tag.lower()

        # heading 종료
        if tag_lower in ("h1", "h2", "h3", "h4", "h5", "h6") and self._in_heading:
            text = "".join(self._heading_text_parts).strip()
            self._in_heading["text"] = text
            self.headings.append(self._in_heading)
            self._in_heading = None

        # a 태그 종료
        if tag_lower == "a":
            if self._in_a is not None:
                text = "".join(self._a_text_parts).strip()
                link_info = {
                    "element": self._in_a,
                    "text": text,
                    "has_img": self._a_has_img,
                    "img_has_alt": self._a_img_has_alt,
                }
                self.completed_links.append(link_info)
                self._in_a = None
            self._a_depth = max(0, self._a_depth - 1)

        # button 종료
        if tag_lower == "button":
            self._button_depth = max(0, self._button_depth - 1)

        # style 종료
        if tag_lower == "style" and self._in_style:
            content = "".join(self._style_parts)
            self.style_contents.append((content, self._style_line))
            self._in_style = False

        # title 종료
        if tag_lower == "title" and self._in_title:
            self.title_text = "".join(self._title_parts).strip()
            self._in_title = False

        # svg 종료
        if tag_lower == "svg" and self._in_svg:
            if self._svg_element is not None:
                self._svg_element["has_title"] = self._svg_has_title
            self._in_svg = False
            self._svg_element = None

        # media 종료
        if tag_lower in ("video", "audio") and self._in_media is not None:
            self._in_media["has_track_captions"] = self._media_has_track_captions
            self._in_media = None

        # table 종료
        if tag_lower == "table" and self._in_table is not None:
            self._in_table["has_th"] = self._table_has_th
            self._in_table["has_td"] = self._table_has_td
            self._in_table["th_elements"] = self._th_elements
            self.tables.append(self._in_table)
            self._in_table = None

        # 스택에서 제거
        if self.element_stack:
            for i in range(len(self.element_stack) - 1, -1, -1):
                if self.element_stack[i]["tag"] == tag_lower:
                    self.element_stack.pop(i)
                    break

    def handle_data(self, data: str):
        # style 내용 수집
        if self._in_style:
            self._style_parts.append(data)
            return

        # title 내용 수집
        if self._in_title:
            self._title_parts.append(data)

        # heading 텍스트 수집
        if self._in_heading:
            self._heading_text_parts.append(data)

        # a 태그 텍스트 수집
        if self._in_a is not None:
            self._a_text_parts.append(data)


# ---------------------------------------------------------------------------
# KWCAG Static Checker
# ---------------------------------------------------------------------------

class KWCAGStaticChecker:
    """
    KWCAG 2.2 기반 정적 접근성 검사기.
    HTMLAccessibilityParser로 파싱한 결과를 기반으로
    22개 검사항목을 패턴 매칭으로 점검한다.
    """

    def __init__(self, file_path: str):
        self.file_path = os.path.abspath(file_path)
        self.parser = HTMLAccessibilityParser()
        self.violations: list[dict] = []
        self._html_source: str = ""

    def parse(self):
        """HTML 파일을 읽어 파싱한다."""
        with open(self.file_path, "r", encoding="utf-8", errors="replace") as f:
            self._html_source = f.read()
        self.parser.feed(self._html_source)

    def _add(
        self,
        requirement_id: str,
        severity: str,
        line: int,
        element: str,
        message: str,
        fix: str,
    ):
        """위반 사항을 목록에 추가한다."""
        self.violations.append({
            "requirement_id": requirement_id,
            "requirement_name": REQUIREMENT_NAMES.get(requirement_id, ""),
            "principle": _get_principle(requirement_id),
            "severity": severity,
            "line": line,
            "element": element,
            "message": message,
            "fix": fix,
        })

    def check_all(self) -> list[dict]:
        """모든 검사를 실행하고 위반 목록을 반환한다."""
        self.violations = []
        self.check_5_1_1()
        self.check_5_2_1()
        self.check_5_3_1()
        self.check_5_3_2()
        self.check_5_4_2()
        self.check_6_1_1()
        self.check_6_1_2()
        self.check_6_1_4()
        self.check_6_4_1()
        self.check_6_4_2()
        self.check_6_4_3()
        self.check_6_5_3()
        self.check_7_1_1()
        self.check_7_2_1()
        self.check_7_3_2()
        self.check_7_3_3()
        self.check_8_1_1()
        self.check_8_2_1()
        # 라인 번호 기준 정렬
        self.violations.sort(key=lambda v: (v["line"], v["requirement_id"]))
        return self.violations

    # ------------------------------------------------------------------
    # 5.1.1 적절한 대체 텍스트
    # ------------------------------------------------------------------
    def check_5_1_1(self):
        rid = "5.1.1"
        for el in self.parser.elements:
            tag = el["tag"]
            attrs = el["attrs"]
            line = el["line"]
            raw = el["raw"]

            # img without alt
            if tag == "img":
                if "alt" not in attrs:
                    self._add(rid, "critical", line, raw,
                              "이미지에 alt 속성이 없습니다.",
                              'alt="이미지 설명" 속성을 추가하세요.')

            # area without alt
            if tag == "area":
                if "alt" not in attrs:
                    self._add(rid, "critical", line, raw,
                              "이미지 맵 영역(area)에 alt 속성이 없습니다.",
                              'alt="영역 설명" 속성을 추가하세요.')

            # input[type=image] without alt
            if tag == "input":
                input_type = attrs.get("type", "").lower()
                if input_type == "image" and "alt" not in attrs:
                    self._add(rid, "critical", line, raw,
                              "이미지 버튼(input[type=image])에 alt 속성이 없습니다.",
                              'alt="버튼 설명" 속성을 추가하세요.')

            # [role=img] without aria-label/aria-labelledby
            if attrs.get("role", "").lower() == "img":
                has_label = ("aria-label" in attrs and attrs["aria-label"]) or \
                            ("aria-labelledby" in attrs and attrs["aria-labelledby"])
                if not has_label:
                    self._add(rid, "critical", line, raw,
                              'role="img" 요소에 aria-label 또는 aria-labelledby가 없습니다.',
                              'aria-label="설명" 또는 aria-labelledby="id" 속성을 추가하세요.')

            # svg without title/aria-label
            if tag == "svg":
                has_aria = ("aria-label" in attrs and attrs["aria-label"]) or \
                           ("aria-labelledby" in attrs and attrs["aria-labelledby"])
                has_title = el.get("has_title", False)
                if not has_aria and not has_title:
                    self._add(rid, "major", line, raw,
                              "SVG에 대체 텍스트가 없습니다.",
                              '<title>설명</title> 또는 aria-label 속성을 추가하세요.')

    # ------------------------------------------------------------------
    # 5.2.1 자막 제공
    # ------------------------------------------------------------------
    def check_5_2_1(self):
        rid = "5.2.1"
        for el in self.parser.media_elements:
            tag = el["tag"]
            line = el["line"]
            raw = el["raw"]
            has_track = el.get("has_track_captions", False)

            if tag == "video" and not has_track:
                self._add(rid, "critical", line, raw,
                          "비디오에 자막 트랙(track[kind=captions])이 없습니다.",
                          '<track kind="captions" src="captions.vtt" srclang="ko"> 요소를 추가하세요.')

            if tag == "audio" and not has_track:
                self._add(rid, "major", line, raw,
                          "오디오에 자막 또는 대체 텍스트 트랙이 없습니다.",
                          '자막 트랙을 추가하거나 인근에 텍스트 대본을 제공하세요.')

    # ------------------------------------------------------------------
    # 5.3.1 표의 구성
    # ------------------------------------------------------------------
    def check_5_3_1(self):
        rid = "5.3.1"
        for tbl in self.parser.tables:
            line = tbl["line"]
            raw = tbl["raw"]
            has_th = tbl.get("has_th", False)
            has_td = tbl.get("has_td", False)

            # 데이터 테이블(td 있음)인데 th가 없으면
            if has_td and not has_th:
                self._add(rid, "major", line, raw,
                          "데이터 테이블에 제목 셀(th)이 없습니다.",
                          "테이블의 열/행 제목에 <th> 요소를 사용하세요.")

            # th에 scope 속성 없음
            for th in tbl.get("th_elements", []):
                if "scope" not in th["attrs"]:
                    self._add(rid, "minor", th["line"], th["raw"],
                              "th 요소에 scope 속성이 없습니다.",
                              'scope="col" 또는 scope="row" 속성을 추가하세요.')

    # ------------------------------------------------------------------
    # 5.3.2 콘텐츠의 선형구조
    # ------------------------------------------------------------------
    def check_5_3_2(self):
        rid = "5.3.2"
        prev_level = 0
        for h in self.parser.headings:
            level = h["level"]
            line = h["line"]
            raw = h["raw"]
            # 제목 레벨 건너뛰기 검사 (예: h1→h3)
            if prev_level > 0 and level > prev_level + 1:
                self._add(rid, "major", line, raw,
                          f"제목 레벨이 건너뛰어졌습니다 (h{prev_level} → h{level}).",
                          f"h{prev_level + 1}을 사용하거나 제목 계층 구조를 수정하세요.")
            prev_level = level

    # ------------------------------------------------------------------
    # 5.4.2 자동 재생 금지
    # ------------------------------------------------------------------
    def check_5_4_2(self):
        rid = "5.4.2"
        for el in self.parser.elements:
            tag = el["tag"]
            attrs = el["attrs"]
            line = el["line"]
            raw = el["raw"]

            if tag in ("video", "audio") and "autoplay" in attrs:
                self._add(rid, "critical", line, raw,
                          f"{tag} 요소에 autoplay 속성이 설정되어 있습니다.",
                          "autoplay 속성을 제거하고 사용자가 직접 재생하도록 하세요.")

    # ------------------------------------------------------------------
    # 6.1.1 키보드 사용 보장
    # ------------------------------------------------------------------
    def check_6_1_1(self):
        rid = "6.1.1"
        for el in self.parser.elements:
            tag = el["tag"]
            attrs = el["attrs"]
            line = el["line"]
            raw = el["raw"]

            has_onclick = "onclick" in attrs
            if not has_onclick:
                continue

            # 비대화형 요소에 onclick이 있지만 키보드 핸들러가 없는 경우
            has_keyboard = "onkeydown" in attrs or "onkeypress" in attrs or "onkeyup" in attrs
            is_interactive = tag in INTERACTIVE_ELEMENTS
            role = attrs.get("role", "").lower()
            # role이 대화형 역할이면 대화형으로 간주
            interactive_roles = {"button", "link", "menuitem", "tab", "checkbox",
                                 "radio", "switch", "textbox", "combobox"}
            if role in interactive_roles:
                is_interactive = True

            if not is_interactive:
                if not has_keyboard:
                    self._add(rid, "critical", line, raw,
                              f"비대화형 요소({tag})에 onclick이 있지만 키보드 이벤트 핸들러가 없습니다.",
                              "onkeydown 또는 onkeypress 이벤트 핸들러를 추가하세요.")

                # tabindex 또는 role 없는 경우
                has_tabindex = "tabindex" in attrs
                has_role = bool(role)
                if not has_tabindex and not has_role:
                    self._add(rid, "major", line, raw,
                              f"{tag} 요소에 onclick이 있지만 tabindex와 role이 없습니다.",
                              'tabindex="0"과 적절한 role 속성을 추가하세요.')

    # ------------------------------------------------------------------
    # 6.1.2 초점 이동과 표시
    # ------------------------------------------------------------------
    def check_6_1_2(self):
        rid = "6.1.2"
        # 인라인 스타일에서 outline 제거 검사
        for el in self.parser.elements:
            attrs = el["attrs"]
            line = el["line"]
            raw = el["raw"]
            style = attrs.get("style", "")
            if style:
                if re.search(r'outline\s*:\s*(none|0)\b', style, re.IGNORECASE):
                    self._add(rid, "critical", line, raw,
                              "인라인 스타일에서 outline을 제거하여 초점 표시가 보이지 않을 수 있습니다.",
                              "outline:none 대신 대체 초점 스타일을 제공하세요.")

            # tabindex > 0
            tabindex = attrs.get("tabindex")
            if tabindex is not None:
                try:
                    if int(tabindex) > 0:
                        self._add(rid, "major", line, raw,
                                  f"tabindex 값이 0보다 큽니다 (tabindex={tabindex}). 자연스러운 탭 순서가 깨질 수 있습니다.",
                                  'tabindex="0" 이하의 값을 사용하세요.')
                except ValueError:
                    pass

        # style 태그 내부에서 :focus{outline:none} 검사
        for content, style_line in self.parser.style_contents:
            # :focus 블록 내부 outline:none 검사
            focus_pattern = re.finditer(
                r':focus\s*\{([^}]*)\}', content, re.DOTALL
            )
            for match in focus_pattern:
                block = match.group(1)
                if re.search(r'outline\s*:\s*(none|0)\b', block, re.IGNORECASE):
                    # 줄 번호 추정: style 시작 + 내부 오프셋
                    offset = content[:match.start()].count('\n')
                    self._add(rid, "critical", style_line + offset,
                              f"<style> ... :focus {{ outline: none }} ...</style>",
                              ":focus 규칙에서 outline을 제거하여 초점 표시가 보이지 않습니다.",
                              "outline:none 대신 시각적 대체 초점 스타일을 제공하세요.")

    # ------------------------------------------------------------------
    # 6.1.4 문자 단축키
    # ------------------------------------------------------------------
    def check_6_1_4(self):
        rid = "6.1.4"
        for el in self.parser.elements:
            attrs = el["attrs"]
            line = el["line"]
            raw = el["raw"]

            if "accesskey" in attrs:
                self._add(rid, "minor", line, raw,
                          f'accesskey="{attrs["accesskey"]}" 속성이 사용되었습니다. 키보드 단축키 충돌 가능성이 있습니다.',
                          "accesskey 사용 시 충돌하지 않는 키를 선택하고, 사용자가 변경하거나 비활성화할 수 있도록 하세요.")

    # ------------------------------------------------------------------
    # 6.4.1 반복 영역 건너뛰기
    # ------------------------------------------------------------------
    def check_6_4_1(self):
        rid = "6.4.1"
        has_skip = self.parser.has_skip_link
        has_main = self.parser.has_main_element or self.parser.has_role_main

        if not has_skip:
            self._add(rid, "major", 1, "<html>",
                      "건너뛰기 링크가 없습니다.",
                      '<a href="#main">본문 바로가기</a> 링크를 페이지 상단에 추가하세요.')

        if not has_main:
            self._add(rid, "major", 1, "<html>",
                      '<main> 요소 또는 role="main"이 없습니다.',
                      "주요 콘텐츠 영역을 <main> 요소로 감싸세요.")

    # ------------------------------------------------------------------
    # 6.4.2 제목 제공
    # ------------------------------------------------------------------
    def check_6_4_2(self):
        rid = "6.4.2"

        # title 태그 검사
        if not self.parser.title_text:
            self._add(rid, "critical", self.parser.title_line or 1, "<title>",
                      "페이지 제목(title)이 비어있거나 없습니다.",
                      "<title>페이지 제목</title>을 <head> 내에 추가하세요.")

        # h1 존재 검사
        if not self.parser.has_h1:
            self._add(rid, "major", 1, "<html>",
                      "페이지에 h1 제목이 없습니다.",
                      "페이지의 주요 제목에 <h1> 요소를 사용하세요.")

        # 빈 제목 검사
        for h in self.parser.headings:
            text = h.get("text", "")
            if not text:
                self._add(rid, "major", h["line"], h["raw"],
                          f"빈 제목 요소(h{h['level']})가 있습니다.",
                          "제목 요소에 적절한 텍스트 내용을 추가하세요.")

        # iframe without title
        for iframe in self.parser.iframes:
            if "title" not in iframe["attrs"] or not iframe["attrs"]["title"]:
                self._add(rid, "major", iframe["line"], iframe["raw"],
                          "iframe에 title 속성이 없습니다.",
                          'title="프레임 설명" 속성을 추가하세요.')

    # ------------------------------------------------------------------
    # 6.4.3 적절한 링크 텍스트
    # ------------------------------------------------------------------
    def check_6_4_3(self):
        rid = "6.4.3"
        for link_info in self.parser.completed_links:
            el = link_info["element"]
            text = link_info["text"]
            has_img = link_info["has_img"]
            img_has_alt = link_info["img_has_alt"]
            line = el["line"]
            raw = el["raw"]
            attrs = el["attrs"]

            # aria-label이 있으면 접근 가능한 이름이 제공된 것으로 간주
            if attrs.get("aria-label") or attrs.get("aria-labelledby") or attrs.get("title"):
                continue

            # 빈 링크 텍스트
            if not text and not has_img:
                self._add(rid, "critical", line, raw,
                          "링크에 텍스트가 없습니다.",
                          "링크에 설명 텍스트를 추가하거나 aria-label을 사용하세요.")
                continue

            # 이미지만 있는 링크인데 alt가 없는 경우
            if not text and has_img and not img_has_alt:
                self._add(rid, "critical", line, raw,
                          "이미지만 있는 링크에서 이미지에 alt 텍스트가 없습니다.",
                          "링크 내 이미지에 alt 속성으로 링크 목적을 설명하세요.")
                continue

            # 모호한 링크 텍스트
            if text.lower().strip() in VAGUE_LINK_TEXTS:
                self._add(rid, "major", line, raw,
                          f'링크 텍스트가 모호합니다: "{text}".',
                          "링크의 목적을 명확히 설명하는 텍스트를 사용하세요.")

    # ------------------------------------------------------------------
    # 6.5.3 레이블과 네임
    # ------------------------------------------------------------------
    def check_6_5_3(self):
        rid = "6.5.3"
        for el in self.parser.elements:
            attrs = el["attrs"]
            line = el["line"]
            raw = el["raw"]
            aria_label = attrs.get("aria-label", "")
            if not aria_label:
                continue

            # 기본 검사: aria-label이 매우 짧거나 의미 없는 경우
            stripped = aria_label.strip()
            if len(stripped) < 1:
                self._add(rid, "major", line, raw,
                          "aria-label 값이 비어있습니다.",
                          "aria-label에 의미 있는 텍스트를 제공하세요.")

    # ------------------------------------------------------------------
    # 7.1.1 기본 언어 표시
    # ------------------------------------------------------------------
    def check_7_1_1(self):
        rid = "7.1.1"
        html_el = self.parser.html_element
        if html_el is None:
            self._add(rid, "critical", 1, "<html>",
                      "html 요소를 찾을 수 없습니다.",
                      '<html lang="ko"> 형식으로 lang 속성을 지정하세요.')
            return

        lang = html_el["attrs"].get("lang", "")
        line = html_el["line"]
        raw = html_el["raw"]

        if not lang:
            self._add(rid, "critical", line, raw,
                      "html 요소에 lang 속성이 없습니다.",
                      '<html lang="ko"> 형식으로 lang 속성을 추가하세요.')
            return

        # lang 값 유효성 검사 (기본 언어 코드만)
        base_lang = lang.split("-")[0].lower().strip()
        if base_lang not in VALID_LANG_CODES:
            self._add(rid, "major", line, raw,
                      f'html lang 속성의 값이 유효하지 않습니다: "{lang}".',
                      '유효한 BCP 47 언어 코드를 사용하세요 (예: "ko", "en", "ja").')

    # ------------------------------------------------------------------
    # 7.2.1 사용자 요구에 따른 실행
    # ------------------------------------------------------------------
    def check_7_2_1(self):
        rid = "7.2.1"
        for sel in self.parser.selects:
            attrs = sel["attrs"]
            line = sel["line"]
            raw = sel["raw"]

            if "onchange" not in attrs:
                continue

            # 인근 submit 버튼 존재 여부 (±30줄 범위)
            has_nearby_submit = False
            for submit_line in self.parser.submit_button_lines:
                if abs(submit_line - line) <= 30:
                    has_nearby_submit = True
                    break

            if not has_nearby_submit:
                self._add(rid, "major", line, raw,
                          "select 요소에 onchange가 있지만 인근에 제출(submit) 버튼이 없습니다.",
                          "onchange로 페이지를 변경하는 대신 별도의 제출 버튼을 제공하세요.")

    # ------------------------------------------------------------------
    # 7.3.2 레이블 제공
    # ------------------------------------------------------------------
    def check_7_3_2(self):
        rid = "7.3.2"
        # label[for] 값 수집
        label_for_values: set[str] = set()
        for lbl in self.parser.labels:
            for_val = lbl["attrs"].get("for", "")
            if for_val:
                label_for_values.add(for_val)

        for el in self.parser.elements:
            tag = el["tag"]
            attrs = el["attrs"]
            line = el["line"]
            raw = el["raw"]

            if tag not in ("input", "select", "textarea"):
                continue

            # hidden, submit, button, reset, image는 제외
            if tag == "input":
                input_type = attrs.get("type", "text").lower()
                if input_type in ("hidden", "submit", "button", "reset", "image"):
                    continue

            # 레이블 확인 방법: label[for], aria-label, aria-labelledby, title
            el_id = attrs.get("id", "")
            has_label_for = el_id and el_id in label_for_values
            has_aria_label = bool(attrs.get("aria-label", ""))
            has_aria_labelledby = bool(attrs.get("aria-labelledby", ""))
            has_title = bool(attrs.get("title", ""))

            if not (has_label_for or has_aria_label or has_aria_labelledby or has_title):
                has_placeholder = bool(attrs.get("placeholder", ""))
                if has_placeholder:
                    self._add(rid, "major", line, raw,
                              f"{tag} 요소에 placeholder만 있고 레이블이 없습니다.",
                              "placeholder는 레이블을 대체할 수 없습니다. <label> 또는 aria-label을 추가하세요.")
                else:
                    self._add(rid, "critical", line, raw,
                              f"{tag} 요소에 레이블이 없습니다.",
                              '<label for="id">레이블</label> 또는 aria-label 속성을 추가하세요.')

        # label[for] 가 실제 요소 ID와 매칭되지 않는 경우
        all_ids_set = {item[0] for item in self.parser.all_ids}
        for lbl in self.parser.labels:
            for_val = lbl["attrs"].get("for", "")
            if for_val and for_val not in all_ids_set:
                self._add(rid, "major", lbl["line"], lbl["raw"],
                          f'label의 for="{for_val}"에 해당하는 ID를 가진 요소가 없습니다.',
                          "label의 for 속성 값과 대상 요소의 id를 일치시키세요.")

    # ------------------------------------------------------------------
    # 7.3.3 접근 가능한 인증
    # ------------------------------------------------------------------
    def check_7_3_3(self):
        rid = "7.3.3"
        for el in self.parser.elements:
            tag = el["tag"]
            attrs = el["attrs"]
            line = el["line"]
            raw = el["raw"]

            if tag == "input":
                input_type = attrs.get("type", "text").lower()
                if input_type == "password":
                    if "autocomplete" not in attrs:
                        self._add(rid, "minor", line, raw,
                                  "비밀번호 입력란에 autocomplete 속성이 없습니다.",
                                  'autocomplete="current-password" 또는 autocomplete="new-password" 속성을 추가하세요.')

    # ------------------------------------------------------------------
    # 8.1.1 마크업 오류 방지
    # ------------------------------------------------------------------
    def check_8_1_1(self):
        rid = "8.1.1"
        # 중복 ID 검사
        id_occurrences: dict[str, list[tuple[int, str]]] = {}
        for id_val, line, tag in self.parser.all_ids:
            if id_val not in id_occurrences:
                id_occurrences[id_val] = []
            id_occurrences[id_val].append((line, tag))

        for id_val, occurrences in id_occurrences.items():
            if len(occurrences) > 1:
                lines_str = ", ".join(str(l) for l, _ in occurrences)
                for occ_line, occ_tag in occurrences[1:]:
                    self._add(rid, "critical", occ_line,
                              f'<{occ_tag} id="{id_val}">',
                              f'중복된 id="{id_val}"가 발견되었습니다 (라인: {lines_str}).',
                              "각 요소의 id 값은 문서 내에서 고유해야 합니다.")

        # a 안의 a, button 안의 button 중첩
        for violation in self.parser.nesting_violations:
            vtype = violation["type"]
            line = violation["line"]
            raw = violation["raw"]
            if vtype == "a_in_a":
                self._add(rid, "critical", line, raw,
                          "<a> 요소 내부에 <a> 요소가 중첩되어 있습니다.",
                          "링크(a) 요소를 중첩하지 마세요.")
            elif vtype == "button_in_button":
                self._add(rid, "critical", line, raw,
                          "<button> 요소 내부에 <button> 요소가 중첩되어 있습니다.",
                          "버튼(button) 요소를 중첩하지 마세요.")

    # ------------------------------------------------------------------
    # 8.2.1 웹 애플리케이션 접근성
    # ------------------------------------------------------------------
    def check_8_2_1(self):
        rid = "8.2.1"
        for el in self.parser.elements:
            tag = el["tag"]
            attrs = el["attrs"]
            line = el["line"]
            raw = el["raw"]

            # 유효하지 않은 role 값
            role = attrs.get("role", "")
            if role:
                # 여러 role이 공백으로 구분될 수 있음
                roles = role.strip().lower().split()
                for r in roles:
                    if r not in VALID_ARIA_ROLES:
                        self._add(rid, "major", line, raw,
                                  f'유효하지 않은 role 값: "{r}".',
                                  f"유효한 WAI-ARIA role 값을 사용하세요.")

            # aria-hidden=true on focusable elements
            aria_hidden = attrs.get("aria-hidden", "").lower()
            if aria_hidden == "true":
                is_focusable = tag in FOCUSABLE_ELEMENTS
                # tabindex가 있으면 포커스 가능
                if "tabindex" in attrs:
                    try:
                        if int(attrs["tabindex"]) >= 0:
                            is_focusable = True
                    except ValueError:
                        pass
                if is_focusable:
                    self._add(rid, "critical", line, raw,
                              '포커스 가능한 요소에 aria-hidden="true"가 설정되어 있습니다.',
                              "aria-hidden을 제거하거나 tabindex=\"-1\"로 포커스를 비활성화하세요.")


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

def format_json(results: dict) -> str:
    """결과를 JSON 형식으로 변환한다."""
    return json.dumps(results, ensure_ascii=False, indent=2)


def format_markdown(results: dict) -> str:
    """결과를 마크다운 형식으로 변환한다."""
    lines: list[str] = []
    lines.append("# KWCAG 2.2 접근성 검사 보고서")
    lines.append("")
    lines.append(f"- **검사 일시**: {results['metadata']['timestamp']}")
    lines.append(f"- **검사 파일 수**: {results['metadata']['total_files']}")
    lines.append(f"- **총 위반 수**: {results['metadata']['total_violations']}")
    lines.append("")

    # 심각도별 요약
    summary = results["metadata"]["severity_summary"]
    lines.append("## 심각도별 요약")
    lines.append("")
    lines.append("| 심각도 | 건수 |")
    lines.append("|--------|------|")
    lines.append(f"| Critical | {summary.get('critical', 0)} |")
    lines.append(f"| Major | {summary.get('major', 0)} |")
    lines.append(f"| Minor | {summary.get('minor', 0)} |")
    lines.append("")

    # 원칙별 요약
    principle_summary = results["metadata"].get("principle_summary", {})
    if principle_summary:
        lines.append("## 원칙별 요약")
        lines.append("")
        lines.append("| 원칙 | 건수 |")
        lines.append("|------|------|")
        for principle, count in sorted(principle_summary.items()):
            lines.append(f"| {principle} | {count} |")
        lines.append("")

    # 파일별 결과
    for file_result in results["files"]:
        filepath = file_result["file"]
        violations = file_result["violations"]
        lines.append(f"## {os.path.basename(filepath)}")
        lines.append("")
        lines.append(f"> 경로: `{filepath}`")
        lines.append(f"> 위반 수: {len(violations)}")
        lines.append("")

        if not violations:
            lines.append("위반 사항이 없습니다.")
            lines.append("")
            continue

        # 심각도별 그룹핑
        for severity in ("critical", "major", "minor"):
            severity_violations = [v for v in violations if v["severity"] == severity]
            if not severity_violations:
                continue

            severity_label = {"critical": "Critical", "major": "Major", "minor": "Minor"}[severity]
            lines.append(f"### {severity_label} ({len(severity_violations)}건)")
            lines.append("")

            for v in severity_violations:
                lines.append(f"- **[{v['requirement_id']}] {v['requirement_name']}** (라인 {v['line']})")
                lines.append(f"  - 요소: `{v['element']}`")
                lines.append(f"  - 문제: {v['message']}")
                lines.append(f"  - 수정: {v['fix']}")
                lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_check(
    path: str,
    severity_filter: str = "all",
) -> dict:
    """
    단일 파일 또는 디렉토리를 검사하고 결과를 반환한다.
    """
    files: list[str] = []

    if os.path.isfile(path):
        files.append(os.path.abspath(path))
    elif os.path.isdir(path):
        # 재귀적으로 HTML 파일 탐색
        pattern = os.path.join(path, "**", "*.html")
        files = sorted(glob.glob(pattern, recursive=True))
        if not files:
            # htm 확장자도 검색
            pattern_htm = os.path.join(path, "**", "*.htm")
            files = sorted(glob.glob(pattern_htm, recursive=True))
    else:
        print(f"오류: 경로를 찾을 수 없습니다: {path}", file=sys.stderr)
        sys.exit(1)

    if not files:
        print(f"오류: HTML 파일을 찾을 수 없습니다: {path}", file=sys.stderr)
        sys.exit(1)

    all_file_results: list[dict] = []
    total_violations = 0
    severity_summary: dict[str, int] = {"critical": 0, "major": 0, "minor": 0}
    principle_summary: dict[str, int] = {}

    for filepath in files:
        checker = KWCAGStaticChecker(filepath)
        try:
            checker.parse()
        except Exception as e:
            print(f"경고: 파일 파싱 실패 - {filepath}: {e}", file=sys.stderr)
            continue

        violations = checker.check_all()

        # 심각도 필터링
        if severity_filter != "all":
            violations = [v for v in violations if v["severity"] == severity_filter]

        for v in violations:
            severity_summary[v["severity"]] = severity_summary.get(v["severity"], 0) + 1
            principle = v["principle"]
            principle_summary[principle] = principle_summary.get(principle, 0) + 1

        total_violations += len(violations)
        all_file_results.append({
            "file": filepath,
            "violations": violations,
            "violation_count": len(violations),
        })

    results = {
        "metadata": {
            "tool": "KWCAG 2.2 정적 접근성 검사기",
            "version": "1.0.0",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_files": len(files),
            "total_violations": total_violations,
            "severity_filter": severity_filter,
            "severity_summary": severity_summary,
            "principle_summary": principle_summary,
        },
        "files": all_file_results,
    }

    return results


def main():
    parser = argparse.ArgumentParser(
        description="KWCAG 2.2 Tier 1 정적 HTML 접근성 검사기",
        epilog="사용 예: python kwcag-static-check.py ./pages --format md --severity critical",
    )
    parser.add_argument(
        "path",
        help="검사할 HTML 파일 또는 디렉토리 경로",
    )
    parser.add_argument(
        "--format",
        choices=["json", "md"],
        default="json",
        help="출력 형식 (기본값: json)",
    )
    parser.add_argument(
        "--severity",
        choices=["critical", "major", "minor", "all"],
        default="all",
        help="표시할 심각도 필터 (기본값: all)",
    )

    args = parser.parse_args()

    results = run_check(args.path, args.severity)

    if args.format == "json":
        output = format_json(results)
    else:
        output = format_markdown(results)

    # UTF-8 출력 보장 (Windows 환경)
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    print(output)

    # 위반 존재 시 종료 코드 1
    if results["metadata"]["total_violations"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
