# Design Token Analysis Patterns

Reference guide for extracting and translating design tokens from Stitch project HTML/CSS into semantic natural language descriptions for DESIGN.md.

---

## 1. Tailwind Border Radius → Natural Language

| Tailwind Class | CSS Value | Natural Language Description |
|---------------|-----------|------------------------------|
| `rounded-none` | 0px | Sharp, squared-off edges |
| `rounded-sm` | 2px | Barely perceptible rounding |
| `rounded` | 4px | Subtly softened corners |
| `rounded-md` | 6px | Gently rounded corners |
| `rounded-lg` | 8px | Noticeably rounded corners |
| `rounded-xl` | 12px | Generously rounded corners |
| `rounded-2xl` | 16px | Prominently rounded, approaching soft |
| `rounded-3xl` | 24px | Very soft, pillow-like rounding |
| `rounded-full` | 9999px | Pill-shaped / Fully circular |

---

## 2. Tailwind Shadow → Natural Language

| Tailwind Class | Natural Language Description |
|---------------|------------------------------|
| `shadow-none` | Flat, no elevation — content lies flush with the surface |
| `shadow-sm` | Whisper-soft shadow, barely perceptible lift |
| `shadow` | Gentle floating effect, like paper resting on a desk |
| `shadow-md` | Clear card elevation, comfortable floating presence |
| `shadow-lg` | Pronounced depth, drawer-level prominence |
| `shadow-xl` | Heavy elevation, dialog or modal-level weight |
| `shadow-2xl` | Maximum depth, dramatic floating presence |
| `shadow-inner` | Inset depression, pressed or recessed appearance |

---

## 3. Tailwind Spacing → Natural Language

| Scale | Tailwind | Pixels | Natural Language Description |
|-------|----------|--------|------------------------------|
| Micro | `p-0.5`, `gap-0.5` | 2px | Hairline spacing, barely there |
| Tight | `p-1`, `gap-1` | 4px | Compact, minimal breathing room |
| Snug | `p-2`, `gap-2` | 8px | Snug spacing, closely grouped |
| Normal | `p-3`, `gap-3` | 12px | Standard comfortable spacing |
| Comfortable | `p-4`, `gap-4` | 16px | Comfortable breathing room |
| Relaxed | `p-6`, `gap-6` | 24px | Relaxed, airy spacing |
| Spacious | `p-8`, `gap-8` | 32px | Spacious, generous whitespace |
| Expansive | `p-12`, `gap-12` | 48px | Expansive section separation |
| Grand | `p-16`, `gap-16` | 64px | Grand, dramatic whitespace |

---

## 4. Tailwind Font Weight → Natural Language

| Tailwind Class | Weight | Natural Language Description |
|---------------|--------|------------------------------|
| `font-thin` | 100 | Delicate, whisper-thin strokes |
| `font-extralight` | 200 | Ethereal lightness |
| `font-light` | 300 | Airy, elegant weight |
| `font-normal` | 400 | Standard reading weight |
| `font-medium` | 500 | Slightly emphasized, confident |
| `font-semibold` | 600 | Strong presence, assertive |
| `font-bold` | 700 | Bold, commanding attention |
| `font-extrabold` | 800 | Heavy, impactful weight |
| `font-black` | 900 | Maximum weight, dramatic impact |

---

## 5. Tailwind Font Size → Natural Language

| Tailwind Class | Size | Typical Usage |
|---------------|------|---------------|
| `text-xs` | 12px | Fine print, legal text, timestamps |
| `text-sm` | 14px | Secondary text, captions, helper text |
| `text-base` | 16px | Standard body text |
| `text-lg` | 18px | Emphasized body, lead paragraphs |
| `text-xl` | 20px | Card titles, section labels |
| `text-2xl` | 24px | Subsection headings |
| `text-3xl` | 30px | Section headings |
| `text-4xl` | 36px | Page titles |
| `text-5xl` | 48px | Hero headings |
| `text-6xl` | 60px | Display headings |

---

## 6. Color Naming Conventions (Stitch-Optimized)

When naming colors for DESIGN.md, use this pattern:
**[Evocative Adjective] + [Color Family] + (Optional: Modifier)**

### Naming Examples by Color Family

