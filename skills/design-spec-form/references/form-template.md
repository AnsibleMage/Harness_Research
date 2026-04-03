# Design Spec Form — 50-Field Template

> This is the fixed structure. Every field MUST be filled with a concrete value.
> Never leave a field as "auto", "default", or "TBD".
> The combination of all 50 values defines the unique visual identity of a single project.

---

## How to Read This Template

- `Field Name` — description → `example value`
- HSL values use the format: `H S% L%` (e.g., `24 90% 55%`)
- Tailwind classes are written as-is (e.g., `text-5xl`, `rounded-xl`)
- Choice fields list options in `(option-a / option-b / option-c)` format

---

## CATEGORY 1: COLOR (9 fields)

```
[C01] bg-primary        — 페이지 주 배경색 HSL           → e.g., 30 20% 97%
[C02] bg-secondary      — 교차 섹션 배경색 HSL            → e.g., 25 30% 95%
[C03] fg-primary        — 본문 텍스트 HSL                → e.g., 220 10% 10%
[C04] accent-primary    — 주 포인트 색상 HSL              → e.g., 24 90% 55%
[C05] accent-hover      — 포인트 hover 상태 HSL           → e.g., 20 92% 45%
[C06] muted-text        — 보조/설명 텍스트 HSL            → e.g., 220 5% 46%
[C07] border-color      — 기본 보더 HSL                  → e.g., 220 10% 88%
[C08] gradient-start    — 그라데이션 시작 HSL (버튼/장식)  → e.g., 24 100% 72%
[C09] gradient-end      — 그라데이션 끝 HSL               → e.g., 18 98% 53%
```

### Color Harmony Rules
- C01과 C02는 같은 색상 계열이되 명도 차이 2-5% (미묘한 리듬)
- C04와 C05는 같은 hue에서 명도만 -8~-12% (hover 깊이감)
- C08과 C09는 hue 차이 4-8도 + 명도 차이 15-20% (미세 그라데이션)
- C06은 C03과 같은 hue, 채도 낮추고 명도 올림

---

## CATEGORY 2: TYPOGRAPHY (9 fields)

```
[T01] display-font      — 제목/장식용 폰트                → e.g., "Playfair Display", serif
[T02] body-font         — 본문 폰트                      → e.g., "Pretendard", system-ui, sans-serif
[T03] h1-size           — H1 반응형 (sm / md / lg)       → e.g., text-4xl / text-6xl / text-7xl
[T04] h1-weight         — H1 굵기                        → e.g., font-medium
[T05] h1-tracking       — H1 자간                        → e.g., tracking-[-0.04em]
[T06] h1-leading        — H1 행간                        → e.g., leading-[1.05]
[T07] body-size         — 본문 크기                       → e.g., text-base sm:text-lg
[T08] body-leading      — 본문 행간                       → e.g., leading-relaxed
[T09] label-style       — 라벨/캡션 스타일                 → e.g., text-sm tracking-[0.15em] uppercase font-medium
```

### Typography Pairing Rules
- T01(display)와 T02(body)는 반드시 다른 계열 (serif+sans, sans+slab 등)
- T04는 font-bold 대신 font-medium이나 font-semibold를 우선 고려 (세련됨)
- T05 자간이 tight하면 T06 행간은 넓게, 반대도 성립 (가독성 보상)
- T09 라벨은 uppercase + wide tracking일 때 font-size를 한 단계 줄임

---

## CATEGORY 3: SPACING (5 fields)

```
[S01] container-width   — 콘텐츠 최대 너비               → e.g., max-w-7xl
[S02] section-padding   — 섹션 상하 여백                  → e.g., py-24 md:py-32
[S03] card-padding      — 카드 내부 여백                  → e.g., p-6 md:p-8
[S04] component-gap     — 컴포넌트 간 간격                → e.g., gap-6
[S05] radius-scale      — 기본 border-radius              → e.g., rounded-none / rounded-lg / rounded-xl / rounded-2xl
```

