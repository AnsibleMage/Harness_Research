# ansible-prism

> 하나의 빛이 프리즘에 들어가면 — 무한한 색이 나온다.

**An & Ari의 Creative Generation Engine** — Claude Code용 스킬. 매번 구조적으로 완전히 다른 고품질 한국어 랜딩페이지/홈페이지를 생성합니다.

## 특징

`ansible-prism`은 주제 또는 와이어프레임을 입력받아 프로덕션 수준의 HTML 랜딩페이지를 생성합니다. 핵심 차별점: **같은 디자인이 두 번 나오지 않습니다.** 5개 슬롯 × 20개 값 = 320만 개 이상의 고유 조합으로 매번 다른 시각 정체성, 색상, 페이지 구조, 타이포그래피, 악센트 전략을 보장합니다.

## 모드

| 모드 | 입력 | 출력 |
|------|------|------|
| **CREATE** | 주제만: "인테리어 랜딩페이지 만들어줘" | 콘텐츠 자동 생성 + 디자인 적용 |
| **REDESIGN** | 와이어프레임 HTML 파일 | 콘텐츠 100% 보존 + 시각 완전 변환 |

## 사용법

```
/ansible-prism 인테리어 랜딩페이지 만들어줘
/ansible-prism opt1.html 리디자인해줘
/ansible-prism opt1.html 3개 동시에 만들어줘
```

## 구조

```
ansible-prism/
├── SKILL.md              ← 메인 오케스트레이터
├── README.md             ← 영문 리드미
├── README_KO.md          ← 이 파일
└── references/           ← 9개 엔진 모듈 (3,000줄+)
    ├── CREATIVE_GENERATION_FRAMEWORK.md  ← 코어 엔진
    ├── CREATE_MODE.md                    ← 제로 입력 → 콘텐츠+디자인
    ├── REDESIGN_MODE.md                  ← 와이어프레임 → 시각 변환
    ├── SLOT_ENGINE.md                    ← 5슬롯 × 20값 = 320만 조합
    ├── IMAGE_ENGINE.md                   ← gradient+SVG+AI 이미지
    ├── MOTION_RULES.md                   ← 스크롤 등장+hover 효과
    ├── CSS_PRECISION.md                  ← 4px 그리드+다층 shadow
    ├── VISUAL_DENSITY.md                 ← 7계층 시각 콘텐츠 규칙
    └── TECH_SPEC.md                      ← 출력 기술 명세
```

## 5슬롯 조합 엔진

매 생성 시 5개 독립 슬롯에서 각각 1개씩 선택:

| 슬롯 | 역할 | 값 |
|------|------|-----|
| **Visual Identity** | CSS 변수, border, texture, 카드/nav 스타일 | 20개 |
| **Color Temperature** | 전체 색상 팔레트 (구체적 hex 값) | 20개 |
| **Page Structure** | HTML body 골격 (사이드바, 그리드, 스택, sticky, snap...) | 20개 |
| **Typography** | heading 폰트, 크기 위계, 자간 | 20개 |
| **Accent Strategy** | accent가 나타나는 CSS 속성 (text, border, hover, shadow...) | 20개 |

**"진짜 다름" 4차원 체크:** 모든 생성물은 이전과 4개 차원(구조, 색계열, 폰트 카테고리, 악센트 속성) 모두 달라야 합니다.

## 품질 모듈

| 모듈 | 역할 |
|------|------|
| **IMAGE_ENGINE** | 회색 placeholder 금지. 모든 썸네일에 콘텐츠 카테고리 맞춤 gradient+SVG. |
| **MOTION_RULES** | IntersectionObserver 스크롤 등장, 카드 시차 진입, 섹션별 다른 hover. |
| **CSS_PRECISION** | 4px 간격 그리드, 5단계 색상 깊이, 4+ font-weight, 다층 box-shadow. |
| **VISUAL_DENSITY** | 7계층 시각 위계. 카드당 2+ 텍스트 레벨. 동일 배경 2연속 금지. |

## 출력

- **형식:** 단일 자립형 HTML 파일
- **CSS:** 임베드 `<style>` (CSS Custom Properties)
- **JS:** 임베드 `<script>` (IntersectionObserver, 탭 전환)
- **폰트:** Google Fonts CDN + Pretendard CDN
- **이미지:** 외부 파일 0개 — CSS gradient + inline SVG만
- **접근성:** WCAG 2.1 AA (포커스 스타일, 명암비, 모션 감소)

## Agent Teams (병렬 생성)

여러 버전을 동시에 생성:

```
/ansible-prism opt1.html 3개 동시에 만들어줘
```

각 에이전트는 고유한 슬롯 조합을 부여받으며, 모든 쌍이 4차원 다름 체크를 통과합니다.

## 크레딧

**앤 (An/Ansible)** & **아리 (Ari/Aria)** — AnsibleMage 제작.

## 라이선스

MIT
