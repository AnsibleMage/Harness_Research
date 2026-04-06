# Anthropic Claude Harness - Analysis Report

## 1. Document Overview

본 문서는 Anthropic이 2025년 11월부터 2026년 3월까지 4개월간 공개한 3개의 공식 엔지니어링 가이드를 시간순으로 정리한 자료이다. Claude Agent SDK를 활용한 장기 실행형 에이전트 하네스의 급속한 진화 과정을 기록하고 있으며, 단순함을 유지하면서도 context anxiety와 long-horizon 작업 안정성을 동시에 해결하는 방향으로 발전해왔다.

**핵심 하네스 진화 로드맵:**
- **2025.11**: Initializer + Coding Agent 2-단계 하네스 (초기 형태, context reset 기반 해결)
- **2026.01**: Eval harness 개념화 (하네스 자체를 평가하는 메타 시스템)
- **2026.03**: Planner + Generator + Evaluator 3-Agent GAN 스타일 (context reset 최소화, auto-compaction)

이 진화는 개인 로컬 AI 에이전트부터 기업 규모 협업 시스템까지 4가지 하네스 유형의 기초를 제공한다. 각 단계는 이전 단계의 한계점(context anxiety, artifact hand-off 복잡성, evaluator bias)을 직접 해결하는 형태로 설계되었다.

---

## 2. Analysis by Harness Type

### 2.1 Personal Local AI Agent Harness

#### 2.1.1 문서 기여도 및 적용 가치

본 문서는 개인 로컬 AI 에이전트 하네스 구축의 **기초 설계 패턴 3가지**를 제공한다:

1. **Initializer Agent Pattern (2025.11 기반)**
   - 첫 세션에서 환경 세팅 전담: `init.sh` 생성, progress log 초기화, git commit 수행
   - 이후 세션의 부담을 극적으로 경감하는 artifact hand-off 메커니즘
   - 개인 개발자가 즉시 적용 가능한 가장 실용적 패턴

2. **Coding Agent + Progress Log Pattern**
   - incremental progress tracking으로 multi-context window에서의 작업 연속성 보장
   - 각 세션 종료 시 `progress.md` 자동 갱신으로 다음 세션의 context 압축
   - Git commit을 작업 단위로 기록하여 롤백/추적 용이

3. **Eval Harness + Self-evaluation Pattern (2026.01-03 진화)**
   - 개인 에이전트 자신이 작업 품질을 자동 평가하는 메타 피드백 루프
   - skeptical evaluator로 self-praise bias 제거
   - long-running 프로젝트에서 표류(drift) 방지

#### 2.1.2 강점

| 강점 카테고리 | 구체적 내용 | 문서 근거 |
|:---|:---|:---|
| **Context 관리** | progress log와 artifact hand-off로 context anxiety 극복 가능 | 2025.11 "Context anxiety 문제를 context reset + hand-off로 해결" |
| **Git 연동** | 초기화 단계에서 git 초기화, 각 진행 단위마다 commit 수행 | 2025.11 "init.sh, progress log, git commit" |
| **장기 안정성** | multi-context window에서도 incremental progress 유지 | 2025.11 "이후 세션마다 incremental progress + artifact hand-off로 안정적" |
| **자동 평가** | 하네스 자체가 작업을 평가하는 메타 시스템 구현 가능 | 2026.01 "Agent harness와 Eval harness를 구분" |
| **Context Reset 최소화** | 3-agent GAN 스타일로 Opus 4.5 이후 수시간 연속 빌드 가능 | 2026.03 "context reset 없이 수시간 연속 빌드 가능" |

#### 2.1.3 약점 및 극복 방안

| 약점 | 원인 | 극복 방안 | 구현 복잡도 |
|:---|:---|:---|:---|
| **Multi-context 전환 오버헤드** | context reset 시 이전 맥락 손실 | progress.md + artifact hand-off로 상태 명시적 저장 | 낮음 |
| **Evaluator Bias** | Generator가 만든 결과를 자신이 평가할 때 과도하게 긍정적 평가 | skeptical evaluator agent 분리 (3-agent 구조) | 중간 |
| **Context Reset 빈도** | 초기 2-agent 구조에서는 여전히 reset 필요 | 3-agent GAN + automatic compaction 적용 | 높음 |
| **Artifact Hand-off 복잡성** | 세션 간 상태 전달이 불명확하면 작업 추적 곤란 | 명확한 artifact spec 정의 필요 (구현체 필요) | 중간 |
| **Local 리소스 제약** | 개인 로컬에서 장시간 실행 시 전력/네트워크 의존 | 문서에서 미언급 - 운영 정책 필요 | 미정 |

**극복 아키텍처 제안 (pseudocode):**

```python
class PersonalLocalAIHarness:
    """
    개인 개발자용 최소 구현 하네스 (v1.0)
    기반: 2025.11 Initializer + Coding + 2026.03 Eval Agent
    """

    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.progress_file = f"{project_dir}/progress.md"
        self.artifacts_dir = f"{project_dir}/.artifacts"

    def initialize_session(self):
        """첫 세션: 환경 세팅 (Initializer Agent)"""
        init_commands = [
            "git init",
            "git config user.email 'agent@local.dev'",
            "mkdir -p .artifacts",
            "echo '# Progress Log' > progress.md",
            "git add . && git commit -m 'init: Setup project structure'"
        ]
        for cmd in init_commands:
            execute_shell(cmd)

    def load_context_from_previous_session(self) -> dict:
        """이전 세션 artifact 복구"""
        if not exists(self.progress_file):
            return {}

        progress_content = read_file(self.progress_file)
        artifacts = {
            "last_commit": get_git_log(limit=1),
            "progress_summary": parse_progress_md(progress_content),
            "unfinished_tasks": extract_todos(progress_content)
        }
        return artifacts

    def execute_coding_task(self, task: str):
        """메인 작업: Coding Agent"""
        # 작업 진행
        pass

    def self_evaluate(self, work_result: str) -> dict:
        """평가: Eval Agent (skeptical mode)"""
        evaluation = {
            "quality_score": 0,  # 0-100
            "issues": [],        # 발견된 문제점
            "recommendations": []  # 개선 사항
        }
        # Evaluator prompt는 명시적으로 비판적 태도 강제
        return evaluation

    def save_artifacts_and_progress(self, work_summary: str):
        """세션 종료: artifact + progress 저장"""
        # progress.md 갱신
        append_to_file(self.progress_file, f"\n## Session {get_current_date()}\n{work_summary}")

        # git commit
        execute_shell("git add -A")
        execute_shell("git commit -m 'progress: {work_summary}'")
```

