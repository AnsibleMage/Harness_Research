# Tier 1 정적 분석 패턴 문서

## 검사 패턴 상세

각 KWCAG 검사항목에 대해 Tier 1 Python 스크립트가 사용하는 검사 로직을 정의한다.

### 5.1.1 적절한 대체 텍스트 제공

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| `<img>` without `alt` | critical | img 태그에 alt 속성 없음 |
| `<img alt="">` (비장식) | info | 빈 alt — 장식 이미지인지 확인 필요 |
| `<area>` without `alt` | critical | 이미지맵 area에 alt 없음 |
| `<input type="image">` without `alt` | critical | 이미지 버튼에 alt 없음 |
| `[role="img"]` without `aria-label/labelledby` | critical | role=img에 접근성 이름 없음 |
| `<svg>` without `<title>` or `aria-label` | major | SVG에 대체 텍스트 없음 |

### 5.2.1 자막 제공

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| `<video>` without `<track kind="captions">` | major | 비디오에 자막 트랙 없음 |
| `<audio>` without transcript link nearby | info | 오디오 근처에 대본 링크 없음 |

### 5.3.1 표의 구성

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| `<table>` with `<td>` but no `<th>` | major | 데이터 테이블에 제목 셀 없음 |
| `<th>` without `scope` | minor | th에 scope 속성 없음 |
| `<table>` without `<caption>` or `aria-label` | minor | 표에 제목/설명 없음 |

### 5.3.2 콘텐츠의 선형구조

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| Heading level skip (h1→h3) | minor | 제목 수준 건너뛰기 |
| `<table>` used for layout (no `<th>`, `role="presentation"` 없음) | info | 레이아웃 테이블 의심 |

### 5.4.2 자동 재생 금지

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| `<video autoplay>` | critical | 비디오 자동 재생 |
| `<audio autoplay>` | critical | 오디오 자동 재생 |
| `autoplay` attribute on media | critical | autoplay 속성 감지 |

### 6.1.1 키보드 사용 보장

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| `onclick` on non-interactive without `onkeydown/onkeypress` | critical | 마우스만 사용 가능 |
| `<div onclick>` without `tabindex` and `role` | critical | 비대화형 요소에 클릭 이벤트 |
| `<a href="javascript:void(0)">` | major | JavaScript 링크 |

### 6.1.2 초점 이동과 표시

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| `outline: none` or `outline: 0` in style | critical | 초점 표시 제거 |
| `tabindex` > 0 | major | 양수 tabindex (초점 순서 강제 변경) |
| `:focus { outline: none }` in `<style>` | critical | CSS로 초점 표시 제거 |

### 6.1.4 문자 단축키

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| `accesskey` attribute 존재 | info | accesskey 사용 — 충돌 위험 검토 필요 |

### 6.4.1 반복 영역 건너뛰기

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| No skip link (`<a href="#main">`, `<a href="#content">` 등) | major | 건너뛰기 링크 없음 |
| No `<main>` or `role="main"` | major | 메인 콘텐츠 영역 미지정 |
| No landmark roles | info | 랜드마크 역할 없음 |

### 6.4.2 제목 제공

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| Empty `<title>` | major | 페이지 제목 비어있음 |
| Missing `<title>` | major | 페이지 제목 없음 |
| No `<h1>` | major | h1 제목 없음 |
| Empty heading (`<h1></h1>`) | minor | 빈 제목 요소 |
| `<iframe>` without `title` | major | iframe에 title 없음 |

### 6.4.3 적절한 링크 텍스트

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| Link text: "여기", "클릭", "더보기", "more", "click here", "read more" | major | 모호한 링크 텍스트 |
| Empty link (`<a href="..."></a>`) | major | 빈 링크 |
| Link with only image, no alt | critical | 이미지만 있는 링크, alt 없음 |

### 6.5.3 레이블과 네임

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| `aria-label` 과 visible text 불일치 | major | 접근성 이름과 시각적 텍스트 불일치 |

### 7.1.1 기본 언어 표시

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| `<html>` without `lang` | major | html에 lang 속성 없음 |
| `lang` value not valid BCP 47 | major | 유효하지 않은 lang 값 |

### 7.2.1 사용자 요구에 따른 실행

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| `<select onchange>` without nearby submit button | major | select 변경 시 자동 실행 의심 |
| `onfocus` with navigation code | major | 포커스 시 자동 이동 |

### 7.3.2 레이블 제공

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| `<input>` without `<label>`, `aria-label`, or `aria-labelledby` | critical | 입력 필드에 레이블 없음 |
| `<select>` without label | critical | 선택 필드에 레이블 없음 |
| `<textarea>` without label | critical | 텍스트 영역에 레이블 없음 |
| `<label for="x">` but no `id="x"` element | major | label의 for와 일치하는 id 없음 |
| `placeholder` only (no `<label>`) | major | placeholder만 사용, label 없음 |

### 7.3.3 접근 가능한 인증

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| `<input type="password">` without `autocomplete` | info | 비밀번호 필드에 autocomplete 없음 |

### 8.1.1 마크업 오류 방지

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| Duplicate `id` attributes | major | 중복 id |
| Invalid nesting (`<p>` 안에 `<div>`) | major | 잘못된 중첩 |
| `<a>` 안에 `<a>` | critical | 링크 안 링크 |
| `<button>` 안에 `<button>` | critical | 버튼 안 버튼 |

### 8.2.1 웹 애플리케이션 접근성 준수

| 패턴 | 심각도 | 검사 내용 |
|------|--------|----------|
| Invalid `role` value | critical | 유효하지 않은 role |
| `aria-*` on wrong element | major | 부적절한 ARIA 속성 |
| `aria-hidden="true"` on focusable element | critical | 숨겨진 요소에 포커스 가능 |
