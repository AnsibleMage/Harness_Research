# Section Redesign Workflow Reference

## Phase 1: Analysis (Read Before Write)

### 1.1 Identify Target Section
- User specifies section name (e.g., "T1 메인 비주얼", "T7 도서 섹션")
- Locate HTML boundaries: find opening/closing tags and line numbers
- Locate CSS boundaries: find related style block and line numbers
- Locate JS boundaries: find initialization code if interactive (Swiper, slick, etc.)

### 1.2 Read Design Reference Image
- Use Read tool to view the provided screenshot/design image
- Identify key visual elements:
  - Layout structure (grid, flex, columns)
  - Typography (sizes, weights, colors)
  - Spacing (padding, margin, gaps)
  - Background treatment (solid, image, gradient)
  - Interactive elements (buttons, inputs, carousels)
  - Decorative elements (shadows, borders, radius)

### 1.3 Map Current vs Target
- List what exists in current code
- List what the target design requires
- Identify: keep / modify / remove / add

## Phase 2: Implementation Order

ALWAYS follow this sequence:
1. **CSS first** — Replace or modify styles for the section
2. **HTML second** — Replace or modify markup structure
3. **JS third** (if needed) — Update or add initialization code

Rationale: CSS changes don't break existing HTML, but HTML changes without CSS look broken.

## Phase 3: CSS Implementation Patterns

### Background Patterns
```css
/* Full-wide background image */
.section { background: url('path/to/image') center center / cover no-repeat; }

/* Contained background (white sides) */
.section { background: #fff; }
.section .container { background: url('path/to/image') center center / cover no-repeat; }

/* Solid with overlay */
.section { background: #f5f5f5; }
```

### Layout Patterns
```css
/* Two-column: text left + image right */
.content { display: flex; align-items: center; justify-content: space-between; gap: 30px; }
.text-side { flex: 1; }
.image-side { flex: 0 0 auto; }

/* Card grid */
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }

/* Horizontal scroll / carousel */
.carousel { display: flex; overflow-x: auto; gap: 20px; }
```

### Overlap / Floating Elements
```css
/* Element overlapping section boundary */
.parent { position: relative; padding-bottom: 30px; }
.floating-child { position: relative; margin-top: -28px; z-index: 10; }
```

### Button Patterns
```css
/* Pill button */
.btn { padding: 10px 24px; border-radius: 50px; background: #fff; color: #333; font-weight: 600; }

/* Circle arrow button */
.arrow-btn { width: 48px; height: 48px; border: 1px solid #ddd; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
```

### Search Bar Pattern
```css
.search { position: relative; max-width: 720px; margin: 0 auto; }
.search input { width: 100%; height: 56px; padding: 0 60px 0 28px; border: 1px solid #e0e0e0; border-radius: 50px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
.search button { position: absolute; right: 18px; top: 50%; transform: translateY(-50%); }
```

## Phase 4: HTML Structure Patterns

### Section Header
```html
<div class="section-head">
  <div>
    <span class="section-label">Label Text</span>
    <div class="section-title">Title <strong>Bold Part</strong></div>
    <p class="section-desc">Description text</p>
  </div>
  <button class="section-arrow">→</button>
</div>
```

### Card with Tags
```html
<div class="card">
  <div class="card-cover"><img src="..." alt="..."></div>
  <div class="card-title">Title</div>
  <div class="card-tags">
    <span class="card-tag">#Tag1</span>
    <span class="card-tag">#Tag2</span>
  </div>
</div>
```

### Hero Banner (text + thumbnail)
```html
<div class="visual-content">
  <div class="visual-text">
    <p class="visual-sub">Subtitle</p>
    <h2 class="visual-title">Title</h2>
    <p class="visual-desc">Description</p>
    <div class="visual-btns">
      <a href="#">Button 1</a>
      <a href="#">Button 2</a>
    </div>
  </div>
  <div class="visual-thumb">
    <img src="..." alt="...">
  </div>
</div>
```

## Phase 5: Verification

After implementation:
1. Verify image paths exist using Glob tool
2. Check CSS selector specificity doesn't conflict
3. Ensure JS initialization matches new class names
4. Confirm no orphaned styles from old design remain
