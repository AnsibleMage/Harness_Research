# HTML→PPTX 변환 스킬 E2E 테스트 — 테스트 계획 및 예상결과

> Version: 1.0 | Date: 2026-03-11
> Skill: html2pptx-converter | Engine: html2pptx.js (PptxGenJS + Playwright)

---

## 1. 테스트 개요

| 항목 | 값 |
|------|-----|
| 테스트 유형 | End-to-End 블라인드 테스트 |
| 테스트 대상 | `~/.claude/skills/html2pptx-converter/` 스킬 전체 파이프라인 |
| 테스트 방법 | 새 Claude Code 세션에서 4개 입력 파일로 스킬 실행, 결과 기록 |
| 합격 기준 | 14개 TC 중 TC-01~TC-12 전원 PASS (TC-13은 조건부, TC-14는 전체 결과 확인) |

---

## 2. 테스트 환경

| 항목 | 값 |
|------|-----|
| OS | Windows 11 Pro |
| Shell | bash (Git Bash) |
| Node.js | 16.x 이상 |
| Python | 3.8 이상 |
| 필수 패키지 (Node) | pptxgenjs |
| 필수 패키지 (Python) | Pillow, chardet, playwright |
| 스킬 경로 | `C:\Users\name\.claude\skills\html2pptx-converter\` |
| SKILL_DIR | `~/.claude/skills/html2pptx-converter` (bash 경로) |

---

## 3. 입력 파일 (4개)

| # | 파일 | 경로 | 설명 |
|---|------|------|------|
| 1 | test_layout.html | `{SKILL_DIR}/test/test_layout.html` | TestCorp Portal 테스트 페이지 (~450줄) |
| 2 | test_layout.png | `{SKILL_DIR}/test/test_layout.png` | HTML 스크린샷 (1280x full-page) |
| 3 | test_layout_description.md | `{SKILL_DIR}/test/test_layout_description.md` | 7개 영역 기능 설명서 (~170줄) |
| 4 | test_layout_fields.md | `{SKILL_DIR}/test/test_layout_fields.md` | 16개 UI 요소 정의서 (~218줄) |

### 테스트 페이지 구조 요약

| 영역 | 주요 요소 | 핵심 색상 |
|------|----------|----------|
| 코너 마커 | TL(#E53E3E), TR(#3182CE), BL(#38A169), BR(#D69E2E), CENTER(#805AD5) | 5개 고정 위치 마커 |
| 헤더 | 로고 "TestCorp Portal" + 메뉴 5개 | #1E3A5F 배경 |
| 히어로 | 제목 42px + 부제목 + CTA 버튼 2개 | #2B6CB0 배경 |
| 통계 바 | 1,247 / 358 / 99.9% / 24/7 | #FFFFFF 배경 |
| 게시판+사이드바 | 5행 테이블 + 4색 태그 + 리스트 + 2x2 그리드 | 2단 레이아웃 |
| 도형/라인 | 5종 도형 + 4종 라인 | 각각 고유 색상 |
| 푸터 | 4단 컬럼 + 저작권 + 소셜 링크 | #1A202C 배경 |

### 예상 슬라이드 분할 (fields.md 기준)

| Slide | 영역 | 이유 |
|-------|------|------|
| Slide 0 | 코너 마커 + 헤더 + 히어로 | 좌표 마커는 첫 슬라이드 꼭짓점/중앙 배치 |
| Slide 1 | 통계 바 + 게시판 + 사이드바 | 콘텐츠 영역 통합 |
| Slide 2 | 도형 & 라인 테스트 | 렌더링 검증 전용 |
| Slide 3 | 푸터 | 다단 레이아웃 검증 |

---

## 4. 테스트 항목 (TC-01 ~ TC-14)

---

### TC-01: 스킬 트리거 및 입력 수집

**검증 항목**: 스킬이 정상 활성화되고 입력 가이드 텍스트를 표시하며 4개 파일 경로를 수집하는가

**예상 실행 플로우**:

1. 사용자가 html2pptx 변환 요청 (예: "이 파일들로 HTML→PPTX 변환해줘")
2. `html2pptx-converter` 스킬 트리거됨
3. Leader(메인 세션)가 SKILL.md를 읽음 → Skill tool 호출
4. 입력 가이드 텍스트 출력:
   ```
   📋 HTML→PPTX 변환을 시작합니다.

   다음 4개 파일의 경로를 알려주세요:
   1. HTML 소스 파일 (.html)
   2. 스크린샷 파일 (.png)
   3. 페이지 기능 설명서 (.md)
   4. 입력 항목 정의서 (.md)

   📂 출력 경로를 선택해주세요:
     a) 프로젝트 폴더 루트
     b) 입력 파일과 같은 폴더
     c) 직접 지정
   ```
5. 사용자가 4개 파일 경로 제공 (또는 이미 프롬프트에 포함)

**예상 도구 호출**:
- `Skill("html2pptx-converter")` — 스킬 로드
- 또는 사용자 프롬프트에 의해 자동 트리거

**통과 조건**:
- [ ] 스킬이 정상 활성화됨
- [ ] 입력 가이드 텍스트가 사용자에게 표시됨 (4개 파일 + 출력 경로 선택지)
- [ ] 4개 파일 경로가 수집됨

---

### TC-02: 출력 경로 설정 및 디렉토리 생성

**검증 항목**: OUTPUT_DIR이 설정되고 slides 하위 디렉토리가 생성되는가

**예상 실행 플로우**:

1. Leader가 출력 경로 선택을 사용자에게 질문 (AskUserQuestion 또는 직접 질문)
2. 사용자 응답에 따라 OUTPUT_DIR 결정
3. Leader가 디렉토리 생성

**예상 명령어 로그**:
```bash
# OUTPUT_DIR 생성 (사용자 선택에 따라 경로 변동)
# 옵션 b 선택 시 예시:
mkdir -p "~/.claude/skills/html2pptx-converter/test/output/slides"
```

**예상 OUTPUT_DIR 경로** (옵션별):
- a) `{CWD}/output/`
- b) `~/.claude/skills/html2pptx-converter/test/output/`
- c) 사용자 지정 경로

**통과 조건**:
- [ ] OUTPUT_DIR이 명확히 결정됨
- [ ] `{OUTPUT_DIR}/` 디렉토리 존재
- [ ] `{OUTPUT_DIR}/slides/` 하위 디렉토리 존재

---

### TC-03: Phase 1 — 입력 파일 무결성 검증 (Leader)

**검증 항목**: Leader가 4개 파일의 존재, 인코딩, 형식을 검증하는가

**예상 실행 플로우**:

1. Leader가 4개 파일을 확인 (Glob/Read/Bash)
2. HTML 인코딩 확인
3. PNG 형식 확인
4. MD 파일 최소 내용 확인

**예상 도구 호출 (Leader)**:
```
Read("test/test_layout.html")          → HTML 내용 확인
Read("test/test_layout.png")           → PNG 이미지 확인 (시각적 확인)
Read("test/test_layout_description.md") → MD 내용 존재 확인
Read("test/test_layout_fields.md")      → MD 내용 존재 확인
```

또는 Bash로 파일 존재 확인:
```bash
# 파일 존재 및 인코딩 확인
file "~/.claude/skills/html2pptx-converter/test/test_layout.html"
file "~/.claude/skills/html2pptx-converter/test/test_layout.png"
```

**예상 결과**:
- test_layout.html: UTF-8, HTML 문서, 정상
- test_layout.png: PNG image data, 정상
- test_layout_description.md: UTF-8, ~170줄, 정상
- test_layout_fields.md: UTF-8, ~218줄, 정상

**통과 조건**:
- [ ] 4개 파일 모두 존재 확인됨
- [ ] HTML 인코딩 확인됨 (UTF-8)
- [ ] PNG 형식 유효성 확인됨
- [ ] MD 파일에 내용이 있음이 확인됨
- [ ] 누락/불량 파일 없음 (AskUserQuestion 미발생)

---

### TC-04: Phase 1 — 스펙 분석 (Teammate-A: spec-analyzer)

**검증 항목**: Teammate-A가 4개 파일을 분석하여 올바른 구조의 spec.json을 생성하는가

**예상 실행 플로우**:

1. Leader가 Agent 도구로 Teammate-A 생성 (01-spec-analyzer 프롬프트)
2. Teammate-A가 4개 입력 파일 + agents/01-spec-analyzer.md를 읽음
3. Step 1: HTML DOM 구조 분석 (Read → test_layout.html)
4. Step 2: CSS 스타일 추출 (inline style + style 블록)
5. Step 3: PNG 스크린샷 시각 분석 (Read → test_layout.png)
6. Step 4: description.md 분석 (Read)
7. Step 5: fields.md 분석 (Read)
8. Step 6: spec.json 생성 (Write)
9. JSON 파싱 검증 (Bash)

**예상 Agent 스폰**:
```
Agent(
  prompt: "01-spec-analyzer.md 내용 + 입력 파일 경로 + OUTPUT_DIR 경로",
  model: opus,
  mode: bypassPermissions,
  run_in_background: false  # 동기(foreground) 실행 — SKILL.md 규칙
)
```

**예상 Teammate-A 내부 도구 호출**:
```
Read(test_layout.html)           → DOM 구조 파악
Read(test_layout.png)            → 시각 레이아웃 확인
Read(test_layout_description.md) → 7개 영역 기능 매핑
Read(test_layout_fields.md)      → 16개 UI 요소 속성 매핑
Read(engine/html2pptx.md)        → 변환 규칙 참조 (선택적)
Read(references/slide-design-patterns.md) → 디자인 패턴 참조 (선택적)
Write({OUTPUT_DIR}/spec.json)    → 스펙 JSON 생성
Bash("python -c \"import json; json.load(open('{OUTPUT_DIR}/spec.json'))\"") → 파싱 검증
```

**예상 spec.json 구조**:
```json
{
  "presentation": {
    "layout": "CUSTOM",
    "width_pt": 1235,
    "height_pt": 1491,
    "title": "TestCorp Portal"
  },
  "design": {
    "mode": "wireframe",
    "wireframe_palette": {
      "border": "#000000",
      "accent_bg": "#808080",
      "section_bg": "#E0E0E0",
      "card_bg": "#FFFFFF",
      "text": "#000000",
      "text_on_accent": "#FFFFFF"
    },
    "original_palette": {
      "primary": "#2B6CB0",
      "secondary": "#1E3A5F",
      "accent": "#E53E3E",
      "background": "#F5F5F5",
      "text_primary": "#1F2937",
      "text_secondary": "#718096"
    },
    "fonts": {
      "heading": "Arial",
      "body": "Arial"
    }
  },
  "slides": [
    {
      "slide_index": 0,
      "slide_type": "title 또는 content",
      "source_section": "코너 마커 + header + hero 영역",
      "elements": [
        {"type": "shape", "content": "TL marker", "style": {"color": "#E53E3E", ...}},
        {"type": "shape", "content": "TR marker", "style": {"color": "#3182CE", ...}},
        {"type": "shape", "content": "BL marker", "style": {"color": "#38A169", ...}},
        {"type": "shape", "content": "BR marker", "style": {"color": "#D69E2E", ...}},
        {"type": "shape", "content": "CENTER marker", "style": {"color": "#805AD5", ...}},
        {"type": "heading", "content": "TestCorp Portal", ...},
        {"type": "text", "content": "Home, Services, Board, About, Contact", ...},
        {"type": "heading", "content": "Welcome to TestCorp Portal", "style": {"font_size_pt": 31, ...}},
        {"type": "text", "content": "부제목 텍스트...", ...},
        {"type": "shape", "content": "Get Started 버튼", ...},
        {"type": "shape", "content": "Learn More 버튼", ...}
      ],
      "background": {"type": "solid", "value": "#2B6CB0"}
    },
    {
      "slide_index": 1,
      "slide_type": "two_column 또는 content",
      "source_section": "stats-bar + board-section + sidebar",
      "elements": [
        {"type": "text", "content": "1,247 / Active Users", ...},
        {"type": "text", "content": "358 / Projects", ...},
        {"type": "text", "content": "99.9% / Uptime", ...},
        {"type": "text", "content": "24/7 / Support", ...},
        {"type": "heading", "content": "Notice Board", ...},
        {"type": "list 또는 text", "content": "테이블 행 데이터...", ...},
        {"type": "heading", "content": "Recent Updates", ...},
        {"type": "list", "content": "API v2.5 released...", ...},
        {"type": "heading", "content": "Quick Links", ...},
        {"type": "text", "content": "Docs, Support, Reports, Settings", ...}
      ],
      "background": {"type": "solid", "value": "#FFFFFF 또는 #F5F5F5"}
    },
    {
      "slide_index": 2,
      "slide_type": "content",
      "source_section": "shape-line-section 도형 & 라인 테스트",
      "elements": [
        {"type": "heading", "content": "Shape & Line Rendering Test", ...},
        {"type": "shape", "content": "Rectangle", "style": {"color": "#2B6CB0", ...}},
        {"type": "shape", "content": "Rounded Rect", "style": {"color": "#38A169", ...}},
        {"type": "shape", "content": "Circle", "style": {"color": "#E53E3E", ...}},
        {"type": "shape", "content": "Border Only", "style": {"color": "#D69E2E", ...}},
        {"type": "shape", "content": "Box Shadow", "style": {"color": "#805AD5", ...}},
        {"type": "shape", "content": "Top Border line", ...},
        {"type": "shape", "content": "Left Border line", ...},
        {"type": "shape", "content": "Bottom Border line", ...},
        {"type": "shape", "content": "Full Border line", ...}
      ],
      "background": {"type": "solid", "value": "#FFFFFF"}
    },
    {
      "slide_index": 3,
      "slide_type": "content",
      "source_section": "footer 영역 — 4단 레이아웃",
      "elements": [
        {"type": "heading", "content": "TestCorp Portal (회사명)", ...},
        {"type": "text", "content": "회사 소개 텍스트...", ...},
        {"type": "heading", "content": "Company", ...},
        {"type": "list", "content": "About Us, Careers, Press, Blog", ...},
        {"type": "heading", "content": "Resources", ...},
        {"type": "list", "content": "Documentation, API Reference, Status Page, Changelog", ...},
        {"type": "heading", "content": "Legal", ...},
        {"type": "list", "content": "Privacy Policy, Terms of Service, Cookie Policy, GDPR", ...},
        {"type": "text", "content": "© 2026 TestCorp. All rights reserved.", ...}
      ],
      "background": {"type": "solid", "value": "#1A202C"}
    }
  ]
}
```

**핵심 검증 포인트**:
- `slides` 배열 길이: **3~5개** (4개 권장)
- `color_palette.primary`: **#2B6CB0** (HTML에서 추출)
- `fonts.heading`: **Arial** (web-safe 폰트)
- 모든 `position`이 720pt x 405pt 범위 내
- 모든 색상이 `#hex` 형식

