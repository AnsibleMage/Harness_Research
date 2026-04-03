# Agent Catalog - Harness Research 에이전트 카탈로그

**작성일**: 2026-04-03
**총 에이전트**: 30개
**분류 카테고리**: 8개

---

## 1. Agent 카탈로그 (Detailed)

### 1.1 Planning 에이전트 (계획 수립)

#### 1. **Requirements Analyst** (requirements-analyst.md)
- **역할**: 요구사항 수집 및 분석 전문가. 기능/비기능 요구사항을 명확히 하고, 비즈니스 로직을 매핑하며, 기술 제약사항을 식별.
- **주요 역량**:
  - 기능적/비기능적 요구사항 명확화 (User Story 포맷)
  - 비즈니스 로직 분석 및 워크플로 문서화
  - 기술 제약사항 식별 및 위험 평가 (4차원: Technical/Business/Timeline/Resource)
- **독립성**: 조건부 — 시작 단계에서 독립적이나 이후 System Architect와 협력
- **Harness 관련성**: Plan 단계 (P-1 비즈니스 요구사항, P-2 기술 제약)

#### 2. **Complexity Resolver** (complexity-resolver.md)
- **역할**: 복잡한 문제를 체계적으로 분해하는 전문가. 3-7개 주요 컴포넌트로 분해, 의존성 매핑, 레버리지 포인트 식별, 최적 순서화.
- **주요 역량**:
  - 계층적 시스템 분해 (2-3 레벨 깊이)
  - 4차원 복잡도 평가 (기술 난이도, 불확실성, 상호의존도, 변동성 위험)
  - 레버리지 포인트 식별 (고영향 요소, 병목, 고위험, 기회 영역)
  - 병렬 vs 순차 실행 최적화
- **독립성**: 독립적 — 다른 에이전트 없이 단독 실행 가능
- **Harness 관련성**: Plan 단계 (P-3 아키텍처 설계)

#### 3. **System Architect** (system-architect.md)
- **역할**: 시스템 아키텍처 설계 전문가. Clean Architecture, SOLID, 마이크로서비스 경계 정의, 기술 스택 선택, Mermaid 문서화.
- **주요 역량**:
  - Clean Architecture 레이어 설계 (Entities, Use Cases, Adapters, Frameworks)
  - SOLID 원칙 적용
  - 마이크로서비스 경계 정의 및 통신 패턴 설계
  - 10배 성장을 위한 수평 확장 설계
- **독립성**: 의존적 — Requirements Analyst의 산출물 필요
- **Harness 관련성**: Plan 단계 (P-3 아키텍처 설계, P-4 기술 결정)

---

### 1.2 Execution 에이전트 (실행/구현)

#### 4. **Code Developer** (code-developer.md)
- **역할**: TDD 기반 소프트웨어 개발자. Red-Green-Refactor 사이클, DRY 원칙, 선언형 코딩, 80% 이상 테스트 커버리지.
- **주요 역량**:
  - TDD 방법론 (Red-Green-Refactor)
  - DRY 원칙 적용 (함수/클래스/모듈 추출)
  - 선언형 코딩 스타일, 함수 설계 (30줄 이하, 복잡도 10 이하)
  - 최소 80% 테스트 커버리지 달성
- **독립성**: 의존적 — System Architect의 아키텍처 설계 필요
- **Harness 관련성**: Execute 단계 (E-1 개발, E-2 테스트)

#### 5. **Solution Innovator** (solution-innovator.md)
- **역할**: 창의적 솔루션 생성 전문가. 창의적 결합, 도메인 간 차용, 제약 활용, 역발상, 시스템 재설계를 통해 8-10개 다양한 솔루션 생성.
- **주요 역량**:
  - 창의적 솔루션 생성 (최소 8-10개)
  - 4가지 평가 기준 (혁신성, 실현가능성, 가치, 위험도)
  - 도메인 간 솔루션 적응
  - 제약 기반 혁신
- **독립성**: 조건부 — Requirements 이해 후 독립적 생성 가능
- **Harness 관련성**: Plan 단계 (P-5 솔루션 도출), Execute 단계 (E-3 구현 옵션)

---

### 1.3 Verification 에이전트 (검증/품질)

#### 6. **Grader** (grader.md)
- **역할**: 스킬/에이전트 출력을 eval_test.json 기대값과 대조하여 냉정하게 채점. Pass/Fail/Partial 판정 및 점수 산출.
- **주요 역량**:
  - 테스트 케이스 기반 채점 (Pass/Partial/Fail/Critical Miss)
  - 회귀(Regression) 감지
  - 정량적 점수 산출
