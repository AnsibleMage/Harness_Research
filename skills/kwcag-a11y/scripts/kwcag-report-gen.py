#!/usr/bin/env python3
"""
KWCAG 2.2 통합 보고서 생성기

Tier 1 (정적 분석) 및 Tier 2 (axe-core) JSON 결과를 병합하여
한국어 접근성 검사 보고서를 Markdown 또는 HTML 형식으로 생성한다.

Usage:
    python kwcag-report-gen.py --tier1 t1.json [--tier2 t2.json] --output report.md --format md|html
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# KWCAG 2.2 전체 33개 검사항목 정의 (Single Source of Truth)
# ---------------------------------------------------------------------------
KWCAG_REQUIREMENTS = [
    # 인식의 용이성 (9개)
    {"id": "5.1.1", "name": "적절한 대체 텍스트 제공", "principle": "인식의 용이성", "guideline": "대체 텍스트", "severity": "critical"},
    {"id": "5.2.1", "name": "자막 제공", "principle": "인식의 용이성", "guideline": "멀티미디어 대체수단", "severity": "major"},
    {"id": "5.3.1", "name": "표의 구성", "principle": "인식의 용이성", "guideline": "적응성", "severity": "major"},
    {"id": "5.3.2", "name": "콘텐츠의 선형구조", "principle": "인식의 용이성", "guideline": "적응성", "severity": "major"},
    {"id": "5.3.3", "name": "명확한 지시사항 제공", "principle": "인식의 용이성", "guideline": "적응성", "severity": "minor"},
    {"id": "5.4.1", "name": "색에 무관한 콘텐츠 인식", "principle": "인식의 용이성", "guideline": "명료성", "severity": "major"},
    {"id": "5.4.2", "name": "자동 재생 금지", "principle": "인식의 용이성", "guideline": "명료성", "severity": "critical"},
    {"id": "5.4.3", "name": "텍스트 콘텐츠의 명도 대비", "principle": "인식의 용이성", "guideline": "명료성", "severity": "major"},
    {"id": "5.4.4", "name": "콘텐츠 간의 구분", "principle": "인식의 용이성", "guideline": "명료성", "severity": "minor"},
    # 운용의 용이성 (15개)
    {"id": "6.1.1", "name": "키보드 사용 보장", "principle": "운용의 용이성", "guideline": "입력장치 접근성", "severity": "critical"},
    {"id": "6.1.2", "name": "초점 이동과 표시", "principle": "운용의 용이성", "guideline": "입력장치 접근성", "severity": "critical"},
    {"id": "6.1.3", "name": "조작 가능", "principle": "운용의 용이성", "guideline": "입력장치 접근성", "severity": "major"},
    {"id": "6.1.4", "name": "문자 단축키", "principle": "운용의 용이성", "guideline": "입력장치 접근성", "severity": "minor"},
    {"id": "6.2.1", "name": "응답시간 조절", "principle": "운용의 용이성", "guideline": "충분한 시간 제공", "severity": "major"},
    {"id": "6.2.2", "name": "정지 기능 제공", "principle": "운용의 용이성", "guideline": "충분한 시간 제공", "severity": "major"},
    {"id": "6.3.1", "name": "깜빡임과 번쩍임 사용 제한", "principle": "운용의 용이성", "guideline": "광과민성 발작 예방", "severity": "critical"},
    {"id": "6.4.1", "name": "반복 영역 건너뛰기", "principle": "운용의 용이성", "guideline": "쉬운 내비게이션", "severity": "major"},
    {"id": "6.4.2", "name": "제목 제공", "principle": "운용의 용이성", "guideline": "쉬운 내비게이션", "severity": "major"},
    {"id": "6.4.3", "name": "적절한 링크 텍스트", "principle": "운용의 용이성", "guideline": "쉬운 내비게이션", "severity": "major"},
    {"id": "6.4.4", "name": "고정된 참조 위치 정보", "principle": "운용의 용이성", "guideline": "쉬운 내비게이션", "severity": "minor"},
    {"id": "6.5.1", "name": "단일 포인터 입력 지원", "principle": "운용의 용이성", "guideline": "입력 방식", "severity": "major"},
    {"id": "6.5.2", "name": "포인터 입력 취소", "principle": "운용의 용이성", "guideline": "입력 방식", "severity": "major"},
    {"id": "6.5.3", "name": "레이블과 네임", "principle": "운용의 용이성", "guideline": "입력 방식", "severity": "major"},
    {"id": "6.5.4", "name": "동작기반 작동", "principle": "운용의 용이성", "guideline": "입력 방식", "severity": "major"},
    # 이해의 용이성 (7개)
    {"id": "7.1.1", "name": "기본 언어 표시", "principle": "이해의 용이성", "guideline": "가독성", "severity": "major"},
    {"id": "7.2.1", "name": "사용자 요구에 따른 실행", "principle": "이해의 용이성", "guideline": "예측 가능성", "severity": "major"},
    {"id": "7.2.2", "name": "찾기 쉬운 도움 정보", "principle": "이해의 용이성", "guideline": "예측 가능성", "severity": "minor"},
    {"id": "7.3.1", "name": "오류 정정", "principle": "이해의 용이성", "guideline": "입력 도움", "severity": "major"},
    {"id": "7.3.2", "name": "레이블 제공", "principle": "이해의 용이성", "guideline": "입력 도움", "severity": "critical"},
    {"id": "7.3.3", "name": "접근 가능한 인증", "principle": "이해의 용이성", "guideline": "입력 도움", "severity": "major"},
    {"id": "7.3.4", "name": "반복 입력 정보", "principle": "이해의 용이성", "guideline": "입력 도움", "severity": "minor"},
    # 견고성 (2개)
    {"id": "8.1.1", "name": "마크업 오류 방지", "principle": "견고성", "guideline": "문법 준수", "severity": "major"},
    {"id": "8.2.1", "name": "웹 애플리케이션 접근성 준수", "principle": "견고성", "guideline": "웹 애플리케이션 접근성", "severity": "critical"},
]

PRINCIPLES = ["인식의 용이성", "운용의 용이성", "이해의 용이성", "견고성"]

PRINCIPLE_ENGLISH = {
    "인식의 용이성": "Perceivable",
    "운용의 용이성": "Operable",
    "이해의 용이성": "Understandable",
    "견고성": "Robust",
}

PRINCIPLE_COUNTS = {
    "인식의 용이성": 9,
    "운용의 용이성": 15,
    "이해의 용이성": 7,
    "견고성": 2,
}

SEVERITY_ORDER = {"critical": 0, "major": 1, "minor": 2, "info": 3}
SEVERITY_LABELS = {
    "critical": "심각 (Critical)",
    "major": "주요 (Major)",
    "minor": "경미 (Minor)",
    "info": "참고 (Info)",
}

# 수동 검토 대상 항목 ID
MANUAL_CHECK_IDS = {"5.4.1", "6.2.1", "6.2.2", "6.3.1", "6.4.4", "6.5.1", "6.5.2", "6.5.4", "7.2.2"}

# ---------------------------------------------------------------------------
# 수동 검토 체크리스트 (인라인 -- references/manual-checklist-template.md 기반)
# ---------------------------------------------------------------------------
MANUAL_CHECKLIST = """
### 인식의 용이성