**통과 조건**:
- [ ] Teammate-A Agent가 정상 생성/실행됨
- [ ] Teammate-A가 spawn 후 30초 이내에 착수 보고 (첫 진행 메시지)
- [ ] `{OUTPUT_DIR}/spec.json` 파일 존재
- [ ] JSON 파싱 가능 (문법 오류 없음)
- [ ] `presentation.width_pt` = 720, `height_pt` = 405
- [ ] `slides` 배열 길이 ≥ 3
- [ ] 모든 slide에 `elements` 배열이 존재하고 비어있지 않음
- [ ] `color_palette` 6개 필드 모두 존재
- [ ] `fonts.heading`과 `fonts.body`가 web-safe 폰트
- [ ] 모든 slide에 `source_section` 필드 존재
- [ ] 모든 색상 값이 `#hex` 형식

---

### TC-05: Phase 1→2 전환 — Leader의 spec.json 스키마 검증

**검증 항목**: Leader가 spec.json의 필수 필드와 스키마를 검증한 후 Phase 2를 개시하는가

**예상 실행 플로우**:

1. Teammate-A 완료 후 Leader가 spec.json을 Read
2. 필수 필드 존재 확인:
   - `presentation.width_pt`, `presentation.height_pt`
   - `slides[]` 배열 (길이 ≥ 1)
   - 각 slide의 `elements[]` (비어있지 않음)
   - `design.color_palette` (6개 필드)
   - `design.fonts` (heading, body)
