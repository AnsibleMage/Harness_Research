# ansible-prism

> One light enters the prism — infinite colors emerge.

**An & Ari's Creative Generation Engine** for Claude Code. Generates diverse, high-quality Korean landing pages and homepages where every generation is structurally unique.

## What It Does

`ansible-prism` takes a topic or wireframe and produces a complete, production-ready HTML landing page. The key differentiator: **it never generates the same design twice.** A 5-slot combination engine with 20 values per slot creates over 3.2 million unique design combinations, ensuring every output has a different visual identity, color palette, page structure, typography, and accent strategy.

## Modes

| Mode | Input | Output |
|------|-------|--------|
| **CREATE** | Just a topic: "인테리어 랜딩페이지 만들어줘" | Full page with auto-generated content + design |
| **REDESIGN** | Wireframe HTML file | Same content, completely different visual treatment |

## Quick Start

```
/ansible-prism 인테리어 랜딩페이지 만들어줘
/ansible-prism opt1.html 리디자인해줘
/ansible-prism opt1.html 3개 동시에 만들어줘
```

## Architecture

```
ansible-prism/
├── SKILL.md              ← Main orchestrator (~200 lines)
├── README.md             ← This file
├── README_KO.md          ← Korean version
└── references/           ← 9 engine modules (3,000+ lines)
    ├── CREATIVE_GENERATION_FRAMEWORK.md  ← Core engine
    ├── CREATE_MODE.md                    ← Zero-input content generation
    ├── REDESIGN_MODE.md                  ← Wireframe visual transformation
    ├── SLOT_ENGINE.md                    ← 5×20 = 3.2M combinations
    ├── IMAGE_ENGINE.md                   ← Gradient + SVG + AI images
    ├── MOTION_RULES.md                   ← Scroll reveal + hover effects
    ├── CSS_PRECISION.md                  ← 4px grid + multi-layer shadows
    ├── VISUAL_DENSITY.md                 ← 7-layer visual content rules
    └── TECH_SPEC.md                      ← Output technical specification
```

## The 5-Slot Combination Engine

Each generation selects one value from each of five independent slots:

| Slot | What It Controls | Values |
|------|-----------------|--------|
| **Visual Identity** | CSS variables, borders, textures, card style, nav style | 20 |
| **Color Temperature** | Entire color palette with specific hex values | 20 |
| **Page Structure** | HTML `<body>` skeleton (sidebar, grid, stack, sticky, snap...) | 20 |
| **Typography** | Heading font family, size hierarchy, spacing | 20 |
| **Accent Strategy** | Where accent color appears in CSS (text, border, hover, shadow...) | 20 |

**"Real Difference" 4-Dimension Check:** Every generation must differ from the previous on all four visual dimensions (structure, color family, font category, accent property).

## Quality Modules

| Module | Purpose |
|--------|---------|
| **IMAGE_ENGINE** | No gray placeholders. Every thumbnail gets a gradient + SVG icon matched to its content category. |
| **MOTION_RULES** | IntersectionObserver scroll reveals, staggered card entrances, varied hover effects per section. |
| **CSS_PRECISION** | 4px spacing grid, 5-level color depth, 4+ font weights, multi-layer box shadows, per-element line heights. |
| **VISUAL_DENSITY** | 7-layer visual hierarchy. Every card has 2+ text levels. No identical adjacent section backgrounds. |

## Output

- **Format:** Single self-contained HTML file
- **CSS:** Embedded `<style>` with CSS Custom Properties
- **JS:** Embedded `<script>` (IntersectionObserver, tab switching)
- **Fonts:** Google Fonts CDN + Pretendard CDN
- **Images:** Zero external files — CSS gradients + inline SVG only
- **Accessibility:** WCAG 2.1 AA (focus styles, contrast ratios, reduced-motion)

## Agent Teams (Parallel Generation)

Request multiple versions and they generate simultaneously:

```
/ansible-prism opt1.html 3개 동시에 만들어줘
```

Each agent receives a unique slot combination. All pairs are pre-verified to pass the 4-dimension difference check.

## Credits

Created by **An (Ansible)** & **Ari (Aria)** — AnsibleMage.

## License

MIT
