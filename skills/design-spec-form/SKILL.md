---
name: design-spec-form
description: |
  Translates vague human prompts into a precise 50-field Design Spec Form, then generates
  websites using those exact values. Eliminates "AI-looking" results by removing all
  interpretation room — every color, font weight, spacing, and interaction is decided
  BEFORE code generation begins.

  Use this skill when:
  - User wants to create a website/landing page and wants precise, non-generic design
  - User says "디자인 스펙", "스펙 폼", "design spec", "design-spec-form"
  - User says "AI스럽지 않게", "인공지능 느낌 없이", "제네릭하지 않게"
  - User wants to see the design decisions before code generation
  - User asks for a "디자인 브리프", "디자인 시스템 생성", "수치화"
  - User mentions wanting different/unique designs each time
  - Before running supanova-forge or ansible-prism, when quality control over design tokens matters

  Trigger aggressively when: website creation + any mention of design quality, uniqueness,
  non-AI aesthetics, or wanting to review design decisions before building.
---

# Design Spec Form

## CONCEPT

This skill solves a fundamental problem: **humans describe designs in feelings ("따뜻하게", "세련되게"), but code requires exact values (HSL, px, Tailwind classes).** The gap between these two produces "AI-looking" results — where the AI fills in vague specifications with generic defaults.

The solution: a **50-field Design Spec Form** that acts as a mandatory translation layer.

```
Human input (feeling)     →  AI translates  →  50-field Form (exact values)  →  Code generation
"따뜻하고 신뢰감 있게"        내부 처리          C04: 24 85% 52%                 수치 기반 구현
                                               T04: font-medium
                                               N01: floating
                                               ...48 more fields
```

The form STRUCTURE is fixed (always the same 50 fields). The VALUES change every time. This means:
- Every project gets a completely unique visual identity
- Zero room for AI to fall back on generic patterns
- The user can review and adjust values before code is written

---

## WORKFLOW

### Step 1: Receive Input

Accept any level of specificity from the user. All of these are valid inputs:

```
Level 1 (느낌만): "따뜻하고 신뢰감 있는 교육 포털"
Level 2 (방향성): "흰 배경, 주황 포인트, 세리프 제목, 미니멀"
Level 3 (부분 지정): "배경 #FFF7ED, 폰트 Pretendard, 나머지는 알아서"
Level 4 (레퍼런스): "이 사이트처럼 만들어줘" + URL/스크린샷
```

No level is wrong. The less specific the input, the more creative freedom you have in filling the form — but every field still gets a concrete value.

**Brand Override Rule:** When the user provides a brand identity spec, design system, or CI document, its values take absolute priority over the aesthetics engine's avoid rules. If the brand uses Inter → use Inter. If the brand uses blue CTA on white → use it. The aesthetics engine's filters apply ONLY to fields that the brand doc does NOT constrain. Mark overridden fields with `[BRAND]` in the form output.

### Step 2: Interpret the Prompt

Before filling the form, analyze the input to extract design direction:

**Feeling Keywords → Design Direction Mapping:**

| 키워드 | Color 방향 | Type 방향 | Layout 방향 | Motion 방향 |
|--------|-----------|----------|------------|------------|
| 따뜻한, 포근한, 편안한 | warm HSL (H:15-40), muted saturation | serif display, relaxed leading | spacious, balanced symmetry | ease-out, gentle |
| 차가운, 모던, 테크 | cool HSL (H:200-260), high contrast | sans-serif, tight tracking | compact, asymmetric | snappy bezier, precise |
| 세련된, 고급, 럭셔리 | low saturation, deep tones | medium weight (NOT bold), tight | editorial-offset, asymmetric-bleed | slow, deliberate |
| 강렬한, 임팩트, 에너지 | high saturation, complementary | black/heavy weight, condensed | asymmetric, bleed both | fast, scale-based |
| 부드러운, 감성, 여성적 | pastel, warm white bg | rounded sans, wide tracking | centered-stack, generous spacing | gentle, slow |
| 신뢰, 공공, 기관 | conservative, blue-green family | clean sans, balanced weight | symmetric, structured grid | minimal, professional |
| 자연, 오가닉, 건강 | earth tones (H:80-160), low sat | humanist sans + serif accent | flowing, generous whitespace | organic, ease-in-out |

