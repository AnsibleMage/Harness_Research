# 슬라이드 디자인 패턴

> spec-analyzer와 html-slide-builder가 참조하는 레이아웃 패턴

---

## 슬라이드 타입별 레이아웃

모든 좌표는 16:9 기준 (720pt x 405pt) body 내부 절대 위치다.

---

### title (타이틀 슬라이드)

발표 시작 슬라이드. 제목과 부제목을 중앙 정렬로 배치한다. 배경색 또는 배경 이미지를 사용하여 인상적인 첫 슬라이드를 만든다.

**레이아웃 구조**

```
┌───────────────────────────────────────────────┐
│                                               │
│                                               │
│          [메인 제목 텍스트]                    │  ← y: 120pt
│          [부제목 또는 설명]                    │  ← y: 220pt
│                                               │
│                                               │
│          [발표자 / 날짜 / 소속]                │  ← y: 330pt (선택)
└───────────────────────────────────────────────┘
```

**위치 가이드**

| 요소 | x | y | w | h |
|------|---|---|---|---|
| 메인 제목 | 60pt | 120pt | 600pt | 80pt |
| 부제목 | 100pt | 220pt | 520pt | 50pt |
| 부가 정보 | 100pt | 330pt | 520pt | 40pt |

**HTML 예시**

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      width: 720pt;
      height: 405pt;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: #1F2937;
    }
    .title-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-top: 20pt;
    }
  </style>
</head>
<body>
  <div class="title-container">
    <h1 style="
      font-family: Arial;
      font-size: 40pt;
      color: #FFFFFF;
      text-align: center;
      margin-bottom: 20pt;
    ">메인 제목</h1>
    <p style="
      font-family: Arial;
      font-size: 18pt;
      color: #D1D5DB;
      text-align: center;
    ">부제목 또는 핵심 메시지</p>
  </div>
</body>
</html>
```

---

### content (콘텐츠 슬라이드)

가장 일반적인 슬라이드 타입. 상단에 제목을 두고 본문 영역에 텍스트 또는 리스트를 배치한다.

**레이아웃 구조**

```
┌───────────────────────────────────────────────┐
│ [슬라이드 제목]                                │  ← y: 20pt
├───────────────────────────────────────────────┤
│                                               │
│  • 본문 항목 1                                 │  ← y: 80pt
│  • 본문 항목 2                                 │
│  • 본문 항목 3                                 │
│                                               │
└───────────────────────────────────────────────┘
```

**위치 가이드**

| 요소 | x | y | w | h |
|------|---|---|---|---|
| 제목 | 20pt | 20pt | 680pt | 45pt |
| 구분선 (선택) | 20pt | 65pt | 680pt | 2pt |
| 본문 영역 | 20pt | 80pt | 680pt | 305pt |

**HTML 예시**

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      width: 720pt;
      height: 405pt;
      display: flex;
      flex-direction: column;
      padding: 20pt;
      box-sizing: border-box;
    }
  </style>
</head>
<body>
  <h2 style="
    font-family: Arial;
    font-size: 28pt;
    color: #1F2937;
    margin-bottom: 15pt;
    border-bottom: 2pt solid #4A90D9;
    padding-bottom: 8pt;
  ">슬라이드 제목</h2>
  <ul style="font-family: Arial; font-size: 16pt; color: #374151; line-height: 1.6;">
    <li>첫 번째 핵심 내용을 여기에 작성한다</li>
    <li>두 번째 핵심 내용을 여기에 작성한다</li>
    <li>세 번째 핵심 내용을 여기에 작성한다</li>
  </ul>
</body>
</html>
```

---

### two_column (2단 레이아웃)

두 가지 내용을 나란히 비교하거나 텍스트와 이미지/차트를 함께 보여줄 때 사용한다.

**레이아웃 구조**

