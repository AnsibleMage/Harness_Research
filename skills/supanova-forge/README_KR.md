# Supanova Forge

4개의 개별 디자인 스킬을 1개로 통합한 프리미엄 랜딩페이지 디자인 엔진입니다. $150k 에이전시 수준의 한국어 랜딩페이지를 생성하거나, 기존 페이지를 업그레이드합니다.

## What It Does

웹사이트 URL 또는 프로젝트 요구사항을 입력하면, 프리미엄 한국어 랜딩페이지를 자동 생성합니다:

- **CREATE 모드** — 새 랜딩페이지를 처음부터 생성 (VIBE 프리셋 기반)
- **REDESIGN 모드** — 기존 HTML을 분석하여 업그레이드 (Scan-Diagnose-Fix)
- **VIBE Preset 시스템** — 5가지 분위기(dark / warm / clean / bold / soft) 선택 시 16개 하위 속성 자동 연동
- **Anti-Generic 엔진** — "AI가 만든 느낌"을 제거하는 금지 패턴 레지스트리
- **한국어 최적화** — Pretendard 타이포, 한국어 줄바꿈 규칙, 자연스러운 카피
- **접근성 & SEO** — WCAG 2.1 AA, Open Graph, JSON-LD 내장

출력물은 단일 HTML 파일 (Tailwind CSS CDN 기반)로 브라우저에서 바로 확인 가능합니다.

## Prerequisites

| 구성요소 | 유형 | 설치 필요 |
|---------|------|----------|
| Tailwind CSS | CDN | 불필요 (HTML에 CDN 링크 포함) |
| Pretendard Font | CDN | 불필요 (HTML에 CDN 링크 포함) |
| Iconify Solar Icons | CDN | 불필요 (HTML에 CDN 링크 포함) |

> 모든 의존성이 CDN 기반이므로 별도 설치가 필요 없습니다. 브라우저와 인터넷 연결만 있으면 됩니다.

## Usage

### Quick Start

```
/supanova-forge 교육 포털 메인페이지 만들어줘
```

스킬이 3가지 질문 후 자동으로 VIBE 프리셋을 적용합니다:

```
1. 페이지 목적은? → brand
2. 분위기? → warm
3. 추가 요청? → 디자인시스템 파일 참조
```

Or trigger naturally:

```
"SaaS 제품 랜딩페이지 다크 분위기로 만들어줘"
"이 HTML 리디자인해줘" (기존 파일 제공 시 자동 REDESIGN 모드)
```

### VIBE별 결과 비교

| VIBE | 느낌 | 적합한 프로젝트 |
|------|------|---------------|
| `dark` | 테크 스타트업, SaaS, AI | 제품 런칭, 기술 소개 |
| `warm` | 에디토리얼, 브랜드, 고급 | 교육, 문화, 라이프스타일 |
| `clean` | 깔끔, 구조적, 신뢰감 | 헬스케어, 포트폴리오, 공공 |
| `bold` | 강렬, 임팩트, 에너지 | 스타트업 런칭, 이벤트, 프로모션 |
| `soft` | 부드러움, 감성, 따뜻함 | 뷰티, 웰빙, F&B, 교육 |

### Mode Routing

| 상황 | 자동 모드 | 적용 |
|------|----------|------|
| 새 랜딩페이지 생성 | **CREATE** | Section 2-6, 8-11 전체 |
| 기존 HTML 제공 | **REDESIGN** | Section 7 (VIBE preset 기반) |

## How It Works

```
프롬프트 ─→ Mode Routing (CREATE / REDESIGN)
             │
             ├─ CREATE ──→ Configuration Interview (3Q)
             │              ├─ VIBE Preset 선택 (dark/warm/clean/bold/soft)
             │              ├─ 12개 하위 속성 자동 연동
             │              ├─ Section Library (17종 패턴)
             │              └─ Anti-Pattern 검증 → HTML 출력
             │
             └─ REDESIGN ─→ 기존 HTML Scan
                             ├─ VIBE Preset 기반 진단
                             ├─ Fix Priority (8단계)
                             └─ 개선된 HTML 출력
```

## 스킬 구조 (11 Sections)

