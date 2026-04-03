# 글로벌 CLAUDE.md 구축 — Phase별 실행 보고서

## Phase 1: 플랜 (Plan)

### 1.1 6개 리포트에서 추출한 글로벌 CLAUDE.md 핵심 요소

#### Report_01 (Anthropic) → 도출 요소
- [x] Initializer Agent 패턴: 매 세션 시작 시 환경/규칙 주입 → CLAUDE.md의 존재 이유
- [x] Progress Log 패턴: 세션 간 상태 전달 → compaction 보존 규칙 필요
- [x] Skeptical Evaluator: 자기 평가 시 반드시 문제점 1개 이상 찾기 → 검증 규칙
- [x] Context Anxiety 해결: artifact hand-off, incremental progress → 작업 단위 규칙

#### Report_02 (OpenAI Codex) → 도출 요소
- [x] Skills/Compaction: 재사용 가능한 procedure + 자동 context 압축 → Skills 활용 지침
- [x] AGENTS.md 패턴: durable guidance를 git 연동 → CLAUDE.md 유지보수 원칙
- [x] Approval Flow: 승인 필요 작업 분리 → 보안 규칙 명시
- [x] Multi-client 하네스: 동일 하네스 여러 환경 재사용 → 환경 독립적 규칙

#### Report_03 (Google Gemini ADK) → 도출 요소
- [x] Hierarchical Delegation: LLM Agent + Workflow Agent + Custom Agent → 작업 위임 규칙
- [x] Tool Orchestration 추상화 → 도구 사용 원칙
- [x] Self-eval + Human-in-the-loop → 검증 절차 규칙
- [x] Skills 라이브러리: 117개 프롬프트 테스트 → Skills 우선 활용 지침

#### Report_04 (xAI Grok) → 도출 요소
- [x] Long-horizon Reasoning: multi-step 사고 지원 → 5단계 사고 과정
- [x] 2M Context 활용: 대규모 context 효율 관리 → context 관리 규칙
- [x] Vendor Abstraction: tool wrapper layer → vendor-agnostic 원칙
- [x] Active/Warm/Cold Context 전략 → compaction 지침

#### Report_05 (추가 프레임워크) → 도출 요소
- [x] NLAH portable spec: vendor lock-in 방지 → 이식 가능한 규칙 작성
- [x] Agent = Model + Harness 공식 → CLAUDE.md = Harness의 핵심
- [x] LangGraph stateful workflow → 상태 기반 작업 관리 원칙
- [x] MetaGPT SOP: 표준운영절차 → 워크플로우 표준화

#### Report_06 (Claude Code 공식) → 제약조건
- [x] **200줄 이하** 권장
- [x] **Advisory** 성격 → 강제 사항은 Hooks/Permissions으로
- [x] **구체적이고 검증 가능한** 지시만
- [x] **프로젝트 특화 내용 불포함**
- [x] **"IMPORTANT"/"YOU MUST"** 남용 금지
- [x] `/compact` 후 완전 생존 → compaction 보존 규칙 포함 가능
- [x] HTML 주석 → 토큰 비용 없이 유지보수 메모

### 1.2 섹션 구성안

```
# ~/.claude/CLAUDE.md 구조

## 1. Persona (페르소나)                    ~15줄  [Report_01: Initializer, Report_05: NLAH]
   - 앤(Ann)과 미르(Mir) 역할 정의
   - 공공기관 SI PM + 바이브코더 맥락

## 2. Thinking Process (사고 과정)          ~15줄  [Report_04: Long-horizon, Report_01: Eval]
   - PARALLEL-FIRST 원칙
   - CLEAR Framework
   - 5단계 사고: 인식 → 탐색∥리스크 → 선택 → 검증

## 3. Workflow (워크플로우)                  ~25줄  [Report_02: Skills, Report_03: ADK, Report_05: MetaGPT SOP]
   - 바이브코딩 흐름: 탐색 → 계획 → 구현 → 검증 → 커밋
   - 복잡도별 접근 (단순/중간/높음)
   - Subagent 활용 원칙

## 4. Context Management (컨텍스트 관리)    ~20줄  [Report_01: Context Anxiety, Report_02: Compaction, Report_04: 3-tier]
   - /clear, /compact 사용 원칙
   - Compaction 보존 규칙
   - 세션 간 상태 전달 (progress log)

## 5. Code & Quality (코드 및 품질)         ~25줄  [Report_02: AGENTS.md, Report_03: Self-eval]
   - 공통 코딩 표준
   - Git 워크플로우
   - 검증 우선 원칙 (테스트/스크린샷/비교)

## 6. Security & Audit (보안 및 감사)       ~15줄  [Report_06: 보안 적합성, 공공기관 SI]
   - 민감 정보 처리 규칙
   - 감사 추적 원칙

## 7. Language & Response (언어 및 응답)    ~20줄  [Report_06: 응답 규칙]
   - 출력 언어 규칙
   - 응답 복잡도별 규칙
   - 단순 확인 → 예/아니오

## 8. Self-Maintenance (자기 유지보수)       ~10줄  [Report_06: 유지보수 원칙]
   - CLAUDE.md 자율 갱신 규칙
   - 충돌 시 확인 절차

─────────────────────────────────
추정 총 줄 수: ~145줄 (빈 줄 포함 ~170줄)
→ 200줄 제한 내 여유 있음
```

### 1.3 설계 원칙

| 원칙 | 근거 | 적용 방법 |
|------|------|-----------|
| Initializer 패턴 | Report_01 | CLAUDE.md 자체가 매 세션의 Initializer 역할 |
| Advisory 한계 인식 | Report_06 | 강제 필요 규칙은 Hooks/Permissions 분리 제안 포함 |
| Portable 설계 | Report_05 (NLAH) | vendor-specific 내용 배제, 보편적 원칙만 |
| Token 효율 | Report_06 | 매 줄 "삭제하면 실수하나?" 테스트 적용 |
| Scope 분리 | Report_06 | 글로벌 = 불변 원칙 / 프로젝트 = 구체 실행 |
