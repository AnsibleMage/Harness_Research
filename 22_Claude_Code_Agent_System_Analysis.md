# 07. Claude Code 에이전트 시스템 분석
## Agent Teams + Subagents + Skills 통합 분석

> **분석 범위**: Claude Code Agent Teams, Subagents, Skills 및 3가지 시스템의 통합 관점 분석
> **분석일**: 2026-04-03
> **상태**: Experimental (Agent Teams) / Stable (Subagents, Skills)

---

# Part 1: Agent Teams 분석

> **소스**: https://code.claude.com/docs/ko/agent-teams
> **상태**: Experimental (기본 비활성화, v2.1.32+)

## 1.1 개요

Agent Teams는 **여러 Claude Code 인스턴스를 조율하여 병렬로 협업**시키는 실험적 기능이다. 단일 세션의 Subagent와 달리, 팀원들은 **각자 독립된 컨텍스트 윈도우**를 가지며 **서로 직접 통신**한다.

### 핵심 구조

```
┌─────────────┐
│   Team Leader  │  ← 메인 Claude Code 세션, 팀 생성·조율·종합
├─────────────┤
│  Teammate A    │  ← 독립 인스턴스, 자체 컨텍스트
│  Teammate B    │  ← 독립 인스턴스, 자체 컨텍스트
│  Teammate C    │  ← 독립 인스턴스, 자체 컨텍스트
├─────────────┤
│  Shared Task List  │  ← 공유 작업 목록 (요청/완료/종속성)
│  Mailbox System    │  ← 에이전트 간 메시징
└─────────────┘
```

---

## 1.2 Subagent vs Agent Teams 비교

| 항목 | Subagent | Agent Teams |
|------|----------|-------------|
| **컨텍스트** | 자체 윈도우, 결과만 호출자에게 반환 | 자체 윈도우, 완전히 독립적 |
| **통신** | 메인 에이전트에게만 보고 | 팀원 간 직접 메시지 전송 |
| **조율** | 메인 에이전트가 모든 작업 관리 | 공유 작업 목록 기반 자체 조율 |
| **최적 용도** | 결과만 중요한 집중 작업 | 논의·협업 필요한 복잡한 작업 |
| **토큰 비용** | 낮음 (결과 요약) | 높음 (각 팀원이 별도 인스턴스) |
| **독립성** | 부분적 (메인에 종속) | 완전 (독립 컨텍스트 + 직접 통신) |

**핵심 차이**: Subagent는 "위임-보고" 패턴이고, Agent Teams는 "협업-토론" 패턴이다.

---

## 1.3 아키텍처 상세 분석

### 1.3.1 구성 요소

| 구성 요소 | 역할 | 저장 위치 |
|-----------|------|-----------|
| **Team Leader** | 팀 생성, 팀원 생성, 작업 조율 | 메인 세션 |
| **Teammates** | 할당된 작업에서 독립 작업 | 별도 Claude Code 인스턴스 |
| **Task List** | 공유 작업 항목 (대기/진행/완료) | `~/.claude/tasks/{team-name}/` |
| **Mailbox** | 에이전트 간 비동기 메시징 | 런타임 메모리 |
| **Team Config** | 팀 멤버 정보, 런타임 상태 | `~/.claude/teams/{team-name}/config.json` |

### 1.3.2 작업 관리 메커니즘

- **작업 상태**: 대기 중(pending) → 진행 중(in-progress) → 완료(done)
- **종속성 관리**: 작업 간 dependency 자동 관리, 선행 작업 완료 시 후속 작업 자동 차단 해제
- **할당 방식**: 리더 지정 할당 또는 팀원 자체 요청(self-claiming)
- **경합 방지**: 파일 잠금(file lock)으로 동시 요청 시 race condition 방지

### 1.3.3 통신 시스템

| 통신 유형 | 설명 |
|-----------|------|
| **message** | 특정 팀원 1명에게 메시지 |
| **broadcast** | 전체 팀원에게 동시 전송 (비용 높음, 드물게 사용) |
| **자동 전달** | 팀원 메시지 → 수신자에게 자동 도착 (폴링 불필요) |
| **유휴 알림** | 팀원 완료/중지 시 → 리더에게 자동 알림 |

### 1.3.4 컨텍스트 격리

- 각 팀원은 **독립된 컨텍스트 윈도우** 보유
- 생성 시 로드: CLAUDE.md + MCP servers + Skills + 리더의 생성 프롬프트
- **리더의 대화 기록은 전달되지 않음** ← 구조적 독립성의 핵심
- 팀원 간 정보 공유는 명시적 메시지로만 가능

### 1.3.5 표시 모드

| 모드 | 설명 | 요구사항 |
|------|------|----------|
| **In-process** | 메인 터미널 내, Shift+Down으로 팀원 순환 | 없음 (모든 터미널) |
| **분할 창 (Split pane)** | 각 팀원 별도 창, 한눈에 전체 상황 | tmux 또는 iTerm2 |

---

## 1.4 운영 패턴

### 1.4.1 계획 승인 패턴 (Plan Approval)

```
팀원 생성 (plan mode) → 팀원 계획 수립 → 리더에게 승인 요청
  → 승인: 계획 모드 종료, 구현 시작
  → 거부: 피드백 반영, 재계획, 재제출
```

- 복잡하거나 위험한 작업에 활용
- 리더가 승인 기준 설정 가능 ("테스트 커버리지 포함하는 계획만 승인")
- **하네스 관점**: Plan과 Execute의 구조적 분리를 강제하는 메커니즘

### 1.4.2 Subagent 정의 재사용

- `.claude/agents/` 에 정의된 Subagent 유형을 팀원으로 사용 가능
- 시스템 프롬프트, 도구, 모델 상속
- 한 번 정의 → Subagent와 Teammate 양쪽 모두에서 재사용

### 1.4.3 Hooks를 통한 품질 게이트

| Hook | 트리거 시점 | 활용 |
|------|-----------|------|
| **TeammateIdle** | 팀원 유휴 상태 직전 | 종료 코드 2로 피드백 → 팀원 계속 작동 |
| **TaskCreated** | 작업 생성 시 | 종료 코드 2로 생성 차단 + 피드백 |
| **TaskCompleted** | 작업 완료 표시 시 | 종료 코드 2로 완료 차단 + 피드백 |

**하네스 관점**: Hooks는 **독립적 검증 레이어**로 기능. 팀원(실행자)이 아닌 외부 스크립트(검증자)가 품질을 판단.

### 1.4.4 권한 모델

- 팀원은 리더의 권한 설정 상속
- `--dangerously-skip-permissions` 시 전체 팀 적용
- 생성 후 개별 변경 가능, 생성 시 개별 설정 불가

---

## 1.5 사용 사례 및 최적 패턴

### 1.5.1 최적 사용 사례

| 사용 사례 | 이유 | 팀원 구성 예시 |
|-----------|------|-------------|
| **연구 및 검토** | 다양한 관점의 병렬 탐색 | UX + Architecture + Devil's Advocate |
| **새 모듈/기능** | 각 팀원이 별도 부분 소유 | Frontend + Backend + Test |
| **경쟁 가설 디버깅** | 독립 조사로 앵커링 편향 제거 | 가설 A + 가설 B + 가설 C + ... |
| **교차 계층 조율** | 다른 레이어의 동시 변경 | Frontend + Backend + Test |
| **병렬 코드 리뷰** | 관점별 독립 검토 | Security + Performance + Coverage |

### 1.5.2 부적합 사례

- 순차적 작업 (앞 결과가 뒤 작업의 입력)
- 동일 파일 편집 (덮어쓰기 위험)
- 단순/일상적 작업 (조율 오버헤드 > 이점)
- 많은 종속성이 있는 작업

### 1.5.3 팀 크기 가이드

- **권장**: 3-5명
- **작업 배분**: 팀원당 5-6개 task
- 예시: 15개 독립 작업 → 3명 팀원
- 3명의 집중된 팀원 > 5명의 산만한 팀원

---

## 1.6 제한 사항