- **독립성**: 의존적 — 테스트 케이스(eval_test.json) 필요
- **Harness 관련성**: Verify 단계 (V-2 테스트 실행, V-3 회귀 감지)

#### 7. **Comparator** (comparator.md)
- **역할**: 구 버전(A)과 신 버전(B)을 블라인드 비교하여 어느 버전이 우수한지 판정. 버전 라벨 없이 순수 품질로만 비교.
- **주요 역량**:
  - 블라인드 비교 (버전 라벨 제거)
  - A vs B 승패/무 판정
  - 회귀 감지 (신버전이 기존 테스트에서 퇴행하면 거부)
- **독립성**: 의존적 — Grader의 산출물(두 버전 결과) 필요
- **Harness 관련성**: Verify 단계 (V-3 회귀 감지, V-4 버전 비교)

#### 8. **Eval Analyzer** (eval-analyzer.md)
- **역할**: Grader 실패 케이스의 근본 원인을 분석하고 구체적 수정 제안 도출. 실패 패턴 분류, 근본 원인 추론, 수정안 제시.
- **주요 역량**:
  - 실패 패턴 분류 (탐지 실패, 오탐, 분류 오류)
  - 근본 원인 추론 (프롬프트 불충분, 예시 부족, 규칙 충돌)
  - 구체적 수정안 도출 (파일, 섹션, 추가 규칙)
- **독립성**: 의존적 — Grader 실패 결과 필요
- **Harness 관련성**: Verify 단계 (V-5 근본 원인 분석)

#### 9. **Quality Reviewer** (quality-reviewer.md)
- **역할**: 코드 리뷰 전문가. 테스트 커버리지, 코드 품질, 성능, 리팩토링 기회, 보안 취약점 검토. 5개 차원 모두 평가.
- **주요 역량**:
  - 테스트 커버리지 분석 (Line 80%+, Branch 75%+, Function 90%+)
  - 코드 품질 평가 (가독성, 유지보수성, SOLID)
  - 성능 분석 (O(n^2) 최적화, N+1 쿼리, 메모리 누수)
  - OWASP Top 10 보안 취약점 감지
- **독립성**: 의존적 — 코드 및 테스트 필요
- **Harness 관련성**: Verify 단계 (V-1 품질 리뷰, V-2 테스트 검증)

#### 10. **Edge Case Reviewer** (edge-case-reviewer.md)
- **역할**: 엣지 케이스 및 경계 조건 전문 리뷰어. Null, 빈 컬렉션, 경계값, 동시성, 대용량 처리, 리소스 관리 중점 분석.
- **주요 역량**:
  - Null/Undefined 검증
  - 빈 컬렉션 처리
  - 경계값 (off-by-one, Max/Min, 정수 오버플로) 검증
  - 동시성 (레이스 컨디션, 데드락) 검증
  - 리소스 관리 (미해제 파일, DB 연결)
- **독립성**: 의존적 — 코드 필요
- **Harness 관련성**: Verify 단계 (V-1 품질 리뷰)

#### 11. **Logic Reviewer** (logic-reviewer.md)
- **역할**: 논리적 정합성 전문 리뷰어. 변수 흐름, 조건 분기, 반환값, 타입 일관성, 데드코드, 루프 로직 중점 분석.
- **주요 역량**:
  - 변수 흐름 추적 (초기화, 범위, 섀도잉)
  - 조건 분기 검증 (누락된 else, 불가능한 조건)
  - 반환값 검증 (모든 경로에서 올바른 타입)
  - 데드코드 식별
- **독립성**: 의존적 — 코드 필요
- **Harness 관련성**: Verify 단계 (V-1 품질 리뷰)

#### 12. **Security Reviewer** (security-reviewer.md)
- **역할**: 보안 취약점 전문 리뷰어. OWASP Top 10, 인증/인가, 민감 데이터 노출 중점 분석.
- **주요 역량**:
  - 인젝션 취약점 감지 (SQL, XSS, 명령어, 경로 탐색)
  - 인증/인가 검증 (우회, 권한 상승)
  - 민감 데이터 보호 (하드코딩, 로그 노출, 평문 전송)
  - 입력 검증 및 CORS/CSP
- **독립성**: 의존적 — 코드 필요
- **Harness 관련성**: Verify 단계 (V-1 품질 리뷰, V-6 보안 검증)

#### 13. **Quality Manager** (quality-manager.md)
- **역할**: 품질 관리 전문가. STEP-BY-STEP, TODO, CLEAR 프레임워크 준수 확인. 5단계 워크플로 검증, 품질 메트릭 모니터링, 종합 리뷰, 지속적 개선 권고.
- **주요 역량**:
  - 글로벌 원칙 준수 검증 (STEP-BY-STEP, TODO, CLEAR)
  - 5단계 워크플로 검증 (Understand/Explore/Select/Implement/Review)
  - 품질 메트릭 평가 (완전성, 정확성, 명확성, 일관성 각 1-10점)
  - 오류 감지 (논리, 사실, 일관성, 완전성, 맥락)
  - 개선 권고
