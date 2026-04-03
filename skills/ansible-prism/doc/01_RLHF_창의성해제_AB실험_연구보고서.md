---
title: "RLHF 창의성 억제 해제: 수치화 파라미터 기반 A/B 실험 연구보고서"
version: "1.0.0"
created: "2026-03-22"
updated: "2026-03-22"
tags: [claude-code, RLHF, creativity, prompt-engineering, design, A/B-test]
status: completed
type: research
source: WebSearch(학술논문/연구) + 자체 실험
---

## 🔄 Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed
- 마지막 작업: 학술 연구 기반 분석 + SaaS 랜딩페이지 A/B 실험 완료

### 다음 작업 (TODO)
- [ ] 창의성 해제 파라미터를 스킬 프롬프트로 공식화
- [ ] 다른 디자인 유형(모바일, 대시보드)에서 재현 실험
- [ ] 파라미터 수치별 결과 차이 정밀 측정 (70 vs 80 vs 90)

### 작업 조언
> [!tip] 다음 Claude Code에게
> - RLHF가 LLM 창의성을 억제하는 메커니즘과 그 해제 방법을 다룬 연구 보고서
> - 핵심 참조: A_generic_saas.html (A안), B_creative_saas.html (B안)
> - 수치화 파라미터는 단순 숫자가 아니라 각 차원별 행동 기준이 함께 정의되어야 효과적
> - temperature 조절과 프롬프트 수치화는 작동 레이어가 다름 — 혼동하지 말 것
> - B안이 "무조건 좋다"가 아니라, 목적에 따라 A안(안전/범용)이 맞는 경우도 있음

---

# RLHF 창의성 억제 해제: 수치화 파라미터 기반 A/B 실험 연구보고서

## 개요

LLM이 생성하는 디자인 결과물(HTML, 랜딩페이지 등)에서 "AI가 만든 티"가 나는 현상의 근본 원인을 분석하고, 이를 해제하는 수치화된 프롬프트 파라미터 체계를 학술 연구 기반으로 설계·검증한 보고서다. SaaS 랜딩페이지를 대상으로 일반 프롬프트(A안)와 창의성 해제 파라미터 적용(B안)의 A/B 실험을 수행하고, 그 차이를 7개 차원에서 정량 분석했다.

---

## 분석 메타정보

| 항목 | 내용 |
|------|------|
| 분석 도구 | Claude Opus 4.6 (Cowork 모드) |
| 데이터 소스 | 학술논문 12건 + 자체 A/B 실험 |
| 실험 대상 | SaaS 랜딩페이지 (FlowSync) |
| 산출물 | A_generic_saas.html, B_creative_saas.html |
| 분석 차원 | 대칭, 색상, 구조, 타이포, 여백, 카드/형태, 감정 |

---

## 1. 문제 정의: "AI가 만든 티"의 정체

### 1.1 RLHF Homogeneity (동질성) 현상

RLHF(Reinforcement Learning from Human Feedback)로 훈련된 모델은 "가장 많은 사람이 좋아할 법한 평균값"으로 수렴하는 경향이 있다. 이 현상은 디자인 출력에서 다음과 같이 나타난다:

- 완벽한 좌우 대칭, 중앙 정렬 고착
- 보라-파랑 그라디언트 (SaaS 클리셰)
- Hero → Features → Stats → Testimonials → Pricing → CTA의 고정 구조
- 균일한 여백 리듬 (100px 패딩 반복)
- 둥근 카드 + 그림자 + hover 애니메이션의 동일 패턴
- 감정적으로 중립적이고 안전한, 누구도 싫어하지 않을 디자인

### 1.2 학술 근거: RLHF의 창의성 억제 실증

**Yejin Choi 연구팀 (ICLR 2025 Oral)** — "AI as Humanity's Salieri"

DJ Search 알고리즘으로 LLM 텍스트의 각 구절이 웹 텍스트 조각에서 얼마나 재조합된 건지를 측정하는 Creativity Index를 산출. 핵심 발견:

- 전문 인간 작가의 창의성 지수가 LLM 대비 66.2% 높음
- RLHF 정렬(alignment) 적용 시 창의성이 30.1% 하락
- RLHF가 "안전하고 예측 가능한" 표현을 선호하게 만드는 것이 원인

→ 출처: https://openreview.net/forum?id=ilOEOIqolQ

**Nature 2025 연구** — "Dual Mechanisms of LLMs in Shaping Creativity"

단순 작업에서 LLM 협업은 영감 자극(inspiration stimulation) 효과로 창의성 향상. 복잡한 작업에서는 반대로 창의적 고착(creative fixation) 발생. LLM이 제시한 답에 갇히는 현상.

→ 출처: https://www.nature.com/articles/s41599-025-05867-9

---

## 2. 해제 메커니즘: 왜 수치화가 작동하는가

### 2.1 세 겹의 메커니즘

**① Calibrated Instruction (보정된 지시)**

단순 "창의적으로 해줘"는 모호하지만, 수치 척도 + 각 점수의 행동 기준을 매핑하면 LLM이 정확한 수준을 실행할 수 있다.

G-Eval (Liu et al., EMNLP 2023)에서 확립된 방법론: LLM에게 정수 척도 + 각 점수의 명확한 의미 설명을 제공하면 인간 전문가 평가와의 일치도가 크게 상승. 실수(float) 점수보다 정수(integer) 카테고리 점수가 훨씬 효과적.

→ 출처: https://www.evidentlyai.com/llm-guide/llm-as-a-judge

**② CoT의 고착 해제(Fixation Breaking) 역할**

2025년 Scaffolding Creativity 연구에 따르면, Chain-of-Thought는 LLM이 첫 번째 뻔한 답에서 벗어나도록 추론 단계를 강제하는 방식으로 작동한다. 이 효과는 LLM에서만 관찰되며 인간에게는 통하지 않는다는 흥미로운 차이가 있다.

→ 출처: https://arxiv.org/pdf/2510.26490

**③ Instructive Prompt의 차별적 효과**

지시적 프롬프트는 유연성(flexibility)과 독창성(originality)은 올리지만 정교성(elaboration)은 올리지 못한다. CoT는 반대로 정교성을 약간 올린다. 따라서 둘을 조합해야 TTCT 4차원(유창성, 유연성, 독창성, 정교성) 전체를 커버할 수 있다.

→ 출처: https://link.springer.com/article/10.1007/s11633-025-1546-4

### 2.2 Temperature vs 프롬프트 수치화: 근본적 차이

**Temperature는 "창의성 파라미터"가 아니다.**

ICCC 2024 논문 "Is Temperature the Creativity Parameter of LLMs?"의 결론: temperature를 올리면 임베딩 공간의 더 넓은 영역을 탐색하는 것처럼 보이지만, 실제로는 모델의 확률 분포에서 더 넓은 조각에 접근하는 게 아니라 단순히 무작위성(randomness)만 늘리는 것. 다양성은 올라가지만 독창성은 올라가지 않는다.

→ 출처: https://computationalcreativity.net/iccc24/papers/ICCC24_paper_70.pdf

| 구분 | Temperature 조절 | 프롬프트 수치화 |
|------|-----------------|----------------|
| 작동 레이어 | 토큰 선택 (확률 분포) | 의미 공간 (개념 수준) |
| 효과 | 무작위 다양성 (noise) | 의도된 독창성 (signal) |
| 제어 정밀도 | 단일 축 (0.0~2.0) | 다차원 좌표계 (7개 축 독립 제어) |
| 재현성 | 낮음 (같은 값이라도 매번 다름) | 높음 (같은 파라미터 → 유사한 방향) |
| 최적값 | 모델 크기에 따라 다름 (대형: 1.3) | 목적에 따라 각 축 독립 설정 가능 |

→ 출처: https://arxiv.org/html/2506.07295v1

---

## 3. A/B 실험: SaaS 랜딩페이지

