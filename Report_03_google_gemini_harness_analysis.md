# Google Gemini ADK Harness - Analysis Report

## 1. Document Overview

본 문서는 Google이 2025년부터 2026년에 걸쳐 공개한 Agent Development Kit(ADK), Gemini 모델 시리즈의 agentic 기능 확장, 그리고 Skills 라이브러리의 발전 흐름을 시간순으로 정리한 공식 자료이다. Google의 하네스 엔지니어링 관점은 기존의 명시적 "harness" 용어보다는 **"model + framework의 통합 접근"**에 초점을 맞추고 있다: ADK라는 강력한 multi-agent orchestration 프레임워크, Gemini 모델의 Computer Use 능력, 그리고 재사용 가능한 Skills 라이브러리의 조합으로 production-grade long-running agent 시스템을 구축하는 것이다.

문서의 핵심은 2025년 초의 multi-agent 기초(ADK) → 2025년 10월의 실행 능력 강화(Computer Use) → 2026년의 실전화(Terminus-2 harness, Skills 라이브러리, Vertex AI 통합)라는 명확한 진화 단계를 보여준다. 각 단계는 "context 관리, tool orchestration, 상태 추적, 자동 평가"라는 하네스의 핵심 요소들을 점진적으로 강화하는 방향으로 설계되었다. Google의 접근은 Claude의 3-agent GAN-style delegation이나 OpenAI의 Codex harness처럼 "에이전트의 역할 분리"보다는, "하나의 모델이 여러 도구와 skills를 유연하게 조합하고 학습하는 방식"에 더 가깝다.

---

## 2. Analysis by Harness Type

### 2.1 Personal Local AI Agent Harness

#### 2.1.1 문서가 제공하는 구체적 가치와 적용 가능성

**Gemini 2.5 Computer Use 모델의 직접적 활용**

Google 문서에서 가장 직접적으로 개인 로컬 에이전트 구축에 기여하는 부분은 "Introducing the Gemini 2.5 Computer Use model (2025.10)"이다. 이 모델은:

- 브라우저, 모바일 UI를 직접 제어하는 능력 제공
- 낮은 지연시간으로 real-time 인터랙션 가능
- long-running agent의 "손" 역할을 담당

이는 개인 로컬 에이전트가 터미널/브라우저에 직접 명령을 내릴 수 있음을 의미한다. OpenAI의 hosted Shell과 달리, Computer Use 모델은 로컬에서도 실행 가능한 구조를 암시한다.

**ADK의 Multi-agent 기초 프레임워크**

"Making it easy to build multi-agent applications (2025.04)"에서 제시하는 ADK의 구조:

```
ADK의 기본 구조:
├─ LLM Agent (단순 LLM 호출 기반)
├─ Workflow Agent (사전 정의된 workflow 실행)
└─ Custom Agent (사용자 정의 로직)
```

개인 로컬 에이전트는 이 중 **LLM Agent + Custom Agent의 조합**으로 구성될 수 있다. 예를 들어:

- **LLM Agent**: Gemini 2.5 Computer Use 모델
- **Custom Agent**: Shell 명령 실행, Git 연동, 로컬 파일시스템 접근 로직

#### 2.1.2 강점 (context 관리, Git 연동, long-running session, self-eval, local deployment)

| 강점 영역 | 문서 근거 | 구체적 이점 |
|---------|---------|----------|
| **Context 관리** | ADK의 상태 관리, tool orchestration 추상화 | long-running session에서 context 손실 최소화, 자동 상태 추적 |
| **Tool Orchestration** | "ADK가 tool calling orchestration을 추상화" (2025.07) | Shell/Computer Use/파일 접근 등을 통일된 인터페이스로 제어 |
| **Computer Use 능력** | Gemini 2.5 Computer Use (2025.10) | 터미널·브라우저 직접 제어 가능 |
| **Self-evaluation** | Gemini 3.1 Pro의 SWE-Bench 고성능 (2026.02) | agent가 자동으로 작업 결과 평가 및 보정 가능 |
| **Long-running** | Terminus-2 harness (2026) | long-horizon task의 context 압축, memory 관리 최적화 |
| **Local Deployment** | ADK + Vertex AI의 model-agnostic 설계 | 로컬 또는 클라우드 유연한 배포 |

#### 2.1.3 약점 및 극복 방안

| 약점 | 근거 및 분석 | 극복 방안 |
|------|----------|---------|
| **명시적 Harness 문서 부족** | Google은 "harness" 용어를 공식으로 사용하지 않음 (ADK + Skills로 표현) | ADK의 agent orchestration을 harness의 context/state management로 재해석하여 적용 |
| **Local Computer Use의 제약** | Gemini 2.5 Computer Use는 주로 cloud 기반 설명. 로컬 실행 비용/지연 불명확 | OpenAI의 hosted Shell과 비교하여 비용-성능 trade-off 실험 필요 |
| **Skills 라이브러리의 도메인 편향** | "Evaluation harness로 117개 프롬프트 테스트"는 coding agent 중심 (2026.03) | 개인 에이전트의 다양한 use case(research, data analysis 등)에 맞는 custom skills 개발 필요 |
| **Self-correction의 reliability** | SWE-Bench에서 높은 성능도 실제 로컬 환경에서 오류 가능성 | Human-in-the-loop approval flow 필수 (self-eval + human review) |
| **Vertex AI 종속성** | Gemini 3.1 Pro의 enterprise deployment는 Vertex AI 기반 (2026.02) | 개인/로컬 사용 시 open-source 모델과의 호환성 검토 필요 |

#### 2.1.4 실무 적용 단계 (구체적 아키텍처 제안, pseudocode나 패턴 포함)

**아키텍처 제안**

```
┌─────────────────────────────────────────────────┐
│         Personal Local AI Agent Harness         │
└─────────────────────────────────────────────────┘
         │
         ├─ [Model Layer]
         │  ├─ Gemini 2.5 (Computer Use)
         │  └─ Gemini 3.1 Pro (self-correction)
         │
         ├─ [Orchestration Layer] - ADK
         │  ├─ LLM Agent (main reasoning)
         │  ├─ Custom Agent (tool routing)
         │  └─ State Management (context compression)
         │
         ├─ [Tool Layer]
         │  ├─ Computer Use (browser/terminal)
         │  ├─ Shell (local commands, Git)
         │  ├─ Filesystem (file read/write, Git clone)
         │  └─ Skills Library (reusable procedures)
         │
         ├─ [Evaluation Layer]
         │  ├─ Self-eval (model-based task verification)
         │  └─ Human approval (critical decisions)
         │
         └─ [Persistence Layer]
            ├─ Git (code/context versioning)
            ├─ Local DB (session history, metrics)
            └─ Logging (activity trace for debugging)
```

**Pseudocode: Personal Agent의 Main Loop**

```python
# Personal Local AI Agent Main Loop
# ADK + Gemini 2.5 Computer Use 기반

class PersonalLocalAgent:
    def __init__(self, model="gemini-2.5"):
        self.adk = ADK(model=model)
        self.computer_use = ComputerUseWrapper(model)
        self.shell_tool = ShellTool(local_only=True)
        self.git_tool = GitTool()
        self.context_manager = ContextManager(max_tokens=200000)
        self.evaluator = SelfEvaluator(model=model)

    def run_task(self, user_request: str) -> Result:
        """
        사용자 요청 → 작업 실행 → 자동 평가 → 결과 반환
        """
        # 1. Context 준비 (이전 session 기반 상태 복구)
        context = self.context_manager.load_or_init(user_request)

        # 2. ADK를 통한 multi-agent orchestration
        response = self.adk.run(
            user_request=user_request,
            agents=[
                LLMAgent(role="planner", model=self.adk.model),
                CustomAgent(role="executor", tools=[
                    self.computer_use,
                    self.shell_tool,
                    self.git_tool
                ]),
                LLMAgent(role="reviewer", model=self.adk.model)
            ],
            context=context
        )

        # 3. Self-evaluation (작업이 올바른지 모델 스스로 확인)
        eval_result = self.evaluator.evaluate(
            task=user_request,
            execution=response,
            context=context
        )

        # 4. 평가 결과에 따른 재시도 또는 Human-in-the-loop
        if eval_result.passed:
            result = Result(status="success", output=response)
        elif eval_result.needs_human_review:
            result = await self.human_approval_flow(
                task=user_request,
                execution=response,
                eval_reason=eval_result.reason
            )
        else:
            # 자동 재시도 (최대 N회)
            result = await self.retry_with_correction(
                user_request=user_request,
                context=context,
                previous_error=eval_result.error
            )

        # 5. Context 저장 및 Git 커밋
        self.context_manager.save(
            user_request=user_request,
            result=result,
            git_commit=True
        )

        return result

    def retry_with_correction(self, user_request, context, previous_error):
        """
        이전 오류를 context에 추가하여 재시도
        (Gemini 3.1의 multi-step task 능력 활용)
        """
        correction_context = context + f"\nPrevious error: {previous_error}\n"
        return self.run_task(user_request)
```

**패턴: Skills 기반 작업 분해**

Google의 "Closing the knowledge gap with agent skills (2026.03)"에서 제시하는 Skills 개념을 개인 에이전트에 적용:

```python
# Skills Library 패턴
class SkillsLibrary:
    """
    재사용 가능한 작업 패턴 관리
    Google의 Skills 라이브러리와 유사
    """

    @skill("git_analysis")
    def analyze_git_repo(self, repo_path: str) -> Dict:
        """
        Git 저장소 분석: commit 히스토리, branch 구조 등
        """
        tools_needed = [self.git_tool, self.shell_tool]
        return {
            "name": "git_analysis",
            "description": "Analyze repository structure and history",
            "required_tools": tools_needed,
            "prompt_template": """
            Analyze the git repository at {repo_path}:
            1. Count commits per author
            2. Identify main branches and recent merges
            3. Detect large files and potential refactoring points
            Return as JSON
            """
        }

    @skill("code_review")
    def review_code_diff(self, file_path: str) -> Dict:
        """
        코드 변경 리뷰
        """
        return {
            "name": "code_review",
            "description": "Review code changes for security and style",
            "required_tools": [self.shell_tool],
            "prompt_template": """
            Review the code at {file_path}:
            - Security issues
            - Style violations
            - Performance concerns
            - Suggest improvements
            """
        }

    @skill("research_and_summarize")
    def research_topic(self, topic: str) -> Dict:
        """
        웹 리서치 및 요약
        """
        return {
            "name": "research_and_summarize",
            "description": "Search web and summarize findings",
            "required_tools": [self.computer_use],
            "prompt_template": """
            Research the topic: {topic}
            1. Use browser to search
            2. Visit top 3-5 sources
            3. Extract key insights
            4. Summarize in < 500 words
            """
        }

# 실제 사용
agent = PersonalLocalAgent()
result = agent.run_skill("git_analysis", repo_path="/my/project")
```

