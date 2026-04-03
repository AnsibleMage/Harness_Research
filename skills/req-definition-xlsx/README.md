# req-definition-xlsx

마크다운 요구사항 정의서(`.md`)를 3시트 엑셀(`.xlsx`)로 자동 변환하는 Claude Code 스킬.

## 사용법

```
요구사항 정의서를 엑셀로 변환해줘
소스: path/to/요구사항_정의서.md
출력: path/to/output/
```

## 출력 구조

| 시트 | 내용 |
|------|------|
| 표지 | 사업명, 문서번호, 버전, 작성자 등 |
| 개정이력 | 버전 이력 19행 + 주석 |
| 세부요구사항 | 14컬럼 요구사항 전체 목록 |

---

## 스킬 작동 프로세스

### 전체 흐름

```
사용자 프롬프트 ("요구사항 엑셀", "md를 xlsx로" 등)
    │
    ▼
[트리거] req-definition-xlsx 스킬 자동 로드
    │
    ▼
[Phase 0] 환경 확인
    ├── openpyxl 설치 확인 (없으면 pip install)
    ├── source_md 파일 존재 확인
    └── output_dir 디렉토리 확인
    │
    ▼
[Phase 1] md 파싱
    ├── Step 1: Frontmatter(YAML) 파싱 → doc_id, title, project, version, created, author...
    ├── Step 2: 요구사항 분류 체계 추출 (### 4.X 패턴)
    └── Step 3: 개별 요구사항 파싱 (#### [ID] 패턴 → ID, 분류, 정의, 세부내용 추출)
    │
    ├── 30건 이하 → [단일 스크립트 모드] Phase 2로 직행
    └── 30건 초과 → [병렬 에이전트 모드] code_developer × 3 스폰
    │
    ▼
[Phase 2] 엑셀 생성
    │
    ├── Sheet 1: 표지 (templates/cover.py 참조)
    │   ├── A4 가로, 여백 L/R:0.7 T/B:0.75
    │   ├── 상단 Navy 바 → 기관명 → 제목(22pt) → 사업명(16pt) → 악센트 라인
    │   ├── 정보 테이블 7행 (문서번호/버전/작성일/작성자/검토자/승인자/보안등급)
    │   └── 날짜 → 하단 Navy 바
    │
    ├── Sheet 2: 개정이력 (templates/revision.py 참조)
    │   ├── A4 가로, 컬럼 A~G (7개)
    │   ├── "개 정 이 력" 제목 + 헤더 행
    │   ├── Row 3: 초기 데이터 (frontmatter에서 자동 채움)
    │   ├── Row 4~21: 빈 행 (No 2~19, 교대 줄무늬)
    │   └── Row 22~26: 주석 3항목
    │
    └── Sheet 3: 세부요구사항 (templates/detail.py 참조)
        ├── A4 가로, 컬럼 A~N (14개), freeze A2
        ├── 헤더: 번호 | 분류 | ID | 명칭 | 정의 | 세부내용 | 출처 | 기술현상 | 인터뷰 | 설계개발 | 비고 | 요구부서 | 수용여부 | 사유
        ├── 데이터 행: md에서 파싱한 요구사항 자동 채움 (A~G열)
        ├── H~N열: 빈칸 (추후 수동 입력용)
        ├── 행 높이: max(줄수 × 14, 30) 자동 계산
        └── 교대 줄무늬: 홀수=white, 짝수=light_gray
    │
    ▼
[Phase 3] 검증
    ├── 시트 수 == 3, 이름 [표지, 개정이력, 세부요구사항]
    ├── 모든 시트 landscape
    ├── 세부요구사항 행 수 == 파싱된 요구사항 건수
    ├── A~G열 필수값 누락 없음
    └── 요구사항 ID 중복 없음
    │
    ▼
[저장] safe_save() → 파일 잠금 시 temp 우회
    │
    ▼
[완료] .xlsx 파일 생성 + 검증 결과 보고
```

### Phase별 상세