- **독립성**: 독립적 — 다른 에이전트와 별도로 프로세스 검증
- **Harness 관련성**: Verify 단계 (V-1 품질 리뷰, V-7 프로세스 준수)

---

### 1.4 Analysis 에이전트 (분석/통찰)

#### 14. **Insight Explorer** (insight-explorer.md)
- **역할**: 깊은 관찰 및 패턴 인식 전문가. 5단계 이상 "Why?" 분석, 교차 도메인 연결, 인지 편향 최소화, 통합 이해 합성.
- **주요 역량**:
  - 깊은 관찰 ("Why?" 5회 반복)
  - 창의적 연결 (도메인 간 유사성)
  - 패턴 인식 (반복 구조, 근본 규칙)
  - 편향 최소화 (가정 명시, 반대 증거 추구, 다각적 관점)
- **독립성**: 독립적 — 단독 분석 가능
- **Harness 관련성**: Analysis 단계 (A-1 패턴 발견, A-2 근본 원인 분석)

#### 15. **Insight Amplifier** (insight-amplifier.md)
- **역할**: 인사이트 심화 전문가. 반복적 "Why/What-if/How-might-we" 질문, 5가지 관점 다양화(Skeptic/Optimist/Pragmatist/User/Critic), 3회 이상 반복 정제.
- **주요 역량**:
  - 깊이 있는 질문 ("Why" 5+회, "What-if", "How-might-we")
  - 관점 다양화 (5가지 이상)
  - 반복적 정제 (3회 이상)
  - 신뢰도 캘리브레이션 (1-10 신뢰도)
- **독립성**: 의존적 — Insight Explorer의 초기 발견 기반
- **Harness 관련성**: Analysis 단계 (A-1 인사이트 심화)

#### 16. **Multidimensional Analyst** (multidimensional-analyst.md)
- **역할**: 5차원 분석 전문가. 시간적(과거/현재/미래), 공간적(로컬/글로벌), 추상화 레벨(구체/추상), 인과관계, 규모별 분석으로 다각도 평가.
- **주요 역량**:
  - 5개 차원 분석 (시간, 공간, 추상화, 인과, 규모)
  - 각 차원 3개 이상 서브레벨 분석
  - 차원 간 패턴 및 모순 식별
  - 3-5개 핵심 발견사항 통합
- **독립성**: 독립적 — 다각도 분석 가능
- **Harness 관련성**: Analysis 단계 (A-2 다차원 분석)

#### 17. **Learning Evolver** (learning-evolver.md)
- **역할**: 학습 및 인지 발전 전문가. 현재 이해도 자기 평가, 지식 격차 식별, 메타인지 점검, 전략적 학습 경로 설계.
- **주요 역량**:
  - 4사분면 자기 평가 (Known-Known/Known-Unknown/Unknown-Known/Unknown-Unknown)
  - 지식 격차 식별 및 우선순위화
  - 메타인지 모니터링 (논리 오류, 인지 편향)
  - 구체적 다음 단계 정의
- **독립성**: 독립적 — 자가 진단 가능
- **Harness 관련성**: Analysis 단계 (A-3 학습 갭 분석)

#### 18. **Balanced Judge** (balanced-judge.md)
- **역할**: 의사결정 전문가. 체계적 분석과 직관적 도약 결합, 3-5개 대안 비교, 3회 이상 반복 검증, 신뢰도 명시.
- **주요 역량**:
  - 분석적 기반 구축 (컴포넌트 분해, 대안 열거)
  - 직관적 도약 (정적 사고, 경험 참조, 직관 신뢰)
  - 분석 + 직관 통합 (충돌 해결)
  - 4가지 검증 (논리, 완전성, 현실성, 대안 가능성)
- **독립성**: 독립적 — 의사결정 가능
- **Harness 관련성**: Plan 단계 (P-4 기술 선택), Execute 단계 (E-4 방향 결정)

#### 19. **Problem Reframer** (problem-reframer.md)
- **역할**: 문제 재정의 전문가. 관점 전환, 범위 조정, 메타 레벨 탐색, 도메인 전환, 제약 재검토를 통해 5가지 이상 재정의 제시.
- **주요 역량**:
  - 관점 전환 (180° 역설, 이해관계자 회전, 시간적 이동)
  - 범위 조정 (10배 확장, 1/10 축소)
  - 메타 레벨 네비게이션 (상향/하향)
  - 제약 재검토 (제약 제거 시나리오)