#### 2.1.4 실무 적용 단계

**Stage 1: 기본 하네스 (첫 1주)**
- Initializer Agent로 프로젝트 폴더 자동 구성
- Git + progress.md 기본 구조 수립
- 각 코딩 세션 후 progress 자동 업데이트

**Stage 2: Context 최적화 (1-2주)**
- artifact spec 정의 (파일 목록, 상태 변수, 키 메타데이터)
- progress.md에 "Last 5 commits" + "Unfinished tasks" 자동 기록
- 세션 시작 시 context window 사용량 추정 및 자동 압축

**Stage 3: Self-evaluation (2-3주)**
- Eval Agent 정의: "비판적으로 이전 작업 검토하기" prompt
- Quality threshold 설정 (예: 점수 < 70이면 재작업 권장)
- 반복 루프: Coding → Eval → Improvement

**Stage 4: Multi-agent Orchestration (선택 - 3-4주)**
- Planner Agent 추가: 작업 분해 및 일정 수립
- Generator + Evaluator 병렬화
- GAN-style 자동 개선 루프

---

### 2.2 Single Project Harness

#### 2.2.1 문서 기여도 및 적용 가치

단일 프로젝트 하네스는 개인 에이전트의 진화판으로, **팀 규모의 프로젝트(소규모 스타트업 1-2개 팀)에 최적화**된다. 문서의 3개 가이드 모두가 단일 프로젝트 맥락에서 논의되었으므로, 적용 가치가 높다.

**핵심 기여:**
- Initializer Agent가 프로젝트 전체 구조 세팅 가능 (개인 vs 팀 수준의 complexity 처리)
- Eval harness가 feature branch 머지 전 자동 검증
- 3-agent 구조로 프론트엔드 디자인 + 풀스택 코딩 동시 처리

#### 2.2.2 강점

| 강점 | 상세 | 근거 |
|:---|:---|:---|
| **스케일 최적화** | 개인 로컬과 달리 multi-agent 분산 실행으로 throughput 증가 | 2026.03 "Planner + Generator + Evaluator" 3-agent 설계 |
| **병렬 작업 처리** | 프론트엔드(subjective) + 풀스택 코딩(verifiable) 동시 진행 | 2026.03 "Frontend design과 full-stack coding을 동시에 처리" |
| **검증 가능성** | 풀스택 코딩은 테스트/실행으로 검증 가능, self-praise bias 제거 | 2026.03 "검증 가능한" 작업과 평가 분리 |
| **Context 안정성** | auto-compaction + multi-context window로 장시간 연속 작업 가능 | 2026.03 "context reset 없이 수시간 연속 빌드 가능" |
| **Artifact Hand-off 표준화** | 프로젝트 규모에서 hand-off spec이 중요 → 자동화 가능 | 2025.11 "artifact hand-off로 multi-context window에서도 안정적" |

#### 2.2.3 약점 및 극복 방안

| 약점 | 원인 | 극복 방안 |
|:---|:---|:---|
| **Agent 간 상태 동기화** | 3개 agent가 동시에 동작할 때 race condition 가능성 | Planner가 작업 스케줄 명시, Generator/Evaluator는 독립적 작업 영역 |
| **Frontend Design 검증 어려움** | 주관적 판단이라 자동 평가 곤란 | Evaluator prompt에서 "design consistency", "user experience principles" 등 객관화 |
| **Multi-context 복잡성** | 여러 agent의 context를 동시 관리 → 메모리/비용 증가 | Automatic compaction으로 각 agent의 context 독립 압축 |
| **프로젝트 변경 추적** | 여러 agent가 동시 수정 시 git conflict 가능 | 각 agent는 특정 파일/디렉토리만 담당 (role-based code ownership) |
| **평가 신뢰성** | Eval agent도 충분히 skeptical한가? | Eval agent prompt에 "반드시 3개 이상 문제점 찾기" 강제 |

**극복 아키텍처 제안:**

```python
class SingleProjectHarness:
    """
    단일 프로젝트용 3-Agent 하네스 (GAN 스타일)
    구성: Planner + Generator + Evaluator (2026.03 기반)
    """

    def __init__(self, project_root: str):
        self.project_root = project_root
        self.planner_context = {}
        self.generator_context = {}
        self.evaluator_context = {}
        self.shared_state = {
            "current_iteration": 0,
            "generated_artifacts": [],
            "evaluation_results": []
        }

    class PlannerAgent:
        """작업 분해 및 순서 결정"""
        def plan(self, feature_request: str) -> list:
            """
            feature_request를 분해하여 작업 순서 결정
            - 프론트엔드 mockup 설계
            - 백엔드 API 구현
            - 풀스택 통합
            - 테스트 작성
            """
            return [
                {"type": "frontend", "task": "Design mockup for feature X"},
                {"type": "backend", "task": "Implement API endpoints"},
                {"type": "integration", "task": "Connect frontend to backend"}
            ]

    class GeneratorAgent:
        """실제 코드/디자인 생성"""
        def generate(self, task: dict) -> dict:
            """
            Planner의 task를 받아 구현
            결과는 git branch에 commit
            """
            artifact = {
                "type": task["type"],
                "files_modified": [],
                "commit_hash": None,
                "description": None
            }
            return artifact

    class EvaluatorAgent:
        """생성 결과 평가 (skeptical mode)"""
        def evaluate(self, artifact: dict) -> dict:
            """
            Generator의 결과를 비판적으로 검토
            - 코드 스타일, 테스트 커버리지
            - 디자인 일관성, 접근성
            - 성능 요구사항 충족 여부

            반드시 1개 이상 문제점 도출
            """
            evaluation = {
                "passed": False,
                "issues": [],      # 반드시 1개 이상
                "improvements": []
            }
            return evaluation

    def iteration_loop(self, feature_request: str):
        """GAN-style 반복 루프"""
        iteration = 0
        max_iterations = 5

        plan = self.PlannerAgent().plan(feature_request)

        while iteration < max_iterations:
            # Generator: 계획에 따라 생성
            artifacts = []
            for task in plan:
                artifact = self.GeneratorAgent().generate(task)
                artifacts.append(artifact)

            # Evaluator: 모든 artifact 평가
            all_passed = True
            for artifact in artifacts:
                evaluation = self.EvaluatorAgent().evaluate(artifact)
                self.shared_state["evaluation_results"].append(evaluation)

                if not evaluation["passed"]:
                    all_passed = False
                    # 재생성을 위해 피드백을 Generator에 전달
                    artifact["feedback"] = evaluation["issues"]

            iteration += 1

            if all_passed:
                break

        return {
            "feature": feature_request,
            "iterations": iteration,
            "final_artifacts": artifacts,
            "success": all_passed
        }
```

