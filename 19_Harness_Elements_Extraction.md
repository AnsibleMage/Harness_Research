# 하네스 엘리먼트 추출 리포트
**대상 파일**: 07_Report_anthropic_harness_analysis.md, 08_Report_openai_codex_harness_analysis.md
**날짜**: 2026-04-03

---

## 1. 추출된 하네스 엘리먼트 (미반영 항목)

### A. 아키텍처 패턴 & 구조

#### A.1 3-Agent GAN 스타일 구조
- **보고서**: Report_01 (2026.03 진화 단계)
- **역할**: Planner + Generator + Evaluator의 병렬-반복 루프로 self-praise bias 제거 및 context reset 최소화
- **현재 CLAUDE.md 반영 여부**: 아니오 (Subagent 개념만 있음, 3-agent orchestration 부재)
- **구조적 제약**:
  - Planner가 작업 분해 → Generator는 독립적 구현 → Evaluator가 skeptical mode로 검증
  - 모든 artifact가 명시적 feedback loop을 통해 순환

#### A.2 Initializer Agent 패턴
- **보고서**: Report_01 (2025.11 기초 하네스)
- **역할**: 첫 세션에서 환경 전체 세팅 (init.sh, git init, progress.md 초기화, 첫 commit)
- **현재 CLAUDE.md 반영 여부**: 아니오 (Session 관리만 있음, initialization ceremony 부재)
- **구조적 제약**:
  - 이후 세션이 이 initialization을 가정하고 context reset 부담 경감
  - Artifact hand-off 메커니즘의 기초

#### A.3 Eval Harness (메타 평가 시스템)
- **보고서**: Report_01 (2026.01 개념화, 2026.03 통합)
- **역할**: 에이전트 자신이 작업 품질을 자동 평가하는 피드백 루프
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Skeptical evaluator로 명시적으로 비판적 태도 강제 (1개 이상 문제점 도출)
  - Generator와 Evaluator 완전 분리로 self-praise bias 제거

#### A.4 Codex Harness App Server 아키텍처
- **보고서**: Report_02 (2026.02 완성 설계)
- **역할**: JSON-RPC 기반의 백엔드로 여러 클라이언트(CLI, Web, IDE, Desktop)가 동일 harness 공유
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - 단일 entry point (App Server) → 모든 클라이언트가 동일 orchestration 로직 사용
  - Thread lifecycle management로 상태 persistence
  - Skills registry로 procedure 중앙화

#### A.5 Handoff 메커니즘
- **보고서**: Report_02 (Swarm 기초, Codex에서 고도화)
- **역할**: 에이전트 간 동적 task 라우팅 및 context 전파
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Stateful handoff: 전전 에이전트의 context가 다음 에이전트에 명시적으로 전달
  - Handoff rule을 state machine으로 정의 (현재 상태 + 조건 → 다음 에이전트)

#### A.6 Approval Workflow (Explicit Permission 체인)
- **보고서**: Report_02 (Codex harness의 core feature)
- **역할**: 위험한 작업(deploy, delete) 실행 전 명시적 승인 프로세스
- **현재 CLAUDE.md 반영 여부**: 아니오 (보안 규칙에는 있으나 orchestration level 부재)
- **구조적 제약**:
  - Skill이 approval_required flag를 가짐
  - Approval request가 모든 active client에 broadcast
  - Multi-client에서 일관된 승인 UX 필요

---

### B. Context & Memory 관리

#### B.1 Automatic Context Compaction
- **보고서**: Report_02 (2026.02 Codex harness)
- **역할**: Server-side에서 자동으로 context 압축하여 long-running session 지원
- **현재 CLAUDE.md 반영 여부**: 부분 (Compaction 보존 규칙은 있으나 자동화 메커니즘 부재)
- **구조적 제약**:
  - 각 agent의 context를 독립적으로 압축 (multi-agent 환경에서 중요)
  - Compaction trigger를 명시적으로 정의 (token threshold, task completion 등)

#### B.2 Artifact Hand-off 스펙 정의
- **보고서**: Report_01 (2025.11 기초)
- **역할**: 세션 간 상태 전달을 위한 명확한 artifact 포맷 정의
- **현재 CLAUDE.md 반영 여부**: 아니오 (progress.md는 있으나 artifact spec 정의 부재)
- **구조적 제약**:
  - Artifact는 파일 목록 + 상태 변수 + 키 메타데이터로 구성
  - 각 working directory/project마다 artifact spec이 필수

