# PptxGenJS API 가이드

> convert.js 작성 시 참조하는 API 레퍼런스

---

## 기본 설정

### pptxgen 인스턴스 생성

```javascript
const PptxGenJS = require('pptxgenjs');
const pres = new PptxGenJS();
```

### layout 설정

슬라이드 비율은 pres.layout으로 설정한다. HTML body의 치수와 반드시 일치해야 한다.

| layout 값 | 비율 | body 치수 |
|-----------|------|----------|
| `'LAYOUT_16x9'` | 16:9 | 720pt x 405pt |
| `'LAYOUT_4x3'` | 4:3 | 720pt x 540pt |
| `'LAYOUT_16x10'` | 16:10 | 720pt x 450pt |
| `'LAYOUT_WIDE'` | 16:9 (와이드) | 별도 확인 필요 |
| `'CUSTOM'` | 자유 | 임의 pt 값 (`defineLayout()` 필수) |

### CUSTOM 레이아웃 (defineLayout)

표준 레이아웃에 없는 비표준 크기를 사용할 때 `defineLayout()`으로 커스텀 레이아웃을 정의한다.

```javascript
// pt → inches 변환: inches = pt / 72
const widthInches = 1684 / 72;   // ≈ 23.39"
const heightInches = 1191 / 72;  // ≈ 16.54"

pres.defineLayout({ name: 'CUSTOM', width: widthInches, height: heightInches });
pres.layout = 'CUSTOM';
```

| 항목 | 설명 |
|------|------|
| `name` | 레이아웃 이름 (문자열, 임의 지정 가능) |
| `width` | 슬라이드 너비 (**인치** 단위, pt가 아님) |
| `height` | 슬라이드 높이 (**인치** 단위, pt가 아님) |
| 변환 공식 | `inches = pt / 72` |

> defineLayout 호출 후 반드시 `pres.layout = 'CUSTOM'`으로 설정해야 적용된다.
> HTML body의 width/height(pt)와 defineLayout의 width/height(inches)가 일치해야 한다.

#### 사용 예시 — spec.json 기반 동적 설정

```javascript
const spec = JSON.parse(fs.readFileSync(
  path.join(__dirname, 'spec.json'), 'utf8'));

const pptx = new pptxgen();

if (spec.presentation.layout === 'CUSTOM') {
    const w = spec.presentation.width_pt / 72;
    const h = spec.presentation.height_pt / 72;
    pptx.defineLayout({ name: 'CUSTOM', width: w, height: h });
    pptx.layout = 'CUSTOM';
} else {
    pptx.layout = spec.presentation.layout;
}
```

```javascript
// 16:9 설정 예시
pres.layout = 'LAYOUT_16x9';

// 메타데이터 설정 (선택사항)
pres.author = '작성자 이름';
pres.title = '프레젠테이션 제목';
pres.subject = '프레젠테이션 주제';
```

> layout 불일치 시 슬라이드 요소가 잘리거나 위치가 틀어진다.

---

## html2pptx 함수

### 함수 시그니처

```javascript
const { html2pptx } = require('./engine/html2pptx');

const result = await html2pptx(htmlFile, pres, options);
```

### 파라미터 상세

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| `htmlFile` | string | 필수 | 변환할 HTML 파일의 절대 경로 또는 상대 경로 |
| `pres` | PptxGenJS | 필수 | layout이 설정된 pptxgen 인스턴스 |
| `options` | object | 선택 | 추가 옵션 객체 |
| `options.tmpDir` | string | 선택 | 임시 파일 저장 디렉토리 경로 (기본값: 시스템 temp) |
| `options.slide` | object | 선택 | 기존 슬라이드 객체. 미전달 시 새 슬라이드 자동 생성 |

### 반환값

```javascript
{
  slide: object,           // PptxGenJS 슬라이드 객체
  placeholders: [          // class="placeholder" div 목록
    {
      id: 'chart-revenue', // placeholder의 id 속성 값
      x: 0.5,              // 인치 단위 X 좌표
      y: 1.2,              // 인치 단위 Y 좌표
      w: 5.5,              // 인치 단위 너비
      h: 3.4               // 인치 단위 높이
    }
  ]
}
```