- **독립성**: 독립적 — 문제 재정의 가능
- **Harness 관련성**: Plan 단계 (P-5 문제 재해석)

#### 20. **Integrated Sage** (integrated-sage.md)
- **역할**: 통합 지혜 전문가. 지식(K) + 이해(U) + 지혜(W) + 공감(C) + 실행(A) × 겸손(H) × 윤리(E)의 공식으로 전략적 결정 지원.
- **주요 역량**:
  - 7가지 요소 균형 (K, U, W, C, A, H, E)
  - 공감 섹션 필수 (정서적 공명, 상황적 이해, 취약성 인식)
  - 윤리적 고려 (영향, 공정성, 투명성, 책임성, 지속가능성)
  - 실행 가능한 권고안
- **독립성**: 독립적 — 전략적 종합 가능
- **Harness 관련성**: Plan 단계 (P-1 비즈니스 목표), Verify 단계 (V-7 윤리 검증)

#### 21. **Connection Creator** (connection-creator.md)
- **역할**: 창의적 연결 전문가. 직접/간접 연결, 대조 분석, 역설적 연결, 메타포 구성, 시스템 관점으로 4가지 이상 연결 유형 탐색.
- **주요 역량**:
  - 직접 연결 (공유 특성, 기능 유사)
  - 대조 분석 (차이점, 보완 강점)
  - 간접 연결 (3단계 이상 다중 홉)
  - 역설적 연결 (양립 모순)
  - 메타포 구성
- **독립성**: 독립적 — 개념 간 연결 가능
- **Harness 관련성**: Analysis 단계 (A-2 크로스 도메인 분석)

#### 22. **Knowledge Mapper** (knowledge-mapper.md)
- **역할**: Obsidian 지식 구조 분석 및 시각화 전문가. 링크 네트워크 분석, 허브 문서 식별, 고립 문서 발견, Mermaid 맵 생성.
- **주요 역량**:
  - 링크 네트워크 분석 (직접 연결, 2-hop, 전체 경로)
  - 허브 문서 식별 (많은 링크 수신)
  - 고립 문서 발견 (링크 0개)
  - 지식 클러스터 발견
  - Mermaid 시각화
- **독립성**: 독립적 — Obsidian Vault 기반 분석
- **Harness 관련성**: Context Management (C-1 지식 맵)

---

### 1.5 Context Management 에이전트 (컨텍스트/기억)

#### 23. **Context Manager** (context-manager.md)
- **역할**: 에이전트 간 원활한 정보 흐름 보장 전문가. 요구사항/출력/중간결과/의사결정 근거 캡처, 의존성 관리, 메모리 최적화, 체크포인트 생성.
- **주요 역량**:
  - 포괄적 컨텍스트 캡처 (요구사항, 출력, 중간 결과, 의사결정)
  - 지능형 컨텍스트 필터링 (대상 에이전트에 필요한 정보만)
  - 의존성 추적 (순차/병렬/조건부)
  - 메모리 최적화 (압축, 선택적 보관, 체크포인트)
  - 상태 추적
- **독립성**: 조건부 — 전체 워크플로의 중추로 다른 에이전트와 협력
- **Harness 관련성**: Context Management (C-1 컨텍스트 관리, C-2 의존성 추적)

#### 24. **Session Memo Writer** (session-memo-writer.md)
- **역할**: Claude Code 세션 메모 자동 생성 전문가. 작업 내용 요약(3-5줄), 파일 수정 목록, 핵심 결정사항, 다음 TODO 기록으로 세션 간 컨텍스트 연속성 유지.
- **주요 역량**:
  - 빠른 세션 요약 (3-5줄)
  - 파일 수정 추적 (생성/업데이트/삭제)
  - 핵심 결정사항 기록 (1-3개)
  - 프로젝트 목표 carry forward
  - TODO 관리 (즉시/단기/중기/장기)
- **독립성**: 독립적 — 매 세션 종료 시 단독 실행
- **Harness 관련성**: Context Management (C-3 세션 메모, C-4 기억 연속성)

#### 25. **Memory Report Generator** (memory-report-generator.md)
- **역할**: AI 기억 시스템 전문가. 작업 진화 과정 상세 기록, 5단계 기억 계층 구현(사실/맥락/이유/과정/원리/진화), 미래 AI를 위한 시간 캡슐 생성.
- **주요 역량**:
  - 진화 과정 완전 기록 (v1→v2→v3 버전 추적)
  - 5단계 기억 계층 구현
  - 사용자 피드백 기반 전환점 식별
  - v1 vs v2 비교 분석
  - 시간 캡슐 메시지 (미래 AI 대상)
  - 작업 폴더 자동 감지
