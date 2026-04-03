# SLOT ENGINE v1.0 — 조합 다양성 엔진

> CREATIVE_GENERATION_FRAMEWORK에서 분리된 모듈.
> 5슬롯 × 20개 값 = 3,200,000 고유 조합 가능.
> 각 값은 실제 고품질 사이트에서 추출한 디자인 패턴 기반.

---

## 사용법

```
1. CREATIVE_GENERATION_FRAMEWORK.md의 STEP 3에서 이 파일 참조
2. 각 슬롯에서 1개씩 선택 (5개 슬롯 × 1개 값 = 1 조합)
3. 이전 생성과 4차원 DIM 모두 달라야 함
4. 선택한 값의 Execution Spec에 따라 CSS/HTML 구현
```

---

## SLOT_1: VISUAL IDENTITY (시각 정체성) — 20개

> 이전명: 메타포. CSS 변수명, border, texture, card, button, nav 스타일을 결정.
> 출처: Awwwards SOTD, Behance Top Projects, 한국 수상 사이트.

### 1-01. 활판인쇄소 (Letterpress Studio)
- **참조**: Copenhagen Archive (Awwwards SOTD 2025)
- css_vars: `--press, --paper, --ink, --stamp, --rule`
- border: `2px solid var(--ink)`. radius: 0. 인쇄 프레임.
- texture: 없음. 종이 질감은 배경색으로.
- card: 사각, 날카로운 모서리, 인쇄물 느낌. 패딩 넉넉.
- button: outline 스타일. hover 시 fill 반전.
- nav: serif 로고. 소문자 링크. 얇은 라벨 바.
- 특수: `::before` 3px 세로 바 마커. blockquote 큰 따옴표.

### 1-02. 글래스 스튜디오 (Glass Studio)
- **참조**: Attio, Apple Vision Pro 사이트
- css_vars: `--glass, --frost, --refract, --clarity, --haze`
- border: `1px solid rgba(255,255,255,0.12)`. radius: 12px (예외적 허용).
- texture: 없음. `backdrop-filter: blur(20px)` 글래스모피즘.
- card: 반투명 배경. `background: rgba(255,255,255,0.04~0.08)`.
- button: 반투명 + blur. hover 시 opacity 증가.
- nav: 투명 + blur. 스크롤 시 blur 강도 변화.
- 특수: 카드 뒤 요소가 비침. 겹침 레이어 연출.

### 1-03. 건축사무소 (Architecture Firm)
- **참조**: Zaha Hadid Architects, Foster + Partners
- css_vars: `--concrete, --blueprint, --steel, --beam, --draft`
- border: `border-left: 4px solid`. 한 면만 강조. radius: 0.
- texture: `repeating-linear-gradient` 미세 격자 (청사진 모눈).
- card: 직각 정렬. 상단에 도면 번호 라벨 (`DWG-01`).
- button: outline. 직각. uppercase letter-spacing.
- nav: 좁은 바. uppercase. letter-spacing 3px+.
- 특수: 카드 상단 좌측에 분류 코드. gap 정밀 통일.

### 1-04. 갤러리 화이트큐브 (Gallery White Cube)
- **참조**: Gagosian, White Cube London
- css_vars: `--wall, --frame, --plinth, --spotlight, --void`
- border: 없음. 그림자/간격으로만 분리. radius: 0.
- texture: 없음. 순백 벽면.
- card: 콘텐츠=작품. 설명은 14px 아래에. 압도적 여백.
- button: 텍스트 링크만 (버튼 형태 지양). underline hover.
- nav: 극미니멀. 로고+필수 링크만. font-weight 300.
- 특수: 여백이 콘텐츠. 하나의 큰 이미지 + 작은 캡션.

### 1-05. 레코드 숍 (Record Shop)
- **참조**: Spotify 연말 결산, Vinyl Me Please
- css_vars: `--vinyl, --sleeve, --groove, --amp, --wax`
- border: 없음 또는 1px. radius: 0. LP 재킷 직각.
- texture: 미세 노이즈 grain 오버레이.
- card: 정사각~4:3. 큰 썸네일 중심. 텍스트 최소.
- button: fill. 직각. hover 시 색상 반전.
- nav: 간판 느낌. 로고 크게. 링크 적게.
- 특수: 재생 관련 원형 모티프. 큰 이미지 카드.

### 1-06. 천문대 (Observatory)
- **참조**: NASA JPL, SpaceX Starship
- css_vars: `--void, --nebula, --star, --corona, --dust`
- border: 없음. `box-shadow: 0 0 Npx rgba(glow)` 대체.
- texture: `radial-gradient` 점 패턴 (별자리) 또는 없음.
- card: 어둠에 떠 있는 느낌. `backdrop-filter: blur`. 글래스.
- button: glow 효과. `border: 1px solid rgba(빛)`. hover 광도↑.
- nav: 투명 오버레이. 텍스트만 보임. 배경 투과.
- 특수: `tabular-nums`. 큰 숫자 glow. 데이터 계기판.

