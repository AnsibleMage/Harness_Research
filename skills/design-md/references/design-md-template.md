# DESIGN.md Output Template

This template defines the structure for generated DESIGN.md files.
Replace all `[placeholders]` with actual values extracted from the Stitch project.

---

```markdown
# Design System: [Project Title]

**Project ID:** `[projectId]`
**Generated:** [YYYY-MM-DD]
**Screens Analyzed:** [count] ([Screen Name 1, Screen Name 2, ...])

---

## 1. Visual Theme & Atmosphere

[Write an evocative paragraph of 3-5 sentences describing the overall aesthetic philosophy.
Describe the mood, visual density, and emotional impression. Use specific adjectives that
Stitch can interpret to reproduce the feel.]

**Keywords:** [adjective1], [adjective2], [adjective3], [adjective4], [adjective5]

---

## 2. Color Palette & Roles

| Role | Name | Hex | Usage |
|------|------|-----|-------|
| Primary | [Descriptive Name, e.g., "Deep Ocean Teal"] | [#XXXXXX] | [e.g., "Primary buttons, active navigation indicators, key CTAs"] |
| Secondary | [Descriptive Name] | [#XXXXXX] | [functional description] |
| Background | [Descriptive Name] | [#XXXXXX] | [functional description] |
| Surface | [Descriptive Name] | [#XXXXXX] | [functional description — cards, panels] |
| Text Primary | [Descriptive Name] | [#XXXXXX] | [functional description — headings, body text] |
| Text Secondary | [Descriptive Name] | [#XXXXXX] | [functional description — captions, helper text] |
| Accent | [Descriptive Name] | [#XXXXXX] | [functional description — highlights, badges] |
| Border | [Descriptive Name] | [#XXXXXX] | [functional description — dividers, input borders] |
| Success | [Descriptive Name] | [#XXXXXX] | [functional description] |
| Warning | [Descriptive Name] | [#XXXXXX] | [functional description] |
| Error | [Descriptive Name] | [#XXXXXX] | [functional description] |

### Color Mode
[LIGHT / DARK / AUTO] — [Brief description of how color mode affects the palette]

---

## 3. Typography Rules

**Heading Font:** [Font Family] — [descriptive quality, e.g., "Clean geometric sans-serif with confident weight"]
**Body Font:** [Font Family] — [descriptive quality, e.g., "Highly legible humanist sans-serif"]

| Element | Font | Size | Weight | Line Height | Letter Spacing | Color |
|---------|------|------|--------|-------------|----------------|-------|
| H1 (Page Title) | [family] | [size] | [weight] | [lh] | [ls] | [color ref] |
| H2 (Section Title) | [family] | [size] | [weight] | [lh] | [ls] | [color ref] |
| H3 (Subsection) | [family] | [size] | [weight] | [lh] | [ls] | [color ref] |
| Body | [family] | [size] | [weight] | [lh] | [ls] | [color ref] |
| Body Small | [family] | [size] | [weight] | [lh] | [ls] | [color ref] |
| Caption | [family] | [size] | [weight] | [lh] | [ls] | [color ref] |
| Button Label | [family] | [size] | [weight] | [lh] | [ls] | [color ref] |
| Navigation | [family] | [size] | [weight] | [lh] | [ls] | [color ref] |

---

## 4. Component Stylings

### Buttons
- **Primary:** [Shape description, e.g., "Pill-shaped with fully rounded ends"]. Background: [Color Name]. Text: [Color Name]. [Hover/active behavior if observable].
- **Secondary:** [Description]. Background: [Color Name]. Border: [description].
- **Tertiary/Ghost:** [Description if present].
- **Size:** [small/medium/large — relative sizing description]

### Cards & Containers
- **Corner Radius:** [Natural language, e.g., "Subtly rounded corners (medium radius)"]
- **Background:** [Color Name]
- **Shadow:** [Natural language, e.g., "Whisper-soft diffused shadow creating gentle lift"]
- **Border:** [description or "None"]
- **Padding:** [description, e.g., "Generous internal spacing"]

### Navigation
- **Type:** [Top bar / Sidebar / Bottom tab bar / Breadcrumb]
- **Style:** [description of visual treatment]
- **Active Indicator:** [how the current page/section is highlighted]

### Forms & Inputs
- **Border:** [description, e.g., "Thin, light gray stroke"]
- **Background:** [Color Name]
- **Corner Radius:** [description]
- **Placeholder Style:** [color, weight]
- **Focus State:** [description, e.g., "Primary color border glow"]
- **Labels:** [position — above/inline, style]

### Modals & Overlays
- **Backdrop:** [description, e.g., "Semi-transparent dark overlay"]
- **Corner Radius:** [description]
- **Shadow:** [description]
- **Positioning:** [centered/slide-in/bottom-sheet]

### [Additional Components]
[Add any project-specific components found: tabs, accordions, badges, avatars, sliders, etc.]

---

## 5. Layout Principles

- **Grid System:** [description, e.g., "12-column responsive grid with 24px gutters"]
- **Content Max Width:** [value, e.g., "1280px maximum content width, centered"]
- **Spacing Scale:** [values, e.g., "4px base unit — 8, 16, 24, 32, 48, 64px"]
- **Section Padding:** [description, e.g., "64px vertical padding between major sections"]
- **Card Grid:** [description, e.g., "3-column card grid on desktop, single column on mobile"]
- **Responsive Behavior:** [description of any mobile/tablet patterns observed]
- **Content Alignment:** [left-aligned / center-aligned / mixed]

---

## 6. Depth & Elevation

| Level | Usage | Shadow Description |
|-------|-------|--------------------|
| Level 0 (Flat) | Background, inline content | No shadow — content lies flat on the surface |
| Level 1 (Subtle) | Cards, content sections | [description, e.g., "Barely perceptible lift, like paper resting on a desk"] |
| Level 2 (Medium) | Dropdowns, popovers, hover states | [description] |
| Level 3 (High) | Modals, dialogs, drawers | [description] |

**Border Radius Scale:**
- None: [usage — e.g., "Tables, horizontal dividers"]
- Small ([value]): [usage — e.g., "Badges, tags"]
- Medium ([value]): [usage — e.g., "Cards, inputs, buttons"]
- Large ([value]): [usage — e.g., "Hero sections, featured cards"]
- Full (pill): [usage — e.g., "Avatar frames, pill buttons"]

---

## 7. Image & Icon Style

- **Image Treatment:** [description — e.g., "Rounded corners matching card radius, no borders, 16:9 aspect ratio"]
- **Image Content Tone:** [e.g., "Professional photography with natural lighting and warm tones"]
- **Icon Style:** [Outlined / Filled / Dual-tone / Custom]
- **Icon Size Scale:** [small/medium/large values]
- **Illustration Style:** [if present — e.g., "Flat vector illustrations with limited palette"]
- **Avatar Style:** [if present — e.g., "Circular, 40px, with subtle border"]

---

## 8. Prompt Guide (for Stitch)

When generating new screens for this project, prepend the following to your prompt:

> [COMPOSE A 3-5 SENTENCE PARAGRAPH that weaves together:
>  - The atmosphere keywords from Section 1
>  - The primary and secondary colors with hex codes from Section 2
>  - The font family names from Section 3
>  - The border-radius style from Section 6
>  - The layout max-width from Section 5
>  This paragraph should be directly paste-able as a Stitch prompt prefix.]

### Screen-Type Prompt Templates

**Dashboard / Overview Screen:**
> [Project Title] design system. [Atmosphere keywords]. Create a dashboard screen with [layout description]. Use [Primary Color Name] (#hex) for key metrics and CTAs, [Surface Color Name] (#hex) for card backgrounds. [Font family] font throughout. [Border radius style]. [Spacing description].

**Detail / Content Screen:**
> [Project Title] design system. [Atmosphere keywords]. Create a detail page with [layout description]. Hero section with [image treatment]. Content in [typography style]. [Color palette summary with hex codes].

**Form / Input Screen:**
> [Project Title] design system. [Atmosphere keywords]. Create a form screen with [input styling from Section 4]. [Button style from Section 4]. [Layout principles]. [Color palette with hex codes].

**List / Browse Screen:**
> [Project Title] design system. [Atmosphere keywords]. Create a browsing/listing page with [card style from Section 4]. [Grid layout from Section 5]. [Color palette with hex codes]. [Typography for list items].
```