This is a starting point, not a rigid lookup. Blend multiple keywords and add your own interpretation.

### Step 3: Fill the Form

**Before filling any field**, read these two reference files in order:
1. `references/aesthetics-engine.md` — Anti-AI-Slop processing rules. This is your **mindset** while filling. It contains forbidden fonts, color clichés to avoid, layout anti-patterns, and a final checklist.
2. `references/form-template.md` — The 50-field structure with harmony rules and examples.

The aesthetics engine is not optional. It is the quality floor that prevents generic output. Every value you write must pass through its filters — if the engine says "avoid Inter", then T01/T02 cannot be Inter regardless of the prompt. If the engine says "avoid purple gradient on white", then C08/C09 cannot be purple on a white C01.

**Mandatory rules when filling:**

1. **Every field gets a concrete value.** No "auto", "default", "varies", or "TBD".
2. **Internal consistency matters.** The 50 values must feel like they belong to ONE design system, not 50 random choices. Follow the harmony rules in each category.
3. **Avoid the Generic 5.** These are the most common AI defaults — actively avoid them unless the input specifically demands them:
   - `font-bold` for headings (prefer `font-medium` or `font-semibold`)
   - `rounded-lg` for everything (vary by component: nav vs button vs card)
   - `shadow-md` for depth (prefer `shadow-sm`, tinted shadows, or border-based depth)
   - `gap-4` everywhere (vary: `gap-3` for tight, `gap-6` for breathing, `gap-8` for sections)
   - `hover:bg-[darker-color]` (prefer opacity shift, scale, border color, or glow)

4. **The Gradient Button Rule.** Unless the design is explicitly minimal/flat, always consider gradient buttons (`B01: gradient`). The micro-gradient from C08→C09 creates physical depth that single-color buttons cannot. This is the single highest-impact anti-AI pattern.

5. **The Weight Rule.** `font-medium` headings + `font-normal` body = professional. `font-bold` headings + `font-normal` body = generic. `font-black` headings are only for `bold` vibe or impact-focused designs.

6. **The Asymmetry Rule.** At least ONE layout field (L01-L05) should break perfect symmetry. Perfect symmetry = AI default. Even one asymmetric choice (e.g., `L05: right` bleed) transforms the feel.

### Step 4: Present the Form

Show the completed form to the user using the format in `references/form-template.md` (the boxed output format at the bottom).

After presenting, ask:

```
📐 스펙 폼 완성! 검토 후 알려주세요:
  • 이대로 진행 → "진행" 또는 "ㅇㅇ"
  • 수정할 항목 → 필드 번호로 알려주세요 (예: "C04를 좀 더 진한 오렌지로", "T04를 bold로")
  • 전체 방향 수정 → "더 차갑게", "더 대담하게" 등 느낌으로
```

### Step 5: Generate Code

Once the user approves (or immediately if they skip review), generate the website HTML.

**Pre-generation validation:** Before writing any code, run the 10-item checklist at the bottom of `references/aesthetics-engine.md`. If any item fails, fix the form value first, then proceed.

**Code generation rules:**

1. **The form IS the design system.** Every CSS value, Tailwind class, and style decision must trace back to a specific form field. If you're writing a color that isn't in C01-C09, you're improvising — stop and derive it from the form.

2. **CSS Custom Properties first.** Convert form values to `:root` variables:
   ```css
   :root {
     --bg-primary: C01;
     --bg-secondary: C02;
     --fg: C03;
     --accent: C04;
     --accent-hover: C05;
     /* ... all 9 color fields */
   }
   ```

3. **Tailwind config extension.** Extend Tailwind with the form's typography:
   ```js
   tailwind.config = {
     theme: {
       extend: {
         fontFamily: {
           display: [T01],
           sans: [T02],
         }
       }
     }
   }
   ```

4. **One HTML file.** Output is a complete, standalone HTML file. Include:
   - Tailwind CDN
   - Google Fonts (for T01, T02)
   - Iconify (for icons)
   - All CSS custom properties
   - Responsive design
   - Accessibility basics (lang, alt, aria-labels)
   - Scroll reveal animations (if M04 ≠ none)

5. **Section structure.** Generate 5-7 sections minimum:
   - Navbar (based on N01-N05)
   - Hero (based on L01, L04, L05)
   - 3-5 content sections (alternating per L03)
   - Contact/CTA section
   - Footer