#### 5.4.1 색에 무관한 콘텐츠 인식

> 색상만으로 정보를 구분하지 않아야 합니다.

- [ ] 링크가 색상 외 밑줄/굵기/아이콘 등으로 구분됨
- [ ] 그래프/차트에서 색상 외 패턴/레이블로 데이터 구분
- [ ] 오류 메시지가 색상만이 아닌 텍스트/아이콘으로 표시
- [ ] 필수 입력 필드가 색상 외 별표(*)/텍스트로 표시
- [ ] 상태 표시(활성/비활성)가 색상 외 형태 변화 포함

### 운용의 용이성

#### 6.2.1 응답시간 조절

> 시간 제한이 있는 콘텐츠는 해제/연장/조절이 가능해야 합니다.

- [ ] 세션 만료 전 최소 20초 전에 경고 알림 제공
- [ ] 시간 연장 또는 해제 옵션이 존재
- [ ] 연장 요청을 최소 10회 이상 할 수 있음

#### 6.2.2 정지 기능 제공

> 자동으로 변경되는 콘텐츠는 정지/일시정지가 가능해야 합니다.

- [ ] 슬라이드/캐러셀에 정지 버튼 또는 이전/다음 컨트롤 제공
- [ ] 자동 갱신 콘텐츠에 정지 기능 제공
- [ ] 5초 이상 지속되는 움직이는 콘텐츠에 정지 가능
- [ ] 정지 후 사용자가 수동으로 재시작할 수 있음

#### 6.3.1 깜빡임과 번쩍임 사용 제한

> 초당 3~50회 깜빡이는 콘텐츠를 사용하지 않아야 합니다.

- [ ] 1초에 3회 이상 깜빡이는 콘텐츠 없음
- [ ] 번쩍이는 영역이 화면의 10% 미만
- [ ] `<blink>`, `<marquee>` 태그 미사용
- [ ] CSS animation으로 깜빡임 효과 미사용

#### 6.4.4 고정된 참조 위치 정보

> 사이트 내 페이지를 찾을 수 있는 수단을 2개 이상 제공해야 합니다.

- [ ] 사이트맵 또는 전체 메뉴 제공
- [ ] 검색 기능 제공
- [ ] 일관된 내비게이션 구조 유지
- [ ] 현재 위치 표시 (브레드크럼 등)

