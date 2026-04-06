# Claude Code 사용 전략 — 연말정산 계산기 개발

> 작성일: 2026-02-13
> 목적: 개발 계획서 작성 전, Claude Code의 체인/에이전트/스킬/팀/훅을 최대한 활용하는 **사용 전략** 수립
> 참고: CLAUDE.md V4.2.1, [[03_참고자료_및_기술스택]] (설계 원칙), [[04_개발용_계산스펙]], [[05_화면디자인_설계]]

---

## 1. 프로젝트 특성 분석 → Claude Code 매핑

### 1-1. 이 프로젝트의 작업 유형 분류

| 작업 유형 | 해당 작업 | 특성 | 최적 도구 |
|----------|----------|------|----------|
| 프로젝트 초기화 | Next.js 셋업, 패키지 설치 | 순차, 단순 | Bash 직접 실행 |
| 계산 엔진 개발 | 11개 순수 함수 (TDD) | 순차, 핵심 | **DevChain** |
| UI 컴포넌트 개발 | Step 위저드, CurrencyInput 등 | 독립 병렬 가능 | **WebDevChain+** or **Teams** |
| 통합 & 연결 | 계산엔진 ↔ UI 연결, 상태관리 | 순차, 의존성 | **DevChain** |
| 테스트 & 검증 | 단위테스트, E2E, 홈택스 대조 | 병렬 가능 | **Teams** + `/webapp-testing` |
| 디자인 정제 | 테마, 반응형, 접근성 | 독립 | `/theme-factory` + `/frontend-design` |
| 배포 | Vercel 배포 | 단순 | Bash 직접 실행 |
| 버그 수정 | 계산 오류, UI 깨짐 | 긴급 | **HotfixChain** |

### 1-2. 병렬 vs 순차 의존성 맵

```
[프로젝트 초기화]
        │
        ▼
┌───────┴───────┐
│               │
▼               ▼
[계산 엔진]   [UI 컴포넌트]     ← ★ 병렬 가능 (Teams 적합)
│               │
└───────┬───────┘
        │
        ▼
    [통합 & 연결]               ← 순차 (DevChain)
        │
        ▼
┌───────┴───────┐
│               │
▼               ▼
[테스트/검증]  [디자인 정제]     ← ★ 병렬 가능 (Teams 적합)
│               │
└───────┬───────┘
        │
        ▼
      [배포]
```

---

## 2. 체인(Chain) 선택 전략

### 2-1. 개발 단계별 체인 매핑

| 단계 | 체인 | 프롬프트 패턴 | 핵심 에이전트 |
|------|------|-------------|-------------|
| **0. 초기화** | 체인 생략 | "Next.js 프로젝트 초기화해줘" | Bash 직접 |
| **1. 계산 엔진** | **DevChain** | "근로소득공제 계산 함수를 TDD로 개발해줘. 1함수=1파일 원칙" | requirements_analyst → system_architect → code_developer |
| **2. UI 개발** | **WebDevChain+** | "Step1Salary 컴포넌트를 개발해줘" | requirements_analyst → /theme-factory → /frontend-design |
| **3. 통합** | **DevChain** | "계산 엔진과 UI를 연결해줘" | system_architect → code_developer |
| **4. 테스트** | **DevChain** | "전체 계산 로직 테스트를 작성해줘" | code_developer → quality_reviewer |
| **5. 디자인** | **WebDevChain+** | "반응형 디자인과 접근성을 적용해줘" | /theme-factory → /frontend-design |
| **6. 배포** | 체인 생략 | "Vercel로 배포해줘" | Bash 직접 |
| **긴급 수정** | **HotfixChain** | "세율 계산 버그 긴급 수정해줘" | complexity_resolver → code_developer |

### 2-2. 체인 선택 프롬프트 전략

> **핵심**: 프롬프트에 포함하는 키워드가 Hook의 4-Layer 분석을 통해 체인을 활성화한다.

#### DevChain 트리거 키워드
```
"개발해줘", "TDD", "함수 구현", "코딩", "테스트 작성"
```

#### WebDevChain+ 트리거 키워드
```
"UI 개발", "컴포넌트", "프론트엔드", "shadcn", "디자인 적용"
```

#### HotfixChain 트리거 키워드
```
"긴급", "버그 수정", "핫픽스", "오류 발생"
```

