# Supanova Design Skill 통합 개선안

> 작성일: 2026-03-21
> 목적: 4개 개별 스킬을 1개의 통합 스킬로 합쳐 품질과 효율을 동시에 향상

---

## 1. 현황 분석

### 1.1 4개 스킬 정량 요약

| 스킬 | 파일 | 줄 수 | 핵심 역할 |
|------|------|-------|-----------|
| **taste-skill** | `taste-skill/SKILL.md` | 213줄 | 메인 디자인 엔진 — 설정값 시스템, 디자인 규칙 6개, 섹션 라이브러리 17종, HTML 템플릿 |
| **redesign-skill** | `redesign-skill/SKILL.md` | 142줄 | 기존 페이지 업그레이드 — Scan-Diagnose-Fix 워크플로우, 감사 체크리스트, Fix Priority |
| **soft-skill** | `soft-skill/SKILL.md` | 121줄 | $150k 에이전시 품질 — Creative Variance Engine, Double-Bezel 카드, 모션 안무 |
| **output-skill** | `output-skill/SKILL.md` | 93줄 | AI 출력 생략 방지 — Banned Patterns, PAUSE/CONTINUE 메커니즘 |
| **합계** | | **569줄** | |

### 1.2 현재 구조의 문제점

1. **중복**: 7개 영역에서 ~200줄이 3중 반복 (전체의 35%)
2. **불일치**: 동일 규칙이 스킬마다 미묘하게 다른 표현 (예: 패딩 값, 금지 폰트 목록)
3. **사용자 부담**: 상황에 따라 스킬 조합을 직접 선택해야 함 (README의 "추천 조합" 테이블)
4. **누락 영역**: 접근성(WCAG), SEO, 다크/라이트 모드 지원이 4개 스킬 어디에도 없음

---

## 2. 중복 매트릭스 (7개 영역)

### 2.1 타이포그래피 (~35줄 중복, 3곳)

| 규칙 | taste (Rule 1) | soft (4.C) | redesign (Typography) |
|------|---------------|------------|----------------------|
| Pretendard 필수 | 22줄 | 27줄 암시 | 20줄 |
| Banned fonts (Inter, Noto Sans KR 등) | 45줄 | 16줄 | 20줄 |
| Korean `leading-tight`/`leading-snug` | 41줄 | 57줄 | 21줄 |
| `break-keep-all` | 42줄 | 57줄 | 22줄 |
| 영어 디스플레이 폰트 목록 | 23줄 | 27줄 | 20줄 |
| `max-w-[65ch]` body | 44줄 | — | 23줄 |

### 2.2 컬러/서피스 (~20줄 중복, 3곳)

| 규칙 | taste (Rule 2) | soft (Absolute Zero) | redesign (Color) |
|------|---------------|---------------------|------------------|
| Purple/AI 그라디언트 금지 | 49줄 | 14줄 | 33줄 |
| Saturation < 80% | 48줄 | — | 31줄 |
| 1 Accent Color 규칙 | 48줄 | — | 32줄 |
| Dark mode 기본 | 52줄 | 27줄 (Vantablack) | — |
| Tinted shadow | 65줄 | 18줄 | 34,122줄 |

### 2.3 안티패턴/금지 규칙 (~40줄 중복, 3곳)

taste Section 7 (AI Tells) 전체가 soft Section 2 (Absolute Zero)와 redesign 감사 체크리스트에 분산 반복.

| 금지 항목 | taste 7 | soft 2 | redesign |
|----------|---------|--------|----------|
| Banned fonts | O | O | O |
| Banned icons | 암시 | O | O |
| Banned borders/shadows | — | O | O |
| Banned layouts (3-col equal) | O | O | O |
| Banned motion (linear) | — | O | — |
| Banned content (AI cliche) | O | O | O |
| No emoji | O | — | — |
| No round numbers | O | — | O |
| No Unsplash | O | — | O |

### 2.4 퍼포먼스 가드레일 (~10줄 중복, 2곳)

taste Section 5와 soft Section 6이 거의 동일. taste가 z-index 규칙을, soft가 backdrop-blur 제한을 추가로 보유.

### 2.5 한국어 콘텐츠 (~25줄 중복, 3곳)

| 항목 | taste (Rule 6) | soft (Section 7) | redesign (Korean) |
|------|---------------|-----------------|-------------------|
| 자연스러운 한국어 | O | O | O |
| 합니다/하세요 통일 | O | O | O |
| CTA 예시 | O | O | — |
| AI cliche 금지 | O | — | O |
| 이름/기업/직함/메트릭 예시 | 부분 | **가장 상세** | 부분 |

### 2.6 아이콘/이미지 (~8줄 중복, 2곳)

taste Section 2와 redesign Icons audit에서 Iconify Solar, picsum.photos, i.pravatar.cc 동일 반복.

### 2.7 섹션 구조/완전성 (~15줄 중복, 2곳)

taste Section 8 Formula (7개 필수 섹션)와 output Required Elements (11개)가 동일 구조를 다른 형식으로 표현.

### 중복 요약

