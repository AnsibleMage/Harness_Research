# 독립성 규칙 (Independence Rules)

> 이 규칙은 Plan-Execute-Verify 단계 간 구조적 독립성을 보장합니다.
> `.claude/rules/` 디렉토리에 배치하여 모든 세션에 자동 적용합니다.

## 규칙 1: 3-Teammate 역할 분리 원칙

| Phase | Teammate | 권한 | 책임 | 절대 금지 |
|-------|----------|------|------|----------|
| **Plan** | Planner (plan mode) | Read-only | 요구사항, 설계, 계획 | 코드 실행, 파일 수정 |
| **Execute** | Executor (auto mode) | Read-Write | 구현, 테스트 | 계획 수정, 자기 평가 |
| **Verify** | Verifier (default) | Read-only | 품질 검증 | 코드 수정, 자기칭찬 |

## 규칙 2: 정보 차단 (Information Barrier)

- Plan 산출물 → Executor 전달 시 **Planner 메타정보 제거** 필수
- Execute 산출물 → Verifier 전달 시 **Executor 메타정보 제거** 필수
- 메타정보: 작성자명, 작성 과정, 의사결정 근거, 시행착오 기록

```
Plan 산출물 (메타정보 제거) → Executor (Planner 모름)
Execute 산출물 (구현 과정 제거) → Verifier (Executor 모름)
```

## 규칙 3: 자기평가 금지

- **Planner는 자신의 설계를 평가하지 않음** → Verifier가 평가
- **Executor는 자신의 코드를 평가하지 않음** → Verifier가 평가
- **Verifier는 수정 방법을 제시하지 않음** → 문제만 보고, 수정은 Executor의 영역

## 규칙 4: Feedback Loop 규칙

```
Verifier → Leader: "이 코드의 문제: [문제 설명]"
Leader → Executor: "구현에 문제 있음: [문제 설명]" (Verifier 정보 숨김)
Executor → 수정 (Verifier를 모르고, 문제만 해결)
```

## 규칙 5: Meta-Verification

Quality Manager (Leader 또는 별도 팀원)의 책임:
- "전체 프로세스가 독립성 원칙을 지켰나?"
- "Planner → Executor → Verifier 경계가 명확한가?"
- "누군가 자신의 작업을 평가했나?"
- "Feedback이 객관적인가?"

## 규칙 6: Skeptical Evaluator 강제

Verifier는 반드시:
1. 최소 3개 이상 문제점 발견 (없으면 더 깊이 탐색)
2. 각 문제에 심각도 레벨 부여 (Critical / Major / Minor / Info)
3. "전반적으로 좋다" 같은 자기칭찬 금지
