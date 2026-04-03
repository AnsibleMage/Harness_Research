# design-md 스킬 사용법 가이드

## 한 줄 요약

Stitch에 디자인된 스크린이 있으면 바로 사용 가능. 프로젝트만 선택하면 나머지는 자동.

---

## 호출 방법

### 슬래시 커맨드
```
/design-md
```

### 자연어 트리거 (한국어)
- "DESIGN.md 만들어줘"
- "스티치 디자인 분석"
- "디자인 시스템 추출"
- "디자인 토큰 추출"
- "디자인 언어 문서화"
- "스티치 프로젝트 분석"

### 자연어 트리거 (English)
- "generate DESIGN.md"
- "extract design tokens"
- "analyze Stitch project design"

---

## 사전 조건

| 조건 | 필수 여부 | 비고 |
|------|----------|------|
| Stitch MCP 서버 연결 | **필수** | `mcp__stitch__*` 도구가 사용 가능해야 함 |
| Stitch 프로젝트 (스크린 1개+) | **필수** | 디자인이 완성된 스크린이 최소 1개 |
| 프로젝트 ID | 선택 | 없으면 목록에서 선택 |
| 브랜드 가이드라인 | 선택 | 없으면 HTML에서 자동 추출 |

---

## 사용 시나리오별 예시

### 1. 가장 간단한 사용

```
앤: DESIGN.md 만들어줘
아리: 프로젝트 목록을 보여드릴게요. (mcp__stitch__list_projects 호출)
     1. My App - 5 screens
     2. Landing Page - 3 screens
     어떤 프로젝트를 분석할까요?
앤: 1번
아리: (분석 진행 → 중간 결과 표시 → DESIGN.md 생성)
```

### 2. 프로젝트 ID 직접 지정

```
앤: 프로젝트 2119859971848534106의 DESIGN.md 만들어줘
아리: (바로 분석 시작 → 인터뷰 최소화)
```

### 3. 특정 스크린만 분석

```
앤: DESIGN.md 만들어줘. Home이랑 Dashboard 스크린만 분석해
아리: (해당 스크린만 집중 분석)
```

### 4. 브랜드 가이드라인 포함

```
앤: DESIGN.md 만들어줘. 브랜드 색상은 Primary #2563EB, Secondary #10B981이고 폰트는 Pretendard야
아리: (브랜드 스펙을 기준으로 색상 이름/역할 매핑)
```

### 5. 새 스크린 생성용 (stitch-image-to-prompt 연동)

```
앤: DESIGN.md 만들어줘. 새 스크린 생성할 때 쓸 거야
아리: (Section 8 Prompt Guide를 특히 상세하게 생성)
     ...
     생성 완료! Section 8의 프롬프트 프리픽스로 테스트 스크린을 만들어볼까요?
앤: 응
아리: (mcp__stitch__generate_screen_from_text으로 테스트 생성)
```

---

## 워크플로우 상세

```
Phase 0: Interview (인터뷰)
  ↓ 프로젝트 선택, 범위/목적 확인 (1-2회 대화)
Phase 1: Retrieval (데이터 수집)
  ↓ MCP로 프로젝트 메타데이터 + 스크린별 HTML/스크린샷 수집
Phase 2: Analysis (분석)
  ↓ 6차원 분석 → 중간 결과 표시 → 사용자 확인
Phase 3: Generation (생성)
  ↓ DESIGN.md 8개 섹션 영어로 생성
Phase 4: Verification (검증)
  → 체크리스트 검증 + 후속 옵션 제공
```

### 중간 결과 확인 포인트

Phase 2 완료 후 아래와 같은 중간 결과를 표시합니다:

```
📊 분석 중간 결과:
- 스크린 수: 5개 분석 완료
- 주요 색상: 6개 추출 (Primary #2563EB, Secondary #10B981, ...)
- 폰트: Inter (headings), Inter (body)
- 레이아웃: 12-column grid, max-width 1280px
- 분위기: Clean, modern, professional

계속 진행할까요? 조정이 필요한 부분이 있나요?
```

이 시점에서 색상 이름 변경, 분위기 조정, 추가 분석 등을 요청할 수 있습니다.

---

## DESIGN.md 출력 구조

| 섹션 | 내용 | 활용도 |
|------|------|--------|
| 1. Visual Theme & Atmosphere | 분위기 형용사, 미학 철학 | Stitch 프롬프트의 톤 설정 |
| 2. Color Palette & Roles | 색상별 이름 + hex + 기능 역할 | 정확한 색상 지정 |
| 3. Typography Rules | 폰트, 사이즈, 웨이트 테이블 | 타이포 일관성 |
| 4. Component Stylings | 버튼, 카드, 네비, 폼, 모달 | 컴포넌트 재현 |
| 5. Layout Principles | 그리드, 간격, 반응형 | 레이아웃 일관성 |
| 6. Depth & Elevation | 그림자 레벨, 보더 라디우스 | 깊이감 재현 |
| 7. Image & Icon Style | 이미지/아이콘 처리 방식 | 비주얼 일관성 |
| **8. Prompt Guide** | **바로 쓸 수 있는 프롬프트 프리픽스** | **핵심 — 새 스크린 생성 시 복사/붙여넣기** |

### Section 8 예시

```
When generating new screens for this project, prepend the following to your prompt:

> Clean, spacious, and modern SaaS dashboard. Use Deep Ocean Blue (#2563EB) for primary
> actions and key metrics, Soft Cloud Gray (#F9FAFB) for page background. Inter font
> throughout — bold for headings, regular for body. Generously rounded corners on all
> cards and buttons. Comfortable 24px spacing between sections.
```

---

## 후속 옵션

DESIGN.md 생성 완료 후 선택 가능한 옵션:

| 옵션 | 설명 |
|------|------|
| **확장** | 추가 컴포넌트나 특정 스크린의 디테일 보강 |
| **테스트** | Section 8 프롬프트로 실제 스크린 생성하여 디자인 일관성 검증 |
| **연동** | stitch-image-to-prompt과 함께 사용하여 새 화면 디자인 |
| **수정** | 특정 섹션의 톤, 상세도, 색상 이름 등 조정 |

---

## stitch-image-to-prompt 연동

DESIGN.md가 있는 상태에서 이미지 기반 스크린 생성 시:

```
1. [design-md]로 기존 프로젝트 분석 → DESIGN.md 생성
2. 새 디자인 이미지 첨부 + "스티치 프롬프트로 만들어줘"
3. [stitch-image-to-prompt]이 DESIGN.md Section 8을 컨텍스트로 참조
4. 기존 디자인 언어와 일치하는 프롬프트 생성
5. Stitch MCP로 실행 → 디자인 일관성 보장
```

---

## 팁

- **스크린이 많으면** (10개+): "대표 스크린만 분석해줘"로 시간 절약
- **빠르게 쓰고 싶으면**: "DESIGN.md 만들어줘 빨리" → 인터뷰 스킵, 기본값으로 진행
- **색상 이름이 마음에 안 들면**: 중간 결과에서 "Primary를 '브랜드 블루'로 바꿔줘"
- **여러 프로젝트 비교**: 각 프로젝트별 DESIGN.md를 생성하면 디자인 언어 차이점 파악 가능
- **출력 언어**: DESIGN.md는 항상 영어 (Stitch가 영어를 가장 잘 해석)
