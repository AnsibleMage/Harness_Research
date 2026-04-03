# Plan: HTML→PPTX 변환 커스텀 스킬 생성 V2

> V2 변경점: 샌드위치 구조 + 엔진 내장 + 에이전트 4개로 단순화
> V2.1 추가: 생성 가이드 + 강제 실행 정책

---

## ⛔ 강제 실행 정책 (MANDATORY ENFORCEMENT)

> **이 섹션은 전체 계획서에서 가장 높은 우선순위를 가진다.**

### 정책 1: 완전 실행 원칙 (No Shortcuts)

```
┌─────────────────────────────────────────────────────────────────┐
│  🔴 절대 규칙: 모든 파일은 계획서에 정의된 전체 내용을 포함해야 한다  │
│                                                                 │
│  ❌ 금지 행위:                                                   │
│  - "간략히 작성", "요약하여 작성", "핵심만 작성" — 금지            │
│  - "나머지는 유사하게", "위와 같은 패턴으로" — 금지                │
│  - "TODO", "여기에 추가", "추후 작성" 플레이스홀더 — 금지          │
│  - 섹션 누락, 필드 누락, 스키마 필드 누락 — 금지                  │
│  - "충분하다"는 자의적 판단으로 내용 축소 — 금지                   │
│                                                                 │
│  ✅ 필수 행위:                                                   │
│  - 계획서의 모든 섹션을 빠짐없이 작성                             │
│  - JSON 스키마는 모든 필드를 포함                                 │
│  - 에이전트 .md는 모든 필수 섹션을 포함                           │
│  - 코드 블록은 실행 가능한 완전한 코드                            │
│  - 규칙/지시사항은 구체적 예시 포함                               │
└─────────────────────────────────────────────────────────────────┘
```