#### 6.5.1 단일 포인터 입력 지원

> 다중 포인터 제스처에 대한 단일 포인터 대안이 있어야 합니다.

- [ ] 핀치 줌 대신 버튼으로 확대/축소 가능
- [ ] 스와이프 대신 이전/다음 버튼 제공
- [ ] 멀티터치 제스처 없이도 모든 기능 사용 가능

#### 6.5.2 포인터 입력 취소

> 포인터 입력을 취소할 수 있어야 합니다.

- [ ] mousedown/touchstart에서 즉시 기능 실행하지 않음
- [ ] mouseup/touchend 또는 click 이벤트에서 실행
- [ ] 드래그 중 원래 위치로 복귀하면 취소됨

#### 6.5.4 동작기반 작동

> 기기의 움직임에 대한 대안 UI가 있어야 합니다.

- [ ] 기기 흔들기/기울이기 기능에 버튼 대안 제공
- [ ] 동작 기반 기능을 비활성화할 수 있음
- [ ] DeviceMotion/DeviceOrientation 미사용 또는 대안 존재

### 이해의 용이성

#### 7.2.2 찾기 쉬운 도움 정보

> 도움 정보가 각 페이지에서 동일한 위치에 제공되어야 합니다.

- [ ] 도움말/FAQ 링크가 모든 페이지에 존재
- [ ] 도움말 링크가 일관된 위치에 배치
- [ ] 고객센터 연락처가 제공됨
""".strip()


# ---------------------------------------------------------------------------
# JSON 로딩 -- 단일 파일 또는 배열 형식 모두 지원
# ---------------------------------------------------------------------------
def load_json(filepath):
    """JSON 파일을 읽어 결과 리스트로 반환한다.

    Tier 1 출력 형식: {"metadata": {...}, "files": [{"file": "...", "violations": [...]}]}
    Tier 2 출력 형식: {"file": "...", "violations": [...]} 또는 배열
    두 형식 모두 지원하여 [{"file": "...", "violations": [...]}] 형태로 정규화한다.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Tier 1 래핑 형식: {"metadata": {...}, "files": [...]}
    if isinstance(data, dict) and "files" in data:
        return data["files"]

    if isinstance(data, list):
        # 배열 내부에도 래핑 형식이 있을 수 있음
        normalized = []
        for item in data:
            if isinstance(item, dict) and "files" in item:
                normalized.extend(item["files"])
            else:
                normalized.append(item)
        return normalized

    return [data]


# ---------------------------------------------------------------------------
# 위반 사항 병합 및 중복 제거
# ---------------------------------------------------------------------------
def merge_violations(tier1_results, tier2_results):
    """
    Tier 1과 Tier 2 결과를 병합한다.
    같은 requirement_id + 같은 line(또는 element)이면 하나로 합치며, Tier 2를 우선한다.
    """
    all_violations = []
    target_files = set()
    tiers_used = set()

    for result_list, tier_label in [(tier1_results, 1), (tier2_results, 2)]:
        if not result_list:
            continue
        tiers_used.add(tier_label)
        for result in result_list:
            file_path = result.get("file", "")
            if file_path:
                target_files.add(file_path)
            for v in result.get("violations", []):
                violation = {
                    "requirement_id": v.get("requirement_id", ""),
                    "requirement_name": v.get("requirement_name", ""),
                    "principle": v.get("principle", ""),
                    "severity": v.get("severity", "info"),
                    "line": v.get("line", ""),
                    "element": v.get("element", ""),
                    "message": v.get("message", ""),
                    "fix": v.get("fix", v.get("message", "")),
                    "file": file_path,
                    "tier": tier_label,
                    "selector": v.get("selector", ""),
                    "axe_rule_id": v.get("axe_rule_id", ""),
                }
                all_violations.append(violation)

    deduplicated = _deduplicate(all_violations)
    return deduplicated, sorted(target_files), tiers_used


def _deduplicate(violations):
    """
    동일 requirement_id + 동일 위치(line 또는 element)의 위반을 중복 제거한다.
    Tier 2 데이터를 우선한다.
    """
    seen = {}

    # Tier 2를 먼저 처리하여 우선권 부여
    tier2_first = sorted(violations, key=lambda v: 0 if v.get("tier") == 2 else 1)

    for v in tier2_first:
        dedup_key = _make_dedup_key(v)
        if dedup_key not in seen:
            seen[dedup_key] = v

    return list(seen.values())


def _make_dedup_key(violation):
    """중복 판별 키를 생성한다."""
    req_id = violation.get("requirement_id", "")
    file_path = violation.get("file", "")
    line = str(violation.get("line", ""))
    # line이 있으면 requirement_id + file + line으로 식별
    if line and line != "":
        return f"{req_id}|{file_path}|{line}"
    # line이 없으면 element 텍스트의 앞 80자를 사용
    element = violation.get("element", "")[:80]
    return f"{req_id}|{file_path}|{element}"