### 1-07. 무인양품 (MUJI Minimal)
- **참조**: 무인양품 온라인스토어, Aesop
- css_vars: `--linen, --ash, --cedar, --rice, --stone`
- border: `1px solid rgba(0,0,0,0.06)`. radius: 2px.
- texture: 없음. 극도의 절제.
- card: 얇은 선 구분. 넉넉한 여백. 최소 장식.
- button: 가느다란 outline. 작은 크기. 조용한.
- nav: 시스템 폰트. 최소 링크. 넓은 간격.
- 특수: 여백 비율이 콘텐츠보다 크다. 침묵의 디자인.

### 1-08. 네온사인 (Neon Sign)
- **참조**: Huly, Twingate, 클럽/바 사이트
- css_vars: `--dark, --neon, --glow, --concrete, --smoke`
- border: `1px solid rgba(accent,0.3)`. radius: 8px. glow shadow.
- texture: 미세 노이즈 grain on dark.
- card: 다크 배경 + 네온 accent border/glow.
- button: fill accent + glow shadow. hover 시 pulse.
- nav: 다크 배경. accent 텍스트 or glow.
- 특수: `text-shadow: 0 0 10px` 네온 글로우. 하나의 색만 빛남.

### 1-09. 북바인더리 (Bookbindery)
- **참조**: 세종대 학술정보원, 국립중앙도서관
- css_vars: `--spine, --page, --leather, --gilt, --ribbon`
- border: `1px solid var(--gilt)`. radius: 4px. 책등 느낌.
- texture: 없음.
- card: 세로형 (3:4 비율). 책 표지 느낌.
- button: fill + serif 텍스트. 고급 인쇄 느낌.
- nav: 두꺼운 상단 바. 도서관 카탈로그 느낌.
- 특수: 세로형 카드 중심. 책 표지 그리드.

### 1-10. 약국 서랍장 (Pharmacy Cabinet)
- **참조**: 올리브영, Boots UK
- css_vars: `--cabinet, --label, --vial, --brass, --remedy`
- border: `1px solid`. radius: 2px. 정밀한 서랍 테두리.
- texture: 없음.
- card: 서랍 하나=카드 하나. 라벨+내용 명확.
- button: 작은 라벨 태그. padding 작음. font-weight bold.
- nav: 탭 형태 (서랍 손잡이). 가로 일렬.
- 특수: 카드 상단 분류 라벨 필수. 번호+이름 체계.

### 1-11. 재봉공방 (Tailor Workshop)
- **참조**: Etsy, 핸드메이드 마켓플레이스
- css_vars: `--fabric, --thread, --needle, --patch, --spool`
- border: `1px dashed`. 바느질 선. radius: 6px.
- texture: `repeating-linear-gradient 45deg` 직물 직조.
- card: 패치워크. 카드마다 미묘하게 다른 배경색.
- button: `border-radius: 20px+` 단추 느낌.
- nav: 부드러운 둥근 모서리. 아기자기.
- 특수: dashed 구분선. wavy 장식.

### 1-12. 지도제작실 (Cartography Studio)
- **참조**: National Geographic, Mapbox
- css_vars: `--parchment, --vellum, --ink, --sepia, --terracotta`
- border: `1px solid rgba(0,0,0,0.08)`. radius: 4px.
- texture: `repeating-linear-gradient 160deg` 등고선.
- card: 정밀 배치. 좌표 라벨 느낌.
- button: fill. 탐험 동사 사용.
- nav: 사이드바(범례 패널) 또는 미니멀 상단.
- 특수: monospace 숫자/좌표. 데이터 라벨.

### 1-13. 온실 (Greenhouse)
- **참조**: Aesop, 이솝 가든
- css_vars: `--glass, --leaf, --soil, --dew, --canopy`
- border: 없음 또는 `rgba(0,0,0,0.03)`. radius: 8px.
- texture: 없음. 투명 빛 통과.
- card: 가벼움. 그림자 없음. padding 넉넉.
- button: 투명 + 텍스트만. 또는 얇은 outline.
- nav: 반투명 `backdrop-filter: blur`. 떠 있는 느낌.
- 특수: 요소 간 gap 넓음 (공기감). 부드러운 transition.