### 정책 2: 생성 순서 강제

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 (순서 변경 금지)
각 Phase 내 병렬 가능 항목은 병렬 실행 권장
단, Phase 경계를 넘는 선행 작업 없이 다음 Phase 진입 금지
```

### 정책 3: 파일별 완성도 체크리스트

모든 파일 생성 후 아래 체크리스트를 **반드시 확인**한다. 하나라도 미충족 시 파일 재작성.

| 파일 유형 | 필수 체크 항목 |
|----------|--------------|
| **SKILL.md** | ☐ YAML frontmatter 완전 ☐ 입력 가이드 텍스트 포함 ☐ 출력 경로 질문 포함 ☐ 파이프라인 흐름도 포함 ☐ Phase별 상세 설명 포함 ☐ 소통 규칙 포함 ☐ 에러 처리 규칙 포함 |
| **에이전트 .md** | ☐ YAML frontmatter 완전 ☐ 역할 섹션 ☐ 입력 파일 경로 명시 ☐ 수행 작업 단계별 서술 ☐ 출력 형식 + JSON 스키마 완전 ☐ 규칙/원칙 섹션 ☐ 에러 처리 섹션 ☐ 금지 사항 섹션 |
| **references/*.md** | ☐ 목적 설명 ☐ 규칙/패턴 전체 나열 ☐ 예시 코드 포함 ☐ 금지 사항 명시 |
| **scripts/*.py** | ☐ argparse CLI 인터페이스 ☐ 에러 핸들링 ☐ JSON 출력 ☐ 실행 가능한 완전한 코드 |

### 정책 4: 생성 중 참조 규칙

| 생성 대상 | 반드시 참조해야 하는 파일 |
|----------|----------------------|
| SKILL.md | `예시스킬/landing-page-generator-main/SKILL.md` (구조 패턴) |
| 에이전트 .md | `예시스킬/.../agents/01-intake.md` ~ `05-prompt-generator.md` (구조 패턴) |
| html2pptx 관련 | `engine/html2pptx.md` (규칙 원본, 복사 후 참조) |
| references/ | `engine/html2pptx.md` + PptxGenJS 공식 문서 (Context7) |
| scripts/ | `engine/html2pptx.js`, `engine/thumbnail.py` (인터페이스 확인) |

### 정책 5: 위반 시 처리

```
위반 감지 → 해당 파일 즉시 재작성 (수정이 아닌 전체 재작성)
2회 위반 → 사용자에게 보고 후 진행 방향 확인
체크리스트 미확인 → 파일 생성 미완료로 간주
```

## Context

**문제**: 공식 `/pptx` 스킬은 단일 오케스트레이터로, HTML→PPTX 변환 시 모든 단계를 순차 수행해야 하고 중간 데이터가 구조화되지 않아 에이전트 간 협업이 어렵다.

**목적**: `예시스킬/landing-page-generator-main/`의 아키텍처 패턴을 적용하여 **HTML→PPTX 변환 전용 스킬**을 만든다.

**핵심 설계 원칙**:
1. **샌드위치 구조** — 병렬 사전 작업 → 단독 변환 → 병렬 검증
2. **엔진 내장** — `/pptx` 스킬의 핵심 파일을 `engine/`에 복사하여 자체 완결
3. **JSON 기반 데이터 전달** — 에이전트 간 구조화된 중간산출물로 협업

---

## 디렉토리 구조

```
~/.claude/skills/html2pptx-converter/
├── PLAN.md                               # 이 계획서
├── SKILL.md                              # Leader 오케스트레이터 + 입력 가이드
├── agents/
│   ├── 01-spec-analyzer.md               # 입력 → 스펙 JSON
│   ├── 02-html-slide-builder.md          # 스펙 JSON → HTML 슬라이드
│   ├── 03-executor-validator.md          # 변환 실행 + 썸네일 검증
│   └── 04-iterative-fixer.md             # 반복 수정 루프
├── engine/                               # pptx 스킬 핵심 엔진 (내장)
│   ├── html2pptx.js                      # HTML→PPTX 변환 엔진
│   ├── html2pptx.md                      # 변환 규칙 원본
│   └── thumbnail.py                      # 썸네일 생성기
├── references/
│   ├── html2pptx-rules.md                # html2pptx 규칙 요약 (에이전트용)
│   ├── pptxgenjs-api-guide.md            # PptxGenJS API 레퍼런스
│   └── slide-design-patterns.md          # 디자인 패턴 모음
├── scripts/
│   ├── validate_html.py                  # HTML 사전 검증
│   └── compare_slides.py                 # 원본-결과 비교
└── output/                               # 자동 생성
```

**설치 경로**: `C:\Users\name\.claude\skills\html2pptx-converter\`

---

## 엔진 내장 전략

### engine/ — 공식 /pptx 스킬에서 복사하는 파일 3개

| 파일 | 원본 경로 | 역할 |
|------|----------|------|
| `engine/html2pptx.js` | `~/.claude/skills/pptx/scripts/html2pptx.js` | HTML→PPTX 변환 엔진 (PptxGenJS 기반) |
| `engine/html2pptx.md` | `~/.claude/skills/pptx/html2pptx.md` | HTML 작성 규칙 원본 문서 |
| `engine/thumbnail.py` | `~/.claude/skills/pptx/scripts/thumbnail.py` | PPTX→썸네일 생성 (Playwright 기반) |

**내장 장점**:
- 외부 스킬 경로에 종속되지 않음 → **자체 완결**
- 폴더 통째로 이동/배포 가능 → **이식성**
- `/pptx` 스킬 업데이트에 의도치 않게 영향받지 않음 → **안정성**
- `require('./engine/html2pptx.js')` 상대경로로 확실한 참조 → **호출 확실성**

**업데이트 방침**: 공식 스킬에 중요 업데이트가 있을 때 수동으로 `engine/` 파일 교체

---

## 입력/출력 파일 정의

### INPUT — 사용자 제공 파일 (4개)

스킬 시작 시 사용자에게 아래 4개 파일을 요청한다. **이 4개만 사용자가 제공하고, 나머지는 전부 스킬이 신규 생성한다.**

| # | 파일명 | 목적 |
|---|--------|------|
| 1 | `*.html` | **변환 대상 HTML 소스** — DOM 구조, CSS 스타일, 레이아웃, 색상, 타이포그래피를 파싱하여 PPTX로 재현하는 원본 |
| 2 | `*.png` | **시각 비교 참조 스크린샷** — PPTX 변환 후 썸네일과 비교하여 레이아웃/텍스트/색상 일치도를 검증하는 기준 이미지 |
| 3 | `*_description.md` | **페이지 기능 설명서** — 영역별 기능 설명, UI 구성, 연결 흐름. 에이전트가 각 영역의 목적을 이해하여 의미적으로 정확한 배치를 수행 |
| 4 | `*_fields.md` | **입력 항목 정의서** — UI 요소별 역할, 입력 형식, 상호작용 방식. 텍스트 콘텐츠 추출과 레이아웃 우선순위 결정에 활용 |

### OUTPUT 경로 정책

스킬 시작 시 사용자에게 출력 경로를 질문한다. 3가지 옵션 + 기본값:

| 옵션 | 경로 | 예시 |
|------|------|------|
| **a) 프로젝트 루트** (기본값) | `{CWD}/output/` | `C:\Users\name\Documents\project\output\` |
| **b) 입력 파일 옆** | `{INPUT_DIR}/output/` | `C:\...\Aitest\output\` |
| **c) 직접 지정** | 사용자 입력 경로 | `D:\presentations\output\` |

**구현 방식**:
- Leader가 `AskUserQuestion`으로 출력 경로를 질문
- 응답을 `OUTPUT_DIR` 변수로 저장하여 모든 Teammate에 전달
- 각 Teammate는 `output/` 대신 `{OUTPUT_DIR}/`을 사용
- 미응답 또는 "기본" 시 → 프로젝트 루트(`CWD`)에 `output/` 생성
- 경로가 존재하지 않으면 자동 생성 (`mkdir -p`)

### OUTPUT — 스킬이 신규 생성하는 파일

**모두 신규 생성**이며, 엔진 내부 임시 파일(Playwright 캐시 등)은 제외하고 사용자에게 의미 있는 파일만 `{OUTPUT_DIR}/`에 저장한다.

| Phase | 출력 파일 | 설명 | 생성 에이전트 |
|-------|----------|------|-------------|
| 1 | `{OUTPUT_DIR}/spec.json` | 구조화된 슬라이드 스펙 (레이아웃, 색상, 요소, 위치) | 01-spec-analyzer |
| 2 | `{OUTPUT_DIR}/slides/slide_00.html` ... | **html2pptx 규칙 준수 HTML 슬라이드** (신규 생성) | 02-html-slide-builder |
| 2 | `{OUTPUT_DIR}/html_validation.json` | HTML 사전 검증 결과 | validate_html.py |
| 3 | `{OUTPUT_DIR}/convert.js` | html2pptx.js를 사용하는 변환 스크립트 | 03-executor-validator |
| 3 | `{OUTPUT_DIR}/presentation.pptx` | **최종 PPTX 프레젠테이션** | 03-executor-validator |
| 3 | `{OUTPUT_DIR}/thumbnails.jpg` | PPTX 썸네일 (시각 검증용) | 03-executor-validator |
| 3 | `{OUTPUT_DIR}/validation.json` | 시각 검증 결과 (이슈 목록) | 03-executor-validator |
| 3 | `{OUTPUT_DIR}/comparison.jpg` | 원본 PNG vs 썸네일 나란히 비교 | compare_slides.py |
| 4 | `{OUTPUT_DIR}/presentation_final.pptx` | 수정 후 최종 PPTX (이슈 시만) | 04-iterative-fixer |
| 4 | `{OUTPUT_DIR}/fix_log.json` | 수정 이력 (이슈 시만) | 04-iterative-fixer |

> **핵심**: `{OUTPUT_DIR}/slides/slide_*.html`은 입력 HTML(원본 웹 페이지)과는 별개로, html2pptx 규칙에 맞춰 **새로 작성된** 슬라이드 HTML이다.

---

## SKILL.md 설계

```yaml
---
name: html2pptx-converter
description: |
  HTML을 PPTX 프레젠테이션으로 변환하는 스킬. 웹 디자인 시안, HTML 파일,
  또는 스크린샷을 입력받아 정확한 레이아웃의 PowerPoint 파일을 생성합니다.
  engine/ 폴더에 html2pptx 변환 엔진을 내장하여 자체 완결적으로 동작합니다.

  Use when: HTML→PPTX 변환, 웹디자인을 프레젠테이션으로, html2pptx 변환
