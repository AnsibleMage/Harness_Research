# axe-core 룰 → KWCAG 2.2 매핑

## 매핑 JSON

Tier 2 스크립트(`kwcag-axe-check.js`)에서 사용하는 매핑 데이터.
axe-core 위반 결과를 KWCAG 요구사항 번호로 변환한다.

```json
{
  "image-alt": {
    "kwcag": "5.1.1",
    "name": "적절한 대체 텍스트 제공",
    "principle": "인식의 용이성",
    "severity": "critical",
    "fix": "이미지에 적절한 alt 속성을 추가하세요."
  },
  "area-alt": {
    "kwcag": "5.1.1",
    "name": "적절한 대체 텍스트 제공",
    "principle": "인식의 용이성",
    "severity": "critical",
    "fix": "이미지맵 <area>에 alt 속성을 추가하세요."
  },
  "input-image-alt": {
    "kwcag": "5.1.1",
    "name": "적절한 대체 텍스트 제공",
    "principle": "인식의 용이성",
    "severity": "critical",
    "fix": "이미지 버튼에 alt 속성을 추가하세요."
  },
  "role-img-alt": {
    "kwcag": "5.1.1",
    "name": "적절한 대체 텍스트 제공",
    "principle": "인식의 용이성",
    "severity": "critical",
    "fix": "role=\"img\" 요소에 aria-label 또는 aria-labelledby를 추가하세요."
  },
  "svg-img-alt": {
    "kwcag": "5.1.1",
    "name": "적절한 대체 텍스트 제공",
    "principle": "인식의 용이성",
    "severity": "critical",
    "fix": "SVG 이미지에 <title> 또는 aria-label을 추가하세요."
  },
  "object-alt": {
    "kwcag": "5.1.1",
    "name": "적절한 대체 텍스트 제공",
    "principle": "인식의 용이성",
    "severity": "critical",
    "fix": "<object>에 대체 텍스트를 제공하세요."
  },
  "video-caption": {
    "kwcag": "5.2.1",
    "name": "자막 제공",
    "principle": "인식의 용이성",
    "severity": "major",
    "fix": "<video>에 <track kind=\"captions\">을 추가하세요."
  },
  "th-has-data-cells": {
    "kwcag": "5.3.1",
    "name": "표의 구성",
    "principle": "인식의 용이성",
    "severity": "major",
    "fix": "표 제목 셀(<th>)이 데이터 셀과 올바르게 연결되도록 하세요."
  },
  "td-headers-attr": {
    "kwcag": "5.3.1",
    "name": "표의 구성",
    "principle": "인식의 용이성",
    "severity": "major",
    "fix": "<td>의 headers 속성이 올바른 <th> id를 참조하도록 수정하세요."
  },
  "table-duplicate-name": {
    "kwcag": "5.3.1",
    "name": "표의 구성",
    "principle": "인식의 용이성",
    "severity": "minor",
    "fix": "표의 caption과 summary가 중복되지 않도록 수정하세요."
  },
  "heading-order": {
    "kwcag": "5.3.2",
    "name": "콘텐츠의 선형구조",
    "principle": "인식의 용이성",
    "severity": "minor",
    "fix": "제목 수준을 순차적으로 사용하세요 (h1 → h2 → h3)."
  },
  "list": {
    "kwcag": "5.3.2",
    "name": "콘텐츠의 선형구조",
    "principle": "인식의 용이성",
    "severity": "major",
    "fix": "목록 요소를 올바르게 구성하세요 (<ul>/<ol> 안에 <li>)."
  },
  "listitem": {
    "kwcag": "5.3.2",
    "name": "콘텐츠의 선형구조",
    "principle": "인식의 용이성",
    "severity": "major",
    "fix": "<li>는 반드시 <ul> 또는 <ol> 안에 있어야 합니다."
  },
  "definition-list": {
    "kwcag": "5.3.2",
    "name": "콘텐츠의 선형구조",
    "principle": "인식의 용이성",
    "severity": "major",
    "fix": "<dl> 안에는 <dt>와 <dd>만 사용하세요."
  },
  "dlitem": {
    "kwcag": "5.3.2",
    "name": "콘텐츠의 선형구조",
    "principle": "인식의 용이성",
    "severity": "major",
    "fix": "<dt>와 <dd>는 <dl> 안에 있어야 합니다."
  },
  "color-contrast": {
    "kwcag": "5.4.3",
    "name": "텍스트 콘텐츠의 명도 대비",
    "principle": "인식의 용이성",
    "severity": "major",
    "fix": "텍스트와 배경 간 명도 대비를 4.5:1 이상으로 조정하세요 (큰 텍스트는 3:1)."
  },
  "color-contrast-enhanced": {
    "kwcag": "5.4.3",
    "name": "텍스트 콘텐츠의 명도 대비",
    "principle": "인식의 용이성",
    "severity": "minor",
    "fix": "향상된 명도 대비 7:1을 권장합니다."
  },
  "scrollable-region-focusable": {
    "kwcag": "6.1.1",
    "name": "키보드 사용 보장",
    "principle": "운용의 용이성",
    "severity": "critical",
    "fix": "스크롤 가능한 영역이 키보드로 접근 가능하도록 tabindex를 추가하세요."
  },
  "nested-interactive": {
    "kwcag": "6.1.1",
    "name": "키보드 사용 보장",
    "principle": "운용의 용이성",
    "severity": "critical",
    "fix": "대화형 요소를 중첩하지 마세요 (예: <a> 안에 <button>)."
  },
  "tabindex": {
    "kwcag": "6.1.2",
    "name": "초점 이동과 표시",
    "principle": "운용의 용이성",
    "severity": "major",
    "fix": "tabindex 값이 0보다 큰 경우 제거하세요. tabindex=\"0\" 또는 자연 포커스 순서를 사용하세요."
  },
  "target-size": {
    "kwcag": "6.1.3",
    "name": "조작 가능",
    "principle": "운용의 용이성",
    "severity": "major",
    "fix": "터치 대상의 크기를 최소 24x24 CSS 픽셀로 조정하세요."
  },
  "bypass": {
    "kwcag": "6.4.1",
    "name": "반복 영역 건너뛰기",
    "principle": "운용의 용이성",
    "severity": "major",
    "fix": "페이지 상단에 '본문 바로가기' 링크를 추가하세요."
  },
  "document-title": {
    "kwcag": "6.4.2",
    "name": "제목 제공",
    "principle": "운용의 용이성",
    "severity": "major",
    "fix": "<title> 요소에 페이지를 설명하는 제목을 작성하세요."
  },
  "page-has-heading-one": {
    "kwcag": "6.4.2",
    "name": "제목 제공",
    "principle": "운용의 용이성",
    "severity": "major",
    "fix": "페이지에 <h1> 제목을 추가하세요."
  },
  "empty-heading": {
    "kwcag": "6.4.2",
    "name": "제목 제공",
    "principle": "운용의 용이성",
    "severity": "minor",
    "fix": "빈 제목 요소에 텍스트를 추가하거나 불필요한 경우 제거하세요."
  },
  "frame-title": {
    "kwcag": "6.4.2",
    "name": "제목 제공",
    "principle": "운용의 용이성",
    "severity": "major",
    "fix": "<iframe>에 title 속성을 추가하세요."
  },
  "link-name": {
    "kwcag": "6.4.3",
    "name": "적절한 링크 텍스트",
    "principle": "운용의 용이성",
    "severity": "major",
    "fix": "링크에 용도를 알 수 있는 텍스트를 추가하세요."
  },
  "button-name": {
    "kwcag": "6.4.3",
    "name": "적절한 링크 텍스트",
    "principle": "운용의 용이성",
    "severity": "major",
    "fix": "버튼에 용도를 알 수 있는 텍스트를 추가하세요."
  },
  "label-title-only": {
    "kwcag": "6.5.3",
    "name": "레이블과 네임",
    "principle": "운용의 용이성",
    "severity": "major",
    "fix": "title 속성만이 아닌 <label> 또는 aria-label로 레이블을 제공하세요."
  },
  "html-has-lang": {
    "kwcag": "7.1.1",
    "name": "기본 언어 표시",
    "principle": "이해의 용이성",
    "severity": "major",
    "fix": "<html> 요소에 lang 속성을 추가하세요 (예: lang=\"ko\")."
  },
  "html-lang-valid": {
    "kwcag": "7.1.1",
    "name": "기본 언어 표시",
    "principle": "이해의 용이성",
    "severity": "major",
    "fix": "lang 속성의 값을 유효한 언어 코드로 수정하세요 (예: ko, en, ja)."
  },
  "valid-lang": {
    "kwcag": "7.1.1",
    "name": "기본 언어 표시",
    "principle": "이해의 용이성",
    "severity": "major",
    "fix": "lang 속성 값이 유효한 BCP 47 언어 코드인지 확인하세요."
  },
  "label": {
    "kwcag": "7.3.2",
    "name": "레이블 제공",
    "principle": "이해의 용이성",
    "severity": "critical",
    "fix": "입력 필드에 <label>을 연결하세요 (for 속성 또는 감싸기)."
  },
  "select-name": {
    "kwcag": "7.3.2",
    "name": "레이블 제공",
    "principle": "이해의 용이성",
    "severity": "critical",
    "fix": "<select>에 연결된 <label>을 추가하세요."
  },
  "autocomplete-valid": {
    "kwcag": "7.3.4",
    "name": "반복 입력 정보",
    "principle": "이해의 용이성",
    "severity": "minor",
    "fix": "autocomplete 속성 값을 유효한 값으로 수정하세요."
  },
  "duplicate-id-aria": {
    "kwcag": "8.1.1",
    "name": "마크업 오류 방지",
    "principle": "견고성",
    "severity": "major",
    "fix": "ARIA에서 참조하는 id가 중복되지 않도록 수정하세요."
  },
  "duplicate-id-active": {
    "kwcag": "8.1.1",
    "name": "마크업 오류 방지",
    "principle": "견고성",
    "severity": "major",
    "fix": "활성 요소의 id가 중복되지 않도록 수정하세요."
  },
  "duplicate-id": {
    "kwcag": "8.1.1",
    "name": "마크업 오류 방지",
    "principle": "견고성",
    "severity": "minor",
    "fix": "중복된 id 속성을 고유한 값으로 수정하세요."
  },
  "aria-allowed-attr": {
    "kwcag": "8.2.1",
    "name": "웹 애플리케이션 접근성 준수",
    "principle": "견고성",
    "severity": "critical",
    "fix": "해당 role에 허용되지 않는 ARIA 속성을 제거하세요."
  },
  "aria-required-attr": {
    "kwcag": "8.2.1",
    "name": "웹 애플리케이션 접근성 준수",
    "principle": "견고성",
    "severity": "critical",
    "fix": "해당 role에 필수인 ARIA 속성을 추가하세요."
  },
  "aria-roles": {
    "kwcag": "8.2.1",
    "name": "웹 애플리케이션 접근성 준수",
    "principle": "견고성",
    "severity": "critical",
    "fix": "유효한 ARIA role 값을 사용하세요."
  },
  "aria-valid-attr": {
    "kwcag": "8.2.1",
    "name": "웹 애플리케이션 접근성 준수",
    "principle": "견고성",
    "severity": "critical",
    "fix": "유효한 ARIA 속성 이름을 사용하세요."
  },
  "aria-valid-attr-value": {
    "kwcag": "8.2.1",
    "name": "웹 애플리케이션 접근성 준수",
    "principle": "견고성",
    "severity": "critical",
    "fix": "ARIA 속성의 값을 유효한 값으로 수정하세요."
  },
  "aria-hidden-focus": {
    "kwcag": "8.2.1",
    "name": "웹 애플리케이션 접근성 준수",
    "principle": "견고성",
    "severity": "critical",
    "fix": "aria-hidden=\"true\"인 요소 내에 포커스 가능한 요소가 없도록 하세요."
  }
}
```

## 미매핑 axe-core 룰 (KWCAG 직접 대응 없음)

아래 axe-core 룰은 KWCAG 2.2에 직접 대응하는 항목이 없으나, Best Practice로 보고할 수 있음:

- `landmark-*` — 랜드마크 관련 (KWCAG에 별도 항목 없음)
- `meta-viewport` — 뷰포트 확대 제한 (WCAG 2.1 1.4.4)
- `region` — 모든 콘텐츠가 랜드마크 안에 있어야 함