- **독립성**: 의존적 — Session Memo 또는 사용자 요청 기반
- **Harness 관련성**: Context Management (C-3 깊은 기억, C-4 학습 자료 생성)

---

### 1.6 Documentation 에이전트 (문서/조직)

#### 26. **Doc Indexer** (doc-indexer.md)
- **역할**: Obsidian 문서 인덱서. 폴더별 인덱스 파일 자동 생성/업데이트, 파일 목록 정리, 폴더 구조 시각화.
- **주요 역량**:
  - 인덱스 파일 자동 생성/업데이트
  - 파일 카테고리별 분류 (회의록, 요구사항, 작업 로그 등)
  - 날짜순/중요도순 정렬
  - 폴더 트리 구조 생성
  - 통계 정보 포함
- **독립성**: 독립적 — Obsidian Vault 자체 정리
- **Harness 관련성**: Documentation (D-1 문서 조직, D-2 인덱싱)

#### 27. **Link Doctor** (link-doctor.md)
- **역할**: Obsidian 양방향 링크 관리 전문가. 누락된 역링크 찾기, 깨진 링크 수정, 양방향 링크 일관성 보장.
- **주요 역량**:
  - 양방향 링크 검증 (A→B 시 B→A 확인)
  - 깨진 링크 탐지 (존재하지 않는 파일, 경로 오류)
  - 링크 품질 개선 (설명 텍스트, 경로 일관성)
  - "관련 문서" 섹션 자동 수정
- **독립성**: 독립적 — 링크 시스템 자체 관리
- **Harness 관련성**: Documentation (D-1 링크 관리)

#### 28. **Meeting Note Wizard** (meeting-note-wizard.md)
- **역할**: Obsidian 회의록 생성 마법사. 템플릿 자동 생성, 이전 회의록 자동 연결, 스마트 정보 자동 채우기, 액션 아이템 관리.
- **주요 역량**:
  - 프로젝트별 맞춤 템플릿 생성
  - 자동 번호 부여 (1차, 2차...)
  - 이전 회의록 링크 자동화
  - 참석자 목록 자동 승계
  - TODO 형식 액션 아이템
- **독립성**: 의존적 — 이전 회의록 조회 필요
- **Harness 관련성**: Documentation (D-2 회의록 관리)

#### 29. **Project Dashboard** (project-dashboard.md)
- **역할**: Obsidian 프로젝트 현황 대시보드 생성기. 프로젝트별 문서 통계, 최근 업데이트, 진행 상황(TODO 완료율)을 한눈에 시각화.
- **주요 역량**:
  - 프로젝트별 문서 수 계산
  - 완료율 계산 (TODO 비율)
  - 최근 7일/30일 활동 분석
  - 마크다운 표 형식 대시보드 생성
  - 우선순위 판단 및 인사이트 제시
- **독립성**: 독립적 — Vault 스캔 기반 분석
- **Harness 관련성**: Documentation (D-3 현황 추적)

#### 30. **Worklog Analyzer** (worklog-analyzer.md)
- **역할**: Obsidian 작업 로그 분석 전문가. 일일 로그 요약, 프로젝트별 시간 추적, 작업 패턴 분석, 생산성 인사이트 제공.
- **주요 역량**:
  - 작업 로그 요약 (일일→주간→월간)
  - 프로젝트별 작업 시간 추적
  - 작업 패턴 분석 (가장 생산적인 요일/시간)
  - 병목 구간 식별
  - 우선순위 재조정 제안
- **독립성**: 독립적 — 작업 로그 자체 분석
- **Harness 관련성**: Documentation (D-3 작업 추적)

---

## 2. 카테고리별 분포 요약

| 카테고리 | 에이전트 수 | 비율 | 에이전트명 |
|---------|-----------|------|----------|
| Planning (계획) | 5 | 17% | Requirements Analyst, Complexity Resolver, System Architect, Solution Innovator, Problem Reframer |
| Execution (실행) | 1 | 3% | Code Developer |
| Verification (검증) | 8 | 27% | Grader, Comparator, Eval Analyzer, Quality Reviewer, Edge Case Reviewer, Logic Reviewer, Security Reviewer, Quality Manager |
| Analysis (분석) | 9 | 30% | Insight Explorer, Insight Amplifier, Multidimensional Analyst, Learning Evolver, Balanced Judge, Integrated Sage, Connection Creator, Knowledge Mapper |
| Context Management (컨텍스트) | 3 | 10% | Context Manager, Session Memo Writer, Memory Report Generator |
| Documentation (문서) | 4 | 13% | Doc Indexer, Link Doctor, Meeting Note Wizard, Project Dashboard, Worklog Analyzer |
| **합계** | **30** | **100%** | - |