3. 검증 통과 시 Phase 2 진행
4. 검증 실패 시 Teammate-A 재실행

**예상 도구 호출 (Leader)**:
```
Read({OUTPUT_DIR}/spec.json) → 스키마 검증
```

**예상 결과**: 검증 통과 → Phase 2 진행

**통과 조건**:
- [ ] Leader가 spec.json을 읽고 스키마를 검증함
- [ ] 검증 통과 확인 메시지 또는 Phase 2 진행 선언
- [ ] (실패 시) Teammate-A 재실행이 트리거됨

---

### TC-06: Phase 2 — HTML 슬라이드 생성 (Teammate-B: html-slide-builder)

**검증 항목**: Teammate-B가 spec.json을 기반으로 html2pptx 규칙을 준수하는 슬라이드 HTML 파일을 생성하는가

**예상 실행 플로우**:

1. Leader가 Agent 도구로 Teammate-B 생성 (02-html-slide-builder 프롬프트)
2. Teammate-B가 spec.json + html2pptx.md + references를 읽음
3. slides 디렉토리 확인/생성
4. 슬라이드별 HTML 파일 생성 (Write)
5. 자체 검증 (각 HTML 규칙 체크)
6. validate_html.py 실행 (Bash)
7. html_validation.json 생성 (Write)

