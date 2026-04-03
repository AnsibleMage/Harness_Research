# Plan Phase 규칙

> Plan Phase에서 적용되는 규칙입니다.

## 허용 도구

- `file_read`: 기존 코드/문서 읽기
- `code_search`: 코드 검색
- `grep`: 패턴 검색
- `glob`: 파일 패턴 매칭

## 금지 도구

- `file_create`, `file_edit`: 파일 생성/수정 금지
- `bash`: 명령 실행 금지
- `git_push`, `git_commit`: Git 작업 금지

## 산출물 요구사항

모든 Plan Phase 산출물은 다음 형식을 따릅니다:

```
P-1: Functional Requirements (User Stories)
P-2: Non-Functional Requirements (성능, 가용성, 보안)
P-3: Architecture Decision (기술 스택, 시스템 구조)
P-4: Implementation Roadmap (마일스톤, 의존성)
P-5: Risk Assessment (위험 목록, 완화 전략)
```

## Plan Approval 프로세스

1. Planner가 P-1~P-5 산출물 완성
2. Leader에게 "계획 완료, 승인 요청" 메시지 전송
3. Leader 검토:
   - 승인 → Execute Phase 시작 허용
   - 거부 → 피드백 반영하여 재계획
4. 승인 기준: "테스트 커버리지 포함, 위험 분석 완료"

## 품질 기준

- 요구사항 완전성: 모든 기능이 User Story로 표현
- 설계 명확성: 기술 선택 근거 명시
- 위험 분석: 최소 3개 위험 식별 + 완화 전략
