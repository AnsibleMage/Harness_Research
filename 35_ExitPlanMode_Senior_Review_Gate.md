---
title: "ExitPlanMode 시니어 검증 Gate Hook 구현 — Mac"
version: "1.0.0"
created: "2026-04-07"
updated: "2026-04-07"
tags: [claude-code, V5.3.0, mac, hook, plan-mode, senior-review, PreToolUse]
status: completed
type: design
---

## 🔄 Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed
- 마지막 작업: ExitPlanMode PreToolUse Hook 구현 + 테스트 완료 (Mac)

### 다음 작업 (TODO)
- [x] 문제 분석: plan-review-trigger.sh가 Plan 모드에서 트리거 안 됨 ✅
- [x] 방법 2(ExitPlanMode PreToolUse) 설계 ✅
- [x] Hook 스크립트 구현 ✅
- [x] settings.json PreToolUse matcher 추가 ✅
- [x] 3가지 테스트 케이스 통과 ✅
- [ ] 실전 테스트: 다음 Plan 모드 세션에서 실제 deny→검증→통과 사이클 확인

### 작업 조언
> [!tip] 다음 Claude Code에게
> - 이 Hook은 Plan 모드 전용. 체인 워크플로우의 plan-review-trigger.sh와 상호 보완
> - grep 패턴 `^## 시니어 검증 결과`의 `^` 앵커 필수 — 제거하면 plan 설명 텍스트에서 오탐 6건 발생
> - PreToolUse는 `permissionDecision: "deny"` (deprecated `decision: "block"` 아님)
> - deny 후 Agent spawn → plan Edit → ExitPlanMode 재호출 흐름이 정상 작동하는지 실전 확인 필요
> - [[34_V530_Mac_Senior_Verification.md]]과 교차 참조

---

# ExitPlanMode 시니어 검증 Gate Hook 구현

> **환경**: macOS (Darwin 24.6.0) | Claude Code V5.3.0 | Opus 4.6

## §1. 문제 분석

### 기존 Hook의 한계

`plan-review-trigger.sh`(PostToolUse)는 `plan.md` 또는 `plan_*.md` 파일명으로 Write될 때 시니어 검토를 트리거한다. 그러나 **두 가지 이유로 Claude 기본 Plan 모드에서는 작동하지 않는다**:

| 문제 | 코드 위치 | 설명 |
|------|----------|------|
| **경로 제외** | 28-29줄 | `.claude/plans/` 경로를 명시적으로 `exit 0` 처리 |
| **파일명 불일치** | 32-38줄 | `^plan` 패턴 매칭이나, Plan 모드는 `modular-foraging-bear.md` 같은 랜덤 파일명 사용 |

```bash
# plan-review-trigger.sh 28-29줄 — Plan 모드 경로 제외
if echo "$FILE_PATH" | grep -q "/.claude/plans/"; then
    exit 0
fi
```

### 결론

`plan-review-trigger.sh`는 **체인 워크플로우**(DevChain/SystemDesignChain에서 프로젝트 폴더에 `plan.md` Write)용이며, **Claude 기본 Plan 모드**와는 완전히 별개.

## §2. 해결 방안 검토

| 방법 | 트리거 | 장단점 |
|------|--------|--------|
| **1. 기존 Hook 수정** | PostToolUse Write | plan 점진적 Write마다 과다 트리거 ❌ |
| **2. ExitPlanMode PreToolUse (채택)** | Plan 완료 시점 1회 | 정확한 타이밍, 1회만 트리거 ✅ |
| **3. plan 내용 마커 기반** | Write + 내용 검사 | 복잡도 대비 이점 적음 ❌ |

**방법 2 채택 이유**: ExitPlanMode 호출 = "plan 완성 선언" 시점. 이 순간에 검증을 강제하면 과다 트리거 없이 정확히 1회만 실행.

## §3. 구현 상세

### 3.1 Hook 스크립트

**파일**: `~/.claude/hooks/plan-exit-senior-review.sh`

