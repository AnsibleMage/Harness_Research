# Design System Extractor

Extract a complete design system from any website URL and output it as a visual, browsable HTML document.

## What It Does

Given a website URL, this skill reverse-engineers the site's design system and packages it into a single HTML file containing:

- **Colors** — Core palette, CSS variables, hover/focus states with confidence scores
- **Typography** — Font families, type scale, weights, line heights
- **Spacing** — Common spacing values with usage frequency
- **Borders & Radius** — Border styles and radius patterns
- **Shadows** — Box shadow definitions
- **Components** — Buttons (with hover interactions), links
- **CSS Variables Export** — Copy-ready `:root` block with all tokens

The output HTML includes dark mode toggle and click-to-copy on all values.

## Prerequisites

| Program | Version | Check | Install |
|---------|---------|-------|---------|
| Node.js | v18+ | `node --version` | `brew install node` (macOS) |
| npm | (bundled) | `npm --version` | Included with Node.js |
| Dembrandt | latest | `npx dembrandt --version` | `npm i -g dembrandt` |

> Claude Code will automatically check and install missing dependencies when running the skill.

## Usage

Invoke via Claude Code:

```
/design-extractor
```

Or trigger naturally:

```
"이 사이트의 디자인 시스템 추출해줘: https://example.com"
"Extract the design system from https://example.com"
```

### Output

```
{siteName}_design-system.html
```

Open in any browser to view the full design system.

## How It Works

```
URL ─→ Dembrandt (headless browser)
       ├─ DOM traversal + getComputedStyle
       ├─ Hover/focus state simulation
       └─ Structured JSON output
                │
                ▼
       Claude Code (template engine)
       ├─ JSON parsing + filtering
       ├─ HTML template population
       └─ Single-file HTML output
```

## Engine

[Dembrandt](https://www.npmjs.com/package/dembrandt) — A headless browser-based design token extraction tool that crawls websites and extracts colors, typography, spacing, shadows, borders, and component styles as structured JSON.

## Author

**An (Ansible)** — [github.com/AnsibleMage](https://github.com/AnsibleMage)

## License

MIT License

Copyright (c) 2026 An (Ansible)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