| Section | 역할 |
|---------|------|
| 1. Identity & Configuration | VIBE Preset 연동 시스템 + 모드 라우팅 |
| 2. Architecture & Conventions | 기술 스택 + HTML 템플릿 |
| 3. Anti-Pattern Registry | 통합 금지 규칙 |
| 4. Design Engineering | 타이포/컬러/레이아웃/깊이/전환UI/한국어 |
| 5. Creative Variance Engine | VIBE 연동 아키타입 + 프리미엄 컴포넌트 + 모션 |
| 6. Section Library | 17종 랜딩페이지 패턴 |
| 7. Redesign Protocol | VIBE 기반 Scan-Diagnose-Fix 워크플로우 |
| 8. Accessibility & SEO | WCAG 2.1 AA + OG + JSON-LD |
| 9. Output Enforcement | 생략 방지 + PAUSE/CONTINUE |
| 10. Performance Guardrails | GPU-safe 애니메이션 + CDN 규율 |
| 11. Pre-Output Checklist | CREATE/REDESIGN 모드별 최종 검증 |

## 기술 스택

```html
<!-- Tailwind CSS (CDN) -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- Pretendard Korean Font -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.min.css">

<!-- Iconify Solar Icons -->
<script src="https://code.iconify.design/iconify-icon/2.3.0/iconify-icon.min.js"></script>
```

---

## Credits & Acknowledgments

이 스킬은 여러 뛰어난 오픈소스 프로젝트와 개발자들의 작업 위에 만들어졌습니다. 그들의 공유 정신과 디자인 철학에 깊이 감사드립니다.

### Original Authors

