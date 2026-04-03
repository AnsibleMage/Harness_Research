---
name: stitch-image-to-prompt
description: >
  Use this skill when the user attaches an image and asks to create a Google Stitch UI design prompt.
  이미지를 첨부하고 "스티치 프롬프트로 만들어줘", "이 UI를 스티치로 재현", "이 화면을 Stitch용으로 변환" 같은 요청이 트리거입니다.
  Triggers: "convert this to Stitch", "generate Stitch prompt from this image", "create Stitch design from screenshot",
  "이 스크린샷 기반으로 스티치 디자인", "이 디자인을 Stitch에서 만들 수 있게", "스티치로 만들어줘",
  "Stitch prompt", "stitch design", "구글 스티치".
  Trigger aggressively when an image is attached with any mention of: Stitch, 스티치, Google Stitch, 구글 스티치,
  UI prototype, 프로토타입, design prompt, 디자인 프롬프트.
  Covers all visual sources: Figma captures, web screenshots, hand-drawn wireframes, app screens, design mockups.
  This skill analyzes the image and generates an optimized natural-language prompt for Google Stitch's
  generate_screen_from_text API, then optionally executes it via MCP to create the actual screen.
---

# Stitch Image-to-Prompt

Analyze images and generate design prompts optimized for Google Stitch MCP tools.
Do NOT generate the prompt immediately — interview the user first to establish context.

### Language Rule
- Conversation with the user (interview, analysis summary, guidance): **user's language**
- The **prompt output for Stitch must always be in English**. Stitch (powered by Gemini) interprets English prompts most accurately and produces better results.

### How Stitch Differs from Code-Based Design Tools
Stitch uses **natural language prompts** — not structured JSON, CSS, or code. The prompt describes *what you want to see* in plain English. Stitch's AI (Gemini) interprets this and generates a complete UI screen. Think of it as describing a design to a skilled designer, not writing markup.

---

## Phase 0: Interview — Ask First, Then Build

Gather context before generating a prompt. This ensures the output matches the user's intent.

### Required Questions (ask 2-3 at a time, skip what you can infer)

1. **Purpose** — "What is this design for? (rapid prototyping / client presentation / developer handoff / exploring ideas)"
2. **Device type** — "Which device? (desktop / mobile / tablet / device-agnostic)"
   - If the image clearly shows a phone UI → infer MOBILE; wide layout → infer DESKTOP
3. **Fidelity** — "Pixel-perfect reproduction or capture the overall structure and feel?"
4. **Scope** — "Just this one screen, or part of a multi-screen flow?"

### Conditional Follow-up Questions

- Color mode preference (light / dark / match the image)
- Brand colors or specific color palette to follow
- Font style preference (modern sans-serif / classic serif / playful / match the image)
- Whether the text content is real or placeholder
- If multiple screens are needed, the navigation flow between them

### Interview Principles

- If you can infer the answer from the image, state your inference and move on — only ask about genuinely uncertain things.
- If the user says "just make it" or "빨리 해줘", proceed immediately with reasonable defaults.
- Keep the interview to 1-2 exchanges maximum. The goal is clarity, not interrogation.

---

## Phase 1: Image Analysis

After the interview, systematically analyze the image. This is the foundation of a good prompt.

### What to Identify

| Category | Details to Extract |
|---|---|
| **Layout** | Overall structure (header/sidebar/main/footer), column count, content flow direction |
| **Components** | Navigation bars, cards, buttons, forms, modals, tables, lists, tabs, hero sections |
| **Colors** | Background color, primary/accent colors, text colors, border colors, gradient presence |
| **Typography** | Heading sizes (large/medium/small), body text style, font weight patterns |
| **Images/Icons** | Hero images, product photos, avatars, icon style (outlined/filled), illustration style |
| **Spacing** | Dense vs spacious, card padding, section gaps |
| **Vibe** | Overall aesthetic — minimal, corporate, playful, dark, luxurious, clinical, etc. |

### Analysis Output

