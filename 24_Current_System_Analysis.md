# 현재 Claude Code 시스템 분석 보고서

> 분석 대상: ~/.claude/ (V5.2.0-WE) | 분석일: 2026-04-06
> 기준: Harness Research 49개 엘리먼트 (01~23 문서)
> 체인: ResearchChain HIGH
> 분석 프레임워크: 5차원 분석 + 5+ Why 체인 + 5 관점 분석 + 3회 반복적 정제 + What-If & HMW

---

## 1. Executive Summary

### 종합 점수: 72/100

**한 줄 진단**: 핵심 기능(오케스트레이션, 메모리, 품질 평가)은 업계 권장사항의 70~85%를 달성한 "고급 사용자 수준의 성숙한 하네스"이나, 인프라 레벨 기능과 Enforcement 메커니즘에서 구조적 한계를 보인다.

**핵심 발견 3개**:

1. **Advisory vs Enforcement 간극**: 시스템의 규칙 대부분이 문서 기반(Advisory)이며, Hook 기반 코드 강제(Enforcement)는 3개에 불과하다. 규칙이 스킵되어도 즉각적 오류가 없어 "잘 작동한다"고 오인하는 구조적 문제가 존재한다.

2. **메모리 시스템의 이중성**: 1P=1M 규칙으로 439개 메모리를 축적한 것은 "기록 시스템"으로서 완벽하나, "기억 시스템"으로서는 실패하고 있다. 최근 10개 시간순 리콜만 존재하여 95%의 메모리가 사실상 미활용 상태다.

3. **복잡도 임계점 접근**: 10개 Chain + 31개 Agent + 47개 Skill + 439개 Memory의 조합 가능성이 천문학적이며, V5.1.1에서 "템플릿 Read 절차 스킵 문제"가 발생한 것이 복잡도 임계점 접근의 실증이다.

---

## 2. 시스템 인벤토리 요약

| 구성 요소 | 수량 | 세부 사항 |
|----------|------|----------|
| CLAUDE.md | ~90줄 | V5.0.0 C3 모듈화 결과 (486줄에서 81% 감량) |
| Agents | 31개 | Cognitive 10, Role 4, Review 3, Eval 3, Vault 3, 기타 8 |
| Skills | 47개 | 1,967개 파일, YAML frontmatter 기반 |
| Chains | 10개 | A~H, J~K (I 없음), 3단계 Effort Level |
| Rules | 4파일 | orchestration, memory-protocol, template-protocol, lessons-learned |
| Templates | 3파일 | md-general, meeting-minutes, worklog |
| Hooks | 3개 | debug-residue-check, plan-review-trigger, memory-recall |
| Memory 파일 | 439개 | 1P=1M 규칙, frontmatter 필수, 스마트 저장 판단 |
| MCP 서버 | 19개 | prompt-analyzer 포함 |
| Default Model | Opus | 31개 에이전트 전원 Opus |
| Default Mode | Plan | 모든 세션 Plan 모드로 시작 |
| 종합 점수 | 72/100 | 가중 평균 기준 |

---

## 3. 카테고리별 채점 (9개)

### CAT 1: Architecture & Structure (아키텍처 & 구조) -- 58/100

| 엘리먼트 | 권장 상태 | 현재 구현 | 점수 |
|----------|----------|----------|------|
| PGE 3-Agent GAN Loop | 완전한 Planner-Generator-Evaluator 순환 루프 | Agent Teams의 Plan-Execute-Verify로 구조적 분리 달성. 그러나 GAN 스타일 반복 수렴(quality threshold 기반 재작업) 미구현. 검증 루프 MAX 3이 유사하나 closed-loop 환류 아님 | 65 |
| Initializer Agent Pattern | 세션 초기화 의식 | SessionStart Hook + memory-recall.sh로 메모리 리콜 자동화. 프로젝트별 초기화 의식(git init, progress.md, artifact 초기화) 미체계화 | 55 |
| App Server Architecture | 단일 백엔드, 다중 클라이언트 | 미구현. CLI 단일 클라이언트만 사용 | 10 |
| NLAH Specification | Vendor-agnostic YAML 명세 | 미구현. Claude Code 전용 설계로 vendor lock-in 상태 | 10 |
| Shared Context Store | 멀티 에이전트 간 context 공유 | Agent Teams의 shared task list + Leader-Teammate 구조로 부분 구현. 명시적 write conflict 처리(lock/CRDT) 없음 | 70 |
| Distributed Checkpoint | 분산 상태 관리, 세션 복구 | Hooks로 체크포인트 시점 트리거 존재. 분산 저장소나 자동 복구 경로 없음 | 40 |

**채점 근거**: 구조적 분리(Plan-Execute-Verify)라는 핵심 목표는 달성했으나, 인프라 레벨 아키텍처(App Server, 분산 시스템)와 프레임워크 독립성(NLAH)은 CLI 도구의 태생적 한계로 미구현 상태. 6개 엘리먼트 중 2개는 플랫폼 수준 해결 필요.

**강점**: Plan-Execute-Verify 3-Teammate 분리로 자기평가 편향 제거 구조 확보
**약점**: 인프라 레벨 아키텍처 부재, vendor lock-in

**.claude_harness 대비 갭**: .claude_harness의 에이전트 6개는 역할 분리가 더 명확(planner/executor/verifier 독립성 극대화). 현재 시스템은 범용 오케스트레이션 지향.

---

### CAT 2: Context & Memory (컨텍스트 & 메모리) -- 78/100

| 엘리먼트 | 권장 상태 | 현재 구현 | 점수 |
|----------|----------|----------|------|
| Auto Context Compaction | 토큰 임계값 기반 자동 압축 트리거 | /compact 명령어 존재하나 자동 트리거 미구현. 수동 실행 의존 | 60 |
| Auto Memory System | 프로젝트별 학습 자동 저장/로드 | 1P=1M 규칙으로 완전 구현. 439개 메모리, frontmatter 필수, 스마트 저장 판단, SessionStart 리콜, 중복 방지. 업계 권장 수준 초과 달성 | 95 |
| Artifact Hand-off Spec | 세션 간 상태 전달 포맷 정의 | progress.md 패턴 존재. 공식 artifact spec 미정의 | 55 |
| Context Reuse Strategy | 멀티 세션 artifact 선택적 로딩 | SessionStart 리콜(최근 10개 메모리 자동 주입)이 부분 구현. 관련성 기반이 아닌 시간순 로딩. 토큰 예산 기반 context budgeting 없음 | 65 |