```
┌───────────────────────────────────────────────┐
│ [슬라이드 제목]                                │  ← y: 20pt
├──────────────────────┬────────────────────────┤
│                      │                        │
│  [왼쪽 콘텐츠]       │  [오른쪽 콘텐츠]        │
│                      │                        │
│  x: 20pt, w: 340pt   │  x: 370pt, w: 340pt    │
│                      │                        │
└──────────────────────┴────────────────────────┘
```

**위치 가이드**

| 요소 | x | y | w | h |
|------|---|---|---|---|
| 제목 | 20pt | 20pt | 680pt | 45pt |
| 좌측 영역 | 20pt | 80pt | 340pt | 305pt |
| 우측 영역 | 370pt | 80pt | 340pt | 305pt |
| 중앙 구분선 (선택) | 358pt | 80pt | 2pt | 305pt |

**HTML 예시**

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      width: 720pt;
      height: 405pt;
      display: flex;
      flex-direction: column;
      padding: 20pt;
      box-sizing: border-box;
    }
    .content-row {
      display: flex;
      flex-direction: row;
      flex: 1;
      gap: 10pt;
    }
    .column {
      width: 340pt;
      display: flex;
      flex-direction: column;
    }
  </style>
</head>
<body>
  <h2 style="font-family: Arial; font-size: 26pt; color: #1F2937; margin-bottom: 15pt;">
    비교 분석 슬라이드
  </h2>
  <div class="content-row">
    <div class="column">
      <h3 style="font-family: Arial; font-size: 18pt; color: #4A90D9;">장점</h3>
      <ul style="font-family: Arial; font-size: 14pt; color: #374151;">
        <li>비용 효율성 높음</li>
        <li>구현 속도 빠름</li>
        <li>유지보수 용이</li>
      </ul>
    </div>
    <div class="column">
      <h3 style="font-family: Arial; font-size: 18pt; color: #E74C3C;">단점</h3>
      <ul style="font-family: Arial; font-size: 14pt; color: #374151;">
        <li>확장성 제한</li>
        <li>커스터마이징 어려움</li>
        <li>의존성 증가</li>
      </ul>
    </div>
  </div>
</body>
</html>
```

---

### section_header (섹션 구분 슬라이드)

발표 흐름에서 새로운 섹션의 시작을 알리는 슬라이드. 큰 텍스트와 강조 배경색을 사용한다.

**레이아웃 구조**

```
┌───────────────────────────────────────────────┐
│                                               │
│                                               │
│              [섹션 번호]                       │  ← y: 140pt (선택)
│              [섹션 제목]                       │  ← y: 180pt
│              [짧은 설명]                       │  ← y: 250pt (선택)
│                                               │
│                                               │
└───────────────────────────────────────────────┘
```

**HTML 예시**

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      width: 720pt;
      height: 405pt;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: #4A90D9;
    }
  </style>
</head>
<body>
  <p style="
    font-family: Arial;
    font-size: 16pt;
    color: #BFD9F5;
    text-align: center;
    margin-bottom: 10pt;
  ">SECTION 02</p>
  <h1 style="
    font-family: Arial;
    font-size: 42pt;
    color: #FFFFFF;
    text-align: center;
    margin-bottom: 15pt;
  ">시장 분석</h1>
  <p style="
    font-family: Arial;
    font-size: 16pt;
    color: #D6EAF8;
    text-align: center;
  ">현재 시장 상황과 기회 요인을 살펴봅니다</p>
</body>
</html>
```

---

### wireframe (와이어프레임 슬라이드)

전체 UI를 1개의 큰 슬라이드로 표현한다. 원본 색상을 흑백으로 변환하고, 각 영역에 번호 배지를 달고, 오른쪽에 디스크립션 패널을 배치한다.

**레이아웃 구조**

```
┌────────────────────────────────────────┬─────────────┐
│                                        │ 화면 구성    │
│  ①  광고 배너 (#808080)               │ 설명         │
│                                        │             │
│  ②  사이드바    ③  헤더               │ 1. 광고 배너  │
│     (#E0E0E0)      (#FFFFFF)          │    설명...    │
│                                        │             │
│  ④  메인 콘텐츠                        │ 2. 사이드바   │
│     (#FFFFFF, border #000000)          │    설명...    │
│                                        │             │
│  ⑤  푸터                              │ ...          │
│     (#E0E0E0)                          │             │
└────────────────────────────────────────┴─────────────┘
 ←── 콘텐츠 영역 (가변) ──→←── 275pt ──→
```

