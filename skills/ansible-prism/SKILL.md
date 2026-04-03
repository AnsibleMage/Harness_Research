---
name: ansible-prism
description: |
  An & Ari's Creative Generation Engine — generates diverse, high-quality Korean
  landing pages and homepages. Every generation produces a structurally unique result
  through a 5-slot combination engine (3.2M+ unique combinations).

  Two modes:
  - CREATE: Generate from scratch with just a topic ("인테리어 랜딩페이지 만들어줘")
  - REDESIGN: Transform an existing wireframe with completely new visual identity

  Use this skill when:
  - User asks to create a landing page, homepage, or website from scratch
  - User provides a wireframe/HTML and wants it redesigned
  - User says "랜딩페이지", "홈페이지", "메인페이지", "웹사이트 만들어줘"
  - User asks for multiple diverse versions of the same page
  - User wants "completely different" or "unique" designs each time
  - User mentions "ansible-prism" or "/ansible-prism"
  - Any request for Korean web page generation with high design quality

  Do NOT use for: simple HTML edits, bug fixes, React/Vue components, or non-page-level work.
model: opus
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - WebFetch
  - WebSearch
---

# ansible-prism — Creative Generation Engine v4.0

> Created by An & Ari. Every generation is structurally unique.
> "One light enters the prism — infinite colors emerge."

---

## Quick Start

```
/ansible-prism 인테리어 랜딩페이지 만들어줘          → CREATE mode
/ansible-prism opt1.html 리디자인해줘                → REDESIGN mode
/ansible-prism opt1.html 3개 동시에 만들어줘          → Agent Teams 병렬
```

---

## Architecture

```
ansible-prism/
├── SKILL.md (this file) ← 오케스트레이터
└── references/
    ├── CREATIVE_GENERATION_FRAMEWORK.md  ← 메인 엔진 (FOUNDATIONS + STEPS)
    ├── CREATE_MODE.md                    ← 제로 입력 → 콘텐츠+디자인
    ├── REDESIGN_MODE.md                  ← 와이어프레임 → 시각 변환
    ├── SLOT_ENGINE.md                    ← 5슬롯 × 20값 = 320만 조합
    ├── IMAGE_ENGINE.md                   ← gradient+SVG+AI 이미지
    ├── MOTION_RULES.md                   ← 등장+hover+마이크로 인터랙션
    ├── CSS_PRECISION.md                  ← 4px그리드+다층shadow+5단계명도
    ├── VISUAL_DENSITY.md                 ← 7계층+빈공간금지
    └── TECH_SPEC.md                      ← 출력 기술 명세
```

**When to read which file:**
- Always read: `CREATIVE_GENERATION_FRAMEWORK.md` (core engine)
- Mode-specific: `CREATE_MODE.md` or `REDESIGN_MODE.md`
- Slot selection: `SLOT_ENGINE.md`
- During HTML generation: `IMAGE_ENGINE.md`, `MOTION_RULES.md`, `CSS_PRECISION.md`, `VISUAL_DENSITY.md`, `TECH_SPEC.md`

---

## Mode Routing

```
입력 분석:
  와이어프레임/HTML 파일 있음? → REDESIGN mode (references/REDESIGN_MODE.md)
  주제/업종 텍스트만 있음?     → CREATE mode   (references/CREATE_MODE.md)
```

### CREATE Mode Flow
```
"인테리어 랜딩페이지 만들어줘"
  → [0a] 도메인 분석 (업종→톤→추천 SLOT)
  → [0b] 섹션 구조 선택 (H + 본문 6~10개 + F)
  → [0c] 카피라이팅 (한국어 구어체, 구체적 숫자)
  → [0d] 내부 와이어프레임 JSON
  → [STEP 1~7] 슬롯 엔진 + 품질 모듈 → HTML
```

### REDESIGN Mode Flow
```
"opt1.html 리디자인해줘"
  → 와이어프레임 파싱 (텍스트 100% 보존)
  → [STEP 1~7] 슬롯 엔진 + 품질 모듈 → HTML
```

---

## Core Pipeline (STEP 1~7)

Read `references/CREATIVE_GENERATION_FRAMEWORK.md` for full details.

### STEP 1: RLHF SCAN
Scan for AI design patterns to avoid. Calculate A+B suppression score.

### STEP 2: OL Decision
Default: **OL 10** (Genius Originality).
- GI target: O×C×P×S ≥ 6000
- PR: T(180°) ×3 + M(ψ≥+2) ×2
- SLOT_3 must differ from previous generation