| 제한 | 영향 |
|------|------|
| In-process 팀원 세션 재개 불가 | `/resume`, `/rewind` 미지원 |
| 작업 상태 지연 가능 | 종속 작업 차단 위험 |
| 종료 지연 | 현재 도구 호출 완료 후 종료 |
| 세션당 한 팀만 | 동시 다중 팀 불가 |
| 중첩 팀 불가 | 팀원이 하위 팀 생성 불가 |
| 리더 고정 | 리더십 이전/승격 불가 |
| 분할 창 호환성 | VS Code 통합 터미널, Windows Terminal 미지원 |

---

## 1.7 하네스 엔지니어링 관점 (Part 1)

### 1.7.1 Agent Teams가 해결하는 하네스 요소

| 하네스 요소 | Agent Teams 해결 방식 |
|-----|-----|
| **#1 PGE 3-Agent GAN Loop** | Leader(Planner) + Teammate(Generator) + 별도 Teammate(Evaluator)로 구조적 분리 가능 |
| **#14 Skeptical Evaluator** | Devil's Advocate 팀원으로 명시적 비판적 검증자 배치 |
| **#22 Handoff State Machine** | 공유 작업 목록 + 종속성 관리 = 자동 라우팅 |
| **#25 Approval Workflow** | Plan Approval 패턴으로 리더가 게이트키퍼 역할 |
| **#44 Subagent Delegation** | Agent 정의 재사용으로 역할 표준화 |

### 1.7.2 독립성 확보 — 구조적 강제

Agent Teams는 **구조적으로 독립성을 강제**한다:

1. **컨텍스트 격리**: 각 팀원은 독립 컨텍스트. 리더 대화 기록 미전달.
2. **역할 분리**: 계획자 팀원 ≠ 실행자 팀원 ≠ 검증자 팀원
3. **정보 차단**: 팀원 간 정보는 **명시적 메시지**로만 전달 (암묵적 공유 없음)
4. **Plan Approval**: 계획과 실행 사이에 승인 게이트 강제

**핵심**: Subagent는 "같은 세션 안에서 분리"였지만, Agent Teams는 "아예 다른 인스턴스로 분리". 이것이 진정한 의미의 독립성.

### 1.7.3 구체적 하네스 구현 패턴

#### 패턴 A: Plan-Execute-Verify 완전 분리

```
Leader: "팀을 만들어줘"
  ├── Planner Teammate (requirements-analyst agent 타입)
  │     → 요구사항 분석, 작업 분해, 설계 문서 생성
  │     → Plan Approval 요청 → Leader 승인
  │
  ├── Executor Teammate (code-developer agent 타입)
  │     → 승인된 계획 기반 구현 (Planner의 과정은 모름)
  │     → 산출물만 공유 작업으로 완료 표시
  │
  └── Verifier Teammate (quality-reviewer agent 타입)
        → TaskCompleted Hook: 산출물만 받아 독립 검증
        → 실행 과정을 모른 채 산출물 품질만 판정
        → 실패 시 → Leader에게 피드백 (수정 방법은 미포함)
```

#### 패턴 B: 경쟁적 검증 (Adversarial Review)

```
Leader: "이 버그를 조사해줘, 가설을 세워서 서로 반박해"
  ├── Investigator A: 가설 1 조사 + B,C 가설 반박 시도
  ├── Investigator B: 가설 2 조사 + A,C 가설 반박 시도
  └── Investigator C: 가설 3 조사 + A,B 가설 반박 시도

→ 상호 반박을 견딘 가설 = 높은 확률로 진짜 원인
→ 앵커링 편향 구조적으로 제거
```

#### 패턴 C: 교차 검증 리뷰

```
Leader: "PR #142 리뷰해줘"
  ├── Security Reviewer: 보안 관점만 검토
  ├── Performance Reviewer: 성능 관점만 검토
  └── Coverage Reviewer: 테스트 커버리지만 검토

→ 각 검토자는 다른 검토자의 관점을 모름
→ 동일 코드에 대한 독립적 평가 = 편향 없는 다각적 검토
→ Leader가 세 결과를 종합
```

### 1.7.4 Hooks와의 결합 — 외부 검증 레이어

```
Agent Teams (내부 독립성)
  + TaskCompleted Hook (외부 품질 게이트)
  + TeammateIdle Hook (외부 완료 검증)
  = 3중 검증 체계

  1차: 팀원 자체 완료 판단 (실행자 관점)
  2차: 다른 팀원의 독립 검증 (팀 내 독립성)
  3차: Hook 스크립트의 자동 검증 (시스템 수준 독립성)
```

### 1.7.5 기존 Agent/Skill 자산과의 결합

현재 보유한 30개 Agent와 47개 Skill을 Agent Teams 체계로 재구성 시:

| 하네스 단계 | Agent Teams 역할 | 활용 가능 Agent (기존 자산) |
|------------|-----------------|-------------------------|
| **Plan** | Planner Teammate | requirements-analyst, system-architect, complexity-resolver |
| **Execute** | Executor Teammate | code-developer + vibe-dev skill + design skills |
| **Verify** | Verifier Teammate(s) | quality-reviewer, edge-case-reviewer, security-reviewer, logic-reviewer |
| **Analyze** | Analyst Teammate | eval-analyzer, multidimensional-analyst, insight-explorer |
| **Context** | Context Teammate | context-manager, session-memo-writer |
| **Adversarial** | Devil's Advocate | balanced-judge, comparator, problem-reframer |

**기존 30개 Agent → Agent Teams의 팀원 타입으로 즉시 전환 가능**

---

## 1.8 활성화 및 설정 가이드

### 1.8.1 활성화

```json
// settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### 1.8.2 표시 모드 설정

```json
// ~/.claude.json
{
  "teammateMode": "in-process"  // 또는 "tmux", "auto"
}
```

### 1.8.3 Subagent 정의를 팀원으로 활용

```
// .claude/agents/security-reviewer.md 에 정의된 에이전트를
// 팀원으로 생성:
"Spawn a teammate using the security-reviewer agent type to audit the auth module."
```

### 1.8.4 Hooks 설정 (품질 게이트)

```json
// .claude/settings.json
{
  "hooks": {
    "TaskCompleted": [
      {
        "command": "bash .claude/hooks/verify-task.sh"
      }
    ],
    "TeammateIdle": [
      {
        "command": "bash .claude/hooks/check-idle-reason.sh"
      }
    ]
  }
}
```

---

## 1.9 모범 사례 요약

| 원칙 | 내용 |
|------|------|
| **충분한 컨텍스트** | 생성 프롬프트에 작업 세부사항 포함 (리더 대화 기록 미전달) |
| **적절한 팀 크기** | 3-5명, 팀원당 5-6개 task |
| **파일 충돌 방지** | 각 팀원이 다른 파일 집합 소유 |
| **연구/검토 우선** | 코드 작성보다 연구/리뷰로 먼저 경험 |
| **모니터링** | 무인 장시간 운영 금지, 주기적 확인 |
| **대기 지시** | 리더가 선 실행하면 "팀원 완료까지 대기" 지시 |
| **정리 필수** | 작업 완료 후 반드시 리더가 `clean up the team` 실행 |

---

## 1.10 한계 및 리스크

### 1.10.1 기술적 한계
- 실험적 기능 (기본 비활성화)
- 세션 재개 미지원 (in-process 모드)
- 중첩 팀 불가
- 리더 고정 (이전 불가)

### 1.10.2 하네스 관점 리스크
- **토큰 비용 선형 증가**: 팀원 수 × 독립 컨텍스트 = 비용 폭발 가능
- **조율 오버헤드**: 팀원 수 증가 시 통신·조율 복잡도 급증
- **작업 상태 지연**: 종속성 관리 실패 시 전체 파이프라인 차단
- **리더 단일 장애점**: 리더 세션 문제 시 전체 팀 영향

### 1.10.3 Ann의 워크플로우에 대한 고려
- Windows 환경에서 tmux 제한 → in-process 모드 권장
- Claude Desktop (Cowork)과 Claude Code CLI 간 연동 확인 필요
- 실험적 기능이므로 핵심 업무보다 연구/프로토타이핑에 우선 적용 권장

---

# Part 2: Subagents 분석

> **소스**: Claude Code 공식 문서 (Subagents)
> **상태**: Stable

## 2.1 개요 및 개념

Subagent는 **동일 세션 내에서 특정 작업을 위임받은 AI 에이전트**이다. 메인 에이전트가 작업을 할당하면, Subagent는 **제한된 도구 집합과 격리된 컨텍스트** 내에서 독립적으로 작업을 수행하고 결과만 반환한다.

### 핵심 개념

| 개념 | 설명 |
|------|------|
| **컨텍스트 보존** | Subagent는 자체 격리된 컨텍스트 윈도우를 가지며, 메인 세션과는 별도로 운영. 독립적 기억 관리 가능. |
| **제약 적용** | Subagent 정의에서 명시적으로 제약을 설정 (도구 제한, 권한 모드, 최대 턴 수 등) |
| **비용 제어** | Subagent는 토큰을 독립적으로 소비. 메인 세션의 컨텍스트를 증가시키지 않음. |

---

## 2.2 내장 Subagent 타입

Claude Code에는 3가지 기본 제공 Subagent 타입이 있다:

### 2.2.1 Explore Agent

```yaml
# 특징
- Model: Claude Haiku (경량)
- 권한: 읽기 전용 (read-only)
- 도구: 파일 읽기, 코드 검색, 구조 분석만 가능
- 용도: 코드 탐색, 문제 진단, 기초 분석

