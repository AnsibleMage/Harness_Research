# html2pptx 변환 규칙 요약

> 에이전트가 빠르게 참조할 수 있는 규칙 체크리스트

---

## 필수 HTML 구조

모든 슬라이드 HTML 파일은 아래 기본 구조를 반드시 따라야 한다.

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      width: 720pt;
      height: 405pt;   /* 16:9 */
      display: flex;
      /* 추가 레이아웃 속성 */
    }
  </style>
</head>
<body>
  <!-- 슬라이드 콘텐츠 -->
</body>
</html>
```

### body 치수 (레이아웃별)

| 비율 | width | height |
|------|-------|--------|
| 16:9 | 720pt | 405pt |
| 4:3 | 720pt | 540pt |
| 16:10 | 720pt | 450pt |

### 커스텀 body 크기 (CUSTOM 레이아웃)

와이어프레임 모드 등에서는 표준 3가지 비율 외의 body 크기를 사용할 수 있다.

| 항목 | 조건 |
|------|------|
| width | 양수 pt 값 (예: 1684pt) |
| height | 양수 pt 값 (예: 1191pt) |
| display: flex | 필수 (변경 없음) |
| defineLayout | CUSTOM 크기 사용 시 convert.js에서 `pres.defineLayout()` 호출 필수 |

```javascript
// convert.js에서 CUSTOM 레이아웃 설정 예시
if (spec.presentation.layout === 'CUSTOM') {
    const w = spec.presentation.width_pt / 72;
    const h = spec.presentation.height_pt / 72;
    pptx.defineLayout({ name: 'CUSTOM', width: w, height: h });
    pptx.layout = 'CUSTOM';
}
```

> 비표준 body 크기 사용 시 validate_html.py는 `--mode wireframe` 플래그로 실행한다.

### 필수 body 속성

- `width`와 `height`는 반드시 명시해야 한다. 생략 시 변환이 올바르게 이루어지지 않는다.
- `display: flex`는 body에 반드시 선언해야 한다. 이것이 없으면 레이아웃 엔진이 작동하지 않는다.
- `DOCTYPE html` 선언은 파일 최상단에 위치해야 한다.
- `html`, `head`, `style`, `body` 태그는 모두 포함되어야 한다.

---

## 텍스트 규칙

### 허용되는 블록 텍스트 태그

텍스트는 반드시 아래 태그 중 하나 안에 있어야 한다.

| 태그 | 용도 |
|------|------|
| `p` | 일반 단락 텍스트 |
| `h1` | 최상위 제목 |
| `h2` | 2단계 제목 |
| `h3` | 3단계 제목 |
| `h4` | 4단계 제목 |
| `h5` | 5단계 제목 |
| `h6` | 6단계 제목 |
| `ul` | 순서 없는 리스트 |
| `ol` | 순서 있는 리스트 |

### 허용되는 인라인 포맷 태그

블록 태그 내부에서 사용 가능한 인라인 태그는 다음과 같다.

| 태그 | 효과 |
|------|------|
| `b` | 굵게 |
| `strong` | 굵게 (의미론적) |
| `i` | 기울임 |
| `em` | 기울임 (의미론적) |
| `u` | 밑줄 |
| `span` | 인라인 스타일 적용 |
| `br` | 줄 바꿈 |

### 금지 사항

**div에 직접 텍스트 삽입 — 절대 금지**

```html
<!-- 잘못된 예: div 안에 직접 텍스트 → 엔진이 SILENTLY IGNORE 처리 -->
<div style="...">
  이 텍스트는 슬라이드에 나타나지 않는다
</div>

<!-- 올바른 예: p 태그로 감싸야 함 -->
<div style="...">
  <p>이 텍스트는 정상적으로 표시된다</p>
</div>
```

**span에 직접 텍스트 삽입 (부모 텍스트 태그 없이) — 절대 금지**

```html
<!-- 잘못된 예: span이 div 바로 아래에 있어서 p/h 태그가 없음 → 무시됨 -->
<div>
  <span style="color: #FF0000;">이 텍스트도 무시된다</span>
</div>

<!-- 올바른 예: p 안에 span 사용 -->
<p>
  <span style="color: #FF0000;">이 텍스트는 빨간색으로 표시된다</span>
</p>
```

**수동 불릿 문자 사용 — 절대 금지**

```html
<!-- 잘못된 예: 수동으로 불릿 문자를 입력 -->
<p>• 항목 1</p>
<p>- 항목 2</p>
<p>* 항목 3</p>

<!-- 올바른 예: ul/li 태그 사용 -->
<ul>
  <li>항목 1</li>
  <li>항목 2</li>
  <li>항목 3</li>
