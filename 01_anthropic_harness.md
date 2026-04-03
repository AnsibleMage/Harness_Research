# Anthropic Claude 하네스엔지니어링 공식 문서 정리 (시간순)

## 하네스 발전 로드맵 요약

- 2025.11: 2-Agent (Initializer + Coding) long-running harness 탄생
- 2026.01: Eval harness 개념화
- 2026.03: 3-Agent GAN-style (Planner + Generator + Evaluator)로 업그레이드 → context reset 최소화

### 1. Effective harnesses for long-running agents (2025.11.26)

**URL**: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

**요약**:

- Claude Agent SDK를 활용한 **Initializer Agent + Coding Agent** 2단계 하네스 설계.
- 첫 세션에서 환경 세팅(init.sh, progress log, git commit) 후, 이후 세션마다 incremental progress + artifact hand-off로 multi-context window에서도 안정적 장기 작업 가능.
- Context anxiety 문제를 context reset + hand-off로 해결.

**우리 하네스 적용 포인트**: 개인 로컬 AI 에이전트 장기 프로젝트 시 가장 먼저 적용할 기본 패턴.

### 2. Demystifying evals for AI agents (2026.01.09)

**URL**: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

**요약**:

- Agent harness(실행 스캐폴드)와 Eval harness(평가 인프라)를 구분.
- Claude Code 자체를 예시로 long-running harness의 성공/실패 사례 분석.
- Harness 자체를 평가하는 메타 시스템 개념 도입.

**우리 하네스 적용 포인트**: 회사/팀 하네스 구축 시 자동 self-eval 시스템 설계 가이드라인.

### 3. Harness design for long-running application development (2026.03.24)

**URL**: https://www.anthropic.com/engineering/harness-design-long-running-apps

**요약**:

- 이전 2-agent를 **Planner + Generator + Evaluator** 3-agent (GAN 스타일)로 업그레이드.
- Frontend design(주관적)과 full-stack coding(검증 가능)을 동시에 처리. Opus 4.5 이후 context reset 없이 수시간 연속 빌드 가능.
- Automatic compaction + skeptical evaluator로 self-praise bias 해결.

**우리 하네스 적용 포인트**: 개인 로컬 AI 에이전트 하네스 v1.0 최종 형태로 가장 추천. 팀 협업 시 multi-agent orchestration 기반.

**추가 참고 문서**:

- Agent SDK Overview: https://docs.anthropic.com/en/docs/claude-code/sdk
- Claude 4 Prompting Guide (multi-context section)

**하네스엔지니어링 관점 결론**: 단순함 유지하면서도 context anxiety와 long-horizon 작업 안정성을 동시에 해결하는 방향으로 급속 발전.