```bash
#!/bin/bash
# plan-exit-senior-review.sh — PreToolUse Hook: ExitPlanMode 시니어 검증 Gate
# V1.0 (2026-04-07) — Mac 환경 구현

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // .toolName // empty' 2>/dev/null)

# ExitPlanMode만 감지
if [ "$TOOL_NAME" != "ExitPlanMode" ]; then
    exit 0
fi

# 최신 plan 파일 찾기
PLAN_FILE=$(ls -t ~/.claude/plans/*.md 2>/dev/null | head -1)

# plan 파일 없으면 통과 (graceful fallback)
if [ -z "$PLAN_FILE" ]; then
    exit 0
fi

# 시니어 검증 결과 섹션 확인 (^앵커로 인라인 오탐 방지)
if grep -qE '^## 시니어 검증 결과' "$PLAN_FILE" 2>/dev/null; then
    exit 0  # 검증 완료 → 통과
fi

# 검증 미완료 → deny + 검증 지시 주입
jq -n --arg path "$PLAN_FILE" '{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "⚠️ [시니어 검증 필수] ExitPlanMode 차단\n..."
  }
}'
exit 0
```

### 3.2 핵심 설계 결정

| 결정 | 이유 |
|------|------|
| **PreToolUse (Pre, not Post)** | ExitPlanMode 실행 전에 차단해야 Plan 모드를 유지할 수 있음 |
| **plan 내 마커 섹션 검사** | 임시 플래그 파일 불필요, plan에 검증 결과가 직접 포함되어 앤이 확인 가능 |
| **`^` grep 앵커** | plan 설명에 마커 텍스트가 포함될 때 오탐 방지 (테스트에서 6건 오탐 발견→수정) |
| **`permissionDecision: "deny"`** | Claude Code 공식 형식. deprecated `decision: "block"` 아님 |
| **`hookSpecificOutput` wrapper** | PreToolUse JSON 출력 필수 래퍼 |

### 3.3 settings.json 변경

```json
"PreToolUse": [
  {
    "matcher": "Write|Edit",
    "hooks": [{ "command": "보안 파일 차단 (기존)" }]
  },
  {
    "matcher": "ExitPlanMode",          // ← 신규 추가
    "hooks": [{
      "type": "command",
      "command": "~/.claude/hooks/plan-exit-senior-review.sh"
    }]
  }
]
```

## §4. 실행 흐름

```
1. 아리가 plan 작성 완료
2. ExitPlanMode 호출 시도
3. PreToolUse Hook 실행
   ├─ plan에 "## 시니어 검증 결과" 없음
   └─ permissionDecision: "deny" → ExitPlanMode 차단
4. deny reason이 아리에게 전달
5. 아리가 Agent spawn (plan 파일 경로만 전달, reasoning 차단)
6. Agent 독립 검토: 허점 3개+ 필수, 실패 시나리오, 확신도 X/10
7. 아리가 plan 파일에 "## 시니어 검증 결과" 섹션 Edit
8. ExitPlanMode 재호출
9. Hook 재실행 → "## 시니어 검증 결과" 발견 → 통과
10. 앤에게 시니어 검증이 반영된 최종 plan 제시
```

## §5. Hook 생태계 정리

| Hook | 이벤트 | 대상 | 역할 |
|------|--------|------|------|
| `plan-review-trigger.sh` | PostToolUse (Write) | 체인 워크플로우 `plan.md` | 체인에서 plan.md Write 시 검토 주입 |
| **`plan-exit-senior-review.sh`** | **PreToolUse (ExitPlanMode)** | **Plan 모드 `~/.claude/plans/*.md`** | **Plan 모드 종료 시 검증 강제** |

두 Hook은 **상호 보완적**:
- 체인 워크플로우 → `plan-review-trigger.sh` (PostToolUse)
- Claude 기본 Plan 모드 → `plan-exit-senior-review.sh` (PreToolUse)

## §6. 테스트 결과