**채점 근거**: 메모리 시스템이 V5.2.0-WE의 가장 강력한 차별점. 1P=1M, L1/L2 실수 캐시, 스마트 저장 판단은 업계 초과 달성. 그러나 "기록"과 "기억"의 간극이 존재 -- 439개 축적은 완벽하나 검색/리콜 효율이 병목.

**강점**: 1P=1M 규칙, L1/L2 실수 캐시, SessionStart 자동 리콜
**약점**: 벡터 검색 미도입, 시간순 리콜의 한계, 자동 compaction 부재

**.claude_harness 대비 갭**: 현재 시스템이 메모리 양에서 압도적이나, 검색 레이어 부재로 실질적 활용률은 저조. 3계층 분류(Core/Reference/Archive)로 개선 가능.

**인사이트 보정**: Why Chain 분석 결과, 1P=1M은 "잊어버리면 안 된다"는 공포에서 출발하여 기억의 양(coverage)에 집중한 반면, 기억의 질(retrieval effectiveness)은 후순위가 되었다. 기억의 목적은 저장이 아니라 "적시에 올바른 맥락을 제공하는 것"이다.

---

### CAT 3: Skill & Procedure (스킬 & 절차) -- 82/100

| 엘리먼트 | 권장 상태 | 현재 구현 | 점수 |
|----------|----------|----------|------|
| Skills as Versioned Procedures | Git 버전 관리, 중앙 레지스트리, 동적 진화 | 47개 스킬 디렉토리, 1,967개 파일. SKILL.md 형식. Git 버전 관리 중. 명시적 버전 번호 관리(v1.0, v1.1)와 자동 format validation 미구현 | 80 |
| AGENTS.md Pattern | 프로젝트별 에이전트 지침 | .claude/agents/ 31개 에이전트 정의 파일로 구현 완료. YAML frontmatter 표준화 | 90 |
| Skill Format Specification | YAML/JSON 기반 표준 포맷 정의 | YAML frontmatter 존재. 스킬 간 포맷 일관성 불완전. Pre-commit 자동 검증 없음 | 75 |

**채점 근거**: 47개 스킬과 31개 에이전트는 업계 최상위 수준의 규모. 에이전트 정의의 표준화(YAML frontmatter + permissionMode + disallowedTools)가 우수. 스킬 포맷 완전 표준화와 자동 검증이 과제.

**강점**: 에이전트 수에서 .claude_harness 목표 대비 5배, 풍부한 스킬 생태계
**약점**: 스킬 간 포맷 불일치, 자동 검증 부재

---

### CAT 4: Evaluation & Quality (평가 & 품질) -- 76/100

| 엘리먼트 | 권장 상태 | 현재 구현 | 점수 |
|----------|----------|----------|------|
| Skeptical Evaluator Mode | 비판적 평가 강제, 최소 3개 문제점 | plan-verifier TeamCreate + Skeptical Evaluator 규칙으로 완전 구현. 필수 출력: 문제점 3개+, 실패 시나리오 3개, 확신도(X/10), 판정 | 90 |
| Eval Harness | 자동 품질 평가 피드백 루프 | 3종 리뷰어(logic/security/edge-case) 병렬 + 검증 루프 MAX 3 + Eval Agents. 구조적 완전 구현이나 quality threshold 수렴 조건 자동화 미완 | 80 |
| Confidence-Based Auto-Approval | 확신도 기반 자동 승인 게이트 | 확신도(X/10) 출력 구현. 자동 승인 로직(>=0.95 auto 등) 미구현. 모든 승인이 수동(Gate 2) | 45 |
| Audit Log & Observability | 불변 감사 로그, 팀 메트릭스 | Hook 기반 로깅 부분적. 체계적 로깅과 팀 메트릭스 미구현 | 55 |
| Audit Trail & Regression Detection | 변경 추적, 회귀 감지 | pr-review + comparator로 부분 구현. 자동화된 regression detection 미구현 | 65 |

**채점 근거**: Skeptical Evaluator와 3종 리뷰어 병렬이 핵심 강점. Boris "이게 된다는 걸 증명해 봐" 원칙의 체계적 구현. 그러나 Confidence-Based Auto-Approval 부재로 모든 승인이 수동이며 워크플로우 병목 초래.

**강점**: 편향 제거 아키텍처, 검증 루프 프로토콜
**약점**: 자동 승인 미구현, Observability 부재

**인사이트 보정**: 비평가 관점에서 검증 루프 MAX 3이 실제로 품질을 향상시킨다는 정량적 데이터가 부재하다. Critical 발견 빈도, 재시도 후 해결률, MAX 초과 빈도가 추적되지 않는다. 측정 없는 최적화는 맹목적이다.

---

### CAT 5: Multi-Client & Integration (멀티 클라이언트 & 통합) -- 28/100

| 엘리먼트 | 권장 상태 | 현재 구현 | 점수 |
|----------|----------|----------|------|
| Multi-Client Architecture | 단일 백엔드, 다중 프론트엔드 | 미구현. CLI 단독 사용. Claude Code 플랫폼의 구조적 제약 | 5 |
| Streaming Progress | SSE/WebSocket 실시간 피드백 | 미구현. 구조화된 스트리밍 프로토콜 없음 | 10 |
| IDE Plugin Integration | VS Code 확장 + 하네스 통합 | VS Code 확장 사용 중이나 하네스 통합 없음 | 30 |
| Git + CI-CD Integration | 스킬 -> Git -> CI/CD -> 자동 배포 | commit-push, pr-review 스킬로 Git 워크플로우 구현. CI/CD 파이프라인 통합 미구현 | 40 |

**채점 근거**: 가장 낮은 점수의 카테고리. Claude Code CLI 도구의 태생적 한계에서 기인. Multi-Client/Streaming은 Anthropic 플랫폼 레벨 기능이므로 사용자가 직접 구현 불가. 외부 종속적 제약이 가장 큰 카테고리.

**강점**: Git 워크플로우 스킬 수준 구현
**약점**: 플랫폼 종속으로 대부분 구현 불가

---