### 1-14. 다크룸 (Darkroom)
- **참조**: Resend, Linear, Raycast
- css_vars: `--darkroom, --safelight, --fixer, --grain, --negative`
- border: `1px solid rgba(255,255,255,0.06)`. radius: 8px.
- texture: 미세 grain 노이즈 오버레이 (필름 입자).
- card: 다크 배경. 밝은 텍스트. 미니멀.
- button: 밝은 fill on dark. 작은 radius.
- nav: 다크 배경 + 밝은 텍스트. 미니멀.
- 특수: 코드블록 스타일 UI. 개발자 도구 느낌.

### 1-15. 미술관 카페 (Museum Café)
- **참조**: Blue Bottle, 떠뜯 카페
- css_vars: `--espresso, --cream, --ceramic, --steam, --counter`
- border: 없음. 배경색 차이로 분리. radius: 8px.
- texture: 없음.
- card: 따뜻한 배경에 둥근 모서리. 부드러운 그림자.
- button: 따뜻한 fill. 둥근 모서리. 친근한.
- nav: 미니멀. 따뜻한 색조. serif 또는 rounded sans.
- 특수: 따뜻한 톤 + 부드러운 곡선. 라떼 아트 느낌.

### 1-16. 공사현장 (Construction Site)
- **참조**: WeWork, 산업 브랜드
- css_vars: `--rebar, --safety, --scaffold, --hard, --zone`
- border: `2px solid`. radius: 0. 거친 산업 느낌.
- texture: 대각선 스트라이프 (경고 테이프).
- card: 두꺼운 보더. 높은 대비. bold 텍스트.
- button: 크고 두꺼운. uppercase. 강한 fill.
- nav: 두꺼운 상단 바. 안전 색상 계열.
- 특수: 경고 테이프 패턴. 높은 대비 색상.

### 1-17. 일본정원 (Japanese Garden)
- **참조**: Aman Resorts, 료칸 웹사이트
- css_vars: `--tatami, --zen, --bamboo, --moss, --mist`
- border: 없음. 공간(ma)으로 분리. radius: 0.
- texture: 없음. 극도의 여백.
- card: 수평 긴 카드. 텍스트 좌측, 이미지 우측.
- button: 텍스트만. 밑줄. 작은 화살표.
- nav: 극미니멀. 넓은 자간. 가벼운 weight.
- 특수: 비대칭 여백. 수평선 구분. 호흡하는 레이아웃.

### 1-18. 실험실 (Laboratory)
- **참조**: 23andMe, 의료 SaaS
- css_vars: `--lab, --sample, --pipette, --clean, --data`
- border: `1px solid rgba(0,0,0,0.08)`. radius: 8px.
- texture: 없음. 깨끗한 표면.
- card: 데이터 카드. 숫자 강조. 정밀 레이아웃.
- button: pill 형태. `border-radius: 999px`.
- nav: 미니멀 + 검색 강조. 깔끔.
- 특수: 데이터 시각화 요소. 차트/게이지. pill 버튼.

### 1-19. 빈티지 포스터 (Vintage Poster)
- **참조**: Behance 타이포 프로젝트, 영화 포스터
- css_vars: `--poster, --headline, --torn, --stamp, --fade`
- border: 없음. 텍스트 크기 차이로 구분. radius: 0.
- texture: 미세 노이즈 (오래된 종이).
- card: 텍스트가 곧 카드. 거대 타이포.
- button: 텍스트만. uppercase. 큰 크기.
- nav: 거대 타이포 메뉴. 전체 화면 메뉴.
- 특수: `font-size: 80px+` 거대 제목. 텍스트=디자인.

### 1-20. 미디어 플레이어 (Media Player)
- **참조**: Netflix, Spotify, YouTube
- css_vars: `--screen, --control, --progress, --thumb, --queue`
- border: 없음 또는 미세. radius: 4~8px.
- texture: 없음.
- card: 16:9 썸네일 중심. 메타데이터 하단.
- button: pill 또는 circle (재생 버튼). fill.
- nav: 상단 고정 + 사이드바 가능.
- 특수: 진행 바. 썸네일 hover 확대. 가로 스크롤 행.

---

## SLOT_2: COLOR TEMPERATURE (색온도) — 20개

> CSS color 값 결정. DIM_2 (base bg 계열) 핵심.
> 출처: 실제 사이트 추출 hex + Tailwind/Radix 팔레트.

### 2-01. 순백 (Pure White)
- base_bg: `#ffffff`
- card_bg: `#f8f9fa`
- dark_bg: `#111827`
- heading: `#111827`
- body: `#6b7280`
- muted: `#9ca3af`
- accent_pool: `[#2563eb, #7c3aed, #059669]`
- feel: 깨끗, 중립, 만능