| 영역 | 중복 줄 수 | 관련 스킬 |
|------|-----------|----------|
| 타이포그래피 | ~35줄 | taste + soft + redesign |
| 컬러/서피스 | ~20줄 | taste + soft + redesign |
| 안티패턴 | ~40줄 | taste + soft + redesign + output |
| 퍼포먼스 | ~10줄 | taste + soft |
| 한국어 콘텐츠 | ~25줄 | taste + soft + redesign |
| 아이콘/이미지 | ~8줄 | taste + redesign |
| 섹션 구조 | ~15줄 | taste + output |
| **합계** | **~153줄** | |

> 실제 중복은 교차 참조와 부분 중복을 포함하면 **~200줄**로 추정 (전체의 35%)

---

## 3. 고유 가치 보존 분석

각 스킬에서 **다른 스킬에 존재하지 않는** 고유 요소를 식별합니다. 통합 시 이 요소들은 100% 보존되어야 합니다.

### 3.1 taste-skill 고유 가치

| 요소 | 원본 위치 | 통합 배치 |
|------|----------|----------|
| **설정값 시스템** (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, LANDING_PURPOSE) | Section 1 (8-14줄) | Section 1 |
| **섹션 라이브러리** (Hero 4종, Feature 4종, Social Proof 4종, CTA 3종, Footer 2종 = 17패턴) | Section 6 (98-126줄) | Section 6 |
| **HTML Document Setup 템플릿** (코드 블록) | Section 8.A (161-183줄) | Section 2 |
| **Pre-flight Check** (11항목) | Section 9 (201-213줄) | Section 11 |
| **Creative Proactivity 패턴** (Liquid Glass, Magnetic CTA, Staggered Reveals, Float, Gradient Mesh, Scroll-Triggered) | Section 4 (82-89줄) | Section 5 |

### 3.2 redesign-skill 고유 가치

| 요소 | 원본 위치 | 통합 배치 |
|------|----------|----------|
| **Scan-Diagnose-Fix 워크플로우** | 10-14줄 | Section 7 |
| **7단계 Fix Priority** (Font→Color→Korean→Hover→Layout→Animation→Polish) | 124-134줄 | Section 7 |
| **Upgrade Techniques** (Typography/Layout/Motion/Surface 각 3-4개) | 99-122줄 | Section 7 |
| **점진적 개선 규칙** (기존 구조 유지, 전체 재작성 금지) | 136-142줄 | Section 7 |

### 3.3 soft-skill 고유 가치

| 요소 | 원본 위치 | 통합 배치 |
|------|----------|----------|
| **Creative Variance Engine** — Vibe Archetypes 3종 (Vantablack Luxe, Warm Editorial, Clean Structural) | Section 3.A (26-29줄) | Section 5 |
| **Layout Archetypes** 3종 (Asymmetrical Bento, Z-Axis Cascade, Editorial Split) + 모바일 collapse | Section 3.B (31-38줄) | Section 5 |
| **Double-Bezel Card Architecture** (outer shell + inner core) | Section 4.A (43-46줄) | Section 5 |
| **Premium CTA Button Architecture** (pill + nested icon + hover physics + glow) | Section 4.B (48-52줄) | Section 5 |
| **Spatial Rhythm** (Macro-Whitespace py-24~py-40, Eyebrow Tags) | Section 4.C (54-57줄) | Section 5 |
| **Motion Choreography** (Floating Glass Nav, Perpetual Micro-Motion) | Section 5 (59-86줄) | Section 5 |
| **$150k 에이전시 페르소나** | Section 1 (9-11줄) | Section 1 |

### 3.4 output-skill 고유 가치

| 요소 | 원본 위치 | 통합 배치 |
|------|----------|----------|
| **Execution Process** (Scope→Build→Cross-check) | 40-44줄 | Section 9 |
| **PAUSE/CONTINUE 메커니즘** (토큰 한계 대응) | 48-58줄 | Section 9 |
| **Completeness Standards** (Required Elements 11개 + Required Quality 5개) | 62-83줄 | Section 9 |

---

## 4. 통합 아키텍처 설계

### 4.1 설계 원칙

1. **Single Source of Truth** — 모든 규칙은 정확히 1곳에만 존재
2. **Mode-Based Routing** — 새 생성(CREATE) vs 리디자인(REDESIGN) 자동 판별
3. **고유 가치 100% 보존** — 각 스킬의 고유 요소 전부 유지
4. **신규 개선 요소 통합** — 접근성, SEO, 다크/라이트 모드, 반응형 테스트
5. **토큰 효율 극대화** — 중복 제거로 52% 줄 수 절감

### 4.2 통합 스킬 11개 섹션 구조

