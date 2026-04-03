# MOTION RULES v1.0 — 모션/인터랙션 규칙 모듈

> CREATIVE_GENERATION_FRAMEWORK 품질 모듈.
> 정적인 페이지를 살아있는 인터페이스로 변환.
> 참조: ilrobotics.co.kr (GSAP ScrollTrigger), Awwwards SOTD 2025-2026

---

## 원칙

```
1. 모든 섹션에 최소 1개의 등장 애니메이션 필수
2. hover 효과는 섹션마다 다르게 (균일 hover 금지)
3. CSS만으로 구현 (외부 라이브러리 불필요)
4. prefers-reduced-motion 존중
5. GPU 가속: transform/opacity만 애니메이션 (layout 트리거 금지)
```

---

## 필수 모션 3종

### 1. 스크롤 등장 (Intersection Observer)

> 모든 섹션/카드에 적용. 페이지 로드 시 보이지 않다가 스크롤하면 등장.

```css
/* 등장 전 상태 */
.reveal {
  opacity: 0;
  transform: translateY(32px);
  transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

/* 등장 후 상태 */
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* 시차 등장 (카드 그룹) */
.reveal:nth-child(1) { transition-delay: 0ms; }
.reveal:nth-child(2) { transition-delay: 80ms; }
.reveal:nth-child(3) { transition-delay: 160ms; }
.reveal:nth-child(4) { transition-delay: 240ms; }
.reveal:nth-child(5) { transition-delay: 320ms; }
```

```javascript
/* 필수 JS — 모든 생성물에 포함 */
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

### 2. Hover Transform (섹션별 차등)

> 같은 hover 효과가 전체 페이지에 반복되면 AI 티 남.

```css
/* ── 코스/동영상 카드: scale + shadow ── */
.course-card {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1),
              box-shadow 0.3s ease;
}
.course-card:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 12px 32px rgba(0,0,0,0.08);
}

/* ── 이어서학습 카드: 좌측 border 등장 ── */
.continue-card {
  border-left: 3px solid transparent;
  transition: border-color 0.2s, transform 0.2s;
}
.continue-card:hover {
  border-left-color: var(--accent);
  transform: translateX(4px);
}

/* ── 책 표지: tilt 효과 ── */
.book-cover {
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.book-cover:hover {
  transform: perspective(600px) rotateY(-5deg) scale(1.03);
}

/* ── 채널 카드: 배경색 전환 ── */
.channel-card {
  transition: background-color 0.25s ease;
}
.channel-card:hover {
  background-color: rgba(0,0,0,0.04);
}

/* ── 연락처 카드: 숫자 색상 변화 ── */
.contact-card strong {
  transition: color 0.2s;
}
.contact-card:hover strong {
  color: var(--accent);
}

/* ── 버튼: 미세 확대 + 그림자 ── */
.btn-primary {
  transition: transform 0.2s, box-shadow 0.2s;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
```

### 3. 마이크로 인터랙션

```css
/* ── 프로그레스 바: 로딩 애니메이션 ── */
.progress-fill {
  animation: progressLoad 1.2s ease-out forwards;
  transform-origin: left;
}
@keyframes progressLoad {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}

/* ── 탭 전환: 밑줄 슬라이드 ── */
.tab-indicator {
  transition: left 0.3s cubic-bezier(0.16, 1, 0.3, 1),
              width 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

/* ── 검색 입력: 포커스 확장 ── */
.search-input {
  transition: box-shadow 0.2s, border-color 0.2s;
}
.search-input:focus {
  box-shadow: 0 0 0 3px rgba(var(--accent-rgb), 0.1);
  border-color: var(--accent);
}

/* ── 스크롤 인디케이터 (히어로 하단) ── */
.scroll-hint {
  animation: scrollBounce 2s ease-in-out infinite;
}
@keyframes scrollBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(8px); }
}
```

---

## 접근성

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
  .reveal { opacity: 1; transform: none; }
}
```

---

## 구현 체크리스트

```yaml
motion_check:
  - [ ] IntersectionObserver JS가 포함되어 있는가?
  - [ ] 모든 섹션/카드에 .reveal 클래스가 적용되었는가?
  - [ ] 카드 그룹에 시차 등장 (nth-child delay)이 있는가?
  - [ ] 최소 3종 이상의 서로 다른 hover 효과가 있는가?
  - [ ] 프로그레스 바에 로딩 애니메이션이 있는가?
  - [ ] 검색 입력에 focus 효과가 있는가?
  - [ ] prefers-reduced-motion이 존중되는가?
  - [ ] transform/opacity만 사용하고 layout 속성(width, height, top)은 애니메이션하지 않는가?
```
