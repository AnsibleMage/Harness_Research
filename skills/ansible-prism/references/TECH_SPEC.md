# 적용 기술스택 정의서 — ansible-prism

> An & Ari's Creative Generation Engine의 출력 기술 명세.
> CREATIVE_GENERATION_FRAMEWORK.md가 "무엇을 만들지" 결정하면, 이 문서가 "어떻게 구현할지" 결정한다.

---

## 1. 기술스택 구성

### 1.1 스택 요약

| 계층 | 기술 | 버전 | 역할 | 의존성 |
|------|------|------|------|--------|
| **마크업** | HTML5 (시맨틱) | HTML Living Standard | 페이지 구조. `<header>`, `<main>`, `<section>`, `<footer>` | 없음 |
| **스타일** | Embedded CSS | CSS3 | 단일 `<style>` 태그. CSS Custom Properties 필수 | 없음 |
| **타이포** | Google Fonts CDN | — | Display + Body 폰트 페어링 | CDN (필수) |
| **한글 폰트** | Pretendard CDN | — | 한글 본문 기본 폰트 | CDN (필수) |
| **인터랙션** | Vanilla JavaScript | ES6+ | 탭 전환, IntersectionObserver, 이벤트 핸들러 | 없음 (inline) |
| **이미지** | CSS Gradient + Inline SVG | — | 썸네일, 배경, 아이콘 (IMAGE_ENGINE.md 참조) | 없음 |
| **아이콘** | Inline SVG 또는 CSS 도형 | SVG 1.1 | 카테고리 아이콘, 재생 버튼, UI 요소 | 없음 (임베드) |
| **프레임워크** | 없음 | — | React/Vue/Tailwind 사용 안 함 | — |

### 1.2 단일 파일 원칙

```
출력: 단일 HTML 파일 (*.html)
  - CSS:  <style> 태그 내 임베드 (외부 CSS 파일 없음)
  - JS:   <script> 태그 내 임베드 (외부 JS 파일 없음)
  - 폰트: <link> 태그로 Google Fonts + Pretendard CDN 로드
  - 이미지: CSS gradient + inline SVG (외부 이미지 파일 없음)

→ 파일 1개를 브라우저에서 열면 완전 작동하는 자립형 페이지
```

### 1.3 금지 항목

```
✕ Tailwind CSS CDN         — 순수 CSS만 사용
✕ React / Vue / Svelte     — 프레임워크 없음
✕ jQuery                   — Vanilla JS만
✕ 외부 이미지 URL           — CSS gradient + inline SVG로 대체
✕ npm / 빌드 도구           — 번들러, 트랜스파일러 없음
✕ 외부 아이콘 CDN           — FontAwesome, Heroicons CDN 금지
```

---

## 2. HTML 구조

### 2.1 필수 메타 태그

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{페이지 설명 — 80자 이내}">
  <title>{브랜드명} — {페이지 제목}</title>

  <!-- 폰트 로드 (SLOT_4에 따라 결정) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family={SLOT_4_font}:wght@{weights}&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.min.css">

  <style>
    /* CSS METADATA (필수) */
    /*
    FRAMEWORK: v4.0
    ENGINE: ansible-prism
    MODE: {CREATE | REDESIGN}
    OL: {score}
    WORLD: "{세계관 1문장}"
    SLOTS: identity={1-XX} | color={2-XX} | structure={3-XX} | typo={4-XX} | accent={5-XX}
    */

    /* ... CSS 본문 ... */
  </style>
</head>
<body>
  <!-- 콘텐츠 -->
  <script>
    /* ... JS (IntersectionObserver, 탭 전환 등) ... */
  </script>
</body>
</html>
```

### 2.2 시맨틱 HTML 규칙

| 요소 | HTML 태그 | 용도 |
|------|----------|------|
| 헤더/네비 | `<header>`, `<nav>` | 로고 + GNB + 사용자 영역 |
| 히어로 | `<section>` 또는 첫 `<div>` | 메인 배너 |
| 콘텐츠 섹션 | `<section>` | 각 본문 섹션 (서비스, 후기, 연락처 등) |
| 메인 영역 | `<main>` | 헤더/푸터 제외한 본문 전체 |
| 푸터 | `<footer>` | 회사 정보 + 링크 + 저작권 |
| 카드 목록 | `<div>` + role 속성 | 카드 그리드/가로 스크롤 |
| 링크 | `<a href="#">` | 네비게이션, CTA, 전체보기 |
| 버튼 | `<button>` | 탭 전환, 폼 제출 등 인터랙션 |

### 2.3 접근성 (WCAG 2.1 AA)

```
필수:
  - 모든 인터랙티브 요소에 focus 스타일 (outline 또는 box-shadow)
  - 색상 대비 4.5:1 이상 (본문 텍스트)
  - 대비 3:1 이상 (큰 텍스트 18px+)
  - alt 텍스트: 장식 SVG → aria-hidden="true", 의미 SVG → aria-label
  - 탭 네비게이션: 논리적 순서
  - prefers-reduced-motion 존중 (MOTION_RULES.md 참조)

