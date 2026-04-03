# Stitch Prompting Guide Reference

Stitch 프롬프트 작성 시 참조하는 상세 가이드.
이 문서는 프롬프트 생성 중 구체적인 패턴이나 테크닉 확인이 필요할 때 참조한다.

---

## 목차

1. [Stitch 프롬프트 기본 원칙](#1-stitch-프롬프트-기본-원칙)
2. [프로젝트 시작 전략](#2-프로젝트-시작-전략)
3. [화면별 반복 개선](#3-화면별-반복-개선)
4. [테마 제어](#4-테마-제어)
5. [이미지 수정](#5-이미지-수정)
6. [다국어 지원](#6-다국어-지원)
7. [MCP 도구 활용 패턴](#7-mcp-도구-활용-패턴)
8. [안티패턴](#8-안티패턴)

---

## 1. Stitch 프롬프트 기본 원칙

Stitch는 Gemini 기반 AI UI 디자인 도구로, **자연어 프롬프트**로 화면을 생성한다.
코드나 JSON이 아닌 영어 문장으로 디자인 의도를 전달한다.

### 핵심 원칙 6가지

| # | 원칙 | 설명 |
|---|---|---|
| 1 | **Clear & Concise** | 모호하지 않게. 하나의 문장이 하나의 의도를 전달 |
| 2 | **One Change at a Time** | 반복 수정 시 한 번에 하나의 주요 변경만 |
| 3 | **Use UI/UX Keywords** | "navigation bar", "card layout", "hero section" 등 표준 용어 사용 |
| 4 | **Reference Specifically** | "primary button on sign-up form", "image in hero section" 등 정확히 지칭 |
| 5 | **Iterate & Experiment** | 한 번에 완벽을 기대하지 말고, 점진적 개선 |
| 6 | **Review & Refine** | 결과가 다르면, 리프레이즈하거나 더 타겟팅된 프롬프트 |

---

## 2. 프로젝트 시작 전략

### High-Level 시작 (브레인스토밍/복잡한 앱)

전체 개념부터 시작하여 화면별로 디테일을 추가하는 방식.

```
"An app for marathon runners."
→ "An app for marathon runners to engage with a community, find partners,
   get training advice, and find races near them."
```

### Detailed 시작 (명확한 요구사항)

핵심 기능을 구체적으로 기술하여 바로 시작.

```
"Product detail page for a Japandi-styled tea store. Sells herbal teas, ceramics.
 Neutral, minimal colors, black buttons. Soft, elegant font."
```

### Vibe 설정

형용사로 앱의 분위기를 정의하면 색상, 폰트, 이미지 스타일에 영향.

| Vibe 형용사 | 결과 경향 |
|---|---|
| vibrant, encouraging | 밝은 색상, 활기찬 레이아웃 |
| minimalist, focused | 여백 많음, 단색 계열, 깔끔 |
| dark, premium | 어두운 배경, 골드/실버 악센트 |
| playful, friendly | 둥근 코너, 밝은 파스텔, 일러스트 |
| corporate, professional | 블루/그레이 계열, 직선적, 정돈된 |
| warm, inviting | 어스톤, 부드러운 그림자, 자연광 이미지 |

---

## 3. 화면별 반복 개선

### 증분 수정 패턴

```
초기: "Homepage for a fitness app"
1차: "On the homepage, add a search bar to the header."
2차: "Change the primary call-to-action button to be larger and use bright green."
3차: "Add a bottom navigation bar with Home, Workouts, Profile, Settings tabs."
```

### 이미지 스타일 가이드

```
"Music player page for 'Suburban Legends.' Album art is a macro, zoomed-in photo
 of ocean water. Page background/imagery should reflect this."
```

이미지 설명은 구체적일수록 좋다. "pretty image" 보다 "warm-toned photo of a coffee shop interior with morning sunlight" 가 훨씬 정확한 결과를 낸다.

---

## 4. 테마 제어

### 색상

```
구체적: "Change primary color to forest green."
무드 기반: "Update theme to a warm, inviting color palette."
정확한 값: "Primary color: #1E40AF. Accent: #F59E0B. Background: #FAFAF9."
```

### 폰트 & 테두리

```
폰트: "Use a playful sans-serif font."
      "Change headings to a serif font."
테두리: "Make all buttons have fully rounded corners."
       "Give input fields a 2px solid black border."
결합: "Book discovery app: serif font for text, light green brand color for accents."
```

### 테마 변경 시 이미지 동기화

```
"Update theme to light orange. Ensure all images and illustrative icons match
 this new color scheme."
```

테마 색상 변경 시 이미지도 함께 변경할지 명시하지 않으면, 이미지는 기존 것이 유지될 수 있다.

---

## 5. 이미지 수정

### 일반 이미지 타겟팅

```
"Change background of all product images on landing page to light taupe."
```

### 특정 이미지 타겟팅

```
"On 'Team' page, image of 'Dr. Carter (Lead Dentist)': update her lab coat to black."
```

### 이미지 수정 팁

- 이미지를 지칭할 때 앱 콘텐츠의 서술적 용어를 사용
- 페이지명 + 이미지의 내용/위치로 특정
- 여러 이미지 일괄 변경 시 [all] 키워드 사용

---

## 6. 다국어 지원

```
"Switch all product copy and button text to Spanish."
"Change all UI text to Korean. Keep brand names in English."
```

---

## 7. MCP 도구 활용 패턴

### 도구 매핑

| 작업 | MCP 도구 | 주요 파라미터 |
|---|---|---|
| 프로젝트 생성 | `create_project` | title |
| 프로젝트 조회 | `get_project`, `list_projects` | name, filter |
| 스크린 생성 | `generate_screen_from_text` | projectId, prompt, deviceType, modelId |
| 스크린 수정 | `edit_screens` | projectId, selectedScreenIds, prompt |
| 변형 생성 | `generate_variants` | projectId, selectedScreenIds, prompt, variantOptions |
| 스크린 조회 | `get_screen`, `list_screens` | name/projectId |

### Device Type 선택 가이드

| 이미지 특성 | 권장 deviceType |
|---|---|
| 넓은 레이아웃, 사이드바 있음 | DESKTOP |
| 좁은 세로 레이아웃, 하단 네비게이션 | MOBILE |
| 중간 크기, 분할 뷰 | TABLET |
| 범용/개념적 | AGNOSTIC |

### Model 선택 가이드

| 상황 | 권장 모델 |
|---|---|
| 복잡한 대시보드, 다수 컴포넌트 | GEMINI_3_1_PRO |
| 빠른 프로토타이핑, 단순 화면 | GEMINI_3_FLASH |
| 최고 품질 필요 | GEMINI_3_1_PRO |

### Variant 활용 패턴

```python
# 레이아웃 변형 탐색
variantOptions = {
    "aspects": ["LAYOUT"],
    "creativeRange": "EXPLORE",  # REFINE / EXPLORE / REIMAGINE
    "variantCount": 3
}

# 색상 스킴 변형
variantOptions = {
    "aspects": ["COLOR_SCHEME"],
    "creativeRange": "REIMAGINE",
    "variantCount": 5
}

# 미세 조정
variantOptions = {
    "aspects": ["LAYOUT", "COLOR_SCHEME", "TEXT_FONT"],
    "creativeRange": "REFINE",
    "variantCount": 3
}
```

### 생성 → 반복 수정 워크플로우

```
1. generate_screen_from_text → 초기 화면 생성
2. list_screens → 생성된 스크린 ID 확인
3. edit_screens → 특정 수정 사항 적용
4. generate_variants → 대안 탐색
5. 반복 (2-4) → 만족할 때까지
```

---

## 8. 안티패턴

### 하지 말아야 할 것

| 안티패턴 | 왜 문제인가 | 대신 이렇게 |
|---|---|---|
| CSS/코드 문법 사용 | Stitch는 코드를 해석하지 않음 | 자연어로 설명 |
| 한 프롬프트에 모든 것 | 결과 품질 저하, 디버깅 어려움 | 화면 하나씩, 변경 하나씩 |
| 모호한 지시 | "좀 더 좋게" → 어떻게? | "버튼을 더 크게, 파란색으로" |
| 파일명 참조 | "logo.png 사용해줘" | "왼쪽 상단에 회사 로고" |
| 픽셀 단위 지정 | Stitch는 반응형 디자인 | "넓은/좁은", "크게/작게" 등 상대적 표현 |
| 한국어 프롬프트 | 영어 대비 품질 차이 | 프롬프트는 항상 영어로 |

### 흔한 실수와 해결

| 실수 | 해결 |
|---|---|
| 생성된 색상이 의도와 다름 | 구체적 HEX 값 또는 색상명 명시 |
| 이미지가 테마와 안 맞음 | "Ensure images match the [color] theme" 추가 |
| 레이아웃 구조가 뒤바뀜 | 섹션을 위에서 아래로 순서대로 기술 |
| 텍스트가 placeholder로 나옴 | 실제 텍스트 내용을 프롬프트에 직접 포함 |
| 컴포넌트가 누락됨 | 각 섹션의 요소를 빠짐없이 나열 |