#### 2.2.4 실무 적용 단계

**Stage 1: 기본 구조 (1주)**
- Git workflow: `main` (Planner 계획) → `feature/*` (Generator 작업) → `main` (Evaluator 검증 후 merge)
- Agent role 정의: Planner 프롬프트, Generator 프롬프트, Evaluator 프롬프트
- Artifact spec: 각 agent가 출력할 파일 형식 정의

**Stage 2: Agent 구현 (1-2주)**
- Planner: feature request → 작업 분해 (JSON 형식)
- Generator: 작업 → 코드/디자인 생성 (git commit)
- Evaluator: artifact → 평가 리포트 (markdown)

**Stage 3: 자동화 CI/CD 통합 (1주)**
- 각 feature 브랜치에서 Evaluator 자동 실행
- 평가 통과 시에만 PR 병합 허용
- 실패 시 피드백 + Generator 재실행

**Stage 4: Context 최적화 (진행 중)**
- shared_state에서 각 agent의 context 분리 저장
- auto-compaction: 각 agent는 관련 artifact만 유지
- long-running 프로젝트: multi-context window 활용

---

### 2.3 Team Collaboration Harness

#### 2.3.1 문서 기여도 및 적용 가치

문서는 직접적으로 "팀 협업 하네스"를 명시하지는 않으나, 다음 단계로의 확장성을 암시한다:

- 2026.01: "회사/팀 하네스 구축 시 자동 self-eval 시스템 설계 가이드라인"
- 2026.03: "팀 협업 시 multi-agent orchestration 기반"

**문서가 제공하는 협업 기초:**
1. Multi-agent orchestration의 개념 (Planner/Generator/Evaluator)
2. Self-eval 시스템이 팀 내 신뢰도 향상
3. Context reset 최소화로 장기 프로젝트 안정성

#### 2.3.2 강점

| 강점 | 상세 | 근거 |
|:---|:---|:---|
| **자동 평가로 인한 신뢰** | Eval agent가 자동으로 코드 검증 → human reviewer 부담 감소 | 2026.01 "Claude Code 자체를 예시로 long-running harness의 성공/실패 사례 분석" |
| **Multi-agent 병렬화** | 팀원들이 동시에 다양한 작업 수행 가능 | 2026.03 "3-agent GAN-style" |
| **Self-praise bias 제거** | skeptical evaluator로 과도한 긍정 평가 방지 | 2026.03 "skeptical evaluator로 self-praise bias 해결" |
| **Long-running 프로젝트 안정성** | context reset 최소화로 팀 프로젝트 지속성 보장 | 2026.03 "context reset 없이 수시간 연속 빌드 가능" |
| **투명한 평가 기준** | Evaluator prompt가 명확하면 팀 내 기준 일관성 | 2026.01-03 "Eval harness" 개념으로 평가 표준화 가능 |

#### 2.3.3 약점 및 극복 방안

| 약점 | 원인 | 극복 방안 |
|:---|:---|:---|
| **Human-in-the-loop 부재** | 문서에서 최종 approval flow 미언급 | Evaluator 평가 → Human reviewer 확인 → merge 의사결정 단계 추가 필요 |
| **팀 내 의견 충돌** | Generator의 설계 선택과 Evaluator의 기준이 충돌 가능 | 팀 워크숍: 코딩 컨벤션, 디자인 원칙 문서화 → Evaluator prompt에 반영 |
| **다중 팀 협업 복잡성** | 팀 A, B가 동시 작업 시 artifact 의존성 관리 곤란 | 계층적 orchestration: 팀 Level orchestrator 필요 (문서 미제시) |
| **비용 증가** | Agent 수 증가 = API call 증가 = 비용 증가 | Context compaction + 효율적 prompt 설계로 비용 제어 |
| **평가 신뢰도** | 자동 평가가 휴먼 기준을 완벽히 반영할 수 없음 | 자동 평가 + 통계 기반 샘플링 (10%는 human review) |

**극복 아키텍처 제안:**

```python
class TeamCollaborationHarness:
    """
    팀 협업용 확장 하네스
    구성: Planner → [Team 1, Team 2, ...] Generators 병렬 → Evaluator → Human Approval → Merger
    """

    def __init__(self, org_name: str):
        self.org_name = org_name
        self.teams = {}  # team_name -> Team instance
        self.global_standards = {
            "coding_style": "...",
            "design_principles": "...",
            "testing_requirements": "..."
        }

    class TeamGenerator:
        """각 팀이 담당할 작업 생성"""
        def __init__(self, team_name: str, domain: str):
            self.team_name = team_name
            self.domain = domain  # "backend", "frontend", "devops", etc.

        def generate(self, task: dict) -> dict:
            """
            팀의 domain에 맞는 작업 생성
            결과는 feature branch에 commit
            """
            pass

    class CentralizedEvaluator:
        """조직 전체 기준으로 평가"""
        def __init__(self, global_standards: dict):
            self.standards = global_standards

        def evaluate_team_output(self, team_artifacts: dict) -> dict:
            """
            다중 팀의 output을 종합 평가
            - 각 팀의 코드 품질
            - 팀 간 의존성 충돌 확인
            - 조직 표준 준수 여부
            """
            evaluation = {
                "team_evaluations": {},  # team_name -> result
                "integration_issues": [],  # 팀 간 충돌
                "overall_passed": False
            }
            return evaluation

    class HumanApprovalGateway:
        """최종 승인 (사람의 판단)"""
        def request_approval(self, evaluation: dict) -> bool:
            """
            자동 평가 결과를 PM/Tech Lead에게 제시
            - Evaluator가 "passed"면 확인만
            - Evaluator가 "failed"면 상세 검토 후 결정
            """
            # 실제 구현: Slack/Email로 approval 요청
            return True  # or False

    def full_workflow(self, feature_request: str):
        """팀 협업 전체 흐름"""
        # 1. Planner: 기능 분해 및 팀 할당
        plan = self.planner.plan(feature_request)  # returns task list with team assignments

        # 2. Multi-team Generation (병렬)
        team_artifacts = {}
        for team_name, tasks in plan.items():
            generator = self.TeamGenerator(team_name, domain=tasks[0]["domain"])
            artifacts = [generator.generate(task) for task in tasks]
            team_artifacts[team_name] = artifacts

        # 3. Centralized Evaluation
        evaluation = self.CentralizedEvaluator(self.global_standards).evaluate_team_output(team_artifacts)

        # 4. Human Approval
        approved = self.HumanApprovalGateway().request_approval(evaluation)

        # 5. Merge to main (if approved)
        if approved:
            self.merge_to_main(team_artifacts)
            return {"status": "merged", "feature": feature_request}
        else:
            return {"status": "rejected", "feedback": evaluation}
```

