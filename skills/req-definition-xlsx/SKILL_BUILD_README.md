# 스킬 생성 리드미 — req-definition-xlsx

> **스킬명**: `req-definition-xlsx`
> **생성일**: 2026-03-16
> **생성 근거**: `doc/WORKLOG_정원도시서울.md` (12개 세션, 수동 작업 → 스킬 자동화)
> **목적**: 이 스킬을 재생성, 수정, 또는 유사 스킬을 만들 때 참고하는 문서

---

## 1. 생성 프로세스 전체 흐름

이 스킬은 **수동 작업 12세션**을 거쳐 패턴을 추출하고 자동화한 결과물이다.

```
[Phase A] 수동 작업으로 산출물 생성 (Session 001~007)
    │
    ▼
[Phase B] 스킬 스펙문서 작성 (Session 008~010)
    │
    ▼
[Phase C] /skill-creator로 스킬 생성 (Session 011)
    │
    ▼
[Phase D] 스킬 테스트 (Session 012)
```

### Phase A: 수동 작업 → 패턴 발견 (Session 001~007)

| Session | 작업 | 발견된 패턴 |
|---------|------|-----------|
| 001 | md 요구사항 정의서 생성 | 대용량 md 분할 읽기 + 병렬 에이전트 조합 패턴 |
| 002 | 이미지 삽입 | Grep→Read→Edit 위치 탐색 패턴 |
| 003 | 엑셀 표지 시트 | openpyxl 표지 레이아웃 + Navy 디자인 시스템 |
| 004 | 엑셀 개정이력 시트 | load_workbook + create_sheet 시트 추가 패턴 |
| 005 | 엑셀 세부요구사항 시트 | 14컬럼 구조 + PermissionError 우회 패턴 |
| 006~007 | 데이터 행 추가 | md→엑셀 데이터 매핑 + 교대 줄무늬 패턴 |

**핵심**: Session 003~007에서 시트를 하나씩 만들어보면서 디자인과 데이터 매핑 규칙이 확립되었다. 이 과정을 생략하고 바로 스킬을 만들면 디자인 품질이 떨어진다.

### Phase B: 스펙문서 작성 (Session 008~010)

| Session | 추가된 섹션 |
|---------|-----------|
| 008 | 12개 섹션 초안 (입출력, 디자인, 파싱, 워크플로, 검증) |
| 009 | xlsx 스킬 내장 정책 (글로벌 의존 제거) |
| 010 | /skill-creator 생성 절차 + 검증 체크리스트 |

### Phase C: 스킬 생성 (Session 011)

`/skill-creator` 스킬로 자동 생성. 실제로는 스펙문서를 읽고 파일을 하나씩 Write.

### Phase D: 테스트 (Session 012)

`_2.md` 파일로 MAR-005~008 4건 테스트. 3시트 정상 생성 확인.

---

## 2. 폴더 구조

```
req-definition-xlsx/
├── .claude/
│   └── settings.local.json      ← 자동승인 패턴
├── SKILL.md                     ← 메인 스킬 정의 (트리거, 워크플로, 디자인)
├── SKILL_BUILD_README.md        ← 이 파일 (생성 프로세스 문서)
├── README.md                    ← 사용법 요약
│
├── doc/                         ← 참조 문서 (스킬 로직의 근거)
│   ├── WORKLOG_정원도시서울.md    ← 12세션 작업 로그 (핵심 레퍼런스)
│   ├── SKILL_SPEC_*.md          ← 스킬 스펙문서 (12개 섹션)
│   ├── 31001_*.md               ← md 파싱 대상 레퍼런스
│   ├── 31001_*.xlsx             ← 디자인 레퍼런스
│   ├── 01_002_*.md              ← 문서 양식 표준
│   └── 2026_*복사원본.md         ← 원본 RFP
│
├── test/                        ← 테스트 파일
│   ├── 31001_*_2.md             ← 테스트용 md (축소판)
│   └── 31001_*_2.xlsx           ← 테스트 결과물
│
├── xlsx/                        ← 내장 xlsx 스킬 (글로벌 의존 X)
│   ├── SKILL.md                 ← xlsx 가이드라인
│   ├── recalc.py                ← 수식 재계산
│   └── LICENSE.txt
│
├── templates/                   ← 시트별 Python 생성 모듈
│   ├── __init__.py
│   ├── common.py                ← 컬러 7색, 폰트 14종, safe_save(), row_height_for_text()
│   ├── cover.py                 ← Sheet 1 표지
│   ├── revision.py              ← Sheet 2 개정이력
│   └── detail.py                ← Sheet 3 세부요구사항
│
└── parser/                      ← md 파싱 모듈
    ├── __init__.py
    └── md_parser.py             ← parse_frontmatter(), parse_requirements(), convert_bullet()
```

