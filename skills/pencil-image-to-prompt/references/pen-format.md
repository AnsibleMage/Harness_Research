# .pen 포맷 레퍼런스

Pencil 프롬프트 작성 시 참조하는 .pen 파일의 상세 구조.
이 문서는 프롬프트 생성 중 구체적인 속성명이나 타입 확인이 필요할 때 참조한다.

---

## 목차

1. [오브젝트 기본 구조](#오브젝트-기본-구조)
2. [레이아웃 시스템](#레이아웃-시스템)
3. [그래픽 속성](#그래픽-속성)
4. [컴포넌트와 인스턴스](#컴포넌트와-인스턴스)
5. [슬롯](#슬롯)
6. [변수와 테마](#변수와-테마)
7. [오브젝트 타입별 속성](#오브젝트-타입별-속성)

---

## 오브젝트 기본 구조

.pen 파일은 JSON 기반 오브젝트 트리다. 각 오브젝트의 필수/공통 속성:

```
id        (필수) 고유 문자열. 슬래시(/) 포함 불가.
type      (필수) 오브젝트 타입
name      (선택) 표시용 이름
x, y      위치. 부모 좌상단 기준. 부모가 flexbox layout이면 무시됨.
width, height  크기. 고정값 또는 SizingBehavior(fit_content, fill_container)
rotation  도 단위, 반시계방향
opacity   0~1
enabled   boolean, 활성화 여부
reusable  true로 설정하면 재사용 가능 컴포넌트
theme     테마 설정 객체
```

---

## 레이아웃 시스템

frame과 group에서 사용하는 flexbox 스타일 레이아웃:

```
layout          "none" | "vertical" | "horizontal" (frame 기본: horizontal)
gap             자식 간 간격 (기본: 0)
padding         [전체] 또는 [수평, 수직] 또는 [top, right, bottom, left]
justifyContent  "start" | "center" | "end" | "space_between" | "space_around"
alignItems      "start" | "center" | "end"
```

**크기 지정 (SizingBehavior)**:
- `fit_content` — 자식 크기에 맞춤. 괄호 안에 fallback 가능: `fit_content(100)`
- `fill_container` — 부모 크기에 맞춤. 괄호 안에 fallback 가능: `fill_container(200)`

---

## 그래픽 속성

### Fill (채우기)

단일 또는 배열로 여러 개 중첩 가능:

```
단색:     "#FF0000" 또는 "#FF0000FF" (RGBA)
변수:     "$color.primary"
그라디언트: { type: "gradient", gradientType: "linear"|"radial"|"angular", colors: [{color, position}], rotation, center, size }
이미지:    { type: "image", url: "상대경로", mode: "stretch"|"fill"|"fit" }
메시:     { type: "mesh_gradient", columns, rows, colors, points }
```

### Stroke (선)

```
align:       "inside" | "center" | "outside"
thickness:   숫자 또는 { top, right, bottom, left }
join:        "miter" | "bevel" | "round"
cap:         "none" | "round" | "square"
dashPattern: [숫자 배열]
fill:        Fill과 동일 (단색, 그라디언트 등)
```

### Effect (효과)

단일 또는 배열:

```
블러:       { type: "blur", radius }
배경블러:   { type: "background_blur", radius }
그림자:     { type: "shadow", shadowType: "inner"|"outer", offset: {x,y}, spread, blur, color }
```

---

## 컴포넌트와 인스턴스

### 컴포넌트 정의

```json
{
  "id": "my-button",
  "type": "frame",
  "reusable": true,
  "children": [
    { "id": "label", "type": "text", "content": "Click" }
  ]
}
```

### 인스턴스 생성 (ref)

```json
{
  "id": "submit-btn",
  "type": "ref",
  "ref": "my-button"
}
```

### 속성 오버라이드 (descendants)

```json
{
  "id": "cancel-btn",
  "type": "ref",
  "ref": "my-button",
  "fill": "#FF0000",
  "descendants": {
    "label": { "content": "Cancel", "fill": "#FFFFFF" }
  }
}
```

### 중첩 인스턴스의 하위 요소 커스터마이징

슬래시(/)로 경로 표기:

```json
{
  "descendants": {
    "ok-button/label": { "content": "Save" },
    "cancel-button/label": { "content": "Discard" }
  }
}
```

### 오브젝트 교체

descendants에서 type을 포함하면 완전 교체:

```json
{
  "descendants": {
    "label": {
      "id": "icon",
      "type": "icon_font",
      "iconFontFamily": "lucide",
      "iconFontName": "check"
    }
  }
}
```

### children 교체

```json
{
  "descendants": {
    "content": {
      "children": [
        { "id": "item-1", "type": "ref", "ref": "menu-item" },
        { "id": "item-2", "type": "ref", "ref": "menu-item" }
      ]
    }
  }
}
```

---

## 슬롯

frame에 slot 속성을 설정하면 인스턴스에서 children 교체가 의도된 영역이 됨:

```json
{
  "id": "content-area",
  "type": "frame",
  "slot": ["card-component", "list-item"]
}
```

slot 배열의 각 요소는 해당 슬롯에 삽입하기 권장되는 reusable 컴포넌트의 id.

---

## 변수와 테마

### 변수 정의

```json
{
  "variables": {
    "color.primary": { "type": "color", "value": "#3b82f6" },
    "spacing.md": { "type": "number", "value": 16 },
    "is.visible": { "type": "boolean", "value": true },
    "label.text": { "type": "string", "value": "Hello" }
  }
}
```

사용: `"fill": "$color.primary"`, `"gap": "$spacing.md"`

### 테마별 변수값

```json
{
  "variables": {
    "color.background": {
      "type": "color",
      "value": [
        { "value": "#FFFFFF", "theme": { "mode": "light" } },
        { "value": "#000000", "theme": { "mode": "dark" } }
      ]
    }
  },
  "themes": {
    "mode": ["light", "dark"]
  }
}
```

테마 축의 첫 번째 값이 기본값. 오브젝트에 `"theme": { "mode": "dark" }` 설정하면 하위 전체에 적용.

---

## 오브젝트 타입별 속성

### frame
컨테이너. children 가능, 레이아웃 가능, fill/stroke/effect, cornerRadius, clip(오버플로우 숨김).

### rectangle
사각형. fill/stroke/effect, cornerRadius (단일 또는 [TL, TR, BR, BL]).

### ellipse
타원. innerRadius(도넛), startAngle, sweepAngle(호).

### text
텍스트. content(문자열 또는 TextStyle 배열), fontFamily, fontSize, fontWeight, letterSpacing, lineHeight, textAlign(left/center/right/justify), textAlignVertical(top/middle/bottom), textGrowth(auto/fixed-width/fixed-width-height). **textGrowth를 설정해야 width/height가 동작함.**

### line
선. 바운딩 박스의 위치와 크기로 정의.

### polygon
정다각형. polygonCount(변 수), cornerRadius.

### path
SVG 패스. geometry(SVG path 문자열), fillRule(nonzero/evenodd).

### group
그룹. children 가능, 레이아웃 가능. fill/stroke 없음(effect만 가능).

### icon_font
아이콘. iconFontFamily + iconFontName. 지원 폰트: lucide, feather, Material Symbols Outlined, Material Symbols Rounded, Material Symbols Sharp, phosphor. weight(100~700, 가변 폰트용).

### ref
인스턴스. ref(참조할 컴포넌트 id), descendants(오버라이드).

### note
메모. 캔버스에 표시되는 노트.

### prompt
AI 프롬프트 오브젝트. content, model 속성.

### context
컨텍스트 정보 오브젝트. content 속성.