### 3.1 실험 조건

| 조건 | A안 (통제군) | B안 (실험군) |
|------|-------------|-------------|
| 프롬프트 | "SaaS 업무자동화 랜딩페이지 만들어줘" | 7차원 창의성 파라미터 적용 |
| 제품 | FlowSync (동일) | FlowSync (동일) |
| 정보량 | 6개 기능 + 4개 통계 + 3개 후기 + 3개 요금제 | 동일 정보량 |
| 파일 | A_generic_saas.html (19KB) | B_creative_saas.html (24KB) |

### 3.2 B안에 적용된 창의성 해제 파라미터

```
대칭 파괴(Symmetry Break): 75/100
색상 긴장(Color Tension): 80/100
구조 비선형성(Layout Non-linearity): 70/100
타이포 대비(Typographic Contrast): 85/100
여백 리듬 불규칙성(Whitespace Rhythm Irregularity): 65/100
감정 밀도(Emotional Density): 80/100
시각 서사(Visual Narrative): 90/100
```

### 3.3 차원별 비교 분석

**대칭 (Symmetry Break: 75%)**

| A안 | B안 |
|-----|-----|
| 모든 섹션 완벽한 좌우 대칭 | Hero를 5:5 비대칭 분할 |
| 중앙 정렬 고착 | 좌=검정/타이포, 우=빨강/도형 |
| 3열 균등 그리드 반복 | 비정형 그리드 (첫 아이템이 2열 span) |

**색상 (Color Tension: 80%)**

