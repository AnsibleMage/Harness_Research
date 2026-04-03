# 하네스 엘리먼트 통합 리포트 (Consolidated & Deduplicated)
**생성 날짜**: 2026-04-03
**대상**: Report_01~06에서 추출된 CLAUDE.md 미반영 항목 통합 분석

---

## 목차
1. [아키텍처 & 구조 패턴](#아키텍처--구조-패턴)
2. [컨텍스트 & 메모리 관리](#컨텍스트--메모리-관리)
3. [스킬 & 절차 관리](#스킬--절차-관리)
4. [평가 & 품질 제어](#평가--품질-제어)
5. [멀티 클라이언트 & 통합](#멀티-클라이언트--통합)
6. [오케스트레이션 & 워크플로우](#오케스트레이션--워크플로우)
7. [보안 & 접근 제어](#보안--접근-제어)
8. [구성 & 계층화 (Configuration Layering)](#구성--계층화-configuration-layering)
9. [자동화 & 효율성](#자동화--효율성)

---

## 아키텍처 & 구조 패턴

### 1. Planner-Generator-Evaluator (PGE) 3-Agent GAN 루프
**소스**: Report_01 (2026.03 진화 단계), Report_05 (Self-Eval Loop 참고)
**적용성**: 구조 제안 (Hooks/Skills로 구현 필요)
**핵심 원칙**: GAN 스타일 반복으로 self-praise bias 제거 및 task quality 향상.
**설명**: Planner가 작업 분해(JSON) → Generator가 독립적 구현 → Evaluator가 skeptical mode로 비판적 검증. 모든 artifact가 명시적 feedback loop 통해 순환하며 수렴 조건(반복 횟수, quality threshold) 정의.

### 2. Initializer Agent 패턴 (Session Initialization Ceremony)
**소스**: Report_01 (2025.11 기초), Report_06 (CLAUDE.md as Session Initializer)
**적용성**: 구조 제안 (Hooks 단계)
**핵심 원칙**: 첫 세션에서 환경 전체 세팅하여 이후 sessions의 context reset 부담 경감.
**설명**: init.sh, git init, progress.md 초기화, 첫 commit 등 initialization ceremony 수행. CLAUDE.md 자체가 session initializer 메커니즘으로 작동 (모든 session 시작 시 자동 로드).

### 3. App Server 아키텍처 (JSON-RPC 기반 중앙화)
**소스**: Report_02 (2026.02 Codex harness), Report_06 (Multi-Layer Scope System 통해 확장)
**적용성**: 구조 제안 (Infrastructure-level 구현)
**핵심 원칙**: 단일 entry point (App Server)를 통해 여러 클라이언트(CLI, Web, IDE, Desktop)가 동일 harness 로직 공유.
**설명**: JSON-RPC 표준 프로토콜, Thread lifecycle management (session creation → execution → persistence → recovery), Skills registry 중앙화, Stateless client 아키텍처.

### 4. NLAH (Natural-Language Agent Harnesses) 명세 패턴
**소스**: Report_05 (Section 3.5.4)
**적용성**: 구조 제안 (Framework layer)
**핵심 원칙**: Vendor-agnostic YAML 명세로 LangGraph, CrewAI, MetaGPT 등 모든 framework 지원 가능하게 하여 model/vendor switching 비용 최소화.
**설명**: 프레임워크별 구현은 교체 가능하나 명세는 동일 (adapter pattern). 포팅성(portability) 극대화.

### 5. Shared Context Store (멀티 에이전트 협업)
**소스**: Report_02 (Codex harness)
**적용성**: 구조 제안 (Infrastructure-level)
**핵심 원칙**: 여러 agent가 동일한 context data(PR details, test results 등)에 접근하며 write conflict 처리 필요(lock 또는 CRDT).
**설명**: 각 agent는 shared context의 특정 부분을 읽고/쓰기. Multi-agent 환경에서의 상태 일관성 보장 메커니즘.

### 6. 분산 Checkpoint 시스템 (Distributed State Management)
**소스**: Report_05 (Section 3.5.1, Scalable Harness)
**적용성**: 구조 제안 (Infrastructure)
**핵심 원칙**: Redis/DynamoDB 등 distributed checkpoint store로 여러 worker 간 concurrent session 처리 가능.
**설명**: 각 session/agent의 checkpoint를 중앙화된 store에 보관하여 scaling 및 recovery 지원. Multi-tenant 격리도 자동 제공.

---

## 컨텍스트 & 메모리 관리

### 7. 자동 Context Compaction (자동 압축 및 트리거)
**소스**: Report_02 (2026.02 Codex harness), Report_05 (Section 4.3.2, Auto-pruning), Report_06 (Compaction 메커니즘)
**적용성**: 직접 반영 (instructions에 compaction 규칙 + trigger 명시)
**핵심 원칙**: Server-side에서 자동으로 token 초과 감지 시 context 압축하되, core system message와 최근 N개 message는 유지하고 중요도 기반으로 선택적 제거.
**설명**: Compaction trigger (token threshold, task completion 등) 명시적 정의. 각 agent의 context를 독립적으로 압축. Compaction 중에 보존할 항목(수정 파일 목록, 테스트 명령어, 핵심 설계 결정, 현재 TODO 상태) 지정. CLAUDE.md는 `/compact` 후에도 완전히 재로드되어 보존 보장.

### 8. 자동 메모리 시스템 (Auto Memory)
**소스**: Report_06 (Section 3, Auto Memory vs CLAUDE.md 비교)
**적용성**: 구조 제안 (Hooks/Memory system level)
**핵심 원칙**: 사용자 주도 없이 Claude가 프로젝트별 학습(패턴, debugging insights)을 `~/.claude/projects/<project>/memory/MEMORY.md`에 자동 저장 및 session 시작 시 로드.
**설명**: 200줄/25KB 크기의 index (MEMORY.md)를 항상 로드하고, 세부 항목은 `.md` 파일로 분리하여 on-demand 로드 (two-tier architecture). CLAUDE.md와 별개의 지속성 메커니즘.

### 9. Artifact Hand-off 명세 (Cross-session State Transfer)
**소스**: Report_01 (2025.11 기초)
**적용성**: 직접 반영 (artifact spec formal definition)
**핵심 원칙**: 세션 간 상태 전달을 위한 명확한 artifact 포맷 정의로 session 의존성 최소화.
**설명**: Artifact = {파일 목록, 상태 변수, 키 메타데이터}. 각 working directory/project마다 artifact spec 필수. progress.md 확장 형식.

### 10. Context Reuse Strategy (멀티 세션 효율성)
**소스**: Report_01 (section 2.2.4)
**적용성**: 구조 제안 (Context 관리 strategy)
**핵심 원칙**: 여러 session에서 동일 artifact를 공유하여 token 재사용 및 context budgeting.
**설명**: Artifact registry (이전 session 산물)에서 새 session 시작 시 관련 artifacts만 selective loading. 반복 작업의 token cost 절감.

---

## 스킬 & 절차 관리

### 11. Skills as Versioned, Reusable Procedures (버전 관리 & 중앙 레지스트리)
**소스**: Report_02 (2026.02 Codex harness), Report_05 (Skills Library Evolution)
**적용성**: 구조 제안 (Skills registry + versioning infrastructure)
**핵심 원칙**: Natural language instructions + tools 조합을 skill 파일로 정형화하여 Git 버전 관리 및 중앙 레지스트리로 관리하며, 동적 진화(새 skill 자동 추가, 경험 기반 개선) 지원.
**설명**: Skill = {name, instructions, tools, approval_required, version}. `/skills/*.skill` 형식 Git 저장소. Pre-commit hook으로 format validation. Skill evolution: agent experience 기반으로 새로운 skill patterns 자동 발견 및 추가.

### 12. AGENTS.md Pattern (Repository-level Agent Instructions)
**소스**: Report_02 (2026.02 best practices)
**적용성**: 직접 반영 (project-level guidance file)
**핵심 원칙**: Git 저장소 루트에 `.agents.md` 파일로 프로젝트별 agent guidance 제공하며, Git commit으로 변경 이력 추적 및 agent harness 시작 시 항상 로드되는 system context.
**설명**: Durable guidance with version control. Repository-level instructions separate from CLAUDE.md (global). CLAUDE.md 대비 프로젝트 특화 content.

### 13. Skill Format Specification (표준화)
**소스**: Report_02 (2026.02)
**적용성**: 구조 제안 (Skill infrastructure)
**핵심 원칙**: Skill 파일의 표준 형식 정의(instructions, parameters, tools, approval_required)로 각 skill의 독립적 lint/test 및 자동 검증 가능하게 함.
**설명**: YAML 또는 JSON 기반 스펙. Pre-commit/Pre-push hook 자동 검증. Skill reusability 극대화.

---

## 평가 & 품질 제어

### 14. Skeptical Evaluator Mode (비판적 평가 강제)
**소스**: Report_01 (2026.03), Report_05 (Eval Harness with Recursive Improvement)
**적용성**: 직접 반영 (Evaluator prompt template)
**핵심 원칙**: Evaluator agent가 명시적으로 비판적 태도를 취하여 Generator의 과도한 긍정 평가(self-praise bias) 방지하고, 반드시 1개 이상 문제점 도출 강제.
**설명**: Evaluator prompt: "반드시 3개 이상 문제점 찾기". Quality threshold 설정 (점수 < threshold이면 재작업). Generator 제안을 무조건 수용하지 않음. Recursive improvement loop: 0.7 quality threshold까지 자동 개선.

### 15. Eval Harness (메타 평가 시스템)
**소스**: Report_01 (2026.01 개념화, 2026.03 통합), Report_05 (Recursive Improvement Loop)
**적용성**: 구조 제안 (Eval infrastructure + feedback loop)
**핵심 원칙**: 에이전트 자신이 작업 품질을 자동 평가하는 피드백 루프로 task completion quality 향상.
**설명**: Coding → Eval → Improvement 반복. Evaluation result가 Generator에 feedback으로 전달. Evaluation structure: 자동 quality assessment + recursive refinement. 수렴 조건 명시 (반복 횟수, threshold).

### 16. Confidence-Based Auto-Approval Logic
**소스**: Report_05 (Section 4.3.2, Best Practices)
**적용성**: 구조 제안 (Approval gateway mechanism)
**핵심 원칙**: Confidence score 기반으로 approval gates 자동 우회 (≥0.95 auto, 0.85 team_lead, 0.75 director, 이하 human review).
**설명**: 자동 approval 의사결정으로 bottleneck 감소. 신뢰도 기반 escalation path.

### 17. Audit Log & Observability (불변 감사 로그)
**소스**: Report_02 (2026.02), Report_05 (Team Metrics 추적)
**적용성**: 구조 제안 (Audit infrastructure)
**핵심 원칙**: 모든 action(code generation, evaluation, approval, execution)을 append-only 불변 로그에 기록하여 감사 추적성 및 재현성 보장.
**설명**: 각 entry: timestamp, actor, action, result, context snapshot. Team metrics aggregation (sprint goals, completion rates, cycle time, bug density, agent-by-agent scoring). Observability 극대화.

---

## 멀티 클라이언트 & 통합

### 18. Multi-client Architecture (단일 Backend, 다중 클라이언트)
**소스**: Report_02 (2026.02 Codex harness), Report_05 (Scaling considerations)
**적용성**: 구조 제안 (Infrastructure-level)
**핵심 원칙**: 단일 App Server가 모든 클라이언트(CLI, Web, IDE, Desktop)를 JSON-RPC 표준 프로토콜로 지원하며 각 client는 stateless (server-side 상태 추적).
**설명**: Session ID로 server-side 상태 관리. Client는 중간 결과를 실시간으로 display 가능.

### 19. Streaming Progress & Response (실시간 피드백)
**소스**: Report_02 (2026.02), Report_05 (Scalable execution)
**적용성**: 구조 제안 (Client/Server infrastructure)
**핵심 원칙**: 장시간 작업의 진행 상황을 실시간으로 클라이언트에 스트리밍(SSE 또는 WebSocket)하여 사용자 대기 경험 개선.
**설명**: 중간 결과 progressive display. 작업 cancellation 지원 가능.

### 20. IDE Plugin Integration Pattern (VSCode Extension)
**소스**: Report_02 (2026.02), Report_05 (Section 3.6.3, HarnessVSCodeExtension), Report_06 (IDE Integration context)
**적용성**: 구조 제안 (IDE integration infrastructure)
**핵심 원칙**: VSCode 등 IDE에서 harness를 native extension으로 사용하여 inline execution, debugging, quick actions, session/approval 관리를 sidebar에서 수행.
**설명**: JSON-RPC로 App Server와 통신. `.skill` file syntax highlighting. Selected code review, auto-complete 같은 in-editor actions. Extension이 client 역할.

### 21. Git + CI-CD + IDE 통합 워크플로우
**소스**: Report_02 (섹션 3.6), Report_05 (Section 3.6.1-3.6.2), Report_06 (Integrated workflow context)
**적용성**: 구조 제안 (CI/CD pipeline integration)
**핵심 원칙**: Skill 작성 → Git commit → CI/CD validation → Agent review → Human approval → Deploy → Registry auto-update를 자동화하여 skill evolution 가속화.
**설명**: Pre-commit hook: skill format validation. GitHub Actions: lint, test, integration tests. Agent + Human approval before merge. Post-merge: skill auto-deployed to registry, App Server reload triggered. YAML-driven pipeline으로 agent execution on PR, output quality evaluation, PR comment 자동 작성.

---

## 오케스트레이션 & 워크플로우

### 22. Handoff 메커니즘 (State Machine 기반 동적 라우팅)
**소스**: Report_02 (Swarm 기초, Codex에서 고도화), Report_05 (Task delegation patterns)
**적용성**: 구조 제안 (Orchestration engine)
**핵심 원칙**: State + condition → next agent 결정하는 state machine 기반 handoff로 에이전트 간 동적 task 라우팅 및 context 전파.
**설명**:
```
handoff_rules = {
  'initial': {'next_agent': 'developer', 'routine': 'code_review'},
  'code_review_done': {
    'condition': 'has_security_concerns',
    'next_agent': 'security',
    'routine': 'security_audit'
  }
}
```
Stateful handoff: 전 에이전트의 context가 명시적으로 다음 에이전트에 전달. Agent-to-human handoff도 지원 (approval request broadcast, timeout 5분 기본, timeout 시 decline 또는 escalate).

### 23. 계층적 Task Delegation (Manager Agent Pattern)
**소스**: Report_05 (Section 2.3, Manager Agent example)
**적용성**: 구조 제안 (Orchestration pattern)
**핵심 원칙**: Manager agent가 planning output을 구조화된 task list로 파싱(task IDs, descriptions, types, assignment state) 하여 downstream execution 지원.
**설명**: Task structure formal definition으로 distributed execution 가능. Role-based code ownership (Frontend agent → /frontend/**, Backend agent → /backend/** 등) race condition 방지.

### 24. Hybrid Execution Strategy (Complexity-Based Task Routing)
**소스**: Report_05 (Section 4.2.2, Execution diagram)
**적용성**: 구조 제안 (Execution routing logic)
**핵심 원칙**: Task 예상 복잡도에 따라 execution path 결정 (simple → local/Grok Haiku, medium → Grok Standard, complex → Grok Pro + Multi-Agent).
**설명**: Cost-aware skill selection (lightweight vs full-featured). Model selection by complexity estimation + budget constraints (Cost Optimizer 참고).

---

## 보안 & 접근 제어

### 25. Approval Workflow (Explicit Permission Chain)
**소스**: Report_02 (Codex harness core feature), Report_05 (Approval Gateway, multi-level authorization), Report_06 (Governance context)
**적용성**: 구조 제안 (Approval infrastructure)
**핵심 원칙**: 위험한 작업(deploy, delete, financial, architectural changes) 실행 전 명시적 승인 프로세스를 거쳐 human-in-the-loop 보장.
**설명**: Skill에 approval_required flag. Approval request가 모든 active client에 broadcast. Multi-level approval chain: AI evaluation (auto/manual) → Team lead → Director 등 다층 구조. 각 level의 승인 권한 명시적 정의. Escalation path: lower level reject 시 상위 level으로 escalate. Multi-client에서 일관된 승인 UX 필요.

### 26. Filesystem Access Control Policy (화이트리스트/블랙리스트)
**소스**: Report_02 (섹션 3.6.4)
**적용성**: 구조 제안 (Access control infrastructure)
**핵심 원칙**: Agent가 접근 가능한 파일 영역을 명시적으로 화이트리스트/블랙리스트로 정의하여 보안 경계 강제.
**설명**:
- READ_ALLOWED: src/**, *.md, *.json 등 프로젝트 파일
- WRITE_ALLOWED: artifacts/, build/, logs/
- BLOCKED: .git/config, .env, /etc/** 등

### 27. Skill Permission Model (세분화된 접근 제어)
**소스**: Report_02 (2026.02), Report_05 (Permission granularity)
**적용성**: 구조 제안 (Permission infrastructure)
**핵심 원칙**: 각 skill이 수행 가능한 작업의 범위를 명시적으로 정의(read:filesystem, write:artifacts, execute:shell 등)하여 granular control 실현.
**설명**: Skill execution 시 permission check 강제. Role-based code ownership 통해 multi-agent 환경에서 conflict 방지.

### 28. Multi-Tenant Isolation (조직/팀 세션 격리)
**소스**: Report_05 (Section 2.4.4, Persistent Checkpoints)
**적용성**: 구조 제안 (Infrastructure-level)
**핵심 원칙**: 여러 organization/team sessions를 separate checkpoint directories로 격리하고 concurrent access control로 관리.
**설명**: Enterprise scale에서 data isolation 보장. 분산 checkpoint 시스템과 연계.

---

## 구성 & 계층화 (Configuration Layering)

### 29. Multi-Layer Scope System (CLAUDE.md 우선순위 체계)
**소스**: Report_06 (Section 2.1-2.2, Scope hierarchy table)
**적용성**: 직접 반영 (Scope hierarchy documentation)
**핵심 원칙**: CLAUDE.md 로드 우선순위를 명확히 정의하여 중첩된 규칙 상속 및 override semantics 투명화.
**설명**:
Priority 순서: Managed Policy (org) > Project > User (global) > Subdirectory

각 layer는 override 및 확장 가능. Inheritance with clear resolution.

### 30. Managed Policy CLAUDE.md Layer (조직 수준 강제 규칙)
**소스**: Report_06 (Section 2.2, "Managed Policy" row)
**적용성**: 구조 제안 (Organization-level policy enforcement)
**핵심 원칙**: IT/DevOps가 `/etc/claude-code/CLAUDE.md` (Linux) 또는 system paths를 통해 organization-wide 규칙 강제하여 모든 사용자가 우회 불가능하게 함.
**설명**: Non-bypassable governance layer. 보안, 규정 준수 규칙 중앙 관리.

### 31. Path-Specific Rules (경로별 조건부 규칙)
**소스**: Report_06 (Section 6.2, "Path-specific Rules")
**적용성**: 구조 제안 (Rules infrastructure)
**핵심 원칙**: `.claude/rules/` 파일이 YAML frontmatter의 `paths:` glob pattern(e.g., `src/api/**/*.ts`)으로 규칙 적용 범위 한정하여 context-aware rule application 실현.
**설명**: 파일별/디렉토리별 맞춤 규칙. Conditional execution of rules based on file path.

### 32. `.claude/rules/` Directory Partitioning (규칙 분산 관리)
**소스**: Report_06 (Section 6.2)
**적용성**: 직접 반영 (Modular rules organization)
**핵심 원칙**: 큰 규칙 집합을 topic-specific files (code-style.md, testing.md, security.md, frontend/react.md)로 분산하여 on-demand loading으로 session context 오버헤드 감소.
**설명**: `.claude/rules/` directory structure:
- code-style.md
- testing.md
- security.md
- frontend/react.md
- backend/api.md
등등. Rule composability 극대화.

### 33. Import Syntax (`@` 문법)
**소스**: Report_06 (Section 6.1)
**적용성**: 구조 제안 (File composition mechanism)
**핵심 원칙**: CLAUDE.md가 `@path/to/file` 문법으로 외부 파일을 recursive expansion(최대 5 hops)하여 session 시작 시 전개 가능.
**설명**: File-based composition. Optional user approval for expansion. Monorepo 환경에서 규칙 공유 용이.

### 34. HTML Comment Stripping (Token 최적화)
**소스**: Report_06 (Section 6.4)
**적용성**: 구조 제안 (Session-level optimization)
**핵심 원칙**: Block-level HTML comments (`<!-- -->`)를 context 주입 전 제거하여 maintenance notes token cost 제거.
**설명**: 주석은 git에 보존되나 session에서만 제거. 유용한 optimization technique.

### 35. `claudeMdExcludes` Configuration (Monorepo 필터링)
**소스**: Report_06 (Section 6.3)
**적용성**: 구조 제안 (Configuration mechanism)
**핵심 원칙**: `.claude/settings.local.json`의 `claudeMdExcludes` glob pattern으로 monorepo 환경에서 다른 팀의 CLAUDE.md 로드 제외.
**설명**: Scope filtering for multi-team environments. 팀 간 규칙 간섭 방지.

### 36. User-Level Path-Specific Rules (`~/.claude/rules/`)
**소스**: Report_06 (Section 6.2, "User-level Rules")
**적용성**: 직접 반영 (User-global rules management)
**핵심 원칙**: `~/.claude/rules/` 파일들이 모든 프로젝트에 적용되되 project-level rules가 override하도록 하여 사용자 전역 규칙 + 프로젝트 특화 규칙 계층화.
**설명**: Layered inheritance: User-global > Project-specific. Symlink-based rule sharing으로 조직 전체에서 shared security/quality rules 단일 소스로 관리 가능.

---

## 자동화 & 효율성

### 37. Cost Monitoring & Control (비용 예산 관리)
**소스**: Report_01 (section 2.4.3, enterprise scale), Report_05 (Cost Optimizer), Report_06 (Enterprise context)
**적용성**: 직접 반영 (Cost awareness guidelines)
**핵심 원칙**: Per-session, per-agent token 예산 설정 및 cost-aware skill selection(lightweight vs full-featured)으로 API cost 폭발 제어.
**설명**: Cost estimation at task planning phase. Model selection by cost-complexity trade-off. Budget enforcement 및 alert mechanism. Enterprise scale에서 필수.

### 38. Selective Compaction (중요도 기반 압축)
**소스**: Report_02 (2026.02), Report_05 (Section 4.3.2)
**적용성**: 구조 제안 (Compaction strategy)
**핵심 원칙**: Context 압축 시 중요도에 따라 선택적 제거 (core system message 항상 유지, 최근 N개 message 유지, 오래된 diagnostic info 제거).
**설명**: Importance scoring for context items. Selective preservation criteria. 항상 CLAUDE.md는 재로드로 보존 보장.

### 39. 4-Step Best Practice Workflow (Explore→Plan→Implement→Commit)
**소스**: Report_06 (Section 7.1.2), Report_02 (Vibe Coding 기초)
**적용성**: 직접 반영 (Workflow methodology)
**핵심 원칙**: 구조화된 4단계 워크플로우로 task 실행의 일관성 및 재현성 보장.
**설명**:
1. **Explore**: Plan Mode에서 코드 읽기, 요구사항 파악, 변경 금지
2. **Plan**: 상세 구현 전략, 아키텍처/설계 결정 작성
3. **Implement**: Normal Mode에서 코드 작성, 테스트 실행, 수정
4. **Commit**: 커밋 메시지, PR 생성, 문서화

Current CLAUDE.md의 "바이브코딩 4단계"와 매칭.

### 40. Context Management Commands 명문화 (`/clear`, `/compact`, `/rewind`, `/btw`)
**소스**: Report_06 (Section 7.1.3)
**적용성**: 직접 반영 (Command documentation)
**핵심 원칙**: Session control command들의 목적과 사용 패턴을 명시적으로 문서화하여 context 최적화 실천 가능하게 함.
**설명**:
- `/clear`: 무관한 작업 간 context reset
- `/compact <instructions>`: 선택적 보존하며 압축
- `/rewind`: 특정 시점으로 point-in-time rollback
- `/btw`: 비 기록 질문 (archive 생략)

각 command의 사용 가이드라인.

### 41. Compaction Instruction Preservation (상태 보존 명시)
**소스**: Report_06 (Section 7.1.3, Example)
**적용성**: 직접 반영 (Compaction rules)
**핵심 원칙**: CLAUDE.md에서 `/compact` 작업 중 반드시 보존할 항목을 명시적으로 선언하여 critical state 손실 방지.
**설명**: Preservation criteria specification. Example: "When compacting, always preserve the full list of modified files, test commands, key design decisions, current TODO status".

### 42. 200-Line Limit & Compliance Penalty (규모 제약 및 준수)
**소스**: Report_06 (Section 4.1)
**적용성**: 직접 반영 (Length constraint guideline)
**핵심 원칙**: CLAUDE.md >200줄 시 compliance 저하 경고로 파일 bloat 방지 ("Bloated CLAUDE.md files cause Claude to ignore your actual instructions!").
**설명**: Performance impact (compliance degradation). 필요시 `.claude/rules/` 분산 권장. 현재 GLOBAL_CLAUDE_MD_DRAFT는 142줄로 양호.

### 43. Specificity Verification Pattern (구체성 검증)
**소스**: Report_06 (Section 4.3)
**적용성**: 직접 반영 (Quality principle)
**핵심 원칙**: 규칙은 검증 가능해야 함. 추상적 표현 금지, 구체적 예시 필수.
**설명**:
- Bad: "Format code properly"
- Good: "Use 2-space indentation, kebab-case filenames, camelCase functions"

Instructions clarity & verifiability 강화.

### 44. Subagent Delegation Pattern (병렬 조사)
**소스**: Report_06 (Section 7.1.4), Report_01 (Subagent 개념)
**적용성**: 직접 반영 (Delegation guidelines)
**핵심 원칙**: 서브시스템 조사를 subagent에 위임하여 메인 context 보호 및 병렬 진행 가속화.
**설명**: Subagent delegation pattern: "use a subagent to review this code for edge cases". 독립적 context window에서 parallel investigation. 메인 session의 token budget 보호.

### 45. CLAUDE.md as Code Practice (코드처럼 관리)
**소스**: Report_06 (Section 4.6)
**적용성**: 직접 반영 (Maintenance discipline)
**핵심 원칙**: CLAUDE.md를 code처럼 취급하여 Git commit, behavior change test, dead rule pruning 정기적으로 실행.
**설명**: Version control에 포함. 규칙 변경 후 behavior 실제 변화 검증. 구식화된 규칙 정기적 제거. CLAUDE.md evolution tracking.

### 46. IMPORTANCE & YOU MUST 강조 원칙
**소스**: Report_06 (Section 4.5)
**적용성**: 직접 반영 (Communication technique)
**핵심 원칙**: "IMPORTANT" 또는 "YOU MUST" 마커 사용으로 adherence 증대하나 과다 사용 시 효력 저하. 진정 중요한 규칙에만 예약.
**설명**: Emphasis marker strategy. Overuse dilution 주의. Selective application으로 효과 극대화.

### 47. Failure Antipatterns Documentation (실패 패턴 문서화)
**소스**: Report_06 (Section 7.1.5, Antipatterns table)
**적용성**: 직접 반영 (Negative examples)
**핵심 원칙**: 알려진 실패 mode(kitchen sink session, bloated CLAUDE.md, verification 없이 신뢰 등) 명시적으로 문서화하여 회피 가능하게 함.
**설명**: Antipattern examples:
- Kitchen sink: 무관한 여러 작업을 한 session에서 처리 → context 오염
- Oversized CLAUDE.md: 200줄 초과 → compliance 저하
- No verification: 검증 없이 output 신뢰 → quality risk

Anti-patterns awareness 높이기.

### 48. Content Inclusion Checklist (포함/제외 경계)
**소스**: Report_06 (Section 5, Two tables: "Include" ✅, "Exclude" ❌)
**적용성**: 직접 반영 (Content boundary specification)
**핵심 원칙**: CLAUDE.md에 포함할 항목(bash commands, non-default code styles, architecture decisions)과 제외할 항목(code-readable conventions, standard docs) 구조적으로 정의.
**설명**:
**Include** ✅:
- Project-specific bash commands
- Non-default code formatting rules
- Architecture/design decisions
- Custom tool usage patterns

**Exclude** ❌:
- Standard documentation (README는 프로젝트에)
- Universal coding conventions
- Code-readable comments
- Framework documentation

### 49. Advisory vs. Hooks Distinction (권고 vs. 강제)
**소스**: Report_06 (Section 1.2 & 1.3)
**적용성**: 직접 반영 (Enforcement model clarification)
**핵심 원칙**: CLAUDE.md는 context(advisory, losable)이지 config이 아님. 강제 필요 시 Hooks(deterministic execution) 또는 Permissions(settings.json) 사용.
**설명**:
- **CLAUDE.md**: Advisory guidelines (context)
- **Hooks**: Deterministic enforcement (execution phase)
- **Permissions**: settings.json access control (configuration)

3-tier enforcement model 이해 필수.

---

## 통합 매트릭스

| 엘리먼트 | 소스 | 카테고리 | 적용성 | 우선순위 |
|---------|------|---------|--------|---------|
| PGE 3-Agent GAN Loop | R01,R05 | Architecture | 구조 제안 | 높음 |
| Initializer Agent | R01,R06 | Architecture | 구조 제안 | 높음 |
| App Server (JSON-RPC) | R02,R06 | Architecture | 구조 제안 | 중간 |
| NLAH Specification | R05 | Architecture | 구조 제안 | 중간 |
| Shared Context Store | R02 | Architecture | 구조 제안 | 중간 |
| Distributed Checkpoints | R05 | Architecture | 구조 제안 | 중간 |
| Auto Context Compaction | R02,R05,R06 | Context Mgmt | 직접 반영 | 높음 |
| Auto Memory System | R06 | Context Mgmt | 구조 제안 | 중간 |
| Artifact Hand-off Spec | R01 | Context Mgmt | 직접 반영 | 높음 |
| Context Reuse Strategy | R01 | Context Mgmt | 구조 제안 | 낮음 |
| Skills Versioning | R02,R05 | Skills Mgmt | 구조 제안 | 중간 |
| AGENTS.md Pattern | R02 | Skills Mgmt | 직접 반영 | 높음 |
| Skill Format Spec | R02 | Skills Mgmt | 구조 제안 | 중간 |
| Skeptical Evaluator | R01,R05 | Evaluation | 직접 반영 | 높음 |
| Eval Harness | R01,R05 | Evaluation | 구조 제안 | 높음 |
| Confidence-Based Auto-Approval | R05 | Evaluation | 구조 제안 | 중간 |
| Audit Log & Observability | R02,R05 | Evaluation | 구조 제안 | 중간 |
| Multi-client Architecture | R02,R05 | Multi-Client | 구조 제안 | 중간 |
| Streaming Progress | R02,R05 | Multi-Client | 구조 제안 | 낮음 |
| IDE Plugin (VSCode) | R02,R05,R06 | Multi-Client | 구조 제안 | 중간 |
| Git+CI-CD+IDE Workflow | R02,R05,R06 | Multi-Client | 구조 제안 | 중간 |
| Handoff State Machine | R02,R05 | Orchestration | 구조 제안 | 높음 |
| Hierarchical Task Delegation | R05 | Orchestration | 구조 제안 | 중간 |
| Hybrid Execution Strategy | R05 | Orchestration | 구조 제안 | 중간 |
| Approval Workflow | R02,R05,R06 | Security | 구조 제안 | 높음 |
| Filesystem Access Control | R02 | Security | 구조 제안 | 중간 |
| Skill Permission Model | R02,R05 | Security | 구조 제안 | 중간 |
| Multi-Tenant Isolation | R05 | Security | 구조 제안 | 중간 |
| Multi-Layer Scope System | R06 | Configuration | 직접 반영 | 높음 |
| Managed Policy Layer | R06 | Configuration | 구조 제안 | 낮음 |
| Path-Specific Rules (YAML) | R06 | Configuration | 구조 제안 | 높음 |
| `.claude/rules/` Partitioning | R06 | Configuration | 직접 반영 | 높음 |
| Import Syntax (`@`) | R06 | Configuration | 구조 제안 | 중간 |
| HTML Comment Stripping | R06 | Configuration | 구조 제안 | 낮음 |
| `claudeMdExcludes` Config | R06 | Configuration | 구조 제안 | 낮음 |
| User-Level Rules | R06 | Configuration | 직접 반영 | 중간 |
| Symlink Rule Sharing | R06 | Configuration | 직접 반영 | 중간 |
| Cost Monitoring & Control | R01,R05,R06 | Automation | 직접 반영 | 중간 |
| Selective Compaction | R02,R05 | Automation | 구조 제안 | 중간 |
| 4-Step Workflow | R06,R02 | Automation | 직접 반영 | 높음 |
| Context Commands (`/clear` etc.) | R06 | Automation | 직접 반영 | 높음 |
| Compaction Preservation | R06 | Automation | 직접 반영 | 높음 |
| IMPORTANCE Principle | R06 | Automation | 직접 반영 | 낮음 |
| CLAUDE.md as Code | R06 | Automation | 직접 반영 | 중간 |
| Specificity Verification | R06 | Automation | 직접 반영 | 중간 |
| Subagent Delegation | R06,R01 | Automation | 직접 반영 | 중간 |
| Failure Antipatterns | R06 | Automation | 직접 반영 | 낮음 |
| Content Inclusion Checklist | R06 | Automation | 직접 반영 | 중간 |
| Advisory vs. Hooks | R06 | Automation | 직접 반영 | 높음 |
| 200-Line Limit & Penalty | R06 | Automation | 직접 반영 | 낮음 |

---

## 반영 우선순위 (Priority Matrix)

### 긴급 (Immediate - 다음 버전)
직접 반영 가능 + 높은 가치:
1. **Auto Context Compaction** — 장시간 session 필수
2. **Skeptical Evaluator Mode** — Quality control 강화
3. **Eval Harness** — Self-evaluation loop 구조화
4. **Handoff State Machine** — Multi-agent coordination
5. **Approval Workflow** — Security & governance
6. **AGENTS.md Pattern** — Project-level guidance
7. **Artifact Hand-off Spec** — Cross-session continuity
8. **Multi-Layer Scope System** — Configuration clarity
9. **Path-Specific Rules** — Context-aware rules
10. **Advisory vs. Hooks Distinction** — Enforcement model clarity

### 높음 (High - 1-2주 내)
직접 반영 가능:
- Context Commands Documentation
- Compaction Preservation
- 4-Step Workflow (현재 유사하나 명확화)
- `.claude/rules/` Partitioning
- Cost Monitoring & Control
- Specificity Verification Pattern
- Subagent Delegation
- Content Inclusion Checklist
- User-Level Rules
- CLAUDE.md as Code Practice

### 중간 (Medium - 구조 설계 필요)
구조 제안 (기술 설계 필요):
- PGE 3-Agent Loop
- Initializer Agent
- Eval Harness Detailed Implementation
- Distributed Checkpoints
- Skills Versioning & Registry
- Multi-client Architecture
- IDE Plugin Pattern
- Git+CI-CD+IDE Workflow
- Skill Permission Model
- Cost Optimizer

### 낮음 (Low - 선택적)
- Streaming Progress
- HTML Comment Stripping
- 200-Line Limit (이미 충족)
- IMPORTANCE Principle
- Failure Antipatterns
- Managed Policy Layer (enterprise-only)
- `claudeMdExcludes` (monorepo-only)
- Context Reuse Strategy

---

## 종합 분석

### 중복 제거 결과
원본 60+ 항목 → **통합 49개 엘리먼트**

**주요 중복 제거 사례**:
1. "Eval Harness" + "Self-evaluation loop" + "Recursive Improvement" → **단일 Eval Harness 정의**
2. "Approval Workflow" + "Approval Gateway" + "Multi-level Approval" → **통합 Approval Workflow**
3. "Handoff" + "Agent-to-Agent routing" + "State Machine" → **단일 Handoff State Machine**
4. "Context Compaction" 여러 언급 → **통합 Auto Context Compaction**
5. "CLAUDE.md scope" + "Managed Policy" + "User Rules" + "Path-Specific" → **Multi-Layer Scope System**

### CLAUDE.md 반영 가능도
- **직접 반영 (직접 지침 작성)**: 20개 항목 (40%)
- **구조 제안 (Hooks/Infrastructure 설계 필요)**: 29개 항목 (60%)

### 다음 액션
1. **v1.1 (Immediate)**: 10개 긴급 항목 → CLAUDE.md 직접 반영
2. **v1.2 (High)**: 10개 높음 항목 + 기술 설계
3. **v2.0 (Medium)**: Infrastructure layer (App Server, Distributed Checkpoints 등) 기본 설계
4. **Enterprise (Low)**: 조직 규모 확대 시 선택적 구현

---

**생성**: 2026-04-03 | **대상**: Ann의 CLAUDE.md 진화 버전 설계
