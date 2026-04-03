# Google Gemini / ADK 하네스엔지니어링 공식 문서 정리 (시간순)

## 하네스 발전 로드맵 요약 (Google 관점)

- 2025년: Agent Development Kit (ADK) 공개 → multi-agent orchestration 프레임워크 중심
- 2025.10~2026: Gemini 2.5 Computer Use + Gemini 3 시리즈 → 실제 UI/터미널 제어 agentic 능력 강화
- 2026: Terminus-2 harness (Terminal-Bench 평가용), Skills 라이브러리, Vertex AI multi-agent 시스템으로 production-grade long-running agent 실전화
- 특징: “harness” 대신 ADK + Skills + Computer Use로 context 관리와 tool orchestration 강조. 모델(Gemini)과 framework(ADK)를 결합한 통합 접근

### 1. Making it easy to build multi-agent applications (2025.04)

**URL**: https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/

**요약**:

- Google Agent Development Kit (ADK) 공개. Pythonic하게 multi-agent 시스템을 쉽게 구축할 수 있는 오픈소스 프레임워크.
- LLM Agent, Workflow Agent, Custom Agent 3가지 타입으로 구성. 계층적 multi-agent (hierarchical delegation)와 tool ecosystem 지원.

**우리 하네스 적용 포인트**: 팀 협업 하네스나 회사 중앙 하네스에서 multi-agent orchestration의 기본 골격으로 바로 사용 가능. (Claude 3-agent와 유사한 역할 분리)

### 2. Build multi-agentic systems using Google ADK (2025.07)

**URL**: https://cloud.google.com/blog/products/ai-machine-learning/build-multi-agentic-systems-using-google-adk

**요약**:

- ADK를 활용한 실제 multi-agent workflow 예시와 소스코드 제공.
- 상태 관리, tool calling orchestration, Gemini 모델 연동을 ADK가 추상화하여 복잡한 agentic 시스템 개발을 단순화.

**우리 하네스 적용 포인트**: 프로젝트 하네스 구축 시 ADK를 backbone으로 삼아 Git 연동 + 장기 작업 흐름을 설계할 때 강력.

### 3. Introducing the Gemini 2.5 Computer Use model (2025.10)

**URL**: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/

**요약**:

- Gemini 2.5 기반 Computer Use 모델 출시. 브라우저·모바일 UI를 직접 제어하는 agent 구축 가능.
- 낮은 지연시간과 높은 성능으로 실제 환경에서 long-running agent의 “손” 역할을 담당.

**우리 하네스 적용 포인트**: 개인 로컬 AI 에이전트 하네스에서 Shell/Computer Use 기능 구현 시 핵심. OpenAI의 hosted Shell과 직접 비교 가능.

### 4. Gemini 3.1 Pro Model Card & Agentic Capabilities (2026.02)

**URL**: https://deepmind.google/models/model-cards/gemini-3-1-pro/  
**관련**: https://deepmind.google/models/gemini/pro/

**요약**:

- Gemini 3.1 Pro의 agentic 기능 대폭 강화. Terminal-Bench 2.0에서 Terminus-2 harness 사용, SWE-Bench 등 agentic coding 벤치마크 고성능 기록.
- Multi-step task, tool use, long-horizon 작업 능력 강조. Vertex AI와 ADK를 통해 enterprise-scale 배포 지원.

**우리 하네스 적용 포인트**: long-running application development에서 context 관리와 self-correction을 Gemini + ADK 조합으로 구현. 회사 하네스 규모 확장 시 Vertex AI 기반으로 가장 적합.

### 5. Closing the knowledge gap with agent skills (2026.03)

**URL**: https://developers.googleblog.com/closing-the-knowledge-gap-with-agent-skills/

**요약**:

- Gemini API용 Skills 라이브러리 공개 (GitHub: google-gemini/gemini-skills).
- Evaluation harness로 117개 프롬프트 테스트. Skills 추가로 coding agent 성능 크게 향상. SDK 지식 주입과 repeatable workflow 지원.

**우리 하네스 적용 포인트**: OpenAI의 Skills/Compaction과 유사. 개인/프로젝트 하네스에서 prompt spaghetti 방지와 재사용 가능한 procedure 관리에 바로 적용.

**추가 참고 문서**:

- Agent Development Kit 공식 문서: https://google.github.io/adk-docs/
- Gemini API Agents Overview: https://ai.google.dev/gemini-api/docs/agents
- Vertex AI Multi-agent Architecture: https://docs.cloud.google.com/architecture/multiagent-ai-system

**하네스엔지니어링 관점 결론**: Google은 ADK라는 강력한 framework + Gemini의 Computer Use/Skills로 “model + harness 통합” 접근. Claude의 3-agent GAN-style이나 OpenAI Codex harness만큼 명시적 “harness” 용어는 적지만, 실전 multi-agent와 long-running 작업에 매우 구체적인 도구를 제공. 모델 agnostic 성향도 강점.