# ---------------------------------------------------------------------------
# 통계 계산
# ---------------------------------------------------------------------------
def compute_statistics(violations):
    """원칙별, 심각도별 통계를 계산한다."""
    # 심각도별 집계
    severity_counts = {"critical": 0, "major": 0, "minor": 0, "info": 0}
    for v in violations:
        sev = v.get("severity", "info")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    # 요구사항별 위반 존재 여부
    violated_req_ids = {v["requirement_id"] for v in violations}

    # 원칙별 준수율 계산
    principle_stats = {}
    for principle in PRINCIPLES:
        reqs_in_principle = [r for r in KWCAG_REQUIREMENTS if r["principle"] == principle]
        total = len(reqs_in_principle)
        violated = sum(1 for r in reqs_in_principle if r["id"] in violated_req_ids)
        compliant = total - violated
        rate = (compliant / total * 100) if total > 0 else 100.0
        principle_stats[principle] = {
            "total": total,
            "compliant": compliant,
            "violated": violated,
            "rate": rate,
        }

    # 전체 합계
    total_all = sum(s["total"] for s in principle_stats.values())
    compliant_all = sum(s["compliant"] for s in principle_stats.values())
    violated_all = sum(s["violated"] for s in principle_stats.values())
    rate_all = (compliant_all / total_all * 100) if total_all > 0 else 100.0

    return {
        "severity_counts": severity_counts,
        "principle_stats": principle_stats,
        "totals": {
            "total": total_all,
            "compliant": compliant_all,
            "violated": violated_all,
            "rate": rate_all,
        },
    }


# ---------------------------------------------------------------------------
# 우선순위 권고 목록 생성
# ---------------------------------------------------------------------------
def build_priority_recommendations(violations):
    """심각도 순으로 정렬하고, 같은 심각도 내에서는 건수가 많은 것을 우선한다."""
    # requirement_id별 집계
    req_counts = {}
    for v in violations:
        req_id = v["requirement_id"]
        if req_id not in req_counts:
            req_counts[req_id] = {
                "requirement_id": req_id,
                "requirement_name": v.get("requirement_name", ""),
                "severity": v.get("severity", "info"),
                "count": 0,
                "example_fix": v.get("fix", v.get("message", "")),
            }
        req_counts[req_id]["count"] += 1

    items = list(req_counts.values())
    items.sort(key=lambda x: (SEVERITY_ORDER.get(x["severity"], 9), -x["count"]))
    return items


