# IMAGE ENGINE v1.0 — 이미지 자동 생성 모듈

> CREATIVE_GENERATION_FRAMEWORK 품질 모듈.
> 모든 placeholder를 실제 시각 콘텐츠로 교체.
> 이미지가 없는 웹페이지는 미완성이다.

---

## 원칙

```
1. 회색 직사각형 placeholder 절대 금지
2. 모든 썸네일/이미지 영역에 시각 콘텐츠 필수
3. 이미지는 해당 카드의 제목/성격에 맞게 생성
4. 3가지 이미지 전략 중 최소 1가지 이상 적용
```

---

## 이미지 전략 3가지

### 전략 1: CSS Gradient Art (기본 — 외부 의존 없음)

> 코드만으로 시각적 풍성함 확보. 모든 환경에서 작동.

```css
/* 패턴 A: 추상 그라디언트 아트 (섹션 분위기 반영) */
.thumb-education {
  background:
    linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 패턴 B: 기하학적 패턴 */
.thumb-data {
  background:
    conic-gradient(from 45deg at 50% 50%, #1e293b 0%, #3b82f6 25%, #1e293b 50%, #60a5fa 75%, #1e293b 100%);
}

/* 패턴 C: 메시 그라디언트 (유기적) */
.thumb-creative {
  background:
    radial-gradient(at 40% 20%, #e879f9 0px, transparent 50%),
    radial-gradient(at 80% 0%, #38bdf8 0px, transparent 50%),
    radial-gradient(at 0% 50%, #818cf8 0px, transparent 50%),
    #0f172a;
}
```

**제목→그라디언트 매핑 규칙:**

| 카드 제목 키워드 | 그라디언트 방향 | 색상 계열 |
|---------------|-------------|---------|
| 보호/보안/방지 | 대각선 135deg | 남색→보라 (안정/보호) |
| 교육/학습/기초 | 수평 90deg | 청→하늘 (지식/성장) |
| 실무/테크닉/도전 | 원형 radial | 청록→에메랄드 (실행/동적) |
| 법규/정책/규정 | 수직 180deg | 슬레이트→그레이 (공식/권위) |
| 문화/가치/윤리 | 메시 multi | 보라→핑크 (가치/감성) |
| 데이터/분석/엑셀 | conic | 다크+블루 포인트 (기술/정밀) |

**구현 코드 예시:**
```css
/* 각 썸네일에 data-category로 그라디언트 자동 적용 */
[data-category="보안"] .thumb {
  background: linear-gradient(135deg, #312e81 0%, #7c3aed 50%, #4c1d95 100%);
}
[data-category="교육"] .thumb {
  background: linear-gradient(90deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
}
[data-category="실무"] .thumb {
  background: radial-gradient(circle at 30% 40%, #059669, #0d9488, #0891b2);
}
[data-category="법규"] .thumb {
  background: linear-gradient(180deg, #334155 0%, #64748b 100%);
}
```

### 전략 2: SVG Inline 아이콘/일러스트 (중급)

> 가벼운 SVG 아이콘을 썸네일 중앙에 배치.

```html
<div class="thumb" data-category="보안">
  <svg viewBox="0 0 48 48" class="thumb-icon">
    <path d="M24 4L6 12v12c0 10.5 7.7 20.3 18 22.6C34.3 44.3 42 34.5 42 24V12L24 4z"
          fill="none" stroke="currentColor" stroke-width="2"/>
    <path d="M18 24l4 4 8-8" fill="none" stroke="currentColor" stroke-width="2"/>
  </svg>
</div>
```

**SVG 아이콘 매핑:**

| 카테고리 | SVG 아이콘 | 형태 설명 |
|---------|----------|---------|
| 보안/보호 | shield + check | 방패 + 체크마크 |
| 교육/학습 | book-open | 펼친 책 |
| 법규/정책 | scroll/gavel | 두루마리/법봉 |
| 실무/기술 | wrench/code | 렌치/코드 브래킷 |
| 데이터/분석 | chart-bar | 막대 차트 |
| 커뮤니케이션 | users/message | 사람들/말풍선 |

```css
.thumb-icon {
  width: 64px; height: 64px;
  color: rgba(255,255,255,0.3);
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
}
```

### 전략 3: AI 이미지 생성 (최고 품질 — Gemini/DALL-E)