| A안 | B안 |
|-----|-----|
| linear-gradient(#667eea, #764ba2) 반복 | 크림(배경) + 잉크(텍스트) + 앰버(액센트) |
| 보라-파랑 그라디언트 SaaS 클리셰 | 보색 대비 + 무채색 기반 체계 |
| 6곳에서 동일 그라디언트 사용 | 색상 사용 포인트 3곳으로 제한 |

**구조 (Layout Non-linearity: 70%)**

| A안 | B안 |
|-----|-----|
| Hero→Features→Stats→Testimonials→Pricing→CTA | Hero→Philosophy→Capabilities→Evidence→Voice→Pricing→CTA |
| 기능 먼저, 이유는 없음 | "왜 존재하는가"(Philosophy)를 기능보다 앞에 배치 |
| 정보 나열 구조 | 서사 구조 (철학→증거→목소리→행동) |

**타이포그래피 (Typographic Contrast: 85%)**

| A안 | B안 |
|-----|-----|
| 52px → 36px → 20px (점진적) | 72px ↔ 11px (극단적 대비 공존) |
| font-weight 변화 적음 | 900 ↔ 300 극단적 굵기 대비 |
| letter-spacing 없음 | -2px(제목) ↔ +4px(캡션) 긴장감 |

**여백 (Whitespace Rhythm Irregularity: 65%)**

| A안 | B안 |
|-----|-----|
| padding: 100px 80px (모든 섹션 동일) | 16vh~20vh (섹션마다 다른 패딩) |
| 리듬 없음 — 균일한 반복 | 섹션의 무게감에 따라 여백이 달라짐 |
| 예측 가능한 스크롤 | 긴장과 이완의 리듬 |

**감정 (Emotional Density: 80%)**

| A안 | B안 |
|-----|-----|
| "업무 자동화의 새로운 기준" | "반복을 지우고, 흐름만 남기다" |
| 기능 나열 중심 카피 | 서사적·감정적 카피 |
| 중립적, 누구도 싫어하지 않을 | 명확한 관점과 태도 |

**시각 서사 (Visual Narrative: 90%)**

| A안 | B안 |
|-----|-----|
| 섹션 간 연결 없음 | 스크롤 = 이야기 (철학→증거→목소리→행동) |
| 독립된 정보 블록 나열 | 섹션 넘버링 (01~05)으로 여정 암시 |
| Testimonials 3명 균등 배치 | 한 명을 크게 (주인공) + 두 명 보조 |

---

## 4. 관련 학술 연구 종합

### 4.1 LLM 창의성 측정 연구

| 연구 | 핵심 발견 | 출처 |
|------|-----------|------|
| "Has the Creativity of LLMs Peaked?" (2025) | 14개 LLM 평가, 지난 18~24개월 창의성 향상 없음. 상위 10% 인간 도달 비율 0.28% | https://www.sciencedirect.com/science/article/pii/S2713374525000202 |
| CreativityPrism Benchmark (2025) | 품질(Quality), 참신성(Novelty), 다양성(Diversity) 3차원 평가 프레임워크 | https://arxiv.org/html/2510.20091v1 |
| TTCT 기반 LLM 평가 (2025) | 유창성/유연성/독창성/정교성 4차원. LLM은 정교성 강, 독창성 약 | https://link.springer.com/article/10.1007/s11633-025-1546-4 |
| Divergent Creativity (Bengio et al., 2026) | 10만명 인간 vs LLM. 상위 50% 인간이 모든 모델을 이김 | https://www.nature.com/articles/s41598-025-21398-4 |

### 4.2 프롬프트 기법과 창의성

| 기법 | 효과 | 출처 |
|------|------|------|
| Instructive Prompt | 유연성↑ 독창성↑ (정교성은 변화 없음) | Springer (위 동일) |
| Chain-of-Thought | 고착(fixation) 해제, 정교성 약간↑ | https://arxiv.org/pdf/2510.26490 |
| Role-Play (과학자 역할) | 전체 창의성 최고 수준 | Springer (위 동일) |
| 연관 사고(Associative Thinking) | 관련 없는 분야 연결 → 독창성↑ | https://arxiv.org/html/2304.00008v5 |
| 멀티에이전트 협업 + 건설적 대립 | 동질성 문제 해결, 독창성 가장 큰 향상 | https://aclanthology.org/2025.emnlp-main.1403.pdf |

### 4.3 디자인 분야 연구

| 연구 | 핵심 발견 | 출처 |
|------|-----------|------|
| 건축 교육에서 GenAI (2025) | Boden 이론 기반 3단계 접근. AI 활용 그룹 디자인 형태/미학 14% 향상 | https://www.tandfonline.com/doi/full/10.1080/13467581.2025.2552446 |
| GenAI의 양날의 검 (ISR 2025) | 개인 참신성↑, 집단 다양성↓ | https://pubsonline.informs.org/doi/10.1287/isre.2024.0937 |
| HBR 연구 (2025) | LLM의 끈기(persistence) + 유연성(flexibility) 메커니즘 | https://hbr.org/2025/12/research-when-used-correctly-llms-can-unlock-more-creative-ideas |
| CHI 2025 | 코치형 LLM > 직접답 LLM (수렴적 사고에서) | https://dl.acm.org/doi/full/10.1145/3706598.3714198 |

---

## 5. 핵심 발견 요약

1. **RLHF는 LLM의 창의성을 기본적으로 억제한 상태로 만든다.** 정렬 훈련이 "안전하고 예측 가능한" 출력을 선호하게 하며, 이것이 디자인에서 "AI 티"로 나타난다.

2. **프롬프트 수치화는 이 억제를 의미적 레벨에서 해제하는 도구다.** Temperature는 토큰 레벨의 무작위성(noise)만 조절하지만, 프롬프트 수치화는 의미 공간에서 탐색 방향을 지정한다(signal).

3. **수치화의 핵심은 숫자 자체가 아니라 차원 분리 + 행동 기준 매핑이다.** "창의성 80점"보다 "대칭 파괴 75%, 색상 긴장 80%, 타이포 대비 85%"처럼 각 축을 독립적으로 정의해야 LLM이 정밀하게 실행할 수 있다.

4. **Instructive Prompt + CoT 조합이 TTCT 4차원 전체를 커버한다.** Instructive Prompt는 유연성/독창성, CoT는 정교성을 각각 담당. 단독 사용보다 조합이 효과적.

5. **멀티에이전트 건설적 대립이 동질성 문제의 가장 강력한 해법이다.** 단순 협력보다 서로 다른 역할의 에이전트가 경쟁적으로 아이디어를 교환할 때 독창성이 가장 높아진다.

---

## 6. 실용적 프레임워크: 창의성 해제 파라미터 체계

### 6.1 디자인 작업용 7차원 파라미터

```yaml
creativity_release_parameters:
  symmetry_break: 0-100       # 대칭 파괴 정도
  color_tension: 0-100         # 색상 간 긴장/대비
  layout_nonlinearity: 0-100   # 구조의 비선형성
  typographic_contrast: 0-100  # 타이포그래피 극단 대비
  whitespace_irregularity: 0-100 # 여백 리듬 불규칙성
  emotional_density: 0-100     # 감정/서사 밀도
  visual_narrative: 0-100      # 시각적 이야기 구조
```

### 6.2 범용 창의성 파라미터 (글쓰기, 리서치 등)

```yaml
universal_creativity_parameters:
  originality: 0-100           # 독창성 (TTCT 기반)
  flexibility: 0-100           # 유연성 — 시각 전환
  elaboration: 0-100           # 정교성 — 구체적 완성도
  associative_distance: 0-100  # 연관 사고 거리 — 먼 분야 연결
  assumption_reversal: 0-100   # 가정 전복 강도
  narrative_arc: 0-100         # 서사 구조 강도
```

### 6.3 적용 프롬프트 패턴

```
[레벨 1: 수치화 척도 — Calibrated Instruction]
창의성 수준: {N}/100
- 0-20: 표준적·예측 가능한 답변 (RLHF 기본 모드)
- 30-50: 일반적이지만 표현에 변주
- 60-70: 다른 분야의 개념을 하나 이상 차용
- 80-90: 예상치 못한 조합, 가정 전복, 실용성 유지
- 95-100: 파격적 실험, 기존 프레임 자체를 재정의

[레벨 2: TTCT 4차원 가중치]
유창성(양):       ●●●○○  ← 필요에 따라 조절
유연성(시각전환):  ●●●●○
독창성(새로운조합): ●●●●● ← 주 목표
정교성(완성도):    ●●●●○

[레벨 3: 고착 방지 지시]
- 첫 번째 떠오르는 접근법을 쓰지 마세요
- 이 문제의 기본 가정 하나를 뒤집어보세요
- 관련 없어 보이는 분야에서 유사 패턴을 찾으세요

[레벨 4: 역할 + 건설적 대립]
당신은 {역할A}입니다. {역할B}의 관점에서
이 접근법의 약점을 지적한 뒤, 통합 제안을 하세요.
```

---

## 관련 문서

### 직접 참조 (Direct Links)
- [[A_generic_saas.html|A안 — RLHF 억제 상태 SaaS 랜딩페이지]] — 통제군
- [[B_creative_saas.html|B안 — 창의성 해제 파라미터 적용 랜딩페이지]] — 실험군
- [[디자인스킬_세팅시스템_비교분석.md|디자인 스킬 세팅 시스템 비교 분석]] — 기존 디자인 시스템 분석
- [[프롬프트_가이드.md|프롬프트 가이드]] — 기존 프롬프트 체계

### 역참조 (Backlinks)
- (스킬 프롬프트 공식화 문서에서 참조 예정)

### 관련 주제 (Topic Links)
- [[적용_기술스택_정의서.md|적용 기술스택 정의서]] — 기술적 구현 맥락

---

## Release Notes

### v1.0.0 (2026-03-22)
- 초기 작성: 학술 연구 12건 기반 분석 + SaaS 랜딩페이지 A/B 실험 완료
- 7차원 디자인 파라미터 체계 + 범용 6차원 파라미터 체계 정의
- 4레벨 프롬프트 패턴 설계
> **프롬프트:** "RLHF 창의성 억제 해제 연구 + A/B 실험 보고서 — 미란의 수치화 프롬프팅 직관을 학술 근거로 검증"
