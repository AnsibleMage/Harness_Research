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

# HTML→PPTX 변환기

## 개요

HTML 소스 파일과 보조 문서를 입력받아 PowerPoint(.pptx) 프레젠테이션으로 자동 변환하는 스킬입니다.
4개의 전문 Teammate가 분석→생성→변환→검증→수정 파이프라인을 순서에 따라 처리하며,
`engine/` 폴더에 내장된 html2pptx.js(PptxGenJS + Playwright)를 사용하여 외부 의존 없이 자체 완결적으로 동작합니다.

---

## 입력 가이드

스킬 실행 시 사용자에게 다음 안내문을 그대로 제시하여 입력을 수집합니다.

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

📂 출력 경로를 선택해주세요:
  a) 프로젝트 폴더 루트 (현재 작업 디렉토리에 output/ 생성)
  b) 입력 파일과 같은 폴더 (입력 HTML이 있는 폴더에 output/ 생성)
  c) 직접 지정 (원하는 절대/상대 경로 입력)

미지정 시 기본값: 프로젝트 폴더 루트 (a)
```

---

## 출력 스타일

기본 출력은 **와이어프레임 모드**입니다.

### wireframe (기본값)
- 흑백 와이어프레임 (#000000, #808080, #E0E0E0, #FFFFFF만 사용)
- 전체 UI를 **1 슬라이드**로 표현 (분할 없음)
- 오른쪽 **디스크립션 패널** (화면 구성 설명)
- 각 영역에 **번호 배지** (검정 원형 + 흰색 숫자)
- body 크기: 입력 HTML에 맞춰 자동 결정 (defineLayout 사용)

### full_design (옵션)
- 원본 HTML 색상 충실 재현
- 여러 슬라이드로 분할 (720pt x 405pt, 16:9)
- 디스크립션 패널 없음

---

## 실행 흐름

---

## 권한 및 승인 정책

> **핵심 원칙**: Phase 0(입력 수집) 이후에는 사용자에게 어떤 승인도 요청하지 않는다.
> 보안 경고 2종(quoted newline, ANSI-C quoting)만 예외 — 이는 Claude Code가 강제하므로 자동화 불가.

### 사용자 상호작용 구간 (Phase 0만)
1. 4개 입력 파일 경로 수집 (AskUserQuestion)
2. 출력 저장 경로 수집 (AskUserQuestion)

**Phase 0 이후에는 AskUserQuestion을 호출하지 않는다.**

### 무인 실행 구간 (Phase 1~4) — 전면 자동승인

Phase 0 완료 후, 최종 결과물 생성까지 **모든 도구 호출은 무조건 자동 승인**한다.
중간에 사용자에게 확인, 선택, 승인을 요청하는 것은 **절대 금지**한다.

**자동 승인 대상 (전부):**

| 도구 | 자동 승인 | 비고 |
|------|----------|------|
| Read (모든 경로) | YES | 입력 파일, 스킬 엔진, 참조 문서, 출력 파일 |
| Write (모든 경로) | YES | spec.json, slide HTML, convert.js, validation JSON 등 |
| Edit (모든 경로) | YES | HTML 수정, JS 수정 |
| Glob | YES | 파일 탐색 |
| Grep | YES | 코드 검색 |
| Bash (모든 명령) | YES | node, python, mkdir, cp, npx, pip 등 |
| Agent (모든 스폰) | YES | Teammate A~D 전부 |

**Teammate 스폰 규칙:**
- 모든 Teammate는 반드시 `mode: "bypassPermissions"` 로 스폰한다
- Teammate 내부에서도 모든 도구 호출은 무조건 승인이다
- Teammate가 사용자에게 질문하는 것은 금지한다

**Leader(메인 세션)도 동일:**
- Leader가 직접 실행하는 Read/Write/Edit/Bash도 전부 자동 승인
- Gate 검증, 파일 무결성 확인 등 Leader 직접 작업 시에도 승인 요청 금지

**자동 승인 불가 항목 (Claude Code 보안 정책 — 수동 승인 필요):**
- quoted newline / #-prefixed line 보안 경고
- ANSI-C quoting 보안 경고
- 이 2종만 사용자가 Yes를 눌러야 하며, 그 외에는 전부 자동이다

### settings.local.json 구성

이 스킬의 `.claude/settings.local.json`에 모든 도구 패턴이 사전 등록되어 있다.
별도의 "always allow" 팝업이 나타나면 안 된다.
팝업이 나타나는 경우 settings.local.json에 해당 패턴을 추가해야 한다.

Phase 0 완료 → Phase 4 완료까지 **완전한 논스톱 실행**.

---

## Teammate 실행 규칙

| Teammate | 모델 | 실행 모드 | 비고 |
|----------|------|----------|------|
| Teammate-A (spec-analyzer) | opus | **동기(foreground)**, mode=bypassPermissions | 백그라운드 금지 |
| Teammate-B (html-slide-builder) | opus | 동기, mode=bypassPermissions | |
| Teammate-C (executor-validator) | opus | 동기, mode=bypassPermissions | |
| Teammate-D (iterative-fixer) | opus | 동기, mode=bypassPermissions | 조건부 |

---

## 실행 흐름

```
[파일 수신] 4개 입력 파일 확인 + 출력 경로 설정
         |
         v
