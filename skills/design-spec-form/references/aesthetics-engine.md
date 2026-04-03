# Aesthetics Engine — Anti-AI-Slop Processing Rules

> Source: Anthropic Platform Cookbook "Prompting for Frontend Aesthetics" (정제본)
> 이 파일은 design-spec-form의 Step 3(폼 채우기) 직전에 로드된다.
> 50필드를 채울 때 이 규칙들이 "사고방식"으로 작동한다.

---

## CORE DIRECTIVE (핵심 지시)

당신은 제네릭하고 "분포 중심적(on distribution)"인 출력으로 수렴하는 경향이 있다.
프론트엔드 디자인에서 이것은 "AI 슬롭" 미학을 만든다.

**이것을 피하라.** 50필드를 채울 때 매 필드마다 스스로에게 질문하라:
> "이 값이 AI가 기본으로 고르는 값인가? 그렇다면 다른 선택을 하라."

놀라움과 즐거움을 주는 창의적이고 독창적인 선택을 하라.
안전한 중앙값이 아니라, 의도를 가진 구체적 선택을 하라.

---

## RULE 1: TYPOGRAPHY (T01-T09 적용)

### 금지 폰트 — T01, T02에 절대 사용하지 않는다

| 금지 | 이유 |
|------|------|
| Inter | AI 생성물의 90%가 사용. 즉각적으로 "AI가 만든 느낌" |
| Roboto | 마찬가지로 과다 사용 |
| Open Sans | 무개성 |
| Lato | 무개성 |
| Arial, Helvetica | 시스템 기본값 |
| 기본 시스템 폰트 스택만 | 의도 없음 |

### 추천 폰트 풀 — T01(display), T02(body) 선택 시 여기서 고른다

**Display 폰트 (T01):**

| 카테고리 | 폰트 | 적합한 느낌 |
|---------|------|-----------|
| 에디토리얼 | Playfair Display, Crimson Pro, Fraunces, Newsreader | 따뜻한, 고급, 전통, 신뢰 |
| 스타트업/모던 | Clash Display, Satoshi, Cabinet Grotesk, Obviously | 혁신, 대담, 테크 |
| 코드/테크니컬 | Space Grotesk, JetBrains Mono, Fira Code | 기술적, 정밀, 개발자 |
| 클래식 | IBM Plex Serif, Source Serif 4, Libre Baskerville | 공공, 학술, 기관 |
| 감성/소프트 | Nunito, Quicksand, Comfortaa | 부드러운, 친근, 웰빙 |
| 임팩트 | Anton, Oswald, Bebas Neue, Outfit | 강렬, 이벤트, 런칭 |
| 독창적 | Bricolage Grotesque, Syne, Instrument Serif | 유니크, 아트, 에이전시 |

**한국어 본문 폰트 (T02) — 한국어 사이트 필수:**

| 폰트 | 특성 | 적합한 프로젝트 |
|------|------|--------------|
| Pretendard | 깔끔, 현대적, 가독성 최고 | 범용 (가장 안전하지만 AI 기본값 주의) |
| SUIT | Pretendard 대안, 약간 더 특색 | 스타트업, 테크 |
| Wanted Sans | 모던, 기하학적 | 채용, SaaS |
| Noto Sans KR | Google 기본 한국어 | 범용 (단독 사용 시 무개성 주의) |
| Noto Serif KR | 세리프 한국어 | 에디토리얼, 공공, 전통 |
| KoPub 바탕 | 출판 세리프 | 문학, 출판, 교육 |
| 나눔스퀘어라운드 | 둥근 산세리프 | 친근, 교육, 어린이 |
| Gmarket Sans | 특색 있는 산세리프 | 커머스, 이벤트 |

**⚠️ Pretendard 주의:** 한국어 사이트에서 Pretendard는 Inter처럼 "AI 기본값"이 될 수 있다.
Pretendard를 쓸 경우, T01(display)은 반드시 강한 개성의 폰트(세리프, 클래시 등)로 대비를 만들어라.

### 웨이트 규칙 (T04)

```
❌ AI 기본값: font-bold (700)
✅ 세련된 선택: font-medium (500) 또는 font-semibold (600)
✅ 임팩트 선택: font-black (900) — 단, bold/임팩트 방향일 때만

규칙: font-bold(700)는 "중간"이라 개성이 없다.
      위(900)든 아래(500)든 극단으로 가라.
```

### 사이즈 점프 규칙 (T03, T07)

```
❌ AI 기본값: H1=text-3xl, body=text-base (2배 차이)
✅ 드라마틱: H1=text-6xl~7xl, body=text-base (4~5배 차이)

규칙: 제목과 본문의 사이즈 차이가 3배 이상이면 시각적 계층이 극적으로 형성된다.
      1.5~2배 차이는 "안전하지만 지루하다".
```

### 자간 극단 규칙 (T05, T09)

```
❌ AI 기본값: tracking-normal (0)
✅ 제목: tracking-[-0.04em] ~ tracking-[-0.02em] (타이트)
✅ 라벨/캡션: tracking-[0.1em] ~ tracking-[0.2em] (와이드 + uppercase)

규칙: 자간은 "보통"이 가장 재미없다. tight 또는 wide, 둘 중 하나.
      제목=tight, 라벨=wide가 가장 일반적이고 효과적인 조합.
```

---