### 사용 예시 — 단일 슬라이드

```javascript
const PptxGenJS = require('pptxgenjs');
const { html2pptx } = require('./engine/html2pptx');
const path = require('path');

async function createPresentation() {
  const pres = new PptxGenJS();
  pres.layout = 'LAYOUT_16x9';

  const htmlFile = path.join(__dirname, 'slides', 'slide1.html');
  const { slide, placeholders } = await html2pptx(htmlFile, pres, {
    tmpDir: path.join(__dirname, 'tmp')
  });

  // 플레이스홀더에 차트 추가
  const chartPlaceholder = placeholders.find(p => p.id === 'chart-main');
  if (chartPlaceholder) {
    slide.addChart(pres.ChartType.BAR, chartData, {
      x: chartPlaceholder.x,
      y: chartPlaceholder.y,
      w: chartPlaceholder.w,
      h: chartPlaceholder.h
    });
  }

  await pres.writeFile({ fileName: 'output.pptx' });
}
```

### 사용 예시 — 멀티 슬라이드

```javascript
async function createMultiSlidePresentation() {
  const pres = new PptxGenJS();
  pres.layout = 'LAYOUT_16x9';

  const slideFiles = [
    'slides/title.html',
    'slides/content1.html',
    'slides/content2.html',
    'slides/summary.html'
  ];

  for (const htmlFile of slideFiles) {
    const { slide, placeholders } = await html2pptx(
      path.join(__dirname, htmlFile),
      pres,
      { tmpDir: path.join(__dirname, 'tmp') }
    );

    // 각 슬라이드별 플레이스홀더 처리
    for (const ph of placeholders) {
      await addChartToPlaceholder(slide, ph, pres);
    }
  }

  await pres.writeFile({ fileName: 'multi-slide-output.pptx' });
}
```

---

## 차트 추가 (addChart)

> 색상 배열 `chartColors`에 절대로 `#` prefix를 포함하지 않는다.

### BAR 차트 — 수직 단일 시리즈

```javascript
const barData = [
  {
    name: '매출',
    labels: ['1월', '2월', '3월', '4월', '5월'],
    values: [120, 150, 180, 140, 200]
  }
];

slide.addChart(pres.ChartType.BAR, barData, {
  x: 0.5,
  y: 1.0,
  w: 8.0,
  h: 4.5,
  barDir: 'col',          // 'col' = 수직, 'bar' = 수평
  showTitle: true,
  title: '월별 매출 현황',
  showLegend: true,
  legendPos: 'b',         // 'b'=하단, 't'=상단, 'l'=좌측, 'r'=우측
  chartColors: ['4A90D9'],
  showValue: true,
  dataLabelFontSize: 10
});
```

### BAR 차트 — 수평 다중 시리즈

```javascript
const multiBarData = [
  {
    name: '2024년',
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    values: [300, 350, 400, 450]
  },
  {
    name: '2025년',
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    values: [320, 380, 420, 500]
  }
];

slide.addChart(pres.ChartType.BAR, multiBarData, {
  x: 0.5,
  y: 1.0,
  w: 8.0,
  h: 4.5,
  barDir: 'bar',          // 수평 막대
  barGrouping: 'clustered', // 'clustered'=묶음, 'stacked'=누적
  showTitle: true,
  title: '연도별 분기 실적 비교',
  showLegend: true,
  legendPos: 'b',
  chartColors: ['4A90D9', 'E74C3C'],
  showCatAxisTitle: true,
  catAxisTitle: '분기',
  showValAxisTitle: true,
  valAxisTitle: '매출 (만원)'
});
```

### LINE 차트 — 직선 단일 시리즈

```javascript
const lineData = [
  {
    name: '방문자 수',
    labels: ['1월', '2월', '3월', '4월', '5월', '6월'],
    values: [1200, 1500, 1350, 1800, 2100, 1950]
  }
];

slide.addChart(pres.ChartType.LINE, lineData, {
  x: 0.5,
  y: 1.0,
  w: 8.0,
  h: 4.5,
  lineDataSymbol: 'circle',  // 'circle', 'square', 'triangle', 'none'
  lineSize: 2,
  showTitle: true,
  title: '월별 방문자 추이',
  showLegend: false,
  chartColors: ['27AE60']
});
```