```
Section 1:  Identity & Configuration       — 설정값 + 모드 라우팅
Section 2:  Architecture & Conventions      — 기술 스택 + HTML 템플릿
Section 3:  Anti-Pattern Registry           — 통합 금지 규칙 (Single Source)
Section 4:  Design Engineering              — 타이포/컬러/레이아웃/깊이/전환UI/한국어
Section 5:  Creative Variance Engine        — 아키타입 + 프리미엄 컴포넌트 + 모션
Section 6:  Section Library                 — 17종 랜딩페이지 패턴
Section 7:  Redesign Protocol               — Scan-Diagnose-Fix + Priority
Section 8:  Accessibility & SEO             — [신규] WCAG + OG + 반응형
Section 9:  Output Enforcement              — 생략 방지 + PAUSE/CONTINUE
Section 10: Performance Guardrails          — 통합 퍼포먼스
Section 11: Pre-Output Checklist            — 모드별 최종 검증
```

### 4.3 각 섹션 상세 설계

---

#### Section 1: Identity & Configuration (~20줄)

**역할**: 스킬 정체성 + 설정값 시스템 + 모드 자동 라우팅

**출처**: taste Section 1 (설정값) + soft Section 1 (페르소나) + 신규 (라우팅)

**핵심 내용**:
- frontmatter: name `supanova-unified`, description 통합 설명
- 페르소나: `Supanova_Design_Director` — $150k 에이전시 수준의 랜딩페이지 생성
- 변동 불가 지시: "AI 템플릿이 아닌 핸드크래프트 느낌, 동일 레이아웃 재사용 금지"
- 4개 설정값:
  - `DESIGN_VARIANCE: 8` (1=대칭, 10=비대칭)
  - `MOTION_INTENSITY: 6` (1=정적, 10=시네마틱)
  - `VISUAL_DENSITY: 3` (1=럭셔리, 10=데이터 밀집)
  - `LANDING_PURPOSE: conversion` (conversion/brand/portfolio/saas/ecommerce)
- 동적 오버라이드: 사용자 프롬프트에 명시된 값으로 자동 조정
- **[신규] Mode Routing**:
  - `CREATE` 모드: 프롬프트에 기존 HTML 없음 → Section 2-6, 8-11 전체 적용
  - `REDESIGN` 모드: 프롬프트에 기존 HTML 코드/파일 포함 → Section 7 우선 적용 → 나머지 참조
  - 자동 판별 기준: 기존 HTML 코드 또는 "기존", "업그레이드", "개선", "리디자인" 키워드 감지

**중복 제거**: soft의 페르소나(9-11줄)를 여기에 흡수

---

#### Section 2: Architecture & Conventions (~25줄)

**역할**: 기술 스택, CDN, 출력 형식, 반응형 규범, HTML 템플릿

**출처**: taste Section 2 (16-34줄) + taste Section 8.A (Document Setup 코드 블록)

**핵심 내용**:
- 출력 형식: 단일 standalone HTML 파일 (빌드 도구 없음)
- 기술 스택:
  - Tailwind CSS CDN (`cdn.tailwindcss.com`)
  - Pretendard 폰트 CDN (비협상 사항)
  - Iconify Solar 아이콘 세트
  - Motion One (MOTION_INTENSITY > 5일 때 조건부)
- 영어 디스플레이 폰트: Geist, Outfit, Cabinet Grotesk, Satoshi 중 택 1
- HTML Document Setup 코드 블록 (<!DOCTYPE html> 템플릿)
- tailwind.config 확장 블록
- 반응형 규범: `max-w-7xl mx-auto`, `min-h-[100dvh]`, Grid over Flex-Math
- ANTI-EMOJI POLICY: 마크업 내 이모지 금지, Iconify Solar 또는 SVG로 대체
- 기본 언어: 한국어

**변경점**: taste Section 8.A의 Document Setup 코드를 기술 규범과 함께 배치하여 논리적 흐름 개선

---

#### Section 3: Anti-Pattern Registry (~35줄)

**역할**: 금지 규칙 단일 저장소 — 3-4곳에 분산되던 "하지 말 것"을 1곳으로 통합

**출처**: taste Section 7 (AI Tells) + soft Section 2 (Absolute Zero) + redesign 감사항목 내 금지사항 + output Banned Patterns

**구조** (카테고리별 정리):

```
Typography Bans
  - Banned fonts: Inter, Noto Sans KR, Roboto, Arial, Open Sans, Helvetica, Malgun Gothic
  - leading-none on Korean text

Visual Bans
  - Pure #000000 → #0a0a0a 또는 zinc-950
  - Purple/blue AI gradients
  - Oversaturated accents (>80%)
  - Neon/outer glows → inner borders 또는 tinted shadows
  - Generic box-shadow rgba(0,0,0,0.3) → background hue tinted
  - Excessive gradient text (max 1/page)

Icon & Image Bans
  - Lucide, FontAwesome, Material Icons → Iconify Solar only
  - Unsplash URLs → picsum.photos/seed/{name}/{w}/{h}
  - Emoji in markup → Iconify Solar 또는 SVG

Layout Bans
  - 3-column equal card rows → Bento, zig-zag, asymmetric
  - Identical adjacent section layouts
  - Sticky top navbar glued to edge → floating glass pill
  - h-screen → min-h-[100dvh]
  - Edge-to-edge content without max-w container

Motion Bans
  - linear 또는 ease-in-out → cubic-bezier(0.16, 1, 0.3, 1)
  - window.addEventListener('scroll') → IntersectionObserver
  - Instant state changes without transition

Content Bans
  - AI cliches: "혁신적인", "원활한", "차세대", "게임 체인저", "한 차원 높은"
  - "김철수", "이영희" → 현실적 한국 이름
  - Round numbers (50,000+) → organic numbers (47,200+)
  - Lorem Ipsum, 영문 placeholder
  - Mixed honorific levels (반말/존댓말)

Output Bans
  - <!-- ... -->, <!-- rest of sections -->, // ...
  - "Let me know if you want me to continue"
  - "The rest follows the same pattern"
  - Skeleton/wireframe when full page requested
  - Describing HTML instead of writing it
```