| 테스트 케이스 | 입력 | 기대 | 결과 |
|-------------|------|------|------|
| **ExitPlanMode + 검증 없음** | `{"tool_name": "ExitPlanMode"}` | deny JSON 출력 | ✅ 정상 deny |
| **ExitPlanMode + 검증 있음** | plan에 `## 시니어 검증 결과` 추가 후 | 무출력 + exit 0 | ✅ 통과 |
| **다른 도구 (Write)** | `{"tool_name": "Write"}` | 무출력 + exit 0 | ✅ 무시 |
| **grep 오탐 방지** | plan 설명에 마커 텍스트 6건 포함 | 오탐 0건 | ✅ `^` 앵커 작동 |

### 오탐 사례 (수정 전)

```
# 수정 전: grep -q "## 시니어 검증 결과" → 6건 매치 (오탐)
24:→ "## 시니어 검증 결과" 섹션 존재 여부 확인
31:- `## 시니어 검증 결과` 섹션이 plan에 직접 포함되므로...
66:   └─ plan 파일에 "## 시니어 검증 결과" 없음 → BLOCK
70:6. 아리가 plan 파일에 "## 시니어 검증 결과" 섹션 Edit
73:   └─ "## 시니어 검증 결과" 발견 → 통과
97:2. Agent 검토 결과가 plan에 `## 시니어 검증 결과`로 추가되는지 확인

# 수정 후: grep -qE '^## 시니어 검증 결과' → 0건 (정상)
# 인라인 텍스트는 모두 행 중간에 위치 → ^앵커로 정확히 필터링
```

## §7. PreToolUse Hook 형식 레퍼런스

Claude Code PreToolUse Hook의 공식 JSON 출력 형식:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",        // "allow" | "deny" | "ask" | "defer"
    "permissionDecisionReason": "사유"   // deny 시 Claude에게 표시
  }
}
```

| 필드 | 설명 |
|------|------|
| `hookSpecificOutput` | 필수 wrapper |
| `hookEventName` | `"PreToolUse"` 고정 |
| `permissionDecision` | `allow`: 통과, `deny`: 차단, `ask`: 사용자 확인, `defer`: 기본 동작 |
| `permissionDecisionReason` | deny 사유. Claude에게 additionalContext처럼 전달 |
| exit code | 항상 `0` (JSON으로 결정 전달) |

> ⚠️ `decision: "block"` 형식은 deprecated. 반드시 `permissionDecision: "deny"` 사용.

## 관련 문서

### Direct Links
- [[33_V530_Mac_Migration_Plan.md]] — V5.3.0 Mac 마이그레이션 계획
- [[34_V530_Mac_Senior_Verification.md]] — V5.3.0 Mac 시니어 검증 보고서

### Backlinks
- (신규 문서 — 아직 역링크 없음)

### Topic Links
- [[30_V530_Application_Report.md]] — V5.3.0 적용 보고서

## Release Notes

### v1.0.0 (2026-04-07)
- 초기 작성: ExitPlanMode 시니어 검증 Gate Hook 설계+구현+테스트

> **앤의 원본 프롬프트**:
> 1. "클로드 시스템에 스킬이랑 서브에이전트 검색해서 작업계획서 만드는것 있는지 확인해줘 클로드의 기본 플랜모드같은거면 좋겠어"
> 2. "plan-review-trigger.sh 이건 작동안하겠는데? 플랜엠디는 작성되지 않잖아 저 파일명이 트리거일테니"
> 3. "클로드 플랜 폴더에 랜덤파일명이 생성되면 연속으로 시니어 검증을 하는걸로 훅을 설정할 수는 있어?"
> 4. "응 결론으로 방법 2로 하고 시니어검증이 반영된 플랜을 최종결과로 나오게 까지 할 수 있나?"
> 5. "Harness_Research 폴더에 35번 문서로 방금 구현한걸 정리해서 문서로 작성해줘 맥에서 구현한거 명시해주고"