### 2-02. 쿨 그레이 (Cool Gray)
- base_bg: `#f8fafc`
- card_bg: `#f1f5f9`
- dark_bg: `#0f172a`
- heading: `#0f172a`
- body: `#475569`
- muted: `#94a3b8`
- accent_pool: `[#3b82f6, #06b6d4, #8b5cf6]`
- feel: 테크, 프로, SaaS

### 2-03. 웜 크림 (Warm Cream)
- base_bg: `#f5f0e8`
- card_bg: `#fffcf7`
- dark_bg: `#1c1917`
- heading: `#1c1917`
- body: `#78716c`
- muted: `#a8a29e`
- accent_pool: `[#c05621, #b45309, #a16207]`
- feel: 따뜻한, 교육, 커뮤니티

### 2-04. 양피지 (Parchment)
- base_bg: `#f9f6f1`
- card_bg: `#f0ebe3`
- dark_bg: `#1a1612`
- heading: `#1a1612`
- body: `#6b5c4d`
- muted: `#a39585`
- accent_pool: `[#c45d3e, #92400e, #b45309]`
- feel: 대지, 탐험, 고고학

### 2-05. 딥 네이비 (Deep Navy)
- base_bg: `#0f172a`
- card_bg: `rgba(255,255,255,0.04)`
- dark_bg: `#020617`
- heading: `#f8fafc`
- body: `#94a3b8`
- muted: `#475569`
- accent_pool: `[#38bdf8, #818cf8, #34d399]`
- feel: 프리미엄 다크, 천문, 밤

### 2-06. 차콜 (Charcoal)
- base_bg: `#1c1c1e`
- card_bg: `#2c2c2e`
- dark_bg: `#000000`
- heading: `#ffffff`
- body: `#aeaeb2`
- muted: `#636366`
- accent_pool: `[#ff3b30, #ff6b00, #ff2d55]`
- feel: 도시적, 모던, 대비

### 2-07. 민트 (Mint Fresh)
- base_bg: `#f0fdf4`
- card_bg: `#dcfce7`
- dark_bg: `#14532d`
- heading: `#14532d`
- body: `#4d7c5f`
- muted: `#86a896`
- accent_pool: `[#16a34a, #059669, #10b981]`
- feel: 신선, 건강, 자연

### 2-08. 로즈 (Rose)
- base_bg: `#fff1f2`
- card_bg: `#ffe4e6`
- dark_bg: `#4c0519`
- heading: `#4c0519`
- body: `#9f1239`
- muted: `#e11d48`
- accent_pool: `[#e11d48, #db2777, #f43f5e]`
- feel: 뷰티, 패션, 감성

### 2-09. 슬레이트 블루 (Slate Blue)
- base_bg: `#f8fafc`
- card_bg: `#e2e8f0`
- dark_bg: `#1e293b`
- heading: `#1e293b`
- body: `#64748b`
- muted: `#94a3b8`
- accent_pool: `[#4f46e5, #7c3aed, #6366f1]`
- feel: 기업, 금융, 안정

### 2-10. 앰버 (Amber)
- base_bg: `#fffbeb`
- card_bg: `#fef3c7`
- dark_bg: `#451a03`
- heading: `#451a03`
- body: `#92400e`
- muted: `#b45309`
- accent_pool: `[#d97706, #ea580c, #b45309]`
- feel: 에너지, 긴급, 세일즈

### 2-11. 숲 (Forest)
- base_bg: `#f0f4f1`
- card_bg: `#e8ede9`
- dark_bg: `#1a2e1a`
- heading: `#1a2e1a`
- body: `#4a5d4a`
- muted: `#7d8f7d`
- accent_pool: `[#15803d, #059669, #65a30d]`
- feel: 자연, 지속가능, 치유

### 2-12. 아쿠아 (Aqua)
- base_bg: `#f0f9ff`
- card_bg: `#e0f2fe`
- dark_bg: `#0c4a6e`
- heading: `#0c4a6e`
- body: `#0369a1`
- muted: `#7dd3fc`
- accent_pool: `[#0ea5e9, #06b6d4, #0891b2]`
- feel: 수중, 깊이, 투명

### 2-13. 오크 (Oak)
- base_bg: `#faf6f0`
- card_bg: `#f2ece4`
- dark_bg: `#292118`
- heading: `#292118`
- body: `#6d5d4b`
- muted: `#9c8b78`
- accent_pool: `[#a0522d, #8b4513, #cd853f]`
- feel: 나무, 가구, 수공예

### 2-14. 라벤더 (Lavender)
- base_bg: `#faf5ff`
- card_bg: `#f3e8ff`
- dark_bg: `#3b0764`
- heading: `#3b0764`
- body: `#6b21a8`
- muted: `#a855f7`
- accent_pool: `[#7c3aed, #a855f7, #c084fc]`
- feel: 창의, 커뮤니티, 교육