---

## 3. 생성 시 유의사항

### 3.1 디자인은 반드시 수동 검증 먼저

| 유의사항 | 상세 |
|---------|------|
| **시트별 1장씩 만들어서 확인** | Session 003~005처럼 표지→개정이력→세부요구사항 순서로 1시트씩 생성하고 사용자에게 엑셀을 열어보게 한 후 다음 시트 진행 |
| **컬럼 폭은 이미지로 조정** | 사용자가 엑셀 스크린샷을 보내면 그 비율에 맞춤 (Session 005: F열 42→75) |
| **행 높이도 이미지로 조정** | 텍스트가 잘리면 사용자가 알려줌 (Session 행 높이 조정) |
| **정렬은 마지막에 통일** | top/center 혼재 이슈 (Session: E,F 컬럼 정렬 수정) |

### 3.2 PermissionError 대응 (Windows 필수)

```
문제: 사용자가 엑셀에서 파일을 열어본 후 수정 요청 → PermissionError
해결: temp 경로 우회 패턴 (Session 005에서 발견)
```

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
        return alt
    return target_path
```

### 3.3 대용량 md 파일 처리

| 상황 | 대응 |
|------|------|
| 25,000 토큰 초과 | `Read`의 `offset`/`limit` 파라미터로 분할 읽기 |
| 요구사항 30건 초과 | 병렬 에이전트(code_developer × 3)로 분할 생성 |
| heredoc 한글 특수문자 | `<< 'EOF'` 내 `·` 등이 bash 파싱 에러 유발 → Write 도구로 .py 파일 생성 후 실행 |

### 3.4 md 파싱 엣지 케이스

| 케이스 | 대응 | 발견 세션 |
|--------|------|----------|
| 동일 ID가 2곳에 분리 기재 (MHR-001) | 합쳐서 하나의 요구사항으로 처리 | Session 001 |
| 분류명 오기 (PSR-006이 "유지관리수행"으로 표기) | 시리즈 접두어(PSR)에 맞게 교정 | Session 001 |
| 원문 건수 불일치 (60건 표기, 실제 59건) | 실제 파싱 건수 사용, 불일치 사항 보고 | Session 001 |
| 세부 내용 내 테이블 (MAR-006 상용SW 표) | 텍스트로 평탄화하여 단일 셀에 삽입 | Session 012 |
| 세부 내용 내 섹션 구분 ([공통사항], [정원도시]) | 그대로 유지하여 가독성 보존 | Session 012 |

### 3.5 xlsx 스킬 내장 원칙

```
글로벌 스킬 (~/.claude/skills/xlsx/)에 의존하면:
  - 배포 시 누락 위험
  - 글로벌 스킬 업데이트 시 호환성 깨질 수 있음

내장하면:
  - 독립 실행 보장
  - 버전 고정으로 안정성 확보
  - 3개 파일(SKILL.md, recalc.py, LICENSE.txt)만 복사하면 됨