#### Phase 0: 환경 확인

```python
# openpyxl 확인
python -c "import openpyxl; print(openpyxl.__version__)"
# 없으면 설치
pip install openpyxl
```

#### Phase 1: md 파싱 흐름

```
md 파일 읽기
    │
    ├── --- ~ --- 사이 → Frontmatter (YAML key:value)
    │
    ├── ### 4.X [분류명] → 분류 테이블 구성
    │   예: "### 4.1 유지관리수행 요구사항" → category = "유지관리수행"
    │
    └── #### [ID] [요구사항명] → 개별 요구사항 추출
        ├── | **요구사항 ID** | → ID
        ├── **정의**: → 정의 텍스트
        └── **세부 내용**: ~ **산출물**:/**변경 내역**: → 불릿 목록 추출
            └── 불릿 변환: "- 항목" → "* 항목", "  - 하위" → "  - 하위"
```

#### Phase 2: 엑셀 생성 분기

```
요구사항 건수 확인
    │
    ├── ≤ 30건: 단일 Python 스크립트
    │   └── Workbook() → 3시트 순차 생성 → save
    │
    └── > 30건: 병렬 에이전트
        ├── Agent A (code_developer): Sheet 1 표지 → temp_cover.xlsx
        ├── Agent B (code_developer): Sheet 2 개정이력 → temp_revision.xlsx
        └── Agent C (code_developer): Sheet 3 세부요구사항 → temp_detail.xlsx
            │
            └── 메인 세션: 3개 temp → 하나의 workbook으로 통합
```

#### Phase 3: 저장 + 파일 잠금 대응

```
wb.save(target_path)
    │
    ├── 성공 → 완료
    │
    └── PermissionError (파일이 엑셀에서 열려 있음)
        ├── Step 1: temp 디렉토리에 저장
        ├── Step 2: shutil.copy2(temp, target) 시도
        └── Step 3: 실패 시 → target_v2.xlsx로 대체 저장 + 사용자에게 안내
```

### 디자인 시스템

| 컬러 | HEX | 용도 |
|------|-----|------|
| Navy | #1B2A4A | 상/하단 바, 제목, 데이터 텍스트 |
| Accent Blue | #2E5090 | 헤더 배경, No 숫자, 라벨 |
| Light Gray | #F2F4F7 | 교대 행 배경 |
| Border Gray | #B0B8C4 | thin 테두리 |

폰트: 맑은 고딕 기본. 제목 22pt Bold, 헤더 9-10pt Bold White, 데이터 9pt, 장문 8.5pt.

---

## 폴더 구조

```
req-definition-xlsx/
├── SKILL.md                     # 스킬 정의 (트리거, 워크플로, 디자인)
├── SKILL_BUILD_README.md        # 생성 프로세스 + 유의사항 + 트러블슈팅
├── README.md                    # 이 파일 (사용법 + 작동 프로세스)
├── doc/                         # 참조 문서
│   ├── WORKLOG_정원도시서울.md    # 12세션 작업 로그
│   ├── SKILL_SPEC_*.md          # 스킬 스펙문서
│   ├── 31001_*.md / .xlsx       # 레퍼런스 파일
│   └── 01_002_*.md              # 문서 양식 표준
├── test/                        # 테스트 파일
├── xlsx/                        # 내장 xlsx 스킬 (글로벌 의존 X)
│   ├── SKILL.md, recalc.py, LICENSE.txt
├── templates/                   # 시트별 Python 생성 모듈
│   ├── common.py                # 컬러/폰트/테두리/safe_save/row_height
│   ├── cover.py                 # Sheet 1 표지
│   ├── revision.py              # Sheet 2 개정이력
│   └── detail.py                # Sheet 3 세부요구사항
└── parser/
    └── md_parser.py             # frontmatter + 요구사항 파싱
```

## 의존성

- Python 3.10+
- openpyxl 3.1+
- LibreOffice (선택 — 수식 사용 시트가 있을 때만)