#### 2.3.4 실무 적용 단계

**Stage 1: 기본 팀 구조 (2주)**
- 팀별 domain 정의 (백엔드, 프론트엔드, DevOps)
- 조직 코딩 표준 문서화
- Evaluator prompt에 기준 명시

**Stage 2: 자동화 워크플로우 (2주)**
- CI/CD: feature branch → auto-test → evaluator → slack notification
- Multi-team orchestration: 팀 간 의존성 자동 감지
- Approval gateway: PM/Tech Lead에게만 "실패" 경우 알림

**Stage 3: 신뢰도 검증 (1-2주)**
- 자동 평가 vs 휴먼 평가 비교 분석
- 평가 일치도 < 80%이면 Evaluator prompt 개선
- 샘플링 기반 인스펙션 (전체 10%)

**Stage 4: 비용 최적화 (지속)**
- 각 team의 context 분리 저장
- auto-compaction으로 불필요한 history 제거

---

### 2.4 Company-wide Enterprise Harness

#### 2.4.1 문서 기여도 및 적용 가능성

문서는 직접적인 "엔터프라이즈 하네스" 명시는 없으나, 다음과 같은 지침을 제공한다:

> "회사/팀 하네스 구축 시 자동 self-eval 시스템 설계 가이드라인" (2026.01)
> "팀 협업 시 multi-agent orchestration 기반" (2026.03)

이를 조직 규모(수십 개 팀, 수백 개 마이크로서비스)로 확장하면 엔터프라이즈 하네스의 원칙을 도출할 수 있다.

#### 2.4.2 강점

| 강점 | 상세 | 근거 |
|:---|:---|:---|
| **표준화된 평가** | 조직 전체 Evaluator 기준 → 일관성 있는 품질 관리 | 2026.01 "하네스 자체를 평가하는 메타 시스템" |
| **자동 승인 흐름** | Evaluator 기준 충족 시 자동 merge → 배포 속도 향상 | 2026.03 "auto-compaction" 수단으로 속도 개선 |
| **Long-running 안정성** | context reset 최소화 기술로 장기 운영 안정성 | 2026.03 "context reset 없이 수시간 연속" → 수일/주 연속 운영 가능 |
| **다중 프로젝트 동시 진행** | 각 프로젝트가 독립적 harness 실행 → 상호 간섭 없음 | 2026.03 "3-agent" 개념을 조직 단위로 확장 |
| **감사 추적성** | 모든 decision(코드 생성, 평가, 승인)이 기록됨 | 2025.11 "git commit" 기반 투명성 |

#### 2.4.3 약점 및 극복 방안

| 약점 | 원인 | 극복 방안 |
|:---|:---|:---|
| **규정 준수 (Compliance)** | 문서에서 미언급. 금융/헬스케어 규제 대응 필요 | 평가 기준에 compliance 체크리스트 추가. Evaluator가 compliance 검증 |
| **다중 조직 정책 충돌** | 여러 부서의 정책이 상충할 수 있음 | 정책 우선순위 정의 + Evaluator hierarchy 구축 (global → dept → team) |
| **Vendor lock-in** | Anthropic Claude 단독 의존 → 위험 | 문서에서 미언급. 아키텍처: LangGraph 등 프레임워크로 추상화 필요 |
| **비용 폭발** | 수백 개 팀 × 다중 agent = 엄청난 API cost | auto-compaction + context 재사용으로 cost 제어. 모니터링 필수 |
| **평가 신뢰도 (규모 한계)** | 규모가 커질수록 자동 평가의 오류율 증가 | 계층적 approval: AI → team lead → director (규모에 따라) |

**극복 아키텍처 제안:**

```python
class EnterpriseHarness:
    """
    엔터프라이즈 규모 하네스 (수백 팀 규모)
    구성: Global Planner → [Department Orchestrators] → [Team Harnesses]
         → [Evaluators (multi-level)] → [Approval Gateway (hierarchical)]
    """

    def __init__(self, company_name: str):
        self.company = company_name
        self.departments = {}  # dept_name -> Department instance
        self.compliance_rules = {
            "security": [...],
            "privacy": [...],
            "performance": [...]
        }
        self.cost_monitor = CostMonitor()

    class GlobalPlanner:
        """회사 전체 전략 수준 계획"""
        def plan_quarters(self, business_goals: dict) -> dict:
            """
            분기별 business goal → 부서별 OKR → 팀별 작업 분해
            """
            pass

    class DepartmentOrchestrator:
        """부서 수준 조정"""
        def __init__(self, dept_name: str):
            self.dept_name = dept_name
            self.teams = {}

        def allocate_work(self, dept_goals: dict) -> dict:
            """
            부서 goal을 팀별로 분배
            팀 간 의존성 관리
            """
            pass

    class MultiLevelEvaluator:
        """다단계 평가 시스템"""
        def __init__(self, compliance_rules: dict):
            self.rules = compliance_rules
            self.evaluators = {
                "tech": TechnicalEvaluator(),
                "compliance": ComplianceEvaluator(rules),
                "security": SecurityEvaluator(rules),
                "performance": PerformanceEvaluator(rules)
            }

        def evaluate_artifact(self, artifact: dict) -> dict:
            """
            다차원 평가:
            1. 기술적 품질
            2. 규정 준수
            3. 보안
            4. 성능
            """
            results = {}
            for eval_type, evaluator in self.evaluators.items():
                results[eval_type] = evaluator.evaluate(artifact)

            return {
                "passed": all(r["passed"] for r in results.values()),
                "details": results
            }

    class HierarchicalApprovalGateway:
        """계층적 승인 (규모에 따라)"""
        def request_approval(self, artifact: dict, evaluation: dict) -> bool:
            """
            - Small change + all passed → auto-approve
            - Medium change + all passed → team lead approve
            - Large change or any failed → director review
            """
            if self.is_small_change(artifact) and evaluation["passed"]:
                return True  # Auto-approve
            elif self.is_medium_change(artifact):
                return self.team_lead_approve(artifact)
            else:
                return self.director_approve(artifact)

    class CostMonitor:
        """API 비용 모니터링"""
        def track_usage(self, dept: str, tokens_used: int):
            """
            부서별 token 사용량 추적
            임계값 초과 시 경고
            """
            pass

    def full_enterprise_workflow(self, business_goals: dict):
        """엔터프라이즈 전체 흐름"""
        # 1. Global planning
        quarterly_plan = self.GlobalPlanner().plan_quarters(business_goals)

        # 2. Department execution (병렬)
        for dept_name, dept_goals in quarterly_plan.items():
            dept = self.departments[dept_name]
            orchestrator = DepartmentOrchestrator(dept_name)

            # 2.1 Team-level work allocation
            team_assignments = orchestrator.allocate_work(dept_goals)

            # 2.2 Team harnesses execute (병렬)
            team_results = {}
            for team_name, tasks in team_assignments.items():
                harness = dept.get_team_harness(team_name)
                result = harness.execute(tasks)
                team_results[team_name] = result

            # 2.3 Multi-level evaluation
            evaluator = MultiLevelEvaluator(self.compliance_rules)
            for team_name, artifacts in team_results.items():
                evaluation = evaluator.evaluate_artifact(artifacts)

                # 2.4 Hierarchical approval
                approved = HierarchicalApprovalGateway().request_approval(
                    artifacts,
                    evaluation
                )

                if approved:
                    self.merge_to_production(artifacts)
                else:
                    self.request_rework(team_name, evaluation)

        # 3. Cost monitoring
        self.cost_monitor.report_summary()
```

