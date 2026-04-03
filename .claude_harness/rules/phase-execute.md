# Execute Phase 규칙

> Execute Phase에서 적용되는 규칙입니다.

## 허용 도구

- `file_read`, `file_create`, `file_edit`: 코드 작성/수정
- `bash`: 빌드, 테스트, 실행
- `git_commit`, `git_push`: 버전 관리
- `glob`, `grep`: 검색

## 금지 행위

- ❌ 계획 수정 (Plan은 Planner의 영역)
- ❌ 자기 평가 ("이 코드는 잘 작성되었다" 금지)
- ❌ Planner 정보 참조 (산출물만 참고)
- ❌ 위험한 명령 (rm -rf, force push 등)

## TDD 필수 규칙

```
1. Red: 실패하는 테스트 먼저 작성
2. Green: 최소한의 코드로 테스트 통과
3. Refactor: 코드 개선 (테스트 유지)
```

## 품질 기준

- 테스트 커버리지: 80% 이상
- 복잡도: Cyclomatic Complexity ≤ 10
- DRY: 중복 코드 없음
- 에러 처리: try-catch + context 포함 에러 메시지
- 코딩 표준: ESLint/Prettier 통과

## 산출물 요구사항

```
E-1: Implementation Code (클린 코드)
E-2: Unit Tests (80%+ 커버리지)
E-3: Integration Tests (모듈 간 검증)
E-4: Performance Metrics (속도, 메모리)
```

## Hook 연동

- `PreToolUse`: 위험 명령 사전 차단
- `PostToolUse`: 파일 변경 감사 로깅
- `TaskCompleted`: 자동 검증 트리거 → Verifier 전달
