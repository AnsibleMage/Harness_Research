---
name: pencil-image-to-prompt
description: >
  Use this skill when the user attaches an image and asks to create a Pencil (.pen) design prompt.
  이미지를 첨부하고 "펜슬 프롬프트로 만들어줘", "이 UI를 .pen으로 재현", "이 화면을 펜슬용으로 변환" 같은 요청이 트리거입니다.
  Triggers: "convert this to Pencil", "generate .pen prompt from this image", "create Pencil prompt from screenshot",
  "이 스크린샷 기반으로 디자인 프롬프트", "이 디자인을 Pencil에서 만들 수 있게".
  Trigger aggressively when an image is attached with any mention of: design, UI, layout, component, .pen, Pencil,
  디자인, 화면, 레이아웃, 컴포넌트.
  Covers all visual sources: Figma captures, web screenshots, hand-drawn wireframes, app screens.
---

# Pencil Image-to-Prompt

Analyze images and generate design prompts optimized for Pencil MCP tools.
Do NOT generate the prompt immediately — interview the user first to establish context.

### Language Rule
- Conversation with the user (interview, analysis summary, guidance) should be in **the user's language**.
- The **prompt output for Pencil MCP must always be in English**. The Pencil engine interprets English instructions most accurately.

---

## Phase 0: Interview — Ask First, Then Build

Do NOT generate a prompt as soon as you receive an image. Gather the following first.

### Required Questions (ask 2-3 at a time)

1. **Purpose** — "What is this design for? (mockup review / actual implementation / design system)"
2. **Tech stack** — "Will this be converted to code? If so, which stack? (React + Tailwind / Vue / Next.js / no conversion)"
3. **Existing design system** — "Any existing .pen files, design libraries, or CSS variables in use?"
4. **Fidelity** — "Pixel-perfect reproduction vs. just capture the structure and feel?"

### Conditional Follow-up Questions

- Whether both light/dark modes are needed
- Whether responsive support is required
- Icon library preference (lucide, feather, Material Symbols, etc.)
- Whether text in the image is real content or placeholder

### Interview Principles

- If you can infer something by looking at the image, infer it directly — only ask about things you're uncertain of.
- If the user says "just make it quickly", proceed to Phase 1 immediately with reasonable defaults.
- If a question can be answered by exploring the codebase, explore it yourself.

---

## Phase 1: Image Analysis

After the interview, systematically analyze the image. Identify:

- **Structure**: overall dimensions, section divisions (header/sidebar/main/footer), layout direction, alignment, spacing patterns (estimate 8px grid)
- **Elements**: text (headings/body/labels), buttons (filled/outlined/ghost), input fields, icons, cards, navigation, badges, toggles, etc.
- **Colors**: background, text, primary, secondary, border, gradient presence
- **Typography**: size hierarchy, weight, alignment

Summarize the analysis concisely to the user and confirm nothing was missed.

---

## Phase 2: Prompt Generation

Combine analysis and interview results to write a Pencil MCP prompt.

### Prompt Structure Order

Pencil requires variables to be defined before they can be referenced, and components to be created before instances can be generated. Follow this order:

```
1. Overview          — what, canvas size, target device
2. Variables         — colors($color.xxx), spacing($spacing.xxx), typography($text.xxx)
3. Components        — extract repeated patterns as reusable: true
4. Layout            — root frame → section frames structure
5. Detail Elements   — concrete elements inside each section
6. Verification      — screenshot and compare with original, fix mismatches
```

### Writing Rules

**Use concrete values.** Not "appropriate size" but `width: 200, height: 48, cornerRadius: 8, padding: [12, 24]`.

**Specify Pencil types.** Containers → frame, text → text, icons → icon_font, reuse → ref.

**Specify all layout properties.** layout(vertical/horizontal), gap, padding, justifyContent, alignItems. Child sizing uses fill_container or fixed values.

**Use variables aggressively.** `$color.primary` instead of hardcoded hex. If an existing design system exists, reuse its variable names.

**Extract repeated patterns as components.** Define with `reusable: true` → create instances with ref → override with descendants. Mark content-swap areas with slot.

**Use icon_font type for icons.** iconFontFamily (lucide/feather/Material Symbols) + iconFontName combination.

**Set textGrowth before controlling text size.** width/height on text objects are ignored without textGrowth. Options: auto, fixed-width, fixed-width-height.

**Use "[placeholder]" for unreadable text.** If font cannot be determined, note "fontFamily: adjust to project settings".

### Image Type Adaptation

| Image Type | Approach |
|---|---|
| High-res UI | Extract hex colors, pixel-level spacing, shadows and rounding in detail |
| Wireframe / hand-drawn | Focus on structure, grayscale palette, minimize styling details |
| Figma capture | Reflect layer structure, component patterns → reusable, tokens → variable mapping |
| Live web/app capture | Estimate responsive behavior, note placeholders, mention interaction possibilities |

### Prompt Output Example

Below is an example prompt for a simple login card. Follow this format in actual output:

```
## Overview
Login card, 480x640. Light mode. Center-aligned layout.

## Variables
- $color.primary: #3b82f6
- $color.background: #ffffff
- $color.text: #1f2937
- $color.border: #e5e7eb
- $spacing.md: 16
- $spacing.lg: 24

## Components
### input-field (reusable: true)
- type: frame, layout: vertical, gap: 6
- children:
  - label: type: text, fontSize: 14, fontWeight: 500, fill: $color.text
  - input-box: type: frame, width: fill_container, height: 44, cornerRadius: 8, stroke: {fill: $color.border, thickness: 1}, padding: [0, 12]
    - placeholder: type: text, fontSize: 14, fill: #9ca3af, textGrowth: fixed-width

## Layout
- root: type: frame, width: 480, height: 640, layout: vertical, alignItems: center, justifyContent: center, fill: #f3f4f6
  - card: type: frame, width: 380, layout: vertical, gap: $spacing.lg, padding: [32, 32], cornerRadius: 12, fill: $color.background, effect: {type: shadow, shadowType: outer, offset: {x: 0, y: 4}, blur: 12, color: #0000001a}

## Detail Elements
- Inside card:
  - title: type: text, content: "Login", fontSize: 24, fontWeight: 700, fill: $color.text, textAlign: center
  - email-field: type: ref, ref: input-field, descendants: {label: {content: "Email"}, placeholder: {content: "name@example.com"}}
  - password-field: type: ref, ref: input-field, descendants: {label: {content: "Password"}, placeholder: {content: "••••••••"}}
  - submit-btn: type: frame, width: fill_container, height: 44, cornerRadius: 8, fill: $color.primary, layout: horizontal, justifyContent: center, alignItems: center
    - btn-text: type: text, content: "Sign In", fontSize: 16, fontWeight: 600, fill: #ffffff

## Verification
Take a screenshot and compare with the original. Adjust any spacing, color, or alignment mismatches.
```

---

## Phase 3: Self-Verification Before Output

Before outputting the prompt, check:

- Are all UI elements included without omission?
- Does every element have a Pencil type specified?
- Are layout properties (layout, gap, padding, justify, align) explicit?
- Are colors defined as variables?
- Are repeated elements extracted as reusable components?
- Is textGrowth set on text elements that need size control?
- Is a screenshot verification step included at the end?

Fix any issues before outputting. If the prompt is very long, split by section and guide step-by-step execution.

---

## Reference

For detailed .pen format structure (object types, fill/stroke/effect, component/instance/slot/theme system), see `references/pen-format.md`.