**Context 압축 전략 (Terminus-2 harness 영감)**

문서의 "Terminus-2 harness (2026)"에서 암시하는 long-running context 관리:

```python
class ContextCompressor:
    """
    Long-running session의 context 최적화
    Gemini 3.1의 long-horizon task 능력 활용
    """

    def compress_old_context(self, context: Dict, max_age_hours: int = 24):
        """
        오래된 context는 요약하여 저장, 최근 context는 full detail 유지
        """
        summarized = {
            "original_size": len(context),
            "summary": self.model.summarize(context),
            "key_decisions": context.get("decisions", []),
            "open_issues": context.get("issues", [])
        }
        return summarized

    def reset_strategy(self, session_count: int):
        """
        매 N회 세션마다 hard reset 수행하여 context drift 방지
        """
        if session_count % 10 == 0:
            return "hard_reset"  # 완전 초기화
        elif session_count % 5 == 0:
            return "soft_reset"  # 최근 활동만 유지
        else:
            return "preserve"  # 현재 context 유지
```

---

### 2.2 Single Project Harness

#### 2.2.1 문서가 제공하는 구체적 가치와 적용 가능성

**ADK를 Backbone으로 한 프로젝트-수준 Workflow 구축**

"Build multi-agentic systems using Google ADK (2025.07)"은 실제 프로젝트에서 multi-agent workflow를 구축하는 방법을 제시한다. 핵심은:

- 상태 관리 (state management)
- Tool calling orchestration
- Gemini 모델 연동

이는 단일 프로젝트 내에서 여러 역할(planner, executor, reviewer)을 가진 에이전트들이 협력하는 구조를 의미한다.

**Git 연동 + Long-running Task의 실무 패턴**

프로젝트 하네스는 다음 기능이 필수:
- 코드 변경 추적 (Git)
- 작업 상태 저장 (세션 복구)
- 장기 작업 스케줄링 (CI/CD 통합)

**Skills 라이브러리의 프로젝트 맥락 적용**

"Closing the knowledge gap with agent skills (2026.03)"은 117개 프롬프트로 평가한 coding agent skills를 제시한다. 프로젝트 하네스는 이를 프로젝트별로 커스터마이징할 수 있다.

#### 2.2.2 강점 (다중 역할 에이전트, 상태 추적, Tool Orchestration)

| 강점 영역 | 문서 근거 | 구체적 이점 |
|---------|---------|----------|
| **계층적 Multi-agent** | "hierarchical delegation과 tool ecosystem" (2025.04) | Planner → Executor → Reviewer의 명확한 역할 분리 |
| **상태 관리** | "ADK가 상태 관리를 추상화" (2025.07) | 여러 에이전트 간 state 동기화, context 일관성 유지 |
| **Tool Orchestration** | ADK의 core feature | 다양한 도구(Shell, Git, LLM, 외부 API)를 통일된 방식으로 제어 |
| **Self-correction** | Gemini 3.1의 SWE-Bench 고성능 (2026.02) | 에이전트가 자동으로 오류 감지 및 재시도 |
| **Evaluation Harness** | "117개 프롬프트로 평가" (2026.03) | 작업 성능을 정량적으로 추적 가능 |
| **Scalability** | ADK + Vertex AI (2026) | 프로젝트 규모 확대 시 중앙 관리 가능 |

#### 2.2.3 약점 및 극복 방안

| 약점 | 근거 및 분석 | 극복 방안 |
|------|----------|---------|
| **기술 문서의 추상성** | ADK의 공식 문서가 "easy to build"에 초점. 실제 구현 세부사항 부족 | Google의 공식 예제 코드(github.com/google-gemini) 활용, 프로젝트별 pattern library 구축 |
| **Workflow 정의 복잡도** | multi-agent 시스템이 복잡할수록 상태 추적 어려움 | DAG (Directed Acyclic Graph) 기반 workflow 시각화 + state checkpoint 자동화 |
| **Tool 호환성** | Git, Shell 등 다양한 tool의 integration complexity | ADK의 tool interface 표준화 + wrapper pattern 적용 |
| **Error Recovery** | Self-correction이 항상 성공하지 않음 | Human-in-the-loop + automatic rollback 메커니즘 |
| **비용 최적화** | Gemini API 호출이 많을수록 비용 증가 | Context 압축, batch processing, caching 전략 필수 |

#### 2.2.4 실무 적용 단계

**프로젝트 하네스 아키텍처**

```
┌─────────────────────────────────────────────────────────┐
│       Single Project AI Agent Harness (ADK)             │
└─────────────────────────────────────────────────────────┘
         │
         ├─ [Project Context Layer]
         │  ├─ Project metadata (repo, tech stack, requirements)
         │  ├─ Git integration (commit history, branches)
         │  ├─ CI/CD pipeline state
         │  └─ Project-specific skills library
         │
         ├─ [Multi-Agent Orchestration] - ADK Core
         │  ├─ Planner Agent (작업 분해, 우선순위 결정)
         │  ├─ Executor Agent (코드 작성, 테스트 실행)
         │  ├─ Reviewer Agent (코드 리뷰, 품질 검증)
         │  └─ State Manager (상태 동기화, context 추적)
         │
         ├─ [Tool Layer]
         │  ├─ Git commands (clone, push, pull, merge)
         │  ├─ Shell execution (build, test, deploy)
         │  ├─ IDE integration (VSCode API, etc)
         │  ├─ Test framework (pytest, Jest, etc)
         │  └─ External APIs (package managers, bug trackers)
         │
         ├─ [Evaluation Layer]
         │  ├─ Unit test results
         │  ├─ Integration test results
         │  ├─ Code quality metrics (coverage, complexity)
         │  ├─ Performance benchmarks
         │  └─ Self-eval checklist (Gemini 3.1)
         │
         ├─ [Storage & Persistence]
         │  ├─ Git repository (code + history)
         │  ├─ Session state DB (checkpoint/recovery)
         │  ├─ Metrics DB (performance tracking)
         │  └─ Log aggregation (observability)
         │
         └─ [Human Interface]
            ├─ Approval workflow (critical changes)
            ├─ Monitoring dashboard
            └─ Alerts (errors, approval needed)
```

**Pseudocode: Project Harness Main Workflow**

```python
class ProjectHarness(ADK):
    """
    Single Project AI Agent Harness
    ADK를 기반으로 프로젝트-수준의 작업 자동화
    """

    def __init__(self, project_config: Dict):
        super().__init__(model="gemini-3.1-pro")
        self.project = ProjectContext.load(project_config)
        self.git = GitAgent(repo=self.project.repo_path)
        self.state_manager = ProjectStateManager(project=self.project)
        self.evaluator = ProjectEvaluator(project=self.project)

    def execute_feature_branch(self, feature_req: str) -> Result:
        """
        기능 요구사항 → 새 branch 생성 → 개발 → PR 생성 → 리뷰
        """

        # 1. Planner Agent: 작업 계획 수립
        plan = self.planner.decompose_task(
            task=feature_req,
            project_context=self.project
        )
        # plan = [
        #   {"step": 1, "action": "design_api", "tools": ["llm"]},
        #   {"step": 2, "action": "implement_feature", "tools": ["shell", "git"]},
        #   {"step": 3, "action": "write_tests", "tools": ["shell"]},
        #   ...
        # ]

        # 2. Git: 새 branch 생성
        branch_name = self.git.create_feature_branch(
            name=plan.feature_name,
            from_branch="main"
        )

        # 3. Executor Agent: 실제 구현
        for step in plan.steps:
            self.state_manager.checkpoint(step_num=step.step)

            execution = self.executor.run_step(
                step=step,
                branch=branch_name,
                project=self.project
            )

            # 동적 평가: 이 스텝이 성공했는가?
            eval = self.evaluator.check_step(
                step=step,
                execution=execution
            )

            if not eval.passed:
                # 자동 재시도 (최대 3회)
                execution = await self.retry_step(
                    step=step,
                    error=eval.error,
                    max_retries=3
                )

                if not execution.success:
                    # Human-in-the-loop: 개발자에게 승인 요청
                    await self.request_human_intervention(
                        step=step,
                        error=eval.error,
                        suggestion=execution.suggestion
                    )
                    break

        # 4. Reviewer Agent: 코드 리뷰
        review = self.reviewer.review_changes(
            branch=branch_name,
            base_branch="main"
        )

        # 5. Git: Pull Request 생성
        pr = self.git.create_pull_request(
            title=plan.pr_title,
            description=plan.pr_description + "\n" + review.summary,
            branch=branch_name,
            reviewers=review.suggested_reviewers
        )

        # 6. State 저장 및 결과 반환
        self.state_manager.save_feature_result(
            feature_req=feature_req,
            pr=pr,
            metrics=self.evaluator.final_metrics()
        )

        return Result(
            status="success",
            pr_url=pr.url,
            metrics=self.evaluator.final_metrics()
        )

    def continuous_improvement_loop(self, cron_schedule: str):
        """
        주기적으로 실행: 코드 품질 개선, 기술 부채 정리, 성능 최적화
        """
        while True:
            await wait_until(cron_schedule)

            # Skills 라이브러리 활용: 주기적 개선 작업들
            improvements = self.skills.run_batch([
                ("code_cleanup", {"repo": self.project}),
                ("dependency_update", {"repo": self.project}),
                ("performance_optimization", {"benchmark_target": "95th percentile"}),
                ("security_audit", {"strict_mode": True})
            ])

            for improvement in improvements:
                if improvement.recommended:
                    branch = self.git.create_branch(
                        name=f"auto-improve-{improvement.id}"
                    )

                    changes = self.executor.apply_improvement(
                        improvement=improvement,
                        branch=branch
                    )

                    if self.evaluator.validate_improvement(changes):
                        await self.request_human_approval(
                            improvement=improvement,
                            changes=changes
                        )
```

**Evaluation Harness 구현 (Skills 라이브러리 평가)**

Google의 "117개 프롬프트 테스트" 방식을 프로젝트에 적용:

```python
class ProjectEvaluationHarness:
    """
    프로젝트별 평가 하네스
    Google의 Skills 평가 방식을 참고
    """

    def __init__(self, project: ProjectContext):
        self.project = project
        self.test_suite = EvaluationTestSuite(
            total_cases=len(project.requirements),  # e.g., 117 cases
            categories={
                "correctness": "Does output match requirement?",
                "safety": "Are security checks performed?",
                "efficiency": "Is performance acceptable?",
                "maintainability": "Is code readable and documented?"
            }
        )

    def run_evaluation(self, agent_result: AgentOutput) -> EvalReport:
        """
        각 requirement에 대해 agent의 output 평가
        """
        report = EvalReport()

        for test_case in self.test_suite.cases:
            # 자동 평가: Gemini 모델로 채점
            auto_score = self.auto_eval(
                test_case=test_case,
                output=agent_result
            )

            # 수동 평가: Human reviewer (샘플링)
            if test_case.importance == "critical":
                manual_score = await self.human_eval(test_case, auto_score)
            else:
                manual_score = None

            report.add_result(
                test_case=test_case,
                auto_score=auto_score,
                manual_score=manual_score,
                status="pass" if auto_score >= 0.8 else "fail"
            )

        # 최종 요약: 통과율, 문제 영역 분석
        report.summarize()
        return report
```

---

### 2.3 Team Collaboration Harness

#### 2.3.1 문서가 제공하는 구체적 가치와 적용 가능성

**Multi-agent Orchestration의 팀 확장 형태**

"Making it easy to build multi-agent applications (2025.04)"에서 ADK의 "hierarchical delegation"과 "tool ecosystem" 개념은 팀 협업 시스템으로 직접 확장 가능하다:

- Planner Agent → 팀의 PM/Tech Lead 역할
- Executor Agent 수집 → 팀원들의 병렬 작업
- Reviewer Agent → 팀의 QA/Senior Engineer 역할

**상태 관리와 Tool Orchestration의 팀-수준 적용**

"Build multi-agentic systems using Google ADK (2025.07)"의 핵심인 "상태 관리"는 팀 협업에서 다음을 의미한다:

- 여러 사람이 동시에 작업할 때 conflict 방지
- Git merge 전략 자동화
- 작업 의존성 추적

#### 2.3.2 강점

| 강점 영역 | 문서 근거 | 구체적 이점 |
|---------|---------|----------|
| **병렬 작업 조율** | ADK의 hierarchical delegation | 여러 팀원이 동시에 작업. 의존성 자동 추적 |
| **충돌 자동 해결** | "상태 관리, tool calling orchestration" (2025.07) | Git merge 충돌 자동 감지 및 해결 제안 |
| **Skills 공유** | Skills 라이브러리 (2026.03) | 팀 전체가 재사용 가능한 작업 procedure 공유 |
| **분산 실행** | ADK + Vertex AI (2026) | 여러 팀이 동시에 agent 실행 가능. 중앙 관리 |
| **실시간 협업** | Computer Use + ADK | 팀원들이 동일한 작업 상태를 실시간 추적 |

#### 2.3.3 약점 및 극복 방안

| 약점 | 근거 및 분석 | 극복 방안 |
|------|----------|---------|
| **충돌 해결의 모호성** | Git merge 자동화는 ADK 문서에서 명시되지 않음 | 3-way merge + AI 기반 conflict resolver 직접 구현 |
| **팀원 간 권한 관리** | ADK는 단일 사용자 중심 설계 | Role-based access control (RBAC) + approval workflow 추가 |
| **실시간 동기화 비용** | 팀 규모 증대 시 상태 동기화 오버헤드 | 변경사항 배치 처리, event-driven architecture 적용 |
| **Human-in-the-loop 병목** | 중요 결정마다 팀원 승인 필요 → 지연 | 신뢰도 기반 자동 승인 정책 (e.g., 저위험 < 80%, 고위험 > 95%) |
| **Skills 라이브러리 버전 관리** | 여러 팀이 동시에 skills 수정 시 충돌 | Git 기반 skills versioning + semantic versioning |

#### 2.3.4 실무 적용 단계

**팀 협업 하네스 아키텍처**

```
┌────────────────────────────────────────────────────┐
│    Team Collaboration AI Agent Harness (ADK)       │
└────────────────────────────────────────────────────┘
         │
         ├─ [Team Context Layer]
         │  ├─ Team members & roles (PM, Engineer, QA, etc)
         │  ├─ Skills library (shared + team-specific)
         │  ├─ Shared repository & workflow
         │  ├─ Team metrics & KPIs
         │  └─ Approval policies & escalation rules
         │
         ├─ [Hierarchical Multi-Agent Orchestration]
         │  ├─ Team Coordinator Agent (작업 분배, 우선순위)
         │  ├─ Domain Expert Agents (각 팀원이 1개씩 담당)
         │  ├─ QA/Review Agent (품질 검증)
         │  ├─ Conflict Resolver Agent (merge 충돌 자동 해결)
         │  └─ State Synchronizer (팀 전체 상태 추적)
         │
         ├─ [Collaboration Tools]
         │  ├─ Git (분산 협업, merge 자동화)
         │  ├─ Issue tracker (작업 의존성, 진행 상황)
         │  ├─ Communication (Slack/email 통합)
         │  ├─ Code review (자동 + 수동)
         │  └─ Shared session storage (한 팀원의 작업을 다른 팀원이 이어받을 수 있도록)
         │
         ├─ [Conflict & Synchronization]
         │  ├─ Git conflict detection & AI resolution
         │  ├─ State consistency checker
         │  ├─ Rollback & checkpoint management
         │  └─ Event log (모든 변경사항 추적)
         │
         ├─ [Approval & Governance]
         │  ├─ Role-based access control (RBAC)
         │  ├─ Approval workflow (critical decisions)
         │  ├─ Audit trail (규정 준수 추적)
         │  └─ Risk assessment (변경의 영향 범위 분석)
         │
         └─ [Observability & Metrics]
            ├─ Team velocity (완료된 작업 수, 평균 시간)
            ├─ Quality metrics (버그 발견율, 리뷰 피드백)
            ├─ Agent performance (각 에이전트의 성공률)
            └─ Team dashboard (실시간 진행 상황)
```

**Pseudocode: Team Coordinator Agent의 작업 분배**

```python
class TeamCoordinatorAgent(ADK.Agent):
    """
    팀 전체의 작업을 조율하고 분배하는 agent
    Google ADK의 hierarchical delegation 패턴을 따름
    """

    def __init__(self, team: TeamContext):
        super().__init__(role="coordinator", model="gemini-3.1-pro")
        self.team = team
        self.team_members = team.get_members()
        self.conflict_resolver = ConflictResolverAgent()
        self.sync_manager = StateSyncManager(team=team)

    def distribute_feature_work(self, feature: FeatureRequest) -> WorkPlan:
        """
        팀에 작업을 분배하고 의존성을 관리
        """

        # 1. 요구사항 분석 및 task decomposition
        tasks = self.decompose_feature(feature)
        # tasks = [
        #   Task(id=1, name="API design", owner=None, depends_on=[]),
        #   Task(id=2, name="Frontend impl", owner=None, depends_on=[1]),
        #   Task(id=3, name="Backend impl", owner=None, depends_on=[1]),
        #   ...
        # ]

        # 2. 팀원의 skill과 현재 workload 고려하여 owner 할당
        assignments = self.assign_tasks_to_team(
            tasks=tasks,
            team_members=self.team_members,
            constraints={
                "max_parallel_tasks": 3,
                "expertise_match": True,
                "current_workload": self.get_team_workload()
            }
        )

        # 3. 작업 의존성을 DAG로 표현
        dag = self.build_dependency_dag(assignments)

        # 4. 각 팀원에게 작업 할당 (parallel + sequential ordering)
        work_plan = WorkPlan(
            feature=feature,
            tasks=assignments,
            dag=dag,
            parallel_groups=self.identify_parallel_groups(dag)
        )

        return work_plan

    def monitor_team_progress(self, work_plan: WorkPlan):
        """
        진행 중인 작업 모니터링 및 자동 조정
        """
        while not work_plan.is_complete():
            # 각 팀원의 agent가 동시에 작업 수행
            results = {
                member: member.agent.run_task(task)
                for member, task in work_plan.active_tasks.items()
            }

            for member, result in results.items():
                if result.status == "completed":
                    work_plan.mark_task_complete(result.task_id)
                    self.sync_manager.broadcast_completion(result)

                elif result.status == "blocked":
                    # 의존하는 task가 준비되지 않음 → 우선순위 재조정
                    self.reprioritize(work_plan, result.blocking_task)

                elif result.status == "conflict":
                    # Git merge 충돌 감지 → 자동 해결 시도
                    resolution = await self.conflict_resolver.resolve(
                        conflict=result.conflict,
                        branch_a=member.branch,
                        branch_b=result.merged_branch
                    )

                    if resolution.confidence < 0.8:
                        # 자신감 낮음 → human review 필요
                        await self.request_human_review(resolution)

            await asyncio.sleep(30)  # 30초마다 확인

    def handle_merge_conflicts(self, conflict: GitConflict) -> Resolution:
        """
        Git merge 충돌을 AI 기반으로 자동 해결
        """

        # Conflict resolver agent가 다음을 분석:
        # 1. 두 branch의 변경사항이 충돌하는 부분
        # 2. 코드의 semantic meaning (단순 라인 충돌이 아님)
        # 3. 팀의 coding style과 architecture 가이드

        resolution = self.conflict_resolver.analyze_and_resolve(
            conflict=conflict,
            team_style_guide=self.team.style_guide,
            architecture=self.team.architecture_doc
        )

        # 해결 방안의 신뢰도에 따라 자동 apply 또는 human review
        if resolution.confidence > 0.95:
            return resolution  # 자동 적용
        else:
            # 낮은 신뢰도 → 팀원에게 승인 요청
            approver = self.select_reviewer(
                conflict=conflict,
                expertise_needed=resolution.expertise_required
            )
            return await self.request_approval(resolution, approver)
```

**Skills 라이브러리의 팀 공유 패턴**

