# Hooks 정책 (Hooks Policy)

> 외부 검증 레이어로서 Hooks의 역할과 정책을 정의합니다.

## 3중 검증 체계

```
1차: 팀원 자체 완료 판단 (실행자 관점)
2차: 다른 팀원의 독립 검증 (팀 내 독립성)
3차: Hook 스크립트의 자동 검증 (시스템 수준 독립성)
```

## Hook 종류 및 역할

| Hook | 트리거 시점 | 역할 | 종료 코드 |
|------|-----------|------|----------|
| **PreToolUse** | 도구 호출 직전 | 위험 작업 사전 차단 | 0=허용, 2=차단 |
| **PostToolUse** | 도구 호출 직후 | 결과 검증 + 감사 로깅 | 0=통과, 2=재검토 |
| **TaskCompleted** | 작업 완료 시 | 최종 품질 게이트 | 0=완료, 2=차단 |
| **TeammateIdle** | 팀원 유휴 시 | 조기 종료 방지 | 0=유휴, 2=계속 |
| **TaskCreated** | 작업 생성 시 | 작업 명세 검증 | 0=허용, 2=차단 |

## 종료 코드 정책

```
exit 0: 검증 통과 → 계속 진행
exit 1: 오류 발생 → 즉시 종료
exit 2: 재시도 필요 → 피드백 전달 후 팀원 계속 작동
```

## 핵심 원칙

1. **Hook은 Agent와 독립적**: Hook 스크립트는 어떤 Agent가 실행했는지 모름
2. **객관적 기준만 적용**: 코드 품질, 테스트 통과, 보안 검사 등
3. **감사 로깅 필수**: 모든 Hook 실행은 audit.log에 기록
4. **실패 시 차단**: 품질 기준 미달 시 exit 2로 완료 차단

## PowerShell 호환성 (Ann의 Windows 환경)

```json
{
  "hooks": {
    "PreToolUse": [{
      "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/pre-tool-use.ps1"
    }],
    "PostToolUse": [{
      "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/post-tool-use.ps1"
    }],
    "TaskCompleted": [{
      "command": "powershell -ExecutionPolicy Bypass -File .claude/hooks/verify-task.ps1"
    }]
  }
}
```