#### 2.4.4 실무 적용 단계

**Stage 1: 기반 구축 (1개월)**
- Global Planner 설정: business goals → quarterly OKR
- Department orchestrators 정의
- Compliance rules 문서화

**Stage 2: 자동화 시스템 (2개월)**
- MultiLevel Evaluator 구현
- Hierarchical approval gateway 연동
- CI/CD 전사 표준화

**Stage 3: 모니터링 (지속)**
- Cost monitoring dashboard
- Evaluation accuracy tracking
- Auto-approval rate 통계

**Stage 4: 최적화 (분기별)**
- Context compaction 효율화
- Token 사용량 기반 prompt 최적화
- Evaluator 기준 개선 (feedback loop)

---

## 3. Multi-Perspective Technical Deep Dive

### 3.1 Architecture & Multi-agent Design

#### 3.1.1 진화 과정

**Stage 1: 2-Agent (2025.11)**
```
[Initializer Agent] → [Coding Agent] → (context reset) → [Coding Agent Session 2]
```
- 첫 세션: 환경 세팅 (git, progress log)
- 이후 세션: incremental coding
- 한계: context reset 빈번, session 간 context hand-off 복잡

**Stage 2: 3-Agent GAN (2026.03)**
```
┌─────────────┐
│   Planner   │ (작업 분해, 일정)
└──────┬──────┘
       │
       ├─→ ┌───────────┐
       │    │Generator  │ (코드 생성)
       │    └─────┬─────┘
       │          │
       └──────┬───┘
              │
         ┌────▼─────────┐
         │   Evaluator  │ (평가, feedback)
         └──────────────┘
```
- Planner: task 분해
- Generator: 병렬 구현
- Evaluator: 자동 평가 (skeptical mode)
- 이점: context reset 최소화, auto-improvement loop

#### 3.1.2 핵심 설계 원칙

| 원칙 | 설명 | 문서 근거 |
|:---|:---|:---|
| **Separation of Concerns** | 각 agent의 역할 명확 분리 | "Planner + Generator + Evaluator로 업그레이드" |
| **Parallel Execution** | 독립적 작업은 병렬 처리 | "Frontend design과 full-stack coding을 동시에" |
| **Automatic Compaction** | context 크기 자동 압축 | "automatic compaction" (문서) |
| **Skeptical Evaluation** | 비판적 평가로 bias 제거 | "skeptical evaluator로 self-praise bias 해결" |
| **Minimal Context Reset** | 세션 간 context 연속성 | "context reset 없이 수시간 연속" |

#### 3.1.3 실제 구현 패턴

**Planner Agent Prompt 템플릿:**
```
당신은 프로젝트 기획자입니다.
주어진 feature request를 다음 단계로 분해하세요:
1. 필수 선행 작업 (prerequisites)
2. 구현 순서 (implementation sequence)
3. 각 단계별 예상 소요 시간
4. 팀 간 의존성 (if multi-team)

JSON 형식으로 출력하세요:
{
  "feature": "...",
  "tasks": [
    {"id": "task-1", "type": "frontend", "title": "...", "depends_on": []},
    {"id": "task-2", "type": "backend", "title": "...", "depends_on": ["task-1"]}
  ],
  "estimated_hours": N
}
```

**Generator Agent Prompt 템플릿:**
```
당신은 숙련된 엔지니어입니다.
다음 작업을 구현하세요:

[Task Details from Planner]

요구사항:
1. 코드는 [회사 코딩 스타일] 준수
2. 단위 테스트 포함 (최소 80% coverage)
3. 변경사항은 명확한 git commit으로 기록
4. README 또는 주석으로 변경 내역 설명

완료 후 다음 정보를 JSON으로 제시하세요:
{
  "task_id": "...",
  "files_modified": [...],
  "tests_added": N,
  "coverage": "X%",
  "commit_message": "..."
}
```

**Evaluator Agent Prompt 템플릿:**
```
당신은 비판적인 code reviewer입니다.
다음 Generator 결과를 평가하세요:

[Artifact from Generator]

평가 기준:
1. 코드 품질 & 스타일: [회사 기준]
2. 테스트 완전성: [기준]
3. 성능 & 보안: [기준]
4. 문서화: [기준]

주의: 반드시 1개 이상의 개선점을 찾으세요.
자동 승인은 금지됩니다. 항상 비판적으로 검토하세요.

JSON 형식:
{
  "overall_passed": boolean,
  "score": 0-100,
  "issues": [
    {"severity": "critical|warning|info", "description": "..."}
  ],
  "improvements": ["...", "..."],
  "recommendation": "approve|rework|reject"
}
```

---

### 3.2 Context / State / Memory Management