# ---------------------------------------------------------------------------
# Markdown 보고서 생성
# ---------------------------------------------------------------------------
def generate_markdown(violations, target_files, tiers_used, stats, priorities):
    """Markdown 형식의 보고서를 생성한다."""
    lines = []
    today = datetime.now().strftime("%Y-%m-%d")

    tier_label = _tier_label(tiers_used)
    files_display = ", ".join(target_files) if target_files else "(대상 없음)"

    # --- 헤더 ---
    lines.append("# KWCAG 2.2 웹 접근성 검사 보고서")
    lines.append("")

    # --- 검사 개요 ---
    lines.append("## 검사 개요")
    lines.append("")
    lines.append("| 항목 | 내용 |")
    lines.append("|------|------|")
    lines.append(f"| 검사 대상 | {files_display} |")
    lines.append(f"| 검사 일시 | {today} |")
    lines.append("| 검사 도구 | KWCAG A11y Checker v1.0 |")
    lines.append(f"| 검사 범위 | {tier_label} |")
    lines.append("")

    # --- 요약 ---
    lines.append("## 요약")
    lines.append("")

    # 준수율 테이블
    lines.append("### 준수율")
    lines.append("")
    lines.append("| 원칙 | 검사 항목 | 준수 | 미준수 | 준수율 |")
    lines.append("|------|----------|------|--------|-------|")

    for principle in PRINCIPLES:
        ps = stats["principle_stats"][principle]
        lines.append(
            f"| {principle} | {ps['total']} | {ps['compliant']} | {ps['violated']} | {ps['rate']:.1f}% |"
        )

    t = stats["totals"]
    lines.append(
        f"| **전체** | **{t['total']}** | **{t['compliant']}** | **{t['violated']}** | **{t['rate']:.1f}%** |"
    )
    lines.append("")

    # 심각도별 현황
    lines.append("### 심각도별 현황")
    lines.append("")
    lines.append("| 심각도 | 건수 |")
    lines.append("|--------|------|")
    for sev_key in ["critical", "major", "minor", "info"]:
        count = stats["severity_counts"].get(sev_key, 0)
        lines.append(f"| {SEVERITY_LABELS[sev_key]} | {count} |")
    lines.append("")

    # --- 상세 결과 ---
    lines.append("## 상세 결과")
    lines.append("")

    violated_req_ids = {v["requirement_id"] for v in violations}

    # 위반 사항을 requirement_id별로 그룹핑
    violations_by_req = {}
    for v in violations:
        req_id = v["requirement_id"]
        if req_id not in violations_by_req:
            violations_by_req[req_id] = []
        violations_by_req[req_id].append(v)

    for principle in PRINCIPLES:
        eng = PRINCIPLE_ENGLISH.get(principle, "")
        lines.append(f"### {principle} ({eng})")
        lines.append("")

        reqs_in_principle = [r for r in KWCAG_REQUIREMENTS if r["principle"] == principle]

        for req in reqs_in_principle:
            req_id = req["id"]
            req_name = req["name"]
            is_violated = req_id in violated_req_ids
            is_manual = req_id in MANUAL_CHECK_IDS

            if is_violated:
                req_violations = violations_by_req.get(req_id, [])
                sev = _highest_severity(req_violations)
                status = "미준수"
                sev_label = SEVERITY_LABELS.get(sev, sev)
                lines.append(f"#### {req_id} {req_name} -- {status} ({sev_label})")
                lines.append("")
                lines.append("| # | 파일 | 위치 | 요소 | 문제 | 수정 권고 |")
                lines.append("|---|------|------|------|------|----------|")

                for idx, v in enumerate(req_violations, 1):
                    file_col = _escape_md(v.get("file", ""))
                    line_col = f"line {v['line']}" if v.get("line") else v.get("selector", "-")
                    element_col = _truncate(_escape_md(v.get("element", "-")), 50)
                    message_col = _escape_md(v.get("message", ""))
                    fix_col = _escape_md(v.get("fix", v.get("message", "")))
                    lines.append(
                        f"| {idx} | {file_col} | {line_col} | `{element_col}` | {message_col} | {fix_col} |"
                    )

                lines.append("")
            elif is_manual:
                lines.append(f"#### {req_id} {req_name} -- 수동 검토 필요")
                lines.append("")
                lines.append("> 이 항목은 자동 검사가 불가능합니다. 아래 수동 검토 체크리스트를 참조하세요.")
                lines.append("")
            else:
                lines.append(f"#### {req_id} {req_name} -- 준수")
                lines.append("")
                lines.append("> 위반 없음")
                lines.append("")

    # --- 수동 검토 체크리스트 ---
    lines.append("## 수동 검토 체크리스트")
    lines.append("")
    lines.append("> 아래 9개 항목은 자동화 검사가 불가능합니다. 브라우저에서 직접 확인하세요.")
    lines.append("")
    lines.append(MANUAL_CHECKLIST)
    lines.append("")

    # --- 수정 우선순위 권고 ---
    lines.append("## 수정 우선순위 권고")
    lines.append("")

    if not priorities:
        lines.append("> 위반 사항이 없습니다.")
        lines.append("")
    else:
        priority_groups = {
            "critical": ("P1 -- 즉시 수정 (Critical)", []),
            "major": ("P2 -- 조기 수정 (Major)", []),
            "minor": ("P3 -- 개선 권고 (Minor)", []),
            "info": ("P4 -- 참고 (Info)", []),
        }
        for p in priorities:
            sev = p["severity"]
            if sev in priority_groups:
                priority_groups[sev][1].append(p)

        for sev_key in ["critical", "major", "minor", "info"]:
            title, items = priority_groups[sev_key]
            if items:
                lines.append(f"### {title}")
                lines.append("")
                for idx, item in enumerate(items, 1):
                    lines.append(
                        f"{idx}. **[{item['requirement_id']}] {item['requirement_name']}** "
                        f"({item['count']}건) -- {item['example_fix']}"
                    )
                lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# HTML 보고서 생성 (템플릿 기반)
# ---------------------------------------------------------------------------
def generate_html(violations, target_files, tiers_used, stats, priorities):
    """HTML 형식의 보고서를 생성한다. 템플릿 파일이 있으면 사용하고, 없으면 직접 생성한다."""
    template_path = Path(__file__).parent.parent / "assets" / "report-template.html"

    if template_path.exists():
        return _render_from_template(
            template_path, violations, target_files, tiers_used, stats, priorities
        )
    return _generate_html_inline(violations, target_files, tiers_used, stats, priorities)