### 2-15. 콘크리트 (Concrete)
- base_bg: `#fafafa`
- card_bg: `#f2f2f7`
- dark_bg: `#1c1c1e`
- heading: `#1c1c1e`
- body: `#8e8e93`
- muted: `#aeaeb2`
- accent_pool: `[#ff3b30, #007aff, #34c759]`
- feel: 도시, 건축, 모던

### 2-16. 미드나잇 (Midnight)
- base_bg: `#020617`
- card_bg: `rgba(255,255,255,0.03)`
- dark_bg: `#000000`
- heading: `#e2e8f0`
- body: `#64748b`
- muted: `#334155`
- accent_pool: `[#38bdf8, #a78bfa, #f472b6]`
- feel: 프리미엄, 럭셔리, SaaS 다크

### 2-17. 올리브 (Olive)
- base_bg: `#f7f7f2`
- card_bg: `#eeeed9`
- dark_bg: `#2d2d1f`
- heading: `#2d2d1f`
- body: `#6b6b4e`
- muted: `#9c9c7a`
- accent_pool: `[#65a30d, #ca8a04, #a3a30d]`
- feel: 오가닉, 자연, 유기농

### 2-18. 블러쉬 (Blush)
- base_bg: `#fdf2f8`
- card_bg: `#fce7f3`
- dark_bg: `#500724`
- heading: `#500724`
- body: `#9d174d`
- muted: `#f472b6`
- accent_pool: `[#ec4899, #db2777, #be185d]`
- feel: 소프트, 여성, 웰니스

### 2-19. 스틸 (Steel)
- base_bg: `#f4f4f5`
- card_bg: `#e4e4e7`
- dark_bg: `#18181b`
- heading: `#18181b`
- body: `#71717a`
- muted: `#a1a1aa`
- accent_pool: `[#2563eb, #dc2626, #16a34a]`
- feel: 산업, 제조, 견고

### 2-20. 카카오 (Cacao)
- base_bg: `#1a1210`
- card_bg: `#2a2018`
- dark_bg: `#0d0a08`
- heading: `#f5e6d3`
- body: `#a89078`
- muted: `#6b5c4d`
- accent_pool: `[#d97706, #f59e0b, #cd853f]`
- feel: 초콜릿, 따뜻한 다크, 프리미엄

---

## SLOT_3: PAGE STRUCTURE (페이지 구조) — 20개

> HTML `<body>` 골격 결정. DIM_1 핵심.
> 각 값은 고유한 HTML 패턴을 강제.

### 3-01. 섹션스택 (Section Stack)
- html: `<main> 안에 <section>이 수직으로 쌓임`
- css: `각 section 독립. max-width 제한.`
- nav: 상단 고정 바
- hero: 전폭 또는 max-width 단일 블록
- cards: section 안에서 grid/flex

### 3-02. 모자이크캔버스 (Mosaic Canvas)
- html: `<main>이 하나의 CSS Grid. 섹션 경계 없음.`
- css: `grid-template-columns: repeat(12, 1fr); gap: 1~2px`
- nav: 그리드 밖 상단
- hero: 없음. 검색=큰 grid 셀.
- cards: `grid-column: span N` 크기 차등

### 3-03. 대시보드 (Dashboard)
- html: `고정 사이드바(왼쪽) + 메인 콘텐츠(오른쪽)`
- css: `sidebar 240px fixed + main margin-left`
- nav: 사이드바 내 수직 네비
- hero: 없음. 검색바+현황 인라인.
- cards: 메인 영역 내 grid

### 3-04. 매거진에디토리얼 (Magazine Editorial)
- html: `2~3컬럼 비대칭. 이미지+텍스트 좌우 번갈아.`
- css: `grid-template-columns: 2fr 1fr 교차`
- nav: 미니멀 로고+링크 1줄
- hero: 풀너비 이미지 + 오버레이
- cards: 큰 이미지 1개 + 텍스트 블록

### 3-05. 싱글스크롤 (Single Scroll / Snap)
- html: `각 섹션 min-height: 100dvh. 풀스크린.`
- css: `scroll-snap-type: y mandatory`
- nav: 투명 오버레이 / 스크롤 시 나타남
- hero: 첫 풀스크린 섹션
- cards: 풀너비 가로 스크롤 행

### 3-06. 카드덱 (Card Deck / Sticky Stack)
- html: `카드가 position: sticky로 겹침. 스크롤 펼침.`
- css: `각 카드 sticky top: Npx (점진 증가)`
- nav: 투명 플로팅
- hero: 첫 카드(가장 큰)
- cards: 모든 콘텐츠가 카드. 순차 공개.