#### B.3 Thread Lifecycle Management
- **보고서**: Report_02 (Codex harness)
- **역할**: 각 agent/session의 생명주기를 명시적으로 관리하여 상태 보존
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Session creation → execution → state persistence → session recovery
  - Recovery path: 이전 session의 마지막 thread state로부터 재개

#### B.4 Shared Context Store (Multi-agent)
- **보고서**: Report_02 (Codex harness)
- **역할**: 여러 agent가 동일한 context data(예: PR details, test results)에 접근
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - 각 agent는 shared context의 특정 부분을 읽고/쓰기
  - Write conflict 처리 필요 (lock 또는 CRDT)

---

### C. Skill & Procedure 관리

#### C.1 Skills as Versioned, Reusable Procedures
- **보고서**: Report_02 (2026.02 Codex harness)
- **역할**: Natural language instructions + tools의 조합을 skill 파일로 정형화하여 재사용 가능
- **현재 CLAUDE.md 반영 여부**: 부분 (Skills 활용 섹션 있으나 versioning/registry 부재)
- **구조적 제약**:
  - Skill = {name, instructions, tools, approval_required, version}
  - Git 저장소에 `/skills/*.skill` 형식으로 버전 관리
  - Skill registry에 중앙화 (App Server가 제공)

#### C.2 AGENTS.md (Repository-level Agent Instructions)
- **보고서**: Report_02 (2026.02 best practices)
- **역할**: Git 저장소 루트에 위치하는 프로젝트별 agent guidance
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - `.agents.md` 파일로 durable guidance 제공
  - Git commit으로 변경 이력 추적
  - Agent harness 시작 시 항상 로드되는 system context

#### C.3 Skill Format Specification
- **보고서**: Report_02 (2026.02)
- **역할**: Skill 파일의 표준 형식 (instructions, parameters, tools, approval_required)
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - YAML 또는 JSON 기반 스펙
  - 각 skill은 독립적으로 lint/test 가능
  - Pre-commit/Pre-push hook으로 자동 검증

---

### D. Evaluation & Quality Control

#### D.1 Skeptical Evaluator Mode
- **보고서**: Report_01 (2026.03)
- **역할**: Evaluator agent가 명시적으로 비판적 태도를 취하여 Generator의 과도한 긍정 평가 방지
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Evaluator prompt: "반드시 3개 이상 문제점 찾기" 강제
  - Quality threshold: 점수 < threshold이면 재작업 권장
  - Generator의 제안을 무조건 수용하지 않음

#### D.2 Self-evaluation with Feedback Loop
- **보고서**: Report_01 (2026.01-03)
- **역할**: Agent가 자신의 작업을 평가하고 그 결과를 다음 iteration에 반영
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Coding → Eval → Improvement의 반복 루프
  - Evaluation result가 Generator에 feedback으로 전달
  - 수렴 조건 정의 필요 (반복 횟수, quality threshold)

#### D.3 Multi-level Approval Chain (Hierarchical)
- **보고서**: Report_02 (Team/Enterprise scale)
- **역할**: AI 평가 → Team lead → Director 등 다층 승인
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - 각 레벨의 승인 권한 명시적 정의
  - Escalation path: lower level에서 reject되면 상위 레벨으로 올림

#### D.4 Audit Log & Observability
- **보고서**: Report_02 (2026.02)
- **역할**: 모든 action(code generation, evaluation, approval, execution)을 기록
- **현재 CLAUDE.md 반영 여부**: 부분 (Git으로 추적은 있으나 audit log structure 부재)
- **구조적 제약**:
  - Immutable audit log (append-only)
  - 각 entry: timestamp, actor, action, result, context snapshot
  - 감사 추적성 및 재현성 보장

---

### E. Multi-client & Integration 패턴

#### E.1 Multi-client Architecture (Single Backend)
- **보고서**: Report_02 (2026.02 Codex harness)
- **역할**: 단일 App Server가 모든 클라이언트(CLI, Web, IDE, Desktop)를 지원
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - JSON-RPC 표준 프로토콜
  - Client는 state를 유지하지 않음 (stateless)
  - Session ID로 server side 상태 추적

#### E.2 Streaming Progress & Response
- **보고서**: Report_02 (2026.02)
- **역할**: 장시간 작업의 진행 상황을 실시간으로 클라이언트에 스트리밍
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Server-sent events (SSE) 또는 WebSocket으로 구현
  - 클라이언트는 중간 결과를 보며 대기 (UX 개선)

