---
name: design-extractor
description: Extract a complete design system from any website URL and output it as a visual HTML document. Uses Dembrandt as the extraction engine. Generates design tokens (colors, typography, spacing, shadows, borders), component styles (buttons, links, inputs), and hover/focus interaction states — all packaged into a single browsable HTML file. Use when the user wants to extract, reverse-engineer, or analyze a website's design system from a URL.
---

# Design System Extractor

## Overview

Extract a website's design system from a URL and package it as a beautiful, browsable HTML document.

**Keywords**: design system, extract, design tokens, colors, typography, components, URL, website analysis, reverse engineer, 디자인 시스템, 추출, 토큰

**Engine**: Dembrandt (npm)

## Prerequisites & Installation

> Claude Code가 스킬 실행 시 아래 의존성을 자동으로 확인하고, 미설치 시 설치를 진행한다.

### Required Programs

| Program | Purpose | Check Command | Install Command |
|---------|---------|---------------|-----------------|
| **Node.js** (v18+) | JavaScript 런타임 | `node --version` | `brew install node` (macOS) / `winget install OpenJS.NodeJS` (Windows) |
| **npm** | 패키지 관리자 | `npm --version` | Node.js에 포함 |
| **Dembrandt** | 디자인 시스템 추출 엔진 | `npx dembrandt --version` | `npm i -g dembrandt` |

### Auto-Install Flow

스킬 실행 시 Step 1.5로 아래 검증을 자동 수행한다:

```bash
# 1. Node.js 확인
node --version 2>/dev/null || { echo "Node.js not found"; exit 1; }

# 2. Dembrandt 확인 — 미설치 시 자동 설치
npx dembrandt --version 2>/dev/null || npm i -g dembrandt
```

- Node.js가 없으면 사용자에게 설치 안내 (`brew install node` / `winget install OpenJS.NodeJS` 또는 공식 사이트)
- Dembrandt가 없으면 `npm i -g dembrandt`로 자동 설치 후 진행
- `npx dembrandt` 사용 시 글로벌 설치 없이도 실행 가능 (임시 다운로드)

## Execution Flow

### Step 1: Gather Inputs

Use `AskUserQuestion` to collect:

1. **Target URL** — The website URL to extract the design system from
2. **Output folder** — Where to save the result HTML file (default: current working directory)

### Step 2: Run Dembrandt

Execute via Bash:

```bash
npx dembrandt <URL> --save-output 2>&1
```

- The JSON output will be saved to `output/<domain>/<timestamp>.json`
- Read the JSON file after extraction completes
- If extraction fails, try with `--browser=firefox` flag (for Cloudflare-protected sites)
- For SPA-heavy sites, add `--slow` flag

### Step 3: Parse JSON & Fill Template

Read the Dembrandt JSON output and fill the **HTML Template** below. The template is FIXED — only data values change.

### Step 4: Save & Report

1. **File naming**: `{siteName}_design-system.html`
   - Extract `siteName` from Dembrandt JSON's `siteName` field
   - If `siteName` is null, derive from the domain (e.g., `visitjeju` from `visitjeju.net`)
   - Sanitize: replace spaces with hyphens, remove special characters, lowercase
   - Examples: `카름스테이_design-system.html`, `apple_design-system.html`
2. Save to the user-specified output folder
3. Clean up the Dembrandt JSON output folder (optional, ask user)
4. Report completion with:
   - File path
   - Summary: number of colors, typography styles, components extracted
   - Suggestion: "Open in browser to view the full design system"

## Error Handling

| Error | Solution |
|-------|----------|
| Dembrandt not installed | Run `npm i -g dembrandt` automatically |
| URL unreachable | Retry with `--browser=firefox` |
| Cloudflare block | Retry with `--browser=firefox --slow` |
| Empty extraction | Report which sections were empty, suggest trying a different page of the site |
| Timeout | Retry with `--slow` flag, increase timeout |

---

## HTML Template (MANDATORY — use this exact structure)

> **RULE**: The CSS block and HTML skeleton below are FIXED. Only replace `{{PLACEHOLDER}}` values with extracted data. Do NOT change class names, layout structure, or styling.

### Placeholder Reference