### LINE 차트 — 다중 시리즈

```javascript
const multiLineData = [
  {
    name: '제품 A',
    labels: ['1월', '2월', '3월', '4월', '5월'],
    values: [100, 120, 115, 140, 160]
  },
  {
    name: '제품 B',
    labels: ['1월', '2월', '3월', '4월', '5월'],
    values: [80, 95, 110, 105, 130]
  }
];

slide.addChart(pres.ChartType.LINE, multiLineData, {
  x: 0.5,
  y: 1.0,
  w: 8.0,
  h: 4.5,
  showTitle: true,
  title: '제품별 판매 추이',
  showLegend: true,
  legendPos: 'b',
  chartColors: ['4A90D9', 'E74C3C']
});
```

### PIE 차트

PIE 차트는 단일 시리즈만 지원한다. 시리즈를 2개 이상 전달하면 첫 번째 시리즈만 사용된다.

```javascript
const pieData = [
  {
    name: '시장 점유율',
    labels: ['제품 A', '제품 B', '제품 C', '기타'],
    values: [45, 25, 20, 10]
  }
];

slide.addChart(pres.ChartType.PIE, pieData, {
  x: 1.5,
  y: 0.8,
  w: 6.0,
  h: 4.5,
  showTitle: true,
  title: '제품별 시장 점유율',
  showLegend: true,
  legendPos: 'r',
  showPercent: true,        // 퍼센트 라벨 표시
  dataLabelFontSize: 12,
  chartColors: ['4A90D9', 'E74C3C', '27AE60', 'F39C12']
});
```

### SCATTER 차트

SCATTER 차트는 특수한 데이터 형식을 사용한다. 첫 번째 시리즈가 X축 값이 되고, 이후 시리즈가 Y축 데이터가 된다.

```javascript
// 첫 번째 시리즈: X값 (values가 X 좌표)
// 두 번째 시리즈 이후: Y값 (values가 Y 좌표)
const scatterData = [
  {
    name: 'X축',
    values: [1, 2, 3, 4, 5, 6, 7, 8]  // X 좌표
  },
  {
    name: '데이터 A',
    values: [2.5, 3.1, 4.8, 4.2, 6.1, 5.8, 7.2, 8.0]  // Y 좌표
  }
];

slide.addChart(pres.ChartType.SCATTER, scatterData, {
  x: 0.5,
  y: 1.0,
  w: 8.0,
  h: 4.5,
  showTitle: true,
  title: '상관관계 분석',
  showLegend: true,
  lineSize: 0,              // 선 없이 점만 표시
  chartColors: ['4A90D9'],
  showCatAxisTitle: true,
  catAxisTitle: 'X 변수',
  showValAxisTitle: true,
  valAxisTitle: 'Y 변수'
});
```

### 공통 차트 옵션