</ul>
```

### span 지원 스타일

span 태그에 적용 가능한 CSS 속성은 다음으로 제한된다.

| CSS 속성 | 지원 여부 | 예시 |
|----------|----------|------|
| `font-weight: bold` | 지원 | `style="font-weight: bold"` |
| `font-style: italic` | 지원 | `style="font-style: italic"` |
| `text-decoration: underline` | 지원 | `style="text-decoration: underline"` |
| `color` | 지원 | `style="color: #FF0000"` |
| `margin` | **미지원** (무시됨) | 사용 불가 |
| `padding` | **미지원** (무시됨) | 사용 불가 |

---

## 폰트 규칙

### Web-safe 폰트 전체 목록

html2pptx 엔진은 web-safe 폰트만 정확히 렌더링한다. 아래 목록에 없는 폰트를 사용하면 폴백 처리되어 의도하지 않은 폰트로 대체된다.

| 폰트 이름 | 계열 |
|-----------|------|
| Arial | Sans-serif |
| Helvetica | Sans-serif |
| Verdana | Sans-serif |
| Tahoma | Sans-serif |
| Trebuchet MS | Sans-serif |
| Impact | Sans-serif |
| Comic Sans MS | Sans-serif |
| Times New Roman | Serif |
| Georgia | Serif |
| Courier New | Monospace |

### 비 web-safe 폰트 대체 표

비 web-safe 폰트를 사용하는 경우 아래 표를 참고하여 가장 유사한 web-safe 폰트로 반드시 대체해야 한다.

| 원본 폰트 | 대체 web-safe 폰트 | 이유 |
|----------|-------------------|------|
| Segoe UI | Arial | 유사한 sans-serif 계열 |
| SF Pro | Helvetica | Apple 계열 sans-serif 대안 |
| Roboto | Arial | 구글 sans-serif 대안 |
| Noto Sans | Arial | 범용 sans-serif 대안 |
| Malgun Gothic | Arial | 한국어 UI 폰트 대안 |
| Pretendard | Arial | 한국어 디자인 폰트 대안 |
| Inter | Arial | 모던 UI sans-serif 대안 |
| Open Sans | Arial | 웹 sans-serif 대안 |
| Lato | Arial | 슬림 sans-serif 대안 |
| Montserrat | Arial | 기하학적 sans-serif 대안 |
| Poppins | Arial | 모던 rounded sans-serif 대안 |

---

## 도형 및 배경 규칙

### background, border, box-shadow 적용 가능 태그

도형 스타일(배경색, 테두리, 그림자)은 반드시 `div` 태그에만 적용해야 한다.

```html
<!-- 올바른 예: div에 도형 스타일 적용 -->
<div style="
  background: #4A90D9;
  border: 2px solid #2C5F8A;
  border-radius: 8pt;
  box-shadow: 4px 4px 8px rgba(0,0,0,0.3);
  width: 200pt;
  height: 100pt;
">
  <p>도형 안의 텍스트</p>
</div>

<!-- 잘못된 예: p 태그에 배경 적용 → 무시됨 -->
<p style="background: #4A90D9;">이 배경은 적용되지 않는다</p>
```

### border-radius

- 일반 둥근 모서리: `border-radius: 8pt` (픽셀이 아닌 pt 단위 권장)
- 원형: `border-radius: 50%`

```html
<!-- 원형 도형 예시 -->
<div style="
  width: 100pt;
  height: 100pt;
  border-radius: 50%;
  background: #FF6B6B;
">
</div>
```

### box-shadow

외부 그림자만 지원된다. `inset` 키워드를 사용한 내부 그림자는 엔진이 무시한다.

```html
<!-- 지원: 외부 그림자 -->
<div style="box-shadow: 4px 4px 8px rgba(0,0,0,0.3);">...</div>

<!-- 미지원 (무시됨): inset 그림자 -->
<div style="box-shadow: inset 4px 4px 8px rgba(0,0,0,0.3);">...</div>
```

---

## 색상 규칙

CSS와 PptxGenJS API에서 색상 표기 형식이 다르다. 이 차이를 혼동하면 파일이 손상될 수 있다.

### CSS vs PptxGenJS 색상 형식 비교

| 컨텍스트 | # prefix | 예시 |
|----------|----------|------|
| HTML/CSS `style` 속성 | 필수 | `color: #FF0000` |
| PptxGenJS API 인수 | **절대 금지** | `color: 'FF0000'` |

### 예시 비교 테이블

| 상황 | 올바른 표기 | 잘못된 표기 |
|------|-----------|-----------|
| CSS에서 텍스트 색상 | `color: #1F2937` | `color: 1F2937` |
| CSS에서 배경 색상 | `background: #4A90D9` | `background: 4A90D9` |
| addText의 color 옵션 | `color: 'FF0000'` | `color: '#FF0000'` |
| addChart의 chartColors | `chartColors: ['FF0000', '00FF00']` | `chartColors: ['#FF0000', '#00FF00']` |
| addShape의 fill 색상 | `fill: { color: 'FF0000' }` | `fill: { color: '#FF0000' }` |