**예상 Agent 스폰**:
```
Agent(
  prompt: "02-html-slide-builder.md 내용 + spec.json 경로 + OUTPUT_DIR 경로 + SKILL_DIR 경로",
  model: opus,
  mode: bypassPermissions,
  run_in_background: false  # 동기(foreground) 실행
)
```

**예상 Teammate-B 내부 도구 호출**:
```
Read({OUTPUT_DIR}/spec.json)                    → 슬라이드 설계 로드
Read(engine/html2pptx.md)                       → 변환 규칙 확인
Read(references/html2pptx-rules.md)             → 규칙 요약 확인
Read(references/slide-design-patterns.md)       → 디자인 패턴 참조
Bash("mkdir -p {OUTPUT_DIR}/slides")            → (이미 존재하면 무작업)
Write({OUTPUT_DIR}/slides/slide_00.html)        → Slide 0 생성
Write({OUTPUT_DIR}/slides/slide_01.html)        → Slide 1 생성
Write({OUTPUT_DIR}/slides/slide_02.html)        → Slide 2 생성
Write({OUTPUT_DIR}/slides/slide_03.html)        → Slide 3 생성
```

**예상 생성 파일 (4개 슬라이드)**:

| 파일 | 슬라이드 내용 | 주요 요소 |
|------|-------------|----------|
| slide_00.html | 코너 마커 + 헤더 + 히어로 | TL/TR/BL/BR/CENTER 마커 div, 로고 텍스트, 메뉴, 제목 h1, 부제목 p, CTA 버튼 div |
| slide_01.html | 통계 + 게시판 + 사이드바 | 통계 숫자/라벨, 테이블 구조, 리스트, 2x2 그리드 |
| slide_02.html | 도형 & 라인 테스트 | 5종 도형 div + 4종 라인 div + 각 라벨 p |
| slide_03.html | 푸터 4단 레이아웃 | 4개 컬럼 div + 링크 리스트 ul/li + 저작권 p |