---

## 3. Harness 단계별 커버리지 분석

### Harness Elements (49개) 매핑

#### Plan Phase (계획 단계)
- **P-1 비즈니스 요구사항 명확화**: Requirements Analyst, Integrated Sage
- **P-2 기술 제약 및 위험 평가**: Requirements Analyst, Complexity Resolver
- **P-3 아키텍처 설계**: System Architect, Complexity Resolver
- **P-4 기술 결정 및 선택**: System Architect, Balanced Judge
- **P-5 솔루션/문제 도출**: Solution Innovator, Problem Reframer

**커버리지**: ✅ 양호 (5개 에이전트, 모든 P-요소 커버)

#### Execute Phase (실행 단계)
- **E-1 개발 구현**: Code Developer
- **E-2 단위 테스트**: Code Developer
- **E-3 통합 구현**: Code Developer, Solution Innovator (선택안 제시)
- **E-4 방향 결정/선택**: Balanced Judge

**커버리지**: ⚠️ 미흡 (Code Developer 주중심, 구현 도메인 제한)

#### Verify Phase (검증 단계)
- **V-1 품질 리뷰**: Quality Reviewer, Edge Case Reviewer, Logic Reviewer, Security Reviewer, Quality Manager
- **V-2 테스트 실행**: Grader, Quality Reviewer
- **V-3 회귀 감지**: Comparator, Grader
- **V-4 버전 비교**: Comparator
- **V-5 근본 원인 분석**: Eval Analyzer
- **V-6 보안 검증**: Security Reviewer
- **V-7 프로세스 준수**: Quality Manager

**커버리지**: ✅ 매우 양호 (8개 에이전트, 모든 V-요소 고도로 커버)

#### Analysis (분석/통찰)
- **A-1 패턴 발견/심화**: Insight Explorer, Insight Amplifier
- **A-2 다차원/크로스 도메인 분석**: Multidimensional Analyst, Connection Creator
- **A-3 학습 갭 분석**: Learning Evolver

**커버리지**: ✅ 양호 (9개 에이전트 지원)

#### Context Management (컨텍스트 관리)
- **C-1 컨텍스트 관리**: Context Manager, Knowledge Mapper
- **C-2 의존성 추적**: Context Manager
- **C-3 세션 메모/깊은 기억**: Session Memo Writer, Memory Report Generator
- **C-4 기억 연속성/학습 자료**: Session Memo Writer, Memory Report Generator

**커버리지**: ✅ 양호 (3개 에이전트, 핵심 기능 모두 커버)

#### Documentation (문서화)
- **D-1 문서 조직/인덱싱/링크**: Doc Indexer, Link Doctor, Knowledge Mapper
- **D-2 회의록 관리**: Meeting Note Wizard
- **D-3 현황 추적/작업 분석**: Project Dashboard, Worklog Analyzer

**커버리지**: ✅ 양호 (5개 에이전트)

---

## 4. 주요 발견사항 및 패턴

### 4.1 강점 (Strengths)

1. **검증 중심 설계**: 30%의 에이전트가 검증/품질 업무 전담
   - 품질 게이트: Grader → Comparator → Eval Analyzer 체인
   - 다각도 리뷰: Quality Reviewer, Edge Case, Logic, Security 독립적 검토
   - 메타 검증: Quality Manager가 프로세스 전체 감시

2. **분석 깊이**: 30%의 에이전트가 심화 분석
   - 인사이트 연쇄: Explorer → Amplifier → 다차원 분석
   - 학습 기반: Learning Evolver가 갭 식별
   - 통합 판단: Integrated Sage가 최종 의사결정 지원

3. **컨텍스트 연속성**: 기억과 메모리 시스템 구축
   - 세션 메모 자동화 (Session Memo Writer)
   - 심층 기억 생성 (Memory Report Generator)
   - 컨텍스트 관리 (Context Manager)

4. **문서 생태계**: Obsidian 기반 완전한 문서 자동화
   - 인덱싱/링크/현황/로그 분석 통합
   - 양방향 링크 일관성 관리

### 4.2 약점 (Weaknesses)

1. **Execution 에이전트 부족**
   - Code Developer 1개만 존재
   - DB 설계, API 개발, DevOps 등 특화 에이전트 부재
   - 제안: Database Architect, API Designer, DevOps Engineer 추가 필요

2. **Plan → Execute 브릿지 부재**
   - Solution Innovator는 아이디어 생성, 구현 가이드 부족
   - 제안: Implementation Planner 에이전트 추가 필요

3. **실시간 모니터링 부재**
   - 진행 중 즉각적인 피드백 메커니즘 부족
   - 제안: Real-time Monitor / Progressive Reviewer 추가 필요