> PptxGenJS API에 # prefix를 포함한 색상을 전달하면 PPTX 파일이 손상되어 PowerPoint에서 열 수 없게 된다.

---

## 와이어프레임 색상 규칙

와이어프레임 모드에서는 아래 4가지 색상만 사용한다.

| 색상 | HEX | 용도 |
|------|-----|------|
| 검정 | `#000000` | 텍스트, 테두리, 배지 배경 |
| 회색 | `#808080` | 강조 배경 (버튼, 배너, 어두운 영역) |
| 연회색 | `#E0E0E0` | 섹션 배경, 비활성 영역 |
| 흰색 | `#FFFFFF` | 카드 배경, 콘텐츠 영역, 배지 텍스트 |

### 원본 색상 → 와이어프레임 매핑 규칙

| 원본 색상 유형 | 와이어프레임 대체 |
|--------------|----------------|
| 밝은 배경색 (L > 80%) | `#FFFFFF` 또는 `#E0E0E0` |
| 어두운/강조 배경색 (L ≤ 80%) | `#808080` |
| 텍스트 색상 (일반) | `#000000` |
| 어두운 배경 위 텍스트 | `#FFFFFF` |
| 모든 테두리 | `#000000` |

### 검증

```bash
python validate_html.py slides/ --mode wireframe
```

비허용 색상은 warning으로 보고된다 (error가 아님 — 엣지 케이스 고려).

### 모드 선택 가이드

| 항목 | wireframe | full_design |
|------|-----------|-------------|
| spec.json `design.mode` | `"wireframe"` | `"full_design"` |
| validate_html.py 옵션 | `--mode wireframe` | (기본값, 옵션 불필요) |
| body 크기 | spec.json의 `presentation.width_pt/height_pt` (CUSTOM) | 720pt × 405pt (16:9) |
| body 크기 검증 | CUSTOM 값 허용 (720×405 강제 아님) | 720×405 필수 |
| 색상 검증 | #000000/#808080/#E0E0E0/#FFFFFF만 허용 (warning) | 모든 #hex 색상 허용 |
| 슬라이드 수 | 1개 (slide_00.html) | 여러 개 (slide_00~NN.html) |
| defineLayout | 필수 (`pptx.defineLayout()` 호출) | 불필요 (LAYOUT_16x9 사용) |

---

## 그래디언트 및 아이콘 규칙

### CSS 그래디언트 — 절대 금지

```html
<!-- 절대 사용 불가: CSS gradient -->
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">...</div>
<div style="background: radial-gradient(circle, #f093fb 0%, #f5576c 100%);">...</div>
```

html2pptx 엔진은 CSS gradient를 처리할 수 없다. 사용하면 배경이 누락되거나 오류가 발생한다.

### 그래디언트 대체 방법

1. Sharp 라이브러리를 사용하여 그래디언트 SVG를 PNG로 래스터화한다.
2. 생성된 PNG 파일을 `img` 태그로 참조한다.

```javascript
// Sharp로 그래디언트 PNG 생성 예시
const sharp = require('sharp');
const svgBuffer = Buffer.from(`
  <svg width="720" height="405" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#667eea"/>
        <stop offset="100%" style="stop-color:#764ba2"/>
      </linearGradient>
    </defs>
    <rect width="720" height="405" fill="url(#grad)"/>
  </svg>
`);
await sharp(svgBuffer).png().toFile('gradient-bg.png');
```

```html
<!-- PNG로 변환 후 img 태그로 참조 -->
<img src="gradient-bg.png" style="width: 720pt; height: 405pt; position: absolute; top: 0; left: 0;" />
```

### 아이콘 처리

react-icons 또는 기타 SVG 아이콘도 동일한 방식으로 처리한다.

1. SVG 아이콘을 Sharp로 PNG 변환
2. `img` 태그로 참조

```javascript
// react-icons SVG → PNG 변환
const { renderToStaticMarkup } = require('react-dom/server');
const { FiCheck } = require('react-icons/fi');
const svgString = renderToStaticMarkup(FiCheck({ size: 48 }));
await sharp(Buffer.from(svgString)).png().toFile('icon-check.png');
```

---

## 이미지 규칙

이미지는 `img` 태그를 사용한다. 크기는 인라인 스타일로 pt 단위로 지정한다.

```html
<!-- 이미지 삽입 예시 -->
<img src="photo.jpg" style="width: 300pt; height: 200pt;" />
```