### 3-07. 타임라인 (Timeline)
- html: `세로축 라인 + 좌우로 콘텐츠 분기`
- css: `::before 세로선. 노드에 원형 마커.`
- nav: 상단 바
- hero: 없음. 첫 노드가 가장 큰 콘텐츠.
- cards: 각 노드=콘텐츠 블록

### 3-08. 스플릿 히어로 (Split Hero)
- html: `히어로가 grid 1fr 1fr 좌우 분할. 이후 스택.`
- css: `hero { display: grid; grid-template-columns: 1fr 1fr }`
- nav: 상단 수평 바
- hero: 화면 양분 (좌=검색/CTA, 우=시각/도서관)
- cards: 히어로 아래 일반 스택

### 3-09. 핀스크롤 (Pin Scroll / Horizontal)
- html: `일부 섹션이 고정되고 내부가 수평 스크롤`
- css: `position: sticky + overflow-x + translateX`
- nav: 상단 고정
- hero: 수직 스택
- cards: 핀 고정 섹션 내 수평 이동

### 3-10. 탭 인터페이스 (Tab Interface)
- html: `상단 탭바 + 탭별 풀 콘텐츠 패널`
- css: `탭 패널 display: none/block 전환`
- nav: 탭바 자체가 네비게이션
- hero: 탭 밖 상단 검색 영역
- cards: 각 탭 패널 내 grid

### 3-11. 오버레이 레이어 (Overlay Layer)
- html: `배경 콘텐츠 위에 모달/패널 레이어`
- css: `position: fixed 레이어 + z-index 관리`
- nav: 배경에 최소 nav. 메인은 레이어 내.
- hero: 배경 풀스크린 이미지/영상
- cards: 오버레이 패널 내 콘텐츠

### 3-12. 밴토 그리드 (Bento Grid)
- html: `CSS Grid로 다양한 크기의 셀 배치`
- css: `grid-template: auto / repeat(4, 1fr); 셀마다 span 차등`
- nav: 상단 바
- hero: 큰 셀 하나 (span 2x2)
- cards: 각 셀이 독립 카드. 크기 다양.

### 3-13. 풀블리드 스택 (Full-Bleed Stack)
- html: `모든 섹션이 100vw 풀너비. 좌우 마진 0.`
- css: `각 section { width: 100vw; padding: 0 }`
- nav: 풀너비 상단 바
- hero: 풀너비 배경 이미지/색상
- cards: section 내부에 max-width 제한된 콘텐츠

### 3-14. 뉴스피드 (News Feed)
- html: `중앙 좁은 칼럼에 카드가 수직으로 쌓임`
- css: `max-width: 680px; margin: 0 auto`
- nav: 상단 고정 + 사이드 위젯 가능
- hero: 첫 카드가 크게
- cards: 단일 칼럼. 카드 사이 간격 균등.

### 3-15. 아코디언 (Accordion Expand)
- html: `각 섹션이 접힌 상태. 클릭/스크롤로 펼침.`
- css: `max-height: 0 → auto 트랜지션`
- nav: 아코디언 제목 자체가 네비
- hero: 첫 아코디언(항상 열림)
- cards: 펼쳐진 아코디언 내부

### 3-16. 사이드 패널 (Side Panel)
- html: `좌측 목차 패널(200px) + 우측 메인 콘텐츠`
- css: `position: sticky 목차 + 메인 스크롤`
- nav: 목차 패널 자체
- hero: 메인 상단
- cards: 메인 영역 내 콘텐츠

### 3-17. 캐러셀 풀스크린 (Carousel Fullscreen)
- html: `각 섹션이 가로로 나열. 좌우 스와이프.`
- css: `display: flex; overflow-x: hidden; transform: translateX`
- nav: 도트 인디케이터 / 화살표
- hero: 첫 슬라이드
- cards: 각 슬라이드가 풀스크린 콘텐츠

### 3-18. 마소닉 폭포 (Masonry Waterfall)
- html: `Pinterest 스타일 다단 폭포 레이아웃`
- css: `columns: 3; column-gap: 16px` 또는 JS masonry
- nav: 상단 필터 바
- hero: 없음. 바로 폭포 시작.
- cards: 높이 불규칙. 자연스러운 폭포.

### 3-19. 센터 스테이지 (Center Stage)
- html: `모든 콘텐츠가 좁은 중앙(max-width: 720px)에 집중`
- css: `max-width: 720px; margin: 0 auto; padding: 0 24px`
- nav: 미니멀 중앙 정렬
- hero: 큰 텍스트 중앙 정렬
- cards: 단일 칼럼 중앙. 좌우 여백 넓음.