### CAT 6: Orchestration & Workflow (오케스트레이션 & 워크플로우) -- 85/100

| 엘리먼트 | 권장 상태 | 현재 구현 | 점수 |
|----------|----------|----------|------|
| Handoff Mechanism | State Machine 기반 동적 라우팅 | Agent Teams 태스크 의존성 + Leader-Teammate 구조로 부분 구현. 명시적 state machine 정의 없음. Chain 패턴이 정적 워크플로우로 대체 | 75 |
| Hierarchical Task Delegation | Manager Agent + 구조화된 task list | Leader + Teammate 구조 + 10개 Chain 계층적 위임. Teams 자동 트리거 6개, 복잡도 분기 구현 | 90 |
| Hybrid Execution Strategy | 복잡도 기반 실행 경로 결정 | 복잡도 분기(단순/중규모/대규모) 완전 구현. Effort Level 3단계, Chain vs Teams 선택 기준 명확 | 90 |

**채점 근거**: 두 번째 강점 영역. 10개 Chain + Effort Level + Agent Teams 통합 + 복잡도 기반 분기는 업계 권장사항 대부분 커버. Chain-Teams 전환 적합도 매트릭스가 정교. 남은 과제는 정적 Chain에서 동적 State Machine 기반 라우팅으로의 진화.

**강점**: 오케스트레이션 정교함, 하이브리드 실행 전략
**약점**: 정적 Chain 패턴, 동적 라우팅 미구현

**인사이트 보정**: Why Chain 분석 결과, Chain과 Teams의 이중 시스템은 "WHAT vs HOW"의 미분리에서 기인한다. Chain이 워크플로우 명세(선언적)로, Teams가 실행 엔진(명령적)으로 진화하면 상호보완성이 된다. 현재 체인 표기법의 `||`(병렬)과 `->`(순차)를 Teams 자동 트리거로 격상하는 것이 최소 비용 접근이다.

---

### CAT 7: Security & Access Control (보안 & 접근 제어) -- 72/100

| 엘리먼트 | 권장 상태 | 현재 구현 | 점수 |
|----------|----------|----------|------|
| Approval Workflow | 다층 승인 체인, 위험 작업 차단 | Plan 모드 + Gate 2 승인 + PreToolUse Hook 차단으로 핵심 구현. 1인 사용자 환경이므로 다층 승인 해당 없음 | 85 |
| Filesystem Access Control | 화이트리스트/블랙리스트 정책 | PreToolUse에서 .env, .pem, 시스템 디렉토리 차단. 전체 화이트리스트 정의 없음 (블랙리스트만) | 55 |
| Skill Permission Model | 스킬별 세분화된 접근 제어 | YAML frontmatter에서 tools, disallowedTools로 도구 제한 구현. permissionMode 분리. 세분화 수준 미달 | 70 |
| Multi-Tenant Isolation | 조직/팀 세션 격리 | 메모리 격리 규칙(Teammate 저장 금지, Leader만 저장)으로 부분 구현. 1인 환경이므로 다중 테넌트 해당 없음 | 60 |

**채점 근거**: 1인 사용자 환경에서의 보안은 잘 구현. PreToolUse Hook의 위험 명령/민감 파일 차단이 실용적. 화이트리스트 전환과 permission 세분화가 개선 포인트.

**강점**: 위험 명령 차단, 민감 파일 보호
**약점**: 화이트리스트 부재, Phase별 권한 분리 미자동화

---

### CAT 8: Configuration & Layering (구성 & 계층화) -- 62/100

| 엘리먼트 | 권장 상태 | 현재 구현 | 점수 |
|----------|----------|----------|------|
| Multi-Layer Scope System | 4계층 우선순위 | ~/.claude/ + 프로젝트 CLAUDE.md 2계층 사용. Managed Policy/Subdirectory 미활용 | 65 |
| Managed Policy Layer | 조직 수준 강제 규칙 | 미구현. 1인 환경에서 불필요 | 20 |
| Path-Specific Rules | YAML paths: glob 기반 규칙 범위 한정 | rules/ 4파일로 주제별 분리. 경로별 조건부 적용 미구현 | 45 |
| .claude/rules/ Partitioning | 주제별 규칙 파일 분산 | 4개 파일로 분리. C3 모듈화 달성 | 85 |
| Import Syntax (@) | 외부 파일 포함 | 미구현. Claude Code 플랫폼 미지원 | 10 |
| HTML Comment Stripping | 블록 주석 토큰 최적화 | 미구현. HTML 주석이 그대로 context에 포함 | 15 |
| claudeMdExcludes | Monorepo 필터링 | 미구현. 단일 프로젝트 환경 | 15 |
| User-Level Path Rules | ~/.claude/rules/ 글로벌 규칙 | 구현 완료. 4개 글로벌 규칙 파일 존재 | 85 |

**채점 근거**: C3 모듈화로 CLAUDE.md ~90줄 달성은 200줄 제한 초과 달성. 그러나 Import Syntax, HTML Comment Stripping, claudeMdExcludes 등 플랫폼 고급 기능 미활용. 플랫폼 기능 활용도에 의해 점수 제한.

**강점**: C3 모듈화, 200줄 제한 초과 달성
**약점**: 플랫폼 고급 기능 미활용

---

### CAT 9: Automation & Efficiency (자동화 & 효율성) -- 71/100

| 엘리먼트 | 권장 상태 | 현재 구현 | 점수 |
|----------|----------|----------|------|
| Cost Monitoring | 세션/에이전트별 토큰 예산 | 미구현. 비용 인식 없이 Opus 전면 사용 | 10 |
| Selective Compaction | 중요도 기반 선택적 압축 | /compact 존재하나 중요도 scoring 없음 | 50 |
| 4-Step Workflow | Explore->Plan->Implement->Commit | 바이브코딩 4단계 + Harness 5단계로 완전 구현. defaultMode: plan으로 워크플로우 강제 | 95 |
| Context Management Commands | /clear, /compact 사용 가이드 | 사용 중. 고급 명령 활용 미문서화 | 75 |
| Compaction Instruction Preservation | /compact 시 보존 항목 명시 | 보존 규칙 문서화 완료 | 90 |
| 200-Line Limit | CLAUDE.md 200줄 이하 | ~90줄로 초과 달성 | 100 |
| Specificity Verification | 구체적, 검증 가능한 규칙 | 3종 리뷰어 + Quality Manager로 구현 | 80 |
| Subagent Delegation | 병렬 조사 위임 | Agent Teams 6개 트리거로 체계적 위임 구현 | 85 |
| CLAUDE.md as Code | Git 버전 관리, dead rule pruning | Git 관리 + CHANGELOG.md + Self-Maintenance 규칙 | 85 |
| Failure Antipatterns Doc | 알려진 실패 패턴 문서화 | L1/L2 실수 캐시(MAX 100, PIN, 졸업 로직)로 구현. 업계 유례 없는 독자적 혁신 | 85 |
| Content Inclusion Checklist | 포함/제외 경계 정의 | 미구현. 명시적 체크리스트 없음 | 25 |
| Advisory vs Hooks | 권고 vs 강제 구분 | 3-tier 구분 시작. 명시적 분류 미완 | 65 |