### 2-3. 의도적 체인 선택 예시

```
❌ "계산 함수 만들어줘"
   → Hook이 애매하게 판단할 수 있음

✅ "근로소득공제 계산 함수를 TDD로 개발해줘. 04_개발용_계산스펙.md 참고"
   → DevChain 명확 트리거 + 컨텍스트 제공
```

---

## 3. 에이전트(Subagent) 활용 전략

### 3-1. 에이전트 유형별 사용 시점

| 에이전트 | 모델 | 이 프로젝트에서 사용 시점 | 비용/속도 |
|---------|------|----------------------|----------|
| `requirements_analyst` | **O** | 각 Phase 시작 시 요구사항 정리 | 비용↑ 정확↑ |
| `system_architect` | **O** | 프로젝트 구조, 상태관리 설계 | 비용↑ 정확↑ |
| `code_developer` | S | 실제 코드 작성 (함수, 컴포넌트) | 비용↓ 빠름 |
| `quality_reviewer` | S | 코드 리뷰, 테스트 검증 | 비용↓ 빠름 |
| `Explore` | S | 생성된 코드베이스 탐색 | 비용↓ 빠름 |
| `Plan` | **O** | 복잡한 구현 전 계획 수립 | 비용↑ 정확↑ |

### 3-2. 에이전트 비용 최적화

```
                비용 효율                    정확도 필요
    ◄────────────────────────────────────────────►

    code_developer[S]    quality_reviewer[S]    system_architect[O]
    Explore[S]           general-purpose[S]     requirements_analyst[O]

    일상 코딩             코드 리뷰/탐색          설계/요구분석
```

**전략**: Opus(O) 에이전트는 **설계/분석 단계에만** 사용하고, 반복적 코딩은 Sonnet(S)으로 처리

### 3-3. 서브에이전트 vs 직접 실행 판단

| 상황 | 선택 | 이유 |
|------|------|------|
| 단일 파일 수정 | 직접 실행 | 서브에이전트 오버헤드 과다 |
| 파일 3개 이상 동시 수정 | 서브에이전트 | 컨텍스트 분리 + 병렬 |
| 복잡한 로직 검토 | Plan[O] 에이전트 | 깊은 사고 필요 |
| 간단한 파일 검색 | Glob/Grep 직접 | Explore 에이전트 불필요 |
| 대규모 코드베이스 탐색 | Explore[S] | 여러 번 검색 필요 |

---

## 4. Agent Teams 활용 전략

### 4-1. Teams 적합 구간

이 프로젝트에서 **Agent Teams가 효과적인 2개 구간**:

#### 구간 A: 계산 엔진 ∥ UI 컴포넌트 (Phase 1 핵심)

```
┌─ Team: yearendtax-phase1 ─────────────────────────┐
│                                                     │
│  Lead (메인 세션)                                    │
│  ├─ Teammate 1: "engine-dev" (code_developer)       │
│  │   → 계산 함수 11개 TDD 개발                       │
│  │   → earned-income-deduction.ts                   │
│  │   → tax-bracket.ts                               │
│  │   → card-deduction.ts                            │
│  │   → medical-credit.ts                            │
│  │   → ...                                          │
│  │                                                   │
│  └─ Teammate 2: "ui-dev" (general-purpose)          │
│      → shadcn/ui 컴포넌트 개발                       │
│      → CurrencyInput, StepIndicator                 │
│      → Step1Salary, Step2Dependents                 │
│      → ...                                          │
│                                                     │
│  Lead: 통합 + calculator.ts 작성                     │
└─────────────────────────────────────────────────────┘
```

**프롬프트 예시**:
```
계산 엔진과 UI를 병렬로 개발해줘.

Teammate 1 (engine-dev):
- 04_개발용_계산스펙.md 의 함수 시그니처 기반으로
- lib/tax/ 폴더에 11개 순수 함수를 TDD로 구현
- 06_계산수식_실행예시.md의 테스트 케이스 활용

Teammate 2 (ui-dev):
- 05_화면디자인_설계.md 기반으로
- components/calculator/steps/ 에 Step 1~4 컴포넌트 구현
- shadcn/ui + Tailwind v4 사용
```

#### 구간 B: 테스트 ∥ 디자인 정제 (Phase 완료 후)