model: opus
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---
```

### 입력 가이드 텍스트

```
📋 HTML→PPTX 변환을 시작합니다.

다음 4개 파일의 경로를 알려주세요:

1. HTML 소스 파일 (.html)
   → 변환할 웹 페이지 원본 코드

2. 스크린샷 파일 (.png)
   → HTML 렌더링 결과 이미지 (검증 비교용)

3. 페이지 기능 설명서 (.md)
   → 각 영역의 기능, UI 구성, 연결 흐름 설명

4. 입력 항목 정의서 (.md)
   → UI 요소별 역할, 입력 형식, 상호작용 정의

예시:
  - partnering_main_eng.html
  - partnering_main_eng.png
  - partnering_main_eng_description.md
  - partnering_main_eng_fields.md

📂 출력 경로를 선택해주세요:
  a) 프로젝트 폴더 루트 (현재 작업 디렉토리에 output/ 생성)
  b) 입력 파일과 같은 폴더 (입력 HTML이 있는 폴더에 output/ 생성)
  c) 직접 지정 (원하는 절대/상대 경로 입력)

미지정 시 기본값: 프로젝트 폴더 루트 (a)

4개 파일 + 출력 경로를 제공하면 자동으로 변환을 시작합니다.
```

---

## SKILL.md 상세 생성 가이드

> **참조 원본**: `예시스킬/landing-page-generator-main/SKILL.md`
> **강제 정책**: 아래 모든 섹션을 빠짐없이 작성해야 한다. 섹션 누락 = 미완성.

### SKILL.md 필수 구조 (12개 섹션)

```markdown
# ── 섹션 1: YAML Frontmatter ──
---
name: html2pptx-converter
description: |
  [스킬 설명 — 2~4줄, 기능, 용도, 엔진 설명 포함]
  Use when: [트리거 키워드 3개 이상]
model: opus
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# ── 섹션 2: 스킬 제목 + 개요 ──
# HTML→PPTX 변환기 (html2pptx-converter)
## 개요
[1~2줄 요약]

# ── 섹션 3: 입력 가이드 텍스트 ──
## 입력 가이드
[사용자에게 4개 파일 요청 + 출력 경로 선택 — 위에 정의된 전체 텍스트 포함]

# ── 섹션 4: 파이프라인 흐름도 ──
## 실행 흐름
[Phase 1~4 전체 ASCII 흐름도 — 위에 정의된 샌드위치 파이프라인 전체 포함]

