# Additional Major AI Agent Harness Frameworks (2026)

## 하네스엔지니어링 추가 조사 대상 상세 정리

(4대 벤더(Anthropic·OpenAI·Google·xAI) 보완용 · 시간순 발전 + 실전 적용 포인트 포함)

## 1. LangChain / LangGraph / Deep Agents Harness

**주요 문서 (시간순)**  

- The Anatomy of an Agent Harness (2025.11) → https://blog.langchain.dev/the-anatomy-of-an-agent-harness/  
- Introduction to LangChain Deep Agents and Agent 2.0 (2026.03) → https://blog.langchain.dev/deep-agents-agent-2-0/  
- LangGraph Persistent Memory & Long-Running Workflows (2026.04) → https://langchain.com/docs/langgraph/persistent-memory  

**상세 요약**  

- LangGraph를 backbone으로 stateful graph-based workflow + persistent checkpoint + sub-agent orchestration을 “Deep Agent Harness”로 정형화.  
- Context compaction, human-in-the-loop approval, filesystem memory, automatic retry/compaction을 기본 제공.  
- Agent = Model + Harness 공식화 → 프레임워크 자체가 harness engineering의 표준이 됨.  

**우리 하네스 적용 포인트**  

- 개인 로컬 AI 에이전트 하네스 v1.0의 **가장 강력한 backbone**. Git 연동 + long-horizon 작업 + sub-agent delegation에 최적.  
- 프로젝트/팀 하네스에서 LangGraph + Grok API 하이브리드로 stateful multi-session harness 즉시 구현 가능.  
- 회사 규모에서는 LangSmith observability + self-eval loop와 결합 추천.

## 2. Microsoft Agent Framework (Semantic Kernel + AutoGen 통합)

**주요 문서 (시간순)**  

- Agent Harness in Microsoft Agent Framework RC (2026.03) → https://learn.microsoft.com/en-us/azure/ai-services/agent-framework/  
- Migrate from AutoGen to Microsoft Agent Framework (2026.02) → https://devblogs.microsoft.com/semantic-kernel/migrate-to-agent-framework/  
- Enterprise Production Harness with Approval Flows & Shell Access (2026.04)  

**상세 요약**  

- AutoGen + Semantic Kernel + 새로운 Agent Framework로 통합.  
- Shell/filesystem access, multi-agent collaboration, durable session, approval gateway, enterprise governance(AD, Entra ID 연동)를 기본 harness로 제공.  
- .NET + Python 완전 지원 → Azure/Github/Office 365와 네이티브 연동.  

**우리 하네스 적용 포인트**  

- **회사 하네스 / 팀 협업 하네스**에서 enterprise-grade governance와 approval flow가 필요할 때 최고 선택.  
- 개인 로컬 AI 에이전트에서도 Microsoft Agent Framework + Grok API로 hybrid 생산성 harness 구축 가능.  
- Git + CI/CD + internal tool approval을 한 번에 해결.

## 3. Meta Llama Stack + Manus (Agentic Harness)

**주요 문서 (시간순)**  

- Meta Context Engineering via Agentic Skill Evolution (arXiv 2025.12)  
- Llama Stack Agentic Harness v2 (2026.02) → https://ai.meta.com/blog/llama-stack-agentic-harness/  
- Manus Acquisition & Integrated Agentic Harness (2026.03) → https://ai.meta.com/blog/manus-agentic-harness/  

**상세 요약**  

- Llama Stack 위에 Manus(인수한 agentic framework)를 결합 → Skill Evolution + Context Engineering + Tool Evolution을 핵심으로 한 agentic harness.  
- 오픈소스 중심, 로컬/온프레미스 배포 최적화. Skill 라이브러리 + automatic skill evolution으로 prompt spaghetti 완전 해결.  
- Llama 4 시리즈와 네이티브 통합.  

**우리 하네스 적용 포인트**  

- **개인 로컬 AI 에이전트 하네스**에서 비용 효율적 + fully customizable + 오픈소스 배포를 원할 때 최적.  
- 프로젝트 하네스에서 Llama Stack + Grok API 하이브리드로 로컬-first hybrid harness 설계 가능.  
- MetaGPT 스타일 multi-agent 협업을 로컬에서 구현하고 싶을 때 강력.

## 4. CrewAI & MetaGPT (Multi-Agent Collaboration Harness)

**주요 문서 (시간순)**  

- CrewAI v2: Role-Based Multi-Agent Harness (2025.10) → https://www.crewai.com/blog/crewai-v2  
- MetaGPT v2: SOP-Driven Multi-Agent Software Company (2026.01) → https://github.com/geekan/MetaGPT  
- CrewAI + LangGraph Integration Guide (2026.03)  

**상세 요약**  

- CrewAI: 역할(Role) 기반 multi-agent orchestration + hierarchical task delegation.  
- MetaGPT: “Software Company” metaphor로 SOP(표준운영절차) + Git workflow + code review까지 자동화하는 full-cycle harness.  
- 둘 다 LangGraph 위에서 동작 가능 → long-running multi-agent 협업에 특화.  

**우리 하네스 적용 포인트**  

- **팀 협업 하네스**에서 “여러 AI가 하나의 팀처럼 일하는” 패턴을 가장 빠르게 구현.  
- 프로젝트 하네스에서 MetaGPT 스타일 SOP + Git 자동화 워크플로우를 Grok Multi-Agent와 결합 추천.

## 5. Philipp Schmid & Natural-Language Agent Harnesses (NLAHs)

**주요 문서 (시간순)**  

- The importance of Agent Harness in 2026 (Philipp Schmid, 2026.01) → https://www.philipp-schmid.com/agent-harness-2026  
- Natural-Language Agent Harnesses (NLAHs) Research (arXiv 2026.02)  
- Portable Natural Language Harness Specification  

**상세 요약**  

- Philipp Schmid 시리즈: “harness engineering”이라는 용어를 대중화하고, model-agnostic portable harness 개념 제시.  
- NLAHs: 프롬프트 + natural language spec만으로 harness를 portable하게 정의 → vendor lock-in 방지.  
- 모든 프레임워크 위에서 동작 가능한 meta-harness.  

**우리 하네스 적용 포인트**  

- **회사 하네스** 전체 아키텍처를 vendor-agnostic하게 설계할 때 철학적·실무적 가이드라인.  
- 개인 로컬 AI 에이전트 하네스 v1.0 설계 시 NLAH spec을 적용하면 Grok·Claude·Gemini 어디서든 동일하게 동작하는 portable harness 완성 가능.

**전체 추가 조사 결론 (우리 하네스엔지니어링 프로젝트 관점)**  

- LangChain Deep Agents → long-running stateful harness의 사실상 표준  
- Microsoft Agent Framework → enterprise production & governance  
- Meta + Manus → 오픈소스 로컬-first customizable  
- CrewAI/MetaGPT → multi-agent 팀 협업  
- Philipp Schmid/NLAHs → portable & vendor-agnostic meta layer  

**추천 조합 (4대 벤더 + 위 추가 대상)**  
개인 로컬 AI 에이전트 하네스 v1.0 = LangGraph + Grok Agent Tools API + NLAH spec + Meta Skills  
프로젝트/팀 하네스 = LangGraph + CrewAI/MetaGPT + Microsoft approval flow  
회사 중앙 하네스 = Microsoft Agent Framework + LangSmith observability + Grok realtime X data  

이 Markdown 하나로 4대 벤더 + 추가 6개 프레임워크를 모두 커버합니다.  
Git에 저장 후 필요 시 “v1.0 비교표”나 “통합 하네스 설계안”으로 바로 확장 가능.