#### 3.2.1 Context Anxiety Problem (문서)

> "Context anxiety 문제를 context reset + hand-off로 해결" (2025.11)

**문제 정의:**
- Claude의 context window는 유한 (최근 200K tokens)
- Long-running 프로젝트는 맥락이 커짐
- Context reset 시 이전 세션의 인텍트 손실

#### 3.2.2 해결 메커니즘

**Strategy 1: Progress Log (문서 기반)**
```markdown
# Progress Log

## Session 2026-04-03
- Completed: Feature X implementation (commit abc123)
- Current: Testing feature X
- Blocked: None

## Last 5 Commits
- abc123: feat: Implement feature X
- def456: test: Add unit tests for feature X
- ...

## Next Steps
1. Integration testing
2. Performance optimization
3. Documentation
```

- 각 세션 종료 시 자동 갱신
- 다음 세션 시작 시 이 파일을 context에 포함
- 문서 기반이므로 크기 제어 가능

**Strategy 2: Artifact Hand-off (구조화된 상태)**
```python
artifact = {
    "session": "session-2",
    "timestamp": "2026-04-03T14:30:00Z",
    "completed_tasks": [
        {
            "id": "task-1",
            "status": "completed",
            "output_files": ["src/feature.py"],
            "commit": "abc123"
        }
    ],
    "working_state": {
        "current_branch": "feature/X",
        "uncommitted_changes": []
    },
    "context_window_used": 145000,  # tokens
    "unfinished": [
        {
            "id": "task-2",
            "status": "in_progress",
            "progress": "50%",
            "notes": "Need to handle edge case..."
        }
    ]
}
```

- JSON 형식으로 상태 완전히 캡슐화
- 다음 세션에서 이를 파싱하면 현재 상태 복구
- 불필요한 history는 제외 (context 절약)

**Strategy 3: Automatic Compaction (문서)**

> "automatic compaction + skeptical evaluator" (2026.03)

- 각 세션의 context window 사용량 추적
- 반복되는 정보나 obsolete 정보 자동 제거
- multi-context window 환경에서 각 agent의 context 독립 관리

**실제 구현 예시:**
```python
class ContextManager:
    """
    Context 크기 제어 및 compaction
    """

    def __init__(self, max_tokens: int = 150000):
        self.max_tokens = max_tokens
        self.current_tokens = 0
        self.history = []

    def add_progress_log(self, log_content: str):
        """Progress log 추가"""
        tokens = len(log_content.split()) * 1.3  # 대략 estimate
        if self.current_tokens + tokens > self.max_tokens:
            # Compaction 필요
            self.compact_history()

        self.current_tokens += tokens
        self.history.append(log_content)

    def compact_history(self):
        """
        History compaction:
        - 7일 이상 된 session은 요약으로 압축
        - commit hash만 유지
        - 세부 내용은 git log에서 복구 가능
        """
        old_sessions = [h for h in self.history if is_older_than_7_days(h)]
        new_sessions = [h for h in self.history if not is_older_than_7_days(h)]

        # Old sessions → summarized version
        summary = summarize_sessions(old_sessions)

        self.history = [summary] + new_sessions
        self.current_tokens = estimate_tokens(self.history)

    def get_context_for_next_session(self) -> str:
        """
        다음 세션에 포함할 context 반환
        """
        return "\n".join(self.history)
```

---

### 3.3 Tool / Skills / Shell / Compaction / Filesystem Integration

#### 3.3.1 Tool Integration (Claude Agent SDK)

문서는 다음 integration point를 암시한다:

**1. Shell Execution (implicit)**
- init.sh 생성 및 실행 (Initializer)
- git commit 수행
- test 실행

**2. Git Integration (explicit)**
- "git commit" (문서 다수 언급)
- feature branch 관리 (단일/팀 프로젝트)
- commit 기반 감시 추적

**3. File System (explicit)**
- progress.md 생성 & 갱신
- artifact directory 관리
- 코드 파일 생성/수정

**4. Artifact Management**
- 이전 세션의 artifact 로드
- JSON 형식으로 구조화
- version 관리

#### 3.3.2 Skill System (암시적 확장)

문서에서 직접 언급하지 않으나, 다음과 같이 확장 가능:

```python
class Skill:
    """
    재사용 가능한 agent capability
    """

    @skill(name="git_operation")
    def handle_git(operation: str, args: dict):
        """
        git 작업 추상화
        - commit: message 필수
        - branch: create/switch/merge
        """
        pass

    @skill(name="test_execution")
    def run_tests(test_pattern: str = None):
        """
        테스트 실행 및 결과 수집
        """
        pass

    @skill(name="progress_tracking")
    def update_progress(summary: str, tasks: list):
        """
        Progress log 자동 갱신
        """
        pass
```

#### 3.3.3 Compaction 전략

**Lexical Compaction (크기 기반)**
```python
def compact_by_size(context: str, target_tokens: int) -> str:
    """
    Context를 target size로 압축
    전략:
    1. obsolete 정보 제거
    2. 반복되는 설명 통합
    3. 긴 error log → 요약
    """
    # 예: 1000줄의 test output → "Tests passed: 245/250"
    pass
```

**Temporal Compaction (시간 기반)**
```python
def compact_by_time(sessions: list, retention_days: int = 7) -> str:
    """
    오래된 session은 summarize
    - 7일 이상: commit list + summary
    - 최근 7일: 전체 정보
    """
    pass
```

---

### 3.4 Observability, Eval Harness, Approval Flow, Human-in-the-loop

#### 3.4.1 Eval Harness (문서의 핵심 개념, 2026.01)

> "Agent harness(실행 스캐폴드)와 Eval harness(평가 인프라)를 구분" (2026.01)

**Eval Harness vs Agent Harness:**

| 차원 | Agent Harness | Eval Harness |
|:---|:---|:---|
| **목적** | 실제 작업 수행 | 작업 결과 검증 |
| **입력** | Feature request | Generated artifact |
| **출력** | Code/design | Quality metrics, feedback |
| **Agent 역할** | Generator | Evaluator |
| **Context** | Task-focused | Evaluation criteria-focused |