**채점 근거**: 4-Step Workflow, CLAUDE.md 경량화, 실패 패턴 문서화가 강점. L1/L2 실수 캐시는 업계 유례 없는 혁신. Cost Monitoring 완전 부재와 Content Inclusion Checklist 미구현이 약점.

**강점**: 4-Step Workflow 완전 구현, L1/L2 실수 캐시
**약점**: Cost Monitoring 완전 부재, Advisory/Hooks 분류 미완

---

## 4. 종합 점수 산출

### 가중치 테이블

| 카테고리 | 가중치 | 근거 |
|----------|--------|------|
| CAT 1: Architecture | 12% | 기반 구조이나 플랫폼 종속적 항목 다수. 사용자 제어 범위 제한적 |
| CAT 2: Context & Memory | 15% | AI 에이전트 하네스의 핵심 차별점. 세션 간 연속성과 학습 능력 직결 |
| CAT 3: Skill & Procedure | 12% | 재사용성과 확장성의 기반. 생태계 크기가 생산성 직결 |
| CAT 4: Evaluation & Quality | 18% | 하네스의 존재 이유. 자기평가 편향 제거와 품질 보증이 핵심 가치 |
| CAT 5: Multi-Client | 5% | 1인 CLI 환경에서 우선순위 낮음. 엔터프라이즈 확장 시 중요도 상승 |
| CAT 6: Orchestration | 15% | 복잡한 작업의 체계적 분해와 실행. 일상 사용에서 가장 빈번히 작동 |
| CAT 7: Security | 10% | 공공기관 SI 환경에서 보안 준수 필수 |
| CAT 8: Configuration | 6% | 설정 체계가 작업 품질에 미치는 영향은 간접적 |
| CAT 9: Automation | 7% | 효율성 최적화. 생산성 향상 기여 |

### 가중 평균 계산

| 카테고리 | 점수 | 가중치 | 가중 점수 |
|----------|------|--------|----------|
| CAT 1: Architecture | 58 | 0.12 | 6.96 |
| CAT 2: Context & Memory | 78 | 0.15 | 11.70 |
| CAT 3: Skill & Procedure | 82 | 0.12 | 9.84 |
| CAT 4: Evaluation & Quality | 76 | 0.18 | 13.68 |
| CAT 5: Multi-Client | 28 | 0.05 | 1.40 |
| CAT 6: Orchestration | 85 | 0.15 | 12.75 |
| CAT 7: Security | 72 | 0.10 | 7.20 |
| CAT 8: Configuration | 62 | 0.06 | 3.72 |
| CAT 9: Automation | 71 | 0.07 | 4.97 |
| **종합** | | **1.00** | **72.22** |

### 레이더 차트용 데이터

```
카테고리,점수
Architecture,58
Context & Memory,78
Skill & Procedure,82
Evaluation & Quality,76
Multi-Client,28
Orchestration,85
Security,72
Configuration,62
Automation,71
```

---

## 5. 핵심 인사이트

### TOP 5 강점

**S-1. 메모리 시스템의 독창성** (CAT 2, Auto Memory 95점)
1P=1M 규칙, 스마트 저장 판단, L1/L2 실수 캐시, SessionStart 자동 리콜은 업계 권장사항을 초과하는 독자적 혁신이다. 특히 L1 실수 캐시의 MAX 100 + PIN + 졸업 로직은 인지 과학의 작업 기억/장기 기억 모델을 실용적으로 구현한 사례이며, "학습하는 하네스" 패러다임의 선구자다.

**S-2. 자기평가 편향 제거 아키텍처** (CAT 4/6, Skeptical Evaluator 90점)
Plan-Execute-Verify 3-Teammate 분리 + 정보 차단 + 메타정보 제거 + Skeptical Evaluator("최소 3개 문제점 필수") + Pre-Mortem Gate. 다층 편향 제거 메커니즘이 PGE 3-Agent GAN Loop 권장사항을 대부분 충족.

**S-3. 오케스트레이션 정교함** (CAT 6, 85점)
10개 Chain + Effort Level 3단계 + Agent Teams 6개 트리거 + 복잡도 분기 + Chain-Teams 하이브리드 선택 기준. 개인 사용자 하네스 중 최상위급. 이 설계 패턴을 NLAH 형식으로 추상화하면 vendor-agnostic 오케스트레이션 프레임워크가 될 잠재력.

**S-4. C3 모듈화의 구조적 우수성** (CAT 8/9)
CLAUDE.md 486줄에서 ~90줄로 81% 감량. rules/(4파일) + templates/(3파일) + skills/(47개) + agents/(31개)의 5계층 분산이 확장성, 유지보수성, context 효율성을 동시에 개선. 이 모듈화가 이후 모든 진화(Boris 통합, 검증 루프, Pre-Mortem)의 기반.

**S-5. 검증 루프 프로토콜** (CAT 4, Eval Harness 80점)
3종 리뷰어(logic/security/edge-case) 병렬 + 검증 루프 MAX 3 + 잔여 보고 형식. 6개 체인(A,B,C,D,G,J)에 통합 적용되어 모든 코드 생산 경로에 품질 게이트 존재.

---

### TOP 5 약점

**W-1. Cost Monitoring 완전 부재** (CAT 9, 10점)
Opus 모델을 31개 에이전트 전원에게 적용하면서 비용 인식이 전무하다. 세션별/에이전트별 토큰 예산 없음. Agent Teams 병렬 실행 + Opus 전원 사용은 비용 폭발의 잠재적 위험. 하네스 리서치의 모든 보고서가 권장하는 유일하게 완전 무시된 항목.

