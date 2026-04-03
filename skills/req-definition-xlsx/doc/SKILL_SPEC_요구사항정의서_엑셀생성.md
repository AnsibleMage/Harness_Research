# 스킬 스펙문서 — 요구사항 정의서 엑셀 생성기

> **스킬명**: `req-definition-xlsx`
> **버전**: 0.1.0 (스펙 초안)
> **작성일**: 2026-03-16
> **목적**: 마크다운 요구사항 정의서(`.md`)를 읽어 구조화된 엑셀 산출물(`.xlsx`)을 자동 생성
> **참조 산출물**: `3000_seoul_parks/31001_사용자_요구사항_정의서.md` → `.xlsx`
> **생성 도구**: `/skill-creator` 스킬 사용

---

## 1. 스킬 개요

### 1.1 문제 정의

서울시 정보화사업 산출물로 요구사항 정의서를 제출할 때:
1. 마크다운(`.md`)으로 요구사항을 구조화하여 작성
2. 이를 **엑셀(`.xlsx`)**로 변환하여 공식 산출물로 제출
3. 현재 이 과정이 수동 — 시트별로 하나씩 Python 스크립트를 작성하여 생성

### 1.2 해결 목표

**입력**: 구조화된 마크다운 요구사항 정의서 (`.md`)
**출력**: 3시트 엑셀 파일 (`.xlsx`) — 표지 + 개정이력 + 세부요구사항

### 1.3 트리거 조건

```
키워드: "요구사항 엑셀", "요구사항 xlsx", "산출물 엑셀 변환"
입력 파일: *요구사항*정의서*.md 패턴
```

---

## 2. 입력 사양

### 2.1 필수 입력

| 파라미터 | 타입 | 설명 | 예시 |
|---------|------|------|------|
| `source_md` | 파일 경로 | 마크다운 요구사항 정의서 | `31001_사용자_요구사항_정의서.md` |
| `output_dir` | 디렉토리 | 출력 폴더 | `3000_seoul_parks/` |

### 2.2 선택 입력

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|-------|------|
| `output_name` | 문자열 | source_md와 동일 (확장자만 .xlsx) | 출력 파일명 |
| `sheets` | 리스트 | `["표지", "개정이력", "세부요구사항"]` | 생성할 시트 목록 |
| `color_scheme` | 문자열 | `"navy"` | 컬러 테마 (`navy`, `green`, `custom`) |

---

## 3. 출력 사양 — 엑셀 3시트 구조

### 3.1 Sheet 1: 표지

| 항목 | 사양 |
|------|------|
| **페이지** | A4 가로 (landscape), 수평/수직 가운데 |
| **여백** | L/R: 0.7, T/B: 0.75 |
| **컬럼** | A~J (10컬럼), 중앙 C~H 활용 |
| **인쇄 영역** | A1:J25 |

**레이아웃**:

| 행 | 높이 | 내용 | 스타일 |
|----|------|------|--------|
| 2 | 6px | 상단 악센트 바 | Navy (#1B2A4A) 풀폭 |
| 4 | 18px | 기관명 (C~H 병합) | 회색 10pt |
| 8 | 50px | 문서 제목 (C~H 병합) | 맑은 고딕 22pt Bold Navy |
| 10 | 38px | 사업명 (C~H 병합) | 맑은 고딕 16pt Blue, 줄바꿈 |
| 12 | 3px | 악센트 라인 (D~G) | Blue (#2E5090) |
| 14~20 | 28px × 7행 | 정보 테이블 | 라벨: Blue배경/흰글씨, 값: 교대 줄무늬 |
| 22 | 18px | 날짜 (C~H 병합) | Blue Bold 13pt |
| 24 | 6px | 하단 악센트 바 | Navy (#1B2A4A) 풀폭 |

**데이터 추출 위치** (md → 엑셀 매핑):

| 엑셀 필드 | md 소스 |
|----------|---------|
| 문서 제목 | frontmatter `title` |
| 사업명 | frontmatter `project` |
| 문서번호 | frontmatter `doc_id` |
| 버전 | frontmatter `version` |
| 작성일 | frontmatter `created` |
| 작성자 | frontmatter `author` |
| 검토자 | frontmatter `reviewer` |
| 승인자 | frontmatter `approver` |
| 보안등급 | frontmatter `classification` |

### 3.2 Sheet 2: 개정이력

| 항목 | 사양 |
|------|------|
| **페이지** | A4 가로, 수평 가운데 |
| **여백** | L/R: 0.5, T: 0.6, B: 0.5 |
| **컬럼** | A~G (7컬럼) |
| **인쇄 영역** | A1:G26 |

**컬럼 구조**:

| 컬럼 | 헤더 | 폭 |
|------|------|-----|
| A | No | 5.5 |
| B | 버전 | 10 |
| C | 변경일 | 14 |
| D | 변경 사유 | 14 |
| E | 변경 내용 | 36 |
| F | 작성자 | 12 |
| G | 승인자 | 12 |

**고정 구조**:
- Row 1: "개 정 이 력" (A~G 병합, 18pt Bold Navy)
- Row 2: 헤더 (Blue 배경, 흰색 텍스트, 상하 medium 테두리)
- Row 3~21: 데이터 19행 (교대 줄무늬, No 1~19)
- Row 3: 초기 데이터 (1.0, 작성일, 신규, 최초 작성, 작성자)
- Row 22~26: 주석 3항목 (5줄, A~G 병합, 회색 8.5pt)

**데이터 추출**:
- Row 3 초기 데이터: frontmatter `version`, `created`, `author`에서 자동 채움
- 주석: 고정 텍스트 (버전 규칙, 변경 사유 규칙, 변경 내용 규칙)

### 3.3 Sheet 3: 세부요구사항

| 항목 | 사양 |
|------|------|
| **페이지** | A4 가로 |
| **여백** | L/R: 0.3, T/B: 0.4 |
| **컬럼** | A~N (14컬럼) |
| **헤더 고정** | freeze_panes = A2 |
| **필터** | 기본 비활성 (사용자가 필요 시 수동 활성화) |

**컬럼 구조**:

| 컬럼 | 헤더 | 폭 | 정렬 | 데이터 폰트 |
|------|------|-----|------|------------|
| A | 번호 | 5 | center | 9pt Bold Blue |
| B | 요구사항 분류 | 12 | left center | 9pt |
| C | 요구사항 ID | 11 | center | 9pt |
| D | 요구사항명 | 16 | left center | 9pt |
| E | 정의 | 18 | left top | 8.5pt |
| F | 세부 내용 | 75 | left top | 8.5pt |
| G | 출처 | 10 | center | 9pt |
| H | 기술현상 | 8 | center | 9pt |
| I | 인터뷰 | 8 | center | 9pt |
| J | 설계 및 개발 | 10 | center | 9pt |
| K | 비고 | 12 | center | 9pt |
| L | 요구부서 | 12 | center | 9pt |
| M | 수용 여부 | 6 | center | 9pt |
| N | 사유(수용불가/부분수용 시) | 20 | left center | 9pt |

**데이터 추출** (md → 엑셀 매핑):

| 엑셀 컬럼 | md 소스 위치 |
|----------|-------------|
| 번호 | 자동 순번 (1~N) |
| 요구사항 분류 | `#### [ID]` 상위의 `### 4.X` 섹션명에서 추출 |
| 요구사항 ID | `\| **요구사항 ID** \| [값]` |
| 요구사항명 | `\| **요구사항명** \| [값]` |
| 정의 | `**정의**: [값]` |
| 세부 내용 | `**세부 내용**:` 이후 `**산출물**:` 또는 `**변경 내역**:` 이전까지의 불릿 목록 |
| 출처 | 고정값 "제안요청서" (또는 사용자 지정) |
| H~N | 빈칸 (추후 수동 입력용) |

**행 높이 자동 계산**:
```
줄 수 = 세부 내용의 \n 개수 + 1
행 높이 = max(줄 수 × 14, 30)   # 최소 30px, 줄당 14px
```

**교대 줄무늬**: 홀수행 = white (#FFFFFF), 짝수행 = light_gray (#F2F4F7)

---

## 4. 디자인 시스템

### 4.1 컬러 팔레트 (Navy 테마)

| 이름 | HEX | 용도 |
|------|-----|------|
| **Navy** | #1B2A4A | 상/하단 바, 제목 텍스트, 데이터 텍스트 |
| **Accent Blue** | #2E5090 | 헤더 배경, No 숫자, 악센트 라인, 라벨 배경 |
| **Light Gray** | #F2F4F7 | 교대 행 배경 |
| **Mid Gray** | #D5D8DC | 테두리 |
| **Border Gray** | #B0B8C4 | thin 테두리 |
| **Note Gray** | #5A6270 | 주석 텍스트 |
| **White** | #FFFFFF | 기본 배경 |

### 4.2 폰트 시스템

| 용도 | 폰트 | 크기 | 굵기 | 색상 |
|------|------|------|------|------|
| 표지 제목 | 맑은 고딕 | 22pt | Bold | Navy |
| 표지 사업명 | 맑은 고딕 | 16pt | - | Blue |
| 시트 제목 | 맑은 고딕 | 18pt | Bold | Navy |
| 헤더 | 맑은 고딕 | 9~10pt | Bold | White |
| 데이터 일반 | 맑은 고딕 | 9pt | - | Navy |
| 데이터 장문 | 맑은 고딕 | 8.5pt | - | Navy |
| No 숫자 | 맑은 고딕 | 9pt | Bold | Blue |
| 주석 | 맑은 고딕 | 8.5pt | - | Note Gray |

### 4.3 테두리 시스템

| 용도 | 스타일 | 색상 |
|------|--------|------|
| 일반 셀 | thin | Border Gray (#B0B8C4) |
| 헤더 상하 | medium | Navy (#1B2A4A) |
| 헤더 좌우 | thin | Border Gray (#B0B8C4) |

---

## 5. 파싱 로직

### 5.1 md 파싱 흐름

```
[md 파일 읽기]
    │
    ├── Phase 1: Frontmatter 파싱 (YAML)
    │   → doc_id, title, project, version, created, author, ...
    │
    ├── Phase 2: 요구사항 분류 체계 파싱
    │   패턴: ### 4.X [분류명] 요구사항
    │   → 분류 목록 + 분류별 시작 위치
    │
    └── Phase 3: 개별 요구사항 파싱
        패턴: #### [ID] [요구사항명]
        → ID, 분류, 요구사항명, 정의, 세부 내용 추출
```

### 5.2 세부 내용 추출 규칙

```python
# 각 요구사항 블록에서:
state = "IDLE"
for line in block:
    if line.startswith("**세부 내용**:"):
        state = "DETAIL"
        continue
    if line.startswith("**산출물**:") or line.startswith("**변경 내역**:"):
        state = "IDLE"
        continue
    if state == "DETAIL":
        # 마크다운 불릿을 * 표기로 변환
        # "- " → "* ", "  - " → "  - " 유지
        detail_lines.append(convert_bullet(line))
```

### 5.3 불릿 변환 규칙

| md 원본 | 엑셀 셀 내 텍스트 |
|---------|-----------------|
| `- 항목` | `* 항목` |
| `  - 하위항목` | `  - 하위항목` |
| `    - 3뎁스` | `    · 3뎁스` |

---

## 6. 실행 워크플로

### 6.1 전체 흐름

```
[사용자 입력: source_md + output_dir]
    │
    ▼
Phase 0: 환경 확인
    ├── openpyxl 설치 확인/설치
    └── 출력 디렉토리 존재 확인
    │
    ▼
Phase 1: md 파싱 (메인 세션)
    ├── Frontmatter YAML 파싱
    ├── 요구사항 분류 체계 추출
    └── 개별 요구사항 59건 파싱 → 구조화 데이터
    │
    ▼
Phase 2: 엑셀 생성 (병렬 가능)
    ├── Agent A: Sheet 1 표지 생성
    ├── Agent B: Sheet 2 개정이력 생성
    └── Agent C: Sheet 3 세부요구사항 생성 (메인 작업)
    │
    ▼
Phase 3: 통합 + 검증
    ├── 3시트를 하나의 workbook에 통합
    ├── 셀 값 검증 (요구사항 건수, 헤더, 필수값)
    └── 파일 저장
```

### 6.2 에이전트 구성

| 에이전트 | subagent_type | 담당 | 병렬 여부 |
|---------|---------------|------|----------|
| **Parser** | `requirements_analyst` | md 파싱 → 구조화 데이터 JSON 생성 | 선행 (Phase 1) |
| **Cover Writer** | `code_developer` | Sheet 1 표지 생성 | Phase 2 병렬 |
| **Revision Writer** | `code_developer` | Sheet 2 개정이력 생성 | Phase 2 병렬 |
| **Detail Writer** | `code_developer` | Sheet 3 세부요구사항 생성 | Phase 2 병렬 |
| **Validator** | `quality_reviewer` | 최종 검증 | Phase 3 순차 |

### 6.3 병렬 실행 다이어그램

```
Phase 1 (순차):
    [Parser Agent] → parsed_data.json

Phase 2 (병렬):
    [Cover Writer]    ──→ temp_cover.xlsx
    [Revision Writer] ──→ temp_revision.xlsx    ← 모두 parsed_data.json 참조
    [Detail Writer]   ──→ temp_detail.xlsx

Phase 3 (순차):
    [메인 세션] 3개 temp → 하나의 workbook 통합 → 최종 .xlsx
    [Validator Agent] 검증 → 완료 보고
```

### 6.4 대안: 단일 스크립트 모드

요구사항 30건 이하의 소규모 프로젝트에서는 에이전트 분할 없이 **단일 Python 스크립트**로 처리:

```
[메인 세션]
    ├── md 파싱 (Python)
    ├── 3시트 생성 (openpyxl, 단일 스크립트)
    └── 검증 (Python)
```

**분기 기준**: 요구사항 30건 초과 → 병렬 에이전트, 30건 이하 → 단일 스크립트

---

## 7. 파일 잠금 대응

| 상황 | 감지 | 대응 |
|------|------|------|
| 엑셀에서 파일 열림 | `PermissionError` | temp 경로 우회: src→temp 복사 → temp에서 작업 → shutil.copy2로 복귀 |
| temp 복귀도 실패 | `PermissionError` on copy2 | `_v2.xlsx` 대체 파일명으로 저장 + 사용자에게 교체 안내 |

```python
import shutil, tempfile

def safe_save(wb, target_path):
    tmp = os.path.join(tempfile.gettempdir(), "req_def_temp.xlsx")
    wb.save(tmp)
    try:
        shutil.copy2(tmp, target_path)
    except PermissionError:
        alt = target_path.replace(".xlsx", "_v2.xlsx")
        shutil.copy2(tmp, alt)
        return alt  # 대체 경로 반환
    return target_path
```

---

## 8. 검증 체크리스트

### 8.1 구조 검증

| # | 항목 | 검증 방법 | 기대값 |
|---|------|---------|--------|
| 1 | 시트 수 | `len(wb.sheetnames)` | 3 |
| 2 | 시트 이름 | `wb.sheetnames` | [표지, 개정이력, 세부요구사항] |
| 3 | 페이지 설정 | 각 시트 `page_setup.orientation` | 전부 landscape |
| 4 | 세부요구사항 헤더 | Row 1 값 14개 | 번호~사유 |
| 5 | 세부요구사항 행 수 | `max_row - 1` | md의 요구사항 건수와 일치 |
| 6 | freeze panes | 세부요구사항 | A2 |

### 8.2 데이터 검증

| # | 항목 | 검증 방법 |
|---|------|---------|
| 1 | 요구사항 ID 중복 | C열 unique count == total count |
| 2 | 필수값 누락 | A~F열 빈칸 없음 (G 출처 포함) |
| 3 | 번호 연속성 | A열 1~N 연속 |
| 4 | 분류-ID 정합성 | MAR → 유지관리수행, SFR → 기능, ... |
| 5 | 표지-개정이력 일관성 | 표지 버전 == 개정이력 최신 버전 |

---

## 9. 확장 계획

### 9.1 Phase 2 확장 시트

| 시트 | 용도 | 우선순위 |
|------|------|---------|
| 요구사항 추적표 | ID별 설계→구현→시험 추적 | P1 |
| 요구사항 매트릭스 | 분류별 통계, 히트맵 | P2 |
| 인터뷰 기록 | 변경 내역 상세 | P3 |

### 9.2 다른 산출물 타입 지원

이 스킬의 파싱/생성 패턴을 재사용하여:
- `34001_기술검토서.md` → `.xlsx`
- `32001_현행시스템_분석서.md` → `.xlsx`
- 범용 `md-to-xlsx` 변환기로 확장 가능

---

## 10. 기술 의존성

| 패키지 | 버전 | 용도 |
|--------|------|------|
| `openpyxl` | 3.1+ | 엑셀 생성/편집 |
| `pyyaml` | 6.0+ | frontmatter 파싱 (선택) |
| Python | 3.10+ | 스크립트 실행 |

**LibreOffice**: 선택 (수식 사용 시트가 있을 때만 필요, 현재 스펙에는 수식 없음)

### 10.1 xlsx 스킬 내장 (MANDATORY)

> **원칙**: 글로벌 xlsx 스킬(`~/.claude/skills/xlsx/`)에 의존하지 않고, 스킬 폴더 내부에 xlsx 스킬을 내장한다. 이렇게 하면 스킬 배포 시 외부 의존성 없이 독립 실행 가능.

**내장 대상 파일** (소스: `3000_seoul_parks/xlsx/`):

| 파일 | 크기 | 용도 |
|------|------|------|
| `SKILL.md` | 10,632 bytes | xlsx 스킬 가이드라인 (Zero Formula Errors, 코드 스타일 등) |
| `recalc.py` | 6,408 bytes | LibreOffice 기반 수식 재계산 스크립트 |
| `LICENSE.txt` | 1,467 bytes | 라이선스 |

**스킬 폴더 구조**:

```
req-definition-xlsx/
├── .claude/
│   └── settings.local.json     ← 스킬 전용 자동승인 패턴
├── SKILL.md                    ← 메인 스킬 정의
├── xlsx/                       ← xlsx 스킬 내장 (글로벌 의존 제거)
│   ├── SKILL.md                ← xlsx 가이드라인
│   ├── recalc.py               ← 수식 재계산
│   └── LICENSE.txt             ← 라이선스
├── templates/                  ← 시트별 Python 템플릿
│   ├── cover.py                ← Sheet 1 표지 생성
│   ├── revision.py             ← Sheet 2 개정이력 생성
│   ├── detail.py               ← Sheet 3 세부요구사항 생성
│   └── common.py               ← 공통 스타일/컬러/폰트 정의
├── parser/                     ← md 파싱 모듈
│   └── md_parser.py            ← frontmatter + 요구사항 파싱
└── README.md                   ← 사용법
```

**SKILL.md 내 xlsx 참조 방식**:

```markdown
# 스킬 내부에 xlsx 가이드라인이 포함되어 있습니다.
# 엑셀 생성 시 아래 규칙을 따릅니다:
# - xlsx/SKILL.md 의 "Zero Formula Errors" 원칙 준수
# - 수식 사용 시 xlsx/recalc.py 로 검증
# - recalc.py 경로: {skill_dir}/xlsx/recalc.py
```

**스킬 생성 시 복사 명령**:

```bash
# 스킬 폴더 생성 후 xlsx 내장 파일 복사
cp -r "C:\Users\name\Documents\Obsidian Vault\3000_seoul_parks\xlsx" "{skill_dir}/xlsx/"
```

**recalc.py 호출 시 경로**:

```python
import os
skill_dir = os.path.dirname(os.path.abspath(__file__))
recalc_path = os.path.join(skill_dir, "xlsx", "recalc.py")
# 사용: subprocess.run(["python", recalc_path, output_file])
```

---

## 11. 참조 파일 목록

| 파일 | 역할 |
|------|------|
| `3000_seoul_parks/31001_사용자_요구사항_정의서.md` | 파싱 대상 레퍼런스 (2,246줄, 59건) |
| `3000_seoul_parks/31001_사용자_요구사항_정의서.xlsx` | 디자인 레퍼런스 (3시트, 현재 3행 데이터) |
| `3000_seoul_parks/WORKLOG_정원도시서울.md` | 작업 이력 (Session 001~007) |
| `3000_seoul_parks/01_002_Document_Template_Standard.md` | 문서 양식 표준 (frontmatter 필드 정의) |

---

## 12. 스킬 생성 절차

### 12.1 생성 도구

`/skill-creator` 스킬을 사용하여 이 스펙문서 기반으로 스킬을 생성한다.

### 12.2 생성 프롬프트

```
/skill-creator 로 req-definition-xlsx 스킬을 생성해줘.
스펙문서: C:\Users\name\Documents\Obsidian Vault\3000_seoul_parks\SKILL_SPEC_요구사항정의서_엑셀생성.md
```

### 12.3 생성 시 skill-creator에게 전달할 핵심 지시

1. **스킬명**: `req-definition-xlsx`
2. **트리거**: "요구사항 엑셀", "요구사항 xlsx", "산출물 엑셀 변환"
3. **스펙문서 전체를 SKILL.md에 반영** — 디자인 시스템, 파싱 로직, 워크플로 포함
4. **xlsx 스킬 내장**: `3000_seoul_parks/xlsx/` 폴더를 스킬 내 `xlsx/`로 복사
5. **참조 파일 4개를 컨텍스트로 제공**:
   - `31001_사용자_요구사항_정의서.md` (파싱 대상 레퍼런스)
   - `31001_사용자_요구사항_정의서.xlsx` (디자인 레퍼런스)
   - `WORKLOG_정원도시서울.md` (작업 이력, 의사결정 근거)
   - `01_002_Document_Template_Standard.md` (frontmatter 필드 정의)
6. **Python 템플릿 파일 생성**: `templates/cover.py`, `revision.py`, `detail.py`, `common.py`
7. **파서 모듈 생성**: `parser/md_parser.py`
8. **settings.local.json**: openpyxl 관련 Bash 명령 자동승인 패턴 등록

### 12.4 생성 후 검증

| # | 검증 항목 | 방법 |
|---|---------|------|
| 1 | 스킬 폴더 구조 | `ls -R` 으로 Section 10.1 트리와 일치 확인 |
| 2 | xlsx 내장 파일 | `xlsx/SKILL.md`, `xlsx/recalc.py`, `xlsx/LICENSE.txt` 존재 확인 |
| 3 | SKILL.md 트리거 | description에 트리거 키워드 포함 확인 |
| 4 | 테스트 실행 | `31001_사용자_요구사항_정의서.md`로 실제 xlsx 생성 테스트 |
| 5 | 생성된 xlsx | 3시트 구조, 59건 데이터, 디자인 일치 검증 |

### 12.5 예상 스킬 폴더 최종 구조

```
~/.claude/skills/req-definition-xlsx/
├── .claude/
│   └── settings.local.json
├── SKILL.md                    ← 메인 (이 스펙문서 내용 반영)
├── xlsx/                       ← 내장 xlsx 스킬
│   ├── SKILL.md
│   ├── recalc.py
│   └── LICENSE.txt
├── templates/
│   ├── common.py               ← 컬러/폰트/테두리 상수
│   ├── cover.py                ← Sheet 1 표지
│   ├── revision.py             ← Sheet 2 개정이력
│   └── detail.py               ← Sheet 3 세부요구사항
├── parser/
│   └── md_parser.py            ← frontmatter + 요구사항 파싱
└── README.md
```

---

*스킬 스펙문서 v0.1.0 — 2026-03-16*