```python
class SharedSkillsLibrary:
    """
    팀 전체가 공유하는 작업 procedure 라이브러리
    Google의 Skills 라이브러리 (2026.03)를 팀 협업용으로 확장
    """

    def __init__(self, team: TeamContext):
        self.team = team
        self.repo = GitRepository(url="https://github.com/team/skills-lib")
        self.version_manager = SemanticVersioning()
        self.eval_harness = SkillEvaluationHarness(num_cases=117)

    @skill("code_review_checklist")
    def review_code_quality(self, pr_url: str) -> Dict:
        """
        팀 전체가 동일한 code review 기준을 적용하기 위한 skill
        """
        return {
            "name": "code_review_checklist",
            "team_version": "1.2.0",
            "checklist": [
                "Unit test coverage > 80%",
                "No security vulnerabilities (SCA scan)",
                "Follows architecture guidelines",
                "Performance acceptable (P99 latency < 100ms)",
                "Documentation updated",
                "No hardcoded secrets or credentials"
            ],
            "auto_eval": True,  # Gemini로 자동 평가
            "human_override": True  # 팀원이 수동으로 override 가능
        }

    @skill("integration_test")
    def test_feature_integration(self, feature_branch: str) -> Dict:
        """
        새로운 feature가 전체 시스템과 통합될 때의 테스트
        """
        return {
            "name": "integration_test",
            "team_version": "2.1.0",
            "steps": [
                "Deploy to staging environment",
                "Run full integration test suite",
                "Check performance regression (< 5%)",
                "Verify cross-team dependencies",
                "Load test (1000 concurrent users)"
            ]
        }

    def publish_skill(self, skill: Skill, bump_version: str = "patch"):
        """
        새로운 skill을 팀 라이브러리에 추가
        Semantic versioning 적용
        """
        new_version = self.version_manager.bump(
            current_version=skill.version,
            bump_type=bump_version
        )

        # 모든 팀원이 new skill을 평가
        eval_results = self.eval_harness.run(
            skill=skill,
            num_test_cases=117,
            reviewers=self.team.get_all_members()
        )

        if eval_results.passed_rate > 0.8:
            # 통과 → Git에 커밋, 모든 agent 업데이트
            self.repo.commit(
                skill=skill,
                version=new_version,
                eval_results=eval_results
            )
            self.broadcast_skill_update(skill, new_version)
        else:
            # 실패 → feedback 수집 후 개선
            feedback = eval_results.get_critical_feedback()
            await self.request_skill_improvement(skill, feedback)
```

---

### 2.4 Company-wide Enterprise Harness

#### 2.4.1 문서가 제공하는 구체적 가치와 적용 가능성

**Vertex AI 기반 Production-grade Deployment**

"Gemini 3.1 Pro Model Card & Agentic Capabilities (2026.02)"에서 강조되는 "Vertex AI와 ADK를 통해 enterprise-scale 배포 지원"이 회사 전체 하네스의 핵심이다:

- Multi-tenant architecture
- Cost 최적화 (batching, caching)
- 규정 준수 (audit trail, data governance)

**Terminus-2 Harness의 실전화**

문서의 "Terminus-2 harness (Terminal-Bench 평가용)"은 회사 수준의 평가 표준을 제시한다. 이는 여러 팀이 동일한 벤치마크로 agent 성능을 평가할 수 있음을 의미한다.

**Skills 라이브러리의 회사 표준화**

"Closing the knowledge gap with agent skills (2026.03)"의 117개 프롬프트 평가 체계는 회사 전체가 skills를 표준화하는 기반이 된다.

#### 2.4.2 강점

| 강점 영역 | 문서 근거 | 구체적 이점 |
|---------|---------|----------|
| **Vertex AI 통합** | "Vertex AI multi-agent 시스템" (2026) | 여러 팀의 agent가 중앙 관리됨. 비용 통제, 보안 강화 |
| **Standard Evaluation** | Terminus-2 harness + 117 test cases | 모든 팀이 동일한 기준으로 agent 성능 평가 |
| **Skills Standardization** | Google의 Skills 라이브러리 모델 | 회사 전체 best practices 공유 및 강제 |
| **Long-running Reliability** | Gemini 3.1의 long-horizon task 능력 | 일주일 이상의 자동화 작업도 가능 |
| **Cost Efficiency** | ADK의 context 압축, 배치 처리 | API 호출 수 최소화로 전체 비용 30-50% 감소 |
| **Security & Governance** | "Vertex AI의 audit trail" (암묵적) | 모든 agent 작업 추적, compliance 검증 용이 |

#### 2.4.3 약점 및 극복 방안

| 약점 | 근거 및 분석 | 극복 방안 |
|------|----------|---------|
| **Vendor Lock-in** | Google Gemini + Vertex AI에만 의존 | Open-source 모델 (LLaMA, Mistral) 병행. Multi-cloud 아키텍처 |
| **초기 Setup 복잡도** | Vertex AI, ADK, Skills 등 여러 component 통합 필요 | 회사 차원의 platform team이 reference architecture 제공 |
| **비용 예측 어려움** | long-running agent의 token 사용량 불확실 | Token 사용량 모니터링 + 자동 throttling 메커니즘 |
| **여러 팀의 우선순위 충돌** | 자원 할당 시 팀 간 경쟁 | 우선순위 큐 + SLA 기반 리소스 예약 |
| **Regulation 준수** | GDPR, HIPAA 등 각 팀의 규제 요구사항 다름 | 회사 차원의 compliance framework + team-specific overrides |
| **Skills 버전 관리** | 수백 개의 skills가 빠르게 변경됨 | Blue-green deployment + automatic rollback |

#### 2.4.4 실무 적용 단계

**회사 전체 하네스 아키텍처**

```
┌─────────────────────────────────────────────────────────────────┐
│    Company-wide Enterprise AI Agent Harness (Vertex AI)         │
└─────────────────────────────────────────────────────────────────┘
         │
         ├─ [Central Platform Layer] - Vertex AI
         │  ├─ Multi-tenant agent infrastructure
         │  ├─ Model management (Gemini 3.1 versioning)
         │  ├─ Resource allocation & quota management
         │  ├─ Cost tracking & billing
         │  └─ Central logging & observability
         │
         ├─ [Company-wide ADK Orchestration]
         │  ├─ Global coordinator (회사 차원의 작업 분배)
         │  ├─ Department level coordinators (각 팀의 coordinator)
         │  ├─ Shared resource manager (GPU, API quota 관리)
         │  ├─ Conflict resolution at enterprise scale
         │  └─ State synchronization across teams
         │
         ├─ [Centralized Skills Library]
         │  ├─ Core skills (모든 팀이 사용하는 기본 skills)
         │  ├─ Domain-specific skills (각 팀의 custom skills)
         │  ├─ Skill governance (approval, versioning)
         │  ├─ Skill evaluation harness (Terminus-2 based)
         │  └─ Skill marketplace & discoverability
         │
         ├─ [Enterprise Integration Points]
         │  ├─ HR system (employee info, org chart)
         │  ├─ Financial system (budget, cost tracking)
         │  ├─ Security system (SSO, encryption key management)
         │  ├─ Compliance system (audit trail, data retention)
         │  ├─ Analytics platform (metrics aggregation)
         │  └─ Communication platform (Slack, email, Jira)
         │
         ├─ [Multi-Tenant Isolation & Governance]
         │  ├─ Role-based access control (RBAC)
         │  ├─ Data isolation per team
         │  ├─ Budget enforcement & alerts
         │  ├─ Compliance policies (GDPR, HIPAA, SOC2)
         │  ├─ Audit trail (모든 작업, 승인, 예외사항 기록)
         │  └─ Security monitoring & threat detection
         │
         ├─ [Evaluation & Quality Assurance]
         │  ├─ Terminus-2 benchmark suite (표준 평가)
         │  ├─ Team-specific evaluation baselines
         │  ├─ Continuous performance monitoring
         │  ├─ Regression detection (성능 저하 자동 감지)
         │  ├─ A/B testing framework (새 모델/skills)
         │  └─ SLA monitoring (uptime, latency, accuracy)
         │
         ├─ [Cost Optimization]
         │  ├─ Request batching & caching
         │  ├─ Model selection optimization (언제 3.1 vs 2.5 사용)
         │  ├─ Context compression & memory management
         │  ├─ Usage analytics & anomaly detection
         │  └─ Budget forecasting & recommendations
         │
         └─ [Company Dashboard & Control Center]
            ├─ Executive view (전체 운영 상황)
            ├─ Team view (팀별 진행 상황)
            ├─ Agent view (개별 에이전트 성능)
            ├─ Cost view (팀별, 프로젝트별 비용)
            ├─ Alerts & notifications
            └─ Manual override & escalation interface
```

**Pseudocode: Enterprise Coordinator Agent**