```
┌─ Team: yearendtax-qa ─────────────────────────────┐
│                                                     │
│  Lead (메인 세션)                                    │
│  ├─ Teammate 1: "tester" (code_developer)           │
│  │   → 단위 테스트 + 통합 테스트                      │
│  │   → 경계값 테스트 (06번 문서 기반)                  │
│  │                                                   │
│  └─ Teammate 2: "designer" (general-purpose)        │
│      → 반응형 디자인 검수                             │
│      → 접근성 (WCAG 2.1 AA) 검수                     │
│      → 다크 모드 (Phase 2)                           │
│                                                     │
│  Lead: E2E 테스트 + /webapp-testing                  │
└─────────────────────────────────────────────────────┘
```

### 4-2. Teams 사용 시 주의사항

| 규칙 | 적용 |
|------|------|
| 메모리 저장은 Lead만 | Teammate에서 memory/ 접근 금지 |
| 착수 보고 30초 내 | spawn 후 무응답이면 120초 후 shutdown |
| 파일 충돌 방지 | Teammate별 작업 폴더를 명확히 분리 |
| 동일 파일 동시 수정 금지 | Lead가 TaskCreate로 파일 할당 관리 |
| **hooks/ 폴더 Lead 전용** | useTaxCalculator, useStepForm은 engine+UI 양쪽 의존 → 통합 단계에서 Lead만 작성 |

### 4-3. Teams 사용하지 말아야 할 구간

| 구간 | 이유 |
|------|------|
| 프로젝트 초기화 | 순차 의존 (디렉토리 → 패키지 → 설정) |
| 계산엔진-UI 통합 | 양쪽 결과물 의존 |
| Vercel 배포 | 단일 명령어, Teams 오버헤드 과다 |
| 긴급 버그 수정 | HotfixChain이 더 빠름 |

---

## 5. 스킬(Skill) 활용 전략

### 5-1. 개발 과정에서 사용할 스킬

| 스킬 | 사용 시점 | 프롬프트 패턴 |
|------|----------|-------------|
| `/frontend-design` | UI 컴포넌트 개발 | "CurrencyInput 컴포넌트를 개발해줘" |
| `/web-artifacts-builder` | 복잡한 React 컴포넌트 | "ResultSummary를 shadcn으로 만들어줘" |
| `/theme-factory` | 테마 시스템 구축 | "환급/납부 컬러 테마를 만들어줘" |
| `/webapp-testing` | E2E 테스트 | "Playwright로 계산 흐름을 테스트해줘" |
| `/commit-push` | 작업 단위 커밋 | `/commit-push` |
| `/project-review` | Phase 완료 후 전체 리뷰 | "프로젝트 리뷰해줘" |
| `/pr-review` | PR 생성 전 점검 | "PR 리뷰해줘" |

### 5-2. 스킬 조합 패턴

#### 패턴 A: UI 컴포넌트 풀 사이클
```
/theme-factory → /frontend-design → /webapp-testing → /commit-push
```
> "환급 결과 카드 컴포넌트를 테마 적용해서 개발하고 테스트까지 해줘"

#### 패턴 B: 코드 → 리뷰 → 커밋
```
[code_developer] → /project-review → /commit-push
```
> "계산 함수 구현 후 리뷰하고 커밋해줘"

#### 패턴 C: 버그 수정 사이클
```
HotfixChain → /webapp-testing → /commit-push
```
> "세율 계산 버그 수정하고 테스트 확인 후 커밋해줘"

### 5-3. 스킬 트리거 키워드 요약

```
"프론트엔드" "UI" "컴포넌트"     → /frontend-design
"React" "shadcn" "아티팩트"      → /web-artifacts-builder
"테마" "팔레트" "컬러"           → /theme-factory
"Playwright" "e2e" "테스트"      → /webapp-testing
"커밋" "푸시"                    → /commit-push
"리뷰" "전체 리뷰"              → /project-review
```

---

## 6. 슬래시 커맨드(/) 활용 전략

### 6-1. 개발 중 사용할 커맨드

| 커맨드 | 시점 | 빈도 |
|--------|------|------|
| `/commit-push` | 기능 단위 완성 시 | 매우 자주 |
| `/project-review` | Phase 완료 시 | Phase당 1회 |
| `/pr-review` | main 브랜치 merge 전 | Phase당 1회 |
| `/memory-save` | 세션 종료 전 | 매 세션 마지막 |
| `/analyze` | 복잡한 프롬프트 디버그 시 | 필요시 |
| `/readme-gen` | 배포 전 | 1회 |