---

## 5. 에이전트 체인 및 협력 패턴

### 5.1 주요 에이전트 체인

#### 체인 1: 계획 → 실행 → 검증 (Plan-Execute-Verify)
```
Requirements Analyst
  ↓ (요구사항)
System Architect
  ↓ (설계)
Code Developer
  ↓ (구현)
Quality Reviewer + Edge Case Reviewer + Logic Reviewer + Security Reviewer
  ↓ (리뷰)
Grader
  ↓ (채점)
Comparator
  ↓ (버전 비교)
Eval Analyzer (실패 시)
```

#### 체인 2: 문제 분석 → 해결책 도출 → 평가 (Analysis-Solution-Judge)
```
Insight Explorer
  ↓ (패턴 발견)
Insight Amplifier
  ↓ (심화)
Multidimensional Analyst
  ↓ (다차원 분석)
Solution Innovator
  ↓ (솔루션 생성)
Balanced Judge
  ↓ (최적안 선택)
```

#### 체인 3: 컨텍스트 관리 (계속)
```
Context Manager (상태 추적)
  ↓
Session Memo Writer (세션 종료 시)
  ↓ (사용자 요청 시)
Memory Report Generator (심층 기억)
```

### 5.2 협력 의존성 매트릭스

| 에이전트 | 의존성 | 공급자 |
|---------|--------|--------|
| System Architect | Requirements Analyst | 요구사항 입력 |
| Code Developer | System Architect | 아키텍처 설계 |
| Quality Reviewer | Code Developer | 코드 리뷰 대상 |
| Grader | 에이전트 출력 | eval_test.json |
| Comparator | Grader × 2 | 두 버전 평가 결과 |
| Eval Analyzer | Grader | 실패 케이스 분석 |
| Solution Innovator | Requirements | 아이디어 생성 |
| Insight Amplifier | Insight Explorer | 초기 발견 심화 |
| Memory Report | Session Memo | 세션 메모 입력 |
| Meeting Note Wizard | 이전 회의록 | 참석자 정보 |

---

## 6. 독립성 분류

### 독립적 에이전트 (11개)
순수 분석, 재정의, 검증, 문서 조직 가능
- Complexity Resolver, Insight Explorer, Insight Amplifier
- Multidimensional Analyst, Learning Evolver, Balanced Judge
- Problem Reframer, Integrated Sage, Connection Creator
- Doc Indexer, Link Doctor, Knowledge Mapper
- Worklog Analyzer, Project Dashboard

### 의존적 에이전트 (15개)
다른 에이전트 산출물 필요
- System Architect (← Requirements)
- Code Developer (← System Architect)
- Quality Reviewer, Edge Case, Logic, Security (← Code)
- Grader (← eval_test.json)
- Comparator (← Grader × 2)
- Eval Analyzer (← Grader 실패)
- Insight Amplifier (← Explorer)
- Memory Report (← Session Memo)
- Meeting Note Wizard (← 이전 회의록)

### 조건부 독립 (4개)
특정 조건에서 독립적/의존적
- Requirements Analyst: 초기 독립, 이후 Architect와 협력
- Solution Innovator: 요구사항 이해 후 독립 가능
- Context Manager: 워크플로 중추로 모든 에이전트와 협력
- Session Memo Writer: 사용자 요청 시 독립 실행

---

## 7. Harness 통합 권고안

### 단계별 에이전트 배치 (최적 활용)

#### Plan Phase
1. **초기**: Requirements Analyst → Complexity Resolver 병렬
2. **설계**: System Architect (Integrated Sage 지원)
3. **솔루션**: Solution Innovator → Problem Reframer (대안 탐색)
4. **선택**: Balanced Judge (최적안 결정)

#### Execute Phase
1. **구현**: Code Developer (TDD 적용)
2. **지원**: Connection Creator (도메인 간 아이디어) / Learning Evolver (갭 채우기)

#### Verify Phase
1. **병렬 리뷰**: Quality Reviewer / Edge Case / Logic / Security (4개 동시)
2. **프로세스**: Quality Manager (STEP/TODO/CLEAR 감시)
3. **채점**: Grader (eval_test.json 대조)
4. **비교**: Comparator (회귀 감지)
5. **분석**: Eval Analyzer (실패 원인)

#### Analysis/Context
1. **분석**: Insight Explorer → Amplifier → Multidimensional
2. **메모**: Session Memo Writer (세션 종료)
3. **기억**: Memory Report Generator (중요 세션)
4. **관리**: Context Manager (상태 추적)

#### Documentation
1. **조직**: Doc Indexer (폴더별 인덱스)
2. **링크**: Link Doctor (양방향 링크)
3. **회의**: Meeting Note Wizard (정기적)
4. **현황**: Project Dashboard + Worklog Analyzer (주/월간)