# 사용 예
"코드베이스에서 인증 로직을 찾아줘"
→ Explore Subagent가 검색하고 분석 결과만 반환
```

### 2.2.2 Plan Agent

```yaml
# 특징
- Model: 메인 세션의 모델 상속 (기본 Claude 3.5 Sonnet)
- 권한: 읽기 전용 (read-only)
- 도구: 제한적 (분석, 검색, 문서화)
- 용도: 계획 수립, 설계 문서 작성, 영향도 분석

# 사용 예
"이 버그를 고치기 위한 변경 계획을 세워줘"
→ Plan Subagent가 계획만 수립 (수정하지 않음)
→ 메인 에이전트가 계획을 검토 후 승인/거부
```

### 2.2.3 General-purpose Agent

```yaml
# 특징
- Model: 메인 세션의 모델 상속
- 권한: 메인 세션의 권한 상속
- 도구: 거의 모든 도구 접근 가능
- 용도: 범용 작업, 코드 생성, 테스트 작성, 배포 등

# 사용 예
"버그를 고쳐줘"
→ General-purpose Subagent가 코드 수정, 테스트 실행 등 모든 작업 가능
```

---

## 2.3 Subagent 범위 및 우선순위

Subagent 정의는 여러 위치에서 찾을 수 있으며, 다음의 우선순위를 따른다:

```
Managed Subagents (Anthropic에서 제공)
  ↓ (찾지 못하면)