### Spacing Personality
- S05가 rounded-none이면 전체적으로 "날카로운" 성격 → S02 여백을 더 넓게
- S05가 rounded-2xl이면 "부드러운" 성격 → 전체 밀도를 낮추고 S04 간격 넓게

---

## CATEGORY 4: NAVIGATION (5 fields)

```
[N01] nav-pattern       — 네비게이션 유형                  → (floating / sticky-flush / sticky-bordered)
[N02] nav-background    — 네비 배경                       → e.g., bg-white, bg-white/90 backdrop-blur-md
[N03] nav-shadow        — 네비 그림자                      → (none / shadow-sm / shadow-md)
[N04] nav-radius        — 네비 border-radius (floating시)  → e.g., rounded-xl / rounded-2xl
[N05] nav-link-hover    — 링크 hover 방식                  → (underline-slide / color-change / opacity-shift / bg-fill)
```

### Navigation Pattern Details
- **floating**: outer wrapper에 px+pt 패딩 → inner nav에 bg+radius+shadow → 공중에 뜬 느낌
- **sticky-flush**: top-0에 붙고 full-width → border-bottom으로 구분
- **sticky-bordered**: sticky + scroll시 backdrop-blur 배경 전환

---

## CATEGORY 5: BUTTONS (6 fields)

```
[B01] primary-style     — 주 버튼 스타일                   → (flat / gradient / outline / glass)
[B02] primary-radius    — 주 버튼 radius                  → e.g., rounded-lg / rounded-full
[B03] primary-padding   — 주 버튼 패딩                     → e.g., px-8 py-3.5
[B04] primary-weight    — 주 버튼 font-weight              → e.g., font-medium
[B05] primary-hover     — 주 버튼 hover 동작               → (opacity / darken / scale / glow / lift)
[B06] secondary-style   — 보조 버튼 스타일                  → (outline / ghost / subtle-fill)
```

### Button Style Details
- **gradient**: `bg-gradient-to-b from-[hsl(C08)] to-[hsl(C09)]` — 위→아래 미세 그라데이션, 물리적 깊이감
- **glass**: `bg-white/10 backdrop-blur-md border border-white/20` — 유리 질감
- **flat**: `bg-[hsl(C04)] text-white` — 단색 채움
- **outline**: `border-2 border-[hsl(C04)] text-[hsl(C04)]` hover시 채움 전환

---

## CATEGORY 6: LAYOUT (5 fields)

```
[L01] hero-pattern      — 히어로 레이아웃                  → (split-equal / asymmetric-bleed / centered-stack / editorial-offset)
[L02] grid-symmetry     — 그리드 대칭성                    → (symmetric / asymmetric / mixed)
[L03] section-rhythm    — 섹션 색상 교차 패턴              → (mono / light-tint / light-dark / gradient-flow)
[L04] visual-weight     — 시각적 무게 중심                  → (left / right / center)
[L05] bleed-direction   — 블리딩(화면 끝까지) 방향          → (none / left / right / both)
```

### Layout Pattern Details
- **asymmetric-bleed**: 한쪽은 max-w-xl 텍스트, 반대쪽은 absolute로 화면 끝까지 이미지/비디오 블리딩
- **editorial-offset**: 텍스트가 그리드 중앙에서 2-3 column 이동, 이미지가 반대편으로 오프셋
- **split-equal**: 전통적 50:50 그리드, 안정감
- **centered-stack**: 모든 요소 중앙 정렬, 순차 배치

---

## CATEGORY 7: CARDS (4 fields)

```
[K01] card-border       — 카드 테두리                      → (line / shadow / none / tinted-shadow)
[K02] card-radius       — 카드 radius                     → e.g., rounded-lg / rounded-xl / rounded-none
[K03] card-hover        — 카드 hover 효과                  → (lift / border-accent / scale / glow / tilt-3d)
[K04] image-treatment   — 이미지 처리                      → (color / grayscale-to-color / overlay-gradient / duotone / soft-blur)
```

