# OpenAI Codex 하네스엔지니어링 공식 문서 정리 (시간순)

## 하네스 발전 로드맵 요약

- 2024.10: Swarm (교육용 lightweight multi-agent handoff)
- 2025.03: Responses API + Agents SDK 실전화
- 2026.02: Codex harness 완성 (App Server + Skills + Shell + Compaction) → production long-running agent

### 1. Orchestrating Agents: Routines and Handoffs (2024.10) + Swarm

**URL**: https://developers.openai.com/cookbook/examples/orchestrating_agents/  
**GitHub**: https://github.com/openai/swarm

**요약**:

- Routines(자연어 instructions + tools)와 Handoffs(에이전트 간 동적 넘김) 중심 lightweight multi-agent.
- Stateless 설계로 observability와 테스트 용이. 교육용으로 명시.

**우리 하네스 적용 포인트**: 팀 협업 하네스 초기 handoff 패턴으로 차용 가능.

### 2. Unlocking the Codex harness: how we built the App Server (2026.02.04)

**URL**: https://openai.com/index/unlocking-the-codex-harness/

**요약**:

- Codex harness(전체 agent loop + thread lifecycle + tool execution)를 JSON-RPC 기반 App Server로 노출.
- Web/CLI/IDE/Desktop에서 **완전히 동일한 harness** 재사용 가능. Streaming progress, approval, persistence 지원.

**우리 하네스 적용 포인트**: 프로젝트/회사 하네스에서 Git + IDE 연동 시 “하나의 harness 여러 클라이언트” 아키텍처 핵심.

### 3. Shell + Skills + Compaction: Tips for long-running agents that do real work (2026.02.11)

**URL**: https://developers.openai.com/blog/skills-shell-tips/ (관련 best practices)

**요약**:

- **Skills**(재사용·버전 관리 가능한 procedure), hosted Shell(실제 컴퓨터 작업), server-side Compaction(자동 context 압축) 실전 패턴.
- Prompt spaghetti를 유지보수 가능한 workflow로 전환. Negative examples, secure networking 가이드 포함.

**우리 하네스 적용 포인트**: 개인 로컬 AI 에이전트 하네스에서 context anxiety와 장기 작업 안정성 해결. Git 연동 + 자동화에 강력.

### 4. Best practices & AGENTS.md (2026)

**URL**: https://developers.openai.com/codex/learn/best-practices/  
**AGENTS.md Guide**: https://developers.openai.com/codex/guides/agents-md

**요약**:

- AGENTS.md 파일로 durable guidance 제공 (repository-level agent instructions).
- Skills, MCP, Hooks, Rules 등으로 repeatable workflow 구축.

**우리 하네스 적용 포인트**: 로컬 프로젝트 하네스에서 Git 저장소와 자연스럽게 연동되는 실무 패턴.

**추가 참고 문서**:

- Run long horizon tasks with Codex: https://developers.openai.com/blog/run-long-horizon-tasks-with-codex/
- Codex App Server Docs

**하네스엔지니어링 관점 결론**: Embeddable & client-agnostic한 Codex harness + Skills/Compaction으로 production-level long-running real work agent 완성. Claude보다 더 구체적인 engineering 접근.