> 실제 이미지 생성 API 연동. 최고 품질이지만 API 키 필요.

**프롬프트 자동 생성 규칙:**

```
카드 제목: "{title}"
카테고리: "{category}"
색온도: "{SLOT_2 값}"
메타포: "{SLOT_1 값}"

→ 이미지 프롬프트:
"Professional thumbnail for online education course titled '{title}'.
Category: {category}. Style: {SLOT_1 metaphor} aesthetic.
Color temperature: {SLOT_2}. Abstract, no text, no people.
Aspect ratio: 16:9. 800x450px. High quality, editorial photography style."
```

**API 호출 코드 (Python):**
```python
# scripts/generate_thumbnails.py
import google.generativeai as genai

def generate_thumbnail(title, category, slot1, slot2):
    prompt = f"""Professional thumbnail for education course: {title}
    Category: {category}. Visual style: {slot1} aesthetic.
    Color mood: {slot2}. Abstract background, no text overlay.
    16:9 ratio, high quality, editorial style."""

    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    response = model.generate_content(prompt)
    # Save image to output/thumbnails/
    return response.image
```

---

## 이미지 영역별 규칙

### 히어로/배너 영역
```
- 전략 1 필수: 풀너비 그라디언트 (단색 배경 금지)
- 그라디언트 방향: SLOT_1 메타포에서 파생
  - 천문대 → radial (별/행성 느낌)
  - 건축 → linear 수직 (구조/기둥)
  - 재봉 → linear 대각 45deg (직물 직조)
- 최소 2개 색상, SLOT_2 색온도에서 파생
```

### 코스/동영상 썸네일 (16:9)
```
- 전략 1 + 전략 2 조합: 그라디언트 배경 + SVG 아이콘 오버레이
- 각 카드의 제목에서 카테고리 추출 → 매핑 테이블 참조
- 카드마다 그라디언트 각도/색상이 미묘하게 다를 것 (±15deg, ±10% hue)
- 아이콘은 중앙 하단, opacity 0.25 (은은하게)
```

### 책 표지 (3:4)
```
- 전략 1: 각 책 제목에서 분위기 추출 → 그라디언트 매핑
  - "가짜 노동" → 회색+붉은 포인트 (비판적)
  - "도파민네이션" → 보라+핑크 (뇌과학)
  - "쇼펜하우어" → 남색+골드 (철학/클래식)
- 각 표지의 하단에 작은 텍스트 오버레이 가능 (제목 첫 글자)
```

### 채널 아바타 (1:1 원형)
```
- 이니셜 텍스트 + 그라디언트 배경
- 각 채널마다 다른 그라디언트 색상
- font-size: 16px, font-weight: 700
```

### 학습현황 도넛 차트
```
- CSS conic-gradient로 구현 (이미지 아님)
- 진행률을 실제 각도로 반영
- accent 색상으로 진행 부분 표시
```

---

## 구현 체크리스트

```yaml
image_check:
  - [ ] 히어로/배너에 그라디언트 또는 이미지가 있는가? (단색 배경 금지)
  - [ ] 모든 코스 썸네일에 그라디언트+아이콘이 있는가? (회색 placeholder 금지)
  - [ ] 각 썸네일의 색상이 해당 카드 제목/카테고리와 관련 있는가?
  - [ ] 책 표지에 각각 다른 그라디언트가 적용되었는가?
  - [ ] 채널 아바타에 이니셜+그라디언트가 있는가?
  - [ ] 동일한 그라디언트가 2개 이상 반복되지 않는가?
  - [ ] 학습 도넛 차트가 CSS conic-gradient로 구현되었는가?
```

---

## SLOT 연동

| SLOT | 이미지 영향 |
|------|----------|
| SLOT_1 | 그라디언트 방향/패턴 결정 (천문대→radial, 건축→linear, 재봉→diagonal) |
| SLOT_2 | 그라디언트 색상 계열 결정 (한랭→blue계, 온난→amber계, 대지→brown계) |
| SLOT_3 | 이미지 배치 위치 결정 (대시보드→sidebar 내 아이콘, 모자이크→셀 전체 채움) |
| SLOT_4 | 오버레이 텍스트 서체 (있을 경우) |
| SLOT_5 | 이미지 위 accent 요소 사용 규칙 |