**W-2. Multi-Client & Integration 구조적 한계** (CAT 5, 28점)
CLI 단독 사용, Streaming 미지원, IDE 하네스 미통합. Claude Code 플랫폼의 태생적 한계. Git+CI/CD 통합(GitHub Actions)도 미시도.

**W-3. 자동 Context Compaction 부재** (CAT 2, 60점)
/compact 명령어가 존재하나 토큰 임계값 기반 자동 트리거가 없다. 장시간 세션 context 포화에 수동 대응만 가능. Selective Compaction(중요도 기반)도 미구현.

**W-4. 시스템 복잡도의 자기 증식** (전체 시스템)
10개 Chain * 31개 Agent * 47개 Skill * 439개 Memory의 천문학적 조합. V5.1.1 "템플릿 Read 스킵" 사건이 복잡도 문제의 실증. 시스템 유지보수 비용이 제공 가치와 경쟁하기 시작하는 복잡도 임계점에 근접. 파레토 법칙 적용 시, 전체 에이전트/스킬의 20%가 가치의 80%를 생산하고 있을 가능성이 높다.

**W-5. 동적 라우팅 부재** (CAT 6, Handoff 75점)
10개 Chain이 정적 패턴으로 정의. 새 작업 유형에 Chain 자체 수정 필요. state machine 기반 동적 라우팅 미구현으로 오케스트레이션 확장성 제한.

---

### 반직관적 발견 3개 (Why 5회 분석 포함)

#### 발견 1: "학습하는 하네스"가 실제로는 "기록하는 하네스"다

**현상**: 439개 메모리를 축적한 시스템이 "학습"하고 있다고 판단되지만, 실제로는 95%의 메모리가 다시 로드되지 않는다.

**Why 5회 분석**:
- L1: 왜 미활용? -- SessionStart가 최근 10개만 시간순으로 가져옴
- L2: 왜 시간순만? -- 관련성 기반 검색(벡터)이 미구현
- L3: 왜 벡터 미도입? -- Windows에서 Docker/Qdrant 미사용 결정
- L4: 왜 저장/검색 분리 실패? -- 1P=1M은 저장 빈도만 정의, 검색 경로 설계 부재
- L5: 왜 검색 설계 누락? -- "잊어버리면 안 된다"는 공포에서 출발, 기억의 양(coverage)에 집중하며 질(retrieval)은 후순위

**통찰**: 완벽한 기록(log)과 효과적인 기억(memory)은 근본적으로 다른 시스템이다. 해결 방향은 3계층 분류(Core ~30 / Reference ~100 / Archive ~309) + frontmatter 기반 키워드 매칭 리콜.

#### 발견 2: 규칙이 많을수록 규칙 준수가 어려워진다 (복잡도의 재귀적 함정)

**현상**: .claude_harness가 미배포 상태인 근본 원인은 기술적 문제가 아니라, 이미 복잡도 임계점에 근접한 시스템에 추가 복잡도를 도입하는 것에 대한 암묵적 저항이다.

**Why 5회 분석**:
- L1: 왜 미배포? -- 현재 시스템이 "충분히 잘 작동"
- L2: 왜 전환 안 함? -- 전환 비용이 기대 이익보다 크게 체감
- L3: 왜 이익 과소평가? -- Advisory 실패는 조용히 발생, 손실이 비가시적
- L4: 왜 비가시적? -- Enforcement 없으면 규칙 위반의 피드백 루프가 열림
- L5: 왜 열린 루프 방치? -- 닫힌 루프 생성이 복잡도를 추가하며, 이미 임계점 근접

**통찰**: 해결책은 "추가"가 아니라 "대체". Hook을 도입하면서 대응하는 Advisory 규칙을 CLAUDE.md에서 "졸업"시켜 복잡도를 일정하게 유지해야 한다.

#### 발견 3: L1 실수 캐시 2건은 "실수가 적은 것"이 아니라 "기록이 안 되는 것"일 수 있다

**현상**: MAX 100 용량에 실제 기록 2건. 이는 시스템이 잘 작동해서가 아니라, 기록 행위 자체가 Advisory(규칙)이지 Enforcement(코드)가 아니기 때문일 가능성이 높다.

**통찰**: Advisory vs Enforcement 문제의 또 다른 증거. 시스템의 효과를 주장하려면 효과를 측정해야 한다. 측정 없는 최적화는 맹목적이다.

---

### 숨겨진 패턴

**패턴 1: Advisory에서 Enforcement로의 진화 벡터**
시간적으로 CLAUDE.md 규칙(Advisory)에서 Hook(Enforcement)으로 진화해왔다. V5.1.1 "규칙 스킵 문제"라는 실패 경험이 원인. .claude_harness의 Hook 6종은 이 진화의 다음 단계이며, strip-metadata.py가 정점이다.

**패턴 2: 복잡도-가치 균형의 임계점**
1인 사용자 환경에 31개 에이전트와 47개 스킬은 과잉 공급 가능성. 시스템의 자기 진화 능력(매크로)이 개별 요소 유지 비용(마이크로)과 충돌. 향후 6개월 내 표면화 전망.

**패턴 3: 학습 루프의 비대칭성**
L1 실수 캐시(실패 학습)는 체계화되었으나, "성공 패턴의 학습"은 일반 메모리에 묻혀 검색 불가. lessons-learned.md는 실수만 기록하며, "이 접근이 왜 성공했는가"의 학습이 부재. 강화 학습의 보상 신호 비대칭 문제와 동형.

---

### 시스템 긴장

**긴장 1: Chain(정적 워크플로우) vs Teams(동적 병렬 실행)**
서로 다른 시대(Chain=V4, Teams=V5)의 해결책이 공존. Chain=WHAT, Teams=HOW로 관심사 분리가 필요하나 현재는 관계가 암묵적이어서 "보완인가 대체인가" 혼란 발생.

**긴장 2: 기록 완전성(439개 메모리) vs 검색 효율성(최근 10개 리콜)**
1P=1M의 저장 강박과 시간순 리콜의 단순성이 충돌. 메모리가 많을수록 관련 메모리 발견이 어려워지는 역설.