권장:
  - aria-label on nav, main, footer
  - skip-to-content 링크 (시각적 숨김, focus시 표시)
  - lang="ko" 속성
```

---

## 3. CSS 아키텍처

### 3.1 CSS 작성 순서 (단일 style 태그 내)

```css
/* 1. CSS METADATA (맨 위) */
/* 2. CSS Custom Properties (:root) */
/* 3. Reset & Base */
/* 4. Typography */
/* 5. Layout (Header/Nav) */
/* 6. Hero/Banner */
/* 7. Sections (본문 각 섹션) */
/* 8. Components (카드, 버튼, 뱃지, 진행바) */
/* 9. Footer */
/* 10. Animations & Transitions */
/* 11. Responsive (@media) */
/* 12. prefers-reduced-motion */
```

### 3.2 CSS Custom Properties (필수)

```css
:root {
  /* SLOT_1 메타포 토큰 (5개) */
  --token-1: {값};
  --token-2: {값};
  --token-3: {값};
  --token-4: {값};
  --token-5: {값};

  /* SLOT_2 색상 토큰 (6~8개) */
  --base-bg: {값};
  --card-bg: {값};
  --dark-bg: {값};
  --heading-color: {값};
  --body-color: {값};
  --muted-color: {값};
  --accent: {값};

  /* SLOT_4 폰트 토큰 */
  --font-display: '{SLOT_4 font}', sans-serif;
  --font-body: 'Pretendard', -apple-system, sans-serif;

  /* Spacing (CSS_PRECISION.md 4px 그리드) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;

  /* Border (CSS_PRECISION.md 3등급) */
  --border-subtle: 1px solid rgba(0,0,0,0.04);
  --border-default: 1px solid rgba(0,0,0,0.08);
  --border-strong: 1px solid rgba(0,0,0,0.15);
}
```

### 3.3 Reset (필수 포함)

```css
*, *::before, *::after {
  margin: 0; padding: 0; box-sizing: border-box;
}

html { scroll-behavior: smooth; }

body {
  font-family: var(--font-body);
  background: var(--base-bg);
  color: var(--body-color);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  word-break: keep-all;
}

a { text-decoration: none; color: inherit; }
img { max-width: 100%; display: block; }
button { font-family: inherit; cursor: pointer; border: none; background: none; }
```

---

## 4. 반응형 전략

### 4.1 Breakpoints (3단계)

```css
/* Desktop-first 접근 */
/* 기본: Desktop (1200px+) */

@media (max-width: 1024px) {
  /* 태블릿 */
}

@media (max-width: 768px) {
  /* 모바일 */
  /* 네비: 햄버거 메뉴 또는 간소화 */
  /* 그리드: 1~2컬럼으로 축소 */
  /* 가로 스크롤: 카드 너비 축소 */
  /* 사이드바 구조: 상단 바로 전환 */
}

@media (max-width: 480px) {
  /* 소형 모바일 */
  /* 폰트 크기 축소 */
  /* 패딩 축소 */
}
```

### 4.2 컨테이너

```css
.section-inner, .container {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--space-10); /* 40px */
}

@media (max-width: 768px) {
  .section-inner, .container {
    padding: 0 var(--space-5); /* 20px */
  }
}
```

---

## 5. JavaScript 규칙

### 5.1 허용 범위

| 기능 | 허용 | 구현 방식 |
|------|------|----------|
| 탭 전환 | ✅ | `classList.add/remove` |
| IntersectionObserver | ✅ | 스크롤 등장 애니메이션 (MOTION_RULES.md) |
| 이벤트 핸들러 | ✅ | `addEventListener` |
| 스크롤 감지 | ✅ | nav 배경 변화, 스크롤 인디케이터 |
| DOM 조작 | ✅ | 최소한으로 |
| 외부 라이브러리 | ❌ | GSAP, Lenis, Swiper 등 금지 |
| 프레임워크 | ❌ | React, Vue, Alpine 금지 |
| fetch/API 호출 | ❌ | 정적 페이지만 |

### 5.2 JS 패턴 (ES6+)

```javascript
// 탭 전환 (필수 패턴)
function switchTab(id, btn) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('panel-' + id).classList.add('active');
  btn.classList.add('active');
}