CLI Subagents (.claude/agents/*.md)
  ↓ (찾지 못하면)
Project Subagents (.claude/agents/*.md at project root)
  ↓ (찾지 못하면)
User Subagents (~/.claude/agents/*.md)
  ↓ (찾지 못하면)
Plugin Subagents (설치된 플러그인에서 제공)
```

**우선순위**: Managed > CLI > Project > User > Plugin

---

## 2.4 YAML Frontmatter 구성

Subagent는 Markdown 파일로 정의되며, 다음의 frontmatter 필드를 지원한다:

```yaml
---
name: "Code Reviewer"                 # Subagent 이름
description: "코드 품질을 검토하는 에이전트"  # 설명

# 도구 및 능력 제어
tools: ["file_read", "code_search"]  # 허용할 도구 목록 (allowlist)
disallowedTools: ["file_create"]     # 금지할 도구 목록 (denylist)

# 모델 설정
model: "claude-opus-4-20250101"      # 명시적 모델 지정 (생략 시 상속)

# 권한 및 제어
permissionMode: "default"             # 권한 모드 (아래 설명)
maxTurns: 10                         # 최대 턴 수 제한
maxTokens: 50000                     # 최대 토큰 제한

# Skills 사전 로드
skills: ["debug", "code-review"]     # 이 Subagent에서 항상 사용 가능한 Skills

# MCP 서버 범위 지정
mcpServers:
  - name: "github"
    enabled: true

# Hooks (이벤트 핸들러)
hooks:
  PreToolUse: ".claude/hooks/pre-tool-use.sh"
  PostToolUse: ".claude/hooks/post-tool-use.sh"
  SubagentStop: ".claude/hooks/on-stop.sh"

# 메모리 설정
memory:
  scope: "local"                     # local / project / user
  retention: "session"               # session / persistent

# 배경 및 성격
background: "당신은 보안 전문가입니다."
effort: "high"                       # low / medium / high

# 격리 정책
isolation: "strict"                  # strict / moderate / permissive

# UI 표시
color: "blue"                        # 터미널 색상

# 초기 프롬프트
initialPrompt: "당신의 작업은..."
---
```

### 2.4.1 권한 모드 (permissionMode)

| 모드 | 설명 |
|------|------|
| **default** | 각 도구 호출마다 사용자 승인 요청 (느리지만 안전) |
| **acceptEdits** | 파일 수정은 자동 승인, 기타 도구는 요청 |
| **auto** | 모든 도구 자동 승인 (빠르지만 위험) |
| **dontAsk** | `acceptEdits`와 유사하지만 더 제한적 |
| **bypassPermissions** | 모든 권한 검사 무시 (매우 위험) |
| **plan** | 실행하지 않고 계획만 수립. 실행 전 승인 필수 |

---

## 2.5 핵심 기능

### 2.5.1 도구 제한 (Allowlist / Denylist)

```yaml
# 방식 1: Allowlist (화이트리스트)
tools: ["file_read", "code_search", "grep"]
# → 이 도구들만 사용 가능

# 방식 2: Denylist (블랙리스트)
disallowedTools: ["bash", "git_push"]
# → 이 도구들은 사용 불가, 나머지는 모두 가능

# 혼합
tools: ["file_read", "file_edit"]
disallowedTools: ["bash"]
# → file_read, file_edit만 허용되고, 둘 다에 bash는 금지
```

### 2.5.2 Agent 타입 제한 (Agent Inheritance)

```yaml
# 특정 Agent 타입으로 제한
agent: "security-reviewer"
# → security-reviewer로 정의된 Subagent의 속성 상속
# → 한 번 정의 → 여러 곳에서 재사용
```

### 2.5.3 MCP 서버 범위 지정

```yaml
mcpServers:
  - name: "github"
    enabled: true
  - name: "jira"
    enabled: false      # 이 Subagent는 JIRA 접근 불가
  - name: "slack"
    enabled: true
    scopes: ["read", "write"]
```

### 2.5.4 권한 모드 실전 패턴

#### 패턴: Plan + Review + Execute

```
1. Plan Subagent (plan mode)
   → 수정 계획 수립, 메인 에이전트에게 제출

2. Main Agent가 계획 검토
   → 승인 또는 피드백

3. Execute Subagent (auto mode)
   → 승인된 계획 기반 자동 실행
```

---

## 2.6 Skills 사전 로드

Subagent는 특정 Skills를 **항상 사용 가능**하도록 미리 로드할 수 있다:

```yaml
skills: ["debug", "code-review", "testing-strategy"]

# 효과:
# - Subagent 시작 시 자동으로 이 Skills 로드
# - Subagent 내에서 /debug, /code-review, /testing-strategy 즉시 호출 가능
# - 메인 세션과의 컨텍스트 분리 유지
```

---

## 2.7 지속적 메모리 (Persistent Memory)

Subagent는 메모리를 지속적으로 유지할 수 있다:

```yaml
memory:
  scope: "local"        # 현재 Subagent만 (기본)
             # OR
             # "project" = 같은 프로젝트의 모든 에이전트 공유
             # "user" = 사용자 수준의 전역 메모리

  retention: "session"  # 현재 세션 후 삭제
            # OR
            # "persistent" = 영구 보존
```

**메모리 파일**: `.claude/memory/{scope}/MEMORY.md`

```markdown
# Subagent Memory

## Context
- 현재 프로젝트의 아키텍처 결정사항
- 이전 회차에서 발견한 패턴
- 반복되는 이슈 목록

## Lessons Learned
- 이 프로젝트에서 시도한 것들의 결과
- 작동하지 않은 것들의 이유

## TODO
- 다음 회차에서 확인할 항목
```

---

## 2.8 Hooks (이벤트 핸들러)

Subagent는 특정 이벤트에서 외부 스크립트를 호출할 수 있다:

### 2.8.1 Hook 타입

| Hook | 트리거 | 용도 |
|------|--------|------|
| **PreToolUse** | 도구 호출 직전 | 도구 호출 검증, 입력 검증 |
| **PostToolUse** | 도구 호출 직후 | 결과 검증, 로깅, 트리거 |
| **SubagentStop** | Subagent 종료 시 | 정리, 결과 아카이빙 |

### 2.8.2 Hook 예시

```bash
# .claude/hooks/pre-tool-use.sh
#!/bin/bash
TOOL=$1
ARGS=$2

# bash 도구는 금지 (강제 권한 검사)
if [ "$TOOL" = "bash" ]; then
  echo "Bash is not allowed for this agent"
  exit 1
fi

exit 0  # 통과
```

### 2.8.3 Subagent Event Hooks

Agent Teams의 팀원(Subagent 기반)의 경우:

```yaml
hooks:
  SubagentStart: ".claude/hooks/on-start.sh"
  SubagentStop: ".claude/hooks/on-stop.sh"
```

---

## 2.9 작업 패턴

### 2.9.1 자동 위임 (Auto-delegation)

```
Main Agent: "이 버그를 고쳐줘"
  ↓ (자동 판단)
→ Plan Subagent: 계획 수립
→ Main Agent 승인
→ Execute Subagent: 구현
→ Review Subagent: 검증
→ Main Agent: 결과 확인
```

### 2.9.2 @-mention으로 특정 Subagent 호출

```
Main Agent: "@code-reviewer, 이 파일을 검토해줘"
  ↓
→ code-reviewer라는 정의된 Subagent만 실행
→ 결과 반환
```

### 2.9.3 --agent 플래그로 세션 시작

```bash
claude --agent code-reviewer
# → code-reviewer 정의를 기반으로 세션 시작
```

### 2.9.4 Foreground / Background 실행

```
Foreground: 메인 에이전트가 Subagent 완료 대기
Background: Subagent 실행 후 메인 에이전트는 계속 작업
  (백그라운드 Subagent 결과는 나중에 수집)
```

### 2.9.5 Subagent 체인 (Chaining)

```
Subagent A → 결과 → Subagent B → 결과 → Subagent C
  (순차적 작업 분리)
```

### 2.9.6 세션 재개 (Resume)

```
Session 1: Subagent가 작업 중 중단
Session 2: /resume로 같은 Subagent 세션 재개
  (컨텍스트 유지)
```

---

## 2.10 컨텍스트 관리

### 2.10.1 독립 트랜스크립트

각 Subagent는 **독립 트랜스크립트**를 유지한다:

```
Main Session Transcript:
  User: "이 작업을 해줘"
  Claude: "Subagent를 보낼게"
  [Subagent 실행]
  Claude: "완료했어"

Subagent Transcript (별도):
  System: "당신의 작업은..."
  Claude: "작업 시작"
  ...
  Claude: "작업 완료"
```

### 2.10.2 자동 컨텍스트 압축

Subagent가 토큰 제한에 다다르면:

1. 오래된 턴부터 요약
2. 중요 정보만 남김
3. 새로운 턴에서 요약된 컨텍스트로 계속 진행

### 2.10.3 재개 시 컨텍스트 복구

```bash
claude /resume
# → 중단된 Subagent의 마지막 상태 복구
# → 같은 컨텍스트 윈도우에서 계속
```

---

## 2.11 하네스 엔지니어링 관점 (Part 2)

### 2.11.1 Subagent가 해결하는 하네스 요소

| 하네스 요소 | Subagent 해결 방식 |
|-----|-----|
| **#2 Context Partitioning** | 각 Subagent는 독립 컨텍스트 윈도우 보유 |
| **#11 Cost Control** | Subagent 토큰 독립 소비 = 메인 세션 비용 증가 없음 |
| **#17 Tool Restriction** | tools/disallowedTools로 도구 명시적 제한 |
| **#24 Permission Gate** | permissionMode로 세부 권한 제어 |
| **#44 Subagent Delegation** | 정의 재사용으로 역할 표준화 |

### 2.11.2 기존 30개 Agent와의 연계

```
기존 Agent 정의 (.claude/agents/)
  ↓
Subagent로 재사용 가능
  ↓
특정 도구 제한 추가 가능 (Subagent layer)
  ↓
메모리 및 Hooks로 강화 가능
```

---

# Part 3: Skills 분석

> **소스**: Claude Code Skills 공식 문서
> **상태**: Stable

## 3.1 개요

Skills는 **Claude Code의 개방형 표준**으로, 특정 작업을 자동화하거나 반복 가능한 패턴을 캡슐화한다. `SKILL.md` 파일로 정의되며, 메인 에이전트와 Subagent 모두에서 호출 가능하다.

### 핵심 개념

| 개념 | 설명 |
|------|------|
| **개방형 표준** | 누구나 자신의 Skill을 만들고 공유 가능 |
| **절차 캡슐화** | 복잡한 작업을 단순 명령어(예: `/debug`)로 제공 |
| **컨텍스트 주입** | 동적으로 현재 세션의 정보 주입 가능 |
| **조건부 실행** | 특정 조건 하에서만 실행 가능하도록 제약 가능 |
| **Subagent 통합** | Skill 내에서 특정 Subagent를 호출할 수 있음 |

---

## 3.2 번들 Skills (Built-in)

Claude Code에는 다음의 번들 Skills가 포함되어 있다:

### 3.2.1 /batch

```yaml
# 목적: 여러 파일에 일괄 변경 적용
# 사용: /batch "변경 내용" file1.py file2.py file3.py

# 하네스 활용:
# - 동일한 리팩토링을 여러 파일에 병렬 적용
# - 부분 변경으로 인한 불일치 방지
```

### 3.2.2 /claude-api

```yaml
# 목적: Claude API를 직접 호출하는 코드 생성/실행
# 사용: /claude-api "프롬프트 분석 API 호출"

# 하네스 활용:
# - 메인 Claude Code와 별도의 API 호출 가능
# - 작은 모델로 빠른 검증
```

### 3.2.3 /debug

```yaml
# 목적: 구조화된 디버깅 워크플로우 실행
# 사용: /debug <error message>

# 하네스 활용:
# - 에러 격리, 재현, 진단, 수정의 단계별 진행
# - 일관된 디버깅 프로세스
```

### 3.2.4 /loop

```yaml
# 목적: 특정 작업을 반복적으로 실행하고 조건에 따라 중지
# 사용: /loop "작업" --until "조건"

# 하네스 활용:
# - 자동화된 반복 작업 (테스트 반복 실행, 수렴 기다리기 등)
```

### 3.2.5 /simplify

```yaml
# 목적: 코드를 단순하고 읽기 쉽게 리팩토링
# 사용: /simplify <파일 경로>

# 하네스 활용:
# - 복잡한 로직의 단순화
# - 유지보수성 향상
```

---

## 3.3 Skill 위치와 우선순위

Skill은 여러 위치에서 찾을 수 있으며, 다음의 우선순위를 따른다:

```
Enterprise Skill (조직 관리자 제공)
  ↓ (찾지 못하면)
Personal Skill (~/.claude/skills/)
  ↓ (찾지 못하면)
Project Skill (.claude/skills/)
  ↓ (찾지 못하면)
Plugin Skill (플러그인에서 제공)
```

**우선순위**: Enterprise > Personal > Project > Plugin

---

## 3.4 SKILL.md Frontmatter

Skills는 Markdown 파일로 정의되며, 다음의 frontmatter 필드를 지원한다:

```yaml
---
# 기본 정보
name: "Debug Session"                # Skill 이름
description: "구조화된 디버깅을 실행합니다"  # 설명
argument-hint: "[error message]"    # 사용자에게 표시될 인자 힌트

# 호출 제어
disable-model-invocation: false      # true = AI가 자동 호출 불가 (수동만)
user-invocable: true                # false = 사용자가 호출 불가 (AI만)

# 도구 접근 제어
allowed-tools: ["bash", "file_read", "file_edit"]
                                    # 이 Skill 내에서 사용 가능한 도구

# 모델 설정
model: "claude-opus-4-20250101"     # 명시적 모델 지정

# 작업 분류
effort: "medium"                    # low / medium / high
context: "code"                     # code / doc / research / analysis

# Subagent와의 관계
agent: "code-reviewer"              # 이 Skill을 실행할 Subagent 지정
                                    # (생략 시 = 메인 에이전트)

# Hooks (이벤트 핸들러)
hooks:
  PreSkillRun: ".claude/hooks/pre-skill.sh"
  PostSkillRun: ".claude/hooks/post-skill.sh"

# 파일 경로
paths:
  allowed: ["."]                    # 접근 가능한 디렉토리
  denied: ["node_modules", ".git"]  # 접근 금지 디렉토리

# 셸 설정
shell: "bash"                       # bash / zsh / sh
---
```

---

## 3.5 문자열 치환 (String Interpolation)

Skill 내에서 동적으로 값을 주입할 수 있다:

### 3.5.1 인자 치환

```markdown
# 사용자가 호출: /debug "NullPointerException"

---
argument-hint: "[error message]"
---

## Task
에러: $ARGUMENTS
혹은
에러: $ARGUMENTS[0]
혹은 위치별
에러: $0

# 결과: 에러: NullPointerException
```

### 3.5.2 세션 정보 치환

```markdown
# Skill 내 사용 가능한 변수

${CLAUDE_SESSION_ID}          # 현재 세션 ID
${CLAUDE_SKILL_DIR}          # Skill이 정의된 디렉토리
${CLAUDE_PROJECT_ROOT}       # 프로젝트 루트
${CLAUDE_USER_HOME}          # 사용자 홈 디렉토리
${CLAUDE_TIMESTAMP}          # 현재 타임스탬프
```

### 3.5.3 환경 변수 치환

```markdown
---
shell: "bash"
---

## Commands
echo "API Key: $API_KEY"
echo "Project: $PROJECT_NAME"

# 실행 전에 환경 변수 로드됨
```

---

## 3.6 동적 컨텍스트 주입

Skill은 **동적 컨텍스트 주입** 기능을 지원한다:

### 3.6.1 !`command` 구문

```markdown
---
name: "Code Analysis"
---

## Current Files in Project

!`find . -name "*.py" -type f`

## Recent Commits

!`git log --oneline -10`

## Build Status

!`npm run build --status-only`

# 효과:
# Skill이 실행될 때, !`...` 로 감싼 명령어가 실행되고
# 그 결과가 현재 텍스트로 삽입됨
```

### 3.6.2 조건부 컨텍스트

```markdown
---
paths:
  allowed: ["."]
---

## Conditional Analysis

!`if [ -f package.json ]; then cat package.json; fi`

# Node.js 프로젝트인 경우만 package.json 내용 포함
```

---

## 3.7 Subagent에서의 Skill 실행

Skill은 특정 Subagent에 의해서만 실행되도록 제한 가능하다:

```yaml
---
name: "Security Audit"
agent: "security-reviewer"    # 이 Skill은 security-reviewer Subagent만 실행 가능
user-invocable: false         # 사용자는 직접 호출 불가
disable-model-invocation: false  # security-reviewer에서는 자동 호출 가능

context: fork                 # Skill 실행 시 별도 컨텍스트에서 실행
---

## Security Audit Procedure
...
```

### 3.7.1 컨텍스트 격리 옵션

```yaml
context:
  fork: true          # 별도 프로세스에서 실행 (완전 격리)
  agent: "security"   # security Subagent에서만 실행 가능
  timeout: 300        # 300초 제한시간
```

---

## 3.8 호출 제어

### 3.8.1 disable-model-invocation vs user-invocable

| 설정 | 설명 | 사용 사례 |
|------|------|----------|
| `disable-model-invocation: true` | AI가 자동으로 호출할 수 없음. 사용자만 호출 가능 (`/skill-name`) | 부수 효과가 있는 작업 (배포, 데이터 삭제 등) |
| `user-invocable: false` | 사용자가 직접 호출할 수 없음. AI만 호출 가능 | 내부 보조 작업 (전처리, 정리 등) |
| 둘 다 생략 | 기본값: AI도 호출 가능, 사용자도 호출 가능 | 일반적인 작업 |

### 3.8.2 실전 패턴

#### 패턴 1: 위험한 작업 (사용자 승인 필수)

```yaml
---
name: "Production Deploy"
disable-model-invocation: true    # AI가 자동으로 배포 불가
---

## Deploy to Production
사용자가 `/deploy` 명령어로만 호출 가능
AI는 "배포 준비 완료. 사용자에게 물어봐" 메시지 출력
```

#### 패턴 2: 내부 보조 작업

```yaml
---
name: "Format and Lint"
user-invocable: false             # 사용자가 직접 호출 불가
---

## Auto Format
AI가 코드 생성 후 자동으로 이 Skill 호출
사용자는 직접 호출 불가 (항상 AI의 판단 하에)
```

---

## 3.9 하네스 엔지니어링 관점 (Part 3)

### 3.9.1 Skills가 해결하는 하네스 요소

| 하네스 요소 | Skills 해결 방식 |
|-----|-----|
| **#5 Procedure Isolation** | 각 Skill = 격리된 절차. 다른 Skill과 컨텍스트 분리 |
| **#13 Tool Whitelist** | allowed-tools로 각 Skill이 접근 가능한 도구 제한 |
| **#21 Workflow Template** | 반복 가능한 워크플로우를 Skill로 표준화 |
| **#38 Knowledge Encapsulation** | Skill은 절차적 지식 캡슐화 |
| **#46 Skill Composition** | 여러 Skill을 조합하여 복잡한 작업 구성 |

### 3.9.2 기존 47개 Skills와의 관계

현재 보유 Skills:

```
/batch, /claude-api, /debug, /loop, /simplify (5개 번들)
+ 42개 커스텀 Skills
= 47개 총 Skills
```

이들은 다음과 같이 계층화될 수 있다:

```
Low-level Skills (원시 작업)
  - /debug, /batch, /simplify

Mid-level Skills (프로세스)
  - /code-review, /test-design, /security-audit

High-level Skills (복합 워크플로우)
  - /deploy, /release, /incident-response
```

---

# Part 4: 3가지 시스템 통합 분석
## Agent Teams + Subagents + Skills의 하네스 관점 종합

---

## 4.1 관계 맵

```
┌─────────────────────────────────────────────────────┐
│          Agent Teams (최상위 조율)                   │
├─────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐ ┌──────────────┐
│  │ Planner      │  │ Executor     │ │ Verifier     │
│  │ Teammate     │  │ Teammate     │ │ Teammate     │
│  │(Subagent)    │  │(Subagent)    │ │(Subagent)    │
│  └────┬─────────┘  └────┬─────────┘ └────┬─────────┘
│       │                 │                │
│  ┌────▼─────────┬──────▼──────┬──────────▼─────────┐
│  │  Skills      │   Skills    │    Skills         │
│  │  /design     │   /debug    │    /code-review   │
│  │  /plan       │   /batch    │    /test-design   │
│  └──────────────┴─────────────┴───────────────────┘
│
└─────────────────────────────────────────────────────┘

시계열:
시간 0: Agent Teams 리더가 팀 생성
시간 1: Planner 팀원 시작 (Subagent)
        └─ /design Skill 자동 로드
        └─ /plan Skill 준비
시간 2: Executor 팀원 시작 (다른 Subagent)
        └─ /debug Skill 로드
        └─ /batch Skill 준비
시간 3: Verifier 팀원 시작 (3번째 Subagent)
        └─ /code-review Skill 로드
        └─ /test-design Skill 준비
```

---

## 4.2 독립성 확보 방안

### 4.2.1 완전 독립 인스턴스 (Agent Teams)

```
Teams가 제공하는 구조적 독립성:

1. 컨텍스트 분리
   Planner 대화   (Subagent #1 컨텍스트)
   ≠ (별도 메모리)
   Executor 대화  (Subagent #2 컨텍스트)
   ≠ (별도 메모리)
   Verifier 대화  (Subagent #3 컨텍스트)

2. 정보 흐름 제어
   Planner → [공유 작업 목록] → Executor
   ↓ (Planner의 과정 분석은 불가)
   Executor는 결과만 봄
   ↓
   비편향 실행 가능

3. 역할 강제
   Planner는 수정하지 않음 (plan mode)
   Executor는 계획만 따름
   Verifier는 과정을 모름
```

### 4.2.2 컨텍스트 격리 위임 (Subagents)

```
Subagent가 제공하는 격리:

메인 세션의 300개 메시지 기록
  → Subagent 로드 시 최소 정보만 전달
  → Subagent 자체 컨텍스트 독립 관리
  → 메인 세션 비용 증가 없음

권한 모드로 추가 격리:
  Plan Subagent: permissionMode: plan
                 → 실행하지 않고 계획만

  Verify Subagent: disallowedTools: ["bash", "git"]
                 → 읽기만 가능

  Execute Subagent: tools: ["file_edit", "bash"]
                 → 이 도구들만 사용
```

### 4.2.3 절차 캡슐화 (Skills)

```
각 Skill = 블랙박스 절차

/code-review Skill 호출
  → 내부 동작은 Skill 정의대로
  → 결과만 반환
  → 호출자는 세부사항 모름

Skill의 allowed-tools 제한:
  /test-design는 ["bash", "file_read", "npm"]만 사용
  → 파일 생성 불가
  → Git 푸시 불가

Effect: 의도하지 않은 부수효과 자동 방지
```

---

## 4.3 Plan-Execute-Verify 구현 패턴

### 4.3.1 패턴 구조

```
┌─────────────────────────────────────────────────────────┐
│                    Leader (리더)                        │
│  "이 기능을 구현해줘"                                    │
└────┬──────────────────────────────────────────────────┬─┘
     │                                                   │
┌────▼───────────────────┐  시간 1: 계획         시간 2: 검증
│  Planner Teammate       │──────────────────→   ┌──────────────┐
│ (Subagent: plan mode)   │  Plan Approval    │  Verifier     │
│                         │  Request          │  Teammate     │
│ 작업:                  │                   │              │
│ - 요구사항 분석        ├─────────────────────→  (Hook 기다림)
│ - 작업 분해            │  TaskCreated       │              │
│ - 설계 문서 생성       │  Event             │              │
│ - /design Skill        │                    │              │
│ - /plan Skill          │                    │              │
└────┬───────────────────┘                    └──────────────┘
     │
     │ 리더가 계획 승인
     ▼
┌─────────────────────────┐
│ Executor Teammate       │
│ (Subagent: auto mode)   │
│                         │
│ 작업:                  │
│ - 승인된 계획 구현     │
│ - 테스트 작성          │
│ - /debug Skill         │
│ - /batch Skill         │
│ - 코드 생성            │
└──────┬────────────────┘
       │
       │ 종료 (TaskCompleted)
       ▼
      Verifier
      └─ Hook 트리거
         └─ 독립 검증
         └─ 피드백 생성
```

### 4.3.2 계획 단계 (Plan Phase)

```yaml
# Planner Teammate 정의
---
name: "Planner"
agent: "requirements-analyst"
permissionMode: "plan"              # 실행 금지
skills: ["design", "plan", "complexity-resolver"]
---

# Planner의 작업:
1. /design: 아키텍처 및 설계 문서 작성
2. /plan: 작업 분해, 단계별 계획 수립
3. 메시지: 리더에게 "계획 완료, 승인 요청"
4. Leader가 계획 검토 후 승인
```

### 4.3.3 실행 단계 (Execute Phase)

```yaml
# Executor Teammate 정의
---
name: "Executor"
agent: "code-developer"
permissionMode: "auto"              # 자동 승인
tools: ["file_edit", "bash", "git_commit"]
skills: ["debug", "batch", "testing-strategy"]
---

# Executor의 작업:
1. Planner가 생성한 계획 수신
   (Planner의 과정은 모름. 최종 계획만 봄)
2. 계획 기반 구현:
   - /debug: 마주친 에러 처리
   - /batch: 여러 파일 일괄 수정
   - /testing-strategy: 테스트 코드 작성
3. TaskCompleted 이벤트 발생
```

### 4.3.4 검증 단계 (Verify Phase)

```yaml
# Verifier Teammate 정의
---
name: "Verifier"
agent: "quality-reviewer"
disallowedTools: ["bash", "git_push"]  # 읽기만 가능
skills: ["code-review", "test-design"]
---

# Verifier의 작업:
1. Hook: TaskCompleted 이벤트 감지
   (코드가 완성되었다는 신호만 받음)
2. 독립 검증:
   - /code-review: 코드 품질 검토
   - /test-design: 테스트 커버리지 확인
3. 결과:
   - 통과: "검증 성공"
   - 실패: Leader에게 피드백 (수정 방법 제시 안 함)

# 핵심: Executor의 구현 과정을 모르므로 편향 없이 검증 가능
```

### 4.3.5 Hooks를 통한 외부 검증

```bash
# .claude/hooks/verify-task.sh
#!/bin/bash

TASK_ID=$1
TASK_OUTPUT=$2

# 1차: Verifier 팀원 실행
echo "Verifying task $TASK_ID..."
./.claude/hooks/verify-logic.sh "$TASK_OUTPUT"
LOGIC_RESULT=$?

# 2차: 자동 테스트 실행
npm test
TEST_RESULT=$?

# 3차: 성능 벤치마크
./.claude/hooks/benchmark.sh
PERF_RESULT=$?

# 종합 판정
if [ $LOGIC_RESULT -eq 0 ] && [ $TEST_RESULT -eq 0 ] && [ $PERF_RESULT -eq 0 ]; then
  exit 0  # 검증 통과 → 작업 완료 표시
else
  echo "Verification failed. Re-review required."
  exit 2  # 재검토 필요 → 팀원 계속 작동
fi
```

---

## 4.4 기존 30개 Agent + 47개 Skill 자산의 결합 방안

### 4.4.1 Agent → Subagent 매핑

```
기존 30개 Agent를 Agent Teams의 팀원으로 재구성:

┌──────────────────────────────────────┐
│ Agent 카테고리 → Teammate 역할        │
├──────────────────────────────────────┤
│ 분석 에이전트 (6개)                   │
│  - eval-analyzer                    │
│  - multidimensional-analyst         │
│  - insight-explorer                 │
│  → Analyst Teammate                 │
│
│ 계획 에이전트 (5개)                   │
│  - requirements-analyst             │
│  - system-architect                 │
│  - complexity-resolver              │
│  → Planner Teammate                 │
│
│ 개발 에이전트 (7개)                   │
│  - code-developer                   │
│  - vibe-dev                         │
│  - design-specialist                │
│  → Executor Teammate                │
│
│ 검증 에이전트 (8개)                   │
│  - quality-reviewer                 │
│  - security-reviewer                │
│  - edge-case-reviewer               │
│  - logic-reviewer                   │
│  → Verifier Teammate(s)             │
│
│ 맥락 관리 에이전트 (4개)              │
│  - context-manager                  │
│  - session-memo-writer              │
│  → Context Teammate                 │
└──────────────────────────────────────┘
```

### 4.4.2 Skill → Agent 연계

```
각 Agent (이제는 Teammate)이 사용할 Skills 할당:

Planner Teammate
  ├─ /design (설계 문서 작성)
  ├─ /plan (작업 계획)
  └─ /complexity-resolver (복잡도 분석)

Executor Teammate
  ├─ /debug (에러 처리)
  ├─ /batch (일괄 수정)
  ├─ /testing-strategy (테스트 설계)
  └─ /code-generation (코드 생성)

Verifier Teammate
  ├─ /code-review (코드 검토)
  ├─ /test-design (테스트 커버리지)
  └─ /security-audit (보안 검사)

Context Teammate
  ├─ /memory-management (메모리 관리)
  └─ /session-summary (세션 요약)
```

### 4.4.3 스케일링 전략

```
Phase 1: 작은 팀 (3명)
  Planner + Executor + Verifier
  → 기본 Plan-Execute-Verify 구현

Phase 2: 확장 팀 (5명)
  + Analyst (복잡한 분석 담당)
  + Context (메모리/상태 관리)
  → 대규모 프로젝트 지원

Phase 3: 특화 팀 (7명+)
  + Security Verifier (보안 검증)
  + Performance Verifier (성능 검증)
  + Domain Expert (도메인 전문가)
  → 엔터프라이즈 규모 대응
```

---

## 4.5 Hooks를 통한 외부 검증 레이어

### 4.5.1 Hook 전체 맵

```
Agent Teams Lifecycle
  ↓
  SubagentStart
    └─ .claude/hooks/on-teammate-start.sh
    └─ 팀원 시작 시 초기화

  팀원 작업 중 (반복)
    ├─ PreToolUse
    │   └─ 도구 호출 전 검증
    │   └─ 예: bash 호출 금지
    │
    ├─ PostToolUse
    │   └─ 도구 결과 검증
    │   └─ 예: 파일 수정 로그 기록
    │
    ├─ TaskCreated
    │   └─ 새 작업 생성 시
    │   └─ 예: 작업 명세 자동 검증
    │
    └─ TaskCompleted
        └─ 작업 완료 시
        └─ 예: 결과물 자동 검증 (Hook exit 2 = 재시도)

  SubagentStop
    └─ .claude/hooks/on-teammate-stop.sh
    └─ 팀원 종료 시 정리
```

### 4.5.2 Multi-layer 검증 구현

```
외부 검증 레이어의 3단계:

1차 검증: PreToolUse Hook
   ├─ 도구 화이트리스트 검사
   ├─ 인자 검증 (SQL injection 감지 등)
   └─ 예측 비용 계산

2차 검증: PostToolUse Hook
   ├─ 결과 타입 확인
   ├─ 파일 무결성 검사
   └─ 부수효과 기록

3차 검증: TaskCompleted Hook
   ├─ 산출물 완전성 검사
   ├─ 자동 테스트 실행
   ├─ 보안 스캔
   └─ 성능 벤치마크

Exit Code로 처리:
   0 = 통과 → 계속 진행
   1 = 오류 → 종료
   2 = 재시도 → 팀원 계속 작동
```

### 4.5.3 Hooks 구현 예시

```bash
# .claude/hooks/post-tool-use.sh
#!/bin/bash

TOOL=$1
ARGS=$2
RESULT=$3
EXIT_CODE=$4

# 모든 파일 수정 로그 기록
if [ "$TOOL" = "file_edit" ]; then
  echo "[$(date)] Modified: $ARGS" >> .claude/hooks/audit.log

  # 파일 크기 이상 증가 감지
  if [ $(stat -f%z "$ARGS" 2>/dev/null || stat -c%s "$ARGS") -gt 1000000 ]; then
    echo "WARNING: File size exceeds 1MB"
    exit 2  # 다시 검토하도록 요청
  fi
fi

# bash 호출 결과 검증
if [ "$TOOL" = "bash" ]; then
  if [ $EXIT_CODE -ne 0 ]; then
    echo "Command failed: $ARGS"
    exit 2
  fi
fi

exit 0
```

---

## 4.6 하네스 요소 49개 중 해결 가능한 요소 매핑

### 4.6.1 완전 해결 (11개)

| # | 요소 | 해결 방식 |
|---|------|----------|
| 1 | PGE 3-Agent GAN Loop | Agent Teams: Plan(Planner) + Generator(Executor) + Evaluator(Verifier) |
| 2 | Context Partitioning | Subagent: 독립 컨텍스트 윈도우 |
| 5 | Procedure Isolation | Skills: 각 Skill 블랙박스 격리 |
| 11 | Cost Control | Subagent: 토큰 독립 소비 |
| 14 | Skeptical Evaluator | Agent Teams: Devil's Advocate 팀원 |
| 17 | Tool Restriction | Subagent: tools/disallowedTools |
| 21 | Workflow Template | Skills: 반복 가능 워크플로우 |
| 22 | Handoff State Machine | Agent Teams: 공유 작업 목록 + 종속성 |
| 25 | Approval Workflow | Agent Teams: Plan Approval 패턴 |
| 38 | Knowledge Encapsulation | Skills: 절차적 지식 캡슐화 |
| 44 | Subagent Delegation | Subagent: 정의 재사용 |

### 4.6.2 부분 해결 (12개)

| # | 요소 | 현재 해결 | 추가 필요 |
|---|------|----------|----------|
| 3 | Memory Management | Subagent: persistent memory | 크로스-팀원 메모리 동기화 |
| 6 | Fallback Strategy | Hooks: exit 2로 재시도 | 자동 fallback agent 선택 |
| 8 | Model Ensemble | Skills: 다중 모델 호출 | 자동 모델 선택 로직 |
| 13 | Tool Whitelist | Subagent + Skills: allowed-tools | 런타임 동적 tool binding |
| 16 | Execution Timeout | Subagent: maxTurns | 세밀한 timeout 제어 |
| 19 | Rollback Mechanism | Hooks: 파일 변경 추적 | 자동 git-based rollback |
| 24 | Permission Gate | Subagent: permissionMode | 조직 정책 통합 |
| 30 | Knowledge Graph | Memory: MEMORY.md | 구조화된 그래프 형식 |
| 35 | Version Control | Skills: 자동 git commit | 의미론적 버전 관리 |
| 40 | Async Execution | Agent Teams: background tasks | 스케줄링 메커니즘 |
| 45 | Tool Composition | Skills: 다중 tool 호출 | 자동 composition 제안 |
| 47 | Cross-agent Learning | Memory: user scope | 피드백 루프 자동화 |

### 4.6.3 기반 제공 (13개)

| # | 요소 | 기반 제공 방식 |
|---|------|-----------|
| 4 | Error Recovery | Hooks: PreToolUse로 에러 예측 |
| 7 | Cost Modeling | Subagent: 토큰 비용 추적 |
| 9 | Reasoning Trace | Hooks: 모든 작업 로깅 |
| 10 | Uncertainty Quantification | Verifier: confidence scores |
| 12 | Cache Management | Subagent: 컨텍스트 압축 |
| 15 | Audit Trail | Hooks: 모든 이벤트 기록 |
| 18 | Reproducibility | Subagent memory: 세션 재개 |
| 20 | State Management | Agent Teams: 공유 작업 목록 |
| 23 | Escalation Chain | Agent Teams: 메시지 라우팅 |
| 26 | Quality Assurance | Hooks: PostToolUse 검증 |
| 28 | Continuous Integration | Skills: /batch + Hooks |
| 34 | Security Sandbox | Subagent: tool restriction |
| 37 | API Abstraction | Skills: API 호출 standardization |

### 4.6.4 미해결 (13개)

| # | 요소 | 이유 | 권장 보완 |
|---|------|------|----------|
| 27 | User Research Loop | Claude Code의 범위 밖 | 외부 UX research tool 연동 |
| 29 | Compliance Checker | 조직별 정책 | 커스텀 Hook 또는 external API |
| 31 | Semantic Versioning | VCS 통합 필요 | git tag automation |
| 32 | Regression Testing | 테스트 인프라 | 테스트 자동화 도구 연동 |
| 33 | Deployment Pipeline | CI/CD 필요 | GitHub Actions / GitLab CI 연동 |
| 36 | Domain Adaptation | ML 모델 필요 | 파인튜닝 서비스 |
| 39 | Multi-language Support | 언어 특성 차이 | 언어별 Subagent 정의 |
| 41 | Real-time Collaboration | 동기 프로토콜 필요 | WebSocket 기반 extension |
| 42 | Mobile Optimization | 다른 플랫폼 | Claude on Mobile |
| 43 | Offline Mode | 네트워크 필요 | 로컬 캐시 메커니즘 |
| 46 | Federated Learning | 분산 학습 | 외부 ML 플랫폼 |
| 48 | Hardware Optimization | 인프라 수준 | Anthropic API optimization |
| 49 | Organizational Change Management | 프로세스 개선 | 조직 정책 수립 |

**해결 비율**: 11개 완전 + 12개 부분 + 13개 기반 = 36개 (73%)

---

## 4.7 Ann의 워크플로우 최적화
### Windows + Claude Code CLI + VS Code + Claude Desktop 환경

### 4.7.1 환경 분석

```
Ann의 개발 환경:
├─ Windows OS (PowerShell 환경)
├─ VS Code (터미널, 편집)
├─ Claude Code CLI (main workhorse)
└─ Claude Desktop (Cowork, secondary)

제약사항:
❌ tmux 미지원 (Unix only) → in-process 모드만 사용
❌ 분할 창 (split pane) 미지원 → 팀원 순환 (Shift+Down)
⚠️ PowerShell과 bash 간 호환성 문제
⚠️ 경로 표기법 차이 (\ vs /)
```

### 4.7.2 최적화된 워크플로우

#### Workflow 1: 로컬 개발 (Plan-Execute-Verify)

```powershell
# PowerShell에서 실행
claude --agent code-developer

# 메인 에이전트 프롬프트:
# "이 기능을 구현해줘: [요구사항]
#
#  Plan-Execute-Verify 패턴:
#  1. /plan Skill로 계획 수립 (시간 5분)
#  2. 나에게 계획 승인 요청 (네 / 아니오)
#  3. 승인 후 /debug, /batch로 구현
#  4. 자동 Hook으로 검증"

# 결과:
# - 토큰 비용 절감 (Subagent 독립 소비)
# - 계획과 실행 분리 (편향 제거)
# - 자동 품질 검사 (Hook)
```

#### Workflow 2: 복잡한 디버깅 (Agent Teams)

```powershell
# 여러 이론으로 독립 조사
claude --enable-agent-teams

# 메인 리더:
# "이 버그를 조사해줘. 팀을 만들어줘:
#  - Hypothesis A 조사 팀원
#  - Hypothesis B 조사 팀원
#  - Hypothesis C 조사 팀원
#
#  각 팀원은 다른 팀원의 가설을 반박해봐.
#  상호 반박을 견딘 가설이 진짜 원인이야."

# in-process 모드: Shift+Down으로 팀원 순환
# 시간 1: Hypothesis A 팀원 작업 (5분)
#         Shift+Down → Hypothesis B로 전환
# 시간 2: Hypothesis B 팀원 작업 (5분)
#         Shift+Down → Hypothesis C로 전환
# 시간 3: Hypothesis C 팀원 작업 (5분)
#         Shift+Down → 리더로 복귀
# 시간 4: 세 팀원의 결과 검토 및 종합

# 결과:
# - 앵커링 편향 완전 제거
# - 3가지 관점의 독립 분석
# - 높은 정확도의 원인 파악
```

#### Workflow 3: Cowork (Claude Desktop)와의 병렬 작업

```
Claude Code CLI (메인)         Claude Desktop (보조)
(Windows Terminal)             (Cowork Plugin)

├─ Plan-Execute 담당           ├─ 문서 작성
│  ├─ /plan Skill              │  ├─ README 업데이트
│  ├─ /debug Skill             │  ├─ API 문서화
│  └─ /batch Skill             │  └─ 변경로그 작성
│
├─ 병렬 Subagent               └─ 완료 후 Cowork에서
│  ├─ Security Reviewer        제공된 산출물을
│  ├─ Performance Reviewer     Claude Code로 임포트
│  └─ Test Coverage Reviewer   → 최종 통합
│
└─ Hooks로 외부 검증
   └─ 자동 테스트, 린트
```

### 4.7.3 PowerShell 호환성 최적화

```yaml
# .claude/agents/powershell-safe-executor.md
---
name: "PowerShell Safe Executor"
shell: "powershell"              # bash 대신 PowerShell
paths:
  allowed: ["."]
disallowedTools: ["bash"]         # bash 명령 금지
allowed-tools: ["powershell_exec", "file_edit"]
---

## PowerShell 호환 스크립트

$ProjectRoot = Get-Location
$ConfigPath = Join-Path $ProjectRoot "config"
Get-ChildItem -Path $ConfigPath -Filter "*.json" | ForEach-Object {
  $json = Get-Content $_.FullName | ConvertFrom-Json
  # 처리
}
```

### 4.7.4 권장 설정

```json
// settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "shell": "powershell",
  "workingDirectory": "${workspaceFolder}",
  "hooks": {
    "TaskCompleted": [
      {
        "command": "powershell -NoProfile -ExecutionPolicy Bypass .claude/hooks/verify-task.ps1"
      }
    ]
  }
}
```

```json
// ~/.claude.json (홈 디렉토리)
{
  "defaults": {
    "model": "claude-opus-4-20250101",
    "maxTokens": 200000
  },
  "teammates": {
    "mode": "in-process"          // tmux 대신 in-process
  },
  "skills": {
    "autoLoad": ["debug", "batch", "simplify"]
  }
}
```

### 4.7.5 일일 워크플로우 추천

```
09:00 - 세션 시작
      → claude --agent code-developer
      → 오늘의 계획 수립 (/plan Skill)

09:30 - 구현 작업
      → /debug: 마주친 에러 처리
      → /batch: 일괄 수정
      → /testing-strategy: 테스트 작성

12:00 - 중간 검증
      → Hooks 결과 확인
      → 성능 벤치마크 실행

14:00 - 복잡한 버그 발생
      → Agent Teams로 팀 생성
      → 3가지 가설로 독립 조사
      → 팀원 순환 (Shift+Down)

17:00 - 최종 검증
      → /code-review Skill
      → 자동 테스트 실행
      → 배포 준비

17:30 - 종료
      → 메모리 업데이트 (MEMORY.md)
      → 세션 정리
```

---

## 4.8 종합 판정: 3가지 시스템의 역할

| 시스템 | 주요 역할 | 토큰 비용 | 사용 시기 |
|--------|----------|----------|----------|
| **Agent Teams** | 병렬 협업, 대규모 작업 조율 | 높음 (팀원 수 × 비용) | 복잡 분석, 독립 관점 필요 |
| **Subagents** | 특화 작업 위임, 컨텍스트 격리 | 중간 (독립 윈도우) | 단계별 작업, 권한 제어 필요 |
| **Skills** | 절차 표준화, 반복 작업 | 낮음 (템플릿 기반) | 일상적 작업, 워크플로우 |

**최적 조합**:
- 일상 작업: Skills 활용 (낮은 비용, 높은 생산성)
- 중간 규모 작업: Subagents (격리 + 비용 절감)
- 대규모/복잡한 작업: Agent Teams (독립성 + 병렬성)

---

# 결론

## 3가지 시스템의 통합 하네스

Claude Code의 Agent Teams, Subagents, Skills는 **하네스 엔지니어링의 완전한 구현**을 제공한다:

1. **Agent Teams**: 구조적 독립성 강제 (다른 인스턴스)
2. **Subagents**: 컨텍스트 격리 및 권한 제어 (동일 세션 내 격리)
3. **Skills**: 절차 캡슐화 및 반복성 (템플릿화된 작업)

이 3가지를 조합하면:
- 49개 하네스 요소 중 **73% 완전 또는 부분 해결**
- 기존 30개 Agent + 47개 Skill 자산 **완전 활용**
- Ann의 Windows 환경에서 **실용적 구현 가능**

**다음 단계**:
1. Agent Teams 활성화 및 팀 구조 정의
2. 기존 Agent를 Subagent 타입으로 마이그레이션
3. Skills별 Hook 설정으로 외부 검증 레이어 구축
4. Plan-Execute-Verify 패턴 문서화 및 운영 가이드 정립