---

## FORM FIELD MODIFICATION

When the user requests changes to specific fields after seeing the form:

**By field number:**
```
User: "C04를 더 진하게"
→ C04의 L(lightness)를 10-15% 낮춤, C05/C08/C09도 연동 조정
→ 수정된 폼 다시 표시
```

**By feeling:**
```
User: "전체적으로 더 차갑게"
→ Color 카테고리 전체의 hue를 cool 방향(200-260)으로 시프트
→ Typography의 display font를 sans-serif 계열로 변경
→ 수정된 폼 다시 표시
```

**By reference:**
```
User: "네비를 이 사이트처럼" + 스크린샷
→ N01-N05만 분석하여 해당 사이트의 패턴으로 교체
→ 나머지 46개 필드는 유지
→ 수정된 폼 다시 표시
```

---

## INTEGRATION WITH OTHER SKILLS

This skill generates the Design Spec Form. Code generation can be done by this skill directly, OR the form can be handed off to other skills:

**→ supanova-forge**: Form을 생성 후, supanova-forge에 "이 스펙으로 만들어줘"라고 전달
**→ ansible-prism**: Form을 생성 후, ansible-prism에 스펙 전달
**→ frontend-design**: Form을 생성 후, React 컴포넌트 생성에 활용
**→ section-redesign**: 기존 사이트의 특정 섹션에 Form의 값을 적용

User가 다른 스킬과의 연동을 요청하면, 폼의 50개 값을 해당 스킬이 이해할 수 있는 형태로 변환하여 전달한다.

---

## EXAMPLES

### Example 1: Vague Input

**Input:** "따뜻하고 신뢰감 있는 교육 포털"

**Interpretation:**
- 따뜻한 → warm hue (H:20-35), cream backgrounds, serif display
- 신뢰감 → conservative saturation, structured layout, professional motion
- 교육 포털 → clean grid, readable body, functional cards

**Form excerpt (not full — illustrative):**
```
C01 bg-primary       : 30 20% 98%           (warm off-white)
C04 accent-primary   : 24 75% 50%           (trustworthy warm orange)
T01 display-font     : "Noto Serif KR", serif
T04 h1-weight        : font-semibold
N01 nav-pattern      : sticky-bordered
L01 hero-pattern     : split-equal
B01 primary-style    : gradient
```

### Example 2: Specific Input

**Input:** "테크 스타트업. 다크 배경, 네온 그린 포인트, 날카롭게"

**Interpretation:**
- 테크 → cool tones, sans-serif, tight spacing
- 다크 배경 → near-black primary, light text
- 네온 그린 → high saturation green accent
- 날카롭게 → rounded-none, tight tracking, snappy motion

**Form excerpt:**
```
C01 bg-primary       : 240 10% 5%            (near-black)
C04 accent-primary   : 145 90% 55%           (neon green)
T01 display-font     : "Space Grotesk", sans-serif
T04 h1-weight        : font-medium
T05 h1-tracking      : tracking-[-0.03em]
N01 nav-pattern      : floating
S05 radius-scale     : rounded-none
B01 primary-style    : glass
M02 timing-function  : cubic-bezier(0.16, 1, 0.3, 1)
```

### Example 3: Reference-Based Input

**Input:** "이 사이트 느낌으로" + nickel.co 스크린샷

**Process:**
1. 스크린샷에서 시각 요소 분석 (색상, 타이포, 레이아웃, 네비 패턴)
2. 분석 결과를 50필드에 매핑
3. 원본을 복제하는 게 아니라, 원본의 "설계 의도"를 추출하여 새로운 수치로 재해석

---

## ANTI-PATTERNS (절대 하지 않을 것)

1. **폼 필드를 비워두거나 "auto"로 채우지 않는다.** 50개 전부 구체적 값 필수.
2. **코드 생성 중에 폼에 없는 새로운 디자인 결정을 하지 않는다.** 폼이 곧 설계도.
3. **매번 같은 값 조합을 반복하지 않는다.** 같은 입력("교육 포털")이라도 매번 다른 50개 값을 생성.
4. **"Generic 5"에 안주하지 않는다.** (font-bold, rounded-lg, shadow-md, gap-4, hover:bg-darker)
5. **일관성 없이 값을 섞지 않는다.** 50개 값은 하나의 통일된 성격을 가져야 함.