```

---

## 4. 수정/확장 가이드

### 4.1 디자인 변경

`templates/common.py`의 상수만 수정:
- 컬러 변경: `NAVY`, `ACCENT_BLUE` 등 HEX 값
- 폰트 변경: `FONT_TITLE`, `FONT_DATA` 등 Font 객체
- 테두리 변경: `BORDER_THIN`, `BORDER_HEADER` 등

### 4.2 컬럼 추가/변경

`templates/detail.py`의 `COLUMNS` 리스트 수정:
```python
COLUMNS = [
    ("A", "번호", 5),
    ("B", "요구사항 분류", 12),
    # ... 여기에 추가/수정
]
```

### 4.3 새 시트 추가

1. `templates/` 에 새 파이썬 파일 생성 (예: `tracking.py`)
2. `SKILL.md`에 새 시트 사양 추가
3. 생성 스크립트에서 `wb.create_sheet()` 호출 추가

### 4.4 파싱 규칙 변경

`parser/md_parser.py`의 정규식 수정:
- 분류 패턴: `category_pattern = re.compile(r'^### 4\.\d+\s+(.+?)...')`
- 요구사항 패턴: `req_pattern = re.compile(r'^#### ([A-Z]+-\d+)\s+(.+)$')`
- 정의 패턴: `def_pattern = re.compile(r'^\*\*정의\*\*:\s*(.+)$')`

---

## 5. 테스트 방법

### 5.1 단위 테스트

```bash
# md 파서 테스트
python -c "
import sys; sys.path.insert(0, '<skill_dir>')
from parser.md_parser import parse_md_file
result = parse_md_file('test/31001_사용자_요구사항_정의서_2.md')
print(f'Frontmatter: {result[\"frontmatter\"][\"title\"]}')
print(f'Requirements: {result[\"total_count\"]}건')
for r in result['requirements']:
    print(f'  {r[\"id\"]}: {r[\"name\"]}')
"
```

### 5.2 통합 테스트

```
사용자 프롬프트: "요구사항 정의서를 엑셀로 변환해줘"
입력: test/31001_사용자_요구사항_정의서_2.md
기대: 3시트 xlsx, MAR-005~008 4건 데이터
```

### 5.3 검증 스크립트

```python
from openpyxl import load_workbook
wb = load_workbook('output.xlsx')
assert len(wb.sheetnames) == 3
assert wb.sheetnames == ['표지', '개정이력', '세부요구사항']
for ws in wb:
    assert ws.page_setup.orientation == 'landscape'
ws3 = wb['세부요구사항']
assert ws3.freeze_panes == 'A2'
# 요구사항 ID 중복 체크
ids = [ws3.cell(row=r, column=3).value for r in range(2, ws3.max_row+1) if ws3.cell(row=r,column=3).value]
assert len(ids) == len(set(ids))
```

---

## 6. 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `PermissionError` on save | 엑셀에서 파일 열려 있음 | `safe_save()` 패턴 사용 또는 사용자에게 닫기 요청 |
| `ModuleNotFoundError: openpyxl` | 미설치 | `pip install openpyxl` |
| bash heredoc 파싱 에러 | 한국어 특수문자(`·`) | Write로 .py 파일 생성 후 `python file.py` 실행 |
| 세부 내용 잘림 | 행 높이 부족 | `row_height_for_text()` 자동 계산 또는 수동 조정 |
| 터미널에서 한글 깨짐 | Windows 콘솔 인코딩 | 파일 내부는 정상. openpyxl verify로 확인 |
| frontmatter 파싱 실패 | YAML 형식 불일치 | `---` 구분자, `key: value` 형식 확인 |
| 분류명 비정상 | md의 `### 4.X` 패턴 불일치 | `parser/md_parser.py`의 `category_pattern` 정규식 확인 |

---

## 7. 세션별 핵심 교훈 요약

| Session | 교훈 |
|---------|------|
| 001 | 대용량 파일은 분할+병렬 에이전트로 처리. 원본 데이터의 오기/중복 항상 점검 |
| 002 | 이미지 삽입 위치는 Grep→Read→문맥 판단→Edit 패턴 |
| 003 | openpyxl 미설치 가능성. Phase 0에서 항상 확인 |
| 004 | 기존 xlsx에 시트 추가 시 `load_workbook` + `create_sheet` |
| 005 | **PermissionError는 반드시 발생한다고 가정하고 safe_save 내장** |
| 006~007 | 데이터 행 추가 시 교대 줄무늬(홀수=white, 짝수=gray) 규칙 준수 |
| 008 | 스펙문서는 디자인 시스템(컬러/폰트/테두리)까지 명시해야 재현 가능 |
| 009 | 글로벌 의존성은 내장으로 제거 — 배포 안정성 |
| 010 | 스킬 생성 절차는 스펙문서에 포함해야 재현 가능 |
| 011 | 스킬 파일 생성 순서: mkdir → cp(xlsx) → SKILL.md → templates → parser → settings |
| 012 | heredoc 한글 에러 → Write로 .py 생성 후 실행하는 우회 패턴 |

---

*스킬 생성 리드미 v1.0.0 — 2026-03-16*
