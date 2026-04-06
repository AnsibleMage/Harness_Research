# .claude_harness — Harness Engineering 구현 파일

> Harness_Utilization_Plan.md에 정의된 Plan-Execute-Verify 독립성 아키텍처의 실제 구현 파일

## 배치 방법

이 폴더의 파일들을 프로젝트의 `.claude/` 디렉토리에 복사합니다:

```powershell
# Windows PowerShell
$project = "C:\Users\name\Documents\AnsibleMage\YourProject"

# 디렉토리 생성
New-Item -ItemType Directory -Force -Path "$project\.claude\agents"
New-Item -ItemType Directory -Force -Path "$project\.claude\hooks"
New-Item -ItemType Directory -Force -Path "$project\.claude\rules"
New-Item -ItemType Directory -Force -Path "$project\.claude\memory"

# 파일 복사
Copy-Item -Path "agents\*" -Destination "$project\.claude\agents\" -Recurse
Copy-Item -Path "hooks\*" -Destination "$project\.claude\hooks\" -Recurse
Copy-Item -Path "rules\*" -Destination "$project\.claude\rules\" -Recurse
Copy-Item -Path "settings.json" -Destination "$project\.claude\settings.json"
Copy-Item -Path "CLAUDE.md" -Destination "$env:USERPROFILE\.claude\CLAUDE.md"
```

## 파일 구조

```
.claude_harness/
├── CLAUDE.md                     # Global CLAUDE.md (하네스 v2.0)
│                                  → 배치: ~/.claude/CLAUDE.md
├── settings.json                  # Agent Teams + Hooks 설정
│                                  → 배치: .claude/settings.json
├── README.md                      # 이 파일
│
├── agents/                        # Teammate/Subagent 정의
│   ├── planner.md                 # Plan Phase (plan mode, read-only)
│   ├── executor.md                # Execute Phase (auto mode, read-write)
│   ├── verifier.md                # Verify Phase (default, read-only)
│   ├── security-reviewer.md       # 보안 전문 검증
│   ├── analyst.md                 # 다각도 분석 전담
│   └── devils-advocate.md         # 의도적 반론 제기
│                                  → 배치: .claude/agents/
│
├── hooks/                         # 외부 검증 스크립트 (PowerShell)
│   ├── verify-task.ps1            # TaskCompleted — 최종 품질 게이트
│   ├── pre-tool-use.ps1           # PreToolUse — 위험 작업 사전 차단
│   ├── post-tool-use.ps1          # PostToolUse — 결과 검증 + 감사
│   ├── check-idle-reason.ps1      # TeammateIdle — 조기 종료 방지
│   ├── on-executor-stop.ps1       # SubagentStop — Executor 종료 처리
│   └── strip-metadata.py          # Phase 간 메타정보 제거 유틸리티
│                                  → 배치: .claude/hooks/
│
└── rules/                         # 규칙 파일 (자동 로드)
    ├── independence.md             # 독립성 규칙 (핵심)
    ├── phase-plan.md              # Plan Phase 규칙
    ├── phase-execute.md           # Execute Phase 규칙
    ├── phase-verify.md            # Verify Phase 규칙
    └── hooks-policy.md            # Hooks 정책
                                   → 배치: .claude/rules/
```

## 핵심 아키텍처

```
Agent Teams (구조적 독립성)
  ├── Planner Teammate (plan mode)  → .claude/agents/planner.md
  ├── Executor Teammate (auto mode) → .claude/agents/executor.md
  └── Verifier Teammate (default)   → .claude/agents/verifier.md

Hooks (외부 검증 레이어)
  ├── PreToolUse  → pre-tool-use.ps1   (위험 차단)
  ├── PostToolUse → post-tool-use.ps1  (감사 로깅)
  └── TaskCompleted → verify-task.ps1  (품질 게이트)

Rules (규칙 자동 적용)
  ├── independence.md  (독립성 원칙)
  ├── phase-plan.md    (Plan 규칙)
  ├── phase-execute.md (Execute 규칙)
  └── phase-verify.md  (Verify 규칙)
```

## Agent Teams 활성화

```powershell
# 1. settings.json 확인 (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1")
# 2. Claude Code CLI에서 팀 생성
claude --enable-agent-teams

# 3. 기본 3-Teammate 팀 생성 프롬프트:
# "팀을 만들어줘:
#  - Planner: planner agent 타입, 요구사항 분석 담당
#  - Executor: executor agent 타입, 코드 구현 담당
#  - Verifier: verifier agent 타입, 품질 검증 담당"
```

## 관련 문서

- `23_Harness_Utilization_Plan.md` — 전체 하네스 활용 계획
- `22_Claude_Code_Agent_System_Analysis.md` — Agent Teams/Subagents/Skills 분석
- `16_Final_Global_CLAUDE_MD.md` — CLAUDE.md v1.0 (이전 버전)