### 6-2. 커밋 전략

```
Phase 1 커밋 단위:
├── feat: 프로젝트 초기화 (Next.js + deps)
├── feat: 상수 정의 (tax-2024.ts)
├── feat: 근로소득공제 함수 + 테스트
├── feat: 과세표준 산출세액 함수 + 테스트
├── feat: 신용카드 공제 함수 + 테스트
├── feat: 의료비 세액공제 함수 + 테스트
├── feat: 통합 계산기 (calculator.ts) + 테스트
├── feat: CurrencyInput, StepIndicator 컴포넌트
├── feat: Step1~4 폼 컴포넌트
├── feat: 결과 화면 + Recharts 차트
├── feat: 전체 통합 + E2E 테스트
└── chore: Vercel 배포 설정
```

---

## 7. Hook 활용 전략

### 7-1. 현재 활성화된 Hook

| Hook | 역할 | 개발 중 효과 |
|------|------|------------|
| **UserPromptSubmit** | 4-Layer 분석 → 체인 추천 | 프롬프트마다 자동으로 최적 도구 추천 |
| **PreToolUse:Write** | .env/.secret 보호 | API 키 실수 방지 |
| **PostToolUse:Write** | Prettier 자동 포매팅 | TS/TSX 코드 자동 정리 |
| **PostToolUse** | Git 상태 표시 | 변경사항 실시간 추적 |

### 7-2. 이 프로젝트에서 Hook이 도와주는 것

```
[코드 작성] → PostToolUse → Prettier 자동 실행 → 코드 포맷 일관성
[프롬프트 입력] → UserPromptSubmit → 체인 추천 → 올바른 도구 선택
[파일 저장] → PreToolUse → 보안 파일 차단 → .env.local 실수 방지
[메모리 저장] → 이전 프롬프트 자동 저장 지시 → 세션 연속성
```

### 7-3. Hook 작동 최적화 팁

| 팁 | 설명 |
|-----|------|
| PostToolUse의 Prettier | `.prettierrc` 설정 필수 — TS/TSX 자동 포매팅 |
| 4-Layer 분석 | 프롬프트에 키워드를 명확히 넣으면 정확도 상승 |
| 마지막 프롬프트 | `/memory-save`로 수동 저장 (자동 저장 안됨) |
| Teammate 세션 | Hook 분석 자동 스킵됨 (오버헤드 방지) |

---

## 8. 프롬프트 설계 전략

### 8-1. 효율적인 프롬프트 구조

```markdown
## 좋은 프롬프트 구조

[작업 목표] + [참고 문서] + [구체적 범위] + [검증 방법]

예시:
"04_개발용_계산스펙.md의 calcEarnedIncomeDeduction 함수를 TDD로 구현해줘.
 06번 문서의 경계값 테스트 케이스를 포함하고,
 총급여 500만/1500만/4500만/1억원 경계에서 검증해줘."
```

### 8-2. AI 최적 배치 프롬프트 전략

> **08번 리뷰 반영**: AI는 관련 함수 3~5개를 한 번에 생성할 수 있다.
> 1함수=1프롬프트(인간 방식)가 아닌 **배치 단위**로 프롬프트를 설계한다.

#### 배치 0: 초기화 + 기반 레이어 (1 프롬프트)
```
연말정산 계산기 프로젝트를 초기화해줘.
- 03번 문서의 프로젝트 구조대로 디렉토리 생성
- 04번 문서의 상수(§5 tax-2024.ts), 타입(§4 step-types.ts + tax-input.ts + tax-result.ts) 구현
- 06번 문서의 테스트 픽스처 섹션을 __tests__/fixtures/test-cases.ts로 생성
- Next.js 15 + TypeScript + Tailwind v4 + shadcn/ui
```

#### 배치 A: 독립 계산 함수 그룹 (1 프롬프트)
```
다음 계산 함수들을 TDD로 구현해줘 (04번 §5 상수, §6 시그니처 참조):

1. earned-income-deduction.ts — 근로소득공제
2. tax-bracket.ts — 과세표준 산출세액
3. personal-deduction.ts — 인적공제 (04번 §10-3 중복 규칙 포함)

각 함수: lib/tax/에 구현, __tests__/에 06번 경계값 테이블 기반 테스트
```