**긴장 3: 설계의 정교함 vs 실행의 일관성**
규칙의 양이 아니라 규칙의 준수율을 측정해야 한다. 72점 채점 자체가 자기평가 편향에 빠져 있을 가능성(분석 주체가 시스템 내부자).

---

## 6. 개선 로드맵

### Phase 1: 즉시 실행 (1주 내)

| # | 액션 아이템 | 구체적 작업 | 예상 점수 변화 | 리스크 |
|---|-----------|-----------|--------------|--------|
| 1-1 | Teams 운영 파라미터 추가 | `settings.json`에 `maxTeammates: 5`, `defaultSize: 3`, `autoCleanupTimeout: 3600` 명시 | CAT 6: 85->87 | 낮음. 설정 추가만으로 기존 동작 무영향 |
| 1-2 | 메모리 분석 스크립트 작성 | `memory-analyzer.sh`: 439개 메모리의 type/월/프로젝트별 분포 보고서 생성 | 직접 점수 변화 없음 (Phase 2 전제 조건) | 낮음. 읽기 전용 작업 |
| 1-3 | 5개 핵심 메트릭 정의 | `metrics-definition.md`: Chain 선택 정확도, 검증 루프 해결률, 메모리 리콜 적중률, 승인 소요 시간, L1 실수 누적 속도 | CAT 4: 76->78 | 낮음. 문서 작성만 |
| 1-4 | Advisory 졸업 매핑 테이블 | Hook으로 대체 가능한 Advisory 규칙 식별 + 1:1 매핑 테이블 작성 (`advisory-graduation.md`) | 직접 점수 변화 없음 (로드맵 기반) | 낮음. 분석 작업만 |

**Phase 1 종합 효과**: 72 -> 74 (+2점). 주로 기반 작업. Phase 2/3의 전제 조건 확보에 핵심적.

---

### Phase 2: 단기 (1~3주)

| # | 액션 아이템 | 구체적 작업 | 예상 점수 변화 | 리스크 |
|---|-----------|-----------|--------------|--------|
| 2-1 | verify-task Hook 도입 | Python 기반. TaskCompleted 시 테스트/린트/보안 자동 검사. 1주차 warn-only -> 2주차 enforce. 환경변수 `ENABLED=true/false`로 롤백 경로 확보 | CAT 4: 78->83 (Eval Harness 80->88). **최고 ROI 액션** | 중간. 오탐 가능성. warn-only 기간 필수 |
| 2-2 | 메모리 3계층 분류 실행 | Core(~30) / Reference(~100) / Archive(~309) 분류. `memory-recall.sh` 키워드 매칭 개선. 아카이브는 `~/.claude/.memory/archive/`로 이동. 색인 `index.md` 생성 | CAT 2: 78->84 (Context Reuse 65->80). 리콜 정확도 ~3배 향상 | 중간. 오분류 위험. 아카이브 보존으로 완화 |
| 2-3 | Chain 실행 모드 태그 추가 | 체인 표기법의 `\|\|`를 Teams 자동 트리거로 공식 정의. orchestration.md 업데이트 | CAT 6: 87->89 | 낮음. 문서 업데이트 수준 |
| 2-4 | Confidence-Based Auto-Approval 설계 | 9+/10 자동 승인, 7-8/10 요약 후 무응답 시 자동 진행, 6 이하 수동 승인 | CAT 4: 83->86 (Confidence Auto-Approval 45->70). 사용자 주의 비용 ~50% 감소 | 중간. 초기 임계값 보수적(9+) 설정으로 완화 |
| 2-5 | 메트릭 수집 시작 | PostToolUse Hook에 카운터 로깅 추가. 주간 메트릭 보고서 자동 생성 | CAT 9: 71->75 | 낮음. 로깅 오버헤드 미미 |

**Phase 2 종합 효과**: 74 -> 81 (+7점). "Advanced -> Expert 경계" 도달.

---

### Phase 3: 중기 (1~3개월)

| # | 액션 아이템 | 구체적 작업 | 예상 점수 변화 | 리스크 |
|---|-----------|-----------|--------------|--------|
| 3-1 | phase-guard Hook 도입 | PreToolUse에서 Phase별 도구 제한. Plan Phase에서 file edit 차단 코드화. Phase 상태는 Status 필드 기반 | CAT 7: 72->78 | 중간. Phase 상태 관리 메커니즘 필요 |
| 3-2 | strip-metadata Hook 도입 | SubagentStop 시 산출물 메타정보 자동 제거. 정보 차단의 Enforcement 달성. 보수적 필터링 + 화이트리스트 접근 | CAT 4: 86->89 (GAP 1 해소) | 높음. 유효 정보 오제거 위험 |
| 3-3 | 성공 패턴 학습 시스템 | `wins-captured.md` 도입. 메모리에서 반복 패턴 추출. 3회 반복 시 스킬 후보 자동 제안 | CAT 2: 84->88 | 중간. "성공" 정의가 주관적 |
| 3-4 | Chain 축소 검토 | 메트릭 기반 사용 빈도 하위 2개 Chain 식별 -> 동적 체인 생성으로 대체 | CAT 9: 75->78 (복잡도 ~20% 감소) | 중간. 동적 체인 품질 보장 필요 |
| 3-5 | Cost Monitoring 도입 | 세션별/에이전트별 토큰 추적. 예산 임계값 경고. Opus/Sonnet 혼합 검토 | CAT 9: 78->85 (Cost Monitoring 10->60) | 낮음(모니터링). 중간(모델 혼합 품질) |
| 3-6 | Advisory 졸업 1차 실행 | Phase 2/3 Hook에 대응하는 Advisory 규칙을 CLAUDE.md/rules에서 졸업. Hook 안정화 확인 후 실행 | CAT 8: 62->68 | 중간. 졸업 대상 판단 오류 시 안전망 약화 |

**Phase 3 종합 효과**: 81 -> 87 (+6점). "Expert Level Harness" 도달. 사용자 제어 가능 범위 내 최고 수준 근접.

**점수 개선 경로 요약**: 72 -> 74 (즉시) -> 81 (단기) -> 87 (중기)

---

## 7. .claude_harness 통합 전략

### 전면 배포 vs 점진적 도입 비교

