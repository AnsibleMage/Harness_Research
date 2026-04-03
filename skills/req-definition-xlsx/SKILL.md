---
name: req-definition-xlsx
description: "마크다운(.md) 요구사항 정의서를 읽어 구조화된 엑셀(.xlsx) 산출물을 자동 생성합니다. 표지, 개정이력, 세부요구사항 3시트를 포함하며, 서울시 정보화사업 산출물 양식에 맞는 Navy/Blue 디자인을 적용합니다. 반드시 이 스킬을 사용해야 하는 경우: 사용자가 '요구사항 엑셀', '요구사항 xlsx', '산출물 엑셀 변환', '요구사항 정의서를 엑셀로', 'md를 xlsx로 변환', '요구사항 스프레드시트' 등을 언급하거나, *요구사항*정의서*.md 파일을 엑셀로 변환하려는 경우. 요구사항 관련 엑셀 산출물이 필요한 모든 상황에서 트리거됩니다."
---

# 요구사항 정의서 엑셀 생성기

마크다운 요구사항 정의서(`.md`)를 파싱하여 3시트 엑셀(`.xlsx`)을 자동 생성하는 스킬.

## 내장된 xlsx 가이드라인

이 스킬은 `xlsx/SKILL.md`에 엑셀 생성 가이드라인을 내장하고 있습니다.
엑셀 작업 시 해당 파일을 읽고 "Zero Formula Errors" 원칙을 준수하세요.
수식 사용 시 `xlsx/recalc.py`로 검증하세요.

## 워크플로

```
Phase 0: 환경 확인 → pip install openpyxl (없으면)
Phase 1: md 파싱 → parser/md_parser.py 참조하여 frontmatter + 요구사항 추출
Phase 2: 엑셀 생성 → templates/*.py 참조하여 3시트 생성
Phase 3: 검증 → 시트 수, 행 수, 필수값 확인
```

요구사항 30건 초과 시 Phase 2를 병렬 에이전트(code_developer × 3)로 분할 가능.
30건 이하면 단일 Python 스크립트로 처리.

## 입력

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `source_md` | O | 마크다운 요구사항 정의서 경로 |
| `output_dir` | O | 출력 폴더 |
| `output_name` | - | 출력 파일명 (기본: source_md와 동일, 확장자 .xlsx) |

## 출력: 엑셀 3시트

### Sheet 1: 표지

A4 가로, 여백 L/R:0.7 T/B:0.75, 컬럼 A~J(10개), 인쇄영역 A1:J25

frontmatter에서 추출하는 필드:
- `title` → 문서 제목 (Row 8, 22pt Bold Navy)
- `project` → 사업명 (Row 10, 16pt Blue)
- `doc_id` → 문서번호, `version` → 버전, `created` → 작성일
- `author` → 작성자, `reviewer` → 검토자, `approver` → 승인자
- `classification` → 보안등급

레이아웃: 상단 Navy 바 → 기관명 → 제목 → 사업명 → 악센트 라인 → 정보 테이블(7행) → 날짜 → 하단 Navy 바.
상세 구현은 `templates/cover.py` 참조.

### Sheet 2: 개정이력

A4 가로, 여백 L/R:0.5 T:0.6 B:0.5, 컬럼 A~G(7개), 인쇄영역 A1:G26

- Row 1: "개 정 이 력" 제목 (18pt Bold Navy, A~G 병합)
- Row 2: 헤더 [No|버전|변경일|변경 사유|변경 내용|작성자|승인자] (Blue 배경)
- Row 3: 초기 데이터 (frontmatter version/created/author에서 자동)
- Row 4~21: 빈 행 (No 2~19, 교대 줄무늬)
- Row 22~26: 주석 3항목 (버전 규칙, 변경 사유 규칙, 변경 내용 규칙)

상세 구현은 `templates/revision.py` 참조.

### Sheet 3: 세부요구사항

A4 가로, 여백 L/R:0.3 T/B:0.4, 컬럼 A~N(14개), freeze A2, 필터 비활성

14컬럼: 번호(5) | 요구사항분류(12) | 요구사항ID(11) | 요구사항명(16) | 정의(18) | 세부내용(75) | 출처(10) | 기술현상(8) | 인터뷰(8) | 설계및개발(10) | 비고(12) | 요구부서(12) | 수용여부(6) | 사유(20)

md 파싱으로 자동 채움: A~G열. H~N열은 빈칸(추후 수동 입력).
행 높이 자동: `max(줄수 × 14, 30)`. 교대 줄무늬: 홀수=white, 짝수=light_gray.

상세 구현은 `templates/detail.py` 참조.

## 디자인 시스템

### 컬러 (Navy 테마)

| 이름 | HEX | 용도 |
|------|-----|------|
| Navy | #1B2A4A | 상/하단 바, 제목, 데이터 텍스트 |
| Accent Blue | #2E5090 | 헤더 배경, No 숫자, 라벨 배경 |
| Light Gray | #F2F4F7 | 교대 행 배경 |
| Border Gray | #B0B8C4 | thin 테두리 |
| Note Gray | #5A6270 | 주석 텍스트 |

### 폰트

맑은 고딕 기본. 표지 제목 22pt Bold, 사업명 16pt, 시트 제목 18pt Bold, 헤더 9-10pt Bold White, 데이터 9pt, 장문 8.5pt, No 9pt Bold Blue.

### 테두리

일반 셀: thin Border Gray. 헤더 상하: medium Navy. 헤더 좌우: thin Border Gray.

## md 파싱 규칙

### Frontmatter (YAML)

```yaml
---
doc_id: "31001"
title: "사용자 요구사항 정의서"
project: "사업명"
version: "1.0.0"
created: "2026-03-16"
author: ""
reviewer: ""
approver: ""
classification: 일반
---
```

### 요구사항 추출

분류 패턴: `### 4.X [분류명]` → 해당 섹션의 모든 요구사항에 분류 할당
요구사항 패턴: `#### [ID] [요구사항명]`
정의 패턴: `**정의**: [텍스트]`
세부 내용: `**세부 내용**:` ~ `**산출물**:` 또는 `**변경 내역**:` 사이의 불릿 목록

불릿 변환: `- 항목` → `* 항목`, `  - 하위` → `  - 하위`, `    - 3뎁스` → `    · 3뎁스`

상세 파싱 로직은 `parser/md_parser.py` 참조.

## 파일 잠금 대응

Windows에서 엑셀이 파일을 열고 있으면 PermissionError 발생.
대응: temp 경로에 먼저 저장 → shutil.copy2로 원본 위치에 복사.
실패 시 `_v2.xlsx` 대체 파일명으로 저장.

`templates/common.py`의 `safe_save()` 함수 사용.

## 검증

생성 완료 후 반드시 검증:
1. 시트 수 == 3, 이름 [표지, 개정이력, 세부요구사항]
2. 모든 시트 landscape
3. 세부요구사항 행 수 == md의 요구사항 건수
4. A~G열 필수값 누락 없음
5. 요구사항 ID 중복 없음
