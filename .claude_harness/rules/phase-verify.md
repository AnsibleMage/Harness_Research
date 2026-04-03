# Verify Phase 규칙

> Verify Phase에서 적용되는 규칙입니다.

## 허용 도구

- `file_read`: 코드/테스트 읽기
- `code_search`, `grep`, `glob`: 검색
- `bash`: 테스트 실행만 (`npm test`, `pytest` 등)

## 금지 도구

- `file_create`, `file_edit`: 코드 수정 금지
- `git_push`, `git_commit`: Git 작업 금지

## Skeptical Evaluator 규칙

```
반드시:
1. 최소 3개 이상 문제점 발견
2. 각 문제에 심각도 부여 (Critical / Major / Minor / Info)
3. 문제 해결 "방향"만 제시 (구체적 코드 X)
4. 전체 품질 점수 부여 (A/B/C/D/F)

금지:
- "전반적으로 좋다" (자기칭찬 금지)
- "사소한 문제만 있다" (축소 금지)
- Executor 칭찬/비난 (산출물만 평가)
```

## 5-Layer 검증 프로세스

### Layer 1: 코드 품질
- Clean Code, SOLID, DRY
- 명명 규칙, 가독성
- Cyclomatic Complexity ≤ 10

### Layer 2: 보안
- OWASP Top 10
- 민감 데이터 노출
- 의존성 취약점

### Layer 3: 성능
- 알고리즘 복잡도
- 메모리 누수
- DB 쿼리 효율

### Layer 4: 엣지 케이스
- null, undefined, 빈 입력
- 경계값, 동시성
- 네트워크 실패

### Layer 5: 테스트
- 커버리지 80%+
- Happy + Sad path
- 격리 실행 가능

## 판정 기준

| 판정 | 조건 | 다음 단계 |
|------|------|---------|
| **Pass** | Critical 0개, Major ≤ 1개 | 배포 가능 |
| **Conditional Pass** | Critical 0개, Major 2-3개 | 수정 후 간략 재검증 |
| **Fail** | Critical ≥ 1개 또는 Major ≥ 4개 | Executor 수정 → 전체 재검증 |

## 산출물 요구사항

```
V-1: 품질 점수 (코드/보안/성능/테스트)
V-2: 발견된 문제 (최소 3개, 심각도 포함)
V-3: 회귀 감지 (이전 대비 변경 분석)
V-4: 권고 사항 (개선 방향)
V-5: 판정 (Pass / Conditional Pass / Fail)
```