| 기준 | 전면 배포 | 점진적 도입 (권장) |
|------|---------|-----------------|
| 리스크 | 높음. Hook 언어 충돌(bash vs PS), 규칙 분류 체계 충돌(기능별 vs Phase별), 에이전트 역할 중첩 | 낮음. 충돌 없는 항목부터 도입, 1 Hook씩 안정화 |
| 전환 비용 | 높음. 학습 곡선 + 호환성 테스트 + 안정성 리스크 동시 발생 | 낮음. 각 Hook별 1주 warn-only 기간 |
| 효과 체감 시점 | 즉시 (그러나 불안정) | 점진적 (그러나 안정적) |
| 복잡도 관리 | 위험. "추가 레이어"로 복잡도 급증 | 안전. Advisory 졸업과 병행하여 복잡도 일정 유지 |
| 롤백 용이성 | 어려움 | 쉬움. 개별 Hook ENABLED=false로 즉시 비활성화 |

### 권장 접근법: 선택적 통합 (Cherry-Pick Integration) + "1 Hook, 1 Rule, 1 Metric" 원칙

매번 도입하는 것은 딱 3개: Hook 1개, 그 Hook이 대체하는 Advisory Rule 1개, 효과를 측정하는 Metric 1개.

### 구체적 실행 단계

**Step 1: strip-metadata.py 즉시 도입** (충돌 없이 순수 시너지)
- 역할: TeamCreate의 "reasoning 차단"을 코드로 물리적 보장
- 졸업 Rule: "reasoning 차단 -- 산출물만 전달" Advisory 규칙
- Metric: Verifier 편향 감지 빈도 (전후 비교)
- 리스크: 텍스트 처리 오제거. 보수적 필터링으로 완화

**Step 2: verify-task Hook 1주 내 도입** (최고 ROI)
- 역할: TaskCompleted 시 자동 테스트/린트/보안 검사
- 졸업 Rule: 검증 루프 Advisory 규칙의 1차 필터 (Hook 통과 시 리뷰어 스킵 허용)
- Metric: Hook 통과률(%), 리뷰어 추가 발견률(Hook 미감지 Critical %)
- 리스크: 오탐 가능. 1주 warn-only 기간 필수

**Step 3: phase-guard Hook 2주 내 도입** (Phase별 권한 코드화)
- 역할: PreToolUse에서 현재 Phase에 따라 도구 제한
- 졸업 Rule: "Status: approved 전 code_developer 금지" Advisory 규칙
- Metric: Phase 위반 차단 횟수(/월), 오차단율

**Step 4: Phase별 규칙 파일 3주 내 도입** (기능별 규칙과 병행, 점진적 전환)
- `phase-plan.md`, `phase-execute.md`, `phase-verify.md` 도입
- 기존 기능별 규칙(orchestration, memory 등)과 병존. 중복 영역은 Phase 규칙 우선

**Step 5: devils-advocate 에이전트 유보** (plan-verifier 역할 정리 후)
- 현재 plan-verifier와 기능 중첩. 역할 경계 명확화 후 도입
- Skeptical Evaluator(산출물 검증) vs Devils-Advocate(접근법 도전)의 보완적 역할 정의 필요

**Step 6: check-idle-reason Hook 유보** (Agent Teams 안정화 후)
- Teams가 Experimental 상태. API 변경 시 무효화 위험

### 언어 통일 권장

- 기존 3개 Hook: bash (.sh)
- 추가 Hook 권장: Python 통일
  - bash는 Windows에서 Git Bash 의존
  - PowerShell은 Claude Code Hook에서 제한적 지원
  - Python은 Windows/Mac/Linux 모두 안정적, 텍스트 처리에 최적

### 안정성 보장 메커니즘

- **Canary 배포**: 새 Hook을 "경고 모드(warn-only)"로 도입, 1주간 오탐률 확인 후 "강제 모드(enforce)"로 전환
- **롤백 경로**: 각 Hook에 `ENABLED=true/false` 환경변수 → 즉시 비활성화 가능
- **영향 범위 제한**: Hook별 적용 대상 Chain 지정, 전체 시스템이 아닌 특정 워크플로우만 영향

---

## 8. 부록

### 49개 엘리먼트 전체 매핑표