| Placeholder | Source (Dembrandt JSON) |
|-------------|------------------------|
| `{{SITE_NAME}}` | `siteName` or domain |
| `{{URL}}` | `url` |
| `{{DOMAIN}}` | domain part of `url` |
| `{{DATE}}` | `extractedAt` formatted as YYYY-MM-DD |
| `{{COLOR_COUNT}}` | `colors.palette.length` |
| `{{TYPO_COUNT}}` | `typography.styles.length` |
| `{{SPACING_BASE}}` | `spacing.scaleType` |
| `{{GOOGLE_FONTS_LINK}}` | Google Fonts `<link>` if fonts need loading, or empty |

### Repeating Blocks

For sections with variable-length data (colors, typography, spacing, etc.), repeat the marked HTML block once per item.

---

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Design System — {{SITE_NAME}} ({{DOMAIN}})</title>
{{GOOGLE_FONTS_LINK}}
<style>
  :root {
    --bg: #fafafa;
    --surface: #ffffff;
    --text: #1a1a1a;
    --text-secondary: #666;
    --border: #e5e5e5;
    --accent: #f05423;
    --accent-hover: #f8de08;
    --nav-bg: #ffffff;
    --code-bg: #f3f4f6;
  }
  [data-theme="dark"] {
    --bg: #111111;
    --surface: #1e1e1e;
    --text: #e5e5e5;
    --text-secondary: #999;
    --border: #333;
    --nav-bg: #1a1a1a;
    --code-bg: #2a2a2a;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
  }
  /* NAV */
  nav {
    position: fixed; top: 0; left: 0; width: 240px; height: 100vh;
    background: var(--nav-bg); border-right: 1px solid var(--border);
    padding: 24px 16px; overflow-y: auto; z-index: 100;
  }
  nav .logo { font-size: 14px; font-weight: 700; color: var(--accent); margin-bottom: 8px; }
  nav .site-name { font-size: 20px; font-weight: 700; margin-bottom: 4px; }
  nav .site-url { font-size: 11px; color: var(--text-secondary); word-break: break-all; margin-bottom: 20px; display: block; }
  nav a {
    display: block; padding: 8px 12px; border-radius: 6px;
    color: var(--text-secondary); text-decoration: none; font-size: 13px; font-weight: 500;
    transition: all 0.15s;
  }
  nav a:hover { background: var(--bg); color: var(--text); }
  nav .theme-toggle {
    margin-top: 20px; padding: 8px 12px; border-radius: 6px;
    background: var(--bg); border: 1px solid var(--border);
    color: var(--text); cursor: pointer; font-size: 12px; width: 100%;
    transition: all 0.15s;
  }
  /* MAIN */
  main { margin-left: 240px; padding: 40px 48px 80px; max-width: 1100px; }
  .header { margin-bottom: 48px; padding-bottom: 24px; border-bottom: 2px solid var(--border); }
  .header h1 { font-size: 32px; font-weight: 700; margin-bottom: 4px; }
  .header .meta { font-size: 13px; color: var(--text-secondary); }
  section { margin-bottom: 56px; }
  section > h2 {
    font-size: 22px; font-weight: 700; margin-bottom: 24px;
    padding-bottom: 8px; border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 8px;
  }
  section > h2 .badge {
    font-size: 11px; font-weight: 600; background: var(--accent);
    color: #fff; padding: 2px 8px; border-radius: 10px;
  }
  h3 { font-size: 15px; font-weight: 600; margin-bottom: 12px; color: var(--text-secondary); }
  /* CARDS */
  .card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 24px; margin-bottom: 16px;
  }
  /* SWATCHES */
  .swatch-grid { display: flex; flex-wrap: wrap; gap: 16px; }
  .swatch {
    display: flex; flex-direction: column; align-items: center; gap: 6px; cursor: pointer;
  }
  .swatch-box {
    width: 64px; height: 64px; border-radius: 10px;
    border: 1px solid var(--border); transition: transform 0.15s;
  }
  .swatch:hover .swatch-box { transform: scale(1.08); }
  .swatch-label { font-size: 11px; font-weight: 600; font-family: monospace; }
  .swatch-sub { font-size: 10px; color: var(--text-secondary); }
  .swatch-confidence { font-size: 9px; padding: 1px 5px; border-radius: 4px; background: var(--code-bg); }
  /* TYPO */
  .type-row {
    display: flex; justify-content: space-between; align-items: baseline;
    padding: 16px 0; border-bottom: 1px solid var(--border);
  }
  .type-row:last-child { border-bottom: none; }
  .type-preview { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .type-meta { flex-shrink: 0; text-align: right; margin-left: 24px; }
  .type-meta span { display: block; font-size: 11px; color: var(--text-secondary); font-family: monospace; }
  .type-context {
    font-size: 10px; font-weight: 600; text-transform: uppercase;
    padding: 1px 6px; border-radius: 3px; background: var(--code-bg);
    color: var(--text-secondary); margin-right: 8px;
  }
  /* SPACING */
  .spacing-row {
    display: flex; align-items: center; gap: 16px; margin-bottom: 8px;
  }
  .spacing-bar {
    height: 28px; background: rgba(240, 84, 35, 0.12); border-radius: 4px;
    border-left: 3px solid var(--accent); min-width: 4px;
  }
  .spacing-label { font-size: 12px; font-family: monospace; color: var(--text-secondary); white-space: nowrap; }
  .spacing-count { font-size: 10px; color: var(--text-secondary); }
  /* RADIUS */
  .radius-grid { display: flex; gap: 24px; flex-wrap: wrap; }
  .radius-item { display: flex; flex-direction: column; align-items: center; gap: 8px; }
  .radius-box {
    width: 80px; height: 80px; background: rgba(240, 84, 35, 0.08);
    border: 2px solid var(--accent);
  }
  .radius-label { font-size: 12px; font-family: monospace; }
  /* SHADOW */
  .shadow-grid { display: flex; gap: 24px; flex-wrap: wrap; }
  .shadow-item { display: flex; flex-direction: column; align-items: center; gap: 8px; }
  .shadow-box {
    width: 120px; height: 80px; background: var(--surface);
    border-radius: 10px; border: 1px solid var(--border);
  }
  .shadow-label { font-size: 11px; font-family: monospace; color: var(--text-secondary); max-width: 150px; text-align: center; }
  /* BUTTONS */
  .btn-demo {
    display: inline-block; padding: 0 30px; height: 48px; line-height: 48px;
    font-weight: 600; cursor: pointer; transition: all 0.2s ease;
    text-align: center; text-decoration: none;
  }
  .btn-row { display: flex; gap: 16px; flex-wrap: wrap; align-items: center; margin-bottom: 16px; }
  .btn-states { display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap; }
  .btn-state-tag {
    font-size: 10px; padding: 2px 8px; border-radius: 4px;
    font-family: monospace; background: var(--code-bg); color: var(--text-secondary);
  }
  /* LINKS */
  .link-demo {
    display: inline-block; padding: 8px 0; transition: all 0.2s ease;
    cursor: pointer; margin-right: 24px; margin-bottom: 8px;
  }
  /* BORDERS */
  .border-item {
    display: flex; align-items: center; gap: 16px; padding: 12px 0;
    border-bottom: 1px solid var(--border);
  }
  .border-preview {
    width: 80px; height: 48px; background: var(--surface);
  }
  .border-meta { font-size: 11px; font-family: monospace; color: var(--text-secondary); }
  /* CSS EXPORT */
  .css-export {
    background: var(--code-bg); border-radius: 8px; padding: 20px;
    font-family: monospace; font-size: 12px; line-height: 1.8;
    white-space: pre-wrap; max-height: 400px; overflow-y: auto;
    position: relative;
  }
  .css-export .copy-all {
    position: absolute; top: 8px; right: 8px;
    padding: 4px 12px; border-radius: 4px; border: 1px solid var(--border);
    background: var(--surface); cursor: pointer; font-size: 11px;
    transition: all 0.15s;
  }
  .css-export .copy-all:hover { background: var(--accent); color: #fff; border-color: var(--accent); }
  /* COLLAPSIBLE */
  details { margin-bottom: 12px; }
  details summary {
    cursor: pointer; font-weight: 600; font-size: 14px;
    padding: 8px 0; user-select: none;
  }
  /* TOAST */
  .toast {
    position: fixed; bottom: 24px; right: 24px; padding: 10px 20px;
    background: #333; color: #fff; border-radius: 8px; font-size: 13px;
    opacity: 0; transform: translateY(10px);
    transition: all 0.3s ease; pointer-events: none; z-index: 999;
  }
  .toast.show { opacity: 1; transform: translateY(0); }
  [data-copy] { cursor: pointer; position: relative; }
  [data-copy]:hover::after {
    content: 'Click to copy';
    position: absolute; top: -20px; left: 50%; transform: translateX(-50%);
    font-size: 9px; background: #333; color: #fff; padding: 2px 6px;
    border-radius: 3px; white-space: nowrap;
  }
</style>
</head>
<body>

<!-- NAV (FIXED STRUCTURE) -->
<nav>
  <div class="logo">DESIGN SYSTEM</div>
  <div class="site-name">{{SITE_NAME}}</div>
  <span class="site-url">{{DOMAIN}}</span>
  <a href="#colors">1. Colors</a>
  <a href="#typography">2. Typography</a>
  <a href="#spacing">3. Spacing</a>
  <a href="#borders">4. Borders & Radius</a>
  <a href="#shadows">5. Shadows</a>
  <a href="#components">6. Components</a>
  <a href="#css-export">7. CSS Variables</a>
  <button class="theme-toggle" onclick="toggleTheme()">Toggle Dark Mode</button>
</nav>

<!-- MAIN -->
<main>

<div class="header">
  <h1>{{SITE_NAME}} Design System</h1>
  <div class="meta">
    Source: <strong>{{URL}}</strong><br>
    Extracted: {{DATE}} · Engine: Dembrandt + Claude Code
  </div>
</div>

<!-- 1. COLORS -->
<section id="colors">
  <h2>1. Colors <span class="badge">{{COLOR_COUNT}} colors</span></h2>

  <h3>Core Palette</h3>
  <div class="card">
    <div class="swatch-grid">
      <!-- REPEAT for each colors.palette item where confidence != "medium" or sources != ["hover/focus"] -->
      <div class="swatch" onclick="copyText('{{HEX}}')">
        <div class="swatch-box" style="background:{{HEX}}"></div>
        <span class="swatch-label">{{HEX}}</span>
        <span class="swatch-sub">count: {{COUNT}}</span>
        <span class="swatch-confidence">{{CONFIDENCE}}</span>
      </div>
      <!-- END REPEAT -->
    </div>
  </div>

  <!-- CONDITIONAL: only if colors.cssVariables is not empty -->
  <h3>CSS Variables</h3>
  <div class="card">
    <div class="swatch-grid">
      <!-- REPEAT for each colors.cssVariables entry -->
      <div class="swatch" onclick="copyText('{{VAR_VALUE}}')">
        <div class="swatch-box" style="background:{{VAR_VALUE}}"></div>
        <span class="swatch-label">{{VAR_NAME}}</span>
        <span class="swatch-sub">{{VAR_VALUE}}</span>
      </div>
      <!-- END REPEAT -->
    </div>
  </div>

  <!-- CONDITIONAL: only if hover/focus colors exist -->
  <h3>Hover / Focus States</h3>
  <div class="card">
    <div class="swatch-grid">
      <!-- REPEAT for each colors.palette item where sources includes "hover/focus" -->
      <div class="swatch" onclick="copyText('{{HEX}}')">
        <div class="swatch-box" style="background:{{HEX}}"></div>
        <span class="swatch-label">{{HEX}}</span>
        <span class="swatch-sub">hover/focus</span>
      </div>
      <!-- END REPEAT -->
    </div>
  </div>
</section>

<!-- 2. TYPOGRAPHY -->
<section id="typography">
  <h2>2. Typography <span class="badge">{{TYPO_COUNT}} styles</span></h2>

  <h3>Font Families</h3>
  <div class="card">
    <!-- REPEAT for each unique font family found in typography.styles -->
    <div style="margin-bottom:16px">
      <span class="type-context">{{ROLE}}</span>
      <strong style="font-family:{{FONT_FAMILY}},sans-serif; font-size:20px">{{FONT_FAMILY}}</strong>
      <span style="font-size:12px; color:var(--text-secondary)"> — {{USAGE_CONTEXTS}}</span>
    </div>
    <!-- END REPEAT -->
  </div>

  <h3>Type Scale</h3>
  <div class="card">
    <!-- REPEAT for each unique (family+size+weight) in typography.styles, sorted by size DESC -->
    <!-- Skip 0px sizes and duplicates -->
    <div class="type-row">
      <div class="type-preview" style="font-family:{{FONT_FAMILY}},sans-serif; font-size:{{DISPLAY_SIZE}}; font-weight:{{WEIGHT}}; line-height:{{LINE_HEIGHT}}">{{SAMPLE_TEXT}}</div>
      <div class="type-meta">
        <span>{{SIZE_PX}} / {{SIZE_REM}}</span>
        <span>{{WEIGHT}} · lh {{LINE_HEIGHT}}</span>
        <span class="type-context">{{CONTEXT}}</span>
      </div>
    </div>
    <!-- END REPEAT -->
    <!--
      DISPLAY_SIZE: use actual size for <=56px, cap at 56px for larger sizes
      SAMPLE_TEXT: use SITE_NAME or contextual Korean text (heading→title, button→"예약하기", link→"자세히 보기", body→descriptive sentence, caption→"NEW · OPEN")
    -->
  </div>
</section>

<!-- 3. SPACING -->
<section id="spacing">
  <h2>3. Spacing <span class="badge">{{SPACING_BASE}} base</span></h2>
  <div class="card">
    <!-- REPEAT for each spacing.commonValues (skip extreme outliers like 900px+) -->
    <div class="spacing-row">
      <div class="spacing-bar" style="width:{{PX_VALUE}}"></div>
      <span class="spacing-label" onclick="copyText('{{PX_VALUE}}')">{{PX_VALUE}}</span>
      <span class="spacing-count">×{{COUNT}}</span>
    </div>
    <!-- END REPEAT -->
  </div>
</section>

<!-- 4. BORDERS & RADIUS -->
<section id="borders">
  <h2>4. Borders & Radius</h2>

  <h3>Border Radius</h3>
  <div class="card">
    <div class="radius-grid">
      <!-- REPEAT for each borderRadius.values -->
      <div class="radius-item">
        <div class="radius-box" style="border-radius:{{RADIUS_VALUE}}"></div>
        <span class="radius-label" onclick="copyText('border-radius: {{RADIUS_VALUE}}')">{{RADIUS_VALUE}}</span>
        <span class="swatch-sub">{{ELEMENTS}} · ×{{COUNT}}</span>
      </div>
      <!-- END REPEAT -->
    </div>
  </div>

  <!-- CONDITIONAL: only if borders.combinations exists and has items -->
  <h3>Border Styles</h3>
  <div class="card">
    <!-- REPEAT for each borders.combinations (confidence medium+) -->
    <div class="border-item">
      <div class="border-preview" style="border:{{BORDER_CSS}}"></div>
      <div class="border-meta">
        <div>{{BORDER_DESCRIPTION}}</div>
        <div>{{ELEMENTS}} · ×{{COUNT}} · {{CONFIDENCE}}</div>
      </div>
    </div>
    <!-- END REPEAT -->
  </div>
</section>

<!-- 5. SHADOWS -->
<section id="shadows">
  <h2>5. Shadows <span class="badge">{{SHADOW_COUNT}}</span></h2>
  <div class="card">
    <div class="shadow-grid">
      <!-- REPEAT for each shadows item -->
      <div class="shadow-item">
        <div class="shadow-box" style="box-shadow:{{SHADOW_VALUE}}" onclick="copyText('box-shadow: {{SHADOW_VALUE}}')"></div>
        <span class="shadow-label">{{SHADOW_VALUE}}</span>
        <span class="swatch-confidence">{{CONFIDENCE}} · ×{{COUNT}}</span>
      </div>
      <!-- END REPEAT -->
    </div>
  </div>
</section>

<!-- 6. COMPONENTS -->
<section id="components">
  <h2>6. Components</h2>

  <h3>Buttons</h3>
  <div class="card">
    <p style="font-size:12px; color:var(--text-secondary); margin-bottom:16px">Hover over buttons to see interaction states</p>
    <!-- REPEAT for each components.buttons -->
    <div style="margin-bottom:24px">
      <div style="font-size:12px; font-weight:600; margin-bottom:8px">{{BUTTON_LABEL}} (.{{BUTTON_CLASS}})</div>
      <div class="btn-row">
        <button class="btn-demo btn-{{INDEX}}" style="
          background:{{DEFAULT_BG}}; color:{{DEFAULT_COLOR}};
          border:{{DEFAULT_BORDER}}; border-radius:{{DEFAULT_RADIUS}};
          font-size:{{FONT_SIZE}}; font-weight:{{FONT_WEIGHT}}; font-family:Pretendard,sans-serif;
        ">{{BUTTON_TEXT}}</button>
        <span style="font-size:11px; color:var(--text-secondary)">→ hover: bg {{HOVER_BG}}, color {{HOVER_COLOR}}</span>
      </div>
      <div class="btn-states">
        <span class="btn-state-tag">default: bg {{DEFAULT_BG}}, color {{DEFAULT_COLOR}}</span>
        <span class="btn-state-tag">hover: bg {{HOVER_BG}}, color {{HOVER_COLOR}}</span>
        <!-- Include active/focus if available -->
      </div>
    </div>
    <!-- END REPEAT -->
  </div>

  <!-- CONDITIONAL: only if components.links has items -->
  <h3>Links</h3>
  <div class="card">
    <div style="display:flex; flex-wrap:wrap; gap:24px">
      <!-- REPEAT for each components.links -->
      <div>
        <span class="link-demo" style="color:{{LINK_COLOR}}; font-weight:{{LINK_WEIGHT}}; text-decoration:{{LINK_DECORATION}}">{{LINK_LABEL}}</span>
        <div class="btn-states"><span class="btn-state-tag">{{LINK_COLOR_HEX}} → hover: {{HOVER_COLOR_HEX}}</span></div>
      </div>
      <!-- END REPEAT -->
    </div>
  </div>
</section>

<!-- 7. CSS VARIABLES EXPORT -->
<section id="css-export">
  <h2>7. CSS Variables Export</h2>
  <div class="card">
    <details open>
      <summary>:root { ... } — Click to copy all</summary>
      <div class="css-export" id="cssExport">
<button class="copy-all" onclick="copyText(document.getElementById('cssCode').textContent)">Copy All</button>
<code id="cssCode">:root {
  /* Generate CSS variables from ALL extracted data:
     - Colors (core + hover)
     - Typography (font families, sizes, weights)
     - Spacing scale
     - Border radius
     - Shadows
     - Border styles
     - Button component tokens (default + hover)
     - Link component tokens
     Use semantic naming: --color-primary, --font-display, --space-md, etc.
  */
}</code>
      </div>
    </details>
  </div>
</section>

<footer style="text-align:center; padding:40px 0; color:var(--text-secondary); font-size:12px; border-top:1px solid var(--border)">
  Extracted by <strong>Dembrandt</strong> + <strong>Claude Code</strong> · design-extractor skill
</footer>

</main>

<!-- TOAST -->
<div class="toast" id="toast">Copied!</div>

<script>
// Theme toggle
function toggleTheme() {
  const html = document.documentElement;
  html.dataset.theme = html.dataset.theme === 'dark' ? '' : 'dark';
}

// Copy to clipboard
function copyText(text) {
  navigator.clipboard.writeText(text).then(() => {
    const toast = document.getElementById('toast');
    toast.textContent = `Copied: ${text.length > 40 ? text.slice(0, 40) + '...' : text}`;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 1500);
  });
}

// Button hover interactions — REPEAT for each button variant
// Use btn-{{INDEX}} class matching the buttons above
document.querySelectorAll('.btn-0').forEach(btn => {
  const defaultBg = '{{DEFAULT_BG}}';
  const defaultColor = '{{DEFAULT_COLOR}}';
  const hoverBg = '{{HOVER_BG}}';
  const hoverColor = '{{HOVER_COLOR}}';
  btn.addEventListener('mouseenter', () => { btn.style.background = hoverBg; btn.style.color = hoverColor; });
  btn.addEventListener('mouseleave', () => { btn.style.background = defaultBg; btn.style.color = defaultColor; });
});
</script>

</body>
</html>
```

## Template Rules

1. **CSS is FROZEN** — Do not modify any CSS rule. Copy the `<style>` block exactly as shown.
2. **HTML skeleton is FROZEN** — Sections 1-7 in this exact order. Do not add/remove sections.
3. **Only data changes** — Replace `{{PLACEHOLDER}}` values with Dembrandt JSON data.
4. **REPEAT blocks** — Generate one HTML block per data item. Remove the comment markers.
5. **CONDITIONAL blocks** — Only include the section if data exists. Omit entirely if empty.
6. **Skip junk data** — Filter out 0px sizes, NaN line heights, 900px+ spacing outliers.
7. **Sample text** — Use `siteName` for headings, contextual Korean text for other contexts.
8. **Button hover JS** — Generate one event listener block per button variant with actual colors.
