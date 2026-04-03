# Supanova Forge

A premium landing page design engine that unifies 4 individual design skills into one. Generates $150k-agency-quality Korean landing pages from scratch or upgrades existing pages.

## What It Does

Given a project requirement or existing HTML, this skill automatically generates premium Korean landing pages:

- **CREATE Mode** — Build a new landing page from scratch (VIBE preset-driven)
- **REDESIGN Mode** — Analyze and upgrade existing HTML (Scan-Diagnose-Fix)
- **VIBE Preset System** — 5 vibes (dark / warm / clean / bold / soft) auto-link 16 sub-properties each
- **Anti-Generic Engine** — Pattern registry that eliminates the "AI-generated look"
- **Korean Optimization** — Pretendard typography, Korean line-break rules, natural copy
- **Accessibility & SEO** — WCAG 2.1 AA, Open Graph, JSON-LD built-in

Output is a single HTML file (Tailwind CSS CDN-based) viewable directly in any browser.

## Prerequisites

| Component | Type | Installation |
|-----------|------|-------------|
| Tailwind CSS | CDN | Not required (CDN link included in HTML) |
| Pretendard Font | CDN | Not required (CDN link included in HTML) |
| Iconify Solar Icons | CDN | Not required (CDN link included in HTML) |

> All dependencies are CDN-based — no installation needed. Just a browser and internet connection.

## Usage

### Quick Start

```
/supanova-forge Create a main page for an education portal
```

The skill asks 3 questions then auto-applies the VIBE preset:

```
1. Page purpose? → brand
2. Mood? → warm
3. Additional requests? → Reference design system file
```

Or trigger naturally:

```
"Build a dark-themed SaaS product landing page"
"Redesign this HTML" (auto-switches to REDESIGN mode when existing file is provided)
```

### VIBE Comparison

| VIBE | Feel | Best For |
|------|------|----------|
| `dark` | Tech startup, SaaS, AI | Product launches, tech showcases |
| `warm` | Editorial, brand, premium | Education, culture, lifestyle |
| `clean` | Minimal, structured, trustworthy | Healthcare, portfolio, public sector |
| `bold` | High-impact, energetic, dramatic | Startups, events, launches |
| `soft` | Gentle, emotional, approachable | Beauty, wellness, F&B, education |

### Mode Routing

| Scenario | Auto Mode | Applies |
|----------|----------|---------|
| New landing page | **CREATE** | Sections 2-6, 8-11 (full) |
| Existing HTML provided | **REDESIGN** | Section 7 (VIBE preset-based) |

## How It Works

```
Prompt ─→ Mode Routing (CREATE / REDESIGN)
           │
           ├─ CREATE ──→ Configuration Interview (3Q)
           │              ├─ VIBE Preset selection (dark/warm/clean/bold/soft)
           │              ├─ 16 sub-properties auto-linked
           │              ├─ Section Library (17 patterns)
           │              └─ Anti-Pattern validation → HTML output
           │
           └─ REDESIGN ─→ Existing HTML Scan
                           ├─ VIBE Preset-based diagnosis
                           ├─ Fix Priority (8 steps)
                           └─ Improved HTML output
```

## Skill Structure (11 Sections)

| Section | Role |
|---------|------|
| 1. Identity & Configuration | VIBE Preset linked system + mode routing |
| 2. Architecture & Conventions | Tech stack + HTML templates |
| 3. Anti-Pattern Registry | Unified prohibited patterns |
| 4. Design Engineering | Typography / color / layout / depth / transitions / Korean |
| 5. Creative Variance Engine | VIBE-linked archetypes + premium components + motion |
| 6. Section Library | 17 landing page patterns |
| 7. Redesign Protocol | VIBE-based Scan-Diagnose-Fix workflow |
| 8. Accessibility & SEO | WCAG 2.1 AA + OG + JSON-LD |
| 9. Output Enforcement | No-truncation + PAUSE/CONTINUE |
| 10. Performance Guardrails | GPU-safe animations + CDN discipline |
| 11. Pre-Output Checklist | Final validation per CREATE/REDESIGN mode |

## Tech Stack

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

This skill is built upon the work of outstanding open-source projects and developers. Deep gratitude for their spirit of sharing and design philosophy.

### Original Authors