| # | 엘리먼트명 | 카테고리 | 현재 구현 상태 | 점수 |
|---|----------|---------|-------------|------|
| 1 | PGE 3-Agent GAN Loop | CAT 1: Architecture | 구조적 분리 달성, GAN 수렴 미구현 | 65 |
| 2 | Initializer Agent Pattern | CAT 1: Architecture | SessionStart Hook 존재, 프로젝트별 초기화 미체계화 | 55 |
| 3 | App Server Architecture (JSON-RPC) | CAT 1: Architecture | 미구현 (플랫폼 제약) | 10 |
| 4 | NLAH Specification | CAT 1: Architecture | 미구현 (vendor lock-in) | 10 |
| 5 | Shared Context Store | CAT 1: Architecture | Agent Teams로 부분 구현 | 70 |
| 6 | Distributed Checkpoint | CAT 1: Architecture | Hook 트리거 존재, 분산 저장소 없음 | 40 |
| 7 | Auto Context Compaction | CAT 2: Context & Memory | /compact 존재, 자동 트리거 없음 | 60 |
| 8 | Auto Memory System | CAT 2: Context & Memory | 1P=1M 완전 구현, 업계 초과 달성 | 95 |
| 9 | Artifact Hand-off Spec | CAT 2: Context & Memory | progress.md 존재, 공식 spec 미정의 | 55 |
| 10 | Context Reuse Strategy | CAT 2: Context & Memory | SessionStart 리콜 부분 구현, 시간순 한계 | 65 |
| 11 | Skills as Versioned Procedures | CAT 3: Skill & Procedure | 47개 스킬, 버전 번호/자동 검증 미구현 | 80 |
| 12 | AGENTS.md Pattern | CAT 3: Skill & Procedure | 31개 에이전트, YAML 표준화 완료 | 90 |
| 13 | Skill Format Specification | CAT 3: Skill & Procedure | YAML frontmatter 존재, 일관성 불완전 | 75 |
| 14 | Skeptical Evaluator Mode | CAT 4: Evaluation & Quality | plan-verifier + 규칙으로 완전 구현 | 90 |
| 15 | Eval Harness | CAT 4: Evaluation & Quality | 3종 리뷰어 + 검증 루프 구현 | 80 |
| 16 | Confidence-Based Auto-Approval | CAT 4: Evaluation & Quality | 확신도 출력 구현, 자동 승인 미구현 | 45 |
| 17 | Audit Log & Observability | CAT 4: Evaluation & Quality | 부분적 로깅, 메트릭스 미구현 | 55 |
| 18 | Audit Trail & Regression Detection | CAT 4: Evaluation & Quality | pr-review로 부분 구현, 자동 regression 미구현 | 65 |
| 19 | Multi-Client Architecture | CAT 5: Multi-Client | 미구현 (플랫폼 제약) | 5 |
| 20 | Streaming Progress | CAT 5: Multi-Client | 미구현 | 10 |
| 21 | IDE Plugin Integration | CAT 5: Multi-Client | VS Code 사용, 하네스 미통합 | 30 |
| 22 | Git + CI-CD Integration | CAT 5: Multi-Client | Git 스킬 구현, CI/CD 미통합 | 40 |
| 23 | Handoff Mechanism | CAT 6: Orchestration | Agent Teams로 부분 구현, State Machine 없음 | 75 |
| 24 | Hierarchical Task Delegation | CAT 6: Orchestration | Leader-Teammate + 10 Chain 구현 | 90 |
| 25 | Hybrid Execution Strategy | CAT 6: Orchestration | 복잡도 분기 + Effort Level 완전 구현 | 90 |
| 26 | Approval Workflow | CAT 7: Security | Plan 모드 + Gate 2 + PreToolUse 차단 | 85 |
| 27 | Filesystem Access Control | CAT 7: Security | 블랙리스트 존재, 화이트리스트 없음 | 55 |
| 28 | Skill Permission Model | CAT 7: Security | YAML 도구 제한 구현, 세분화 미달 | 70 |
| 29 | Multi-Tenant Isolation | CAT 7: Security | 메모리 격리 규칙 부분 구현 | 60 |
| 30 | Multi-Layer Scope System | CAT 8: Configuration | 2계층 사용 (4계층 중) | 65 |
| 31 | Managed Policy Layer | CAT 8: Configuration | 미구현 (1인 환경) | 20 |
| 32 | Path-Specific Rules | CAT 8: Configuration | 주제별 분리, 경로별 적용 없음 | 45 |
| 33 | .claude/rules/ Partitioning | CAT 8: Configuration | 4파일 분리, C3 모듈화 달성 | 85 |
| 34 | Import Syntax (@) | CAT 8: Configuration | 미구현 (플랫폼 미지원) | 10 |
| 35 | HTML Comment Stripping | CAT 8: Configuration | 미구현 | 15 |
| 36 | claudeMdExcludes | CAT 8: Configuration | 미구현 (단일 프로젝트) | 15 |
| 37 | User-Level Path Rules | CAT 8: Configuration | 4개 글로벌 규칙 파일 구현 | 85 |
| 38 | Cost Monitoring | CAT 9: Automation | 미구현 (완전 부재) | 10 |
| 39 | Selective Compaction | CAT 9: Automation | /compact 존재, 중요도 scoring 없음 | 50 |
| 40 | 4-Step Workflow | CAT 9: Automation | 완전 구현, defaultMode: plan | 95 |
| 41 | Context Management Commands | CAT 9: Automation | 기본 사용 중, 고급 미문서화 | 75 |
| 42 | Compaction Instruction Preservation | CAT 9: Automation | 보존 규칙 문서화 완료 | 90 |
| 43 | 200-Line Limit | CAT 9: Automation | ~90줄 초과 달성 | 100 |
| 44 | Specificity Verification | CAT 9: Automation | 3종 리뷰어로 구현 | 80 |
| 45 | Subagent Delegation | CAT 9: Automation | Agent Teams 6개 트리거로 체계적 구현 | 85 |
| 46 | CLAUDE.md as Code | CAT 9: Automation | Git + CHANGELOG + Self-Maintenance | 85 |
| 47 | Failure Antipatterns Doc | CAT 9: Automation | L1/L2 실수 캐시 (독자적 혁신) | 85 |
| 48 | Content Inclusion Checklist | CAT 9: Automation | 미구현 | 25 |
| 49 | Advisory vs Hooks | CAT 9: Automation | 3-tier 구분 시작, 분류 미완 | 65 |

---

### 확신도 및 한계 선언

**확신도: 8/10**

| 영역 | 확신도 |
|------|--------|
| 메모리 3계층화 필요성과 방향 | 9/10 |
| verify-task Hook의 높은 ROI | 9/10 |
| Advisory -> Enforcement 졸업 패턴 타당성 | 8/10 |
| Chain/Teams의 WHAT/HOW 분리 방향 | 7/10 (이론 타당, 실행 복잡도 불확실) |
| Confidence-Based Auto-Approval 임계값 | 6/10 (데이터 없이 설정, 조정 필요) |
| strip-metadata Hook 구현 품질 | 5/10 (텍스트 처리 정밀도 불확실) |
| Chain 축소 적정 수준 | 5/10 (사용 빈도 데이터 부재) |

**한계 선언**:

1. 이 분석 자체가 시스템 내부자에 의한 분석이므로, 시스템의 맹점을 완전히 식별하지 못했을 가능성이 있다
2. 점수 변화 추정은 유사 시스템 벤치마크가 아닌 논리적 추론에 기반한다. 실제 효과는 다를 수 있다
3. 439개 메모리의 실제 활용 패턴 데이터가 없어, "95% 미활용" 추정은 SessionStart 리콜 메커니즘의 구조적 한계에서 유추한 것이다
4. .claude_harness와의 통합 시나리오는 프로토타입 상태이므로, 실제 배포 시 예상하지 못한 호환성 문제가 발생할 수 있다
5. 72점이 "고급 수준"이라는 결론은 외부 벤치마크 없이 검증 불가능하다

---

*분석 완료: 2026-04-06 | ResearchChain HIGH*
*분석 프레임워크: multidimensional_analyst (5차원 분석 + 9개 카테고리 채점) + insight_explorer (반직관적 발견) + insight_amplifier (5+ Why / 5 관점 / 3-Round 정제 / What-If & HMW) + integrated_sage (통합)*
*종합 점수 개선 경로: 72 -> 74 (즉시) -> 81 (단기) -> 87 (중기)*