| 프로젝트 | 저자 | 기여 | 링크 |
|---------|------|------|------|
| **supanova** | [supanova.dev](https://supanova.dev) | AI 랜딩페이지 빌더 원본 엔진. 프리미엄 한국어 랜딩페이지의 기초 아키텍처와 Anti-Pattern Registry, Creative Variance Engine의 원형을 제공 | [supanova.dev](https://supanova.dev) |
| **taste-skill** | [@lexnlin](https://x.com/lexnlin) (Leon) | 디자인 미학 엔진의 핵심 철학. "AI가 만든 느낌을 없앤다"는 근본 원칙, Vibe Archetypes, 한국어 타이포그래피 규칙, Anti-Generic 패턴 목록의 원작자 | [GitHub](https://github.com/Leonxlnx/taste-skill) |

이 스킬의 존재는 위 원작자들의 오픈소스 공유 덕분입니다. taste-skill이 제시한 "모든 페이지는 handcrafted처럼 보여야 한다"는 철학이 Forge 전체의 기반입니다.

### Forked by

| 기여자 | 역할 | 작업 |
|--------|------|------|
| **An (앤)** / AnsibleMage | 프로젝트 리더, 디자인 디렉션 | 4스킬 통합 제안, VIBE Preset 연동 시스템 설계, landing-page-generator 비교 분석을 통한 프리셋 철학 도출 |
| **Ari (아리)** / Claude Code | AI 파트너, 구현 | 통합 병합, SKILL.md 구조화, 프리셋 연동 로직 구현, REDESIGN 프로토콜 개선, 문서화 |

---

## Version History

### v2.0.0 (2026-03-21) — VIBE Preset Linked Configuration

**핵심 변경: 독립 슬라이더 → 프리셋 연동 시스템**

landing-page-generator 스킬의 프리셋 결정 로직에서 영감을 받아, VIBE 선택 시 12개 하위 속성이 자동으로 연동되는 구조로 전환. "사람이 만든 느낌"의 핵심이 속성 간 일관성에 있다는 인사이트 기반.

**변경 사항:**

- **Section 1: Configuration Interview 축소**
  - Before: 6개 질문 (목적, 실험성1-10, 애니메이션1-10, 밀도1-10, 분위기, 추가요청)
  - After: 3개 질문 (목적, 분위기, 추가요청)
  - VIBE 선택 시 DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, RADIUS, SHADOW, BORDER, TEXTURE, SECTION_RHYTHM, FONT_DISPLAY, HOVER_STYLE, LETTER_SPACING, TYPO_RANGE 12개 속성 자동 연동

- **Section 1: VIBE Preset System 신설**
  - 5가지 VIBE(dark/warm/clean/bold/soft)별 16개 속성 연동 테이블 추가
  - 적용 규칙 4조 명시 (일괄 세팅, 개별 오버라이드, 일관성 원칙, 독립 조합 금지)

- **Section 5: Vibe Archetypes 연동 강화**
  - 각 VIBE에 `Linked:` 태그 추가 — radius, shadow, border, texture, hover, letter-spacing, typo range 명시
  - warm에 Tenor Sans/Playfair 디스플레이 폰트 명시, radius 0px, NO shadows 강조

- **Section 7: REDESIGN Fix Priority 재구성**
  - Step 0 신설: "VIBE preset 선택이 모든 수정의 시작점"
  - 7단계 → 8단계로 확장, 모든 단계가 VIBE-linked 값 기반

**배경:**
mot.korea.ac.kr과 오픈애즈 디자인시스템을 비교 분석한 결과, warm VIBE(밀도 3, 극적 타이포, 날카운 모서리, 그림자 없음)가 AI 제네릭 느낌을 제거하는 데 가장 효과적이었음. 기존 독립 슬라이더 방식에서는 속성 간 불일치(예: warm인데 radius 16px)가 발생하여 결과물이 어색해지는 문제가 있었음.

### v1.0.0 (2026-03-17) — Forge Edition (Initial Merge)

4개 원본 스킬을 통합한 최초 버전.

**변경 사항:**

- **4스킬 → 1스킬 통합**
  - taste-skill (213줄) — 메인 디자인 엔진
  - redesign-skill (142줄) — 리디자인 엔진
  - soft-skill (121줄) — 프리미엄 미학 엔진
  - output-skill (93줄) — 출력 생략 방지
  - 합계: 569줄 → 275줄 (**52% 절감**)

- **구조 재설계: 11 Sections**
  - Section 1: Identity & Configuration (모드 라우팅 포함)
  - Section 2: Architecture & Conventions
  - Section 3: Anti-Pattern Registry (통합 금지 규칙)
  - Section 4: Design Engineering (타이포/컬러/레이아웃/깊이/전환UI/한국어)
  - Section 5: Creative Variance Engine (아키타입 + 컴포넌트 + 모션)
  - Section 6: Section Library (17종 랜딩페이지 패턴)
  - Section 7: Redesign Protocol (Scan-Diagnose-Fix 워크플로우)
  - Section 8: Accessibility & SEO (WCAG 2.1 AA + OG + JSON-LD)
  - Section 9: Output Enforcement (생략 방지 + PAUSE/CONTINUE)
  - Section 10: Performance Guardrails (GPU-safe 애니메이션)
  - Section 11: Pre-Output Checklist (CREATE/REDESIGN 모드별 검증)

- **신규 기능 추가**
  - 자동 Mode Routing (CREATE/REDESIGN)
  - Configuration Interview (6개 설정 질문)
  - WCAG 2.1 AA 접근성
  - Open Graph + JSON-LD SEO
  - 반응형 테스트 가이드 (5개 브레이크포인트)
  - PAUSE/CONTINUE 프로토콜

### v0.x (Pre-Forge) — Original 4 Skills

원본 스킬들은 `archive/` 폴더에 보관:

```
archive/
  taste-skill/SKILL.md      (213줄)
  redesign-skill/SKILL.md   (142줄)
  soft-skill/SKILL.md       (121줄)
  output-skill/SKILL.md     (93줄)
```

---

## 아카이브

원본 4개 스킬은 `archive/` 폴더에 보관되어 있습니다:

```
archive/
  taste-skill/SKILL.md      (213줄) — 메인 디자인 엔진
  redesign-skill/SKILL.md   (142줄) — 리디자인 엔진
  soft-skill/SKILL.md       (121줄) — 프리미엄 미학 엔진
  output-skill/SKILL.md     (93줄)  — 출력 생략 방지
```

---

## 기여자

- **An (앤)** — 프로젝트 리더, 디자인 디렉션 / [GitHub](https://github.com/AnsibleMage)
- **Ari (아리)** — AI 파트너, 구현 / Claude Code

## 피드백

GitHub [Issue](https://github.com/AnsibleMage) 또는 Pull Request로 제출해 주세요.

## 라이선스

원본 [taste-skill](https://github.com/Leonxlnx/taste-skill)의 라이선스를 따릅니다.