**예상 HTML 공통 구조** (모든 슬라이드):
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
html { background: #ffffff; }
body {
  width: 720pt;
  height: 405pt;
  margin: 0;
  padding: ...;
  background: {배경색};
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  overflow: hidden;
}
/* 요소별 스타일 */
</style>
</head>
<body>
  <!-- 모든 텍스트: p, h1-h6, ul, ol 안에만 -->
  <!-- div: 배경, 테두리, 도형 역할만 -->
</body>
</html>
```

**필수 HTML 규칙 준수 체크**:
- body: `width: 720pt; height: 405pt; display: flex;`
- 텍스트: `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` 안에만
- div에 직접 텍스트 없음
- CSS gradient 없음 (linear-gradient, radial-gradient 없음)
- web-safe 폰트만 (Arial, Helvetica, Georgia, etc.)
- 수동 불릿 기호 없음 (•, -, * 등)
- 색상: #hex 형식만

**통과 조건**:
- [ ] Teammate-B Agent가 정상 생성/실행됨
- [ ] Teammate-B가 spawn 후 30초 이내에 착수 보고 (첫 진행 메시지)
- [ ] `{OUTPUT_DIR}/slides/` 에 3~5개 slide_*.html 파일 존재
- [ ] 모든 HTML에 `body { width: 720pt; height: 405pt; display: flex; }` 존재
- [ ] 모든 텍스트가 p/h1-h6/ul/ol 태그 안에 있음
- [ ] div에 직접 텍스트 없음
- [ ] CSS gradient 사용 없음
- [ ] web-safe 폰트만 사용
- [ ] 수동 불릿 문자 없음

---

### TC-07: Phase 2 — HTML 사전 검증 (validate_html.py)

**검증 항목**: validate_html.py가 각 슬라이드에 실행되고 html_validation.json이 생성되는가

**예상 실행 플로우**:

1. Teammate-B가 각 슬라이드 HTML에 대해 validate_html.py 실행
2. 에러 발생 시 즉시 수정 후 재실행
3. 모든 슬라이드 통과 후 html_validation.json 생성

**예상 명령어 로그** (Teammate-B 내부):
```bash
# 각 슬라이드 파일에 대해 실행
python ~/.claude/skills/html2pptx-converter/scripts/validate_html.py {OUTPUT_DIR}/slides/slide_00.html
python ~/.claude/skills/html2pptx-converter/scripts/validate_html.py {OUTPUT_DIR}/slides/slide_01.html
python ~/.claude/skills/html2pptx-converter/scripts/validate_html.py {OUTPUT_DIR}/slides/slide_02.html
python ~/.claude/skills/html2pptx-converter/scripts/validate_html.py {OUTPUT_DIR}/slides/slide_03.html
```

**예상 validate_html.py 출력** (각 파일별):
```
✓ slide_00.html: 0 errors, 0 warnings
✓ slide_01.html: 0 errors, 0 warnings
✓ slide_02.html: 0 errors, 0 warnings
✓ slide_03.html: 0 errors, 0 warnings
```

주의: 첫 실행에서 에러가 발생할 수 있음. Teammate-B가 수정 후 재실행하여 최종 0 errors 달성.

**예상 html_validation.json**:
```json
{
  "validated_at": "2026-03-11T...",
  "total_files": 4,
  "files": [
    {"file": "slide_00.html", "errors": [], "warnings": [], "status": "pass"},
    {"file": "slide_01.html", "errors": [], "warnings": [], "status": "pass"},
    {"file": "slide_02.html", "errors": [], "warnings": [], "status": "pass"},
    {"file": "slide_03.html", "errors": [], "warnings": [], "status": "pass"}
  ],
  "summary": {
    "pass": 4,
    "fail": 0,
    "total_errors": 0
  }
}
```

**통과 조건**:
- [ ] validate_html.py가 모든 슬라이드에 실행됨
- [ ] `{OUTPUT_DIR}/html_validation.json` 파일 존재
- [ ] JSON 파싱 가능
- [ ] `summary.fail` = 0, `summary.total_errors` = 0
- [ ] 모든 파일의 status가 "pass"

---

### TC-08: Phase 2→3 전환 — Leader의 html_validation 확인

**검증 항목**: Leader가 html_validation.json을 읽고 모든 파일이 pass인지 확인 후 Phase 3을 개시하는가

**예상 실행 플로우**:

1. Teammate-B 완료 후 Leader가 html_validation.json을 Read
2. summary.fail == 0 확인
3. 통과 시 Phase 3 진행
4. 실패 시 Teammate-B 재실행

**예상 도구 호출 (Leader)**:
```
Read({OUTPUT_DIR}/html_validation.json) → 검증 결과 확인
```

**예상 결과**: 전체 pass → Phase 3 진행

**통과 조건**:
- [ ] Leader가 html_validation.json을 읽고 검증함
- [ ] Phase 3 진행 결정 (또는 실패 시 Teammate-B 재실행)

---

### TC-09: Phase 3 — convert.js 생성 및 PPTX 변환 (Teammate-C: executor-validator)

**검증 항목**: Teammate-C가 convert.js를 생성하고 node로 실행하여 presentation.pptx를 생성하는가

**예상 실행 플로우**:

1. Leader가 Agent 도구로 Teammate-C 생성 (03-executor-validator 프롬프트)
2. Step 1: convert.js 생성 (Write)
3. Step 2: node convert.js 실행 (Bash)
4. presentation.pptx 생성 확인

**예상 Agent 스폰**:
```
Agent(
  prompt: "03-executor-validator.md 내용 + OUTPUT_DIR + SKILL_DIR + INPUT_PNG 경로",
  model: opus,
  mode: bypassPermissions,
  run_in_background: false  # 동기(foreground) 실행
)
```

**예상 convert.js 핵심 코드**:
```javascript
const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');
const html2pptx = require(path.resolve(__dirname, '..', 'engine', 'html2pptx'));

async function convert() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    // slides 디렉토리 읽기 → 정렬 → 순회 변환
    // presentation.pptx 저장
}
convert().then(...).catch(...);
```

**예상 명령어 로그 (Teammate-C 내부)**:
```bash
# Step 2: PPTX 변환 실행
cd {OUTPUT_DIR} && node convert.js
```

**예상 node 출력**:
```
변환 시작: 4개 슬라이드
변환 중: slide_00.html
변환 중: slide_01.html
변환 중: slide_02.html
변환 중: slide_03.html
완료: {OUTPUT_DIR}/presentation.pptx
변환 소요 시간: 3000~8000ms
```

**통과 조건**:
- [ ] Teammate-C Agent가 정상 생성/실행됨
- [ ] Teammate-C가 spawn 후 30초 이내에 착수 보고 (첫 진행 메시지)
- [ ] `{OUTPUT_DIR}/convert.js` 파일 존재
- [ ] convert.js의 require 경로가 상대경로 (`path.resolve(__dirname, '..', 'engine', 'html2pptx')`)
- [ ] `node convert.js` 명령이 성공적으로 실행됨 (exit code 0)
- [ ] `{OUTPUT_DIR}/presentation.pptx` 파일 존재
- [ ] presentation.pptx 파일 크기 > 0 bytes

---

### TC-10: Phase 3 — 썸네일 및 시각 비교 생성

**검증 항목**: thumbnail.py로 썸네일이 생성되고 compare_slides.py로 비교 이미지가 생성되는가

**예상 실행 플로우**:

1. Teammate-C가 thumbnail.py 실행 → thumbnails.jpg 생성
2. Teammate-C가 compare_slides.py 실행 → comparison.jpg 생성

**예상 명령어 로그 (Teammate-C 내부)**:
```bash
# Step 3: 썸네일 생성
python ~/.claude/skills/html2pptx-converter/engine/thumbnail.py \
  {OUTPUT_DIR}/presentation.pptx \
  {OUTPUT_DIR}/thumbnails \
  --cols 4

# Step 4: 시각 비교
python ~/.claude/skills/html2pptx-converter/scripts/compare_slides.py \
  ~/.claude/skills/html2pptx-converter/test/test_layout.png \
  {OUTPUT_DIR}/thumbnails.jpg \
  {OUTPUT_DIR}/comparison.jpg
