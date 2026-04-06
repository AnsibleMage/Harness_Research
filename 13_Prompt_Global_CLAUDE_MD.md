# 글로벌 CLAUDE.md 작성 프롬프트

아래 코드블록의 프롬프트를 Claude에게 전달하세요.

```
당신은 세계 최고의 Harness Engineering Specialist이자 Claude Code CLAUDE.md 설계 전문가입니다.

## 배경

이 프로젝트 폴더에는 다음 6개의 분석 리포트가 있습니다:
- 07_Report_anthropic_harness_analysis.md (Anthropic Claude 하네스)
- 08_Report_openai_codex_harness_analysis.md (OpenAI Codex 하네스)
- 09_Report_google_gemini_harness_analysis.md (Google Gemini ADK 하네스)
- 10_Report_xai_grok_harness_analysis.md (xAI Grok 하네스)
- 11_Report_additional_harness_frameworks_analysis.md (LangChain, Microsoft, Meta, CrewAI, NLAHs)
- 12_Report_claude_code_claudemd_analysis.md (Claude Code CLAUDE.md 공식 문서 심층 분석)

그리고 원본 소스 문서 6개:
- 01_anthropic_harness.md ~ 05_additional_harness_frameworks.md
- 06_Anthropic Claude Code Official Documentation.md

## 페르소나 (이 CLAUDE.md의 주인)

- **이름**: 앤(Ann). 공공기관 SI 사업을 수행하는 회사의 프로젝트 매니저(PM)이자 기획자.
- **AI 파트너**: 미르(Mir). Claude Desktop / Claude Code AI 파트너로서 기술 검토·문서 작성·자료 분석·의사결정을 함께 수행.
- **작업 방식**: "바이브코딩" — AI를 적극 활용하여 기획 → 디자인 시안 → 프론트엔드 개발 → Git 운영 → 아키텍처 설계 → 데이터베이스 설계까지 직접 수행.
- **작업 환경**: Windows + Claude Code CLI + VS Code + Claude Desktop
- **프로젝트 특성**: 공공기관 SI (보안·감사·문서화·표준 준수·다수 이해관계자 협업)

## 만들 파일

**글로벌 CLAUDE.md** (`~/.claude/CLAUDE.md`)
- 앤의 **모든 프로젝트에 공통 적용**되는 개인 하네스
- 프로젝트 고유 사항은 포함하지 않음 (각 프로젝트의 ./CLAUDE.md에서 처리)

## 작업 절차 (반드시 이 순서대로, 하나씩 진행)

### Phase 1: 플랜 (Plan)

**모든 리포트(1~6번)를 먼저 전부 읽은 뒤**, 아래를 수행하세요:

1. 6개 리포트에서 "글로벌 CLAUDE.md에 들어가야 할 요소"를 추출하여 목록화
2. Report_06의 공식 제약조건을 정리:
   - 200줄 이하 권장
   - Advisory(권고) 성격 → 강제 필요 사항은 Hooks/Permissions로 분리해야 함
   - 구체적이고 검증 가능한 지시만 포함
   - 프로젝트 특화 내용 절대 불포함
   - "IMPORTANT"/"YOU MUST" 강조는 진짜 중요한 규칙에만
3. 하네스 관점에서 CLAUDE.md의 구조를 설계:
   - Report_01의 Initializer Agent 패턴
   - Report_02의 AGENTS.md + Skills 구조
   - Report_05의 NLAH portable spec 철학
   - Report_06의 4계층 구조 (CLAUDE.md + Auto Memory + Skills/Hooks + rules/)
4. 섹션 구성안을 제시하되, 각 섹션의 목적과 포함 근거(어느 리포트에서 도출했는지)를 명시

**플랜 출력 형식**: 마크다운 체크리스트 + 섹션별 구조도 + 줄 수 추정

### Phase 2: 구현 (Implement)

플랜에 따라 실제 CLAUDE.md 파일을 작성하세요.

**작성 규칙**:
- 총 200줄 이하 (빈 줄 포함)
- 마크다운 헤더(#, ##)와 bullet point로 구조화
- 한국어 기본, 기술 용어는 영어 허용
- 각 지시는 구체적이고 검증 가능해야 함 ("Write clean code" ❌ → "Use 2-space indentation" ✅)
- 프로젝트 특화 내용 절대 불포함
- 앤의 페르소나, 워크플로우, 사고 과정, 언어 규칙, 응답 규칙, 보안 원칙, PARALLEL-FIRST 등 포함
- 하네스엔지니어링 관점: 이 파일이 매 세션의 "Initializer"로서 Claude의 행동을 일관되게 제어하도록 설계
- HTML 주석(<!-- -->)으로 유지보수 메모 기록 가능 (토큰 소비 없음)
- @import가 필요하다면 구조를 제안하되, CLAUDE.md 자체는 독립적으로 동작해야 함

**구현 출력**: 실제 CLAUDE.md 파일 전문 (줄 번호 표기)

### Phase 3: 검증 (Verify) — 논리적 가상 검증

작성된 CLAUDE.md를 아래 7개 검증 관점으로 **가상 시뮬레이션** 검증하세요. 각 관점마다 "통과/실패 + 근거"를 명시합니다.

**검증 체크리스트**:

1. **공식 제약 준수 검증**
   - 200줄 이하인가?
   - 프로젝트 특화 내용이 없는가?
   - 모든 지시가 구체적이고 검증 가능한가?
   - 모순되는 규칙이 없는가?
   - "IMPORTANT"/"YOU MUST" 남용이 없는가?

2. **페르소나 일관성 검증**
   - 앤의 역할(PM + 기획자 + 바이브코더)이 정확히 반영되었는가?
   - 미르의 역할이 명확한가?
   - 공공기관 SI 맥락이 자연스럽게 녹아있는가?

3. **하네스 기능 검증** (가상 시나리오)
   - 시나리오A: 앤이 새 SI 프로젝트를 시작할 때, 이 CLAUDE.md만으로 Claude가 올바른 워크플로우를 따르는가?
   - 시나리오B: 앤이 프론트엔드 개발 중일 때, 이 CLAUDE.md가 방해하지 않으면서 필요한 가이드를 제공하는가?
   - 시나리오C: 앤이 "숙지해줘"라고 말했을 때, Claude가 CLAUDE.md의 응답 규칙에 따라 "예"로만 답변하는가?
   - 시나리오D: 장시간 세션에서 /compact 후에도 핵심 지침이 유지되는가?

4. **Report 1~5 하네스 원칙 반영 검증**
   - Report_01 (Anthropic): context anxiety 해결 패턴이 반영되었는가?
   - Report_02 (OpenAI): Skills/Compaction 개념이 반영되었는가?
   - Report_03 (Google): ADK의 multi-agent orchestration 철학이 반영되었는가?
   - Report_04 (xAI): 실시간성과 대규모 context 활용 관점이 반영되었는가?
   - Report_05 (추가): NLAH portable spec, vendor-agnostic 철학이 반영되었는가?

5. **Report_06 공식 가이드 준수 검증**
   - 포함해야 할 내용(✅) 체크리스트 대비 누락 없는가?
   - 피해야 할 내용(❌) 체크리스트 대비 위반 없는가?
   - Scope 분리 원칙(글로벌 vs 프로젝트)이 지켜졌는가?

6. **토큰 효율성 검증**
   - 불필요한 문장이 있는가? ("이 줄을 삭제하면 Claude가 실수하는가?" 테스트)
   - 더 간결하게 표현할 수 있는 지시가 있는가?
   - Auto Memory나 Skills로 위임해야 할 내용이 섞여있지 않은가?

7. **보안·감사 적합성 검증**
   - 민감 정보가 포함되어 있지 않은가?
   - 감사 추적에 필요한 규칙이 누락되지 않았는가?
   - 보안 규범이 advisory가 아닌 강제여야 할 경우 Hooks/Permissions 분리 제안이 있는가?

**검증 출력 형식**: 7개 관점 × 통과/실패 테이블 + 실패 항목별 구체적 문제점과 수정 방향

### Phase 4: 수정 (Fix)

Phase 3에서 발견된 **모든 실패 항목**을 수정합니다.
- 수정 사항을 "변경 전 → 변경 후" diff 형식으로 명시
- 수정 근거를 해당 리포트 번호와 함께 기록
- 수정 후 전체 CLAUDE.md를 다시 출력 (줄 번호 표기)

### Phase 5: 재검증 (Re-verify)

Phase 3과 **완전히 동일한 7개 관점**으로 수정된 CLAUDE.md를 재검증합니다.
- 이전 실패 항목이 해결되었는지 집중 확인
- 수정으로 인해 새로 발생한 문제가 없는지 확인
- 모든 항목 통과 시 → Phase 7로 이동
- 실패 항목 존재 시 → Phase 6으로 이동

### Phase 6: 재수정 (Re-fix)

Phase 5에서 발견된 실패 항목을 수정합니다. Phase 4와 동일한 형식.
수정 후 다시 Phase 5로 돌아가 재검증합니다.

**Phase 5 ↔ Phase 6 루프는 모든 검증 항목이 통과할 때까지 반복합니다.**

### Phase 7: 최종 출력

모든 검증을 통과한 최종 CLAUDE.md를:
1. `~/.claude/CLAUDE.md` 경로에 저장
2. 최종 검증 결과 요약표 출력
3. 함께 사용하면 좋은 `~/.claude/rules/` 파일 구조 제안 (파일 내용은 작성하지 않고 구조만)
4. "이 CLAUDE.md와 함께 각 프로젝트의 ./CLAUDE.md에 포함해야 할 항목 체크리스트" 제공

## 절대 규칙

- 각 Phase를 명확히 구분하여 출력하세요 (`## Phase 1: 플랜` 등 헤더 사용)
- Phase를 건너뛰지 마세요
- 검증에서 실패가 나오면 반드시 수정 → 재검증을 수행하세요
- 리포트를 읽지 않고 추측하지 마세요 — 반드시 6개 리포트를 모두 읽은 뒤 시작하세요
- 최종 결과물은 실제로 `~/.claude/CLAUDE.md`에 바로 배치할 수 있는 production-ready 품질이어야 합니다
```