| Hex Range | Good Names | Avoid |
|-----------|-----------|-------|
| Blues (#0000FF range) | "Deep Ocean Blue", "Sky-bright Cerulean", "Midnight Sapphire", "Soft Periwinkle" | "blue", "dark blue", "light blue" |
| Greens (#00FF00 range) | "Forest Emerald", "Spring Mint", "Sage Whisper", "Deep Teal" | "green", "dark green" |
| Reds (#FF0000 range) | "Warm Crimson", "Soft Coral", "Deep Burgundy", "Sunset Rose" | "red", "dark red" |
| Yellows (#FFFF00 range) | "Honey Gold", "Bright Sunflower", "Warm Amber", "Soft Buttercream" | "yellow", "gold" |
| Purples (#800080 range) | "Royal Violet", "Soft Lavender", "Deep Plum", "Dusty Mauve" | "purple", "violet" |
| Grays (#808080 range) | "Charcoal Slate", "Silver Mist", "Warm Stone", "Cool Pewter" | "gray", "dark gray", "light gray" |
| Blacks (#000000 range) | "Rich Onyx", "Soft Charcoal", "Deep Ink" | "black", "near-black" |
| Whites (#FFFFFF range) | "Pure Snow", "Warm Ivory", "Cool Cloud", "Soft Eggshell" | "white", "off-white" |

### Functional Role Descriptions

| Role | Description Pattern |
|------|-------------------|
| Primary | "Main brand color, used for CTAs, active states, and key interactive elements" |
| Secondary | "Supporting color for secondary actions, category indicators, and visual variety" |
| Background | "Page-level background, establishes the base canvas" |
| Surface | "Card and panel backgrounds, creates depth against the page background" |
| Text Primary | "Headings and body text, maximum readability" |
| Text Secondary | "Captions, labels, and helper text, lower visual priority" |
| Border | "Dividers, input outlines, and subtle separators" |
| Accent | "Highlights, badges, and attention-grabbing elements" |
| Success | "Positive feedback, confirmations, and completed states" |
| Warning | "Caution indicators, pending states" |
| Error | "Error messages, destructive actions, validation failures" |

---

## 7. Component Identification from HTML Structure

### Common Patterns

| HTML Pattern | Component Type |
|-------------|----------------|
| `<nav>`, `role="navigation"` | Navigation bar |
| `<header>` with large image/text | Hero section |
| Repeating `<div>` with image + title + description | Card grid |
| `<form>`, `<input>`, `<select>` | Form / Input area |
| `<button>`, `role="button"` | Button (check variants by class) |
| `<dialog>`, `role="dialog"` | Modal / Dialog |
| `position: fixed` bottom bar | Bottom navigation / Tab bar |
| `<aside>`, sidebar-width elements | Sidebar |
| `<table>`, `role="grid"` | Data table |
| `<ul>`/`<ol>` with styled items | List component |
| `<footer>` | Footer section |

### Button Variant Detection

| Class Pattern | Button Type |
|--------------|-------------|
| Filled background + white text | Primary button |
| Border + transparent background | Secondary / Outlined button |
| No border + no background + text color only | Tertiary / Ghost button |
| Small size + pill shape | Tag / Chip |
| Icon only + circular | Icon button |

---

## 8. Cross-Screen Consistency Verification

When analyzing multiple screens, verify these should be CONSISTENT:

| Token Type | Should Be Consistent Across Screens |
|-----------|-------------------------------------|
| Primary/Secondary colors | Yes — brand identity |
| Background color | Yes — page-level |
| Font families | Yes — design system core |
| Button styles | Yes — interaction patterns |
| Border radius scale | Yes — shape language |
| Shadow scale | Yes — elevation system |
| Spacing base unit | Yes — rhythm system |
| Navigation style | Yes — wayfinding |

If inconsistencies are found:
1. Note them in the analysis summary
2. Use the MOST COMMON pattern as the "system" value
3. Note screen-specific exceptions in DESIGN.md Section 4

---

## 9. designTheme JSON Field Reference

The `get_project` response includes a `designTheme` object:

| Field | Type | Description |
|-------|------|-------------|
| `colorMode` | string | "LIGHT" or "DARK" |
| `fontFamily` | string | Primary font family name |
| `borderRadius` | string | Global border radius setting |
| `customColors` | array | Array of {name, hex} custom color definitions |
| `description` | string | Project-level design description |

These values represent the PROJECT-LEVEL design intent. HTML analysis may reveal additional colors/fonts used at the SCREEN level. Both sources should be synthesized.
