# html2pptx-converter

> A Claude Code skill that converts HTML web pages into PowerPoint (.pptx) presentations with pixel-accurate layout reproduction.

## Overview

html2pptx-converter takes an HTML source file along with supplementary documents (screenshot, feature description, field definitions) and produces a faithful PowerPoint reproduction. A 4-stage teammate pipeline — **Analyze → Build → Convert → Fix** — handles the entire process autonomously, powered by an embedded PptxGenJS + Playwright engine.

## Structure

```
html2pptx-converter/
├── SKILL.md                  # Skill definition & execution flow
├── PLAN.md                   # Architecture & design decisions
├── package.json              # Node.js dependencies (pptxgenjs, playwright, sharp)
├── requirements.txt          # Python dependencies (Pillow, chardet, comtypes)
│
├── engine/                   # Embedded conversion engine
│   ├── html2pptx.js          # HTML→PPTX conversion (PptxGenJS + Playwright)
│   ├── html2pptx.md          # HTML authoring rules for the engine
│   └── thumbnail.py          # PPTX→thumbnail generator (COM / LibreOffice / Playwright)
│
├── agents/                   # Teammate agent definitions
│   ├── 01-spec-analyzer.md       # Phase 1: HTML + docs → spec.json
│   ├── 02-html-slide-builder.md  # Phase 2: spec.json → slide HTML files
│   ├── 03-executor-validator.md  # Phase 3: HTML → PPTX + visual validation
│   └── 04-iterative-fixer.md     # Phase 4: Issue fixing loop (conditional)
│
├── scripts/                  # Validation & comparison utilities
│   ├── validate_html.py      # Pre-conversion HTML rule checker
│   └── compare_slides.py     # Side-by-side visual comparison generator
│
├── references/               # Reference documentation
│   ├── html2pptx-rules.md        # Engine rule summary
│   ├── pptxgenjs-api-guide.md    # PptxGenJS API reference
│   └── slide-design-patterns.md  # Reusable slide layout templates
│
├── .claude/
│   └── settings.local.json   # Auto-approval patterns for autonomous execution
│
└── test ~ test4/             # Test cases with input files and output results
```

## Key Components

| Component | Role | Technology |
|-----------|------|------------|
| `engine/html2pptx.js` | Parses slide HTML, maps DOM elements to PptxGenJS API calls | Node.js, PptxGenJS, Playwright |
| `engine/thumbnail.py` | Renders PPTX slides as thumbnail images for validation | Python, COM/LibreOffice/Playwright |
| `scripts/validate_html.py` | Checks HTML compliance with engine rules before conversion | Python, html.parser |
| `scripts/compare_slides.py` | Generates side-by-side comparison of original vs output | Python, Pillow |
| `agents/01-spec-analyzer` | Extracts structured spec from 4 input files | Claude Opus |
| `agents/02-html-slide-builder` | Generates engine-compatible HTML from spec | Claude Opus |
| `agents/03-executor-validator` | Runs conversion, thumbnails, and visual QA | Claude Opus |
| `agents/04-iterative-fixer` | Fixes issues found in validation (max 3 loops) | Claude Opus |

## Pipeline

```
Input (4 files)          Phase 1              Phase 2              Phase 3              Phase 4
┌──────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ HTML source   │   │ spec-analyzer │   │ slide-builder │   │   executor-   │   │  iterative-   │
│ Screenshot    │──▶│               │──▶│               │──▶│   validator   │──▶│    fixer      │
│ Description   │   │  → spec.json  │   │  → slide HTML │   │  → .pptx      │   │  → final.pptx │
│ Field defs    │   └───────────────┘   └───────────────┘   │  → thumbnails │   │  (if needed)  │
└──────────────┘                                            │  → validation │   └───────────────┘
                                                            └───────────────┘
```

## Output Modes

| Mode | Colors | Slides | Description Panel | Use Case |
|------|--------|--------|-------------------|----------|
| **wireframe** (default) | `#000/#808080/#E0E0E0/#FFF` | 1 slide, custom size | Yes (right side, 275pt) | UI spec review, documentation |
| **full_design** | Original HTML colors | Multiple, 16:9 (720×405pt) | No | Presentation, demo |

## Quick Start

### Prerequisites

```bash
# Node.js 16+ with dependencies
npm install

# Python 3.8+ with dependencies
pip install -r requirements.txt

# Playwright browser (for thumbnail generation)
npx playwright install chromium
```

### Input Files

Prepare 4 files in a folder:

| # | File | Purpose |
|---|------|---------|
| 1 | `.html` | HTML source code to convert |
| 2 | `.png` | Screenshot of the rendered HTML (for validation) |
| 3 | `_description.md` | Feature descriptions for each UI section |
| 4 | `_fields.md` | UI element definitions (roles, input types, interactions) |

### Usage

In Claude Code, invoke the skill:

```
Use html2pptx-converter skill
Input folder: path/to/your/input
Output folder: path/to/your/output
```

The skill runs autonomously through all 4 phases and produces:

| Output | Description |
|--------|-------------|
| `spec.json` | Structured analysis of all input files |
| `slides/slide_00.html` | Engine-compatible HTML slide(s) |
| `convert.js` | Generated Node.js conversion script |
| `presentation.pptx` | Final PowerPoint file |
| `thumbnails.jpg` | Visual preview of converted slides |
| `comparison.jpg` | Original vs result side-by-side |
| `validation.json` | Quality assessment (pass/needs_fix) |

## Related

- [SKILL.md](SKILL.md) — Full skill definition with detailed phase descriptions
- [engine/html2pptx.md](engine/html2pptx.md) — HTML authoring rules for the conversion engine
- [references/](references/) — API guides and design pattern library
- [test/E2E_final_report.md](test/E2E_final_report.md) — End-to-end test results

---
*Generated by Ari & An*