**Eval Harness 구현 예시:**
```python
class EvalHarness:
    """
    AI-powered quality gate
    """

    def __init__(self, criteria: dict):
        self.criteria = {
            "code_quality": CodeQualityEvaluator(),
            "testing": TestingEvaluator(),
            "security": SecurityEvaluator(),
            "performance": PerformanceEvaluator()
        }

    def evaluate(self, artifact: dict) -> dict:
        """
        각 기준별로 평가
        """
        results = {}
        for criterion_name, evaluator in self.criteria.items():
            results[criterion_name] = evaluator.evaluate(artifact)

        return {
            "passed": all(r["passed"] for r in results.values()),
            "details": results,
            "evaluation_timestamp": now(),
            "confidence": calculate_confidence(results)
        }
```

#### 3.4.2 Approval Flow

**Basic Flow (문서 암시):**
```
Generator Output → Evaluator (auto) → Approval Decision → Merge
```

**Hierarchical Flow (기업 규모):**
```
Generator → Evaluator (tech)
         → Evaluator (compliance)
         → Evaluator (security)
         → Approval Gateway
            - Auto (all passed + small change)
            - Notify (all passed + medium change)
            - Review (any failed OR large change)
         → Merge
```

#### 3.4.3 Observability Requirements

문서에서 직접 언급하지 않으나, long-running agent를 운영하려면 필수:

**Metrics to Track:**
1. **Context Health**
   - Context window 사용률 (%)
   - Compaction 빈도
   - Hand-off 성공률

2. **Evaluation Quality**
   - Evaluator의 precision/recall (human review와 비교)
   - False positive rate
   - Evaluation time

3. **System Health**
   - Token consumption (비용)
   - Agent latency
   - Error rate

**구현 예시:**
```python
class ObservabilityCollector:

    def track_context(self, agent_name: str, tokens_used: int):
        """Context 사용량 기록"""
        metrics["context_usage"][agent_name] = {
            "timestamp": now(),
            "tokens": tokens_used,
            "percentage_of_max": tokens_used / max_context * 100
        }

    def track_evaluation(self, eval_result: dict):
        """평가 결과 기록"""
        metrics["evaluations"] = {
            "total": metrics["evaluations"]["total"] + 1,
            "passed": metrics["evaluations"]["passed"] + (1 if eval_result["passed"] else 0),
            "time_ms": eval_result["elapsed_ms"]
        }

    def alert_on_anomaly(self):
        """임계값 초과 시 알림"""
        if metrics["context_usage"] > 0.9 * max_context:
            alert("Context window high!")
```

---

### 3.5 Scalability, Cost Efficiency, Security, Vendor Lock-in Risk

#### 3.5.1 Scalability

**Horizontal Scaling (multi-agent):**
- 문서의 3-agent 패턴은 이미 병렬화 가능
- 더 많은 agent를 추가하려면 orchestrator 필요

**Vertical Scaling (single agent 강화):**
- Context window 증가 (최근 Claude 200K → 400K+)
- 더 강력한 모델 사용 (Opus > Sonnet > Haiku)

**Scaling Challenges (문서 미언급):**
- Multi-agent 간 동기화 오버헤드
- API rate limiting
- 비용 증가

#### 3.5.2 Cost Efficiency

**Token 절약 방법 (문서에서 추론):**

1. **Compaction**
   - obsolete history 제거
   - 요약 기반 저장
   - 예상 절약: 20-40%

2. **Caching**
   - 반복되는 prompt fragment 재사용
   - 평가 기준 document 한 번만 포함
   - 예상 절약: 10-20%

3. **모델 선택**
   - Evaluator는 Haiku (저비용, 충분)
   - Generator는 Opus (고품질)
   - Planner는 Sonnet (중간)
   - 예상 절약: 30-50%

**비용 추정 (가정):**
```
Opus 4.5: $3/1M input, $15/1M output
Sonnet: $3/1M input, $15/1M output  (같음)
Haiku: $0.80/1M input, $4/1M output

프로젝트 당:
- Planner: 10K input tokens (once) = $0.03
- Generator: 100K input + 50K output = $0.30 + $0.75 = $1.05
- Evaluator (Haiku): 100K input + 10K output = $0.08 + $0.04 = $0.12
- 합계: ~$1.50/iteration

월 300 iteration = $450
```

#### 3.5.3 Security

**문서에서 미언침 - 추론 필요:**

**Risk Areas:**
1. **API Key Exposure**
   - Agent가 소스 코드에 key 작성 위험
   - 해결: environment variable 검증

2. **Prompt Injection**
   - User input → agent prompt에 포함
   - 해결: input sanitization, prompt boundaries

3. **Artifact Tampering**
   - hand-off artifact 조작 가능성
   - 해결: artifact signing/hashing

4. **Code Execution**
   - Generated code가 악의적일 수 있음
   - 해결: sandboxed environment + static analysis

#### 3.5.4 Vendor Lock-in Risk

**주요 위험:**

| 위험 | 설명 | 극복 방안 |
|:---|:---|:---|
| **Model Unavailability** | Anthropic Claude 단독 의존 | LangChain/LangGraph로 추상화하여 다른 모델로 전환 가능하게 구조화 |
| **API 인터페이스 변경** | 향후 API 변경 시 코드 대량 수정 | adapter pattern 사용 |
| **가격 인상** | Anthropic이 가격을 올리면 수동 불가 | cost monitoring + alternative model 평가 프로세스 |
| **이용 약관 변경** | 특정 용도 금지 가능 | 계약 검토 필수 |

**Mitigation Strategy:**
```python
class AgentFactory(ABC):
    """
    모델에 무관한 agent 생성
    """

    @abstractmethod
    def create_planner(self) -> Agent:
        pass

    @abstractmethod
    def create_generator(self) -> Agent:
        pass

    @abstractmethod
    def create_evaluator(self) -> Agent:
        pass


class AnthropicAgentFactory(AgentFactory):
    """Anthropic Claude 기반 구현"""
    def create_planner(self):
        return ClaudeAgent(model="claude-opus-4.5", ...)


class OpenAIAgentFactory(AgentFactory):
    """OpenAI GPT 기반 구현 (미래)"""
    def create_planner(self):
        return OpenAIAgent(model="gpt-4o", ...)


# 사용
factory = AnthropicAgentFactory()  # or OpenAIAgentFactory()
planner = factory.create_planner()
```

---

## 4. Practical Recommendations for Our Harness Engineering Project

### 4.1 Immediate Next Steps (이번 주)

#### 4.1.1 문서 기반 학습
1. **3개 공식 문서 전문 읽기**
   - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
   - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
   - https://www.anthropic.com/engineering/harness-design-long-running-apps

2. **핵심 개념 정리**
   - Initializer + Coding + Evaluator 패턴
   - Context compaction 메커니즘
   - Skeptical evaluator의 정의