#### 배치 B: 소득공제 + 세액공제 함수 (1 프롬프트)
```
다음 함수들을 TDD로 구현해줘:

1. card-deduction.ts — 신용카드 소득공제
2. earned-income-credit.ts — 근로소득세액공제

04번 §7 의사코드 참조, 06번 예시 1~6의 기대값으로 검증
```

#### 배치 C: 세액공제 나머지 (1 프롬프트)
```
다음 세액공제 함수들을 TDD로 구현해줘:

1. pension-credit.ts — 연금계좌 세액공제
2. medical-credit.ts — 의료비 세액공제
3. education-credit.ts — 교육비 세액공제
4. rent-credit.ts — 월세 세액공제

04번 §5-5~5-8 상수 참조, 06번 테스트 픽스처 검증
```

#### 배치 D: 통합 계산기 (1 프롬프트)
```
calculator.ts 통합 계산기를 구현해줘.
- 위 모든 함수를 import하여 calculateTax(input: TaxInput): TaxResult 구현
- 04번 §10 에러/경계 동작 규칙 적용
- 06번 TEST_FIXTURES 6개 전체로 통합 테스트
```

#### 배치 E: UI Step 단위 (1 프롬프트씩)
```
Step3 소득공제 화면 전체를 구현해줘 (05번 §4-3 와이어프레임, §5-9 Props 참조):

- Step3Deductions.tsx (레이아웃 + 하위 import)
- InsuranceSection.tsx (05번 InsuranceSectionProps 구현)
- CardUsageSection.tsx (05번 CardUsageSectionProps 구현)
- shared/CurrencyInput.tsx 재사용, React Hook Form + Zod 연결
```

> **효과**: 11개 프롬프트 → **5~7개**로 축소. 관련 함수가 한 프롬프트에 있어 일관성↑

### 8-3. 문서 참조 전략 — AI 최적 참조 맵

> **08번 리뷰 반영**: AI는 작업당 1~2개 핵심 문서만 참조하면 된다.
> 아래 맵은 07번 §8-3의 인간용 매핑을 AI 관점으로 최적화한 것이다.

### 8-3. 문서 참조 전략

> 이 프로젝트의 6개 문서는 각각 다른 역할을 한다.

| 작업 | 필수 참조 | 선택 참조 | 불필요 |
|------|----------|----------|--------|
| 계산 함수 개발 | **04번** | 06번 (검증) | 01, 02, 03, 05 |
| 상수/타입 정의 | **04번** | - | 02 (중복) |
| UI 컴포넌트 개발 | **05번** | 03 (구조) | 01, 02, 04, 06 |
| 통합 테스트 | **06번** | 04 (타입) | 01, 02, 03, 05 |
| 프로젝트 초기화 | **03번** | 04 (구조) | 01, 02, 05, 06 |

> **핵심**: 02번은 AI 개발 프롬프트에서 제외. 04번에 이미 TypeScript로 번역되어 있음.

**프롬프트 예시**:
```
04번 문서의 EARNED_INCOME_DEDUCTION_BRACKETS 상수와
calcEarnedIncomeDeduction 함수를 구현해줘.
06번 문서의 경계값 검증 테이블로 테스트를 작성해줘.
```

---

## 9. 세션 관리 전략

### 9-1. 세션 분할 기준

| 세션 | 작업 범위 | 예상 프롬프트 수 |
|------|----------|---------------|
| 세션 1 | 프로젝트 초기화 + 상수/타입 정의 | 3~5개 |
| 세션 2 | 계산 엔진 핵심 함수 (5개) | 5~7개 |
| 세션 3 | 계산 엔진 나머지 + 통합 | 4~6개 |
| 세션 4 | UI 컴포넌트 (Teams 모드) | 3~5개 |
| 세션 5 | 통합 + E2E 테스트 | 4~6개 |
| 세션 6 | 디자인 정제 + 배포 | 3~5개 |

### 9-2. 세션 시작/종료 프로토콜

**세션 시작**:
```
1. 자동: Hook이 이전 프롬프트 메모리 저장 지시
2. 자동: MEMORY.md 로드 → 이전 세션 컨텍스트 확인
3. 수동: "이전 세션 이어서 [다음 작업] 해줘"
```