**특성**

| 항목 | 값 |
|------|-----|
| body 크기 | 콘텐츠 폭 + 275pt (패널) × 높이 (원본 비율 기반) |
| 색상 | #000000, #808080, #E0E0E0, #FFFFFF 만 사용 |
| 배치 | 모든 요소 absolute positioning |
| 배지 | 20pt 검정 원 + 흰색 숫자, 각 영역 좌상단 |
| 패널 | 275pt 폭, border-left: 1pt solid #000000 |
| 폰트 | Arial only |

**카드/버튼/배너 와이어프레임 패턴**

| 원본 요소 | 와이어프레임 표현 |
|----------|----------------|
| 컬러 섹션 배경 | `#E0E0E0` 또는 `#FFFFFF` |
| 컬러 버튼 | `#808080` bg + `#FFFFFF` 텍스트 |
| 컬러 테두리 | `0.5~2pt solid #000000` |
| 카드/컨테이너 | `#FFFFFF` bg + `0.5pt solid #000000` border |
| 배너 | `#808080` bg |
| 활성/선택 상태 | `#E0E0E0` bg |
| 구분선 | `border-bottom: 0.5pt solid #000000` |

**HTML 예시**

```html
<!DOCTYPE html>
<html>
<head>
<style>
html { background: #ffffff; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  width: 1684pt; height: 1191pt;
  margin: 0; padding: 0;
  background: #ffffff;
  font-family: Arial, sans-serif;
  display: flex;
  position: relative;
}
.badge {
  position: absolute;
  width: 20pt; height: 20pt;
  background: #000000;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  z-index: 100;
}
.badge p {
  color: #ffffff; font-size: 9.75pt; font-weight: bold;
  margin: 0; text-align: center;
}
</style>
</head>
<body>
<!-- 1. 콘텐츠 영역들 (먼저 배치 = 아래 레이어) -->
<div style="position:absolute; left:0pt; top:0pt; width:1409pt; height:96pt; background:#808080;">
  <p style="color:#ffffff; font-size:13.5pt; font-weight:bold;">헤더</p>
</div>
<div style="position:absolute; left:0pt; top:96pt; width:1409pt; height:200pt; background:#E0E0E0;">
  <p style="color:#000000; font-size:13.5pt;">콘텐츠 영역</p>
</div>

<!-- 2. 오버레이 마커 (콘텐츠 뒤에 = 위 레이어, z-index:9999) -->
<div style="position:absolute; left:0pt; top:0pt; width:24pt; height:24pt; background:#000000; z-index:9999;">
  <p style="color:#ffffff; font-size:9pt;">TL</p>
</div>

<!-- 3. 번호 배지 (가장 마지막 = 최상위, 각 배지는 고유 좌표) -->
<div class="badge" style="left:34pt; top:6pt; z-index:9999;"><p>1</p></div>
<div class="badge" style="left:34pt; top:102pt; z-index:9999;"><p>2</p></div>

<!-- 4. 디스크립션 패널 -->
<div style="position:absolute; left:1409pt; top:0pt; width:275pt; height:1191pt; background:#ffffff; border-left:1pt solid #000000;">
  <p style="font-size:12pt; font-weight:bold;">화면 구성 설명</p>
</div>
</body>
</html>
```

---

## 여백 가이드

슬라이드 가독성을 위한 최소 여백 기준이다. 이 기준을 지키지 않으면 텍스트가 가장자리에 붙어 보이거나 요소들이 겹쳐 보인다.