# ── 섹션 5: Phase별 상세 설명 ──
## Phase 상세
### Phase 1: 병렬 사전 작업
[Teammate-A 역할, 입출력, Leader 검증 내용]
### Phase 2: 순차 HTML 생성
[Teammate-B 역할, 입출력, validate_html.py 연동]
### Phase 3: 단독 변환 + 검증
[Teammate-C 역할, convert.js 생성, node 실행, 썸네일, 비교]
### Phase 4: 조건부 수정
[Teammate-D 역할, 수정 루프, 조건 분기]

# ── 섹션 6: Teammate 배분 테이블 ──
## Teammate 배분
[Teammate A~D 테이블 — 에이전트, 모델, Phase, 입출력]

# ── 섹션 7: 소통 규칙 ──
## 소통 규칙
- Leader↔Teammate 간 소통 방식
- JSON 파일 기반 데이터 전달
- Teammate 간 직접 소통 금지
- Leader가 중간산출물 검증 후 다음 Teammate 투입

# ── 섹션 8: OUTPUT_DIR 처리 ──
## 출력 경로 처리
- AskUserQuestion으로 경로 질문
- OUTPUT_DIR 변수 저장 및 Teammate 전달 방법
- 기본값 처리 로직

# ── 섹션 9: 에러 처리 규칙 ──
## 에러 처리
[Phase별 에러 시나리오와 대응 방법]
- Phase 1 실패: 입력 파일 누락 → 재요청
- Phase 2 실패: HTML 검증 실패 → Teammate-B 재시도
- Phase 3 실패: node 실행 에러 → Teammate-C 에러 수정
- Phase 3 실패: 시각 검증 이슈 → Phase 4 진입
- Phase 4 실패: 3회 수정 후에도 미해결 → 사용자 보고

# ── 섹션 10: 참조 문서 링크 ──
## 참조 문서
- [html2pptx 규칙 요약](references/html2pptx-rules.md)
- [PptxGenJS API 가이드](references/pptxgenjs-api-guide.md)
- [슬라이드 디자인 패턴](references/slide-design-patterns.md)

# ── 섹션 11: 엔진 파일 설명 ──
## 내장 엔진
- engine/html2pptx.js — 변환 엔진
- engine/html2pptx.md — 변환 규칙 원본
- engine/thumbnail.py — 썸네일 생성기

# ── 섹션 12: 출력 파일 목록 ──
## 출력 파일
[OUTPUT 테이블 전체 — Phase, 파일명, 설명, 생성 에이전트]
```

### SKILL.md 금지 사항

- ❌ "상세 내용은 에이전트 참조" 같은 위임 문구 금지 — SKILL.md 자체가 완결적이어야 함
- ❌ Phase 흐름도에서 특정 Phase 생략 금지
- ❌ 에러 처리 섹션 누락 금지
- ❌ Teammate 배분 테이블 축약 금지

---

## 서브에이전트 .md 상세 생성 가이드

> **참조 원본**: `예시스킬/.../agents/01-intake.md` ~ `05-prompt-generator.md`
> **강제 정책**: 아래 템플릿의 모든 섹션을 빠짐없이 작성해야 한다.

### 에이전트 .md 필수 구조 (10개 섹션)

```markdown
# ── 섹션 1: YAML Frontmatter ──
---
name: [에이전트 이름, kebab-case]
description: [1줄 설명 — 무엇을 입력받아 무엇을 출력하는지]
model: opus
tools: [사용하는 도구 목록]
---

# ── 섹션 2: 에이전트 제목 + 역할 ──
# [한글 이름] ([영문 이름])
## 역할
[2~3줄로 이 에이전트의 핵심 역할 서술]

# ── 섹션 3: 입력 ──
## 입력
- `{OUTPUT_DIR}/파일명` (이전 에이전트 출력)
- `engine/파일명` (엔진 파일)
- `references/파일명` (참조 문서)
[모든 입력 파일을 절대/상대 경로로 명시. "등" 사용 금지]

# ── 섹션 4: 수행 작업 (단계별) ──
## 수행 작업
### Step 1: [단계명]
[구체적 작업 내용 — 무엇을 읽고, 무엇을 분석하고, 무엇을 생성하는지]

### Step 2: [단계명]
[구체적 작업 내용]

### Step N: [단계명]
[구체적 작업 내용]

※ 각 Step은 반드시 아래를 포함:
- 작업 내용 (무엇을 하는가)
- 사용 도구 (Read/Write/Bash 등)
- 입력 데이터 (무엇을 읽는가)
- 출력 데이터 (무엇을 생성하는가)
- 성공 조건 (어떻게 되면 성공인가)

# ── 섹션 5: 출력 형식 ──
## 출력 형식
`{OUTPUT_DIR}/파일명` 파일 생성:
```json
{
  [전체 JSON 스키마 — 모든 필드, 타입, 예시값 포함]
  [축약 금지 — "..." 사용 금지, 모든 필드 나열]
}
```

# ── 섹션 6: 핵심 규칙 ──
## 핵심 규칙
1. [규칙 1 — 구체적, 검증 가능한 문장]
2. [규칙 2]
...
[최소 5개 이상의 구체적 규칙]

