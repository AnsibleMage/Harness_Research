#!/usr/bin/env python3
"""
strip-metadata.py — Phase 간 메타정보 제거 스크립트

Plan → Execute, Execute → Verify 전환 시
산출물에서 "누가 만들었는지" 메타정보를 제거하여
컨텍스트 독립성을 보장합니다.

사용법:
  python strip-metadata.py <input_file> <output_file>
  python strip-metadata.py plan.md plan_clean.md
"""

import sys
import re
from pathlib import Path


def strip_plan_metadata(content: str) -> str:
    """Plan 문서에서 메타정보 제거 (Executor에게 전달 시)"""
    lines = content.split('\n')
    result = []
    skip_section = False

    # 제거 대상 섹션 헤더
    remove_headers = [
        '# 작성 과정', '## Planner의 생각', '## 분석 과정',
        '## 대안 검토 과정', '## 의사결정 근거', '# Decision Log',
        '## Why this approach', '## Alternatives considered'
    ]

    # 제거 대상 패턴
    remove_patterns = [
        r'^작성자:\s*',          # 작성자 정보
        r'^Planner:\s*',         # Planner 이름
        r'^Agent:\s*',           # Agent 이름
        r'^분석가:\s*',          # 분석가 이름
        r'^Created by:\s*',      # 영어 작성자
        r'^Author:\s*',          # 영어 작성자
        r'^<!-- .* 에이전트.*-->', # HTML 주석 내 에이전트 정보
    ]

    for line in lines:
        # 제거 섹션 시작
        if any(line.strip().startswith(h) for h in remove_headers):
            skip_section = True
            continue

        # 새 섹션 시작 시 제거 섹션 종료
        if skip_section and line.startswith('#') and not any(
            line.strip().startswith(h) for h in remove_headers
        ):
            skip_section = False

        if skip_section:
            continue

        # 패턴 매칭으로 라인 제거
        if any(re.match(p, line.strip()) for p in remove_patterns):
            continue

        result.append(line)

    return '\n'.join(result)


def strip_execute_metadata(content: str) -> str:
    """Execute 산출물에서 메타정보 제거 (Verifier에게 전달 시)"""
    lines = content.split('\n')
    result = []

    remove_patterns = [
        r'^구현자:\s*',          # 구현자 정보
        r'^Developer:\s*',       # 개발자 이름
        r'^Executor:\s*',        # Executor 이름
        r'^구현 시간:\s*',       # 시간 정보
        r'^<!-- .* 개발자.*-->', # HTML 주석
    ]

    remove_headers = [
        '## 구현 과정', '## 디버깅 기록', '## 시행착오',
        '## Implementation Notes', '## Debug Log'
    ]

    skip_section = False

    for line in lines:
        if any(line.strip().startswith(h) for h in remove_headers):
            skip_section = True
            continue

        if skip_section and line.startswith('#') and not any(
            line.strip().startswith(h) for h in remove_headers
        ):
            skip_section = False

        if skip_section:
            continue

        if any(re.match(p, line.strip()) for p in remove_patterns):
            continue

        result.append(line)

    return '\n'.join(result)


def main():
    if len(sys.argv) < 3:
        print("Usage: python strip-metadata.py <input_file> <output_file> [--phase plan|execute]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    phase = sys.argv[3] if len(sys.argv) > 3 else "--phase"
    phase_type = sys.argv[4] if len(sys.argv) > 4 else "plan"

    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)

    content = input_path.read_text(encoding='utf-8')

    if phase_type == "execute":
        cleaned = strip_execute_metadata(content)
    else:
        cleaned = strip_plan_metadata(content)

    output_path.write_text(cleaned, encoding='utf-8')
    print(f"Metadata stripped: {input_path} -> {output_path}")
    print(f"Original: {len(content)} chars, Cleaned: {len(cleaned)} chars")
    print(f"Removed: {len(content) - len(cleaned)} chars")


if __name__ == "__main__":
    main()
