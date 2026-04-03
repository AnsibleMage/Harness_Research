---
title: "Supanova Forge 창의성 엔진 분석 — RLHF 해제 메커니즘과 01_ 연구보고서 대조"
version: "1.0.0"
created: "2026-03-22"
updated: "2026-03-22"
tags: [claude-code, supanova-forge, creativity-engine, RLHF, design-system, VIBE]
status: completed
type: research
source: supanova-forge SKILL.md + research/ + archive/
---

## 🔄 Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed
- 마지막 작업: supanova-forge 스킬 전체 분석 + 01_ 연구보고서와 대조 완료

### 다음 작업 (TODO)
- [ ] 01_ 보고서의 7차원 파라미터를 supanova-forge v3에 직접 통합 설계
- [ ] VIBE 프리셋에 TTCT 4차원 가중치를 연동하는 구조 설계
- [ ] 멀티에이전트 대립 패턴을 디자인 리뷰 워크플로우에 적용

### 작업 조언
> [!tip] 다음 Claude Code에게
> - supanova-forge의 Creative Variance Engine(Section 5)이 01_ 보고서의 "창의성 해제 파라미터"와 사실상 같은 문제를 다른 방식으로 풀고 있다
> - 핵심 차이: forge는 VIBE 프리셋(이산형 5개 선택지), 01_ 보고서는 연속형 0-100 스케일
> - 두 접근법을 합치면 "VIBE 선택 → 세부 파라미터 연속 조절" 2단계 구조가 됨
> - research/laziness 폴더의 RLHF 연구가 01_ 보고서의 학술 근거와 매우 잘 정렬됨
> - taste-skill 원본이 "Anti-Generic"의 기원, forge가 구조화, 01_이 학술적 근거 부여

---

# Supanova Forge 창의성 엔진 분석

## 개요

supanova-forge 스킬의 전체 구조를 분석하고, 그 안에 내장된 "창의성 엔진"이 01_RLHF_창의성해제_AB실험_연구보고서에서 도출한 파라미터 체계와 어떻게 대응하는지를 대조 분석한다. forge는 이미 RLHF 동질성 문제를 실무적으로 풀고 있었고, 01_ 보고서는 그 직관에 학술적 근거를 부여한다.

---

## 1. Supanova Forge 스킬 아키텍처 전체상

### 1.1 스킬 진화 계보

```
taste-skill (Leon, @lexnlin)     ← "AI 티 제거"의 철학적 기원
    ↓
4개 분리 스킬 (v0.x)
├── taste-skill (213줄)          ← 디자인 엔진 코어
├── redesign-skill (142줄)       ← 기존 페이지 개선
├── soft-skill (121줄)           ← 프리미엄 미학
└── output-skill (93줄)          ← 출력 잘림 방지
    ↓
supanova-forge v1.0 (569→275줄, 52% 압축)  ← 4스킬 통합
    ↓
supanova-forge v2.0                          ← VIBE 프리셋 연동 시스템
```

### 1.2 11개 섹션 구조

| 섹션 | 역할 | 창의성 엔진 관련도 |
|------|------|-------------------|
| 1. Identity & Configuration | VIBE 프리셋 + 모드 라우팅 | ★★★★★ 핵심 |
| 2. Architecture & Conventions | 기술 스택 + HTML 템플릿 | ★☆☆☆☆ |
| 3. Anti-Pattern Registry | 금지 패턴 통합 | ★★★★★ 핵심 |
| 4. Design Engineering | 타이포/색상/레이아웃/깊이/한국어 | ★★★★☆ |
| 5. Creative Variance Engine | VIBE별 아키타입 + 컴포넌트 + 모션 | ★★★★★ 핵심 |
| 6. Section Library | 17개 랜딩페이지 패턴 | ★★★☆☆ |
| 7. Redesign Protocol | Scan-Diagnose-Fix | ★★★☆☆ |
| 8. Accessibility & SEO | WCAG 2.1 AA | ★☆☆☆☆ |
| 9. Output Enforcement | 잘림 방지 + PAUSE/CONTINUE | ★★☆☆☆ |
| 10. Performance Guardrails | GPU 최적화 | ★☆☆☆☆ |
| 11. Pre-Output Checklist | 최종 검증 | ★★☆☆☆ |