def _render_from_template(template_path, violations, target_files, tiers_used, stats, priorities):
    """HTML 템플릿의 플레이스홀더를 치환하여 보고서를 생성한다."""
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    today = datetime.now().strftime("%Y-%m-%d")
    tier_label = _tier_label(tiers_used)
    files_display = ", ".join(target_files) if target_files else "(대상 없음)"

    replacements = {
        "{{TITLE}}": "KWCAG 2.2 웹 접근성 검사 보고서",
        "{{DATE}}": today,
        "{{TARGET}}": _escape_html(files_display),
        "{{TOOLS}}": f"KWCAG A11y Checker v1.0 | {tier_label}",
        "{{SUMMARY_TABLE}}": _html_summary_table(stats),
        "{{SEVERITY_TABLE}}": _html_severity_table(stats),
        "{{DETAIL_SECTIONS}}": _html_detail_sections(violations),
        "{{MANUAL_CHECKLIST}}": _html_manual_checklist(),
        "{{PRIORITY_SECTION}}": _html_priority_section(priorities),
    }

    result = template
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)

    return result


def _html_summary_table(stats):
    """준수율 요약 테이블 HTML을 생성한다."""
    rows = []
    for principle in PRINCIPLES:
        ps = stats["principle_stats"][principle]
        rate_class = _rate_class(ps["rate"])
        rows.append(
            f'<tr><td>{principle}</td><td>{ps["total"]}</td>'
            f'<td>{ps["compliant"]}</td><td>{ps["violated"]}</td>'
            f'<td class="{rate_class}">{ps["rate"]:.1f}%</td></tr>'
        )
    t = stats["totals"]
    rate_class = _rate_class(t["rate"])
    rows.append(
        f'<tr class="total-row"><td><strong>전체</strong></td>'
        f'<td><strong>{t["total"]}</strong></td>'
        f'<td><strong>{t["compliant"]}</strong></td>'
        f'<td><strong>{t["violated"]}</strong></td>'
        f'<td class="{rate_class}"><strong>{t["rate"]:.1f}%</strong></td></tr>'
    )
    return "\n".join(rows)


def _html_severity_table(stats):
    """심각도별 현황 테이블 HTML을 생성한다."""
    rows = []
    for sev_key in ["critical", "major", "minor", "info"]:
        count = stats["severity_counts"].get(sev_key, 0)
        badge = f'<span class="badge badge-{sev_key}">{SEVERITY_LABELS[sev_key]}</span>'
        rows.append(f"<tr><td>{badge}</td><td>{count}</td></tr>")
    return "\n".join(rows)


def _html_detail_sections(violations):
    """원칙별/항목별 상세 결과 HTML을 생성한다."""
    violated_req_ids = {v["requirement_id"] for v in violations}
    violations_by_req = {}
    for v in violations:
        req_id = v["requirement_id"]
        if req_id not in violations_by_req:
            violations_by_req[req_id] = []
        violations_by_req[req_id].append(v)

    sections = []

    for principle in PRINCIPLES:
        eng = PRINCIPLE_ENGLISH.get(principle, "")
        section_id = principle.replace(" ", "-")
        items_html = []

        reqs_in_principle = [r for r in KWCAG_REQUIREMENTS if r["principle"] == principle]

        for req in reqs_in_principle:
            req_id = req["id"]
            req_name = req["name"]
            is_violated = req_id in violated_req_ids
            is_manual = req_id in MANUAL_CHECK_IDS

            if is_violated:
                req_violations = violations_by_req.get(req_id, [])
                sev = _highest_severity(req_violations)
                badge = f'<span class="badge badge-{sev}">{SEVERITY_LABELS.get(sev, sev)}</span>'

                table_rows = []
                for idx, v in enumerate(req_violations, 1):
                    file_col = _escape_html(v.get("file", ""))
                    line_col = f"line {v['line']}" if v.get("line") else _escape_html(v.get("selector", "-"))
                    element_col = _escape_html(_truncate(v.get("element", "-"), 60))
                    message_col = _escape_html(v.get("message", ""))
                    fix_col = _escape_html(v.get("fix", v.get("message", "")))
                    table_rows.append(
                        f"<tr><td>{idx}</td><td>{file_col}</td><td>{line_col}</td>"
                        f"<td><code>{element_col}</code></td><td>{message_col}</td><td>{fix_col}</td></tr>"
                    )

                items_html.append(
                    f'<details open>'
                    f'<summary class="req-header violated">'
                    f'<span class="req-id">{req_id}</span> {req_name} '
                    f'{badge} <span class="count">({len(req_violations)}건)</span>'
                    f'</summary>'
                    f'<table class="detail-table">'
                    f'<thead><tr><th>#</th><th>파일</th><th>위치</th><th>요소</th><th>문제</th><th>수정 권고</th></tr></thead>'
                    f'<tbody>{"".join(table_rows)}</tbody>'
                    f'</table></details>'
                )
            elif is_manual:
                items_html.append(
                    f'<details>'
                    f'<summary class="req-header manual">'
                    f'<span class="req-id">{req_id}</span> {req_name} '
                    f'<span class="badge badge-info">수동 검토</span>'
                    f'</summary>'
                    f'<p class="manual-note">이 항목은 자동 검사가 불가능합니다. 수동 검토 체크리스트를 참조하세요.</p>'
                    f'</details>'
                )
            else:
                items_html.append(
                    f'<details>'
                    f'<summary class="req-header compliant">'
                    f'<span class="req-id">{req_id}</span> {req_name} '
                    f'<span class="badge badge-pass">준수</span>'
                    f'</summary>'
                    f'<p class="pass-note">위반 없음</p>'
                    f'</details>'
                )

        sections.append(
            f'<section class="principle-section" id="{section_id}">'
            f'<h3>{principle} ({eng})</h3>'
            f'{"".join(items_html)}'
            f'</section>'
        )

    return "\n".join(sections)