### STEP 3: Slot Selection
Read `references/SLOT_ENGINE.md` for all 100 slot values.

| Slot | Role | Values | DIM |
|------|------|--------|-----|
| SLOT_1 Visual Identity | CSS vars, border, texture, card, nav style | 20 | — |
| SLOT_2 Color Temperature | base_bg, card_bg, heading, body, accent hex | 20 | DIM_2 |
| SLOT_3 Page Structure | HTML body skeleton | 20 | DIM_1 |
| SLOT_4 Typography | font-family, display size, spacing | 20 | DIM_3 |
| SLOT_5 Accent Strategy | CSS property where accent appears | 20 | DIM_4 |

**"Real Difference" 4-Dimension Check (OL 10 mandatory):**
```
DIM_1: SLOT_3 HTML skeleton differs from previous?
DIM_2: SLOT_2 base background color family differs?
DIM_3: SLOT_4 heading font category differs?
DIM_4: SLOT_5 accent CSS property differs?
→ All 4 must differ to qualify as "truly different"
```

### STEP 4: Section Reframing (PR formula)
Apply T(θ), S(φ), M(ψ) transformations to each section.

### STEP 5: Pattern Library
Select 2~3 patterns from 72 available. Never apply all.

### STEP 6: Generate HTML
Apply all quality modules during generation:
- `IMAGE_ENGINE.md` → No gray placeholders. Gradient+SVG for every thumbnail.
- `MOTION_RULES.md` → IntersectionObserver + varied hover per section.
- `CSS_PRECISION.md` → 4px grid, 5-level color depth, multi-layer shadows.
- `VISUAL_DENSITY.md` → 7-layer visual content, no empty spaces.
- `TECH_SPEC.md` → Single HTML, embedded CSS/JS, Google Fonts + Pretendard CDN.

### STEP 7: Self-Audit
Run all checklists from CREATIVE_GENERATION_FRAMEWORK.md §STEP 7.

---

## Output Specification

```
Format:   Single .html file (self-contained)
CSS:      Embedded <style> (no external CSS)
JS:       Embedded <script> (IntersectionObserver, tab switching)
Fonts:    Google Fonts CDN + Pretendard CDN
Images:   CSS gradient + inline SVG only (zero external images)
Naming:   {NN}_{slug}.html (e.g., 01_interior_landing.html)
```

**CSS Metadata (mandatory, top of style block):**
```css
/*
FRAMEWORK: v4.0
ENGINE: ansible-prism
MODE: CREATE | REDESIGN
OL: 10
WORLD: "{世界觀 1문장}"
SLOTS: identity={1-XX} | color={2-XX} | structure={3-XX} | typo={4-XX} | accent={5-XX}
*/
```

---

## Agent Teams (Parallel Generation)

When user requests multiple versions simultaneously:

```
"3개 동시에 만들어줘" → 3 Agent Teams in parallel
```

Each agent receives:
1. Unique slot combination (all 4 DIM must differ between agents)
2. Same wireframe/topic
3. Full reference to all modules
4. Sequential file naming (01_, 02_, 03_)

Pre-verify 4-DIM cross-check between all agent pairs before spawning.

---

## Visual Floor (Always Applied)

```yaml
typography:
  minimum: 14px
  body: 16px+
  badge_text: 14px+

card:
  border-radius: "0 or 4~8px" (12px+ banned)
  min-width: 260px
  min-height: 120px
  padding: 20px+

spacing:
  section_padding: 32px+
  gap: 12px+
```

---

## Anti-AI Design Clichés (Banned)

```
layout:    Split dark/light hero, uniform 3-col cards, identical hover
color:     Purple-blue gradient, uniform accent distribution
typography: Same heading size everywhere, all-uppercase labels
component:  ★★★★★ ratings, emoji+title+desc feature cards
motion:     Uniform fadeInUp on everything, identical scale(1.03) hover
```

---

## Constraint Hierarchy

```
1. World-Building    — SOUL. 세계관이 모든 결정의 원천
2. Wireframe Content — LAW. 콘텐츠 100% 보존 (REDESIGN mode)
3. Quality Modules   — CRAFT. IMAGE+MOTION+CSS+DENSITY 필수
4. Typography Floor  — RULE. 14px 최소
5. Anti-Pattern      — GUARD. RLHF 패턴 차단
6. GI Formula        — COMPASS. 분자↑ 분모↓
7. IL Paradox        — WISDOM. 규칙 과다 = 도약 사망
8. Pattern Library   — DICTIONARY. 2~3개만 참고
```