---

## 2. 창의성 엔진의 3대 핵심 메커니즘

### 2.1 VIBE 프리셋 시스템 (Section 1 + 5)

forge의 가장 독창적인 메커니즘. 5개 VIBE(dark/warm/clean/bold/soft) 중 하나를 선택하면 **16개 하위 속성이 자동 연동**된다.

```
VIBE 선택 (1개)
  └→ 16개 속성 일괄 세팅
     ├── DESIGN_VARIANCE (5~9)
     ├── MOTION_INTENSITY (4~8)
     ├── VISUAL_DENSITY (3~5)
     ├── RADIUS (0px~24px)
     ├── SHADOW (none~ultra-soft)
     ├── BORDER (none~thick 3px)
     ├── TEXTURE (none~mesh gradient)
     ├── SECTION_RHYTHM (교차 패턴)
     ├── FONT_DISPLAY (서체 방향)
     ├── HOVER_STYLE (인터랙션)
     ├── LETTER_SPACING (-0.05em~0.02em)
     ├── TYPO_RANGE (크기 범위)
     └── ACCENT_STYLE (강조색 체계)
```

**핵심 원리:** "속성 간 일관성이 '사람이 만든 느낌'을 만든다" (v2.0 설계 원칙). 독립적으로 속성을 조합하면 어색해지므로 프리셋 단위로만 연동한다.

### 2.2 Anti-Pattern Registry (Section 3)

RLHF가 생성하는 "AI 티"를 **패턴 단위로 명시적 금지**하는 블랙리스트 방식.

| 카테고리 | 금지 패턴 예시 | RLHF 동질성과의 관계 |
|----------|---------------|---------------------|
| 타이포 | Inter, Noto Sans KR, Roboto 금지 | RLHF가 학습 빈도 높은 폰트를 기본값으로 선호 |
| 색상 | 보라/파랑 AI 그라디언트 금지 | SaaS 학습 데이터의 평균 색상 |
| 레이아웃 | 3열 균등 카드 금지 | RLHF가 "안전한" 대칭 레이아웃으로 수렴 |
| 콘텐츠 | "혁신적인", "차세대" 금지 | AI 클리셰 표현 |
| 숫자 | 50,000+ 같은 라운드 넘버 금지 | 인간이 만든 느낌의 47,200+ 등 유기적 숫자 |
| 출력 | "계속할까요?" 같은 중단 패턴 금지 | RLHF의 stopping pressure |

### 2.3 Creative Variance Engine (Section 5)

DESIGN_VARIANCE 값에 따라 레이아웃 다양성을 강제하는 엔진.

- `DESIGN_VARIANCE > 4` → 중앙 정렬 Hero 금지
- 인접 섹션은 반드시 다른 레이아웃 패턴 사용
- 3가지 레이아웃 아키타입: Asymmetrical Bento Grid / Z-Axis Cascade / Editorial Split

---

## 3. research/laziness 폴더: RLHF 억제 자체 연구

forge에는 별도의 research 폴더가 있어서 RLHF 억제 문제를 체계적으로 연구하고 있다.

### 3.1 Root Causes (근본 원인 분석)

| 파일 | 핵심 발견 |
|------|-----------|
| rlhf-and-compute.md | RLHF가 경제적 인센티브로 간결성(brevity)을 선호하게 훈련. "stopping pressure"가 공격적으로 보정됨 |
| training-data-bias.md | 학습 데이터의 플레이스홀더 패턴이 모델 출력에 전파 |
| cognitive-shortcuts.md | LazyBench 연구 — 모델이 작업을 "쉽다"고 인식하면 분석 깊이를 스스로 줄임. 12월 계절적 간결화 현상 |
| output-limits.md | 컨텍스트 윈도우 비대칭 + 소비자 티어 잘림 메커니즘 |

### 3.2 Remediation (해결 방법)