## RULE 2: COLOR (C01-C09 적용)

### 회피 패턴 — 이 조합은 자동 거부한다

| 패턴 | 왜 거부하는가 |
|------|------------|
| 흰 배경 + 보라 그래디언트 | AI 생성물의 #1 클리셰 |
| 흰 배경 + 파란 CTA | 너무 범용적 |
| 회색 텍스트 + 회색 보더 + 회색 배경 | 무채색 지옥, 성격 없음 |
| 네온 색상 남발 (3개 이상) | 혼란, 통일성 없음 |
| 검정 배경 + 흰 텍스트 + 파란 링크 | 2010년대 기본값 |

### 지배적 컬러 원칙

```
❌ AI 기본값: 5색 균등 배분 팔레트
✅ 올바른 접근: 1개 지배색 + 1개 날카로운 액센트

C01(배경)이 지배적이어야 한다. C04(액센트)는 화면의 5-15%만 차지.
"소심하고 균등 분배된 팔레트보다 지배적인 컬러와 날카로운 악센트가 더 나은 성과를 낸다."
```

### 영감 소스

폼의 Color 카테고리를 채울 때, 다음에서 영감을 끌어오라:
- **IDE 테마**: Dracula, Nord, Solarized, One Dark, Tokyo Night, Catppuccin
- **문화적 미학**: 와비사비(일본), 스칸디나비아, 지중해, 한국 전통
- **자연**: 새벽, 숲, 바다, 사막, 화산
- **시대**: 아르데코, 바우하우스, 70년대, Y2K

하나의 소스에 커밋하라. 여러 소스를 섞으면 통일성이 깨진다.

---

## RULE 3: LAYOUT (L01-L05 적용)

### 회피 패턴

| 패턴 | 왜 회피하는가 |
|------|------------|
| 3열 동일 카드 반복 | AI 생성물의 #2 클리셰. "서비스 소개" 섹션의 99% |
| 완전 대칭 좌우 분할 | 안전하지만 개성 없음 |
| 모든 섹션이 같은 여백 | 리듬감 없음 |
| 모든 텍스트 중앙 정렬 | 게으른 레이아웃 |

### 비대칭 강제 규칙

50필드 중 L01-L05에서 **최소 1개**는 비대칭이어야 한다.
방법: asymmetric-bleed(L01), asymmetric grid(L02), left/right weight(L04), directional bleed(L05)

```
비대칭 = "사람이 의도적으로 배치한 느낌"
대칭 = "알고리즘이 균등 분배한 느낌"
```

---

## RULE 4: MOTION (M01-M04 적용)

### 올바른 모션 전략

```
❌ AI 기본값: 모든 요소에 fade-in 0.3s
✅ 올바른 접근: 고영향 순간에 집중

"잘 오케스트레이션된 페이지 로드 하나가,
 흩어진 마이크로 인터랙션보다 더 큰 즐거움을 만든다."
```

### 구체적 지침

- **페이지 로드**: stagger reveal (animation-delay로 요소 순차 등장)이 가장 효과적
- **Hover**: 색상 변경보다 opacity, scale, translate가 더 세련됨
- **Scroll**: fade-up이 가장 안전. slide-left, scale-in은 콘텐츠에 따라
- **Timing**: `cubic-bezier(0.16, 1, 0.3, 1)`은 "빠르게 시작, 부드럽게 착지"의 만능 easing
- **HTML에서**: CSS 전용 솔루션 우선. `@keyframes` + `animation` + `IntersectionObserver`

---

## RULE 5: BACKGROUND & DECORATION (D01-D03 적용)

### 깊이 만들기

```
❌ AI 기본값: 단색 배경 (#ffffff 또는 #000000)
✅ 올바른 접근: 분위기와 깊이를 레이어

방법:
1. CSS 그래디언트 레이어링 (radial + linear 중첩)
2. 기하학적 패턴 (SVG 반복)
3. Noise 텍스처 (opacity 0.01~0.02로 극미세)
4. 장식 텍스트 (font-size: 10vw+, opacity: 0.03~0.06)
```

### 섹션 구분

섹션 간 구분에 "색상 교차"만 쓰면 AI 기본값이다.
더 세련된 방법: border-line, gradient-fade, whitespace 조합.

---

## SUMMARY: 폼 채우기 체크리스트

50필드를 모두 채운 후, 최종 검증으로 이 체크리스트를 통과하라:

- [ ] **T01/T02에 금지 폰트가 없는가?** (Inter, Roboto, Arial, Open Sans, Lato)
- [ ] **T04가 font-bold(700)가 아닌가?** (medium/semibold/black 중 하나)
- [ ] **T03과 T07의 사이즈 차이가 3배 이상인가?**
- [ ] **C01-C09에 "흰+보라" 클리셰가 없는가?**
- [ ] **C04(액센트)가 화면의 5-15%만 차지하도록 설계되었는가?**
- [ ] **L01-L05 중 최소 1개가 비대칭인가?**
- [ ] **B01이 flat 단색이 아닌가?** (gradient, glass, outline 중 하나 우선)
- [ ] **M01이 단순 color-change가 아닌가?** (opacity, scale, translate 우선)
- [ ] **D01이 none이 아닌가?** (최소한의 배경 깊이)
- [ ] **전체 50개 값이 하나의 통일된 성격을 가지는가?**