| 여백 유형 | 최솟값 | 권장값 |
|----------|-------|-------|
| 슬라이드 외곽 여백 (body padding) | 20pt | 30pt |
| 제목과 본문 사이 간격 | 10pt | 15pt |
| 리스트 항목 간 간격 | 5pt | 8pt |
| 이미지와 텍스트 사이 간격 | 10pt | 15pt |
| 텍스트와 도형 경계 사이 간격 | 5pt | 10pt |
| 2단 레이아웃 열 간 간격 | 10pt | 20pt |
| 그래픽 요소와 슬라이드 하단 사이 | 15pt | 25pt |

---

## 폰트 크기 가이드

슬라이드 크기(720pt x 405pt) 기준의 권장 폰트 크기다. 너무 작으면 프로젝터에서 보이지 않고, 너무 크면 내용이 잘린다.

| 요소 | 최솟값 | 권장 범위 | 최댓값 |
|------|-------|---------|-------|
| 메인 타이틀 (title 슬라이드) | 32pt | 36-40pt | 48pt |
| 슬라이드 제목 (h2) | 22pt | 24-32pt | 36pt |
| 섹션 헤더 제목 | 30pt | 36-44pt | 52pt |
| 본문 텍스트 (p) | 12pt | 14-18pt | 22pt |
| 리스트 항목 (li) | 12pt | 14-16pt | 20pt |
| 2단 레이아웃 소제목 | 14pt | 16-20pt | 24pt |
| 2단 레이아웃 본문 | 11pt | 12-14pt | 16pt |
| 캡션 및 출처 주석 | 8pt | 10-12pt | 14pt |
| 차트 제목 | 12pt | 13-16pt | 18pt |
| 차트 데이터 라벨 | 8pt | 10-12pt | 14pt |
| 와이어프레임 제목 | 18pt | 22.5pt | 22.5pt |
| 와이어프레임 섹션 헤더 | 12pt | 13.5pt | 13.5pt |
| 와이어프레임 본문 | 10.5pt | 10.5-12pt | 12pt |
| 와이어프레임 세부 텍스트 | 9pt | 9-9.75pt | 9.75pt |
| 와이어프레임 배지 숫자 | 9.75pt | 9.75pt | 9.75pt |

---

## 색상 패턴

### 밝은 배경 (기본 — Light Mode)

대부분의 슬라이드에 적용하는 기본 색상 체계다. 프리젠테이션의 80% 이상은 이 패턴을 사용한다.

| 역할 | 색상 (CSS) | 용도 |
|------|-----------|------|
| 배경 | `#FFFFFF` 또는 `#F9FAFB` | 슬라이드 배경 |
| 기본 텍스트 | `#1F2937` | 제목, 본문 |
| 보조 텍스트 | `#6B7280` | 캡션, 부제, 설명 |
| 강조 텍스트 | `#4A90D9` | 키워드, 하이라이트 |
| 구분선 | `#E5E7EB` | 테이블 경계, 구분선 |
| 배경 강조 | `#EBF5FB` | 테이블 헤더, 박스 배경 |

### 어두운 배경 (Dark Mode)

타이틀 슬라이드, 섹션 헤더, 특별 강조 슬라이드에 사용한다.

| 역할 | 색상 (CSS) | 용도 |
|------|-----------|------|
| 배경 | `#1F2937` 또는 `#111827` | 슬라이드 배경 |
| 기본 텍스트 | `#FFFFFF` | 제목, 본문 |
| 보조 텍스트 | `#D1D5DB` | 부제목, 설명 |
| 강조 텍스트 | `#93C5FD` | 키워드 강조 |
| 구분선 | `#374151` | 섹션 구분 |

### 강조 배경 (Accent / Brand)

섹션 헤더 슬라이드 또는 핵심 메시지 슬라이드에 사용한다.

| 역할 | 색상 (CSS) | 용도 |
|------|-----------|------|
| 배경 | 브랜드 primary 색상 | 슬라이드 배경 |
| 기본 텍스트 | `#FFFFFF` | 제목, 본문 |
| 보조 텍스트 | 배경색보다 20% 밝은 색 | 부제목, 설명 |