#### E.3 IDE Plugin Integration Pattern
- **보고서**: Report_02 (2026.02)
- **역할**: VSCode 등 IDE에서 harness를 native extension으로 사용
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Extension이 JSON-RPC로 App Server와 통신
  - Syntax highlighting for .skill files
  - Inline execution, debugging, quick actions
  - Sidebar에서 session/approval 관리

#### E.4 Git + CI-CD + IDE 통합 워크플로우
- **보고서**: Report_02 (섹션 3.6)
- **역할**: Skill 작성 → Git commit → CI/CD validation → Agent review → Human approval → Deploy
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Pre-commit hook: skill format validation
  - GitHub Actions: lint, test, integration tests
  - Agent + Human approval before merge
  - Post-merge: skill automatically deployed to registry
  - App Server reload triggered

---

### F. Orchestration & Workflow Patterns

#### F.1 Planner-Generator-Evaluator (PGE) Loop
- **보고서**: Report_01 (2026.03)
- **역할**: GAN 스타일의 반복 개선으로 task completion quality 향상
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Planner: feature request → task decomposition (JSON)
  - Generator: task → implementation (versioned artifact)
  - Evaluator: artifact → quality report (필수 1개 이상 issue)
  - Feedback loop: Evaluator issues → Generator refinement

#### F.2 Handoff State Machine
- **보고서**: Report_02 (Codex harness)
- **역할**: 상태 + 조건 → 다음 agent 결정
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  ```
  handoff_rules = {
    'initial': {'next_agent': 'developer', 'routine': 'code_review'},
    'code_review_done': {
      'condition': 'has_security_concerns',
      'next_agent': 'security',
      'routine': 'security_audit'
    },
    ...
  }
  ```

#### F.3 Agent-to-Human Handoff
- **보고서**: Report_02 (Codex harness)
- **역할**: Agent가 최종 결정을 사람에게 위임
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Approval request broadcast to all active clients
  - Timeout 설정 (기본 5분)
  - Timeout 시 decline 또는 escalate

---

### G. 보안 & 접근 제어