Summarize to the user in a compact format:
```
📐 Layout: [description]
🧩 Components: [list]
🎨 Colors: [palette description]
✍️ Typography: [style]
🖼️ Imagery: [description]
✨ Vibe: [2-3 adjectives]
```

Confirm with the user: "Does this capture everything? Anything I missed or should emphasize?"

---

## Phase 2: Prompt Generation

Combine the analysis and interview results to write a Stitch-optimized prompt.

### Stitch Prompt Anatomy

A great Stitch prompt has these layers, in this order:

```
1. WHAT — App type + screen purpose (1 sentence)
2. WHO — Target audience or brand context (1 sentence, optional)
3. VIBE — 2-3 adjectives setting the aesthetic tone
4. LAYOUT — Overall page structure description
5. SECTIONS — Top-to-bottom walkthrough of each section
6. COMPONENTS — Specific UI elements within each section
7. STYLE — Colors, fonts, borders, spacing details
8. IMAGERY — Description of images, icons, illustrations
```

### Prompt Writing Rules

**Lead with the big picture.** Start with what the screen IS, then drill into details. Stitch works best when it understands the overall concept first.

**Use natural, descriptive language.** Not `"width: 380px, padding: 32px"` but `"a medium-width card with generous padding"`. Stitch interprets intent, not CSS.

**Be specific about what matters, loose about what doesn't.** If the exact shade of blue matters, say `"primary color #2563EB"`. If not, say `"a professional blue"`.

**Describe sections top-to-bottom.** Walk through the screen like you're reading a page — header first, then hero, then content sections, then footer. This helps Stitch maintain spatial coherence.

**Name components using UI/UX vocabulary.** Use terms like: navigation bar, hero section, card grid, call-to-action button, sidebar, breadcrumb, tab bar, modal, search bar, footer. These are well-understood by Stitch.

**Set the vibe with adjectives.** Words like "minimalist", "vibrant", "corporate", "playful", "dark and moody", "clean and spacious" significantly influence the output's look and feel.

**Specify colors and fonts when critical.**
- Colors: `"Primary color: forest green. Accent: warm gold. Background: off-white."`
- Fonts: `"Use a modern sans-serif font"` or `"Serif headings, sans-serif body text"`
- Borders: `"Fully rounded buttons"` or `"Sharp corners on all cards"`

**Use image descriptions, not filenames.** Instead of `"use logo.png"`, say `"company logo in the top-left corner"`. For hero images: `"a wide photo of a mountain landscape at sunset"`.

**One screen at a time.** Don't try to describe an entire app in one prompt. Focus on one screen, get it right, then move to the next.

### Image Type Adaptation

| Source Image Type | Prompt Approach |
|---|---|
| **High-res UI screenshot** | Extract exact colors, describe precise component layout, match spacing and hierarchy closely |
| **Wireframe / sketch** | Focus on structure and flow; let Stitch choose appropriate colors and styling |
| **Figma capture** | Identify design system patterns (component reuse, consistent spacing); describe the system, not just the screen |
| **Live web/app screenshot** | Note responsive behavior; describe interactive states if visible; flag dynamic content areas |
| **Hand-drawn wireframe** | Interpret intent generously; describe the layout structure; note any annotations |

### Prompt Length Guidelines

| Screen Complexity | Recommended Length |
|---|---|
| Simple (login, splash, empty state) | 3-6 sentences |
| Medium (dashboard, profile, settings) | 8-15 sentences |
| Complex (data-heavy dashboard, marketplace) | 15-25 sentences |

Stitch handles detailed prompts well, but each sentence should add value. Padding with filler doesn't help.

---

## Phase 3: Prompt Output & Execution Options

Present the generated prompt to the user, then offer execution options.

### Output Format

```markdown
## Stitch Prompt

> [The complete English prompt, ready to paste into Stitch or execute via MCP]

### Settings
- **Device**: DESKTOP / MOBILE / TABLET
- **Model**: GEMINI_3_1_PRO (recommended for complex) / GEMINI_3_FLASH (faster, simpler)

### Execution Options
1. **Copy & paste** — Use this prompt directly in stitch.withgoogle.com
2. **New project** — Create a new Stitch project and generate this screen (via MCP)
3. **Add to existing** — Generate this screen in an existing project (provide project ID)
```

