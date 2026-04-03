---
title: "{{TARGET}} 웹 취약점 요약 보고서"
version: "1.0.0"
created: "{{DATE}}"
updated: "{{DATE}}"
tags: [claude-code, web-vuln-scan, 보안점검, 시큐어코딩, {{LANG_TAGS}}]
status: completed
type: research
---

## Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed
- 마지막 작업: Tier 1 정적 분석 완료

### 다음 작업 (TODO)
{{TODO_LIST}}

### 작업 조언
> [!tip] 다음 Claude Code에게
> - 이 문서는 {{TARGET}} 프로젝트의 웹 취약점 Tier 1 정적 분석 요약 보고서
> - 건별 세부 코드는 디테일 보고서(`02_` 파일) 참조
> - 수정 작업 시 P1부터 순서대로 진행 권장
> - Tier 2 에이전트 심화 분석으로 오탐 검증 가능

---

# {{TARGET}} 웹 취약점 요약 보고서

## 개요

{{TARGET}} 프로젝트의 소스코드 보안 취약점을 행안부/KISA/OWASP 3축 기준으로 정적 분석한 요약 보고서.
종합등급, 유형별 현황, 수정 우선순위를 한눈에 보여준다.

## 본문

### 1. 점검 개요

| 항목 | 내용 |
|------|------|
| 점검 대상 | {{TARGET}} |
| 점검일시 | {{DATE}} |
| 점검도구 | Claude Code `/web-vuln-scan` v{{VERSION}} |
| 점검기준 | 행안부 SW보안약점 49개, OWASP Top 10, KISA 웹취약점 28개 |
| 점검범위 | {{SCOPE}} |
| 점검 Tier | {{TIERS}} |
| 종합 등급 | **{{GRADE}}** |

### 2. 종합 결과

| 심각도 | 건수 | 비율 | 상태 |
|--------|------|------|------|
| Critical | {{CRITICAL_COUNT}} | {{CRITICAL_PCT}}% | 즉시 조치 필요 |
| Major | {{MAJOR_COUNT}} | {{MAJOR_PCT}}% | 조기 조치 권고 |
| Minor | {{MINOR_COUNT}} | {{MINOR_PCT}}% | 개선 권고 |
| **합계** | **{{TOTAL_VULNS}}** | 100% | |

### 3. 유형별 현황

{{TYPE_TABLE}}

### 4. 영역별 현황

{{AREA_TABLE}}

### 5. 수정 우선순위

{{PRIORITY_TABLE}}

### 6. 수동 점검 체크리스트

{{MANUAL_CHECKLIST}}

## 관련 문서

### 직접 참조 (Direct Links)
- [[02_{{TARGET}}_웹취약점_디테일보고서_{{DATE_COMPACT}}|디테일 보고서]] — 건별 세부 코드 + 수정 예시
- [[remediation-guide|취약점 수정 가이드]] — 언어별 안전한 코드 예시
- [[mois-47-cwe-mapping|행안부 CWE 매핑]] — 점검 기준 참조

### 관련 주제 (Topic Links)
- [[severity-levels|심각도 분류 기준]] — Critical/Major/Minor/Info 판정 기준
- [[manual-checklist-template|수동 점검 체크리스트]] — Tier 1 미커버 항목

---

## Release Notes

### v1.0.0 ({{DATE}})
- 초기 작성: Tier 1 정적 분석 요약 보고서
> **프롬프트:** "{{ORIGINAL_PROMPT}}"