| 파일 | 핵심 기법 |
|------|-----------|
| parameter-tuning.md | Temperature/Top-p 조절. 저온=결정적, 고온=다양성. Gemini thinking_level 설정 |
| prompt-engineering.md | 심리적 패턴 매칭("$200 팁" +45%), XML 구조화, 검증 루프(CoV, Self-Grading) |
| architectural-patterns.md | MCP 통합, lazy-loaded 스킬 아키텍처 |
| reference-prompts.md | 즉시 사용 가능한 프롬프트 템플릿 |

### 3.3 Empirical Results (실증 결과)

2025년 12월 통제 실험 3건의 핵심 결론: **"Laziness(게으름)는 메모리 실패가 아니라 정렬 훈련(alignment training)의 행동적 부산물이다."**

- 실험 A: 복잡한 프롬프트에서 필수 출력 섹션을 일관되게 생략
- 실험 B: 잘림은 디코딩 오류가 아니라 의도적 행동 선택
- 실험 C: 200턴 대화에서도 컨텍스트 유지력은 양호 — 맥락 상실이 원인 아님

---

## 4. 01_ 연구보고서와의 대조 분석

### 4.1 같은 문제, 다른 접근

| 차원 | 01_ 보고서 (학술 연구 기반) | supanova-forge (실무 경험 기반) |
|------|---------------------------|-------------------------------|
| 문제 정의 | "RLHF Homogeneity" | "AI 티", "제네릭 느낌" |
| 해결 철학 | 연속형 수치 파라미터 (0-100) | 이산형 프리셋 선택 (5개 VIBE) |
| 창의성 축 | 7차원 독립 좌표계 | 16개 연동 속성 |
| 금지 체계 | 없음 (긍정적 지시만) | Anti-Pattern Registry (명시적 블랙리스트) |
| 학술 근거 | ICLR/EMNLP/Nature 12건 | Microsoft Research + LazyBench + 자체 실험 |
| 적용 범위 | 범용 (글쓰기, 디자인, 리서치) | 디자인 전용 (HTML 랜딩페이지) |

### 4.2 파라미터 매핑: 01_ 7차원 ↔ forge 16속성

01_ 보고서의 7차원 창의성 해제 파라미터가 forge의 어떤 속성에 대응하는지:

| 01_ 파라미터 | forge 대응 속성 | 매핑 관계 |
|-------------|----------------|-----------|
| 대칭 파괴 (Symmetry Break) | DESIGN_VARIANCE | 직접 대응. forge에서 >4면 중앙정렬 금지 |
| 색상 긴장 (Color Tension) | ACCENT_STYLE + Section 3 색상 금지 | forge는 "보라/파랑 금지"로 역방향 제어 |
| 구조 비선형 (Layout Non-linearity) | Section Library + 인접 섹션 다변화 규칙 | forge는 패턴 라이브러리로 구조 다양성 보장 |
| 타이포 대비 (Typographic Contrast) | TYPO_RANGE + LETTER_SPACING + FONT_DISPLAY | forge가 더 정밀. VIBE별 서체/크기/자간 연동 |
| 여백 불규칙 (Whitespace Irregularity) | VISUAL_DENSITY + SECTION_RHYTHM | forge는 밀도+리듬 2축으로 분리 |
| 감정 밀도 (Emotional Density) | Korean Content Standards (Section 4.6) | forge는 AI 클리셰 금지 + 한국어 자연스러움으로 간접 제어 |
| 시각 서사 (Visual Narrative) | Section Library 순서 + MOTION_INTENSITY | forge는 섹션 순서 공식으로 서사 구조를 강제 |

### 4.3 forge에는 있지만 01_에는 없는 것

1. **Anti-Pattern Registry** — 01_은 "이렇게 해라"(긍정적 지시)만 있고, forge는 "이건 절대 하지 마라"(부정적 금지)도 있음. 연구에 따르면 LLM은 "하지 마라" 지시도 효과적으로 따르며, 두 방식을 조합하면 더 강력.

2. **VIBE 프리셋 연동** — 01_은 7차원을 독립적으로 조절하지만, forge는 16속성이 서로 일관성을 유지하도록 프리셋 단위로 묶음. forge v2.0의 핵심 통찰: "독립적 속성 조합은 어색함을 만든다."