### MCP Execution Flow

When the user chooses to execute:

```
Option 2 (New project):
  mcp__stitch__create_project(title)
  → mcp__stitch__generate_screen_from_text(projectId, prompt, deviceType, modelId)
  → Report result + screen URL

Option 3 (Existing project):
  mcp__stitch__list_projects() → user picks one
  → mcp__stitch__generate_screen_from_text(projectId, prompt, deviceType, modelId)
  → Report result + screen URL
```

**Model selection guidance:**
- `GEMINI_3_1_PRO` — Best quality, recommended for detailed/complex screens. Slower.
- `GEMINI_3_FLASH` — Faster generation, good for simple screens or rapid iteration.

**Important:** `generate_screen_from_text` can take a few minutes. Do NOT retry if it seems slow. If it fails with a connection error, the generation may still succeed — use `get_screen` to check later.

### Post-Generation Refinement

After the initial screen is generated, offer refinement options:

1. **Edit** — Use `edit_screens` with specific, incremental change prompts
2. **Variants** — Use `generate_variants` to explore alternatives (layout, color, images, fonts, content)
3. **Iterate** — Adjust the original prompt and regenerate

Refinement prompt tips (from Stitch best practices):
- Make one major change per prompt
- Be specific: "Change the header background to dark navy" not "make it darker"
- Reference elements by name: "the call-to-action button in the hero section"
- Coordinate related changes: "Update theme to forest green. Ensure all images and icons match."

---

## Phase 4: Self-Verification Before Output

Before presenting the prompt, check:

- [ ] Does the prompt start with a clear description of what the screen IS?
- [ ] Are vibe/aesthetic adjectives included?
- [ ] Is the layout described top-to-bottom in logical order?
- [ ] Are all major UI components from the image accounted for?
- [ ] Are colors specified where the user cares about accuracy?
- [ ] Is typography style mentioned?
- [ ] Are image descriptions included (not filenames)?
- [ ] Is the prompt in English?
- [ ] Is the length appropriate for the complexity?
- [ ] Would a designer reading this prompt understand what to create?

Fix any gaps before outputting.

---

## Prompt Examples

### Example 1: Simple Login Screen

```
A clean, modern login page for a SaaS product. Minimalist and professional.

Centered card on a soft gray background. The card has generous padding, rounded corners, and a subtle shadow.

Inside the card: company logo at the top (simple geometric mark), "Welcome back" heading in dark text, a subheading "Sign in to your account" in gray.

Two input fields with light borders: email and password. Each has a label above it.

A full-width primary button in blue: "Sign In". Below it, a "Forgot password?" text link in blue.

At the bottom, a divider line, then "Don't have an account? Sign up" with "Sign up" as a link.

Modern sans-serif font throughout. Primary color: #2563EB. Background: #F9FAFB.
```

### Example 2: E-commerce Product Page

```
Product detail page for a premium Japanese-inspired tea store. Warm, minimal, Japandi aesthetic.

Desktop layout with a clean navigation bar at top: logo left, search bar center, cart icon right. Below that, breadcrumb navigation.

Main content in two columns. Left column (60%): large product image of a ceramic tea set on a wooden surface, warm natural lighting. Below the main image, a row of 4 thumbnail images.

Right column (40%): product name in a refined serif font, "Sakura Bloom Tea Set". Price "$89.00" in bold. Star rating (4.5 stars) with review count. Brief description in body text. Quantity selector. "Add to Cart" button in matte black, full width, rounded corners. "Add to Wishlist" text link below.

Below the columns: tabbed section with "Description", "Ingredients", "Reviews" tabs. Currently showing Description with paragraph text.

Color palette: warm whites, soft beige, charcoal text, matte black accents. Font: elegant sans-serif for body, thin serif for headings.
```

---

## Reference

For detailed Stitch prompting strategies and tips, see `references/stitch-prompting-guide.md`.