def _html_manual_checklist():
    """수동 검토 체크리스트를 HTML로 변환한다."""
    lines = MANUAL_CHECKLIST.split("\n")
    html_parts = []
    in_list = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("### "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h4>{_escape_html(stripped[4:])}</h4>")
        elif stripped.startswith("#### "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h5>{_escape_html(stripped[5:])}</h5>")
        elif stripped.startswith("> "):
            html_parts.append(f"<blockquote>{_escape_html(stripped[2:])}</blockquote>")
        elif stripped.startswith("- [ ] "):
            if not in_list:
                html_parts.append('<ul class="checklist">')
                in_list = True
            text = _escape_html(stripped[6:])
            html_parts.append(
                f'<li><label><input type="checkbox"> {text}</label></li>'
            )
        elif stripped == "":
            if in_list:
                html_parts.append("</ul>")
                in_list = False
        else:
            html_parts.append(f"<p>{_escape_html(stripped)}</p>")

    if in_list:
        html_parts.append("</ul>")

    return "\n".join(html_parts)


def _html_priority_section(priorities):
    """수정 우선순위 권고 HTML을 생성한다."""
    if not priorities:
        return "<p>위반 사항이 없습니다.</p>"

    priority_groups = {
        "critical": ("P1 -- 즉시 수정 (Critical)", "p1"),
        "major": ("P2 -- 조기 수정 (Major)", "p2"),
        "minor": ("P3 -- 개선 권고 (Minor)", "p3"),
        "info": ("P4 -- 참고 (Info)", "p4"),
    }

    parts = []
    for sev_key in ["critical", "major", "minor", "info"]:
        items = [p for p in priorities if p["severity"] == sev_key]
        if items:
            title, css_class = priority_groups[sev_key]
            list_items = []
            for item in items:
                list_items.append(
                    f'<li><strong>[{item["requirement_id"]}] '
                    f'{_escape_html(item["requirement_name"])}</strong> '
                    f'({item["count"]}건) -- {_escape_html(item["example_fix"])}</li>'
                )
            parts.append(
                f'<div class="priority-group {css_class}">'
                f"<h4>{title}</h4>"
                f'<ol>{"".join(list_items)}</ol>'
                f"</div>"
            )

    return "\n".join(parts)


def _generate_html_inline(violations, target_files, tiers_used, stats, priorities):
    """템플릿 없이 직접 HTML 보고서를 생성한다 (폴백)."""
    today = datetime.now().strftime("%Y-%m-%d")
    tier_label = _tier_label(tiers_used)
    files_display = ", ".join(target_files) if target_files else "(대상 없음)"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KWCAG 2.2 웹 접근성 검사 보고서</title>
<style>
body {{ font-family: 'Noto Sans KR', sans-serif; max-width: 960px; margin: 0 auto; padding: 20px; color: #333; }}
h1 {{ color: #1a365d; border-bottom: 3px solid #1a365d; padding-bottom: 12px; }}
h2 {{ color: #2c5282; margin-top: 2em; }}
table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #f7fafc; }}
.badge {{ padding: 2px 8px; border-radius: 4px; font-size: 0.85em; color: #fff; }}
.badge-critical {{ background: #e53e3e; }}
.badge-major {{ background: #dd6b20; }}
.badge-minor {{ background: #d69e2e; }}
.badge-info {{ background: #3182ce; }}
.badge-pass {{ background: #38a169; }}
</style>
</head>
<body>
<h1>KWCAG 2.2 웹 접근성 검사 보고서</h1>
<h2>검사 개요</h2>
<table>
<tr><td>검사 대상</td><td>{_escape_html(files_display)}</td></tr>
<tr><td>검사 일시</td><td>{today}</td></tr>
<tr><td>검사 도구</td><td>KWCAG A11y Checker v1.0</td></tr>
<tr><td>검사 범위</td><td>{tier_label}</td></tr>
</table>
<h2>요약</h2>
<h3>준수율</h3>
<table>
<thead><tr><th>원칙</th><th>검사 항목</th><th>준수</th><th>미준수</th><th>준수율</th></tr></thead>
<tbody>{_html_summary_table(stats)}</tbody>
</table>
<h3>심각도별 현황</h3>
<table>
<thead><tr><th>심각도</th><th>건수</th></tr></thead>
<tbody>{_html_severity_table(stats)}</tbody>
</table>
<h2>상세 결과</h2>
{_html_detail_sections(violations)}
<h2>수동 검토 체크리스트</h2>
{_html_manual_checklist()}
<h2>수정 우선순위 권고</h2>
{_html_priority_section(priorities)}
</body>
</html>"""


# ---------------------------------------------------------------------------
# 유틸리티 함수
# ---------------------------------------------------------------------------
def _tier_label(tiers_used):
    """사용된 Tier 목록에 따라 검사 범위 라벨을 생성한다."""
    parts = []
    if 1 in tiers_used:
        parts.append("Tier 1 정적 분석")
    if 2 in tiers_used:
        parts.append("Tier 2 axe-core")
    return " + ".join(parts) if parts else "알 수 없음"


def _highest_severity(violations):
    """위반 목록에서 가장 높은 심각도를 반환한다."""
    best = "info"
    for v in violations:
        sev = v.get("severity", "info")
        if SEVERITY_ORDER.get(sev, 9) < SEVERITY_ORDER.get(best, 9):
            best = sev
    return best


def _escape_md(text):
    """Markdown 특수 문자를 이스케이프한다."""
    if not text:
        return ""
    return str(text).replace("|", "\\|").replace("\n", " ").replace("\r", "")


def _escape_html(text):
    """HTML 특수 문자를 이스케이프한다."""
    if not text:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def _truncate(text, max_len):
    """텍스트를 최대 길이로 잘라낸다."""
    if not text or len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _rate_class(rate):
    """준수율에 따른 CSS 클래스를 반환한다."""
    if rate >= 90:
        return "rate-good"
    if rate >= 70:
        return "rate-warn"
    return "rate-bad"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args():
    """커맨드라인 인자를 파싱한다."""
    parser = argparse.ArgumentParser(
        description="KWCAG 2.2 통합 보고서 생성기 -- Tier 1/2 JSON 결과를 병합하여 보고서를 생성합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "사용 예시:\n"
            "  python kwcag-report-gen.py --tier1 t1.json --output report.md --format md\n"
            "  python kwcag-report-gen.py --tier1 t1.json --tier2 t2.json --output report.html --format html\n"
            "  python kwcag-report-gen.py --tier2 t2.json --output report.md\n"
        ),
    )
    parser.add_argument(
        "--tier1",
        type=str,
        default=None,
        help="Tier 1 정적 분석 결과 JSON 파일 경로",
    )
    parser.add_argument(
        "--tier2",
        type=str,
        default=None,
        help="Tier 2 axe-core 결과 JSON 파일 경로",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="출력 파일 경로 (예: report.md, report.html)",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["md", "html"],
        default="md",
        help="출력 형식 (기본: md)",
    )

    args = parser.parse_args()

    if args.tier1 is None and args.tier2 is None:
        parser.error("--tier1 또는 --tier2 중 하나 이상을 지정해야 합니다.")

    return args


def main():
    args = parse_args()

    # JSON 파일 로딩
    tier1_results = None
    tier2_results = None

    if args.tier1:
        if not os.path.exists(args.tier1):
            print(f"[오류] Tier 1 파일을 찾을 수 없습니다: {args.tier1}", file=sys.stderr)
            sys.exit(1)
        tier1_results = load_json(args.tier1)
        print(f"[정보] Tier 1 결과 로드: {args.tier1}", file=sys.stderr)

    if args.tier2:
        if not os.path.exists(args.tier2):
            print(f"[오류] Tier 2 파일을 찾을 수 없습니다: {args.tier2}", file=sys.stderr)
            sys.exit(1)
        tier2_results = load_json(args.tier2)
        print(f"[정보] Tier 2 결과 로드: {args.tier2}", file=sys.stderr)

    # 병합 및 중복 제거
    violations, target_files, tiers_used = merge_violations(tier1_results, tier2_results)
    print(f"[정보] 병합 완료: {len(violations)}건 위반 사항 (중복 제거 후)", file=sys.stderr)

    # 통계 계산
    stats = compute_statistics(violations)

    # 우선순위 권고
    priorities = build_priority_recommendations(violations)

    # 보고서 생성
    if args.format == "html":
        report = generate_html(violations, target_files, tiers_used, stats, priorities)
    else:
        report = generate_markdown(violations, target_files, tiers_used, stats, priorities)

    # 파일 출력
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"[완료] 보고서 생성: {args.output}", file=sys.stderr)

    # 위반 사항이 있으면 exit code 1
    total_violations = len(violations)
    sys.exit(1 if total_violations > 0 else 0)


if __name__ == "__main__":
    main()