# ── 섹션 7: 금지 사항 ──
## 금지 사항
- ❌ [금지 1 — 구체적 행위]
- ❌ [금지 2]
...
[최소 3개 이상]

# ── 섹션 8: 에러 처리 ──
## 에러 처리
| 에러 상황 | 대응 방법 |
|----------|----------|
| [상황 1] | [대응 1] |
| [상황 2] | [대응 2] |
[이 에이전트에서 발생 가능한 모든 에러 시나리오]

# ── 섹션 9: 검증 체크리스트 ──
## 완료 전 체크리스트
- [ ] 출력 파일이 {OUTPUT_DIR}에 존재하는가
- [ ] JSON 스키마가 정의와 일치하는가
- [ ] [에이전트별 추가 검증 항목]

# ── 섹션 10: 참조 ──
## 참조
- [이 에이전트가 읽어야 하는 참조 문서 목록]
- [engine/ 파일 중 관련 파일]
```

### 에이전트별 최소 분량 기준

| 에이전트 | 최소 Step 수 | 최소 규칙 수 | 최소 금지 수 | 최소 에러 시나리오 |
|---------|-------------|-------------|-------------|-----------------|
| 01-spec-analyzer | 6 | 7 | 4 | 4 |
| 02-html-slide-builder | 5 | 10 (html2pptx 규칙 전체) | 6 | 5 |
| 03-executor-validator | 6 | 6 | 4 | 5 |
| 04-iterative-fixer | 4 | 5 | 3 | 3 |

### 에이전트별 특수 요구사항

#### 01-spec-analyzer.md 추가 요구사항
- Step에 **DOM 파싱 구체적 방법** 포함 (CSS 선택자, 정규식 등)
- **색상 추출** 방법 명시 (인라인 스타일, CSS 클래스, computed style)
- **레이아웃 매핑** 로직 명시 (flex? grid? absolute? → 슬라이드 좌표 변환)
- 출력 JSON에 `spec.json` 전체 스키마 (presentation, design, slides 모든 필드)

#### 02-html-slide-builder.md 추가 요구사항
- **html2pptx 규칙 전체**를 "핵심 규칙" 섹션에 포함 (engine/html2pptx.md 기반)
- 규칙별 **올바른 예시 코드**와 **잘못된 예시 코드** 병기
- `validate_html.py` 연동 방법 명시 (Bash 실행 → JSON 파싱 → 에러 시 수정)
- `<body>` 치수, `display:flex`, 텍스트 태그, gradient 금지 등 **모든 규칙 나열**

#### 03-executor-validator.md 추가 요구사항
- `convert.js` 생성 시 **완전한 코드 템플릿** 포함 (require 경로, 슬라이드 로드, 변환 호출)
- `node convert.js` 실행 시 **예상 출력**과 **에러 패턴** 명시
- `engine/thumbnail.py` 실행 커맨드와 **인자 형식** 명시
- `scripts/compare_slides.py` 실행 커맨드와 **인자 형식** 명시
- **시각 검사 기준** 명시 (텍스트 잘림, 겹침, 위치 이탈, 색상 불일치 판단 기준)

#### 04-iterative-fixer.md 추가 요구사항
- **수정 루프 흐름도** 포함 (최대 3회)
- 이슈 유형별 **수정 전략** 명시 (text_cutoff → 폰트 축소? 영역 확장?)
- **종료 조건** 명시 (이슈 0개, 또는 severity:high 0개, 또는 3회 도달)
- `fix_log.json` 스키마에 **수정 전/후 diff** 포함

### 에이전트 .md 금지 사항

- ❌ "위와 유사하게 작성" — 각 에이전트는 독립적으로 완결적이어야 함
- ❌ "spec.json 참조" 같은 위임 — JSON 스키마를 에이전트 내에서도 재명시
- ❌ Step 내용을 1줄로 축약 — 각 Step은 최소 3줄 이상
- ❌ 에러 처리 테이블 누락 — 모든 에이전트에 필수
- ❌ 검증 체크리스트 누락 — 모든 에이전트에 필수
- ❌ "등", "...", "기타" 같은 생략 표현 — 모든 항목을 명시적으로 나열

---

## 샌드위치 파이프라인

> **핵심 아이디어**: 사전 작업과 사후 검증은 병렬, 실제 변환은 단독 실행

```
━━━ Phase 1: 병렬 사전 작업 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ├── Teammate-A (01-spec-analyzer):
  │     HTML + 설명서 + 항목정의서 + PNG
  │     → output/spec.json (DOM 분석, 색상/폰트/레이아웃 추출)
  │
  └── Leader: 입력 파일 무결성 검증 (4개 파일 존재 + 형식 확인)

━━━ Phase 2: 순차 HTML 생성 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  → Teammate-B (02-html-slide-builder):
      spec.json + engine/html2pptx.md(규칙) + references/
      → output/slides/slide_*.html (html2pptx 규칙 준수)
      → validate_html.py 실행 → output/html_validation.json
      ※ 검증 실패 시 즉시 HTML 수정 후 재검증