- `width`와 `height`를 명시하지 않으면 레이아웃이 의도하지 않게 동작할 수 있다.
- 파일 경로는 HTML 파일 기준 상대 경로 또는 절대 경로를 사용한다.

---

## 레이아웃 규칙

### display: flex 활용

html2pptx는 `display: flex`를 기반으로 레이아웃을 처리한다. 내부 요소 배치에도 flex를 사용한다.

```html
<!-- 2단 레이아웃 예시 -->
<body style="width: 720pt; height: 405pt; display: flex; flex-direction: row;">
  <div style="width: 340pt; height: 405pt; padding: 20pt;">
    <h2>왼쪽 제목</h2>
    <p>왼쪽 내용</p>
  </div>
  <div style="width: 340pt; height: 405pt; padding: 20pt;">
    <h2>오른쪽 제목</h2>
    <p>오른쪽 내용</p>
  </div>
</body>
```

### margin 사용

요소 간 간격은 `margin`을 사용한다. `padding`도 사용 가능하지만 div 기준이다.

---

## 차트 플레이스홀더

차트가 들어갈 영역은 `class="placeholder"` div로 표시한다. convert.js에서 이 위치에 addChart를 호출한다.

```html
<!-- 차트 플레이스홀더 -->
<div class="placeholder" id="chart-revenue"
  style="width: 400pt; height: 250pt; margin: 20pt;">
</div>
```

html2pptx 반환값의 `placeholders` 배열에서 id별 좌표(x, y, w, h)를 받아 addChart에 전달한다.

---

## 배지 CSS 클래스

와이어프레임 모드에서 각 UI 영역에 번호 배지를 표시한다.

```html
<div class="badge" style="position:absolute; left:{x}pt; top:{y}pt;">
  <p>{number}</p>
</div>
```

```css
.badge {
  position: absolute;
  width: 20pt; height: 20pt;
  background: #000000;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;  /* 필수: DOM 순서와 무관하게 최상위 렌더링 보장 */
}
.badge p {
  color: #ffffff;
  font-size: 9.75pt;
  font-weight: bold;
  margin: 0;
  text-align: center;
}
```

---

## 디스크립션 패널 HTML 구조

와이어프레임 모드에서 오른쪽에 화면 구성 설명 패널을 배치한다.

```html
<div style="position:absolute; left:{CONTENT_WIDTH}pt; top:0;
     width:275pt; height:{HEIGHT}pt; background:#ffffff;
     border-left:1pt solid #000000; padding:14pt; overflow:hidden;">
  <div style="border-bottom:2pt solid #000000; padding-bottom:6pt; margin-bottom:14pt;">
    <p style="font-size:12pt; font-weight:bold; color:#000000; margin:0;">화면 구성 설명</p>
  </div>
  <!-- 각 영역 설명 반복 -->
  <p style="font-size:10.5pt; font-weight:bold; color:#000000; margin:14pt 0 2pt 0;">1. {name}</p>
  <p style="font-size:9.75pt; color:#000000; margin:0 0 0 11pt;">{description}</p>
</div>
```

| 항목 | 값 |
|------|-----|
| 패널 폭 | 275pt |
| 위치 | 콘텐츠 영역 오른쪽 |
| 제목 | "화면 구성 설명" |
| 항목 번호 폰트 | 10.5pt bold |
| 설명 폰트 | 9.75pt |
| 구분선 | 2pt solid #000000 |

---

## 검증 체크리스트

HTML 작성 후 convert.js 실행 전에 아래 항목을 모두 확인한다.

- [ ] body에 `width`와 `height`가 지정되어 있는가
- [ ] body에 `display: flex`가 선언되어 있는가
- [ ] `<!DOCTYPE html>` 선언이 파일 최상단에 있는가
- [ ] 모든 텍스트가 `p`, `h1`~`h6`, `ul`/`ol` 태그 안에 있는가
- [ ] `div` 또는 루트 레벨 `span`에 직접 텍스트가 없는가
- [ ] `linear-gradient`, `radial-gradient` 등 CSS gradient가 없는가
- [ ] web-safe 폰트만 사용했는가 (비 web-safe는 대체 표 참조)
- [ ] 수동 불릿 문자(•, -, *)를 사용하지 않았는가
- [ ] 배경/테두리/그림자 스타일이 `div`에만 적용되었는가 (p/h 태그에 없는가)
- [ ] CSS 색상에 `#` prefix가 있는가
- [ ] 차트 플레이스홀더 `id`가 convert.js의 id와 일치하는가
- [ ] 모든 배지/마커 요소가 HTML body의 마지막에 위치하는가 (콘텐츠 섹션보다 뒤)
- [ ] 각 배지 위치가 고유한가 (동일 left/top 쌍 없음, 최소 24pt 간격)
- [ ] 오버레이 요소에 z-index ≥ 9999가 명시되어 있는가