| 옵션 | 타입 | 설명 |
|------|------|------|
| `x` | number | X 좌표 (인치) |
| `y` | number | Y 좌표 (인치) |
| `w` | number | 너비 (인치) |
| `h` | number | 높이 (인치) |
| `showTitle` | boolean | 차트 제목 표시 여부 |
| `title` | string | 차트 제목 텍스트 |
| `showLegend` | boolean | 범례 표시 여부 |
| `legendPos` | string | 범례 위치: 'b', 't', 'l', 'r' |
| `chartColors` | string[] | 데이터 시리즈 색상 (# 없이) |
| `showValue` | boolean | 데이터 값 라벨 표시 |
| `dataLabelFontSize` | number | 데이터 라벨 폰트 크기 |
| `showCatAxisTitle` | boolean | 카테고리 축 제목 표시 |
| `catAxisTitle` | string | 카테고리 축 제목 텍스트 |
| `showValAxisTitle` | boolean | 값 축 제목 표시 |
| `valAxisTitle` | string | 값 축 제목 텍스트 |
| `valAxisMinVal` | number | 값 축 최솟값 |
| `valAxisMaxVal` | number | 값 축 최댓값 |

---

## 이미지 추가 (addImage)

### 파일 경로로 추가

```javascript
slide.addImage({
  path: '/absolute/path/to/image.png',
  x: 0.5,
  y: 0.5,
  w: 4.0,
  h: 3.0
});
```

### Base64 데이터로 추가

```javascript
const fs = require('fs');
const imageBuffer = fs.readFileSync('/path/to/image.png');
const base64Data = imageBuffer.toString('base64');

slide.addImage({
  data: `image/png;base64,${base64Data}`,
  x: 0.5,
  y: 0.5,
  w: 4.0,
  h: 3.0
});
```

### 비율 계산 방법

원본 이미지의 비율을 유지하면서 너비를 기준으로 높이를 계산하는 방법이다.

```javascript
const sharp = require('sharp');

async function getImageDimensions(imagePath) {
  const metadata = await sharp(imagePath).metadata();
  return { width: metadata.width, height: metadata.height };
}

async function addImageKeepRatio(slide, imagePath, x, y, targetWidth) {
  const { width, height } = await getImageDimensions(imagePath);
  const ratio = height / width;
  const targetHeight = targetWidth * ratio;

  slide.addImage({
    path: imagePath,
    x,
    y,
    w: targetWidth,
    h: targetHeight
  });
}
```

---

## 텍스트 추가 (addText)

### 단순 텍스트

```javascript
slide.addText('슬라이드 제목', {
  x: 0.5,
  y: 0.3,
  w: 9.0,
  h: 0.8,
  fontSize: 32,
  bold: true,
  color: '1F2937',    // # 없이
  align: 'left',
  valign: 'middle'
});
```

### 리치 텍스트 (텍스트 배열)

여러 서식이 혼합된 텍스트는 배열 형식으로 전달한다.

```javascript
slide.addText(
  [
    { text: '중요: ', options: { bold: true, color: 'E74C3C' } },
    { text: '이 내용은 반드시 확인하세요. ', options: { color: '1F2937' } },
    { text: '(출처: 2025 보고서)', options: { italic: true, color: '6B7280', fontSize: 10 } }
  ],
  {
    x: 0.5,
    y: 1.5,
    w: 9.0,
    h: 1.0,
    fontSize: 14,
    align: 'left',
    valign: 'top',
    wrap: true
  }
);
```

### addText 주요 옵션

| 옵션 | 타입 | 설명 |
|------|------|------|
| `x` | number | X 좌표 (인치) |
| `y` | number | Y 좌표 (인치) |
| `w` | number | 너비 (인치) |
| `h` | number | 높이 (인치) |
| `fontSize` | number | 폰트 크기 (pt) |
| `color` | string | 텍스트 색상 (# 없이) |
| `bold` | boolean | 굵게 여부 |
| `italic` | boolean | 기울임 여부 |
| `underline` | boolean | 밑줄 여부 |
| `align` | string | 수평 정렬: 'left', 'center', 'right' |
| `valign` | string | 수직 정렬: 'top', 'middle', 'bottom' |
| `fontFace` | string | 폰트 이름 |
| `wrap` | boolean | 텍스트 줄 바꿈 여부 |
| `lineSpacingMultiple` | number | 줄 간격 배수 |

---

## 도형 추가 (addShape)

### RECTANGLE (직사각형)

```javascript
slide.addShape(pres.ShapeType.RECT, {
  x: 0.5,
  y: 0.5,
  w: 4.0,
  h: 2.0,
  fill: { color: '4A90D9' },
  line: { color: '2C5F8A', width: 2 }
});
```

### OVAL (타원/원)

```javascript
slide.addShape(pres.ShapeType.ELLIPSE, {
  x: 1.0,
  y: 1.0,
  w: 2.0,
  h: 2.0,         // w == h이면 원
  fill: { color: 'FF6B6B' },
  line: { color: 'C0392B', width: 1 }
});
```

### ROUNDED_RECTANGLE (둥근 직사각형)

```javascript
slide.addShape(pres.ShapeType.ROUND_RECT, {
  x: 0.5,
  y: 0.5,
  w: 4.0,
  h: 1.5,
  rectRadius: 0.1,    // 0~0.5 사이 값, 값이 클수록 더 둥글어짐
  fill: { color: '27AE60' },
  line: { color: '1E8449', width: 1 }
});
```

### 도형에 텍스트 겹치기

도형 위에 텍스트를 배치할 때는 별도의 addText를 도형과 동일한 좌표에 겹쳐서 추가한다.

```javascript
// 도형
slide.addShape(pres.ShapeType.ROUND_RECT, {
  x: 2.0, y: 1.5, w: 3.0, h: 0.8,
  fill: { color: '4A90D9' }
});

// 텍스트 (동일 좌표에 겹침)
slide.addText('버튼 텍스트', {
  x: 2.0, y: 1.5, w: 3.0, h: 0.8,
  align: 'center', valign: 'middle',
  color: 'FFFFFF', fontSize: 14, bold: true
});
```

---

## 테이블 추가 (addTable)

### 기본 테이블

```javascript
const tableData = [
  // 헤더 행
  [
    { text: '항목', options: { bold: true, fill: { color: '4A90D9' }, color: 'FFFFFF' } },
    { text: '2024년', options: { bold: true, fill: { color: '4A90D9' }, color: 'FFFFFF' } },
    { text: '2025년', options: { bold: true, fill: { color: '4A90D9' }, color: 'FFFFFF' } }
  ],
  // 데이터 행
  [
    { text: '매출' },
    { text: '1,200만원' },
    { text: '1,500만원' }
  ],
  [
    { text: '비용' },
    { text: '800만원' },
    { text: '950만원' }
  ],
  [
    { text: '순이익' },
    { text: '400만원' },
    { text: '550만원' }
  ]
];

slide.addTable(tableData, {
  x: 0.5,
  y: 1.0,
  w: 9.0,
  colW: [3.0, 3.0, 3.0],   // 각 열 너비 (인치)
  rowH: 0.4,                // 각 행 높이 (인치)
  border: { type: 'solid', color: 'CCCCCC', pt: 1 },
  fontSize: 12,
  align: 'center',
  valign: 'middle'
});
```

### 스타일 테이블 (셀별 포맷)

```javascript
const styledTableData = [
  [
    { text: '구분', options: { bold: true, align: 'center', fill: { color: '1F2937' }, color: 'FFFFFF', fontSize: 13 } },
    { text: '내용', options: { bold: true, align: 'center', fill: { color: '1F2937' }, color: 'FFFFFF', fontSize: 13 } }
  ],
  [
    { text: '목표', options: { align: 'left', fill: { color: 'EBF5FB' }, bold: true } },
    { text: '연간 매출 20% 성장 달성', options: { align: 'left', fill: { color: 'EBF5FB' } } }
  ],
  [
    { text: '전략', options: { align: 'left', bold: true } },
    { text: '신시장 진출 및 기존 고객 강화', options: { align: 'left' } }
  ]
];

slide.addTable(styledTableData, {
  x: 0.5,
  y: 1.2,
  w: 9.0,
  colW: [2.5, 6.5],
  rowH: 0.5,
  border: { type: 'solid', color: 'D5D8DC', pt: 1 },
  fontSize: 12
});
```

### 병합 셀 (colspan)

```javascript
const mergedTableData = [
  [
    { text: '분류', options: { bold: true, align: 'center' } },
    { text: '상반기 실적', options: { bold: true, align: 'center', colspan: 2 } },  // 2열 병합
    { text: '하반기 실적', options: { bold: true, align: 'center', colspan: 2 } }   // 2열 병합 (실제 셀 수 맞춤)
  ],
  [
    { text: '제품 A', options: { align: 'center' } },
    { text: 'Q1: 300', options: { align: 'right' } },
    { text: 'Q2: 350', options: { align: 'right' } },
    { text: 'Q3: 380', options: { align: 'right' } },
    { text: 'Q4: 420', options: { align: 'right' } }
  ]
];
```

### addTable 주요 옵션

| 옵션 | 타입 | 설명 |
|------|------|------|
| `x` | number | X 좌표 (인치) |
| `y` | number | Y 좌표 (인치) |
| `w` | number | 테이블 전체 너비 (인치) |
| `colW` | number[] | 각 열의 너비 배열 (인치) |
| `rowH` | number | 기본 행 높이 (인치) |
| `border` | object | 테두리: `{ type, color, pt }` |
| `fill` | object | 기본 셀 배경: `{ color }` |
| `fontSize` | number | 기본 폰트 크기 |
| `align` | string | 기본 수평 정렬 |
| `valign` | string | 기본 수직 정렬 |
| `autoPage` | boolean | 내용이 넘칠 때 자동 페이지 분할 |

---

## 파일 저장

### 기본 저장

```javascript
await pres.writeFile({ fileName: 'output.pptx' });
```

### 절대 경로로 저장

```javascript
const path = require('path');

await pres.writeFile({
  fileName: path.join(__dirname, 'output', 'presentation.pptx')
});
```

### 상대 경로로 저장

```javascript
// 현재 작업 디렉토리 기준 상대 경로
await pres.writeFile({ fileName: './dist/presentation.pptx' });
```

> 출력 디렉토리가 존재하지 않으면 오류가 발생한다. 저장 전에 디렉토리를 생성해야 한다.

```javascript
const fs = require('fs');
const outputDir = path.join(__dirname, 'output');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}
await pres.writeFile({ fileName: path.join(outputDir, 'presentation.pptx') });
```

---

## placeholder 활용 패턴

html2pptx가 반환하는 placeholders 배열을 사용하여 차트를 정확한 위치에 배치한다.

```javascript
const { slide, placeholders } = await html2pptx(htmlFile, pres, { tmpDir });

// id로 특정 placeholder 찾기
const revenueChart = placeholders.find(ph => ph.id === 'chart-revenue');
const pieChart = placeholders.find(ph => ph.id === 'chart-share');

if (revenueChart) {
  slide.addChart(pres.ChartType.BAR, revenueData, {
    x: revenueChart.x,
    y: revenueChart.y,
    w: revenueChart.w,
    h: revenueChart.h,
    showTitle: true,
    title: '매출 현황',
    chartColors: ['4A90D9', '27AE60']
  });
}

if (pieChart) {
  slide.addChart(pres.ChartType.PIE, pieData, {
    x: pieChart.x,
    y: pieChart.y,
    w: pieChart.w,
    h: pieChart.h,
    showPercent: true,
    chartColors: ['4A90D9', 'E74C3C', '27AE60', 'F39C12']
  });
}
```

---

## 주의사항

**색상에 # prefix 절대 금지**

PptxGenJS API의 모든 color 옵션에 `#` 기호를 포함하면 PPTX 파일이 손상되어 PowerPoint에서 열 수 없게 된다. 이것은 가장 흔한 오류 원인이다.

```javascript
// 올바른 예
slide.addText('텍스트', { color: 'FF0000' });
slide.addShape(pres.ShapeType.RECT, { fill: { color: '4A90D9' } });
slide.addChart(pres.ChartType.BAR, data, { chartColors: ['FF0000', '00FF00'] });

// 잘못된 예 — 파일 손상 발생
slide.addText('텍스트', { color: '#FF0000' });
slide.addShape(pres.ShapeType.RECT, { fill: { color: '#4A90D9' } });
slide.addChart(pres.ChartType.BAR, data, { chartColors: ['#FF0000', '#00FF00'] });
```

**layout과 HTML body 치수 일치 필수**

pres.layout 설정과 HTML body의 width/height 치수가 일치하지 않으면 요소 위치가 틀어진다.

```javascript
// LAYOUT_16x9 사용 시 HTML body도 반드시 720pt x 405pt
pres.layout = 'LAYOUT_16x9';
// HTML: body { width: 720pt; height: 405pt; }
```

**PIE 차트 단일 시리즈 제한**

PIE 차트에 여러 시리즈를 전달해도 첫 번째 시리즈만 렌더링된다. 여러 카테고리를 비교하려면 BAR 차트를 사용한다.

**SCATTER 차트 데이터 형식**

SCATTER 차트의 첫 번째 시리즈는 반드시 X축 값이어야 한다. 일반 BAR/LINE처럼 labels를 사용하지 않는다.