[Phase 1] 병렬 사전 작업
         |-- Teammate-A (01-spec-analyzer): HTML+설명서+항목정의서+PNG → spec.json
         |-- Leader: 입력 파일 무결성 검증
         |
         v
[Phase 2] 순차 HTML 생성
         --> Teammate-B (02-html-slide-builder): spec.json → slides/*.html
         --> validate_html.py → html_validation.json
         |
         v
[Phase 3] 단독 변환 + 검증
         --> Teammate-C (03-executor-validator):
               slides/*.html → convert.js → node 실행 → presentation.pptx
               → thumbnail → thumbnails.jpg → 시각 검사 → validation.json
               → compare_slides.py → comparison.jpg
         |
         v
[Phase 4] 조건부 수정 (validation.json에 이슈 시만)
         --> Teammate-D (04-iterative-fixer):
               HTML 수정 → 재변환 → 재검증 (최대 3회)
               → presentation_final.pptx + fix_log.json
```

---

## Phase 상세

### Phase 1: 병렬 사전 작업

Leader와 Teammate-A가 동시에 실행됩니다.

**Teammate-A — 01-spec-analyzer (opus)**

역할: 입력 4개 파일 전체를 분석하여 변환 명세(spec)를 추출합니다.

- HTML DOM 파싱: 슬라이드 경계, 섹션 구조, 컨테이너 계층 추출
- CSS 분석: 색상(HEX), 폰트명, 폰트 크기, 여백, 배경 추출
- 설명서(기능 설명 .md) 기반 의미 매핑: 각 HTML 영역의 기능 레이블 부여
- 입력 항목 정의서(.md) 기반 UI 요소 속성 매핑: 입력 형식, 상호작용 정의 반영
- PNG 스크린샷 대조: DOM 구조와 실제 렌더링 간 레이아웃 차이 감지

출력: `{OUTPUT_DIR}/spec.json`

spec.json 필수 필드:
- `slides[]`: 슬라이드 배열 (각 슬라이드의 요소 목록)
- `theme`: 전역 색상, 폰트, 배경 정의
- `layout`: 슬라이드 크기 (기본 720pt x 405pt, 16:9)
- `elements[]`: 각 요소의 type, position, size, style, content
- `warnings[]`: PNG 대조에서 발견된 레이아웃 불일치 목록

**Leader — 입력 파일 무결성 검증**

- 4개 파일 존재 여부 확인 (Glob + Bash stat)
- HTML 파싱 가능 여부 확인 (UTF-8 / EUC-KR 인코딩 검사)
- PNG 파일 형식 유효성 확인 (file 명령 또는 Python imghdr)
- MD 파일 인코딩 및 최소 내용 확인

누락 또는 불량 파일 발견 시: AskUserQuestion으로 재경로 요청 후 재검증.

---

### Phase 2: 순차 HTML 생성

Phase 1 완료 후 순차 실행됩니다. spec.json이 Leader에 의해 스키마 검증 통과 후 Teammate-B에 전달됩니다.

**Teammate-B — 02-html-slide-builder (opus)**

역할: spec.json과 html2pptx.md 규칙을 기반으로 슬라이드별 HTML 파일을 신규 생성합니다.
(원본 HTML을 그대로 사용하는 것이 아니라, 변환 엔진이 처리 가능한 형식으로 재작성)

- `engine/html2pptx.md`에 정의된 HTML 작성 규칙을 엄격히 준수
- `references/` 폴더의 디자인 패턴 및 API 가이드 참조
- 슬라이드 1개 = 파일 1개 (`slide_01.html`, `slide_02.html`, ...)
- 각 파일은 단독 렌더링 가능한 완전한 HTML 문서
- `data-pptx-*` 속성으로 변환 메타데이터 명시
- Web-safe 폰트만 사용 (Arial, Helvetica, Georgia, Times New Roman 등)

생성 직후 `validate_html.py` 실행:
- 각 슬라이드 HTML에 대해 필수 속성, 크기 단위, 폰트 규칙 검사
- 검증 실패 항목은 즉시 Teammate-B가 수정 후 재검증
- 모든 슬라이드 검증 통과 후 `html_validation.json` 저장

출력:
- `{OUTPUT_DIR}/slides/slide_01.html` ~ `slide_NN.html`
- `{OUTPUT_DIR}/html_validation.json`

---

### Phase 3: 단독 변환 + 검증

**Teammate-C — 03-executor-validator (opus)**

역할: 생성된 슬라이드 HTML을 실제 PPTX로 변환하고 시각 검증을 수행합니다.

**Step 3-1: convert.js 생성**

Teammate-C가 `{OUTPUT_DIR}/convert.js`를 직접 작성합니다.

- `require`의 상대 경로는 `engine/html2pptx.js`를 가리켜야 합니다
- `slides/` 폴더의 모든 `slide_*.html`을 입력으로 받아 슬라이드 순서 보장
- 출력 경로: `{OUTPUT_DIR}/presentation.pptx`

예시 구조:
```javascript
const html2pptx = require('../../engine/html2pptx.js'); // 상대경로 조정 필요
const path = require('path');
// slides 폴더 glob → 순서 정렬 → html2pptx 호출 → presentation.pptx 저장
```

**Step 3-2: PPTX 변환 실행**

```bash
node {OUTPUT_DIR}/convert.js
```

실행 성공 시: `{OUTPUT_DIR}/presentation.pptx` 생성 확인

**Step 3-3: 썸네일 생성**

```bash
python engine/thumbnail.py {OUTPUT_DIR}/presentation.pptx {OUTPUT_DIR}/thumbnails.jpg
```

Playwright로 PPTX 각 슬라이드를 렌더링하여 스트립 이미지 생성.

**Step 3-4: 시각 비교**

```bash
python scripts/compare_slides.py {INPUT_PNG} {OUTPUT_DIR}/thumbnails.jpg {OUTPUT_DIR}/comparison.jpg
```

원본 PNG(입력 스크린샷)와 생성된 썸네일을 나란히 배치한 비교 이미지 생성.

**Step 3-5: 시각 검사 및 validation.json 생성**

Teammate-C가 `comparison.jpg`와 `thumbnails.jpg`를 직접 시각 검토하여 다음 항목을 평가합니다:

- 레이아웃 구조 일치 여부
- 색상 재현 정확도
- 텍스트 잘림(clipping) 여부
- 요소 위치 편차
- 폰트 렌더링 품질

평가 결과를 `validation.json`으로 저장:
```json
{
  "overall_quality": "pass | needs_fix",
  "slide_results": [
    {
      "slide_index": 1,
      "issues": [],
      "severity": "none | minor | major"
    }
  ],
  "summary": "..."
}
```

출력: `convert.js`, `presentation.pptx`, `thumbnails.jpg`, `validation.json`, `comparison.jpg`

---

### Phase 4: 조건부 수정

`validation.json`의 `overall_quality`가 `"needs_fix"`인 경우에만 실행됩니다.
`"pass"`인 경우 Phase 4를 건너뛰고 최종 결과를 사용자에게 보고합니다.

**Teammate-D — 04-iterative-fixer (opus)**

역할: 검증에서 발견된 이슈를 반복 수정하여 품질을 개선합니다.

수정 루프 (최대 3회):
1. `validation.json`의 이슈 목록 분석
2. 해당 `slides/slide_NN.html` 파일 수정 (이슈 유형별 처리)
3. `validate_html.py` 재실행 → 검증 통과 확인
4. `node convert.js` 재실행 → `presentation.pptx` 갱신
5. `thumbnail.py` 재실행 → 썸네일 갱신
6. 썸네일 시각 재검사 → `validation.json` 업데이트
7. `overall_quality == "pass"` 이면 루프 종료

3회 수정 후에도 `overall_quality`가 `"needs_fix"`로 남는 경우:
- 미해결 이슈 목록과 원인 분석을 사용자에게 보고
- 수동 수정 가이드라인 제시
- 가장 최근의 `presentation.pptx`를 `presentation_final.pptx`로 복사하여 최선의 결과물 제공

루프 성공 시 최종 `presentation.pptx`를 `presentation_final.pptx`로 복사.

출력: `{OUTPUT_DIR}/presentation_final.pptx`, `{OUTPUT_DIR}/fix_log.json`

fix_log.json 구조:
```json
{
  "total_iterations": 2,
  "iterations": [
    {
      "iteration": 1,
      "issues_fixed": ["slide 2: text clipping in title"],
      "issues_remaining": ["slide 3: color mismatch"]
    }
  ],
  "final_status": "pass | partial"
}
```

---

## Teammate 배분

| Teammate | 에이전트 | 모델 | Phase | 입력 | 출력 |
|----------|----------|------|-------|------|------|
| A | 01-spec-analyzer | opus | 1 병렬 | INPUT 4개 파일 (HTML, PNG, 기능설명.md, 항목정의.md) | spec.json |
| B | 02-html-slide-builder | opus | 2 순차 | spec.json + engine/html2pptx.md + references/ | slides/slide_*.html + html_validation.json |
| C | 03-executor-validator | opus | 3 순차 | slides/*.html + engine/html2pptx.js + engine/thumbnail.py + INPUT PNG | convert.js + presentation.pptx + thumbnails.jpg + validation.json + comparison.jpg |
| D | 04-iterative-fixer | opus | 4 조건부 | validation.json + slides/*.html + engine/* | presentation_final.pptx + fix_log.json |

---

## 소통 규칙

- 모든 Teammate는 Leader(메인 세션)에게만 보고합니다. Teammate 간 직접 통신은 금지됩니다.
- 데이터 전달은 `{OUTPUT_DIR}/` 내 JSON 파일을 통해 이루어집니다. 인라인 텍스트 전달 금지.
- Leader는 각 Phase 전환 전에 중간 JSON 파일의 스키마와 내용을 검증합니다.
  - Phase 1→2 전환: spec.json 스키마 검증 (필수 필드 존재 여부)
  - Phase 2→3 전환: html_validation.json 전체 통과 확인
  - Phase 3→4 전환: validation.json의 overall_quality 판독
- Teammate는 모든 출력 파일을 `{OUTPUT_DIR}/` (또는 그 하위) 에만 기록합니다. 스킬 폴더(`~/.claude/skills/html2pptx-converter/`) 내에는 절대 쓰지 않습니다.
- Teammate 착수 보고: spawn 후 30초 이내에 Leader에게 첫 진행 메시지를 전송해야 합니다.
- 120초 무응답 Teammate는 Leader가 shutdown 후 직접 해당 Phase를 수행합니다.

---

## 출력 경로 처리

스킬 시작 시 `AskUserQuestion` 도구를 사용하여 출력 경로를 확인합니다.

선택지:
- **a) 프로젝트 폴더 루트**: `{CWD}/output/` (현재 작업 디렉토리 기준)
- **b) 입력 파일과 같은 폴더**: `{INPUT_HTML_DIR}/output/` (입력 HTML 파일의 상위 디렉토리 기준)
- **c) 직접 지정**: 사용자가 입력한 절대 경로 또는 상대 경로

미지정 시 기본값: 옵션 a (`{CWD}/output/`)

`OUTPUT_DIR` 변수 결정 후:
```bash
mkdir -p "{OUTPUT_DIR}/slides"
```
`OUTPUT_DIR` 값은 모든 Teammate에게 태스크 프롬프트 내에 명시적으로 전달합니다.

---

## 에러 처리

| Phase | 에러 상황 | 대응 |
|-------|----------|------|
| 1 | 입력 파일 누락 | AskUserQuestion으로 누락 파일 경로 재요청 후 검증 재시작 |
| 1 | HTML 파싱 불가 (인코딩 오류) | 인코딩 자동 변환 시도 (chardet), 실패 시 사용자에게 UTF-8 변환 요청 알림 |
| 1 | PNG 파일 형식 불량 | 파일 재확인 요청, 대체 PNG 경로 수용 |
| 2 | spec.json 스키마 불일치 | Leader가 불일치 필드 목록을 Teammate-A에 전달하여 재실행 |
| 2 | HTML 검증 실패 (validate_html.py) | Teammate-B가 실패 항목을 즉시 수정 후 재검증 (자동, 사용자 개입 불필요) |
| 3 | `node convert.js` 실행 에러 | Teammate-C가 에러 메시지 분석 → convert.js 또는 slide HTML 수정 → 재실행 |
| 3 | PPTX 파일 생성 실패 | `engine/html2pptx.js` 경로 및 Node.js 버전 확인, 재실행 |
| 3 | 썸네일 생성 실패 | Playwright 브라우저 설치 확인 (`npx playwright install`), 재시도 |
| 3 | compare_slides.py 실패 | Pillow 설치 확인 (`pip install pillow`), 재시도 |
| 4 | 3회 수정 후 미해결 이슈 | 남은 이슈 목록 + 원인 분석 + 수동 수정 가이드를 사용자에게 보고 |
| 전체 | Teammate 120초 무응답 | Leader가 shutdown 후 해당 Phase를 직접 수행 |

---

## 참조 문서

- [html2pptx 규칙 요약](references/html2pptx-rules.md)
  - html2pptx.js가 처리 가능한 HTML 구조 규칙, `data-pptx-*` 속성 명세, 단위 규칙 요약
- [PptxGenJS API 가이드](references/pptxgenjs-api-guide.md)
  - PptxGenJS 주요 API 레퍼런스, 텍스트/이미지/도형/표 추가 메서드, 슬라이드 레이아웃 설정
- [슬라이드 디자인 패턴](references/slide-design-patterns.md)
  - 제목 슬라이드, 콘텐츠 슬라이드, 비교 레이아웃 등 재사용 가능한 HTML 슬라이드 템플릿

에이전트 파일:
- [01-spec-analyzer](agents/01-spec-analyzer.md)
- [02-html-slide-builder](agents/02-html-slide-builder.md)
- [03-executor-validator](agents/03-executor-validator.md)
- [04-iterative-fixer](agents/04-iterative-fixer.md)

---

## 내장 엔진

스킬 폴더의 `engine/` 디렉토리에 변환에 필요한 모든 엔진 파일이 내장되어 있습니다.
외부 스킬 폴더를 참조하거나 별도 설치 없이 자체 완결적으로 동작합니다.

| 파일 | 역할 | 원본 경로 |
|------|------|----------|
| `engine/html2pptx.js` | HTML→PPTX 변환 엔진 (PptxGenJS + Playwright 기반) | `~/.claude/skills/pptx/scripts/html2pptx.js` |
| `engine/html2pptx.md` | HTML 작성 규칙 원본 문서 (Teammate-B의 기준 문서) | `~/.claude/skills/pptx/html2pptx.md` |
| `engine/thumbnail.py` | PPTX→썸네일 이미지 생성 (Playwright 기반 슬라이드 렌더링) | `~/.claude/skills/pptx/scripts/thumbnail.py` |

엔진 파일 업데이트 시: 원본 경로에서 복사하여 `engine/` 폴더를 갱신합니다. 스킬 내부 동작에는 영향을 주지 않습니다.

---

## 출력 파일

| Phase | 파일명 | 설명 | 생성 에이전트 |
|-------|--------|------|--------------|
| 1 | `{OUTPUT_DIR}/spec.json` | HTML 분석 결과 변환 명세 (슬라이드 구조, 테마, 요소 목록) | Teammate-A |
| 2 | `{OUTPUT_DIR}/slides/slide_00.html` (wireframe: 1개) 또는 `slide_00~NN.html` (full_design) | 변환 엔진용 슬라이드 HTML 파일 | Teammate-B |
| 2 | `{OUTPUT_DIR}/html_validation.json` | 슬라이드 HTML 사전 검증 결과 | Teammate-B (validate_html.py) |
| 3 | `{OUTPUT_DIR}/convert.js` | PPTX 변환 실행 스크립트 | Teammate-C |
| 3 | `{OUTPUT_DIR}/presentation.pptx` | 1차 변환된 PowerPoint 파일 | Teammate-C (node convert.js) |
| 3 | `{OUTPUT_DIR}/thumbnails.jpg` | PPTX 슬라이드 썸네일 스트립 이미지 | Teammate-C (thumbnail.py) |
| 3 | `{OUTPUT_DIR}/comparison.jpg` | 원본 PNG vs 썸네일 나란히 비교 이미지 | Teammate-C (compare_slides.py) |
| 3 | `{OUTPUT_DIR}/validation.json` | 시각 검증 결과 (overall_quality, 슬라이드별 이슈 목록) | Teammate-C |
| 4 | `{OUTPUT_DIR}/presentation_final.pptx` | 수정 완료된 최종 PowerPoint 파일 | Teammate-D |
| 4 | `{OUTPUT_DIR}/fix_log.json` | 반복 수정 이력 (수정 횟수, 수정 항목, 최종 상태) | Teammate-D |

Phase 4가 실행되지 않는 경우(pass): `presentation.pptx`가 최종 결과물이며, `presentation_final.pptx`는 생성되지 않습니다.
최종 사용자 보고 시 Leader가 실제 최종 파일명을 명시합니다.

---

## 기술 스펙

| 항목 | 값 |
|------|-----|
| 슬라이드 레이아웃 | wireframe=CUSTOM(defineLayout), full_design=LAYOUT_16x9 |
| body 크기 | wireframe=입력 HTML 비율 기반, full_design=720×405pt |
| 변환 엔진 | html2pptx.js (PptxGenJS + Playwright) |
| 썸네일 생성 | thumbnail.py (COM fallback on Windows, LibreOffice fallback) |
| HTML 사전 검증 | validate_html.py (--mode wireframe 지원) |
| 시각 비교 | compare_slides.py (Pillow) |
| 폰트 | Web-safe fonts only (Arial, Helvetica, Georgia, Times New Roman, Courier New 등) |
| 최대 수정 루프 | 3회 |
| Node.js 최소 버전 | 16.x 이상 |
| Python 최소 버전 | 3.8 이상 |
| 필수 Python 패키지 | Pillow |
| 선택 Python 패키지 | chardet, comtypes (Windows), python-pptx |
| 필수 Node 패키지 | pptxgenjs (package.json 참조) |
| Playwright 브라우저 | Chromium (npx playwright install chromium) |
| 슬라이드 파일 명명 | wireframe: slide_00.html (1개), full_design: slide_00~NN.html |
| 중간 파일 위치 | 모두 {OUTPUT_DIR}/ 내부 (스킬 폴더 외부) |

### Windows 인코딩 참고

Windows 환경에서 한국어 등 비ASCII 텍스트가 포함된 파일 처리 시 인코딩 오류가 발생할 수 있다.

| 해결 방법 | 설명 |
|----------|------|
| 환경변수 설정 | `set PYTHONIOENCODING=utf-8` (cmd) 또는 `export PYTHONIOENCODING=utf-8` (bash) |
| Python 실행 옵션 | `python -X utf8 script.py` (Python 3.7+) |
| 스크립트 내장 수정 | `validate_html.py`, `compare_slides.py`에 `sys.stdout.reconfigure(encoding='utf-8')` 이미 내장 |

> 참고: `validate_html.py`는 내부에서 `chardet` 모듈을 사용한 자동 인코딩 감지를 지원한다 (선택 설치).