### 3-20. 듀얼 패널 (Dual Panel)
- html: `화면이 좌우 두 패널로 영구 분할`
- css: `display: grid; grid-template-columns: 1fr 1fr; height: 100dvh`
- nav: 좌측 패널 상단
- hero: 우측 패널 = 시각/이미지. 좌측 = 텍스트/검색.
- cards: 좌측 패널 내 스크롤

---

## SLOT_4: TYPOGRAPHY CHARACTER (타이포 성격) — 20개

> heading font-family + 크기 위계. DIM_3 핵심.

### 4-01. 기하학적 산세리프 (Geometric Sans)
- font: `Space Grotesk, DM Sans, Outfit`
- display: 32~56px. spacing: -1px~-1.5px.
- feel: 깔끔, 현대, 중립

### 4-02. 클래식 세리프 (Classic Serif)
- font: `Instrument Serif, Playfair Display, Lora`
- display: 36~64px. spacing: -0.5px~0.
- feel: 우아, 전통, 권위

### 4-03. 모노스페이스 (Monospace)
- font: `JetBrains Mono, IBM Plex Mono, Fira Code`
- display: 28~48px. spacing: 0.
- feel: 기술, 정밀, 데이터

### 4-04. 둥근 산세리프 (Rounded Sans)
- font: `Nunito, Quicksand, Varela Round`
- display: 28~44px. spacing: 0~0.5px.
- feel: 친근, 부드러운, 접근성

### 4-05. 압축 볼드 (Compressed Bold)
- font: `Bebas Neue, Anton, Oswald`
- display: 40~72px. spacing: 1px~3px.
- feel: 임팩트, 포스터, 헤드라인

### 4-06. 필기체 (Handwriting)
- font: `Caveat, Dancing Script, Kalam`
- display: 24~40px. spacing: 0.
- feel: 수제, 개인, 따뜻한. 1~2곳만.

### 4-07. 네오 그로테스크 (Neo Grotesque)
- font: `Inter, Helvetica Neue, Suisse Int'l`
- display: 32~52px. spacing: -0.5px.
- feel: 프로, 기업, 시스템

### 4-08. 슬랩 세리프 (Slab Serif)
- font: `Roboto Slab, Zilla Slab, Arvo`
- display: 32~56px. spacing: 0.
- feel: 단단한, 신문, 권위+현대

### 4-09. 디스플레이 (Display/Decorative)
- font: `Unbounded, Bungee, Rubik Mono One`
- display: 36~64px. spacing: -1px.
- feel: 대담, 실험, 인상적

### 4-10. 휴머니스트 산세리프 (Humanist Sans)
- font: `Source Sans 3, Fira Sans, Noto Sans`
- display: 30~48px. spacing: 0.
- feel: 가독성, 공공, 중립+따뜻

### 4-11. 올드스타일 세리프 (Oldstyle Serif)
- font: `Libre Baskerville, EB Garamond, Cormorant`
- display: 34~56px. spacing: 0.
- feel: 고전, 문학, 품격

### 4-12. 스퀘어 산세리프 (Square Sans)
- font: `Barlow, Exo 2, Rajdhani`
- display: 32~52px. spacing: 0.5px~1px.
- feel: 기술, 게임, 미래

### 4-13. 인라인 미니멀 (Inline Minimal)
- font: `Manrope, General Sans, Satoshi`
- display: 30~48px. spacing: -0.5px.
- feel: 스타트업, 프로덕트, 깔끔

### 4-14. 한글 강조 (Korean Display)
- font: `Pretendard weight 800~900 단독 사용`
- display: 32~56px. spacing: -1px.
- feel: 한글 네이티브, 강한, 직접적

### 4-15. 세리프+산세리프 믹스 (Serif-Sans Mix)
- font: `제목=Instrument Serif, 소제목=Inter`
- display: 36~56px. 두 서체 교차.
- feel: 대비, 긴장, 에디토리얼

### 4-16. 와이드 (Wide/Extended)
- font: `Archivo Black, Jost, Work Sans`
- display: 32~52px. spacing: 2px~4px. uppercase.
- feel: 넓은, 안정, 건축

### 4-17. 라이트 웨이트 (Light Weight)
- font: `Poppins Light, Inter 300, Outfit 300`
- display: 40~64px. spacing: 0~1px.
- feel: 가벼운, 호흡, 럭셔리

### 4-18. 브루탈리스트 (Brutalist)
- font: `Courier New, Times New Roman (system)`
- display: 28~48px. spacing: 0.
- feel: 반디자인, 실험, 로우파이

### 4-19. 캘리그래피 (Calligraphy)
- font: `Nanum Myeongjo, 나눔명조`
- display: 32~52px. spacing: 0.
- feel: 전통, 한국적, 격식

### 4-20. 듀얼 웨이트 (Dual Weight)
- font: `같은 서체의 900+300 극단적 weight 조합`
- display: 제목=900, 부제=300. 같은 font-family.
- feel: 극적 대비, 모던, 세련