3. **Output Enforcement** — PAUSE/CONTINUE 프로토콜, 잘림 방지 규칙. 이건 창의성이 아니라 완성도 문제지만, research/laziness가 보여주듯 RLHF 억제의 다른 측면.

4. **실제 금지 폰트/색상/레이아웃 목록** — 구체적으로 Inter, Noto Sans KR, #000000, 3열 균등 카드 등을 명시. 01_은 추상적 파라미터만 있음.

### 4.4 01_에는 있지만 forge에는 없는 것

1. **연속형 수치 스케일** — forge는 5개 이산 프리셋만 있어서 VIBE 사이의 미세 조절이 불가. "warm인데 대칭 파괴는 85%로" 같은 요청을 처리 못함.

2. **TTCT 4차원 가중치** — 유창성/유연성/독창성/정교성 차원별 우선순위 지정. forge는 이런 인지과학 기반 프레임이 없음.

3. **고착 방지 지시 (Level 3)** — "첫 번째 접근법 쓰지 마", "가정 뒤집기" 같은 CoT 고착 해제 기법. forge는 Anti-Pattern으로 결과물을 제한하지만, 사고 과정 자체를 바꾸지는 않음.

4. **멀티에이전트 건설적 대립 (Level 4)** — EMNLP 2025 연구 기반. forge는 단일 에이전트 구조.

5. **Temperature vs 프롬프트 수치화의 구분** — forge의 research/laziness에서 temperature를 다루지만, 프롬프트 수치화와의 레이어 차이(noise vs signal)를 명시적으로 구분하지 않음.

---

## 5. 핵심 발견 요약

### 5.1 forge가 이미 해결하고 있는 것

forge는 01_ 보고서가 학술적으로 규명한 문제를 **실무적 직관으로 이미 풀고 있었다.**

- RLHF 동질성 → Anti-Pattern Registry로 블랙리스트 제거
- 대칭 파괴 → DESIGN_VARIANCE > 4면 중앙정렬 금지
- 색상 동질성 → 보라/파랑 그라디언트 명시적 금지
- 타이포 단조로움 → VIBE별 서체/크기/자간 연동 시스템
- 구조 고착 → 인접 섹션 다변화 강제 규칙

### 5.2 01_ 보고서가 추가하는 가치

01_ 보고서는 forge의 실무적 접근에 **학술적 근거와 확장 가능성**을 부여한다.

- forge의 "AI 티 제거"가 왜 작동하는지의 메커니즘 설명 (RLHF brevity bias, Salieri 효과)
- 이산형 프리셋을 넘어 연속형 미세 조절의 가능성
- 디자인을 넘어 글쓰기/리서치/분석으로의 확장
- CoT 고착 해제, 멀티에이전트 대립 같은 새로운 기법 층

### 5.3 두 접근법의 통합 방향

가장 강력한 구조는 **2단계 아키텍처**:

```
[1단계: VIBE 프리셋 선택 — forge 방식]
  → 5개 중 하나를 골라 16속성 일괄 세팅
  → 속성 간 일관성 보장 (forge v2.0의 핵심 통찰)

[2단계: 연속형 파라미터 미세 조절 — 01_ 방식]
  → 선택된 VIBE 내에서 7차원 0-100 스케일로 미세 튜닝
  → TTCT 4차원 가중치로 독창성 방향 지정
  → 고착 방지 + 건설적 대립으로 사고 과정 자체 개선
```

이 구조에서 1단계는 "어색함 방지"(속성 간 일관성), 2단계는 "독창성 증폭"(의미적 레벨 탐색 방향)을 각각 담당한다.

---

## 6. research/laziness와 01_ 학술 연구의 정렬도

forge의 자체 연구(research/laziness)와 01_ 보고서의 학술 연구가 얼마나 일치하는지:

| 주제 | forge research | 01_ 학술 연구 | 일치도 |
|------|---------------|--------------|--------|
| RLHF가 간결성을 선호하게 만든다 | rlhf-and-compute.md | Yejin Choi ICLR 2025 (30.1% 창의성 하락) | ★★★★★ 완전 일치 |
| 잘림은 메모리 실패가 아니라 행동 선택 | empirical-results.md 실험B | Nature 2025 Dual Mechanisms | ★★★★☆ |
| Temperature는 창의성 파라미터가 아니다 | parameter-tuning.md | ICCC 2024 논문 | ★★★★☆ |
| 심리적 프롬프트 자극이 효과적 | prompt-engineering.md ($200 팁 +45%) | EmotionPrompt Microsoft Research | ★★★★★ 동일 출처 |
| 검증 루프(CoV)가 품질을 올린다 | prompt-engineering.md | Scaffolding Creativity 2025 | ★★★★☆ |
| 계절적 행동 변화 | cognitive-shortcuts.md (12월 간결화) | 01_에는 미포함 | — |
| LazyBench 인지 지름길 | cognitive-shortcuts.md | 01_에는 미포함 | — |

forge의 자체 연구와 01_의 학술 연구는 **80% 이상 동일한 결론**에 도달하고 있다. forge가 실무 실험에서 먼저 발견한 것을 01_의 학술 논문이 이론적으로 뒷받침하는 구조.

---

## 7. taste-skill 원본: "Anti-Generic" 철학의 기원

forge의 archive에 보존된 taste-skill 원본(Leon, @lexnlin)이 창의성 엔진의 철학적 뿌리다.

### 원본의 핵심 설계 원칙

1. **"If it looks like a template, it fails"** — 템플릿처럼 보이면 실패
2. **DESIGN_VARIANCE 8/10** — 기본값부터 높은 비대칭성
3. **"THE LILA BAN"** — 보라/파랑 AI 그라디언트 명시적 금지
4. **"ANTI-SLOP FONTS"** — Inter, Noto Sans KR 금지

이 원본에서 forge v1.0(4스킬 통합) → v2.0(VIBE 프리셋 연동)으로 발전하면서, 직관적 금지 규칙이 **구조화된 프리셋 시스템**으로 성숙했다. 01_ 보고서가 이 전체 계보에 학술적 근거를 부여하는 세 번째 층이 된다.

```
[Layer 1] taste-skill — 직관적 금지 ("AI 티 나면 안 돼")
[Layer 2] supanova-forge — 구조화된 프리셋 (VIBE 연동 16속성)
[Layer 3] 01_ 연구보고서 — 학술적 근거 (RLHF 억제 메커니즘 + 수치화 해제)
```

---

## 관련 문서

### 직접 참조 (Direct Links)
- [[01_RLHF_창의성해제_AB실험_연구보고서.md|01_ RLHF 창의성 해제 연구보고서]] — 학술 연구 기반 분석 + A/B 실험
- [[A_generic_saas.html|A안 — RLHF 억제 상태 SaaS]] — A/B 실험 통제군
- [[B_creative_saas.html|B안 — 창의성 해제 파라미터 적용]] — A/B 실험 실험군
- [[디자인스킬_세팅시스템_비교분석.md|디자인 스킬 세팅 시스템 비교 분석]] — VIBE 프리셋 설계 배경

### 역참조 (Backlinks)
- (supanova-forge v3 통합 설계 문서에서 참조 예정)

### 관련 주제 (Topic Links)
- [[적용_기술스택_정의서.md|적용 기술스택 정의서]] — forge의 기술 스택 맥락
- [[프롬프트_가이드.md|프롬프트 가이드]] — 프롬프트 엔지니어링 가이드

---

## Release Notes

### v1.0.0 (2026-03-22)
- 초기 작성: supanova-forge 전체 구조 분석 (SKILL.md + research/ + archive/)
- 01_ 연구보고서와의 7차원 파라미터 ↔ 16속성 대조 매핑
- 3계층 진화 계보 정리 (taste-skill → forge → 학술 근거)
- 두 접근법 통합 방향 (2단계 아키텍처) 제안
> **프롬프트:** "supanova-forge의 창의성 엔진 분석 + 01_ 연구보고서와 대조"
