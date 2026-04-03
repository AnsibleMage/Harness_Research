---
name: section-redesign
description: "웹 페이지의 개별 섹션(단)을 디자인 이미지 기반으로 정밀하게 변경하는 바이브코딩 스킬. 사용자가 스크린샷 또는 디자인 시안 이미지를 제공하면, 해당 이미지를 충실히 분석하여 기존 섹션의 CSS/HTML/JS를 교체 구현한다. Use when: (1) 사용자가 특정 섹션의 디자인 변경을 요청하고 참조 이미지를 제공할 때, (2) '이 디자인으로 바꿔줘', '이 이미지처럼 만들어줘', '이 섹션 리디자인' 등의 요청, (3) 단별(섹션별) UI 변경 작업, (4) 기존 레이아웃을 새 디자인 시안으로 교체할 때. 퍼블리싱, 바이브코딩, 섹션 교체, 디자인 시안 코딩에 해당."
---

# Section Redesign Skill

기존 웹 페이지의 개별 섹션을 디자인 이미지 기반으로 정밀하게 교체 구현하는 스킬.

## Core Principle: Image-Faithful Implementation

**디자인 이미지가 진실의 원천(Single Source of Truth)이다.**

- 제공된 스크린샷/시안을 pixel-level로 분석하여 구현
- 임의 해석 최소화 — 이미지에 보이는 것만 구현
- 불명확한 부분은 사용자에게 확인 후 진행

## Workflow

### Step 1: Scope Identification

대상 섹션의 3가지 경계를 반드시 확인:

```
1. CSS 경계: 관련 스타일 블록의 시작/끝 라인
2. HTML 경계: 섹션 마크업의 시작/끝 라인
3. JS 경계: 인터랙션 초기화 코드 (있는 경우)
```

Read tool로 세 영역을 모두 읽은 후 작업 시작. **읽지 않은 코드는 수정하지 않는다.**

### Step 2: Design Image Analysis

Read tool로 디자인 이미지를 열어 다음을 식별:

| 분석 항목 | 확인 포인트 |
|----------|-----------|
| **레이아웃** | flex/grid, 컬럼 수, 정렬 방향 |
| **타이포그래피** | 각 텍스트의 상대적 크기, 굵기, 색상 |
| **색상** | 배경색, 텍스트색, 액센트색 |
| **간격** | 요소 간 gap, padding, margin |
| **배경** | 단색/이미지/그라데이션, 적용 범위(전폭/컨테이너) |
| **장식** | border-radius, box-shadow, 아이콘, 오버레이 |
| **인터랙션** | 버튼, 슬라이더, 검색바 등 |

### Step 3: Implementation (CSS → HTML → JS)

**반드시 이 순서로 실행:**

1. **CSS 교체** — 기존 섹션 스타일 블록을 새 디자인에 맞게 전면 교체
2. **HTML 교체** — 기존 섹션 마크업을 새 구조로 교체, 기존 콘텐츠(이미지 경로, 텍스트) 보존
3. **JS 수정** — 캐러셀/인터랙션 초기화 코드 업데이트 (필요시)

각 단계에서 Edit tool 사용. 기존 코드의 정확한 old_string 매칭 필수.

### Step 4: Asset Verification

Glob tool로 참조되는 이미지/리소스 파일 존재 여부 확인:
```
Glob: **/filename.png
```

### Step 5: Incremental Refinement

사용자가 추가 스크린샷으로 미세 조정 요청 시:
- 전체 교체가 아닌 **해당 속성만 Edit**
- 변경 사항 요약을 테이블로 제시

## Implementation Rules

### CSS Rules
- 기존 섹션 CSS 블록을 **통째로 교체** (잔여 스타일 방지)
- 셀렉터는 섹션 클래스 기준 네스팅 (`.con_xxx .child`)
- 배경 이미지 경로는 CSS 파일 기준 상대경로
- 컨테이너 너비 제한이 있으면 배경을 container가 아닌 wrapper에 적용하여 좌우 여백 제어

### HTML Rules
- 기존 콘텐츠(텍스트, 이미지 경로, alt 텍스트) 최대한 보존
- 사용자가 제공한 텍스트는 **정확히 그대로** 사용
- `javascript:void(0);` 링크 패턴 유지 (프로토타입)
- SVG 아이콘은 인라인으로 삽입 (외부 의존성 최소화)

### JS Rules
- 기존 라이브러리(Swiper, slick 등) 활용, 새 라이브러리 추가 지양
- effect 변경 시 관련 옵션 전체 업데이트
- 셀렉터가 변경되면 JS 초기화 코드도 반드시 갱신

### Refinement Rules
- 사용자 피드백은 **이미지 > 텍스트** 우선순위
- "크기 키워줘" → 구체적 px 값으로 변환하여 적용
- "이미지처럼" → Read로 이미지 재분석 후 차이점 식별
- 변경 전/후를 비교 테이블로 보고

## Detailed Patterns

구현 패턴, 코드 스니펫, 레이아웃 패턴은 [references/workflow.md](references/workflow.md) 참조.