### Card Hover Details
- **lift**: `hover:-translate-y-1 hover:shadow-lg` — 살짝 떠오름
- **border-accent**: `hover:border-[hsl(C04)]` — 보더 색상 전환
- **tilt-3d**: `hover:rotate-x-2 hover:rotate-y-2` (transform-3d) — 미세 기울기
- **glow**: `hover:shadow-[0_0_30px_hsl(C04/0.15)]` — 포인트색 글로우

---

## CATEGORY 8: MOTION (4 fields)

```
[M01] hover-transition  — hover 전환 종류                  → (color / opacity / scale / translate / multi)
[M02] timing-function   — easing 함수                     → e.g., cubic-bezier(0.16, 1, 0.3, 1)
[M03] duration          — 전환 지속 시간                    → e.g., duration-300 / duration-500
[M04] scroll-reveal     — 스크롤 등장 애니메이션             → (fade-up / slide-left / scale-in / none)
```

### Motion Personality
- M02가 aggressive bezier(0.16,1,0.3,1)이면 전체적으로 "빠르고 정확한" 느낌
- M02가 ease-out이면 "부드럽고 여유로운" 느낌
- M03 duration은 M02와 반비례: aggressive bezier → longer duration OK, ease-out → shorter duration

---

## CATEGORY 9: DECORATION (3 fields)

```
[D01] bg-element        — 배경 장식 요소                   → (behind-text / grain-texture / geometric-svg / gradient-orbs / none)
[D02] density           — 전체 밀도감                      → (spacious / balanced / compact)
[D03] section-divider   — 섹션 간 구분 방식                → (color-change / border-line / whitespace / gradient-fade)
```

### Decoration Rules
- D01이 grain-texture이면 `opacity: 0.015` 이하로 아주 미세하게
- D01이 behind-text이면 `font-size: 10-14vw`, `opacity: 0.03-0.06`, 장식용 영문
- D02가 spacious이면 S02 section-padding을 py-32 md:py-40 수준으로

---

## FORM OUTPUT FORMAT

When presenting the completed form to the user, use this exact format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📐 DESIGN SPEC FORM — [프로젝트명]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 COLOR
  C01 bg-primary       : [value]
  C02 bg-secondary     : [value]
  C03 fg-primary       : [value]
  C04 accent-primary   : [value]
  C05 accent-hover     : [value]
  C06 muted-text       : [value]
  C07 border-color     : [value]
  C08 gradient-start   : [value]
  C09 gradient-end     : [value]

🔤 TYPOGRAPHY
  T01 display-font     : [value]
  T02 body-font        : [value]
  T03 h1-size          : [value]
  T04 h1-weight        : [value]
  T05 h1-tracking      : [value]
  T06 h1-leading       : [value]
  T07 body-size        : [value]
  T08 body-leading     : [value]
  T09 label-style      : [value]

📏 SPACING
  S01 container-width  : [value]
  S02 section-padding  : [value]
  S03 card-padding     : [value]
  S04 component-gap    : [value]
  S05 radius-scale     : [value]

🧭 NAVIGATION
  N01 nav-pattern      : [value]
  N02 nav-background   : [value]
  N03 nav-shadow       : [value]
  N04 nav-radius       : [value]
  N05 nav-link-hover   : [value]

🔘 BUTTONS
  B01 primary-style    : [value]
  B02 primary-radius   : [value]
  B03 primary-padding  : [value]
  B04 primary-weight   : [value]
  B05 primary-hover    : [value]
  B06 secondary-style  : [value]

📐 LAYOUT
  L01 hero-pattern     : [value]
  L02 grid-symmetry    : [value]
  L03 section-rhythm   : [value]
  L04 visual-weight    : [value]
  L05 bleed-direction  : [value]

🃏 CARDS
  K01 card-border      : [value]
  K02 card-radius      : [value]
  K03 card-hover       : [value]
  K04 image-treatment  : [value]

✨ MOTION
  M01 hover-transition : [value]
  M02 timing-function  : [value]
  M03 duration         : [value]
  M04 scroll-reveal    : [value]

🎭 DECORATION
  D01 bg-element       : [value]
  D02 density          : [value]
  D03 section-divider  : [value]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
