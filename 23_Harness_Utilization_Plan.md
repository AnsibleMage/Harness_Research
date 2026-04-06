# 하네스 활용 계획 (Harness Utilization Plan)

**작성일**: 2026-04-03
**대상**: Ann의 독립성 있는 Plan-Execute-Verify 하네스 아키텍처 구현
**범위**: 49개 하네스 요소 × Agent Teams × Subagents × Skills 통합 설계
**핵심 전략**: Agent Teams를 Primary 메커니즘으로 구조적 독립성 강제

---

## 목차

1. [하네스 요소 × 에이전트/스킬 매핑 매트릭스](#1-하네스-요소--에이전트스킬-매핑-매트릭스)
2. [하네스 아키텍처: 3-Layer System (Agent Teams > Subagents > Skills)](#2-하네스-아키텍처-3-layer-system)
3. [독립성 확보 방안 (최우선) - Agent Teams 중심](#3-독립성-확보-방안-최우선)
4. [미커버 영역 및 보완 제안](#4-미커버-영역-및-보완-제안)
5. [구현 로드맵](#5-구현-로드맵)
6. [구현 우선순위 매트릭스](#6-구현-우선순위-매트릭스)
7. [종합 분석 및 권고사항](#7-종합-분석-및-권고사항)

---

## 1. 하네스 요소 × 에이전트/스킬 매핑 매트릭스

### 매핑 개요

49개 하네스 요소에 대한 Agent Teams, Subagents, Skills의 구현 경로를 정의한다. 각 요소는 다음 상태 중 하나:
- **●** (완전 커버): Agent Teams/Subagents/Skills로 완전 구현 가능
- **◐** (부분 커버): 기본 메커니즘 제공, 추가 구성 필요
- **○** (미커버): 인프라/기술 설계 필요 (Agent로 해결 불가)

### 1.1 아키텍처 & 구조 패턴 (6개 요소)

| # | 하네스 요소 | 커버리지 | 구현 메커니즘 | 설명 |
|---|-----------|---------|-------------|------|
| 1 | **PGE 3-Agent GAN 루프** | ●→● | Agent Teams (Plan/Execute/Verify Teammates) | Leader 팀원(계획자) + Executor 팀원 + Verifier 팀원으로 완전 분리 |
| 2 | **Initializer Agent 패턴** | ◐→◐ | Subagent + Skill (memory-save, claude-strategy) | 세션 초기화 스크립트, Skills 자동 로드 |
| 3 | **App Server 아키텍처 (JSON-RPC)** | ○→○ | Infrastructure (기술 설계 필요) | 외부 시스템 - Agent로 해결 불가 |
| 4 | **NLAH 명세** | ○→○ | Framework (기술 설계 필요) | 외부 시스템 - Agent로 해결 불가 |
| 5 | **Shared Context Store** | ◐→● | Agent Teams (shared task list) + Subagent (memory persistent) | 팀원 간 작업 공유 + Subagent 지속 메모리 |
| 6 | **분산 Checkpoint 시스템** | ◐→◐ | Hooks (PreToolUse/PostToolUse) + Subagent persistent memory | 체크포인트 자동 저장, Hooks 검증 |

### 1.2 컨텍스트 & 메모리 관리 (4개 요소)

| # | 하네스 요소 | 커버리지 | 구현 메커니즘 | 설명 |
|---|-----------|---------|-------------|------|
| 7 | **자동 Context Compaction** | ● | Context Manager Skill | 메모리 자동 압축 |
| 8 | **자동 메모리 시스템** | ● | memory-save, claude-strategy Skills | 세션 메모리 자동 저장 |
| 9 | **Artifact Hand-off 명세** | ● | Context Manager, memory-save | 산출물 명시적 전달 |
| 10 | **Context Reuse Strategy** | ◐ | Context Manager, Knowledge Mapper | 컨텍스트 재사용 및 압축 |

### 1.3 스킬 & 절차 관리 (3개 요소)

| # | 하네스 요소 | 커버리지 | 구현 메커니즘 | 설명 |
|---|-----------|---------|-------------|------|
| 11 | **Skills Versioned** | ◐→● | SKILL.md 파일명 + Subagent skills 사전로드 | Skills에 버전 명시, Subagent가 특정 버전 미리 로드 |
| 12 | **AGENTS.md Pattern** | ◐→◐ | Subagent 정의 파일 (.claude/agents/) | Subagent 역할 표준화 및 재사용 |
| 13 | **Skill Format Specification** | ◐→● | YAML frontmatter (SKILL.md) + Subagent config | Skill 정의 포맷 완전 명시 |

### 1.4 평가 & 품질 제어 (5개 요소)

| # | 하네스 요소 | 커버리지 | 구현 메커니즘 | 설명 |
|---|-----------|---------|-------------|------|
| 14 | **Skeptical Evaluator Mode** | ● | Agent Teams Devil's Advocate Teammate | 독립 Verifier Teammate로 비판적 검증 |
| 15 | **Eval Harness** | ● | Agent Teams (TaskCompleted Hook) | 외부 Hooks가 품질 검증 (실행자 제외) |
| 16 | **Confidence-Based Auto-Approval** | ◐ | Hooks (종료 코드 2로 차단/승인) | Hook 스크립트가 승인 게이트 역할 |
| 17 | **Audit Log & Observability** | ◐ | Context Manager, Hooks | 모든 에이전트 액션 로깅 |
| 18 | **Audit Trail & Regression Detection** | ● | Comparator Skill, pr-review | 이전 버전 대비 변경 추적 |

### 1.5 멀티 클라이언트 & 통합 (4개 요소)

| # | 하네스 요소 | 커버리지 | 구현 메커니즘 | 설명 |
|---|-----------|---------|-------------|------|
| 19 | **Multi-client Architecture** | ○ | Infrastructure (CLI/Web/IDE) | 외부 시스템 - 기술 설계 필요 |
| 20 | **Streaming Progress** | ○ | Infrastructure (SSE/WebSocket) | 외부 시스템 - 기술 설계 필요 |
| 21 | **IDE Plugin Integration** | ○ | Infrastructure (VSCode extension) | 외부 시스템 - 기술 설계 필요 |
| 22 | **Git + CI-CD 통합** | ◐→◐ | Hooks + commit-push + pr-review Skills | Skills 제공, CI-CD는 외부 |

### 1.6 오케스트레이션 & 워크플로우 (3개 요소)

| # | 하네스 요소 | 커버리지 | 구현 메커니즘 | 설명 |
|---|-----------|---------|-------------|------|
| 23 | **Handoff 메커니즘** | ◐→● | Agent Teams shared task list + dependency | 작업 목록 기반 자동 라우팅 |
| 24 | **계층적 Task Delegation** | ◐→● | Agent Teams (Leader + Teammates) + Subagent chain | 팀 구조로 자동 위임 |
| 25 | **Hybrid Execution Strategy** | ◐→● | Agent Teams Plan Approval 패턴 | 실행 전 승인 강제 |

### 1.7 보안 & 접근 제어 (4개 요소)

| # | 하네스 요소 | 커버리지 | 구현 메커니즘 | 설명 |
|---|-----------|---------|-------------|------|
| 26 | **Approval Workflow** | ◐→● | Agent Teams Plan Approval + TaskCompleted Hook | 실행 전/후 승인 게이트 |
| 27 | **Filesystem Access Control** | ○ | Infrastructure (OS level) | 외부 시스템 - 설계 필요 |
| 28 | **Skill Permission Model** | ◐→● | YAML frontmatter (allowed-tools, disable-model-invocation) | Skill별 도구 제한 및 모델 호출 제어 |
| 29 | **Multi-Tenant Isolation** | ◐→◐ | Subagent memory scope (local/project/user) | Subagent 메모리 격리, 팀 수준 다중 테넌트는 미지원 |

### 1.8 구성 & 계층화 (8개 요소)

| # | 하네스 요소 | 커버리지 | 구현 메커니즘 | 설명 |
|---|-----------|---------|-------------|------|
| 30 | **Multi-Layer Scope System** | ● | CLAUDE.md 우선순위 (Managed > CLI > Project > User) | 계층 기반 설정 자동 적용 |
| 31 | **Managed Policy Layer** | ◐ | CLAUDE.md (조직 수준) | 조직 정책 자동 상속 |
| 32 | **Path-Specific Rules** | ◐ | YAML 설정 (path-specific) | 경로별 규칙 적용 |
| 33 | **`.claude/rules/` Directory** | ● | 디렉토리 기반 분할 | 규칙 파일 디렉토리 구조 |
| 34 | **Import Syntax** | ◐ | `@` 문법 (CLAUDE.md) | 파일 참조 및 임포트 |
| 35 | **HTML Comment Stripping** | ◐ | CLAUDE.md 처리 | HTML 주석 자동 제거 |
| 36 | **claudeMdExcludes** | ◐ | 설정 (제외 목록) | 특정 파일 제외 |
| 37 | **User-Level Path Rules** | ● | ~/.claude/CLAUDE.md | 사용자 수준 규칙 |

### 1.9 자동화 & 효율성 (13개 요소)

| # | 하네스 요소 | 커버리지 | 구현 메커니즘 | 설명 |
|---|-----------|---------|-------------|------|
| 38 | **Cost Monitoring & Control** | ● | Context Manager, claude-strategy | 토큰 예산 추적 및 제어 |
| 39 | **Selective Compaction** | ◐ | Context Manager (선택적 압축) | 특정 부분만 압축 |
| 40 | **4-Step Workflow** | ● | Quality Manager, vibe-dev, pr-review | 표준 워크플로우 적용 |
| 41 | **Context Commands** | ◐ | /clear, /reset 등 | 컨텍스트 관리 명령 |
| 42 | **Compaction Preservation** | ● | Context Manager | 압축 후 지침 유지 |
| 43 | **200-Line Limit Compliance** | ● | 가이드라인 (강제 수행) | 응답 200줄 제한 |
| 44 | **Specificity Verification** | ● | Quality Manager, pr-review | 구체성 검증 패턴 |
| 45 | **Subagent Delegation Pattern** | ◐→● | Subagent YAML frontmatter (정의 명시) | Subagent 역할 명확화 |
| 46 | **CLAUDE.md as Code** | ◐ | commit-push, pr-review | 설정 파일 버전 관리 |
| 47 | **Failure Antipatterns Documentation** | ● | Quality Manager (가이드) | 실패 패턴 문서화 |
| 48 | **Content Inclusion Checklist** | ● | Quality Manager (체크리스트) | 포함 항목 검증 |
| 49 | **Advisory vs Hooks Distinction** | ◐→● | Hooks (PreToolUse/PostToolUse/TaskCompleted) | 권고와 강제 검증 명확화 |

**커버리지 요약**:
- 완전 해결(●): 18개
- 부분 해결(◐): 19개 (구조적 기반 제공)
- 미해결(○): 12개 (인프라/기술 설계)
- **전체 커버리지: 37/49 (75.5%)** → Agent Teams 적용 시 **73%** 달성 가능

---

## 2. 하네스 아키텍처: 3-Layer System

### 2.0 3-Layer System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                         AGENT TEAMS                               │
│  Leader (Coordinator) + 3-5 Teammates (Planner/Executor/Verifier) │
│                                                                    │
│  [공유 작업 목록] [종속성 관리] [메시지 시스템] [Hooks 게이트]    │
├──────────────────────────────────────────────────────────────────┤
│                       SUBAGENTS (각 Teammate)                     │
│  독립 컨텍스트 + 제한된 도구 + 사전로드 Skills + Persistent Memory │
│                                                                    │
│  [도구 제한] [권한 모드] [메모리 scope] [Hooks]                  │
├──────────────────────────────────────────────────────────────────┤
│                       SKILLS (도구 모음)                          │
│  claude-strategy, vibe-dev, pr-review, memory-save, ...           │
│                                                                    │
│  [YAML frontmatter] [allowed-tools] [권한 제어]                  │
└──────────────────────────────────────────────────────────────────┘
```

**층 관계**:
- **Agent Teams**: Plan-Execute-Verify의 구조적 분리를 강제하는 프레임워크
- **Subagents**: 각 Teammate의 구현체, 도구 제한 및 메모리 격리 제공
- **Skills**: 구체적 작업 수행 도구, 여러 에이전트에서 재사용

### 2.1 Plan Phase (계획 단계) 아키텍처

#### Teammate 구성: Planner (plan mode)

```yaml
# .claude/agents/planner-requirements.md (Subagent 정의)
---
name: "Planner - Requirements Analyst"
description: "요구사항 분석 및 설계 수립"
model: "claude-opus-4-20250101"
permissionMode: "plan"           # ← 실행 불가, 계획만 수립
tools: ["file_read", "code_search", "grep"]
disallowedTools: ["file_create", "bash", "git_push"]
skills: ["claude-strategy", "design-spec-form"]
memory:
  scope: "project"
  retention: "persistent"
hooks:
  PreToolUse: ".claude/hooks/pre-tool-use.sh"
  PostToolUse: ".claude/hooks/post-tool-use.sh"
background: "당신은 요구사항 분석가입니다."
---
```

#### Plan 단계 역할

| 역할 | Agent/Skill | 책임 |
|------|------------|------|
| **Requirements Analyst** | Planner Teammate | 기능/비기능 요구사항 명시 |
| **System Architect** | Subagent (architecture 타입) | 기술 설계, 아키텍처 결정 |
| **Complexity Resolver** | Skill (design-spec-form) | 복잡도 분석, 솔루션 도출 |
| **Solution Innovator** | Skill (claude-strategy) | 대안 생성, 최적안 제시 |
| **Balanced Judge** | Subagent (judge 타입) | 최종 계획 검증 |

#### Plan 산출물

```
- P-1: Functional Requirements (User Stories)
- P-2: Non-Functional Requirements (성능, 가용성)
- P-3: Architecture Decision (기술 선택)
- P-4: Implementation Roadmap (마일스톤)
- P-5: Risk Assessment (위험 요소 및 완화)

[메타정보 제거] → Executor에게 산출물만 전달
```

### 2.2 Execute Phase (실행 단계) 아키텍처

#### Teammate 구성: Executor (auto mode)

```yaml
# .claude/agents/executor-developer.md
---
name: "Executor - Code Developer"
description: "계획 기반 실행 및 구현"
model: "claude-opus-4-20250101"
permissionMode: "auto"           # ← 승인된 계획 기반 자동 실행
tools: ["file_read", "file_create", "file_edit", "bash", "git_push"]
disallowedTools: ["rm", "dangerous-command"]
skills: ["vibe-dev", "debug", "testing-strategy"]
memory:
  scope: "project"
  retention: "persistent"
hooks:
  PreToolUse: ".claude/hooks/pre-tool-use.sh"
  PostToolUse: ".claude/hooks/post-tool-use.sh"
  SubagentStop: ".claude/hooks/on-stop.sh"
background: "당신은 코드 개발자입니다. 주어진 계획을 구현합니다."
---
```

#### Execute 단계 역할

| 역할 | Agent/Skill | 책임 |
|------|------------|------|
| **Code Developer** | Executor Teammate (auto mode) | 코드 작성, 테스트 |
| **Learning Evolver** | Subagent (learning 타입) | 진행 중 학습 및 적응 |
| **Connection Creator** | Skill (vibe-dev) | 모듈 간 연결, 통합 |
| **TDD Agent** | Skill (testing-strategy) | 테스트 기반 개발 |
| **Progress Monitor** | Subagent (monitor 타입) | 진행 상황 추적 |

#### Execute 산출물

```
- E-1: Implementation Code (클린 코드)
- E-2: Unit Tests (80%+ 커버리지)
- E-3: Integration Tests (모듈 간 검증)
- E-4: Performance Metrics (속도, 메모리)

[구현 과정 정보 제거] → Verifier에게 산출물만 전달
```

### 2.3 Verify Phase (검증 단계) 아키텍처

#### Teammate 구성: Verifier(s) (검증 전용)

```yaml
# .claude/agents/verifier-quality-reviewer.md
---
name: "Verifier - Quality Reviewer"
description: "산출물 독립 검증"
model: "claude-opus-4-20250101"
permissionMode: "default"        # ← 도구 호출 시 승인 요청
tools: ["file_read", "code_search", "bash (테스트만)"]
disallowedTools: ["file_create", "file_edit", "git_push"]
skills: ["pr-review", "webapp-testing", "kwcag-a11y"]
memory:
  scope: "project"
  retention: "persistent"
hooks:
  TaskCompleted: ".claude/hooks/verify-task.sh"  # ← 완료 검증
background: "당신은 품질 검증자입니다. 코드와 설계의 품질만 평가합니다."
---
```

#### Verify 단계 역할 (병렬 검증)

| 역할 | Agent/Skill | 책임 |
|------|------------|------|
| **Quality Reviewer** | Verifier Teammate | 코드 구조, 성능 |
| **Security Reviewer** | Subagent (security 타입) | 보안 취약점 검사 |
| **Edge Case Reviewer** | Subagent (edge-case 타입) | 경계값, 예외 상황 |
| **Logic Reviewer** | Subagent (logic 타입) | 로직 정합성 검증 |
| **Grader** | Skill (pr-review) | eval_test.json 비교 |
| **Comparator** | Skill (project-review) | 버전 간 회귀 감지 |

#### Verify 프로세스

```
Task: "Code 검증" → TaskCompleted Hook 트리거
  ↓
Hook 스크립트 실행 (.claude/hooks/verify-task.sh)
  ├─ 품질 메트릭 검증
  ├─ 테스트 커버리지 확인
  └─ 성능 기준 확인

결과:
  ✓ 통과 → 종료
  ✗ 실패 → 종료 코드 2 (차단) + 피드백 → Executor 수정
```

### 2.4 Teammate 통신 및 조율

#### 공유 작업 목록 (Task List)

```
~/.claude/teams/{team-name}/tasks/

Task 1: "요구사항 분석"  [Planner]
  status: done
  assignee: Planner
  dependencies: []

Task 2: "아키텍처 설계" [Planner] (우선순위)
  status: in-progress
  assignee: Planner
  dependencies: [Task 1]

Task 3: "코드 구현" [Executor]
  status: pending
  assignee: Executor
  dependencies: [Task 1, Task 2]
  → Task 2 완료까지 차단됨 (자동 관리)

Task 4: "산출물 검증" [Verifier]
  status: pending
  assignee: Verifier
  dependencies: [Task 3]
  → Task 3 완료까지 차단됨
```

#### 메시지 시스템 (Mailbox)

```
Leader → Planner: "요구사항 분석 시작. 이 문서 검토하고 계획 수립해줘"
  ↓
Planner: [계획 수립] → 승인 요청
  ↓
Leader: [계획 검토] → "승인" or "피드백"
  ↓
(승인 시) Planner → Executor: "계획 완료. 첨부 문서로 구현 시작해줘"
  ↓
Executor: [구현] → 완료
  ↓
Executor → Verifier: "코드 완료. 검증해줘"
  ↓
Verifier: [검증] → 문제 발견 시 Leader에게 보고
```

### 2.5 Hooks를 통한 외부 검증 레이어

```yaml
# .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "command": "bash .claude/hooks/pre-tool-use.sh",
        "timeout": 5
      }
    ],
    "PostToolUse": [
      {
        "command": "bash .claude/hooks/post-tool-use.sh",
        "timeout": 10
      }
    ],
    "TaskCompleted": [
      {
        "command": "bash .claude/hooks/verify-task.sh",
        "timeout": 30,
        "onFailure": "block"  # 실패 시 완료 차단
      }
    ],
    "TeammateIdle": [
      {
        "command": "bash .claude/hooks/check-idle-reason.sh",
        "timeout": 5
      }
    ]
  }
}
```

#### Hook 스크립트 예시

**verify-task.sh** (TaskCompleted 검증):
```bash
#!/bin/bash
TASK_ID=$1
TASK_STATUS=$2

# 품질 게이트
if [ "$TASK_STATUS" = "completed" ]; then
  echo "검증 시작..."

  # 테스트 실행
  npm test --coverage
  if [ $? -ne 0 ]; then
    echo "테스트 실패"
    exit 2  # 완료 차단
  fi

  # 코드 품질 검사
  npx eslint .
  if [ $? -ne 0 ]; then
    echo "코드 품질 기준 미만"
    exit 2
  fi

  echo "검증 통과"
  exit 0
fi
```

**post-tool-use.sh** (도구 사용 후 검증):
```bash
#!/bin/bash
TOOL=$1
ARGS=$2
RESULT=$3

# 위험한 작업 검증
if [ "$TOOL" = "bash" ] && [[ "$ARGS" =~ "rm -rf" ]]; then
  echo "위험: 재귀 삭제는 수동 승인 필수"
  exit 2  # 도구 실행 차단, 사용자 승인 요청
fi

exit 0
```

### 2.6 정보 흐름 (Information Flow Diagram)

```
┌─────────────────────────────────────────────────────────┐
│           PLAN PHASE (Planner Teammate)                 │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Inputs:                                                  │
│  - 비즈니스 요구사항 (Leader가 메시지로 전달)            │
│  - 기존 시스템 설명서 (file_read)                       │
│                                                           │
│  Process:                                                 │
│  - Requirements Analyst가 기능/비기능 요구사항 명시      │
│  - System Architect가 기술 설계                         │
│  - Balanced Judge가 계획 검증                           │
│                                                           │
│  Outputs (메타정보 제거):                                │
│  ├─ User Stories (함수형 요구사항)                      │
│  ├─ Architecture Docs (기술 결정)                       │
│  └─ Implementation Plan (로드맵)                        │
│     → 작업 목록에 저장, Executor에 "계획 완료" 메시지   │
│                                                           │
│  [Plan Approval 게이트]                                  │
│  → Leader가 "승인" or "거부" (피드백 포함)               │
│     [승인] → Execute 단계 진행 허용                     │
│     [거부] → Planner가 피드백 반영, 재계획               │
│                                                           │
└─────────────────────────────────────────────────────────┘
            ↓ (산출물만 전달, Planner 정보 X)
┌─────────────────────────────────────────────────────────┐
│          EXECUTE PHASE (Executor Teammate)               │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Inputs (메타정보 제거):                                  │
│  - User Stories (누가 만들었는지 정보 X)                 │
│  - Architecture Docs (구현 가이드만)                    │
│  - Implementation Plan                                    │
│                                                           │
│  Process:                                                 │
│  - Code Developer가 독립적으로 구현                      │
│  - TDD: Red→Green→Refactor                              │
│  - 테스트 80%+ 커버리지                                  │
│                                                           │
│  Outputs (메타정보 제거):                                │
│  ├─ Code (클린, 테스트 포함)                            │
│  ├─ Unit Tests                                          │
│  ├─ Integration Tests                                    │
│  └─ Performance Metrics                                 │
│     → 작업 목록에 저장, Verifier에 "구현 완료" 메시지   │
│                                                           │
│  [TaskCompleted Hook]                                    │
│  → Hook 스크립트가 코드 품질 검증                       │
│     ✓ 통과 → Verifier에게 전달                         │
│     ✗ 실패 → "수정 필요" 피드백 + 재구현                │
│                                                           │
└─────────────────────────────────────────────────────────┘
            ↓ (산출물만 전달, Executor 정보 X)
┌─────────────────────────────────────────────────────────┐
│           VERIFY PHASE (Verifier Teammate)               │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Inputs (완전히 독립):                                    │
│  - Code (작성자 정보 X)                                 │
│  - Tests                                                │
│  - Metrics                                              │
│                                                           │
│  Process (병렬 검증):                                    │
│  - Quality Reviewer: 구조, 성능, DRY 원칙               │
│  - Security Reviewer: 보안 취약점                       │
│  - Edge Case Reviewer: 경계값, 예외                     │
│  - Logic Reviewer: 로직 정합성                          │
│  - Grader: eval_test.json vs 실행결과                   │
│  - Comparator: 회귀 감지 (이전 버전 대비)               │
│                                                           │
│  Decision:                                                │
│  ✓ 통과 → Leader에게 "승인" 보고                       │
│  ✗ 실패 → "문제: [구체적 내용]" 보고                   │
│     → Executor에게 수정 지시 (Verifier는 Executor를     │
│        누군지 모름, Leader가 중개)                       │
│                                                           │
│  [완전 독립성 보장]                                       │
│  - Verifier는 Planner를 모름                            │
│  - Verifier는 Executor를 모름                           │
│  - Verifier는 설계 과정을 모름                          │
│  - Verifier는 순수 품질만 평가                          │
│                                                           │
└─────────────────────────────────────────────────────────┘
            ↓ (Leader가 최종 판단)
┌─────────────────────────────────────────────────────────┐
│    [Iterate] 실패 시 Executor 수정 후 다시 Verify      │
│    [Complete] 통과 시 최종 승인                          │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 독립성 확보 방안 (최우선) - Agent Teams 중심

### 3.1 Agent Teams를 통한 구조적 독립성 강제

Agent Teams는 **구조적으로 독립성을 강제**하는 PRIMARY 메커니즘이다.

#### 3.1.1 구조적 강제 메커니즘

| 메커니즘 | 설명 | 효과 |
|---------|------|------|
| **완전히 독립된 인스턴스** | 각 Teammate는 별도 Claude Code 프로세스 | 컨텍스트 완전 격리 |
| **리더 대화 기록 미전달** | Teammate 생성 시 Leader의 대화만 보임, 이전 기록 X | 앵커링 편향 제거 |
| **공유 작업 목록** | 명시적 작업 할당, 종속성 자동 관리 | 정보 차단 강제 |
| **메시지 기반 통신** | 암묵적 공유 불가, 명시적 메시지만 가능 | 투명성 확보 |
| **Plan Approval 게이트** | 계획 단계 완료 후 실행 전 승인 필수 | 계획-실행 분리 강제 |
| **Hooks 검증 레이어** | 실행자 제외된 외부 스크립트가 품질 검증 | 자기평가 편향 제거 |

#### 3.1.2 Ann의 Windows 환경 최적화 설정

```json
// settings.json (Ann의 Windows PC)
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "maxTokens": 100000,
  "teamMode": "in-process",  // Windows에서 tmux 불가 → in-process 권장
  "displayMode": "split",     // 또는 "in-process"로 Shift+Down 순환
  "hooks": {
    "TaskCompleted": [
      {
        "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/verify-task.ps1",
        "timeout": 30,
        "onFailure": "block"
      }
    ]
  }
}

// .claude.json (Ann의 프로필)
{
  "teammate": {
    "inProcessMode": true,      // in-process 팀원 표시
    "maxTeammateInstances": 5,
    "autoCleanupTimeout": 3600  // 1시간 유휴 후 정리
  },
  "hooks": {
    "powershellVersion": "7.0",  // PowerShell Core 사용
    "encoding": "UTF-8"
  }
}
```

### 3.2 3가지 독립성 패턴

#### 3.2.1 패턴 A: Plan-Execute-Verify 완전 분리 (표준)

```
Team 구성: Leader + Planner Teammate + Executor Teammate + Verifier Teammate

Step 1: Planner 생성 (plan mode)
────────────────────────────────
Leader: "Create a teammate using the planner agent type"
  → Planner 생성, 독립 컨텍스트에서 실행
  → CLAUDE.md 로드 (Leader의 대화 기록 X)
  → 요구사항 분석, 설계 수립

Step 2: Plan Approval 게이트
──────────────────────────────
Planner: "요구사항 분석 완료. 계획 승인 부탁합니다"
  [작업 목록에 "plan" 작업 완료 표시]

Leader: [계획 검토]
  "✓ 승인" → Executor 생성 진행
  "✗ 거부" → "이 부분 보완 필요: ..." (피드백)
           → Planner가 피드백 반영, 재계획

Step 3: Executor 생성 (auto mode)
──────────────────────────────────
(Plan Approval 통과 후)
Leader: "Create executor using the code-developer agent type. Here's the plan."
  → Executor 생성, 독립 컨텍스트에서 실행
  → Plan의 산출물만 전달 (Planner 정보 X)
  → 구현 시작

Step 4: 구현 프로세스
────────────────────
Executor: [TDD 사이클]
  - Red: 테스트 작성
  - Green: 최소 구현
  - Refactor: 최적화
  → 80%+ 테스트 커버리지

Step 5: TaskCompleted Hook (자동 검증)
────────────────────────────────────────
Executor가 "구현 완료" 표시
  ↓
Hook 스크립트 자동 실행 (.claude/hooks/verify-task.ps1)
  ├─ npm test --coverage (기준: 80%+)
  ├─ npx eslint . (코드 품질)
  ├─ npm run build (빌드 가능 여부)
  └─ Performance check (메모리, 속도)

  ✓ 통과 → Verifier에게 전달
  ✗ 실패 → "테스트 70%, 기준 80%" → Executor 수정

Step 6: Verifier 생성 (검증 전용)
──────────────────────────────────
(자동 검증 통과 후)
Leader: "Create verifier using the quality-reviewer agent type"
  → Verifier 생성, 완전히 독립 컨텍스트
  → Code만 전달 (Planner/Executor 정보 X)

Step 7: 병렬 검증 (Hooks 활용)
──────────────────────────────
Verifier와 함께 Hook 스크립트들도 동시 실행:
  - pre-tool-use.sh: 위험한 도구 호출 검증
  - post-tool-use.sh: 도구 결과 검증
  - verify-task.sh: 최종 품질 게이트

Verifier 피드백:
  "✅ Quality: Good DRY principle, performance optimal"
  "⚠️ Edge Case: Empty user history not handled"
  "✅ Security: No SQL injection, proper JWT validation"
  "❌ Regression: Memory usage 5x vs previous (Redis TTL issue)"

Step 8: 수정 및 재검증 (Iterate)
─────────────────────────────────
Leader: [Verifier의 피드백을 읽고]
  → "Executor, 빈 사용자 기록 처리 추가해줘"
    (Verifier가 찾은 문제, but Verifier 자신은 안 봄)
  → Executor 수정 시작

Executor: [문제 수정]
  → TaskCompleted Hook 다시 실행
  → 통과 시 Verifier 재검증

Step 9: 최종 승인 (Quality Manager)
────────────────────────────────────
Leader (또는 별도 Quality Manager Teammate):
  "모든 검증 완료? 문제점 모두 해결?"
  → ✓ 최종 승인 → 프로덕션 배포
  → ✗ "아직 문제 있음" → 반복
```

#### 3.2.2 패턴 B: 경쟁적 검증 (Adversarial Review)

```
Team 구성: Leader + Investigator A + Investigator B + Investigator C

사용 사례: 버그 원인 분석, 복잡한 문제 해결

Example: "Why is the database query 10x slower than expected?"

Step 1: 독립 가설 수립
─────────────────────
Leader: "Create three investigators. Each proposes a hypothesis."

Investigator A (가설 1: "Index 누락"):
  - DB 스키마 분석 → Index 없음 확인
  - 결론: "CREATE INDEX 필요"

Investigator B (가설 2: "N+1 Query"):
  - 쿼리 로그 분석 → N+1 패턴 발견
  - 결론: "JOINs로 최적화"

Investigator C (가설 3: "Network Latency"):
  - 네트워크 메트릭 분석
  - 결론: "데이터베이스 연결 pool 재설정"

Step 2: 상호 반박 (Adversarial)
───────────────────────────────
Leader: "A, B, C의 가설을 검증. 서로 반박해줘."

Investigator A:
  "B의 N+1은 이미 최적화됨 (JOINs 사용 중). C의 네트워크는 50ms로 정상."
  → "내 가설 Index 누락이 맞다."

Investigator B:
  "A가 최신 로그만 봤다. 어제 로그에 N+1이 있다. C의 pool은 정상."
  → "내 가설이 맞다."

Investigator C:
  "A와 B의 분석 도구 시간이 다르다 (UTC vs Local). 네트워크 지연은..."
  → [약간 약한 가설]

Step 3: 수렴
────────────
Leader: "가장 설득력 있는 가설은?"
  → A와 B 중 선택 필요
  → 실제 테스트: Index 추가 vs JOINs 최적화
  → 데이터 기반 선택

✅ 효과: 앵커링 편향 완전 제거 (3개 팀원이 상호 독립적)
```

#### 3.2.3 패턴 C: 교차 검증 리뷰

```
Team 구성: Leader + Security Reviewer + Performance Reviewer + Coverage Reviewer

사용 사례: PR 리뷰 (다각적 관점)

Example: "Review the new payment processing module"

Step 1: 병렬 독립 검증
──────────────────────
Leader: "Three reviewers, each checks different aspects"

Security Reviewer (보안만 검증):
  - SQL Injection 검사 → ✅ Parameterized queries 사용
  - XSS 취약점 → ✅ Input sanitization OK
  - CSRF Token → ✅ Present and validated
  - 암호화 → ⚠️ Plaintext password log found!
  → 보고: "암호화되지 않은 로그 발견"

Performance Reviewer (성능만 검증):
  - O(n) vs O(n²) 알고리즘 → ✓ O(n)
  - 메모리 누수 → ✓ 없음
  - DB 쿼리 효율 → ⚠️ 1000명 사용자 시 1초 소요
    (실제 필요: 100ms)
  → 보고: "대규모 사용자 성능 미흡"

Coverage Reviewer (테스트만 검증):
  - 단위 테스트 커버리지 → 85%
  - 통합 테스트 → Happy path only
  - 엣지 케이스 → ✗ 테스트 누락
    (금액 0, 음수, 초과)
  → 보고: "엣지 케이스 테스트 필요"

Step 2: 검토자들 간 협력 (팀 내 소통)
──────────────────────────────────────
Security Reviewer → Performance Reviewer:
  "암호화 추가 시 성능 영향 있을까?"

Performance Reviewer:
  "PBKDF2는 무시할 수준. 암호화 추가 권고."

Coverage Reviewer:
  "엣지 케이스 테스트 우선순위 어디?"

Step 3: 최종 리뷰 결과 (Leader가 종합)
────────────────────────────────────────
✗ 승인 거부. 수정 필요:
  1. 암호화되지 않은 로그 제거 (Security)
  2. 대규모 사용자 성능 최적화 (Performance)
  3. 엣지 케이스 테스트 추가 (Coverage)

✅ 효과: 동일 코드에 대한 3개 독립적 관점
```

### 3.3 3중 검증 체계

```
┌────────────────────────────────────────────────────────────┐
│                   1차: 팀 내 독립성                         │
│                 (Agent Teams 구조 자체)                    │
├────────────────────────────────────────────────────────────┤
│                                                              │
│ Planner (독립) → Executor (독립) → Verifier (독립)         │
│                                                              │
│ - 각자 독립 컨텍스트 (리더 대화 기록 X)                    │
│ - 명시적 메시지만 통신                                      │
│ - 서로의 프로세스를 모름                                    │
│                                                              │
├────────────────────────────────────────────────────────────┤
│                 2차: Hook 기반 품질 게이트                   │
│            (실행자 제외된 외부 검증 레이어)                │
├────────────────────────────────────────────────────────────┤
│                                                              │
│ Executor가 완료 표시 → Hook 자동 실행                      │
│   ├─ pre-tool-use.sh: 위험한 도구 호출 차단               │
│   ├─ post-tool-use.sh: 결과 검증                          │
│   ├─ verify-task.sh: 최종 품질 게이트                     │
│   └─ temate-idle.sh: 유휴 상태 검증                       │
│                                                              │
│ [Hook은 독립 스크립트, Executor와 완전 분리]              │
│                                                              │
├────────────────────────────────────────────────────────────┤
│            3차: 팀간 독립성 (다중 팀 활용)                  │
│         (여러 Team Leaders로 상호 검증)                   │
├────────────────────────────────────────────────────────────┤
│                                                              │
│ Main Team:        Plan-Execute-Verify                      │
│   ↓ (산출물 공유, 프로세스 X)                              │
│ Audit Team:       완전히 독립된 다시 검증                  │
│   (같은 산출물, 다른 팀원들, 다른 관점)                    │
│                                                              │
│ [조직 수준의 최종 품질 보증]                               │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

### 3.4 컨텍스트 격리 전략

#### 3.4.1 단계 간 명시적 Handoff

```yaml
# 🚫 위험한 방식 (context sharing)
Leader 세션:
  - [Planner와 모든 대화 기록 포함]
  - Executor 생성: Planner 정보 + 대화 기록 모두 전달
  → Executor가 Planner의 결정에 영향받음 (앵커링 편향)

# ✅ 안전한 방식 (output-only handoff)
Leader 세션:
  - [Planner와 대화]
  - Planner 완료: 산출물만 추출
    ├─ requirements.md (요구사항만, "누가" 정보 X)
    ├─ architecture.md (설계만, "왜" 과정 X)
    └─ plan.md (계획만, Planner의 생각 과정 X)
  - Executor 생성: 산출물만 전달
    "Here are the outputs. Please implement. Don't see Planner's thoughts."
  → Executor가 산출물 기반 독립 판단
```

#### 3.4.2 Subagent 격리 설정

```yaml
# Executor Subagent 정의
---
memory:
  scope: "project"        # Project 수준 메모리 공유
  retention: "persistent" # 세션 후에도 유지
---
# 효과:
# - Executor의 학습은 저장 (다음 회차에서 재사용)
# - 하지만 Planner의 대화 기록은 포함 안 함
# - Verifier도 별도 메모리 (독립성 유지)
```

#### 3.4.3 Metadata 제거 메커니즘

```python
# .claude/hooks/strip-metadata.py
def strip_plan_metadata(plan_doc):
    """Plan 문서에서 메타정보 제거"""
    lines = plan_doc.split('\n')
    result = []

    for line in lines:
        # 제거 대상
        if line.startswith("# 작성 과정"):
            continue
        if line.startswith("## Planner의 생각"):
            continue
        if "Complexity 분석" in line:
            continue

        # 보존 대상
        if line.startswith("# Requirements"):
            result.append(line)
        if line.startswith("# Architecture"):
            result.append(line)
        if line.startswith("# Implementation Plan"):
            result.append(line)

    return '\n'.join(result)

# 사용
with open('plan.md') as f:
    plan = f.read()

clean_plan = strip_plan_metadata(plan)
# → Executor에게 전달
```

### 3.5 독립성 규칙 정리

#### 규칙 1: 3-Teammate 역할 분리

| Phase | Teammate | 권한 | 책임 | 제한사항 |
|-------|----------|------|------|---------|
| **Plan** | Planner (plan mode) | Read-only | 요구사항, 설계, 계획 | 실행 불가 |
| **Execute** | Executor (auto mode) | Read-Write | 구현, 테스트 | Planner를 모름 |
| **Verify** | Verifier (default) | Read-only | 품질 검증 | 실행과정을 모름 |

#### 규칙 2: 정보 차단 (Information Barrier)

```
Plan 산출물 (메타정보 제거)
  ↓
Executor에게 전달 (Planner 정보 X)
  ↓
Execute 산출물 (구현 과정 제거)
  ↓
Verifier에게 전달 (Executor 정보 X)
  ↓
[독립적 평가]
```

#### 규칙 3: Feedback Loop (피드백만 전달)

```
Verifier: "문제 발견: 엣지 케이스 처리 누락"
  ↓
Leader: (Verifier 정보는 숨기고) Executor에게 전달
  "구현에 문제 있음: 엣지 케이스 처리 누락"
  ↓
Executor: 수정
  (Verifier를 모르고, 문제만 해결)
```

#### 규칙 4: Meta-Verification (Quality Manager의 역할)

```
Quality Manager (Leader 또는 별도 팀원)는:
✓ "전체 프로세스가 독립성 원칙을 지켰나?"
✓ "Planner → Executor → Verifier 경계가 명확한가?"
✓ "누군가 자신의 작업을 평가했나?"
✓ "Feedback이 객관적인가?"

✗ "이 결과가 좋은가?" (이건 Verifier의 일)
✗ "이 설계가 맞는가?" (이건 Execute와 Verify의 대상)
```

### 3.6 자기평가 편향 제거 매트릭스

| 편향 유형 | 기존 위험 | Agent Teams 해결 | Hook 강화 |
|----------|---------|----------------|---------|
| **Confirmation Bias** | Planner가 자신의 설계만 검증 | ✓ Verifier가 독립 검증 | Hook 다각적 검사 |
| **Anchoring Bias** | Executor가 첫 설계에 고착 | ✓ 독립 컨텍스트, 새로운 관점 | Hook이 객관적 기준 적용 |
| **Authority Bias** | Planner의 "이렇게 하자"만 따름 | ✓ Executor 독립 판단 권장 | Hook이 최종 판정 |
| **Self-serving Bias** | "내 구현이 좋다"고 평가 | ✓ Verifier가 제3자 평가 | Hook이 강제 검증 |
| **Dunning-Kruger** | "충분하다"고 자기평가 | ✓ Verifier의 전문가 검증 | Hook이 기준점 제시 |

---

## 4. 미커버 영역 및 보완 제안

### 4.1 커버리지 현황

**전체: 49개 요소 중**
- **완전 해결 (●)**: 18개 요소
- **부분 해결 (◐)**: 19개 요소 (기반 제공, 추가 구성 필요)
- **기반 제공 (◐→●)**: 13개 요소 (Agent Teams 적용 시)
- **미해결 (○)**: 12개 요소 (인프라/기술 설계)

**Agent Teams 적용 시 커버리지**: 73% (36/49)

### 4.2 완전히 미커버인 영역 (인프라 설계 필요)

| # | 요소 | 범주 | 이유 | 해결 방안 |
|---|------|------|------|---------|
| 3 | **App Server 아키텍처 (JSON-RPC)** | Architecture | Infrastructure layer | JSON-RPC 서버 명세 설계 |
| 4 | **NLAH 명세** | Framework | Framework abstraction | YAML 명세 포맷 정의 + adapter |
| 19 | **Multi-client Architecture** | Multi-Client | CLI/Web/IDE 지원 | 아키텍처 설계 (3-6개월) |
| 20 | **Streaming Progress** | Real-time | SSE/WebSocket 구현 | 서버 인프라 구현 |
| 21 | **IDE Plugin Integration** | IDE | VSCode extension | IDE 플러그인 개발 |
| 27 | **Filesystem Access Control** | Security | OS-level policy | File ACL + permission layer |

**액션**: 이 6개는 **기술 설계 작업** (3-6개월 병렬 진행 가능)

### 4.3 부분 해결 영역 (추가 구성 필요)

#### 4.3.1 단계 1: Agent Teams 기본 설정 (1-2주)

| 요소 | 현재 상태 | 필요 작업 | 완료 기준 |
|------|---------|---------|---------|
| PGE 3-Agent Loop | ◐→● | Plan/Execute/Verify Teammate 정의 | 샘플 프로젝트 완전 사이클 실행 |
| Shared Context | ◐→● | 팀 작업 목록 구현 | 팀원 간 메시지 동작 확인 |
| Skills Versioning | ◐→● | SKILL.md 버전 명시 + Subagent preload | 버전별 Skill 로드 테스트 |
| Skill Format | ◐→● | YAML frontmatter 완전 명시 | 모든 Skill이 frontmatter 포함 |

#### 4.3.2 단계 2: Hooks 검증 레이어 (1-2주)

| 요소 | 현재 상태 | 필요 작업 | 완료 기준 |
|------|---------|---------|---------|
| Advisory vs Hooks | ◐→● | PreToolUse/PostToolUse/TaskCompleted Hook | Hook이 자동 검증 동작 |
| Skill Permission | ◐→● | allowed-tools + disable-model-invocation | 도구별 권한 제어 확인 |
| Approval Workflow | ◐→● | Plan Approval 게이트 구현 | 승인 전까지 실행 차단 확인 |

#### 4.3.3 단계 3: Subagent 강화 (2-4주)

| 요소 | 현재 상태 | 필요 작업 | 완료 기준 |
|------|---------|---------|---------|
| Checkpoint 시스템 | ◐→◐ | Hooks + Subagent persistent memory | 체크포인트 자동 저장/복구 |
| Handoff State Machine | ◐→● | Task dependency 관리 | 작업 자동 라우팅 동작 |
| Task Delegation | ◐→● | Subagent chain 구현 | 위임-보고 패턴 검증 |

### 4.4 신규 에이전트 추가 제안 (우선순위별)

#### 우선순위 1 (Phase 1: Agent Teams 완성 후)

| # | 에이전트 | 역할 | 필요성 | 하네스 영역 |
|---|---------|------|--------|-----------|
| **1** | **Implementation Planner** | 설계 → 구현 로드맵 변환 | 높음 | Plan-Execute 브릿지 |
| **2** | **Progressive Monitor** | 진행 중 점진적 품질 체크 | 높음 | Verify 실시간 모니터링 |

#### 우선순위 2 (Phase 2: 2-4주)

| # | 에이전트 | 역할 | 하네스 영역 |
|---|---------|------|-----------|
| **3** | **Database Architect** | DB 스키마 설계 + 정규화 | Execute (Backend) |
| **4** | **API Designer** | REST/GraphQL/gRPC 계약 설계 | Execute (API 설계) |

### 4.5 신규 스킬 추가 제안

#### 우선순위 높음

| # | 스킬명 | 목적 | 대상 영역 |
|---|--------|------|---------|
| **1** | **functional-test-generator** | E2E 시나리오 자동 생성 (Playwright) | Execute/Verify |
| **2** | **performance-profiler** | 성능 병목 자동 분석 | Verify |
| **3** | **api-contract-generator** | OpenAPI 계약서 자동 생성 | Plan/Execute |

---

## 5. 구현 로드맵

### Phase 1: Immediate (1-2주) - Agent Teams 핵심 구현

#### 목표
Agent Teams 기본 활성화 + 3-Teammate 구조 정의 + Hook 검증 레이어 구현

#### 할 일

| 순번 | 작업 | 담당 | 완료 기준 |
|------|------|------|---------|
| 1 | **Agent Teams 활성화** | Infrastructure | settings.json에 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 설정 |
| 2 | **Planner Teammate 정의** | Planner Agent | .claude/agents/planner.md (plan mode, read-only) |
| 3 | **Executor Teammate 정의** | Executor Agent | .claude/agents/executor.md (auto mode, read-write) |
| 4 | **Verifier Teammate 정의** | Verifier Agent | .claude/agents/verifier.md (default, read-only) |
| 5 | **기존 30개 Agent → Subagent 마이그레이션** | All Agents | Agent 정의를 Subagent 타입으로 변환 |
| 6 | **Hook 기반 검증 스크립트** | QA | verify-task.ps1, pre-tool-use.ps1 (PowerShell) |
| 7 | **팀 작업 목록 구조 정의** | Context Manager | Task dependencies 및 상태 관리 스키마 |
| 8 | **Sample Project (웹앱)** | All | Plan-Execute-Verify 완전 사이클 실행 |
| 9 | **독립성 규칙 문서화** | Documentation | INDEPENDENCE_RULES.md 작성 |

#### 산출물
- ✅ Agent Teams 설정 파일 (settings.json, .claude.json)
- ✅ 3개 Teammate 정의 (.claude/agents/*.md)
- ✅ Hook 스크립트 세트 (.claude/hooks/*.ps1)
- ✅ 샘플 프로젝트 Plan-Execute-Verify 결과물
- ✅ 독립성 원칙 문서 (한국어)

### Phase 2: High Priority (2-4주) - Agent Teams 스케일링

#### 목표
실제 프로젝트에 Agent Teams 적용 + 복잡한 작업 지원

#### 할 일

| 순번 | 작업 | 완료 기준 |
|------|------|---------|
| 1 | **Agent Teams 팀 크기 확대** (3명→5명) | Specialist Teammate 추가 (DB, API, Security) |
| 2 | **기존 30개 Agent → Subagent 타입 완전 마이그레이션** | 모든 Agent가 Subagent YAML 정의 포함 |
| 3 | **Skill → Agent Teams 연계 최적화** | Teammate가 자동으로 필요 Skill 로드 |
| 4 | **실제 프로젝트 1개에 Agent Teams 적용** | 중간 규모 프로젝트 (2-4주 기간) |
| 5 | **Hooks 검증 레이어 강화** | TaskCompleted, TeammateIdle 모두 작동 |
| 6 | **외부 CI/CD 연동 프로토타입** | Git commit hook + PR workflow |

### Phase 3: Medium Priority (3-6주) - 인프라 설계

#### 목표
Architecture 계층 설계 (기술 팀이 구현)

#### 할 일

| 순번 | 작업 | 담당 |
|------|------|------|
| 1 | **JSON-RPC App Server 아키텍처 설계** | Technical Design |
| 2 | **Multi-client 지원 설계** (CLI/Web/IDE) | Architecture |
| 3 | **Database Architect Agent 개발** | Agent Development |
| 4 | **API Designer Agent 개발** | Agent Development |
| 5 | **functional-test-generator Skill 개발** | Skill Development |
| 6 | **VSCode IDE Plugin 기본 구현** | IDE Integration |

### Phase 4: Enterprise Scale (6개월+)

#### 목표
조직 규모 배포, 특화 팀 구성

#### 할 일
- Multi-tenant isolation 완성도
- 조직 정책 자동 적용 (Organization-level CLAUDE.md)
- VSCode IDE Plugin 완성도
- React Native / Flutter 개발 Skill
- PowerShell 호환 완전 보장 (Ann의 Windows 환경)

---

## 6. 구현 우선순위 매트릭스

```
                              영향도
                        낮음        높음
                      ┌────────────────┐
            높음       │    ◉ Phase 1   │
빠          │         │  1,5,6,11,13   │
    ←───────┤  낮음    │  22,23,25,26   │
    빠       │         │               │
            │         │    ◐ Phase 2  │
            │         │  2,7,10,16,17 │
            │         │               │
            │         │    ○ Phase 3+ │
            │         │   3,4,19,20,21│
            │         │               │
            └────────────────────────┘

PHASE 1 (긴급, 높은 영향, 빠른 구현):
  #1 PGE 3-Agent Loop
  #5 Shared Context Store
  #6 Checkpoint 시스템
  #11 Skills Versioned
  #13 Skill Format
  #22 Git + CI-CD
  #23 Handoff 메커니즘
  #25 Hybrid Execution
  #26 Approval Workflow
  #49 Advisory vs Hooks

PHASE 2 (중요, 중간 영향):
  #2 Initializer Agent
  #7 Auto Context Compaction
  #10 Context Reuse
  #16 Confidence-Based Auto-Approval
  #17 Audit Log

PHASE 3+ (구조적, 낮은 영향, 오래 구현):
  #3 App Server
  #4 NLAH
  #19 Multi-client
  #20 Streaming
  #21 IDE Plugin
```

---

## 7. 종합 분석 및 권고사항

### 7.1 독립성 달성 현황

| 항목 | 기존 | Agent Teams 적용 후 |
|------|------|------------------|
| **Plan vs Execute 분리** | 70% (같은 세션, 컨텍스트 혼재) | 90% (완전히 다른 인스턴스) |
| **Execute vs Verify 분리** | 90% (Hook 제공) | 98% (구조 + Hook 이중) |
| **자기평가 편향 제거** | 60% (규칙 기반) | 20% (구조적 강제) |
| **정보 차단 효과** | 50% (선택적) | 95% (의무적) |

### 7.2 Ann의 Windows 환경 최적화

```json
// recommended settings.json for Ann
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "maxTokens": 100000,
  "teamMode": "in-process",
  "displayMode": "in-process",
  "hooks": {
    "powershellVersion": "7.0",
    "encoding": "UTF-8"
  },
  "teammate": {
    "inProcessMode": true,
    "maxInstances": 5
  }
}

// .claude/agents/ 구조
.claude/
├── agents/
│   ├── planner.md (plan mode)
│   ├── executor.md (auto mode)
│   ├── verifier.md (default mode)
│   ├── security-reviewer.md
│   ├── performance-reviewer.md
│   └── ...기존 30개 Agent
├── hooks/
│   ├── verify-task.ps1 (PowerShell)
│   ├── pre-tool-use.ps1
│   ├── post-tool-use.ps1
│   └── check-idle.ps1
└── settings.json
```

### 7.3 주요 성공 요인 (Critical Success Factors)

1. **Agent Teams 활성화** (즉시)
   - 실험적 기능이므로 비판적으로 모니터링
   - Windows에서 in-process 모드 검증

2. **Teammate 정의 명확화** (1-2주)
   - Planner: read-only, plan mode
   - Executor: auto mode, isolated context
   - Verifier: read-only, independent instance

3. **Hook 검증 자동화** (1-2주)
   - PowerShell 스크립트 (Ann의 환경)
   - 객관적 기준 (코드 품질, 테스트, 성능)

4. **기존 자산 통합** (2-4주)
   - 30개 Agent → Subagent 타입 마이그레이션
   - 47개 Skill을 Teammate가 자동 로드

5. **실제 프로젝트 검증** (4-8주)
   - 샘플이 아닌 실제 프로젝트에 적용
   - 피드백 루프 자동화

### 7.4 리스크 및 완화 전략

| 리스크 | 완화 전략 |
|--------|---------|
| **토큰 비용 폭발** | 팀 크기 3-5명 제한, 비용 모니터링 |
| **Teammate 조율 복잡도** | 처음엔 3명(Plan/Execute/Verify)으로 시작 |
| **Hook 실패 시 처리 불명확** | 종료 코드 2 → 완료 차단 + 피드백 명문화 |
| **Windows 호환성** | PowerShell 스크립트, in-process 모드만 사용 |
| **기존 워크플로우 변경** | Phase별 점진적 도입, 학습 시간 확보 |

### 7.5 권고 (Recommendation)

**즉시 실행** (1주):
1. Agent Teams 활성화 (settings.json)
2. Planner, Executor, Verifier Teammate 정의
3. Hook 스크립트 3개 (verify-task, pre-tool-use, post-tool-use)
4. 샘플 웹앱 프로젝트로 완전 사이클 테스트

**우선 순위** (2주):
1. 기존 30개 Agent → Subagent 타입 변환
2. 47개 Skill YAML frontmatter 완성
3. Task dependency 관리 자동화

**단기** (4주):
1. 실제 프로젝트 1개에 Agent Teams 적용
2. Hooks 검증 레이어 강화
3. 팀 크기 3명 → 5명 확대

**중기** (6-12주):
1. 인프라 설계 시작 (App Server, Multi-client)
2. 신규 Specialist Teammate 추가
3. IDE Plugin 프로토타입

### 7.6 성공 메트릭

```
Month 1 (Phase 1):
  - ✓ Agent Teams 활성화
  - ✓ 3-Teammate 프로토타입 완료
  - ✓ 샘플 프로젝트 Plan-Execute-Verify 사이클 완료
  - 목표: 30% 생산성 증대 (자동화)

Month 2-3 (Phase 2):
  - ✓ 실제 프로젝트 1개 적용
  - ✓ 기존 Agent 마이그레이션 완료
  - 목표: 50% 생산성 증대 + 자기평가 편향 80% 제거

Month 3+ (Phase 3):
  - ✓ 인프라 계층 설계 완료
  - ✓ 특화 팀 구성 (5명→7명)
  - 목표: 75% 생산성 증대 + 자기평가 편향 95% 제거
```

---

## 부록 A: 권장 설정 파일

### settings.json

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "claude": {
    "maxTokens": 100000,
    "teamMode": "in-process",
    "displayMode": "in-process"
  },
  "hooks": {
    "PreToolUse": [
      {
        "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/pre-tool-use.ps1",
        "timeout": 5
      }
    ],
    "PostToolUse": [
      {
        "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/post-tool-use.ps1",
        "timeout": 10
      }
    ],
    "TaskCompleted": [
      {
        "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/verify-task.ps1",
        "timeout": 30,
        "onFailure": "block"
      }
    ],
    "TeammateIdle": [
      {
        "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/check-idle-reason.ps1",
        "timeout": 5
      }
    ]
  },
  "teams": {
    "maxTeammates": 5,
    "defaultSize": 3,
    "autoCleanupTimeout": 3600
  }
}
```

### .claude/agents/planner.md

```yaml
---
name: "Planner - Requirements Analyst"
description: "요구사항 분석 및 설계 수립 (실행 불가)"
model: "claude-opus-4-20250101"
permissionMode: "plan"
tools: ["file_read", "code_search", "grep"]
disallowedTools: ["file_create", "file_edit", "bash", "git_push"]
skills: ["claude-strategy", "design-spec-form"]
memory:
  scope: "project"
  retention: "persistent"
hooks:
  PreToolUse: ".claude/hooks/pre-tool-use.ps1"
background: "당신은 요구사항 분석가입니다. 비즈니스 요구사항을 기술 스펙으로 변환합니다. 실행하지 말고 계획만 수립합니다."
---

# Planner Teammate

당신의 역할:
1. 비즈니스 요구사항 명확화
2. 기능/비기능 요구사항 정의
3. 기술 아키텍처 설계
4. 구현 로드맵 수립
5. 위험 요소 분석

## 작업 프로세스

1. 입력받은 요구사항을 체계적으로 분석
2. User Stories 작성 (As a..., I want..., So that...)
3. 기술 설계 제안 (Architecture, Technology Choices)
4. 구현 마일스톤 정의
5. 위험 요소 및 완화 전략 문서화

## 제약사항

- plan mode: 계획만 수립, 실행 불가
- 실제 코드 작성 금지
- 파일 수정 금지
- Bash 명령어 실행 불가
```

### .claude/agents/executor.md

```yaml
---
name: "Executor - Code Developer"
description: "계획 기반 구현 (자동 실행)"
model: "claude-opus-4-20250101"
permissionMode: "auto"
tools: ["file_read", "file_create", "file_edit", "bash", "git"]
disallowedTools: ["rm -rf", "dangerous-ops"]
skills: ["vibe-dev", "debug", "testing-strategy", "code-review"]
memory:
  scope: "project"
  retention: "persistent"
hooks:
  PreToolUse: ".claude/hooks/pre-tool-use.ps1"
  PostToolUse: ".claude/hooks/post-tool-use.ps1"
background: "당신은 코드 개발자입니다. 주어진 계획을 구현합니다. TDD를 따릅니다."
---
```

### .claude/agents/verifier.md

```yaml
---
name: "Verifier - Quality Reviewer"
description: "산출물 독립 검증 (읽기 전용)"
model: "claude-opus-4-20250101"
permissionMode: "default"
tools: ["file_read", "code_search", "bash (테스트만)"]
disallowedTools: ["file_create", "file_edit", "git_push"]
skills: ["pr-review", "webapp-testing", "kwcag-a11y"]
memory:
  scope: "project"
  retention: "persistent"
hooks:
  TaskCompleted: ".claude/hooks/verify-task.ps1"
background: "당신은 품질 검증자입니다. 코드와 설계의 품질만 평가합니다. 구현자는 누군지 모릅니다."
---
```

---

**최종 정리**: Ann의 핵심 요구사항인 "구조적 Plan-Execute-Verify 독립성"은 **Agent Teams를 Primary 메커니즘으로 사용**할 때 가장 효과적으로 달성된다. 완전히 다른 인스턴스, 격리된 컨텍스트, 명시적 메시지 기반 통신이 자기평가 편향을 구조적으로 제거한다.