---

## 8. 향후 개선 제안

### 추가 필요 에이전트 (3-5개)

1. **Database Architect** (Execution 강화)
   - DB 스키마 설계, 정규화, 성능 최적화
   - 카테고리: Execution

2. **API Designer** (Execution 강화)
   - REST/GraphQL/gRPC API 계약 설계
   - 카테고리: Execution

3. **Implementation Planner** (Plan-Execute 브릿지)
   - 설계를 구현 로드맵으로 변환
   - 마일스톤, 의존성, 타임라인 수립
   - 카테고리: Planning

4. **Progressive Reviewer** (실시간 검증)
   - 진행 중 점진적 피드백
   - 주요 체크포인트 검증
   - 카테고리: Verification

5. **Integration Validator** (Verification 강화)
   - 마이크로서비스 간 통합 검증
   - E2E 테스트 설계
   - 카테고리: Verification

---

## 9. 상세 에이전트 스펙 (빠른 참고)

| # | 에이전트 | 모델 | 색상 | 복잡도 | 독립도 |
|----|---------|------|------|--------|--------|
| 1 | Requirements Analyst | opus | blue | 높음 | 조건부 |
| 2 | Complexity Resolver | opus | brown | 높음 | 독립 |
| 3 | System Architect | opus | blue | 높음 | 의존 |
| 4 | Code Developer | - | green | 중간 | 의존 |
| 5 | Solution Innovator | opus | red | 높음 | 조건부 |
| 6 | Grader | opus | - | 중간 | 의존 |
| 7 | Comparator | opus | - | 중간 | 의존 |
| 8 | Eval Analyzer | opus | - | 높음 | 의존 |
| 9 | Quality Reviewer | - | red | 높음 | 의존 |
| 10 | Edge Case Reviewer | opus | - | 높음 | 의존 |
| 11 | Logic Reviewer | opus | - | 높음 | 의존 |
| 12 | Security Reviewer | opus | - | 높음 | 의존 |
| 13 | Quality Manager | - | gold | 높음 | 독립 |
| 14 | Insight Explorer | sonnet | purple | 높음 | 독립 |
| 15 | Insight Amplifier | opus | cyan | 높음 | 의존 |
| 16 | Multidimensional Analyst | opus | green | 높음 | 독립 |
| 17 | Learning Evolver | opus | indigo | 중간 | 독립 |
| 18 | Balanced Judge | opus | teal | 높음 | 독립 |
| 19 | Problem Reframer | opus | yellow | 높음 | 독립 |
| 20 | Integrated Sage | opus | gold | 높음 | 독립 |
| 21 | Connection Creator | opus | orange | 높음 | 독립 |
| 22 | Knowledge Mapper | - | purple | 중간 | 독립 |
| 23 | Context Manager | - | purple | 높음 | 조건부 |
| 24 | Session Memo Writer | - | magenta | 낮음 | 조건부 |
| 25 | Memory Report Generator | - | red | 높음 | 의존 |
| 26 | Doc Indexer | - | green | 중간 | 독립 |
| 27 | Link Doctor | - | blue | 중간 | 독립 |
| 28 | Meeting Note Wizard | - | yellow | 중간 | 의존 |
| 29 | Project Dashboard | - | cyan | 중간 | 독립 |
| 30 | Worklog Analyzer | - | orange | 중간 | 독립 |

---

## 10. 결론

### 핵심 특징

1. **검증 중심**: Harness의 Verify 단계를 가장 철저히 지원
2. **분석 깊이**: 패턴 발견부터 통합 판단까지 레이어드 분석
3. **기억 시스템**: AI 학습을 위한 기억과 컨텍스트 연속성 구현
4. **문서 자동화**: Obsidian 기반 완전 생태계

### 개선 방향

- **Execution 강화**: 1개 → 4-5개 에이전트로 확대 필요
- **Plan-Execute 브릿지**: Implementation Planner 추가
- **실시간 검증**: Progressive Reviewer 도입
- **통합 검증**: Integration Validator 추가

### 활용 시나리오

✅ 요구사항 명확화 → ✅ 아키텍처 설계 → ✅ 구현 → ✅ 다각도 검증 → ✅ 원인 분석 → ✅ 기억 저장 → ✅ 문서 조직

이 30개 에이전트는 **요구사항 분석에서 문서화까지 전체 소프트웨어 생명주기(SDLC)를 지원하는 통합 시스템**을 형성합니다.

---

**카탈로그 작성**: Claude Code Agent System
**분석 범위**: 30개 에이전트 전수 조사
**검증 방식**: 각 .md 파일 직접 읽음 및 분석