**절감**: taste 7 (25줄) + soft 2 (8줄) + redesign 분산 (~15줄) + output Banned (23줄) = ~71줄 → ~35줄 (**49% 절감**)

---

#### Section 4: Design Engineering (~40줄)

**역할**: 구현해야 할 디자인 규칙의 긍정 표현 ("해야 할 것"만 여기에)

**출처**: taste Section 3 (Rule 1-6) + soft Section 4.C/7 + redesign Typography/Color/Korean

**구조**:

```
4.1 Typography System
  - Korean Headlines: text-4xl md:text-5xl lg:text-6xl tracking-tight leading-tight font-bold
  - Korean Body: leading-relaxed, break-keep-all, max-w-[65ch]
  - English Display: tracking-tighter leading-none
  - Weight Hierarchy: Regular(400) → Medium(500) → SemiBold(600) → Bold(700)
  - Numbers: font-variant-numeric: tabular-nums
  - Headings: text-wrap: balance

4.2 Color System
  - Max 1 Accent Color, Saturation < 80%
  - Supanova Palette: deep neutrals (Zinc-900, Slate-950, Stone-100) + ONE accent
  - Color consistency: warm/cool gray 혼합 금지
  - Dark mode default (프리미엄 느낌)
  - Tinted shadows (background hue 매칭)

4.3 Layout Diversification
  - DESIGN_VARIANCE > 4: centered Hero 금지
    → Split Screen / Asymmetric / Full-bleed overlay
  - 인접 섹션은 반드시 서로 다른 레이아웃 패턴
  - 섹션 플로우 예시: Hero → Features(Bento) → Social Proof(Masonry) → CTA(Full-bleed)

4.4 Materiality & Depth
  - 카드: elevation은 hierarchy 표현 시에만
  - Glass Effects: backdrop-blur + border-white/10 + inset shadow
  - Grain texture: fixed pointer-events-none noise overlay
  - Overlap/Depth: negative margins, z-index layering

4.5 Conversion-Driven UI
  - CTA: hover(scale-1.02), active(scale-0.98), focus states, min px-8 py-4 text-lg
  - Social Proof: organic numbers, 현실적 한국 이름
  - Trust Signals: client logos / testimonials / metrics / press (최소 1개)
  - Urgency (conversion 모드): countdown, limited spots, currently viewing

4.6 Korean Content Standards
  - Native Korean writing (번역체 금지)
  - 합니다/하세요 form 일관 유지
  - Action-oriented CTA: "무료로 시작하기", "3분만에 만들어보기", "지금 바로 체험하기"
  - Realistic Data Pool:
    - 이름: 하윤서, 박도현, 이서진, 김하늘, 정민준, 오예린, 최시우, 한지원
    - 기업: 스텔라랩스, 베리파이, 루미너스, 플로우캔버스, 넥스트비전, 브릿지웍스
    - 직함: 프로덕트 디자이너, 스타트업 대표, 마케팅 리드, 프론트엔드 개발자, 브랜드 디렉터
    - 메트릭: 47,200+, 4.87/5.0, 2.3초, 98.7%, 12,847개
```

**절감**: taste Rule 1-6 (43줄) + soft 4.C+7 (15줄) + redesign Typography/Color/Korean (40줄) = ~98줄 → ~40줄 (**59% 절감**)

---

#### Section 5: Creative Variance Engine (~35줄)

**역할**: 프리미엄 디자인 차별화 요소 — soft의 핵심 고유 가치 + taste의 Creative Proactivity 통합

**출처**: soft Section 3-5 (Variance Engine, Haptic, Motion) + taste Section 4 (Creative Proactivity)

**구조**:

```
5.1 Vibe & Texture Archetypes (코드 작성 전 1개 선택)
  1. Vantablack Luxe (SaaS/AI/Tech): OLED black #050505, mesh gradient orbs, glass cards, Grotesk display
  2. Warm Editorial (Lifestyle/Brand/Agency): creams #FDFBF7, serif English headings, CSS noise paper texture
  3. Clean Structural (Consumer/Health/Portfolio): white/silver-grey, massive bold typography, ultra-diffused shadows

5.2 Layout Archetypes (1개 선택)
  1. Asymmetrical Bento Grid: CSS Grid col-span-8 / col-span-4, mobile → grid-cols-1
  2. Z-Axis Cascade: 카드 오버랩 + 미세 회전, mobile → 회전/음수 마진 제거
  3. Editorial Split: 좌 massive typography + 우 interactive content, mobile → 풀폭 스택

5.3 Haptic Component Patterns
  - Double-Bezel Card: outer shell(bg-white/5, ring-1 ring-white/10, p-1.5, rounded-[2rem])
                        + inner core(distinct bg, inset shadow, rounded-[calc(2rem-0.375rem)])
  - Premium CTA Button: rounded-full px-8 py-4 + nested icon circle(w-8 h-8 rounded-full)
                         + hover:scale-1.02 + active:scale-0.98 + glow effect(dark)
  - Spatial Rhythm: section py-24 md:py-32 lg:py-40
                    + Eyebrow Tags(rounded-full px-3 py-1 text-[11px] uppercase tracking-[0.15em])

5.4 Motion Choreography
  - Transition Standard: all 0.5s cubic-bezier(0.16, 1, 0.3, 1) — 모든 interactive 요소
  - Floating Glass Nav: pill(mt-4 mx-auto w-max rounded-full) + backdrop-blur-xl bg-white/10
                        + mobile: full-screen overlay with stagger-reveal
  - Scroll Entry: fadeInUp(opacity:0 → 1, translateY:2rem → 0, blur:4px → 0)
                  + IntersectionObserver + stagger delay calc(var(--index) * 80ms)
  - Perpetual Micro-Motion: floating orbs(6s ease-in-out infinite), gradient rotation, marquee logos

5.5 Creative Implementation Patterns
  - Liquid Glass Refraction: backdrop-blur-xl + border-white/10 + inset shadow + bg-white/5
  - Magnetic CTA: cubic-bezier hover + directional arrow shift
  - Staggered Reveals: animation-delay cascade (var(--index) * 100ms)
  - Gradient Mesh Backgrounds: multiple radial-gradient layers for organic ambient
```

**절감**: soft 3-5 (63줄) + taste 4 (8줄) = ~71줄 → ~35줄 (**51% 절감**). Liquid Glass/Magnetic CTA 등 양쪽에 있던 내용을 병합.

---

#### Section 6: Section Library (~30줄)

**역할**: 사용 가능한 랜딩페이지 섹션 패턴 라이브러리 + 필수 섹션 순서

**출처**: taste Section 6 (98-126줄) + taste Section 8.B/C (Mandatory Order + Philosophy)

**핵심 내용**:

```
Hero Sections (4종)
  - Split Hero: 60/40 text-to-visual, gradient bleed
  - Full-Bleed Media Hero: full-screen + dark overlay + floating CTA
  - Minimal Statement Hero: text-7xl+ massive typography + extreme whitespace
  - Interactive Hero: typewriter cycling use cases

Feature Sections (4종)
  - Bento Grid: asymmetric 2fr 1fr 1fr, varying heights
  - Zig-Zag Alternating: image-left/text-right → text-left/image-right
  - Icon Strip: horizontal scrolling with hover reveals
  - Comparison Table: Before/After or Us/Them

Social Proof Sections (4종)
  - Logo Cloud: auto-scrolling marquee, grayscale → color hover
  - Testimonial Masonry: staggered heights, photo avatars
  - Metrics Bar: animated counting, organic numbers
  - Case Study Cards: before/after screenshots

CTA Sections (3종)
  - Full-Bleed CTA: dark bg, massive text, glowing accent button
  - Sticky Bottom CTA: fixed bottom bar after hero scroll
  - Inline CTA: embedded in content flow

Footer (2종)
  - Minimal: logo, essential links, language selector, copyright
  - Rich: company description, nav links, social icons, newsletter

Mandatory Section Order (최소 7개)
  Nav → Hero → Social Proof Strip → Features → Testimonials → CTA → Footer

Design Philosophy
  - Premium by Default: 모든 픽셀이 의도적
  - Korean-Native: 한국인이 한국인을 위해 디자인한 느낌
  - Conversion-Focused: 모든 섹션이 CTA로 유도
  - Mobile-First: 한국 웹 트래픽 70%+ 모바일
```

---

#### Section 7: Redesign Protocol (~30줄)

**역할**: 기존 페이지 업그레이드 전용 워크플로우 (REDESIGN 모드에서만 활성화)

**출처**: redesign-skill 고유 가치

**핵심 내용**:

```
7.1 Workflow: Scan → Diagnose → Fix
  - Scan: HTML/CSS 읽기, 스타일링 방법/패턴/폰트/컬러/레이아웃 식별
  - Diagnose: Section 3(Anti-Pattern) + Section 4(Design Engineering) 기준으로 감사
  - Fix: 점진적 개선, 기존 구조 유지

7.2 Audit Checklist (Section 3/4 참조 기반)
  - Typography → Section 4.1 기준
  - Color/Surfaces → Section 4.2 + 3.Visual 기준
  - Layout → Section 4.3 + 3.Layout 기준
  - Interactivity → hover/active/transition/scroll animation 유무
  - Korean Content → Section 4.6 기준
  - Icons/Images → Section 3.Icon 기준
  - Code Quality → semantic HTML, meta tags, lang="ko", loading="lazy", alt text, z-index

7.3 Upgrade Techniques
  Typography: animated reveals, gradient text(1/page), variable weight hover
  Layout: broken grid/asymmetry, parallax, sticky scroll stacking, bleed transitions
  Motion: staggered cascades, spring hover, scroll-driven progress, marquee
  Surface: true glassmorphism, mesh gradients, noise overlay, tinted shadows

7.4 Fix Priority (impact → risk 순서)
  1. Font swap to Pretendard → 2. Color palette cleanup → 3. Korean content rewrite
  → 4. Hover/active states → 5. Layout diversification → 6. Section animation → 7. Polish

7.5 Rules
  - 처음부터 재작성 금지. 기존 구조 위에 점진적 개선.
  - 출력은 단일 standalone HTML 유지
  - CDN URL 추가 전 정확성 검증
  - 집중적 개선 > 전면 재작성
```

**중복 제거 효과**: redesign 원본 142줄에서 타이포/컬러/한국어 규칙 상세 내용(다른 섹션과 중복)을 "Section 3/4 기준으로 진단"이라는 참조로 대체. 고유 워크플로우/Priority/Techniques는 100% 보존. **142줄 → ~30줄** (79% 절감, 중복분만)

---

#### Section 8: Accessibility & SEO — [신규] (~15줄)

**역할**: 현재 4개 스킬에 모두 부재한 접근성, SEO, 다크/라이트 모드 지원

**핵심 내용**:

```
8.1 Accessibility (WCAG 2.1 AA)
  - Semantic HTML: nav, main, section, article, footer (div soup 금지)
  - Color contrast: 4.5:1 body text, 3:1 large text
  - ARIA labels: 모든 interactive 요소(버튼, 링크, 폼)에 aria-label
  - Keyboard navigation: focusable CTAs, skip-to-content link
  - Image alt text: 한국어 설명문
  - prefers-reduced-motion: 모션 비활성화 대응 (@media query)

8.2 SEO Essentials
  - <title> + <meta name="description"> (이미 보유, 강화)
  - Open Graph: og:title, og:description, og:image, og:url
  - Structured data: JSON-LD (Organization 또는 Product)
  - Canonical URL
  - lang="ko" (이미 보유)

8.3 Dark/Light Mode (선택적)
  - prefers-color-scheme 미디어 쿼리 대응
  - CSS custom properties로 테마 변수 관리
  - 토글 버튼 제공 여부는 LANDING_PURPOSE에 따라 판단

8.4 Responsive Testing Guide
  - 필수 브레이크포인트: 375px(iPhone SE), 390px(iPhone 14), 768px(iPad), 1024px(Desktop), 1440px(Wide)
  - iOS Safari 뷰포트: 100dvh 확인
  - 터치 타겟: 최소 48x48px
```

---

#### Section 9: Output Enforcement (~20줄)

**역할**: AI 출력 생략 방지 메커니즘 (output-skill의 핵심 고유 가치)

**출처**: output-skill (Banned Patterns는 Section 3으로 이동됨)

**핵심 내용**:

```
9.1 Execution Process
  1. Scope: 전체 요청 파악, 섹션 수 lock (랜딩페이지 = 최소 7개)
  2. Build: 모든 섹션을 완전 생성 (responsive, animation, Korean content, Iconify icons)
  3. Cross-check: <!DOCTYPE html> ~ </html> 완전성, 모든 섹션 존재 여부 확인

9.2 Long Output Handling (PAUSE/CONTINUE)
  - 토큰 한계 근접 시: 압축하지 않음, footer로 건너뛰지 않음
  - 완전한 </section> 태그에서 깔끔하게 중단
  - PAUSE 메시지: "[PAUSED — X of Y sections complete. Send 'continue' to resume from: next section name]"
  - CONTINUE 시: 중단 지점 바로 다음부터 재개, <head> 재출력 없음, recap 없음

9.3 Completeness Standards
  Required Elements:
  - <!DOCTYPE html> with <html lang="ko">
  - Complete <head> (meta, Tailwind CDN, Pretendard, Iconify, tailwind.config)
  - Navigation (floating glass or minimal bar)
  - Hero section (above the fold)
  - Trust/social proof element
  - Feature presentation (3-5 features minimum)
  - Testimonials or case studies
  - Primary CTA section
  - Footer
  - Scroll animation JavaScript (IntersectionObserver)
  - Complete </html> closing

  Required Quality:
  - 모든 섹션에 실제 한국어 콘텐츠 (placeholder 없음)
  - 모든 섹션에 full responsive classes (sm:, md:, lg:)
  - 모든 interactive 요소에 hover/active states
  - 모든 이미지에 loading="lazy", alt text, valid src
  - 모든 아이콘에 <iconify-icon icon="solar:...">
```

**절감**: output 원본 93줄에서 Banned Patterns(23줄)를 Section 3으로 이동 → **93줄 → ~20줄** (78% 절감)

---

#### Section 10: Performance Guardrails (~10줄)

**역할**: 통합 퍼포먼스 규칙