```python
class EnterpriseCoordinatorAgent(ADK.Agent):
    """
    회사 전체의 AI agent 시스템을 조율하는 최상위 agent
    Vertex AI 기반 production-grade 배포
    """

    def __init__(self):
        super().__init__(
            role="enterprise_coordinator",
            model="gemini-3.1-pro",
            deployment="vertex_ai"
        )
        self.teams = self.load_all_teams()
        self.resource_manager = EnterpriseResourceManager()
        self.cost_controller = CostTracker()
        self.compliance_manager = ComplianceManager()
        self.skills_library = CentralSkillsLibrary()

    def orchestrate_company_operations(self):
        """
        회사 전체의 agent 활동을 조율
        각 팀의 coordinator는 이 enterprise coordinator 아래에 배치됨
        """

        # 1. 모든 팀의 agent로부터 진행 상황 수집
        team_statuses = {
            team: team.coordinator.get_status()
            for team in self.teams
        }

        # 2. 회사 차원의 자원 할당 및 우선순위 결정
        resource_allocation = self.resource_manager.allocate(
            requests=[status.resource_needs for status in team_statuses.values()],
            constraints={
                "total_api_budget": self.cost_controller.monthly_budget,
                "gpu_quota": self.resource_manager.total_gpus,
                "priority_policy": self.get_priority_policy()
            }
        )

        # 3. 각 팀의 coordinator에게 할당된 자원 분배
        for team, allocation in resource_allocation.items():
            team.coordinator.apply_allocation(allocation)

        # 4. 회사 차원의 cost 최적화
        optimization_results = self.optimize_company_costs(
            current_usage=self.cost_controller.get_current_usage(),
            skills=self.skills_library.get_all_skills()
        )
        # 예: "Developer Efficiency skill을 모든 팀에 배포하면 API 호출 20% 감소"

        if optimization_results.roi > 2.0:  # ROI가 2배 이상
            await self.deploy_optimization_to_all_teams(optimization_results)

    def optimize_company_costs(self, current_usage, skills):
        """
        회사 전체의 비용 최적화 기회 찾기
        """

        # 각 skill의 비용 효율성 분석
        efficiency_scores = {}
        for skill in skills:
            # Terminus-2 benchmark에서 skill의 quality score
            quality = self.eval_harness.get_score(skill)

            # skill 사용 시 평균 API 호출 수
            avg_tokens_before = self.get_avg_tokens_for_task(
                task_type=skill.applicable_task,
                using_skill=False
            )
            avg_tokens_after = self.get_avg_tokens_for_task(
                task_type=skill.applicable_task,
                using_skill=True
            )

            token_savings = avg_tokens_before - avg_tokens_after
            efficiency_scores[skill.id] = {
                "quality": quality,
                "token_savings": token_savings,
                "roi": token_savings / quality  # token 절감 대비 품질 유지
            }

        # ROI가 높은 skill부터 순서대로 배포 추천
        sorted_by_roi = sorted(
            efficiency_scores.items(),
            key=lambda x: x[1]["roi"],
            reverse=True
        )

        return {
            "efficiency_scores": efficiency_scores,
            "recommendations": sorted_by_roi[:5],  # 상위 5개 추천
            "potential_savings": sum(
                score["token_savings"]
                for _, score in sorted_by_roi
            ) * self.cost_per_token
        }

    def enforce_compliance_and_governance(self):
        """
        회사 차원의 규정 준수 및 거버넌스 강제
        """

        # 1. 모든 팀의 agent 작업 감시 (audit trail)
        audit_logs = self.compliance_manager.collect_all_agent_actions(
            time_range="last_24_hours"
        )

        # 2. 각 작업이 회사 정책 준수하는지 검증
        compliance_violations = []
        for log in audit_logs:
            violations = self.compliance_manager.check_policy_compliance(
                action=log,
                policies=[
                    "data_residency",  # 데이터 저장 위치 제약
                    "employee_privacy",  # 직원 정보 접근 제약
                    "financial_approval",  # 재정 관련 결정 승인 요구
                    "security_scanning"  # 배포 전 보안 검사
                ]
            )
            if violations:
                compliance_violations.append({
                    "action": log,
                    "violations": violations
                })

        # 3. 위반사항에 대한 자동 조치
        for violation in compliance_violations:
            if violation["violations"][0].severity == "critical":
                # 중요 위반 → 즉시 중단 + 관리자 alert
                team = violation["action"].owner_team
                team.coordinator.pause_all_agents()
                self.send_escalation_alert(violation)
            else:
                # 경미한 위반 → 로그만 기록, 정기 리포트
                self.compliance_manager.log_violation(violation)

    def manage_skill_library_at_scale(self):
        """
        회사 규모의 Skills 라이브러리 관리
        (Google의 Skills 라이브러리를 enterprise scale로 확장)
        """

        # 1. 새로운 skill이 전사 배포되기 전에 strict evaluation
        pending_skills = self.skills_library.get_pending_approval()

        for skill in pending_skills:
            # Terminus-2 기반 평가 (117 test cases)
            eval_results = self.eval_harness.run(
                skill=skill,
                num_cases=117,
                strict_mode=True  # 회사 레벨이므로 strict
            )

            # 평가 결과 요약
            summary = {
                "passed": eval_results.passed_rate,
                "quality_score": eval_results.quality_score,
                "security_review": eval_results.security_issues,
                "performance": eval_results.performance_regression
            }

            # 승인 기준: passed_rate > 95%, no security issues, < 5% perf regression
            if (summary["passed"] > 0.95 and
                summary["security_review"].is_clean and
                summary["performance"].regression < 0.05):

                # 자동 승인 + 모든 팀에 배포
                self.skills_library.approve_and_deploy(skill)
                self.broadcast_skill_deployment(skill)
            else:
                # 조건 미충족 → feedback 수집
                feedback = eval_results.get_detailed_feedback()
                await self.send_skill_improvement_request(skill, feedback)

    def handle_crisis_and_escalation(self):
        """
        회사 차원의 crisis 관리
        예: 특정 team의 agent가 오류를 일으키거나, API rate limit 도달
        """

        while True:
            # 각 팀의 coordinator로부터 escalation 확인
            escalations = [
                team.coordinator.get_pending_escalations()
                for team in self.teams
            ]

            for escalation in escalations:
                if escalation.severity == "critical":
                    # 1. 해당 팀의 모든 agent 일시 중단
                    escalation.team.coordinator.pause_all_agents()

                    # 2. 다른 팀으로부터 supporting agent 배치
                    support_team = self.find_supporting_team(
                        expertise_needed=escalation.required_expertise
                    )

                    if support_team:
                        support_agent = support_team.coordinator.allocate_agent(
                            priority="critical"
                        )
                        support_agent.help_resolve_crisis(escalation)

                    # 3. 회사 차원의 alert (executives)
                    self.send_critical_alert(escalation)

                elif escalation.severity == "high":
                    # Human review 필요
                    specialist = self.find_specialist(escalation.domain)
                    await self.notify_specialist(specialist, escalation)

            await asyncio.sleep(60)  # 1분마다 확인
```

**Terminus-2 Evaluation Harness 구현 (회사 표준)**

```python
class Terminus2EvaluationHarness:
    """
    Google의 Terminus-2 harness를 회사 전체의 평가 표준으로 채택
    """

    def __init__(self):
        self.test_suite = ComprehensiveTestSuite(
            total_cases=10000,  # Google의 Terminal-Bench 규모
            categories={
                "coding": {
                    "swe_bench": 500,  # SWE-Bench 문제들
                    "algorithm": 300,
                    "debugging": 200
                },
                "devops": {
                    "infrastructure": 300,
                    "deployment": 300,
                    "monitoring": 200
                },
                "data": {
                    "data_analysis": 300,
                    "sql": 300,
                    "ml_pipeline": 200
                },
                "business": {
                    "requirements_analysis": 200,
                    "product_strategy": 200
                }
            }
        )

    def evaluate_agent_performance(self, agent_id: str) -> PerformanceReport:
        """
        회사의 모든 agent는 동일한 Terminus-2 기준으로 평가됨
        """

        results = PerformanceReport()

        for category, test_cases in self.test_suite.items():
            for test_case in test_cases:
                # agent에게 test case 실행하도록 요청
                agent_output = self.run_agent_on_task(
                    agent_id=agent_id,
                    task=test_case
                )

                # Gemini 3.1으로 자동 평가
                auto_score = self.grade_output(
                    expected=test_case.expected_output,
                    actual=agent_output,
                    rubric=test_case.rubric
                )

                results.add(
                    category=category,
                    test_case=test_case,
                    score=auto_score
                )

        # 최종 종합 점수
        results.compute_overall_score()
        results.benchmark_against_company_average()

        return results
```

---

## 3. Multi-Perspective Technical Deep Dive

### 3.1 Architecture & Multi-agent Design

**ADK의 Multi-agent Orchestration 핵심**

Google 문서의 가장 핵심적인 기술은 ADK (Agent Development Kit)의 다음과 같은 설계이다:

```
ADK Architecture (from "Making it easy to build multi-agent applications"):

┌─────────────────────────────────────────────┐
│           ADK Framework                      │
├─────────────────────────────────────────────┤
│                                              │
│  ┌──────────────────────────────────────┐  │
│  │  Agent Types                         │  │
│  ├──────────────────────────────────────┤  │
│  │ - LLM Agent (단순 LLM 호출)           │  │
│  │ - Workflow Agent (사전정의 워크플로우)│  │
│  │ - Custom Agent (사용자 정의)         │  │
│  └──────────────────────────────────────┘  │
│           │                                 │
│           ├─ Orchestrator (hierarchical)   │
│           ├─ State Manager (공유 상태 관리)│
│           └─ Tool Registry (도구 등록)     │
│                                              │
│  ┌──────────────────────────────────────┐  │
│  │  Tool Ecosystem                      │  │
│  ├──────────────────────────────────────┤  │
│  │ - LLM Tool (Gemini 모델)             │  │
│  │ - Code Tool (Shell, Git)             │  │
│  │ - Web Tool (Computer Use)            │  │
│  │ - Custom Tool (회사 specific API)    │  │
│  └──────────────────────────────────────┘  │
│                                              │
└─────────────────────────────────────────────┘
```

**Hierarchical Delegation Pattern**

문서에서 "hierarchical delegation"과 "tool ecosystem 지원"이라고 명시하는 설계는 다음과 같이 구현될 수 있다:

```python
# Hierarchical Agent 구조
class Agent(ADK):
    def __init__(self, role: str, level: int):
        self.role = role  # "coordinator", "executor", "reviewer"
        self.level = level  # 계층 레벨 (낮을수록 상위)
        self.subordinates = []  # 하위 agent들
        self.tools = []  # 접근 가능한 도구들

    def delegate(self, task: Task) -> Result:
        """
        자신이 처리할 수 없는 task는 하위 agent에게 위임
        """
        if self.can_handle(task):
            return self.execute(task)
        else:
            # 적절한 subordinate agent 선택
            best_fit = self.select_best_subordinate(task)
            return best_fit.execute(task)
```

**State Management의 핵심: Shared Context**

"ADK가 상태 관리를 추상화한다"는 것은 여러 agent가 안전하게 공유 상태에 접근한다는 의미이다:

```python
class ADKStateManager:
    """
    여러 agent 간의 shared state 관리
    """

    def __init__(self):
        self.context = {}  # 모든 agent가 접근하는 공유 context
        self.locks = {}  # 동시 접근 방지

    def get_shared_context(self, agent_id: str) -> Dict:
        """
        agent가 필요로 하는 context만 조회 (권한 기반)
        """
        context = {}
        for key, value in self.context.items():
            if self.has_access(agent_id, key):
                context[key] = value
        return context

    def update_shared_context(self, agent_id: str, updates: Dict):
        """
        여러 agent가 동시에 context 업데이트할 때 conflict 방지
        """
        for key, value in updates.items():
            if self.has_access(agent_id, key):
                self.locks[key].acquire()
                self.context[key] = value
                self.locks[key].release()
```

### 3.2 Context / State / Memory Management

**Context 압축 전략 (Terminus-2 Inspiration)**

문서의 "Terminus-2 harness (2026)"는 long-running agent의 context를 어떻게 관리하는지 암시한다:

```python
class ContextCompressor:
    """
    장시간 실행되는 agent의 context를 최적화
    """

    MAX_CONTEXT_TOKENS = 200000  # Gemini의 context window
    COMPRESSION_THRESHOLD = 150000  # 이 수준에 도달하면 압축

    def compress_context(self, context: Dict) -> Dict:
        """
        오래된 정보는 요약, 최근 정보는 full detail 유지
        """

        current_size = self.estimate_tokens(context)
        if current_size < self.COMPRESSION_THRESHOLD:
            return context  # 압축 필요 없음

        # 시간 기준으로 context 분류
        old_context = {k: v for k, v in context.items()
                      if v.timestamp < (now - 24h)}
        recent_context = {k: v for k, v in context.items()
                         if v.timestamp >= (now - 24h)}

        # 오래된 부분 요약
        summary = self.model.summarize(old_context)

        # 최근 부분은 그대로 유지
        compressed = {
            "summary_of_old": summary,
            "recent": recent_context,
            "compression_timestamp": now
        }

        return compressed

    def reset_context_strategy(self, session_num: int) -> str:
        """
        주기적인 context reset으로 drift 방지
        """
        if session_num % 50 == 0:
            return "hard_reset"  # context 완전 초기화
        elif session_num % 10 == 0:
            return "partial_reset"  # 최근 정보만 유지
        else:
            return "incremental"  # 현재 context에 추가
```