---

## SLOT_5: ACCENT STRATEGY (악센트 전략) — 20개

> accent 색상의 CSS 적용 위치 결정. DIM_4 핵심.

### 5-01. 단일폭발 (Single Burst)
- rule: accent 페이지 전체에서 **1개 요소에만**
- apply: CTA 1개 OR 히어로 1곳 OR 숫자 1개
- rest: 무채색

### 5-02. 텍스트전용 (Text Only)
- rule: accent는 `color` 속성에만
- apply: 링크, 활성 탭 텍스트, 강조 단어
- rest: background/border 무채색

### 5-03. 보더전용 (Border Only)
- rule: accent는 `border/outline`에만
- apply: hover border, 활성 탭 하단선, 인용 왼쪽 바
- rest: text/background 무채색

### 5-04. 배경반전 (Background Invert)
- rule: **1개 섹션**의 background가 accent
- apply: 해당 섹션 내 텍스트=흰색/밝은색
- rest: 다른 섹션에서 accent 금지

### 5-05. hover서프라이즈 (Hover Surprise)
- rule: 기본 상태 accent 안 보임. hover/focus 시만
- apply: `button:hover, a:hover, card:hover`
- rest: 기본 완전 무채색

### 5-06. 듀얼교차 (Dual Alternating)
- rule: accent 2색이 섹션 단위로 교차
- apply: 짝수=color A, 홀수=color B
- rest: 한 섹션 안 2색 동시 금지

### 5-07. 그라디언트 (Gradient Accent)
- rule: accent가 `linear-gradient`로만 사용
- apply: CTA 버튼 gradient, 히어로 gradient
- rest: 단색 accent 사용 금지

### 5-08. 타이포컬러 (Typo Color)
- rule: accent가 **제목 텍스트 1단어에만**
- apply: 제목 중 핵심 단어 1개만 accent color
- rest: 나머지 전부 무채색

### 5-09. 아이콘전용 (Icon Only)
- rule: accent는 아이콘/이모지/SVG에만
- apply: 아이콘 fill/stroke, 불릿 마커
- rest: text/border/background 무채색

### 5-10. 프로그레스 (Progress Accent)
- rule: accent는 진행/상태 표시에만
- apply: progress bar, 도넛차트, 뱃지
- rest: UI 크롬 무채색

### 5-11. 밑줄 (Underline Only)
- rule: accent는 `text-decoration` 또는 `::after` 밑줄에만
- apply: 링크 밑줄, 제목 하단 라인
- rest: 텍스트/배경 무채색

### 5-12. 쉐도우 (Shadow Accent)
- rule: accent는 `box-shadow`에만
- apply: `box-shadow: 0 4px 14px rgba(accent, 0.2)`
- rest: 텍스트/border 무채색

### 5-13. 배경 도트 (Background Dot)
- rule: accent는 배경 패턴(점, 선)에만
- apply: `radial-gradient` dot 패턴 accent 색
- rest: 전면 요소 무채색

### 5-14. 첫째+마지막 (First & Last)
- rule: accent가 **첫 섹션과 마지막 섹션에만**
- apply: 히어로 CTA + 최종 CTA만 accent
- rest: 중간 섹션 전부 무채색

### 5-15. 데이터 악센트 (Data Accent)
- rule: accent는 숫자/데이터 표시에만
- apply: 큰 숫자, 통계, 퍼센트
- rest: UI/텍스트 무채색

### 5-16. 이미지 마스크 (Image Mask)
- rule: accent가 이미지 위 오버레이에만
- apply: 이미지에 accent 색 `mix-blend-mode`
- rest: 순수 요소 무채색

### 5-17. 포커스 링 (Focus Ring)
- rule: accent는 `:focus-visible` 상태에만
- apply: `outline: 2px solid accent`
- rest: 시각적으로 accent 없음 (접근성용)

### 5-18. 탭/필터 전용 (Tab/Filter Only)
- rule: accent는 활성 탭/필터 인디케이터에만
- apply: 활성 탭 하단선 + 활성 필터 배경
- rest: 나머지 무채색

### 5-19. 스크롤 트리거 (Scroll Trigger)
- rule: accent가 스크롤 진행에 따라 점진 등장
- apply: scroll progress bar + 현재 섹션 indicator
- rest: 초기 상태 무채색

### 5-20. 모노크롬+1 (Monochrome Plus One)
- rule: 전체 모노크롬(단일 색상의 명도 변주) + accent 1색
- apply: accent는 아무 속성이나 가능하지만 **면적 5% 이하**
- rest: 모노크롬 (같은 hue의 밝기 변주)
