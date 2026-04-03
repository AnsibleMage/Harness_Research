# CSS PRECISION v1.0 — CSS 정밀도 규칙 모듈

> CREATIVE_GENERATION_FRAMEWORK 품질 모듈.
> "대충 40px" 대신 "정확히 8px 그리드"로.
> 참조: Tailwind Design System, Radix UI, Apple HIG

---

## 원칙

```
1. 모든 spacing은 4px 단위 (4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96)
2. 색상은 최소 5단계 명도 구분
3. font-weight는 최소 4단계 활용
4. box-shadow는 다층 구조
5. line-height는 요소별 차등
```

---

## 1. Spacing System (4px 그리드)

```css
/* ── 허용된 spacing 값만 사용 ── */
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
}
```

**적용 규칙:**

| 요소 | spacing | 값 |
|------|---------|-----|
| 카드 내부 padding | 중~대 | 20~32px |
| 카드 간 gap | 소~중 | 12~24px |
| 섹션 padding-top | 대 | 64~96px |
| 섹션 padding-bottom | 대 | 48~80px |
| 제목↔본문 간격 | 소 | 8~16px |
| 본문↔메타 간격 | 극소 | 4~8px |
| nav 내부 padding | 소~중 | 12~20px |
| 버튼 padding | 중 | 12px 24px ~ 16px 32px |

**금지:**
- `margin: 50px` (4px 그리드 아님 → `48px` 사용)
- `padding: 15px` (→ `16px` 사용)
- `gap: 18px` (→ `16px` 또는 `20px` 사용)

---

## 2. Color Depth (5단계 명도)

```css
/* ── 라이트 테마 예시 ── */
:root {
  /* 5단계 배경 */
  --bg-1: #ffffff;        /* 최상위 표면 */
  --bg-2: #f8f9fa;        /* 카드/패널 */
  --bg-3: #f1f3f5;        /* 활성/hover */
  --bg-4: #e9ecef;        /* 구분선/비활성 */
  --bg-5: #dee2e6;        /* 강한 구분 */

  /* 5단계 텍스트 */
  --text-1: #111827;      /* 제목/강조 */
  --text-2: #374151;      /* 본문 */
  --text-3: #6b7280;      /* 보조 */
  --text-4: #9ca3af;      /* 힌트/placeholder */
  --text-5: #d1d5db;      /* 비활성/미세 */
}
```

**금지:**
- 배경 2단계만 사용 (white + gray)
- 텍스트 2단계만 사용 (black + gray)

---

## 3. Font Weight Hierarchy (4단계+)

```css
:root {
  --weight-regular: 400;   /* 본문 */
  --weight-medium: 500;    /* 소제목, 라벨 */
  --weight-semibold: 600;  /* 카드 제목, 메뉴 */
  --weight-bold: 700;      /* 섹션 제목 */
  --weight-black: 800;     /* 히어로 제목 (선택) */
}
```

**적용 규칙:**

| 요소 | weight |
|------|--------|
| 히어로 제목 | 700~800 |
| 섹션 제목 | 700 |
| 카드 제목 | 600 |
| 네비 링크 | 500 |
| 본문 텍스트 | 400 |
| 캡션/메타 | 400 (색상으로 구분) |
| 뱃지 텍스트 | 600 |
| 버튼 텍스트 | 600~700 |

**금지:**
- 전체 페이지에서 400과 700만 사용 (중간 단계 없음)

---

## 4. Multi-Layer Shadow

```css
/* ── 단층 shadow 금지. 다층 필수. ── */

/* 카드 기본 */
.card {
  box-shadow:
    0 1px 2px rgba(0,0,0,0.04),
    0 4px 8px rgba(0,0,0,0.04);
}

/* 카드 hover */
.card:hover {
  box-shadow:
    0 2px 4px rgba(0,0,0,0.04),
    0 8px 24px rgba(0,0,0,0.08);
}

/* 드롭다운/모달 */
.dropdown {
  box-shadow:
    0 2px 4px rgba(0,0,0,0.04),
    0 8px 16px rgba(0,0,0,0.08),
    0 24px 48px rgba(0,0,0,0.12);
}

/* 네비게이션 (미세) */
.nav {
  box-shadow: 0 1px 0 rgba(0,0,0,0.06);
}
```

**금지:**
- `box-shadow: 0 4px 6px rgba(0,0,0,0.1)` (단층 그림자)
- shadow 없이 border만으로 모든 깊이 표현

---

## 5. Line Height Matrix

```css
/* ── 요소별 line-height 차등 ── */
.hero-title    { line-height: 1.1; }   /* 큰 제목: 타이트 */
.section-title { line-height: 1.2; }   /* 섹션 제목 */
.card-title    { line-height: 1.3; }   /* 카드 제목 */
.subheading    { line-height: 1.4; }   /* 부제목 */
.body-text     { line-height: 1.6; }   /* 본문 */
.body-relaxed  { line-height: 1.8; }   /* 긴 본문/설명 */
.caption       { line-height: 1.5; }   /* 캡션/메타 */
```

**금지:**
- 전체 `body { line-height: 1.6 }` 하나로 통일

---

## 6. Border Precision

```css
/* ── border 3등급 ── */
--border-subtle:  1px solid rgba(0,0,0,0.04);  /* 미세 구분 */
--border-default: 1px solid rgba(0,0,0,0.08);  /* 기본 구분 */
--border-strong:  1px solid rgba(0,0,0,0.15);  /* 강한 구분 */

/* 적용 */
.card { border: var(--border-subtle); }
.input { border: var(--border-default); }
.input:focus { border: var(--border-strong); }
.nav { border-bottom: var(--border-subtle); }
.section-divider { border-top: var(--border-default); }
```

---

## 7. Responsive Breakpoints

```css
/* ── 3단계 반응형 ── */
@media (max-width: 1024px) { /* 태블릿 */ }
@media (max-width: 768px)  { /* 모바일 */ }
@media (max-width: 480px)  { /* 소형 모바일 */ }
```

---

## 구현 체크리스트

```yaml
precision_check:
  - [ ] 모든 spacing이 4px 그리드인가? (홀수 px 없음)
  - [ ] 배경색이 5단계 이상 명도 구분이 있는가?
  - [ ] font-weight가 4단계 이상 활용되고 있는가?
  - [ ] box-shadow가 다층 구조인가? (2+ layers)
  - [ ] line-height가 요소별로 차등 적용되었는가?
  - [ ] border가 3등급 (subtle/default/strong) 구분되는가?
  - [ ] 반응형 breakpoint가 3단계 이상인가?
```