**출처**: taste Section 5 + soft Section 6 병합

**핵심 내용**:

```
- GPU-safe Animation: transform과 opacity만 animate. top/left/width/height 금지.
- DOM Cost: grain/noise filter는 position:fixed, pointer-events-none, z-[60]에만.
- Blur Constraints: backdrop-blur는 fixed/sticky 요소에만. 스크롤 컨테이너 금지.
- Image Optimization: below-fold 이미지에 loading="lazy" + decoding="async".
- CDN Discipline: 외부 CDN 최대 5개 (Tailwind + Iconify + Pretendard + Motion One + 1).
- Z-Index Scale: nav(40), overlay(50), decorative/noise(60). 다른 값 사용 자제.
```

---

#### Section 11: Pre-Output Checklist (~15줄)

**역할**: 최종 검증 통합 체크리스트 (모드별 분리)

**출처**: taste Section 9 (11항목) + soft Section 8 (13항목) + output Quick Check (6항목) 병합

**구조**:

```
CREATE Mode Checklist:
  [ ] Standalone HTML, 브라우저에서 직접 열림
  [ ] Pretendard loaded as primary font
  [ ] Iconify Solar for all icons
  [ ] All text in natural Korean, break-keep-all 적용
  [ ] min-h-[100dvh] 사용 (h-screen 아님)
  [ ] Mobile layout (w-full, px-4) 전 섹션
  [ ] CTA min 48px height (mobile tap target)
  [ ] 인접 섹션마다 서로 다른 layout pattern
  [ ] Vibe + Layout archetype 의식적 선택 완료
  [ ] Double-Bezel cards, pill CTAs with nested icons
  [ ] All transitions: cubic-bezier(0.16, 1, 0.3, 1)
  [ ] Scroll entry animations present (정적 출현 없음)
  [ ] Section padding minimum py-24
  [ ] ARIA labels on interactive elements
  [ ] Color contrast 4.5:1 verified
  [ ] Complete HTML from <!DOCTYPE> to </html>
  [ ] Zero banned patterns (Section 3 전체 검증)
  [ ] $150k agency feel, not AI template

REDESIGN Mode Checklist:
  [ ] Scan-Diagnose-Fix 워크플로우 완료
  [ ] Fix Priority 순서 준수
  [ ] 기존 구조 보존 (전면 재작성 없음)
  [ ] 7개 감사 카테고리 전부 확인
  [ ] Standalone HTML 출력 유지
```

---

## 5. 신규 개선 요소 상세

### 5.1 Mode Routing (Section 1)

**문제**: 현재 사용자가 "새로 만들기"인지 "기존 개선"인지를 스킬 선택으로 직접 결정해야 함.

**개선**: 프롬프트 내용을 기반으로 자동 모드 판별.

| 판별 기준 | 모드 | 적용 섹션 |
|----------|------|----------|
| 프롬프트에 기존 HTML 코드 포함 | REDESIGN | Section 7 우선 → 3/4/5 참조 |
| "기존", "업그레이드", "개선", "리디자인" 키워드 | REDESIGN | Section 7 우선 → 3/4/5 참조 |
| 위 조건 없음 (새 생성 요청) | CREATE | Section 2-6, 8-11 전체 |
| 명시적 모드 지정 ("CREATE로", "REDESIGN으로") | 사용자 지정 | 해당 모드 |

### 5.2 접근성 (Section 8, 신규)

**문제**: 4개 스킬 어디에도 WCAG, ARIA, 키보드 네비게이션 언급 없음. 프리미엄 랜딩페이지라면 접근성은 필수.

**개선**: WCAG 2.1 AA 기준 최소 요구사항 + prefers-reduced-motion 대응.

### 5.3 SEO 강화 (Section 8, 신규)

**문제**: taste에 기본 meta 태그만 있고 Open Graph, JSON-LD, canonical이 없음.

**개선**: OG 태그 + JSON-LD structured data + canonical URL 템플릿 제공.

### 5.4 다크/라이트 모드 (Section 8, 신규)

**문제**: soft가 "dark mode default"를 권장하지만, 사용자 선호(prefers-color-scheme) 대응이 없음.

**개선**: CSS custom properties 기반 테마 변수 + 선택적 토글 버튼.

### 5.5 반응형 테스트 가이드 (Section 8, 신규)

**문제**: "mobile-first" 원칙만 언급하고, 구체적 테스트 브레이크포인트/기기 목록이 없음.

**개선**: 5개 필수 브레이크포인트 + iOS Safari 이슈 + 터치 타겟 기준.

---

## 6. 효율성 분석

### 6.1 줄 수 비교