| Project | Author | Contribution | Link |
|---------|--------|-------------|------|
| **supanova** | [supanova.dev](https://supanova.dev) | Original AI landing page builder engine. Provided the foundational architecture for premium Korean landing pages, Anti-Pattern Registry, and Creative Variance Engine | [supanova.dev](https://supanova.dev) |
| **taste-skill** | [@lexnlin](https://x.com/lexnlin) (Leon) | Core philosophy of the design aesthetics engine. Original author of the "eliminate the AI-generated look" principle, Vibe Archetypes, Korean typography rules, and Anti-Generic pattern list | [GitHub](https://github.com/Leonxlnx/taste-skill) |

This skill exists thanks to the open-source sharing of the original authors above. The taste-skill philosophy — "every page should look handcrafted" — is the foundation of the entire Forge.

### Forked by

| Contributor | Role | Work |
|-------------|------|------|
| **An** / AnsibleMage | Project lead, design direction | Proposed 4-skill unification, designed VIBE Preset linked system, derived preset philosophy through landing-page-generator comparison |
| **Ari** / Claude Code | AI partner, implementation | Merge integration, SKILL.md structuring, preset linking logic, REDESIGN protocol improvements, documentation |

---

## Version History

### v2.0.0 (2026-03-21) — VIBE Preset Linked Configuration

**Core change: Independent sliders → Preset linked system**

Inspired by the landing-page-generator skill's preset decision logic, switched to a structure where selecting a VIBE auto-links 12 sub-properties. Based on the insight that consistency between properties is key to "the handcrafted feel."

**Changes:**

- **Section 1: Configuration Interview reduced**
  - Before: 6 questions (purpose, experimentality 1-10, animation 1-10, density 1-10, mood, additional)
  - After: 3 questions (purpose, mood, additional)
  - VIBE selection auto-links 12 properties: DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, RADIUS, SHADOW, BORDER, TEXTURE, SECTION_RHYTHM, FONT_DISPLAY, HOVER_STYLE, LETTER_SPACING, TYPO_RANGE

- **Section 1: VIBE Preset System added**
  - Linked property tables for 5 VIBEs (dark/warm/clean/bold/soft)
  - 4 application rules (batch setting, individual override, consistency principle, no independent mixing)

- **Section 5: Vibe Archetypes linking enhanced**
  - Added `Linked:` tags per VIBE — radius, shadow, border, texture, hover, letter-spacing, typo range
  - warm: explicit Tenor Sans/Playfair display fonts, radius 0px, NO shadows

- **Section 7: REDESIGN Fix Priority restructured**
  - Step 0 added: "VIBE preset selection is the starting point of all fixes"
  - 7 steps → 8 steps, all steps based on VIBE-linked values

**Background:**
Comparative analysis of mot.korea.ac.kr and OpenAds design systems showed warm VIBE (density 3, dramatic typography, sharp corners, no shadows) was most effective at removing the AI-generic feel. The previous independent slider approach caused property mismatches (e.g., warm but radius 16px) that made outputs look awkward.

### v1.0.0 (2026-03-17) — Forge Edition (Initial Merge)

First version unifying 4 original skills.

**Changes:**

- **4 skills → 1 skill merge**
  - taste-skill (213 lines) — Main design engine
  - redesign-skill (142 lines) — Redesign engine
  - soft-skill (121 lines) — Premium aesthetics engine
  - output-skill (93 lines) — Output truncation prevention
  - Total: 569 lines → 275 lines (**52% reduction**)

- **Structural redesign: 11 Sections**
  - Section 1: Identity & Configuration (with mode routing)
  - Section 2: Architecture & Conventions
  - Section 3: Anti-Pattern Registry (unified prohibited rules)
  - Section 4: Design Engineering (typo/color/layout/depth/transitions/Korean)
  - Section 5: Creative Variance Engine (archetypes + components + motion)
  - Section 6: Section Library (17 landing page patterns)
  - Section 7: Redesign Protocol (Scan-Diagnose-Fix workflow)
  - Section 8: Accessibility & SEO (WCAG 2.1 AA + OG + JSON-LD)
  - Section 9: Output Enforcement (no-truncation + PAUSE/CONTINUE)
  - Section 10: Performance Guardrails (GPU-safe animations)
  - Section 11: Pre-Output Checklist (per-mode validation)

- **New features**
  - Auto Mode Routing (CREATE/REDESIGN)
  - Configuration Interview (6 setup questions)
  - WCAG 2.1 AA accessibility
  - Open Graph + JSON-LD SEO
  - Responsive test guide (5 breakpoints)
  - PAUSE/CONTINUE protocol

### v0.x (Pre-Forge) — Original 4 Skills

Original skills are archived in the `archive/` folder:

```
archive/
  taste-skill/SKILL.md      (213 lines)
  redesign-skill/SKILL.md   (142 lines)
  soft-skill/SKILL.md       (121 lines)
  output-skill/SKILL.md     (93 lines)
```

---

## Archive

The original 4 skills are preserved in the `archive/` folder:

```
archive/
  taste-skill/SKILL.md      (213 lines) — Main design engine
  redesign-skill/SKILL.md   (142 lines) — Redesign engine
  soft-skill/SKILL.md       (121 lines) — Premium aesthetics engine
  output-skill/SKILL.md     (93 lines)  — Output truncation prevention
```

---

## Contributors

- **An** — Project lead, design direction / [GitHub](https://github.com/AnsibleMage)
- **Ari** — AI partner, implementation / Claude Code

## Feedback

Please submit via GitHub [Issues](https://github.com/AnsibleMage) or Pull Requests.

## License

Licensed under the original [taste-skill](https://github.com/Leonxlnx/taste-skill) license.