#### 4.1.2 PoC (Proof of Concept) 구현
**목표: 2주 내 v0.1 완성**

```python
# Step 1: 기본 하네스 스켈레톤
class SimpleHarness:
    def __init__(self, project_path):
        self.project = project_path

    def initialize(self):
        """Initializer Agent 역할"""
        # git init, progress.md 생성
        pass

    def execute_task(self, task_description):
        """Coding Agent 역할"""
        # task 실행, 결과 저장
        pass

    def evaluate(self, artifact):
        """Eval Agent 역할"""
        # 자동 평가
        pass

    def save_progress(self):
        """세션 종료 시 상태 저장"""
        # progress.md 갱신, git commit
        pass


# Step 2: 테스트
if __name__ == "__main__":
    harness = SimpleHarness("./test_project")
    harness.initialize()
    harness.execute_task("Implement feature X")
    harness.evaluate({...})
    harness.save_progress()
```

### 4.2 Framework Integration Points (1-2주)

#### 4.2.1 LangGraph와의 통합

LangGraph는 multi-agent workflow 구축을 위한 표준 프레임워크:

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# 우리의 3-agent flow를 LangGraph로 구현
workflow = StateGraph(AgentState)

# Nodes
workflow.add_node("planner", planner_node)
workflow.add_node("generator", generator_node)
workflow.add_node("evaluator", evaluator_node)

# Edges
workflow.add_edge("START", "planner")
workflow.add_edge("planner", "generator")
workflow.add_edge("generator", "evaluator")
workflow.add_conditional_edges(
    "evaluator",
    should_rework,  # 함수: evaluator 결과 → rework 필요 여부
    {
        "yes": "generator",  # Rework needed
        "no": END           # Success
    }
)

app = workflow.compile()
```

**이점:**
- 표준화된 orchestration
- 모니터링 지원
- multi-agent 상태 관리

#### 4.2.2 Grok Agent Tools API와의 통합

**가정:** Grok이 custom tool 정의를 지원한다면,

```python
# Grok 스타일 tool 정의
@grok.define_tool
def git_operation(operation: str, args: dict) -> dict:
    """
    Git 작업을 표준화된 way로 처리
    """
    pass

@grok.define_tool
def progress_tracker(summary: str, status: str) -> dict:
    """
    Progress tracking 자동화
    """
    pass
```

### 4.3 Risks & Mitigations (우리 프로젝트)

#### 4.3.1 주요 위험

| 위험 | 영향 | 대응 방안 |
|:---|:---|:---|
| **Context Reset 예측 어려움** | long-running 프로젝트 중단 가능성 | 초기 proto에서 context consumption 측정, scaling 법칙 수립 |
| **Evaluator Bias** | 자동 평가 신뢰성 저하 | 초반부터 skeptical prompt 강제, human review 샘플 비교 |
| **Multi-agent Deadlock** | 순환 의존성으로 진행 중단 | DAG 구조 강제, Planner가 순서 명시 |
| **비용 폭발** | 예산 초과 | token counting 자동화, cost alert 설정 |
| **Vendor Lock-in** | 향후 마이그레이션 어려움 | abstraction layer 초기부터 적용 |

#### 4.3.2 Best Practices (문서 기반)

1. **Progress Log 필수화**
   - 매 세션 종료 시 progress.md 갱신
   - git commit으로 히스토리 보존
   - 다음 세션에서 context의 첫 부분으로 포함

2. **Artifact Hand-off 표준화**
   - JSON schema 정의
   - version 관리
   - 손실 방지

3. **Evaluator의 엄격함 강제**
   - "항상 1개 이상 문제점 찾기" prompt
   - auto-approval 금지
   - human review 샘플링 (10%)

4. **Context Compaction 자동화**
   - session 단위로 크기 추적
   - 7일 이상 된 정보 요약
   - token 절약 target 설정 (예: 30%)

5. **Cost Monitoring**
   - 부서/팀/프로젝트별 비용 추적
   - monthly budget vs actual
   - alert system 구축

### 4.4 Short-term Roadmap (3개월)

**Month 1: Foundation**
- [ ] 문서 정독 & 핵심 개념 정리
- [ ] Simple 2-agent harness (Initializer + Coding) PoC
- [ ] Git + progress log integration
- [ ] Basic context compaction 구현

**Month 2: Enhancement**
- [ ] 3-agent harness로 업그레이드 (Planner, Generator, Evaluator)
- [ ] LangGraph 통합
- [ ] Multi-context window support
- [ ] Cost monitoring 자동화

**Month 3: Scale & Optimize**
- [ ] Multi-team orchestration 시작 (single project → team harness)
- [ ] Eval harness formalization
- [ ] Human-in-the-loop approval flow
- [ ] Enterprise readiness assessment

---

## 5. Summary & Key Takeaways

### 5.1 문서의 핵심 메시지

Anthropic의 3개 공식 문서가 제시하는 하네스 엔지니어링의 핵심은:

1. **Simplicity First**: 복잡한 orchestration보다는 명확한 역할 분리 (Planner/Generator/Evaluator)
2. **Context as First-Class Citizen**: context 관리 자체가 하네스 설계의 중심
3. **Automatic Improvement**: self-evaluation loop로 human review 부담 경감
4. **Evolutionary Design**: 2-agent → 3-agent 진화는 feedback을 받아 개선된 설계

### 5.2 우리 프로젝트에의 시사점

**즉시 적용 (이번 달):**
- progress.md 기반 context management
- Git 중심의 artifact hand-off
- 기본 2-agent 하네스

**중기 적용 (3개월):**
- 3-agent GAN 구조로 업그레이드
- LangGraph 기반 orchestration
- Multi-context window 활용

**장기 고려 (6개월+):**
- 팀/회사 규모 확장
- Compliance & security 강화
- Alternative model 평가 (vendor lock-in 완화)

### 5.3 기술 채무

**피해야 할 것:**
- Hard-coded prompt without abstraction
- Context management 없는 long-running agent
- Evaluator without skeptical bias control
- Vendor lock-in (Anthropic only)

**투자해야 할 것:**
- Abstraction layers (LangGraph, factory pattern)
- Comprehensive observability
- Automated cost monitoring
- Human-in-the-loop approval gates

---

**보고서 작성일**: 2026-04-03
**분석 기반 문서**: 01_anthropic_harness.md (Anthropic 공식 3개 문서 정리)