### 추천 브랜드 강조 색상

| 색상명 | HEX (CSS) | 어울리는 텍스트 |
|-------|----------|--------------|
| 블루 프라이머리 | `#4A90D9` | `#FFFFFF` |
| 다크 네이비 | `#1E3A5F` | `#FFFFFF` |
| 에메랄드 | `#27AE60` | `#FFFFFF` |
| 딥 레드 | `#C0392B` | `#FFFFFF` |
| 골든 앰버 | `#F39C12` | `#1F2937` |
| 퍼플 | `#8E44AD` | `#FFFFFF` |
| 틸 | `#16A085` | `#FFFFFF` |

---

## 웹 요소 → 슬라이드 변환 패턴

웹 페이지나 앱 UI를 슬라이드로 변환할 때 각 웹 요소를 어떻게 표현할지 결정하는 기준표다.

| 웹 요소 | 슬라이드 표현 방법 | 비고 |
|---------|----------------|------|
| 네비게이션 바 | 생략하거나 타이틀 슬라이드 상단에 브랜드명 텍스트만 표시 | 불필요한 UI 제거 |
| 히어로 섹션 | 타이틀 슬라이드 (배경 이미지 + 큰 제목) | 핵심 메시지 중심으로 재구성 |
| 카드 레이아웃 (3열) | 2단 또는 3단 그리드 (슬라이드당 1-2행) | 너무 많은 카드는 슬라이드 분할 |
| 카드 레이아웃 (2열) | two_column 레이아웃 | 카드 테두리는 div border로 표현 |
| 폼 입력 필드 | 도형(rect) + 텍스트 조합으로 입력 영역 시각화 | 실제 입력 불가, 목업 형식 |
| 버튼 | 도형(rounded rect) + 중앙 텍스트 | border-radius: 6-8pt 사용 |
| 드롭다운 | 선택된 값을 텍스트로 표시하거나 옵션 목록 나열 | ul/li로 옵션 표현 |
| 탭 UI | 각 탭 내용을 별도 슬라이드로 분할 | 탭 이름을 슬라이드 제목에 포함 |
| 사이드바 | two_column 레이아웃의 좌측 열 (w: 180-200pt) | 사이드바 내용 축약 필요 |
| 데이터 테이블 | PptxGenJS addTable API 또는 도형 그리드 | 열이 7개 초과 시 분할 고려 |
| 차트/그래프 | PptxGenJS addChart API (class="placeholder" 사용) | 데이터를 JS 변수로 별도 관리 |
| 모달/팝업 | 중앙 배치 div (border + shadow) + overlay 배경 | 슬라이드 전체 context에서 표현 |
| 진행 바 | 배경 rect + 진행 rect 겹침 | fill 색상으로 완료 비율 표현 |
| 아이콘 | SVG를 PNG로 변환 후 img 태그 참조 | Sharp 사용, CSS gradient 금지 |
| 로딩 스피너 | 정적 원형 도형으로 표현 | 애니메이션 불가 |
| 페이지네이션 | 슬라이드 하단에 텍스트로 "X / Y" 표시 | 또는 생략 |
| 푸터 | 슬라이드 최하단 소형 텍스트 | y: 380pt 이상에 배치 |
| 배너/알림 | 상단 div (배경색 + p 태그 텍스트) | 중요도에 따라 색상 선택 |
| 아코디언 | 펼쳐진 상태 하나를 대표로 표시 | 또는 모든 항목을 ul로 나열 |

---

## 콘텐츠 밀도 가이드

슬라이드당 너무 많은 정보를 담으면 가독성이 떨어진다. 아래 기준을 초과하면 슬라이드를 분할한다.

### 요소 수 기준

| 기준 | 권장 | 최대 |
|------|------|------|
| 슬라이드당 총 요소 수 | 5-6개 | 8개 |
| 텍스트 블록 수 | 3-4개 | 6개 |
| 이미지/아이콘 수 | 2-3개 | 5개 |
| 도형 수 | 3-5개 | 8개 |