| 섹션 | 예상 줄 수 | 출처 |
|------|-----------|------|
| 1. Identity & Configuration | ~20 | taste 1 + soft 1 + 신규 |
| 2. Architecture & Conventions | ~25 | taste 2 + taste 8.A |
| 3. Anti-Pattern Registry | ~35 | taste 7 + soft 2 + redesign + output |
| 4. Design Engineering | ~40 | taste 3 + soft 4.C/7 + redesign |
| 5. Creative Variance Engine | ~35 | soft 3-5 + taste 4 |
| 6. Section Library | ~30 | taste 6 + taste 8.B/C |
| 7. Redesign Protocol | ~30 | redesign (고유) |
| 8. Accessibility & SEO | ~15 | 신규 |
| 9. Output Enforcement | ~20 | output (고유) |
| 10. Performance Guardrails | ~10 | taste 5 + soft 6 |
| 11. Pre-Output Checklist | ~15 | taste 9 + soft 8 + output |
| **합계** | **~275줄** | |

### 6.2 효율 메트릭

| 메트릭 | 값 |
|--------|-----|
| 원본 합계 | 569줄 |
| 통합 스킬 | ~275줄 |
| 절감 줄 수 | ~294줄 |
| **총 절감율** | **~52%** |
| 신규 추가 (Section 8) | ~15줄 |
| **순 절감율 (신규 포함)** | **~47%** |

### 6.3 토큰 효율 영향

- 52% 줄 수 절감 ≈ AI 컨텍스트 윈도우 절반으로 축소
- 연구에 따르면 (research/laziness/architectural-patterns.md), 스킬 파일의 간결함이 AI의 규칙 준수율에 직접 영향
- 단일 파일 구조로 AI가 "어떤 스킬을 읽어야 하는지" 판단하는 오버헤드 제거

---

## 7. 구현 로드맵

### Step 1: 통합 SKILL.md 초안 작성
- Section 1-11 순서대로 작성
- 각 섹션 작성 시 원본 파일의 해당 줄을 참조하며 중복 제거
- 신규 Section 8 (Accessibility & SEO) 작성
- **예상 산출물**: `SKILL.md` (~275줄)

### Step 2: 교차 검증 (줄 단위)
- 원본 4개 파일의 모든 규칙이 통합본에 포함되었는지 확인
- 특히 고유 가치(설정값, Scan-Diagnose-Fix, Variance Engine, PAUSE/CONTINUE)가 누락 없는지 확인
- 규칙 간 불일치 해소 (예: 패딩 값 통일)

### Step 3: README.md 업데이트
- 4개 스킬 설명 → 단일 스킬 설명
- 사용법 간소화: 1개 파일만 참조
- "추천 조합" 테이블 제거
- 설정값 섹션 유지

### Step 4: 원본 아카이브
```
supanova-design-skill/
  SKILL.md                    (~275줄, 통합본)
  README.md                   (업데이트)
  examples/
  research/
  archive/                    (원본 보관)
    taste-skill/SKILL.md
    redesign-skill/SKILL.md
    soft-skill/SKILL.md
    output-skill/SKILL.md
```

### Step 5: 실전 테스트
- CREATE 모드: 새 랜딩페이지 생성 → 체크리스트 18항목 검증
- REDESIGN 모드: 기존 HTML 업그레이드 → 체크리스트 5항목 검증
- PAUSE/CONTINUE: 긴 출력 중단/재개 → 정상 작동 확인
- 접근성: ARIA, contrast, keyboard nav 확인

---

## 8. 위험 요소 및 대응

| 위험 | 영향도 | 대응 전략 |
|------|-------|----------|
| **275줄이 여전히 길어 AI가 후반부 규칙 무시** | 중 | Section 9 Output Enforcement가 생략 방지. 핵심 규칙(Anti-Pattern, Checklist)을 상단(3) + 하단(11)에 이중 배치. |
| **Mode Routing 오판 (CREATE↔REDESIGN)** | 중 | 키워드 기반 판별 + 사용자 명시 모드 지정 옵션. 오판 시에도 규칙 대부분이 양쪽에 적용 가능. |
| **중복 제거 시 미묘한 뉘앙스 손실** | 낮 | Step 2 교차 검증에서 줄 단위 대조. 원본을 archive/에 보관하여 롤백 가능. |
| **신규 요소(접근성, SEO)가 기존 규칙과 충돌** | 낮 | Section 8은 독립적 영역으로 기존 디자인 규칙과 충돌 없음. prefers-reduced-motion만 모션 규칙과 조화 필요. |

---

## 9. 기대 효과 요약

| 항목 | Before (4개 스킬) | After (1개 통합 스킬) |
|------|-------------------|---------------------|
| 파일 수 | 4개 | 1개 |
| 총 줄 수 | 569줄 | ~275줄 |
| 중복 규칙 | ~200줄 (35%) | 0줄 (0%) |
| 사용자 선택 부담 | "추천 조합" 테이블 필요 | 자동 Mode Routing |
| 규칙 불일치 | 7개 영역에서 발생 | Single Source of Truth |
| 접근성 | 없음 | WCAG 2.1 AA |
| SEO | 기본 meta만 | OG + JSON-LD + canonical |
| 다크/라이트 모드 | dark 기본만 | prefers-color-scheme 대응 |
| 반응형 테스트 | "mobile-first" 원칙만 | 5개 브레이크포인트 + 기기별 가이드 |
| AI 컨텍스트 효율 | 4파일 로딩 오버헤드 | 단일 파일 즉시 적용 |