#### G.1 Filesystem Access Control Policy
- **보고서**: Report_02 (섹션 3.6.4)
- **역할**: Agent가 접근 가능한 파일 영역을 명시적으로 화이트리스트/블랙리스트
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - READ_ALLOWED: 프로젝트 파일(src, md, json)
  - WRITE_ALLOWED: artifacts, build, logs
  - BLOCKED: .git/config, .env, /etc/**

#### G.2 Skill Permission Model
- **보고서**: Report_02 (2026.02)
- **역할**: 각 skill이 수행 가능한 작업의 범위를 명시적으로 정의
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Skill: {permissions: ['read:filesystem', 'write:artifacts', 'execute:shell']}
  - Skill execution 시 permission check

#### G.3 Role-based Code Ownership (Multi-agent)
- **보고서**: Report_01/02 (팀 협업 섹션)
- **역할**: 각 agent가 특정 파일/디렉토리만 담당 (race condition 방지)
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Frontend agent → /frontend/** only
  - Backend agent → /backend/** only
  - DevOps agent → /infra/** only

---

### H. 비용 & 효율성 관리

#### H.1 Context Reuse Strategy (Multi-session)
- **보고서**: Report_01 (section 2.2.4)
- **역할**: 여러 session에서 동일 artifact를 공유하여 token 재사용
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Artifact registry: 이전 session에서 생성된 파일들
  - 새 session이 시작될 때 relevant artifacts만 loading
  - Context budgeting

#### H.2 Selective Compaction (by Importance)
- **보고서**: Report_02 (2026.02)
- **역할**: 중요도에 따라 context를 선택적으로 압축
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Core system message는 항상 유지
  - 최근 N개 message는 유지
  - 오래된 diagnostic/debug info 제거

#### H.3 Cost Monitoring & Control
- **보고서**: Report_01 (section 2.4.3, enterprise scale)
- **역할**: 조직 규모에서 API cost 폭발을 제어
- **현재 CLAUDE.md 반영 여부**: 아니오
- **구조적 제약**:
  - Per-session, per-agent token 예산
  - Cost-aware skill selection (lightweight vs full-featured)

---

## 2. 현재 CLAUDE.md와 비교 요약

### 현재 CLAUDE.md에 있는 항목
✓ PARALLEL-FIRST 원칙
✓ CLEAR Framework
✓ Thinking Process (5단계)
✓ 바이브코딩 4단계
✓ 복잡도별 접근
✓ 작업 관리 규칙
✓ Subagent 활용 (제한적)
✓ Skills 활용 (제한적)
✓ 세션 관리
✓ Compaction 보존 규칙 (제한적)
✓ 세션 간 상태 전달 (progress.md)
✓ 검증 우선
✓ 공통 코딩 표준
✓ Git 워크플로우
✓ 응답 규칙
✓ 보안 규칙 (일반)

### 추가 필요한 항목 (미반영)
1. **3-Agent GAN 구조** (Planner-Generator-Evaluator 명시적 정의)
2. **Initializer Agent 패턴** (initialization ceremony)
3. **Eval Harness** (메타 평가, self-evaluation loop)
4. **Codex Harness App Server 아키텍처** (JSON-RPC, multi-client)
5. **Handoff 메커니즘** (state machine, agent-to-agent routing)
6. **Approval Workflow** (orchestration level)
7. **Automatic Context Compaction** (trigger, strategy)
8. **Artifact Hand-off 스펙** (formal definition)
9. **Thread Lifecycle Management** (persistence, recovery)
10. **Shared Context Store** (multi-agent coordination)
11. **Skills Versioning & Registry** (중앙화 관리)
12. **AGENTS.md Pattern** (repository-level guidance)
13. **Skill Format Spec** (standardization)
14. **Skeptical Evaluator Mode** (explicit bias prevention)
15. **Multi-level Approval Chain** (hierarchical)
16. **Audit Log Structure** (immutable, traceable)
17. **Multi-client Architecture** (JSON-RPC protocol)
18. **Streaming Progress** (real-time feedback)
19. **IDE Plugin Integration** (VSCode extension pattern)
20. **Git + CI-CD + IDE 워크플로우** (integrated pipeline)
21. **PGE Loop 명시** (iterative improvement)
22. **Handoff State Machine** (formal definition)
23. **Agent-to-Human Handoff** (timeout, escalation)
24. **Filesystem Access Control** (whitelist/blacklist)
25. **Skill Permission Model** (granular control)
26. **Role-based Code Ownership** (multi-agent safety)
27. **Context Reuse Strategy** (multi-session efficiency)
28. **Selective Compaction** (importance-based)
29. **Cost Monitoring & Control** (budget management)

---

## 3. 우선순위 분류

### 긴급 (Immediate - 다음 버전에 추가)
- 3-Agent GAN 구조 정의
- Eval Harness (self-evaluation loop)
- Initializer Agent 패턴
- AGENTS.md Pattern
- Handoff 메커니즘

### 중요 (High - 1-2주 내)
- Approval Workflow (orchestration level)
- Automatic Context Compaction (trigger strategy)
- Artifact Hand-off 스펙 정의
- Skeptical Evaluator Mode
- Audit Log 구조
- PGE Loop 명시

### 중장기 (Medium - 팀/엔터프라이즈 확장 시)
- Codex Harness App Server 아키텍처
- Multi-client Architecture
- IDE Plugin Integration Pattern
- Skill Versioning & Registry
- Thread Lifecycle Management
- Multi-level Approval Chain
- Role-based Code Ownership
- Streaming Progress

### 선택적 (Low - 조직 규모에 따라)
- Filesystem Access Control Policy
- Cost Monitoring & Control
- Context Reuse Strategy
- Selective Compaction

---

## 4. 추가 정보: 두 보고서의 차별점

### Report_01 (Anthropic)
- **초점**: 개인 로컬 AI 에이전트 → 팀 협업 → 엔터프라이즈
- **핵심 진화**: context reset 최소화, self-praise bias 제거
- **기술**: Initializer, Progress Log, Eval Harness, 3-Agent GAN
- **한계**: 구체적 구현 예제 부족 (pseudocode만 제시)

### Report_02 (OpenAI)
- **초점**: 실전 프로덕션 하네스 (Codex)
- **핵심 진화**: stateless → stateful, lightweight → production-grade
- **기술**: App Server, Skills, AGENTS.md, Handoff, Multi-client
- **강점**: 구체적 구현, 실제 코드 예제, 통합 워크플로우
- **한계**: 초기 학습 곡선이 높을 수 있음

### 시너지
- Report_01의 "구조적 패턴" + Report_02의 "실전 구현" = 완성된 하네스 엔지니어링