```

**예상 생성 파일**:
- `{OUTPUT_DIR}/thumbnails/` — 슬라이드별 개별 PNG (slide_1.png, slide_2.png, ...)
- `{OUTPUT_DIR}/thumbnails.jpg` — 그리드 합성 이미지 (4슬라이드 × 1행 또는 2×2)
- `{OUTPUT_DIR}/comparison.jpg` — 원본 PNG vs 썸네일 나란히 비교

**통과 조건**:
- [ ] thumbnail.py 실행 성공
- [ ] `{OUTPUT_DIR}/thumbnails.jpg` 파일 존재
- [ ] `{OUTPUT_DIR}/thumbnails/` 디렉토리에 슬라이드별 PNG 존재
- [ ] compare_slides.py 실행 성공
- [ ] `{OUTPUT_DIR}/comparison.jpg` 파일 존재

---

### TC-11: Phase 3 — 시각 검사 및 validation.json 생성

**검증 항목**: Teammate-C가 thumbnails.jpg를 시각적으로 검토하고 이슈를 기록한 validation.json을 생성하는가

**예상 실행 플로우**:

1. Teammate-C가 Read로 thumbnails.jpg 확인 (시각 검토)
2. Teammate-C가 Read로 comparison.jpg 확인 (원본 비교)
3. 슬라이드별 개별 점검 (텍스트 품질, 레이아웃 품질, 콘텐츠 품질)
4. validation.json 생성 (Write)

**예상 도구 호출 (Teammate-C 내부)**:
```
Read({OUTPUT_DIR}/thumbnails.jpg)    → 전체 슬라이드 미리보기 시각 검사
Read({OUTPUT_DIR}/comparison.jpg)    → 원본 대비 비교
Read({OUTPUT_DIR}/thumbnails/slide_1.png) → 개별 슬라이드 확인 (선택적)
Write({OUTPUT_DIR}/validation.json)  → 검증 결과 기록
```

**예상 시각 검사 관찰 항목**:

| Slide | 예상 관찰 | 잠재 이슈 |
|-------|----------|----------|
| 0 | 코너 마커 5개, 헤더, 히어로 | 마커 위치 정확도, 큰 텍스트 42px→31pt 렌더링 |
| 1 | 통계 바 + 게시판 + 사이드바 | 테이블 구조 복잡, 2단 레이아웃, 태그 색상 |
| 2 | 5종 도형 + 4종 라인 | 도형 shape 정확도, border-radius, box-shadow |
| 3 | 4단 푸터 레이아웃 | 다단 레이아웃, 어두운 배경 위 밝은 텍스트 |

**예상 validation.json 구조**:
```json
{
  "execution": {
    "success": true,
    "pptx_path": "{OUTPUT_DIR}/presentation.pptx",
    "pptx_size_bytes": 50000~300000,
    "thumbnail_path": "{OUTPUT_DIR}/thumbnails.jpg",
    "comparison_path": "{OUTPUT_DIR}/comparison.jpg",
    "no_reference_image": false,
    "slides_converted": 4,
    "conversion_time_ms": 3000~10000
  },
  "validation": {
    "slides_count": 4,
    "inspected_slides": [0, 1, 2, 3],
    "issues": [
      // 0개 이슈(pass) 또는 여러 이슈(needs_fix) 가능
      // 잠재 이슈 예시:
      // - Slide 1: 테이블 텍스트 잘림 (text_cutoff, high)
      // - Slide 2: 도형 크기 불일치 (positioning, medium)
      // - Slide 0: 코너 마커 위치 편차 (positioning, medium)
    ],
    "overall_quality": "pass 또는 needs_fix"
  }
}
```

**overall_quality 결정 규칙**:
- severity:high 이슈 1개 이상 → "needs_fix"
- severity:medium 3개 이상 → "needs_fix"
- 그 외 → "pass"

**통과 조건**:
- [ ] Teammate-C가 thumbnails.jpg를 Read로 시각 확인함
- [ ] 각 슬라이드를 개별적으로 점검함 (일괄 판단 아님)
- [ ] `{OUTPUT_DIR}/validation.json` 파일 존재
- [ ] JSON 파싱 가능
- [ ] `execution.success` = true
- [ ] `slides_count`가 실제 슬라이드 수와 일치
- [ ] `inspected_slides`에 모든 슬라이드 인덱스 포함
- [ ] 발견된 이슈가 모두 `issues` 배열에 기록됨
- [ ] `overall_quality`가 severity 기준에 따라 올바르게 설정됨

---

### TC-12: Phase 3→4 전환 — Leader의 품질 판정

**검증 항목**: Leader가 validation.json을 읽고 overall_quality에 따라 Phase 4 진행 여부를 결정하는가

**예상 실행 플로우**:

1. Teammate-C 완료 후 Leader가 validation.json을 Read
2. overall_quality 값 확인:
   - "pass" → Phase 4 건너뛰고 최종 보고
   - "needs_fix" → Phase 4 (Teammate-D) 시작

**예상 도구 호출 (Leader)**:
```
Read({OUTPUT_DIR}/validation.json) → overall_quality 확인
```

**경로 A — "pass" 인 경우**:
- Phase 4 건너뜀
- presentation.pptx가 최종 결과물
- TC-14 (최종 보고)로 이동

**경로 B — "needs_fix" 인 경우**:
- Phase 4 (TC-13) 실행
- Teammate-D 생성

**통과 조건**:
- [ ] Leader가 validation.json을 읽음
- [ ] overall_quality에 따라 올바른 분기 결정
- [ ] "pass" → Phase 4 건너뜀 + 최종 보고
- [ ] "needs_fix" → Teammate-D 생성

---

### TC-13: Phase 4 — 반복 수정 (Teammate-D: iterative-fixer) [조건부]

> ⚠️ 이 TC는 TC-12에서 overall_quality == "needs_fix"인 경우에만 실행됨.
> "pass"인 경우 이 TC는 SKIP으로 기록.

**검증 항목**: Teammate-D가 이슈를 분석하고 HTML을 수정하여 재변환하고, 품질이 개선된 최종 PPTX를 생성하는가

**예상 실행 플로우**:

1. Leader가 Agent 도구로 Teammate-D 생성 (04-iterative-fixer 프롬프트)
2. Step 1: validation.json 읽기 → 이슈 분석 + 수정 계획 수립
3. Step 2: 이슈별 HTML 수정 (Edit)
4. Step 3: 재검증 루프
   - validate_html.py 실행
   - node convert.js 재실행
   - thumbnail.py 재실행
   - 시각 재검사 (Read thumbnails.jpg)
   - validation.json 업데이트
5. Step 4: presentation_final.pptx 생성 + fix_log.json 작성

**예상 Agent 스폰**:
```
Agent(
  prompt: "04-iterative-fixer.md 내용 + OUTPUT_DIR + SKILL_DIR",
  model: opus,
  mode: bypassPermissions,
  run_in_background: false  # 동기(foreground) 실행
)
```

**예상 Teammate-D 내부 도구 호출 (1 라운드 예시)**:
```
Read({OUTPUT_DIR}/validation.json)       → 이슈 목록 확인
Read({OUTPUT_DIR}/spec.json)             → 원본 설계값 참조
Read({OUTPUT_DIR}/slides/slide_XX.html)  → 수정 대상 HTML 확인
Edit({OUTPUT_DIR}/slides/slide_XX.html)  → 이슈 수정
Bash("python scripts/validate_html.py {OUTPUT_DIR}/slides/slide_XX.html") → HTML 재검증
Bash("cd {OUTPUT_DIR} && node convert.js") → 재변환
Bash("python engine/thumbnail.py ...")    → 썸네일 재생성
Read({OUTPUT_DIR}/thumbnails.jpg)         → 시각 재검사
Write({OUTPUT_DIR}/validation.json)       → 업데이트된 검증 결과
```

**예상 최대 라운드**: 1~3회

**예상 수정 내용** (잠재 이슈별):
| 이슈 | 수정 내용 |
|------|----------|
| text_cutoff | font-size 2pt 축소, line-height 1.3으로 줄임 |
| positioning | position 값 재계산, flexbox 속성 조정 |
| contrast | 텍스트 색상 명도 낮춤 (최소 4.5:1 대비) |
| missing_content | div 직접 텍스트를 p 태그로 감싸기 |

**예상 명령어 로그 (라운드 종료 시)**:
```bash
# 최종 파일 생성
cp {OUTPUT_DIR}/presentation.pptx {OUTPUT_DIR}/presentation_final.pptx
```

**예상 fix_log.json**:
```json
{
  "started_at": "2026-03-11T...",
  "completed_at": "2026-03-11T...",
  "initial_quality": "needs_fix",
  "final_quality": "pass 또는 needs_fix",
  "total_rounds": 1~3,
  "rounds": [
    {
      "round": 1,
      "issues_addressed": N,
      "fixes": [
        {
          "slide_index": X,
          "issue_type": "text_cutoff",
          "severity": "high",
          "fix_applied": "설명",
          "file_modified": "slides/slide_XX.html",
          "before_value": "18pt",
          "after_value": "14pt",
          "validate_html_passed": true,
          "result": "resolved"
        }
      ],
      "remaining_issues_count": 0,
      "round_quality": "pass"
    }
  ],
  "final_quality": "pass",
  "unresolved_issues": [],
  "output_files": {
    "pptx_final": "{OUTPUT_DIR}/presentation_final.pptx",
    "fix_log": "{OUTPUT_DIR}/fix_log.json"
  }
}
```

**통과 조건**:
- [ ] Teammate-D Agent가 정상 생성/실행됨 (needs_fix인 경우)
- [ ] Teammate-D가 spawn 후 30초 이내에 착수 보고 (첫 진행 메시지)
- [ ] 또는 overall_quality == "pass"이면 이 TC는 SKIP
- [ ] 이슈가 severity:high 우선으로 처리됨
- [ ] HTML 수정 후 validate_html.py가 실행됨
- [ ] node convert.js가 재실행됨
- [ ] thumbnails.jpg가 재생성됨
- [ ] 시각 재검사가 수행됨
- [ ] `{OUTPUT_DIR}/presentation_final.pptx` 존재 (크기 > 0)
- [ ] `{OUTPUT_DIR}/fix_log.json` 존재 (JSON 파싱 가능)
- [ ] fix_log.json에 total_rounds, before_value, after_value 기록됨
- [ ] 최대 3라운드 이내에 종료됨

---

### TC-14: 최종 보고 및 출력 파일 검증

**검증 항목**: Leader가 사용자에게 최종 결과를 보고하고 모든 출력 파일이 올바른 위치에 존재하는가

**예상 실행 플로우**:

1. Leader가 최종 결과 요약을 사용자에게 출력
2. 생성된 모든 파일 경로 안내
3. 최종 PPTX 파일명 명시 (presentation.pptx 또는 presentation_final.pptx)

**예상 최종 보고 내용**:
```
✅ HTML→PPTX 변환 완료!