// IntersectionObserver (MOTION_RULES.md 필수)
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

// 스크롤 시 nav 배경 변화 (선택적)
window.addEventListener('scroll', () => {
  const nav = document.querySelector('.nav');
  if (nav) nav.classList.toggle('scrolled', window.scrollY > 50);
});
```

---

## 6. 폰트 로딩

### 6.1 필수 폰트

| 폰트 | 용도 | 로드 방식 |
|------|------|----------|
| **Pretendard** | 한글 본문 (모든 페이지) | CDN `<link>` |
| **SLOT_4 폰트** | Display/Heading (SLOT에 따라 변경) | Google Fonts `<link>` |

### 6.2 로드 최적화

```html
<!-- preconnect 필수 (성능) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- display=swap 필수 (FOUT 방지) -->
<link href="https://fonts.googleapis.com/css2?family={font}:wght@{weights}&display=swap" rel="stylesheet">
```

### 6.3 Fallback 스택

```css
--font-display: '{SLOT_4 font}', sans-serif;
--font-body: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

---

## 7. 이미지 전략 (IMAGE_ENGINE.md 연동)

### 7.1 구현 우선순위

```
1순위: CSS Gradient Art (제로 의존성, 항상 작동)
2순위: Inline SVG 아이콘 (가벼움, 항상 작동)
3순위: AI 생성 이미지 (최고 품질, API 키 필요)
```

### 7.2 CSS Gradient 썸네일 규격

| 요소 | 비율 | 최소 높이 |
|------|------|----------|
| 코스/동영상 썸네일 | 16:9 | 160px |
| 책 표지 | 3:4 | 186px |
| 채널 아바타 | 1:1 | 32px |
| 히어로 배경 | 전폭 | 300px |

### 7.3 Inline SVG 규격

```
크기: 24px (인라인), 48~64px (썸네일 오버레이)
색상: currentColor (CSS로 제어)
스트로크: 2px
viewBox: "0 0 24 24" 또는 "0 0 48 48"
```

---

## 8. 파일 네이밍 규칙

### 8.1 출력 파일

```
{NN}_{slug}.html

예시:
  01_creative_saas.html
  02_creative_saas.html
  04_interior_landing.html
  05_cafe_homepage.html
```

| 구성 | 설명 |
|------|------|
| `NN` | 순번 (01부터 자동 증가) |
| `slug` | 프로젝트/도메인 키워드 (snake_case) |
| `.html` | 항상 HTML |

### 8.2 CSS 메타데이터 (파일 내 주석)

```css
/*
FRAMEWORK: v4.0
ENGINE: ansible-prism
MODE: CREATE | REDESIGN
OL: 10
WORLD: "{세계관 1문장}"
GI: O{n}C{n}P{n}S{n} / A{n}B{n}
CC: f({A→B 경로})
SLOTS: identity={1-XX} | color={2-XX} | structure={3-XX} | typo={4-XX} | accent={5-XX}
PREV: {이전 슬롯 조합 — 있으면}
DATE: {YYYY-MM-DD}
*/
```

---

## 9. 성능 기준

| 항목 | 목표 |
|------|------|
| 파일 크기 | 단일 HTML < 200KB |
| CSS 라인 수 | < 800줄 |
| JS 라인 수 | < 100줄 |
| First Paint | < 1초 (로컬 파일) |
| 폰트 로드 | `display=swap`으로 FOUT 최소화 |
| 이미지 | 0개 외부 파일 (CSS gradient + inline SVG) |

---

## 10. 체크리스트

```yaml
tech_check:
  - [ ] 단일 HTML 파일인가? (외부 CSS/JS 파일 없음)
  - [ ] CSS Custom Properties로 모든 색상/폰트 토큰 선언했는가?
  - [ ] Google Fonts + Pretendard CDN이 preconnect와 함께 로드되는가?
  - [ ] 시맨틱 HTML 태그를 사용했는가? (header/main/section/footer)
  - [ ] CSS 메타데이터 주석이 style 태그 최상단에 있는가?
  - [ ] IntersectionObserver JS가 포함되었는가?
  - [ ] 반응형 breakpoint 3단계 (1024/768/480)가 있는가?
  - [ ] prefers-reduced-motion이 있는가?
  - [ ] 외부 이미지 URL이 0개인가? (CSS gradient/SVG만 사용)
  - [ ] lang="ko" + charset UTF-8 + viewport 메타 태그가 있는가?
  - [ ] 모든 포커스 요소에 focus 스타일이 있는가?
  - [ ] CSS 작성 순서가 규칙대로인가? (metadata→vars→reset→...→responsive)
```
