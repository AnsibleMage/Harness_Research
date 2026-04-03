---
title: "{{TARGET}} 웹 취약점 디테일 보고서"
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
- 마지막 작업: Tier 1 정적 분석 건별 디테일 보고서 생성

### 다음 작업 (TODO)
{{TODO_LIST}}

### 작업 조언
> [!tip] 다음 Claude Code에게
> - 이 문서는 건별 세부 코드가 포함된 개발자용 디테일 보고서
> - 각 건마다 취약 코드 + 수정 방안 + 안전한 코드 예시 포함
> - 요약 보고서(`01_` 파일)와 함께 사용
> - 오탐 후보 섹션을 먼저 확인하여 실제 수정 대상 선별

---

# {{TARGET}} 웹 취약점 디테일 보고서

## 개요

{{TARGET}} 프로젝트의 취약점 건별 세부 코드가 포함된 개발자용 보고서.
각 취약점의 위치, 취약 코드, 수정 방안, 안전한 코드 예시를 포함하여 보고 즉시 수정이 가능하도록 작성.

## 본문

### 1. 점검 요약

| 대상 | 점검일 | 등급 | 총 취약점 |
|------|--------|------|----------|
| {{TARGET}} | {{DATE}} | **{{GRADE}}** | **{{TOTAL_VULNS}}건** (Critical {{CRITICAL_COUNT}} / Major {{MAJOR_COUNT}} / Minor {{MINOR_COUNT}}) |

---

### 2. 취약점 건별 상세

{{DETAIL_ENTRIES}}

### 3. 취약점 요약 테이블

{{SUMMARY_TABLE}}

### 4. 오탐(False Positive) 후보

{{FALSE_POSITIVE_CANDIDATES}}

## 관련 문서

### 직접 참조 (Direct Links)
- [[01_{{TARGET}}_웹취약점_요약보고서_{{DATE_COMPACT}}|요약 보고서]] — 종합등급, 우선순위
- [[remediation-guide|취약점 수정 가이드]] — 언어별 안전한 코드 예시
- [[mois-47-cwe-mapping|행안부 CWE 매핑]] — MOIS-ID 참조

### 관련 주제 (Topic Links)
- [[owasp-top10-mapping|OWASP Top 10 역매핑]] — A03(Injection) 등
- [[kisa-15-checklist|KISA 28개 체크리스트]] — WV-ID 참조

---

## Release Notes

### v1.0.0 ({{DATE}})
- 초기 작성: Tier 1 정적 분석 건별 디테일 보고서
> **프롬프트:** "{{ORIGINAL_PROMPT}}"