━━━ Phase 3: 단독 변환 + 검증 ━━━━━━━━━━━━━━━━━━━━━━━━━━
  → Teammate-C (03-executor-validator):
      slides/*.html + engine/html2pptx.js
      → output/convert.js 생성 (require('./engine/html2pptx.js'))
      → node convert.js 실행 → output/presentation.pptx
      → python engine/thumbnail.py → output/thumbnails.jpg
      → 썸네일 시각 검사 → output/validation.json
      → python scripts/compare_slides.py → output/comparison.jpg

━━━ Phase 4: 조건부 수정 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  → (validation.json에 이슈가 있을 때만)
  → Teammate-D (04-iterative-fixer):
      validation.json + slides/*.html
      → HTML 수정 → node 재실행 → 재검증 (최대 3회)
      → output/presentation_final.pptx + output/fix_log.json
```

### 병렬 구간 정리

| 구간 | 병렬 내용 | 근거 |
|------|----------|------|
| Phase 1 | spec-analyzer ∥ Leader 검증 | 입력 파일을 각각 독립적으로 처리 |
| Phase 2 | 순차 (spec.json에 의존) | — |
| Phase 3 | 순차 (slides에 의존) | — |
| Phase 4 | 조건부 (이슈 없으면 스킵) | — |

---

## Team Agents 구조

### Leader 에이전트 (SKILL.md = 메인 세션)

**역할**: 전체 파이프라인 조율, Teammate 생성/관리, 결과 통합

**책임**:
1. 입력 가이드 텍스트 출력 → 4개 파일 수신 대기
2. 파일 수신 후 무결성 검증 (HTML 존재, PNG 존재, MD 2개 존재)
3. Phase별 Teammate 생성 + 작업 배분
4. Teammate 결과 수신 → 다음 단계 Teammate에 전달
5. 최종 PPTX 완성 보고

**소통 규칙**:
- 모든 Teammate는 Leader에게만 보고
- Teammate 간 직접 소통 금지 → JSON 파일로 데이터 전달
- Leader가 JSON 중간산출물 검증 후 다음 Teammate 투입

### Teammate 배분

| Teammate | 에이전트 | 모델 | Phase | 입력 (READ) | 출력 (WRITE → output/) |
|----------|---------|------|-------|-------------|----------------------|
| A | 01-spec-analyzer | **opus** | 1 병렬 | INPUT 4개 파일 | `spec.json` |
| B | 02-html-slide-builder | **opus** | 2 순차 | `spec.json` + `engine/html2pptx.md` + `references/` | `slides/slide_*.html` + `html_validation.json` |
| C | 03-executor-validator | **opus** | 3 순차 | `slides/*.html` + `engine/html2pptx.js` + `engine/thumbnail.py` + INPUT PNG | `convert.js` + `presentation.pptx` + `thumbnails.jpg` + `validation.json` + `comparison.jpg` |
| D | 04-iterative-fixer | **opus** | 4 조건부 | `validation.json` + `slides/*.html` + `engine/*` | `presentation_final.pptx` + `fix_log.json` |

---

## 서브에이전트 설계

### 01-spec-analyzer.md

```yaml
---
name: spec-analyzer
description: HTML, 스크린샷, 기능설명서, 항목정의서를 분석하여 구조화된 슬라이드 스펙 JSON을 생성합니다.
model: opus
tools: [Read, Write, Glob, Grep, Bash]
---
```

**입력**: HTML 파일 + description.md + fields.md + PNG(참조)
**출력**: `output/spec.json`

**수행 작업**:
1. HTML 파일의 DOM 구조 분석 — 섹션/영역 식별
2. CSS에서 색상 팔레트, 폰트, 간격 추출
3. PNG 스크린샷과 대조하여 시각적 레이아웃 확인
4. description.md 기반으로 각 영역의 의미/목적 매핑
5. fields.md 기반으로 텍스트 콘텐츠와 UI 요소 우선순위 결정
6. 모든 정보를 spec.json 스키마에 맞춰 구조화

### 02-html-slide-builder.md

```yaml
---
name: html-slide-builder
description: 스펙 JSON을 기반으로 html2pptx 규칙을 준수하는 HTML 슬라이드 파일을 생성합니다.
model: opus
tools: [Read, Write, Glob, Bash]
---
```

**입력**: `output/spec.json` + `engine/html2pptx.md` + `references/`
**출력**: `output/slides/slide_00.html`, ...

**필수 규칙** (engine/html2pptx.md 기반):
- `<body>` 치수 필수 (`width`, `height` 인라인 스타일)
- `display: flex` 레이아웃
- 텍스트는 `<p>`, `<h1>`~`<h6>`, `<ul>`, `<ol>` 태그만 사용
- `<div>`만 배경색/테두리 적용 가능
- Web-safe fonts만 사용
- CSS gradient 금지
- `<span>`에 스타일링 가능하지만 제한적

**사전 검증**: `scripts/validate_html.py` 실행하여 규칙 준수 확인 → 실패 시 즉시 수정

### 03-executor-validator.md

```yaml
---
name: executor-validator
description: convert.js를 생성하고 HTML→PPTX 변환을 실행한 뒤 썸네일로 시각 검증을 수행합니다.
model: opus
tools: [Read, Write, Bash, Glob]
---
```

**입력**: `output/slides/*.html` + `engine/html2pptx.js` + `engine/thumbnail.py` + INPUT PNG
**출력**: `output/convert.js` + `output/presentation.pptx` + `output/thumbnails.jpg` + `output/validation.json` + `output/comparison.jpg`

**수행 순서**:
1. `convert.js` 생성 — `require('./engine/html2pptx.js')` 상대경로 사용
2. `node output/convert.js` 실행 → `output/presentation.pptx` 생성
3. `python engine/thumbnail.py` 실행 → `output/thumbnails.jpg` 생성
4. 썸네일을 Read로 시각 검사 → 텍스트 잘림, 겹침, 위치 이상 등 확인
5. `python scripts/compare_slides.py` → `output/comparison.jpg` (원본 vs 결과)
6. 검사 결과를 `output/validation.json`으로 구조화

### 04-iterative-fixer.md

```yaml
---
name: iterative-fixer
description: 검증 이슈를 수정하고 재변환하여 최종 PPTX를 생성합니다.
model: opus
tools: [Read, Write, Edit, Bash, Glob]
---
```

**입력**: `output/validation.json` + `output/slides/*.html` + `engine/*`
**출력**: `output/presentation_final.pptx` + `output/fix_log.json`

**수정 루프** (최대 3회):
1. `validation.json`의 이슈 분석
2. 해당 `slides/slide_*.html` 수정
3. `validate_html.py` 재검증
4. `node convert.js` 재실행
5. 썸네일 재생성 + 시각 재검사
6. 이슈 해결 여부 확인 → 미해결 시 루프 반복

---

## JSON 데이터 흐름

```
[INPUT 4개 파일 — 사용자 제공]
       ↓
  01-spec-analyzer
       → output/spec.json
       ↓
  02-html-slide-builder
       → output/slides/slide_00.html, slide_01.html, ...  ← 신규 생성
       → output/html_validation.json  ← validate_html.py 검증
       ↓
  03-executor-validator
       → output/convert.js  ← 신규 생성 (require engine/html2pptx.js)
       → output/presentation.pptx  ← 최종 PPTX
       → output/thumbnails.jpg  ← 시각 검증용
       → output/comparison.jpg  ← 원본 vs 결과 비교
       → output/validation.json  ← 검증 결과
       ↓
  (이슈 있으면)
  04-iterative-fixer
       → output/presentation_final.pptx  ← 수정 후 최종
       → output/fix_log.json  ← 수정 이력
```

### spec.json 스키마

```json
{
  "presentation": {
    "layout": "LAYOUT_16x9",
    "width_pt": 720,
    "height_pt": 405,
    "title": "제목"
  },
  "design": {
    "mode": "full_design|wireframe",
    "color_palette": {
      "primary": "#2563EB",
      "secondary": "#...",
      "background": "#FFFFFF",
      "text_primary": "#1F2937",
      "text_secondary": "#..."
    },
    "fonts": {
      "heading": "Arial",
      "body": "Arial"
    }
  },
  "slides": [
    {
      "slide_index": 0,
      "slide_type": "title|content|two_column|section_header",
      "source_section": "원본 HTML에서 해당하는 영역 설명",
      "elements": [
        {
          "type": "heading|text|list|image|shape|chart_placeholder",
          "content": "텍스트 내용",
          "style": {
            "font_size_pt": 32,
            "font_weight": "bold|normal",
            "color": "#1F2937",
            "align": "left|center|right",
            "position": {
              "x_pt": 30,
              "y_pt": 20,
              "width_pt": 660,
              "height_pt": 60
            }
          }
        }
      ],
      "background": {
        "type": "solid",
        "value": "#FFFFFF"
      }
    }
  ]
}
```

### validation.json 스키마

```json
{
  "execution": {
    "success": true,
    "pptx_path": "output/presentation.pptx",
    "thumbnail_path": "output/thumbnails.jpg",
    "comparison_path": "output/comparison.jpg"
  },
  "validation": {
    "slides_count": 5,
    "issues": [
      {
        "slide_index": 2,
        "issue_type": "text_cutoff|text_overlap|positioning|contrast|overflow",
        "description": "설명",
        "severity": "high|medium|low",
        "suggested_fix": "수정 방안"
      }
    ],
    "overall_quality": "pass|needs_fix"
  }
}
```

---

## scripts/ 설계

### validate_html.py — HTML 사전 검증

**검증 항목**:
- `<body>` 태그에 width/height 인라인 스타일 존재 여부
- `display: flex` 레이아웃 사용 여부
- 텍스트 태그 규칙: `<p>`, `<h1>`~`<h6>`, `<ul>`, `<ol>`만 허용
- CSS gradient 미사용 여부
- Web-safe font만 사용 여부
- `<span>` 스타일링 제한 준수 여부
- 수동 불릿 사용 금지

**출력**: JSON (errors + warnings)

```bash
python scripts/validate_html.py output/slides/slide_00.html
# → output/html_validation.json
```

### compare_slides.py — 원본 비교

원본 PNG와 PPTX 썸네일을 나란히 배치하여 시각 비교 이미지 생성

```bash
python scripts/compare_slides.py input.png output/thumbnails.jpg output/comparison.jpg
# → output/comparison.jpg (좌: 원본, 우: PPTX 썸네일)
```

---

## 검증 매트릭스

| 검증 항목 | 도구 | 자동화 | 실패 시 |
|-----------|------|--------|---------|
| HTML 규칙 준수 | validate_html.py | 완전 자동 | 02-html-slide-builder 즉시 수정 |
| JS 실행 성공 | node convert.js | 완전 자동 | 03-executor-validator 에러 수정 |
| PPTX 생성 확인 | 파일 존재 확인 | 완전 자동 | 03-executor-validator 재실행 |
| 시각적 품질 | thumbnail + AI Read | 반자동 | 04-iterative-fixer 호출 |
| 원본 일치도 | compare_slides + AI Read | 반자동 | 04-iterative-fixer 호출 |

---

## 구현 순서

### Phase 1: 엔진 내장 + 기본 구조
- [ ] 디렉토리 생성: `agents/`, `engine/`, `references/`, `scripts/`, `output/`
- [ ] `engine/` 파일 복사 (html2pptx.js, html2pptx.md, thumbnail.py)
- [ ] `SKILL.md` 작성 (YAML frontmatter + 입력 가이드 + 파이프라인)

### Phase 2: 에이전트 + 참조 문서 (병렬 가능)
- [ ] `agents/01-spec-analyzer.md`
- [ ] `agents/02-html-slide-builder.md`
- [ ] `agents/03-executor-validator.md`
- [ ] `agents/04-iterative-fixer.md`
- [ ] `references/html2pptx-rules.md` (engine/html2pptx.md 요약)
- [ ] `references/pptxgenjs-api-guide.md`
- [ ] `references/slide-design-patterns.md`

### Phase 3: Python 스크립트
- [ ] `scripts/validate_html.py`
- [ ] `scripts/compare_slides.py`

### Phase 4: 엔드투엔드 테스트
- [ ] INPUT 4개 파일 제공하여 전체 파이프라인 테스트
- [ ] `output/spec.json` 생성 확인 (구조/스키마 검증)
- [ ] `output/slides/slide_*.html` 신규 생성 확인
- [ ] `output/html_validation.json` 에러 0건 확인
- [ ] `output/convert.js` 생성 + `node convert.js` 성공 확인
- [ ] `output/presentation.pptx` 생성 확인
- [ ] `output/thumbnails.jpg` + `output/comparison.jpg` 시각 비교
- [ ] 모든 output 파일이 `output/`에 저장되어 있는지 확인

---

## 핵심 참조 파일

| 파일 | 경로 | 역할 |
|------|------|------|
| 예시스킬 SKILL.md | `Aitest/예시스킬/landing-page-generator-main/SKILL.md` | YAML frontmatter + 오케스트레이터 형식 참조 |
| 예시스킬 에이전트 | `Aitest/예시스킬/.../agents/01-intake.md` | 에이전트 .md 형식 참조 |
| 내장 html2pptx.md | `engine/html2pptx.md` | 변환 규칙 원본 (내장) |
| 내장 html2pptx.js | `engine/html2pptx.js` | 변환 엔진 (내장) |
| 내장 thumbnail.py | `engine/thumbnail.py` | 썸네일 도구 (내장) |
| INPUT HTML | `Aitest/partnering_main_eng.html` | 테스트 입력 (변환 대상) |
| INPUT PNG | `Aitest/partnering_main_eng.png` | 테스트 입력 (비교 기준) |
| INPUT 설명서 | `Aitest/partnering_main_eng_description.md` | 테스트 입력 (기능 설명) |
| INPUT 항목정의 | `Aitest/partnering_main_eng_fields.md` | 테스트 입력 (항목 정의) |

---

## V1 → V2 변경 요약

| 항목 | V1 (기존) | V2 (현재) |
|------|----------|----------|
| 엔진 위치 | 외부 `/pptx` 스킬 참조 | **`engine/` 내장** |
| 에이전트 수 | 5개 | **4개** (js-converter-writer 제거) |
| 스크립트 수 | 3개 (pipeline.py 포함) | **2개** (pipeline.py 제거) |
| 참조 방식 | 절대경로 `require()` | **상대경로** `require('./engine/...')` |
| 구조 | 단방향 순차 | **샌드위치** (병렬→순차→검증) |
| 이식성 | 경로 종속 | **자체 완결** |
| 외부 의존성 | `/pptx` 스킬 필수 | **없음** (내장) |