**Memory Hierarchy**

실무 agent 하네스는 다음과 같은 memory 계층을 필요로 한다:

```
┌──────────────────────────────────────────┐
│      Memory Hierarchy in Agent Harness    │
├──────────────────────────────────────────┤
│                                          │
│  L0: Working Memory (현재 실행 중인 task) │
│      - 현재 작업에만 관련된 정보          │
│      - Size: ~ 100K tokens               │
│      - Lifetime: 현재 task만 유효         │
│                                          │
│  L1: Session Memory (진행 중인 세션)     │
│      - 한 session 내의 모든 작업          │
│      - Size: ~ 500K tokens               │
│      - Lifetime: 세션 종료 시까지         │
│                                          │
│  L2: Long-term Memory (project/team)    │
│      - 여러 세션에 걸친 누적 지식        │
│      - Size: 압축됨 (요약본)             │
│      - Lifetime: indefinite              │
│      - 저장소: Git, DB                   │
│                                          │
│  L3: Persistent Knowledge (회사 전체)   │
│      - Skills 라이브러리                 │
│      - Best practices, standards         │
│      - Size: Unlimited (외부 저장)      │
│      - 저장소: Central Skills Library    │
│                                          │
└──────────────────────────────────────────┘
```

### 3.3 Tool / Skills / Shell / Compaction / Filesystem Integration

**Tool Interface 표준화 (ADK 핵심)**

ADK는 다양한 tool들을 통일된 인터페이스로 제공한다:

```python
class Tool(ABC):
    """
    모든 tool이 구현해야 하는 표준 인터페이스
    """

    @abstractmethod
    async def execute(self, command: str, args: Dict) -> Result:
        """
        도구 실행
        """
        pass

    @abstractmethod
    def get_schema(self) -> Dict:
        """
        도구의 가능한 명령들과 입력/출력 스키마
        """
        pass

# 구체적 구현 예
class ShellTool(Tool):
    async def execute(self, command: str, args: Dict):
        process = subprocess.Popen(
            [command] + args.get("args", []),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await asyncio.to_thread(process.communicate)
        return Result(
            status="success" if process.returncode == 0 else "error",
            stdout=stdout,
            stderr=stderr,
            returncode=process.returncode
        )

class ComputerUseTool(Tool):
    async def execute(self, action: str, args: Dict):
        """
        Gemini 2.5 Computer Use 기반
        """
        response = await self.gemini.computer_use(
            action=action,  # "click", "scroll", "type", etc.
            coordinates=args.get("coordinates"),
            text=args.get("text")
        )
        return Result(status="success", screenshot=response.screenshot)

class GitTool(Tool):
    async def execute(self, command: str, args: Dict):
        """
        Git 명령 wrapper
        """
        repo = Repo(args.get("repo_path"))
        if command == "commit":
            repo.index.add(args["files"])
            repo.index.commit(args["message"])
        # ... other git commands
```

**Skills 라이브러리의 구조 (Google 2026.03 기반)**

문서에서 제시하는 Skills는 "117개 프롬프트"로 평가된다는 것은, 각 skill이 재현 가능한 procedure라는 의미이다:

```python
class Skill:
    """
    재사용 가능한 작업 procedure
    Google의 Skills 라이브러리 패턴
    """

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.required_tools = []  # 이 skill에 필요한 도구들
        self.prompt_template = ""  # skill을 구현하는 프롬프트
        self.evaluation_cases = []  # 평가용 테스트 케이스

    def get_prompt(self, **kwargs) -> str:
        """
        skill의 프롬프트 template에 변수 주입
        """
        return self.prompt_template.format(**kwargs)

    def get_required_tools(self) -> List[Tool]:
        """
        이 skill이 필요로 하는 도구 목록
        """
        return self.required_tools

# Skills 라이브러리 예시
class SkillLibrary:

    @skill("code_analysis", version="1.0")
    def analyze_python_code(self, file_path: str) -> Dict:
        """
        Python 코드를 분석하여 버그와 개선 사항 찾기
        """
        return Skill(
            name="code_analysis",
            required_tools=[ShellTool("pylint"), ShellTool("mypy")],
            prompt_template="""
            Analyze the Python code at {file_path}:
            1. Run pylint and mypy
            2. Identify potential bugs
            3. Suggest improvements for readability and performance
            4. Check for security vulnerabilities
            Return results as JSON
            """,
            evaluation_cases=[
                # 117개 평가 케이스 중 일부
                EvalCase(
                    input_code="def divide(a, b): return a / b",
                    expected_findings=["potential ZeroDivisionError"]
                ),
                # ... 더 많은 케이스
            ]
        )
```

**Filesystem 통합**

agent가 로컬 파일시스템에 접근하는 방식:

```python
class FilesystemAgent(Tool):
    """
    안전한 파일시스템 접근 (권한 기반)
    """

    def __init__(self, allowed_paths: List[str]):
        self.allowed_paths = allowed_paths

    async def execute(self, command: str, args: Dict) -> Result:
        # 1. 권한 확인
        path = args.get("path")
        if not self.is_allowed(path):
            return Result(status="error", error="Access denied")

        # 2. 명령 실행
        if command == "read":
            return await self.read_file(path)
        elif command == "write":
            return await self.write_file(path, args["content"])
        elif command == "list":
            return await self.list_directory(path)

    def is_allowed(self, path: str) -> bool:
        """
        path가 allowed_paths에 포함되는지 확인
        """
        normalized = os.path.normpath(path)
        return any(
            normalized.startswith(os.path.normpath(allowed))
            for allowed in self.allowed_paths
        )
```

### 3.4 Observability, Eval Harness, Approval Flow, Human-in-the-loop

**Observability 아키텍처**

실무 agent 하네스는 완벽한 추적성(observability)을 필수로 요구한다:

```
┌─────────────────────────────────────────────┐
│    Observability Stack for Agent Harness    │
├─────────────────────────────────────────────┤
│                                              │
│  ┌──────────────────────────────────────┐  │
│  │  Metrics                             │  │
│  ├──────────────────────────────────────┤  │
│  │ - Agent success rate (%)             │  │
│  │ - Average task duration (sec)        │  │
│  │ - Tool usage frequency               │  │
│  │ - API calls and costs                │  │
│  │ - Error rate and types               │  │
│  └──────────────────────────────────────┘  │
│           │                                 │
│           ├─ Prometheus (수집)             │
│           └─ Grafana (시각화)              │
│                                              │
│  ┌──────────────────────────────────────┐  │
│  │  Logging                             │  │
│  ├──────────────────────────────────────┤  │
│  │ - Agent decision trace (로직 추적)   │  │
│  │ - Tool execution logs                │  │
│  │ - Context snapshots (checkpoint)     │  │
│  │ - Error stack traces                 │  │
│  └──────────────────────────────────────┘  │
│           │                                 │
│           ├─ ELK Stack (수집/검색)         │
│           └─ CloudWatch (AWS)              │
│                                              │
│  ┌──────────────────────────────────────┐  │
│  │  Tracing                             │  │
│  ├──────────────────────────────────────┤  │
│  │ - Full request trace (사용자 요청 → 결과)│
│  │ - Latency breakdown (어디서 시간 소요?)│
│  │ - Dependency graph (agent 간 호출 흐름)│
│  └──────────────────────────────────────┘  │
│           │                                 │
│           ├─ Jaeger (분산 추적)            │
│           └─ OpenTelemetry (표준)         │
│                                              │
└─────────────────────────────────────────────┘
```

**Evaluation Harness (Terminus-2 Style)**

Google의 "117개 프롬프트 테스트" 방식을 일반화:

```python
class EvaluationHarness:
    """
    표준화된 평가 하네스
    """

    def __init__(self, test_suite_path: str, num_cases: int = 117):
        self.test_suite = self.load_test_suite(test_suite_path)
        self.num_cases = num_cases

    def evaluate_agent(self, agent_id: str) -> DetailedReport:
        """
        agent를 완벽히 평가
        """

        report = DetailedReport()

        for test_case in self.test_suite.cases[:self.num_cases]:
            # 1. 자동 평가 (Gemini로 채점)
            agent_output = self.run_agent(agent_id, test_case.input)

            auto_score = self.auto_grade(
                expected=test_case.expected_output,
                actual=agent_output,
                rubric=test_case.rubric
            )

            # 2. Human review (샘플링 또는 low-confidence 케이스)
            if auto_score < 0.7 or random.random() < 0.1:  # 10% 샘플링
                human_score = await self.request_human_review(
                    test_case=test_case,
                    agent_output=agent_output,
                    auto_score=auto_score
                )
                final_score = (auto_score + human_score) / 2
            else:
                final_score = auto_score

            report.add_result(
                test_case=test_case,
                auto_score=auto_score,
                human_score=human_score if 'human_score' in locals() else None,
                final_score=final_score
            )

        report.compute_aggregate_statistics()
        return report
```

**Approval Workflow 패턴**

critical decision은 반드시 human approval을 거쳐야 한다:

```python
class ApprovalWorkflow:
    """
    Human-in-the-loop approval flow
    """

    def __init__(self, notification_system):
        self.notification = notification_system
        self.approval_timeout = 3600  # 1시간

    async def request_approval(self,
                              action: str,
                              decision_details: Dict,
                              risk_level: str,
                              suggested_approver: str = None) -> bool:
        """
        action에 대한 approval 요청
        risk_level에 따라 timeout과 approver 결정
        """

        if risk_level == "critical":
            # 중요 결정: 상위자(manager/lead) 승인 필요
            approver = suggested_approver or self.find_manager()
            timeout = 300  # 5분 긴급
        elif risk_level == "high":
            # 높은 위험: 관련 팀 lead 승인
            approver = suggested_approver or self.find_team_lead()
            timeout = 3600  # 1시간
        else:
            # 낮은 위험: 자동 승인 (로그만 기록)
            return True

        # Approval 요청 발송
        approval_request = ApprovalRequest(
            action=action,
            details=decision_details,
            approver=approver,
            deadline=now + timedelta(seconds=timeout)
        )

        await self.notification.send(approval_request)

        # Approval 결과 대기
        result = await self.wait_for_approval(
            request_id=approval_request.id,
            timeout_seconds=timeout
        )

        if result.approved:
            self.log_audit_trail("approval_granted", approval_request)
            return True
        else:
            self.log_audit_trail("approval_denied", approval_request)
            return False
```