**세션 종료**:
```
1. 마지막 의미 있는 작업 후: /memory-save 실행
2. 자동: 응답 완료 프로토콜 → 💾 메모리 저장
3. 다음 세션에서 메모리 자동 참조됨
```

### 9-3. 컨텍스트 윈도우 관리

| 상황 | 전략 |
|------|------|
| 컨텍스트 소진 임박 | 서브에이전트로 작업 분산 |
| 대량 코드 생성 | Plan → 승인 → 구현 (2단계) |
| 여러 파일 동시 참조 | Explore 에이전트에 위임 |
| 이전 세션 참조 필요 | 메모리 파일 명시적 참조 |

---

## 10. 개발 순서 최적화 로드맵

### Phase 0: 프로젝트 초기화

```
프롬프트 1개 → 체인 없이 직접 실행
```

### Phase 1: 계산 엔진 (DevChain × 반복)

```
프롬프트 구조:
"[함수]를 TDD로 개발해줘. 04번 스펙, 06번 테스트 참고"

순서 (의존성 기반):
1. constants/tax-2024.ts (상수)
2. earned-income-deduction.ts (근로소득공제)
3. tax-bracket.ts (과세표준 세율)
4. personal-deduction.ts (인적공제)
5. card-deduction.ts (카드 공제)
6. earned-income-credit.ts (근로소득세액공제)
7. pension-credit.ts (연금 세액공제)
8. medical-credit.ts (의료비 세액공제)
9. education-credit.ts (교육비 세액공제)
10. rent-credit.ts (월세 세액공제)
11. calculator.ts (통합) ← 1~10 의존

▶ 1~10은 독립적 → 병렬 가능 (Teams)
▶ 11은 순차 (모든 함수 완성 후)
```

### Phase 2: UI 컴포넌트 (WebDevChain+ or Teams)

```
독립 병렬 가능:
├─ CurrencyInput + NumberInput (공통)
├─ StepIndicator + StepWizard (네비게이션)
├─ Step1Salary (급여 입력)
├─ Step2Dependents (인적공제)
├─ Step3Deductions (소득공제)
├─ Step4Credits (세액공제)
└─ ResultSummary + TaxChart (결과)

▶ Teams: 공통 컴포넌트 / Step 입력 / 결과 화면 3팀
```

### Phase 3: 통합 & 테스트 (DevChain → 마무리)

```
순차:
1. useTaxCalculator 훅 → UI ↔ 계산엔진 연결
2. useStepForm 훅 → React Hook Form 다단계
3. 통합 테스트 (calculator.test.ts)
4. /webapp-testing → E2E 테스트
5. /project-review → 전체 검수
6. /commit-push → 최종 커밋
```

---

## 11. 비용/속도 최적화 요약

| 전략 | 효과 |
|------|------|
| Opus는 설계/분석만, Sonnet은 코딩 | 비용 60%↓ |
| 독립 작업은 Teams 병렬 | 시간 40~50%↓ |
| 문서 참조로 프롬프트 줄이기 | 토큰 절약, 정확도↑ |
| PostToolUse Prettier 활용 | 포매팅 프롬프트 불필요 |
| `/commit-push` 자동화 | 수동 git 명령 제거 |
| 경계값 테스트 데이터 재사용 (06번) | 테스트 작성 시간↓ |

---

## 12. 체크리스트: 프롬프트 작성 전 확인

```
□ 작업이 단순한가? → 체인 생략, 직접 실행
□ 작업이 복잡한가? → 적절한 체인 키워드 포함
□ 독립 병렬 가능한 2+ 작업인가? → Teams 모드 또는 "병렬로" 키워드
□ 참고할 문서가 있는가? → 문서 번호 명시 (04번, 05번, 06번)
□ 테스트가 필요한가? → "TDD", "테스트 포함" 키워드
□ 커밋이 필요한가? → /commit-push 후속 요청
□ 세션 마지막인가? → /memory-save 실행
```

---

## 참고
- [[03_참고자료_및_기술스택]] — 설계 원칙 (1모듈=1파일, SSOT, 공통 추출)
- [[04_개발용_계산스펙]] — 함수/타입/상수 정의
- [[05_화면디자인_설계]] — UI/UX 와이어프레임
- [[06_계산수식_실행예시]] — 테스트 데이터
- CLAUDE.md V4.2.1 — 체인/에이전트/스킬 매핑