### 텍스트 양 기준

| 기준 | 권장 | 최대 |
|------|------|------|
| 텍스트 총 라인 수 | 5-6줄 | 8줄 |
| 리스트 항목 수 | 4-5개 | 6개 |
| 한 줄 텍스트 길이 | 50자 이내 | 70자 |
| 단락(p 태그) 수 | 2-3개 | 5개 |

### 슬라이드 분할 기준

아래 상황에서는 슬라이드를 2개 이상으로 분할한다.

1. 리스트 항목이 6개를 초과하는 경우
2. 텍스트 라인이 8줄을 초과하는 경우
3. 3개 이상의 차트를 한 슬라이드에 배치해야 하는 경우
4. 4열 이상의 복잡한 테이블을 전체 내용으로 표시해야 하는 경우
5. 2단 레이아웃에서 각 열의 내용이 6줄을 초과하는 경우

---

## 차트 플레이스홀더 위치 가이드

차트가 포함된 슬라이드에서 플레이스홀더의 권장 위치다.

### 단일 차트 (full-width)

```html
<div class="placeholder" id="chart-main"
  style="width: 640pt; height: 280pt; margin: 20pt auto;">
</div>
```

### 좌측 차트 + 우측 텍스트

```html
<div style="display: flex; flex-direction: row; gap: 15pt; margin: 0 20pt;">
  <div class="placeholder" id="chart-left"
    style="width: 380pt; height: 280pt;">
  </div>
  <div style="width: 265pt; display: flex; flex-direction: column;">
    <h3 style="font-family: Arial; font-size: 16pt; color: #1F2937;">분석 결과</h3>
    <ul style="font-family: Arial; font-size: 13pt; color: #374151;">
      <li>핵심 인사이트 1</li>
      <li>핵심 인사이트 2</li>
    </ul>
  </div>
</div>
```

### 2개 차트 (나란히)

```html
<div style="display: flex; flex-direction: row; gap: 15pt; margin: 0 15pt;">
  <div class="placeholder" id="chart-left"
    style="width: 325pt; height: 270pt;">
  </div>
  <div class="placeholder" id="chart-right"
    style="width: 325pt; height: 270pt;">
  </div>
</div>
```

---

## 슬라이드 번호 및 헤더 패턴

### 슬라이드 번호 표시

```html
<!-- 슬라이드 우측 하단에 페이지 번호 -->
<p style="
  position: absolute;
  right: 20pt;
  bottom: 10pt;
  font-family: Arial;
  font-size: 10pt;
  color: #9CA3AF;
">3 / 12</p>
```

> `position: absolute`는 html2pptx 엔진에서 제한적으로 지원된다. 필요한 경우 flex 레이아웃 내에서 margin을 사용한 배치를 우선 고려한다.

### 상단 브랜드 헤더

```html
<div style="
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 680pt;
  height: 30pt;
  margin-bottom: 10pt;
">
  <p style="
    font-family: Arial;
    font-size: 11pt;
    color: #6B7280;
    flex: 1;
  ">회사명</p>
  <p style="
    font-family: Arial;
    font-size: 11pt;
    color: #6B7280;
  ">발표 주제</p>
</div>
```

---

## 다단계 리스트 패턴

리스트 항목에 하위 항목이 필요한 경우 중첩 ul/ol을 사용한다.

```html
<ul style="font-family: Arial; font-size: 15pt; color: #1F2937; line-height: 1.5;">
  <li>주요 항목 1
    <ul style="font-size: 12pt; color: #6B7280; margin-top: 4pt;">
      <li>세부 항목 1-1</li>
      <li>세부 항목 1-2</li>
    </ul>
  </li>
  <li>주요 항목 2</li>
  <li>주요 항목 3</li>
</ul>
```

> 2단계 이상의 리스트는 슬라이드 공간을 빠르게 소모한다. 3단계 이상의 중첩은 피하고 슬라이드를 분할하거나 콘텐츠를 재구성한다.