📂 출력 파일:
- 스펙 JSON: {OUTPUT_DIR}/spec.json
- 슬라이드 HTML: {OUTPUT_DIR}/slides/slide_00.html ~ slide_03.html
- HTML 검증: {OUTPUT_DIR}/html_validation.json
- 변환 스크립트: {OUTPUT_DIR}/convert.js
- PPTX: {OUTPUT_DIR}/presentation.pptx (또는 presentation_final.pptx)
- 썸네일: {OUTPUT_DIR}/thumbnails.jpg
- 비교 이미지: {OUTPUT_DIR}/comparison.jpg
- 검증 결과: {OUTPUT_DIR}/validation.json
- (수정 이력: {OUTPUT_DIR}/fix_log.json — Phase 4 실행 시)
```

**예상 출력 파일 전체 목록**:

| 파일 | Phase | 필수 |
|------|-------|------|
| `spec.json` | 1 | ✅ |
| `slides/slide_00.html` ~ `slide_03.html` | 2 | ✅ |
| `html_validation.json` | 2 | ✅ |
| `convert.js` | 3 | ✅ |
| `presentation.pptx` | 3 | ✅ |
| `thumbnails.jpg` | 3 | ✅ |
| `thumbnails/` (디렉토리) | 3 | ✅ |
| `comparison.jpg` | 3 | ✅ |
| `validation.json` | 3 | ✅ |
| `presentation_final.pptx` | 4 | ⚠️ (needs_fix 시만) |
| `fix_log.json` | 4 | ⚠️ (needs_fix 시만) |

**통과 조건**:
- [ ] Leader가 사용자에게 최종 결과를 보고함
- [ ] 최종 PPTX 파일 경로가 명시됨
- [ ] 필수 출력 파일 9개 (Phase 1~3) 모두 존재
- [ ] (Phase 4 실행 시) presentation_final.pptx + fix_log.json 존재
- [ ] 모든 출력 파일이 `{OUTPUT_DIR}/` 내부에 있음 (스킬 폴더 내부가 아님)
- [ ] presentation.pptx 파일 크기 > 0 bytes

---

## 5. 전체 파이프라인 플로우 검증 체크리스트

### Phase 순서 검증
- [ ] Phase 1 (병렬): Teammate-A + Leader 파일검증이 동시에 실행됨
- [ ] Phase 1→2: spec.json 스키마 검증 후 Phase 2 시작
- [ ] Phase 2 (순차): Teammate-B가 spec.json 기반 HTML 생성
- [ ] Phase 2→3: html_validation.json 전체 pass 후 Phase 3 시작
- [ ] Phase 3 (순차): Teammate-C가 convert.js → node → thumbnail → compare → validation
- [ ] Phase 3→4: validation.json overall_quality에 따라 분기
- [ ] Phase 4 (조건부): needs_fix 시 Teammate-D가 수정 루프 실행

### 에이전트 소통 규칙 검증
- [ ] Teammate → Leader만 보고 (Teammate 간 직접 통신 없음)
- [ ] 데이터 전달은 JSON 파일 통해 (인라인 텍스트 전달 아님)
- [ ] Leader가 Phase 전환 전 중간 JSON 검증
- [ ] Teammate가 모든 출력을 `{OUTPUT_DIR}/`에만 기록 (스킬 폴더에 쓰지 않음)
- [ ] 모든 Teammate가 spawn 후 30초 이내에 착수 보고 (SKILL.md 소통 규칙)

### 엔진 참조 검증
- [ ] convert.js가 `engine/html2pptx.js`를 상대경로로 참조
- [ ] thumbnail.py가 `engine/thumbnail.py` 경로에서 실행
- [ ] validate_html.py가 `scripts/validate_html.py` 경로에서 실행
- [ ] compare_slides.py가 `scripts/compare_slides.py` 경로에서 실행

---

## 6. 예상 소요 시간

| Phase | 예상 시간 | 주요 대기 |
|-------|----------|----------|
| Phase 1 | 1~3분 | Agent 생성 + spec.json 작성 |
| Phase 2 | 2~5분 | HTML 4개 파일 생성 + validate_html.py x4 |
| Phase 3 | 2~5분 | node convert.js + thumbnail.py + compare_slides.py |
| Phase 4 | 0~8분 | 0분(pass) 또는 수정 루프 1~3회 |
| **전체** | **5~20분** | |

---

## 7. 잠재 실패 시나리오 및 예상 대응

| 시나리오 | 예상 증상 | 예상 대응 |
|---------|----------|----------|
| pptxgenjs 미설치 | `Cannot find module 'pptxgenjs'` | npm 설치 안내 |
| Playwright 미설치 | thumbnail.py 실행 실패 | `npx playwright install chromium` |
| Pillow 미설치 | compare_slides.py 실패 | `pip install Pillow` |
| spec.json 스키마 불일치 | Leader가 Phase 1→2 전환 거부 | Teammate-A 재실행 |
| HTML 검증 에러 | html_validation.json에 fail 기록 | Teammate-B 자체 수정 후 재검증 |
| node convert.js 실패 | PPTX 미생성 | Teammate-C가 에러 분석 후 수정 |
| 테이블 렌더링 복잡도 | Slide 1 텍스트 잘림 | Phase 4에서 font-size 축소 |
| 코너 마커 위치 편차 | Slide 0 positioning 이슈 | Phase 4에서 position 재계산 |
| Teammate-A Agent 무응답 | spec.json 미생성, 120초 초과 | Leader가 shutdown 후 직접 수행 (SKILL.md 규칙) |
| Teammate-B/C/D Agent 무응답 | 해당 Phase 결과물 미생성 | Leader가 shutdown 후 직접 수행 또는 재spawn |
| LibreOffice 미설치 (Windows) | thumbnail.py Stage 2 실패 | Stage 1 COM 또는 Stage 3 Playwright fallback |
| chardet 미설치 | 자동 인코딩 감지 불가 | Python built-in UTF-8 읽기로 대체 검증 |
| cp949 인코딩 파일 | UnicodeDecodeError 발생 | chardet로 감지 후 변환, 또는 사용자에게 UTF-8 변환 요청 |
| comtypes 미설치 (Windows) | PowerPoint COM 자동화 실패 | LibreOffice 또는 Playwright fallback 사용 |

---

*End of Test Plan & Expected Results*