### 3.5 Scalability, Cost Efficiency, Security, Vendor Lock-in Risk

**Scalability 아키텍처**

개인 → 팀 → 회사 규모로 확대할 때의 설계:

```
Scalability Progression:

┌─────────────────────────────────────────────────────────┐
│  Level 0: Personal (1 agent)                           │
│  ├─ Single machine                                      │
│  ├─ Local execution                                     │
│  └─ Simple context management                          │
└─────────────────────────────────────────────────────────┘
         │ (팀 확장)
         ▼
┌─────────────────────────────────────────────────────────┐
│  Level 1: Small Team (5-10 agents)                     │
│  ├─ Shared Git repository                              │
│  ├─ Central state DB                                   │
│  ├─ Simple orchestration (ADK)                         │
│  └─ Manual approval for critical decisions             │
└─────────────────────────────────────────────────────────┘
         │ (조직 확장)
         ▼
┌─────────────────────────────────────────────────────────┐
│  Level 2: Department (20-100 agents)                   │
│  ├─ Multi-project support                              │
│  ├─ Distributed state management                       │
│  ├─ Advanced orchestration (ADK hierarchy)             │
│  ├─ Approval workflow automation                       │
│  ├─ Skills library management                          │
│  └─ Cost tracking & optimization                       │
└─────────────────────────────────────────────────────────┘
         │ (회사 확장)
         ▼
┌─────────────────────────────────────────────────────────┐
│  Level 3: Enterprise (100+ agents, multi-team)         │
│  ├─ Vertex AI cloud deployment                         │
│  ├─ Multi-tenant isolation                             │
│  ├─ Distributed agent orchestration                    │
│  ├─ Comprehensive governance & compliance              │
│  ├─ Enterprise Skills library                          │
│  ├─ Advanced cost optimization                         │
│  └─ High availability & disaster recovery              │
└─────────────────────────────────────────────────────────┘
```

**Cost Efficiency 전략**

실무 운영에서 비용은 가장 중요한 제약이다:

```python
class CostOptimizer:
    """
    API 호출 비용을 최소화하는 전략들
    """

    def optimize_requests(self, requests: List[Request]) -> OptimizationPlan:
        """
        Batch processing, caching, model selection 최적화
        """

        plan = OptimizationPlan()

        # 1. Batch processing: 여러 독립 요청을 한 번에 처리
        batches = self.group_independent_requests(requests)
        for batch in batches:
            cost_saving = len(batch) * 0.3  # 배치 처리 시 30% 비용 절감
            plan.add_optimization("batch_processing", cost_saving)

        # 2. Caching: 동일한 요청의 결과를 재사용
        cached_results = self.find_cacheable_requests(requests)
        for cached in cached_results:
            cost_saving = cached.cost * len(cached.similar_requests)
            plan.add_optimization("caching", cost_saving)

        # 3. Model selection: 복잡도에 따라 적절한 모델 선택
        #    (Gemini 2.5 < Gemini 3.1, 비용 고려)
        for request in requests:
            if request.complexity < "high":
                use_model = "gemini-2.5"  # 더 저렴
            else:
                use_model = "gemini-3.1"  # 더 강력하지만 비쌈
            plan.add_model_choice(request, use_model)

        # 4. Context compression: 불필요한 context 제거
        compressed_context = self.compress_context(requests)
        token_savings = requests.total_tokens - compressed_context.total_tokens
        plan.add_optimization("context_compression", token_savings)

        # 최종 비용 예상
        plan.compute_total_savings()

        return plan
```

**Security 고려사항**

agent가 시스템에 접근할 때의 보안:

```python
class SecurityLayer:
    """
    Agent의 행동을 감시하고 제한하는 보안 계층
    """

    def __init__(self):
        self.policy_engine = PolicyEngine()
        self.threat_detector = ThreatDetector()

    async def execute_with_security_checks(self,
                                           agent_id: str,
                                           action: str,
                                           args: Dict) -> Result:
        """
        모든 agent 명령을 실행 전에 검증
        """

        # 1. Policy 검증: agent가 이 action을 수행할 권한 있는가?
        if not self.policy_engine.is_allowed(agent_id, action, args):
            return Result(status="error", error="Access denied by policy")

        # 2. Threat 검증: 명령이 악의적이지는 않은가?
        threat_level = self.threat_detector.analyze(action, args)
        if threat_level == "critical":
            # 위협 차단
            await self.alert_security_team(agent_id, action)
            return Result(status="error", error="Action blocked due to security threat")

        # 3. 실행 및 감시
        result = await self.execute_monitored(agent_id, action, args)

        # 4. 감사 로그 기록
        self.audit_log.record(
            agent_id=agent_id,
            action=action,
            args=args,
            result=result,
            timestamp=now
        )

        return result
```

**Vendor Lock-in Risk 완화**

Google Gemini/Vertex AI에만 의존하는 위험을 줄이는 전략:

```python
class ModelAgnosticLayer:
    """
    여러 모델 제공자를 지원하는 abstraction layer
    """

    def __init__(self):
        self.providers = {
            "google": GoogleGeminiProvider(),
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "open_source": LocalLLMProvider()  # LLaMA, Mistral 등
        }

    async def inference(self, prompt: str, model_preference: str = None) -> str:
        """
        primary provider가 다운되면 자동으로 fallback
        """

        providers_to_try = []

        if model_preference:
            providers_to_try.append(self.providers[model_preference])

        # Fallback 순서: Google → OpenAI → Local
        providers_to_try.extend([
            self.providers["google"],
            self.providers["openai"],
            self.providers["open_source"]
        ])

        for provider in providers_to_try:
            try:
                result = await provider.inference(prompt)
                self.log_provider_usage(provider, success=True)
                return result
            except Exception as e:
                self.log_provider_usage(provider, success=False, error=e)
                continue

        # 모든 provider 실패
        raise Exception("All model providers failed")

    def estimate_cost(self, prompt: str, providers: List[str] = None) -> Dict:
        """
        각 provider의 비용 비교
        """
        if providers is None:
            providers = list(self.providers.keys())

        costs = {}
        for provider_name in providers:
            provider = self.providers[provider_name]
            cost = provider.estimate_cost(prompt)
            costs[provider_name] = cost

        return costs
```

### 3.6 Git / CI-CD / IDE / Local Filesystem Integration Potential

**Git Integration 패턴**

agent가 코드 저장소와 상호작용하는 방식:

```python
class GitIntegration:
    """
    Agent가 Git repository와 완전히 통합
    """

    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)

    async def create_feature_branch(self, feature_name: str, base: str = "main"):
        """
        새로운 feature에 대해 branch 생성
        """
        base_ref = self.repo.heads[base]
        new_branch = self.repo.create_head(f"feature/{feature_name}", base_ref)
        new_branch.checkout()
        return new_branch

    async def commit_changes(self, files: List[str], message: str, auto_sign: bool = False):
        """
        변경사항 커밋 (선택적으로 서명)
        """
        self.repo.index.add(files)
        if auto_sign:
            # GPG 서명 (보안)
            self.repo.index.commit(message, sign=True)
        else:
            self.repo.index.commit(message)

    async def create_pull_request(self, branch: str, title: str, description: str):
        """
        PR 자동 생성 (GitHub API)
        """
        from github import Github
        g = Github(self.github_token)
        repo = g.get_repo(self.repo_url)

        pr = repo.create_pull(
            title=title,
            body=description,
            head=branch,
            base="main"
        )

        return pr.url

    async def merge_with_conflict_resolution(self, pr_id: int):
        """
        Merge 충돌을 AI로 자동 해결
        """
        # 1. Merge 시도
        try:
            self.repo.heads.main.merge_base(self.repo.heads[pr_id])
            # ... merge logic
        except GitCommandError as e:
            # 2. Conflict 발견 → AI resolution
            conflicts = self.parse_merge_conflicts(e)

            for conflict in conflicts:
                # Gemini에게 어느 쪽이 맞는지 판단 요청
                resolution = await self.model.resolve_conflict(
                    conflict_file=conflict.file,
                    ours=conflict.ours,
                    theirs=conflict.theirs,
                    base=conflict.base,
                    context=self.get_code_context(conflict.file)
                )

                # Resolution 적용
                self.apply_resolution(conflict, resolution)

            # 3. 다시 merge
            self.repo.heads.main.merge(self.repo.heads[pr_id])
```

**CI/CD 통합**

agent가 CI/CD pipeline과 상호작용:

```python
class CICDIntegration:
    """
    GitHub Actions, GitLab CI, Jenkins 등과의 통합
    """

    def __init__(self, ci_platform: str):
        self.platform = ci_platform
        if platform == "github":
            self.api = GitHubActionsAPI()
        elif platform == "gitlab":
            self.api = GitLabCIAPI()

    async def trigger_pipeline(self, commit_sha: str, pipeline_type: str):
        """
        특정 commit에 대해 CI/CD 파이프라인 실행
        """
        workflow_file = {
            "test": ".github/workflows/test.yml",
            "build": ".github/workflows/build.yml",
            "deploy": ".github/workflows/deploy.yml"
        }[pipeline_type]

        return await self.api.trigger_workflow(commit_sha, workflow_file)

    async def wait_for_pipeline_completion(self, run_id: str, timeout: int = 3600):
        """
        파이프라인 완료까지 대기
        """
        start = now()
        while True:
            status = await self.api.get_pipeline_status(run_id)

            if status.completed:
                return status

            if (now() - start).seconds > timeout:
                raise TimeoutError(f"Pipeline did not complete within {timeout}s")

            await asyncio.sleep(10)

    async def get_pipeline_logs(self, run_id: str) -> str:
        """
        파이프라인 로그 조회 (debugging)
        """
        return await self.api.get_logs(run_id)
```

**IDE Integration Potential**

Visual Studio Code 등과의 통합:

```python
class IDEIntegration:
    """
    IDE 플러그인을 통해 agent 제어
    """

    def __init__(self, ide: str):
        self.ide = ide  # "vscode", "jetbrains", etc.

    def register_code_lens(self):
        """
        코드 라인 위의 CodeLens로 agent 기능 제공
        예: "Ask AI to refactor this function"
        """
        if self.ide == "vscode":
            return {
                "codeLens": {
                    "refactorCommand": "Ask AI to refactor",
                    "explainCommand": "Ask AI to explain",
                    "generateTestCommand": "Generate tests"
                }
            }

    def enable_inline_suggestions(self):
        """
        실시간 제안 (코드 작성 중)
        """
        return {
            "inlineCompletion": True,
            "suggestionModel": "gemini-3.1-pro",
            "updateFrequency": "real_time"
        }
```

---

## 4. Practical Recommendations for Our Harness Engineering Project

### 4.1 Actionable Next Steps (지금 바로 할 수 있는 것들)

**Phase 1: Foundation (1-2주)**

1. **ADK 프로토타입 구현**
   - Google ADK 공식 예제로 시작 (github.com/google/adk)
   - LLM Agent + Custom Agent 기본 구조 구축
   - Gemini 3.1 Pro API로 테스트

2. **Git Integration 자동화**
   - GitPython 또는 pygit2를 사용한 기본 branch/commit 기능
   - PR 생성 자동화 (GitHub API)
   - 간단한 merge conflict 자동 해결 로직 (정규식 기반, AI 아직 아님)

3. **Context Management 기초**
   - Session 저장/복원 메커니즘 (JSON 기반)
   - 간단한 context 압축 (오래된 항목 요약)

**Phase 2: Core Features (2-3주)**

1. **Self-evaluation 통합**
   - Gemini 모델로 작업 결과 자동 평가
   - 평가 결과에 따른 자동 재시도 로직
   - Human-in-the-loop approval workflow

2. **Skills 라이브러리 초안**
   - 공통 작업 5-10개를 skill로 정의
   - 각 skill을 프롬프트 + tool 조합으로 구현
   - 간단한 evaluation harness (10-20 test cases)

3. **Observability**
   - 기본 로깅 (모든 agent 행동 기록)
   - 간단한 메트릭 수집 (성공률, 평균 시간)
   - 대시보드 (Streamlit 또는 Flask 간단 버전)

**Phase 3: Scale-up (3-4주)**

1. **Multi-agent Orchestration**
   - ADK의 hierarchical agent 구현
   - 병렬 작업 및 의존성 관리
   - State synchronization across agents

2. **Advanced Git Features**
   - AI 기반 merge conflict resolution (Gemini 활용)
   - Automated code review (기본)
   - 자동 PR 댓글 (피드백)

3. **Skills Evaluation at Scale**
   - 117 test cases 기반 평가 (Google Terminus-2 참고)
   - 팀 전체가 skills 공유하는 메커니즘
   - Version management (semantic versioning)

### 4.2 Integration with Grok Agent Tools API / LangGraph / Other Frameworks

**Grok Agent Tools API와의 호환성**

문서에서 명시되진 않았지만, Google ADK의 개념을 Grok이나 LangGraph과 연결할 수 있다:

```python
# Grok Agent Tools API로 ADK 구현
from grok import Agent, Tool, State

class ADKCompatibleGrokAgent(Agent):
    """
    Google ADK 패턴을 Grok 위에서 구현
    """

    def __init__(self, role: str):
        super().__init__()
        self.role = role
        self.tools = self.register_tools()

    def register_tools(self) -> List[Tool]:
        """
        ADK의 tool ecosystem을 Grok Tool로 변환
        """
        return [
            Tool(
                name="shell",
                func=self.shell_tool,
                description="Execute shell commands"
            ),
            Tool(
                name="git",
                func=self.git_tool,
                description="Execute git operations"
            ),
            Tool(
                name="computer_use",
                func=self.computer_use_tool,
                description="Control browser/UI"
            )
        ]

    async def execute_with_adk_pattern(self, task: str) -> Result:
        """
        ADK의 orchestration 패턴을 Grok 에이전트에 적용
        """

        # 1. Task decomposition (planning)
        plan = await self.plan_task(task)

        # 2. State management
        state = State()

        # 3. Sequential/parallel execution
        for step in plan.steps:
            result = await self.execute_step(step, state)
            state.update(step.id, result)

        return result
```

**LangGraph와의 통합**

LangGraph는 node-based workflow를 지원하므로, ADK의 계층적 delegation을 구현할 수 있다:

```python
from langgraph.graph import StateGraph

# LangGraph로 ADK의 multi-agent 구조 표현
def create_adk_workflow():
    """
    LangGraph로 ADK의 hierarchical agent pattern 구현
    """

    graph = StateGraph(AgentState)

    # Nodes: 각 agent를 node로 표현
    graph.add_node("planner", plan_task_node)
    graph.add_node("executor", execute_task_node)
    graph.add_node("reviewer", review_result_node)

    # Edges: agent 간의 흐름
    graph.add_edge("START", "planner")
    graph.add_conditional_edges(
        "planner",
        route_to_executor,  # Plan 결과에 따라 routing
        {"execute": "executor", "delegate": "coordinator"}
    )
    graph.add_edge("executor", "reviewer")
    graph.add_conditional_edges(
        "reviewer",
        route_reviewer_decision,
        {
            "approved": "END",
            "needs_revision": "executor",
            "escalate": "human_review"
        }
    )

    return graph.compile()
```

### 4.3 Potential Risks and Best Practices

**위험 1: Context Window 초과**

- **위험**: Long-running task에서 context가 점점 커져 모델의 context window 초과
- **대응**:
  - 정기적인 context compression (매 10 task마다)
  - Sliding window 방식 (최근 N개 작업만 유지)
  - External memory store 활용 (Git, DB)

**위험 2: AI의 자동 결정 신뢰도**

- **위험**: Agent가 자동으로 내린 결정이 잘못될 수 있음 (자신감 있게 틀림)
- **대응**:
  - Self-evaluation 신뢰도 threshold 설정 (< 80%일 때만 human review)
  - Critical decisions는 항상 human review (비용 감수)
  - Diverse reasoning (여러 관점에서 평가)

**위험 3: API 비용 폭발**

- **위험**: 많은 agent가 동시에 실행되면서 API 호출 급증
- **대응**:
  - Budget 제한 (월별 quota 설정)
  - Batch processing (요청 그룹화)
  - Caching (동일 요청 결과 재사용)
  - Rate limiting (시간당 호출 수 제한)

**위험 4: Security & Data Leakage**

- **위험**: Agent가 민감한 정보에 접근하거나 외부로 유출
- **대응**:
  - Fine-grained access control (어떤 파일/API에만 접근 가능)
  - Data masking (민감 정보 자동 마스킹)
  - Audit trail (모든 접근 기록)
  - Encryption (저장된 context는 암호화)

**위험 5: Vendor Lock-in**

- **위험**: Google Gemini/Vertex AI에만 의존하면 향후 이전 어려움
- **대응**:
  - Model-agnostic abstraction layer 설계
  - Open-source 모델도 지원 (fallback)
  - Multi-cloud 아키텍처 고려

**Best Practices**

1. **Checkpoint & Recovery**
   - 모든 중요 단계마다 상태 저장
   - 오류 발생 시 마지막 checkpoint에서 복구

2. **Gradual Rollout**
   - 새로운 skill이나 agent는 작은 그룹부터 시작
   - 성공 메트릭이 안정화되면 확대

3. **Monitoring & Alerting**
   - 실시간 모니터링 (에러율, API 비용)
   - 이상 현상 자동 감지 및 alert

4. **Documentation & Knowledge Sharing**
   - 각 skill의 용도, 한계, 비용 문서화
   - 팀 전체가 best practices 공유

5. **Continuous Evaluation**
   - 매달 agent 성능 재평가
   - 새로운 모델 버전 테스트 (A/B testing)

---

## 5. 최종 결론 및 통합 관점

### 5.1 Google ADK/Gemini의 하네스 엔지니어링 철학

Google의 접근은 다음 3가지 핵심을 강조한다:

1. **Framework First (ADK)**: 명시적 "harness" 용어보다는, 모델-agnostic한 **orchestration framework** (ADK) 제공
2. **Model Agility (Gemini 시리즈)**: 단일 모델이 계속 강화되는 것이 아니라, 상황에 맞는 모델 선택 (2.5 vs 3.1, Computer Use vs standard)
3. **Skill as Primitive (Skills Library)**: 재사용 가능한 "skill"을 기본 단위로, 평가 체계 (117 test cases)와 함께 제공

### 5.2 우리 Harness Engineering 프로젝트에의 시사점

| 관점 | Google의 교훈 | 우리의 액션 |
|------|-----------|----------|
| **Architecture** | ADK의 hierarchical agent + state management | 동일한 패턴을 LangGraph/Grok으로 구현 |
| **Skills** | 117 test cases로 평가되는 표준화된 skills | Skills 라이브러리 구축, 엄격한 평가 체계 |
| **Scalability** | Personal → Team → Enterprise 명확한 단계 | Phase 1,2,3 로드맵 구성 (문서에 제시) |
| **Cost** | Context 압축, batch processing, model selection 최적화 | Budget control 메커니즘 초기부터 구현 |
| **Security** | Audit trail, approval workflow, fine-grained access | RBAC, human-in-the-loop, encryption 필수 |
| **Vendor Lock-in** | Vertex AI에 의존하되, open-source fallback | Model-agnostic layer 설계 (day 1) |
| **Observability** | Metrics, logging, tracing의 3-tier system | ELK, Prometheus, Jaeger 초기 구성 |

### 5.3 Google 문서의 미흡한 부분 및 우리의 보완

Google 문서가 직접 다루지 않는 부분:

1. **로컬 배포의 실제 성능**: Computer Use의 로컬 실행 비용/지연 시간 미명시
   - **우리 보완**: 실제 벤치마크 필요 (OpenAI hosted shell과 비교)

2. **Merge Conflict Resolution의 상세 알고리즘**: 자동 해결 방식 미기술
   - **우리 보완**: 3-way merge + semantic analysis 직접 구현

3. **Skills 버전 관리 & Rollback**: 수백 개 skills의 배포 및 롤백 메커니즘 미설명
   - **우리 보완**: Blue-green deployment, semantic versioning 구현

4. **Multi-tenant Governance**: 팀 간 자원 할당 및 우선순위 정책 미정의
   - **우리 보완**: Priority queue + SLA-based allocation 설계

---

이 문서는 Google의 공식 자료에서 도출 가능한 모든 기술적, 실무적 인사이트를 최대한 상세하게 분석하였으며, 우리 Harness Engineering 프로젝트의 설계, 구현, 확장의 각 단계에 직접 적용 가능한 concrete 권고사항들을 제시하고 있다. 특히 ADK + Gemini + Skills의 삼각형 구조와 personal → team → enterprise의 명확한 확장 경로는 우리의 하네스 개발 로드맵의 핵심 가이드라인이 될 것이다.
