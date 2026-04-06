# Phase 7: 최종 출력 — 글로벌 CLAUDE.md 완성 보고서

## 1. 최종 파일 정보

| 항목 | 값 |
|------|-----|
| 파일명 | `FINAL_GLOBAL_CLAUDE_MD.md` |
| 배치 경로 | `~/.claude/CLAUDE.md` (`C:\Users\name\.claude\CLAUDE.md`) |
| 총 줄 수 | 141줄 (200줄 제한 대비 여유 59줄) |
| 섹션 수 | 8개 (Persona, Thinking, Workflow, Context, Code & Quality, Security, Language, Self-Maintenance) |
| 버전 | v1.0 (2026-04-03) |
| 설계 기반 | 6개 Harness Engineering 분석 리포트 |

---

## 2. 최종 검증 결과 요약표 (Phase 5 Re-verify 결과)

| # | 검증 관점 | 결과 | 핵심 근거 |
|---|-----------|------|-----------|
| 1 | **공식 제약 준수** | ✅ 통과 | 141줄 (< 200), 프로젝트 특화 없음, "IMPORTANT" 2회만 사용 (보안·검증), 모순 없음 |
| 2 | **페르소나 일관성** | ✅ 통과 | 앤(PM+기획+바이브코더), 미르(AI파트너), 공공SI 맥락 자연 반영 |
| 3 | **하네스 기능** | ✅ 통과 | 시나리오 A~D 모두 통과: 신규 프로젝트 시작, 프론트 개발 중 가이드, "숙지해줘"→"예", /compact 후 핵심 보존 |
| 4 | **Report 1~5 원칙 반영** | ✅ 통과 | R01: Context Anxiety 해결(세션관리+progress log), R02: Skills/Compaction, R03: Subagent 위임, R04: 3-tier context 관리, R05: 의도적 미포함 (vendor-specific 파일에 vendor-agnostic 원칙 모순) |
| 5 | **Report_06 공식 가이드** | ✅ 통과 | 포함 항목 전수 충족, 금지 항목 위반 없음, 글로벌/프로젝트 scope 분리 완벽 |
| 6 | **토큰 효율성** | ✅ 통과 | 불필요 문장 0건, 모든 줄이 "삭제 시 실수 유발" 테스트 통과, Auto Memory 위임 대상 없음 |
| 7 | **보안·감사 적합성** | ✅ 통과 | 민감 정보 없음, credential·개인정보·GPL 규칙 포함, Hooks/Permissions 분리 제안 HTML 주석 포함 |

**전체 판정: 7/7 통과 → Phase 6(재수정) 생략, Phase 7 진입**

---

## 3. `~/.claude/rules/` 디렉토리 구조 제안

```
~/.claude/
├── CLAUDE.md                          ← 글로벌 하네스 (이번에 작성한 파일)
├── rules/
│   ├── security.md                    ← 보안 강화 규칙 (paths: "**/*")
│   │   # credential 하드코딩 감지 시 경고
│   │   # .env 파일 커밋 차단 안내
│   │   # 민감 데이터 패턴 감지
│   │
│   ├── frontend.md                    ← 프론트엔드 규칙 (paths: "**/*.{tsx,jsx,vue,svelte}")
│   │   # 컴포넌트 구조, 상태 관리 패턴
│   │   # 접근성(a11y) 체크리스트
│   │   # CSS/Tailwind 컨벤션
│   │
│   ├── backend.md                     ← 백엔드 규칙 (paths: "**/*.{java,py,ts}")
│   │   # API 설계 패턴 (REST/GraphQL)
│   │   # 에러 핸들링 표준
│   │   # DB 쿼리 성능 가이드
│   │
│   ├── documentation.md               ← 문서 작성 규칙 (paths: "**/*.md")
│   │   # 공공기관 문서 표준 양식
│   │   # 변경 이력 기록 방식
│   │   # 다이어그램 작성 도구 (Mermaid 등)
│   │
│   └── testing.md                     ← 테스트 규칙 (paths: "**/*.{test,spec}.*")
│       # 테스트 네이밍 컨벤션
│       # 단위/통합/E2E 구분 기준
│       # 커버리지 목표
│
├── settings.json                      ← Hooks/Permissions 설정
│   # PreCommit hook: lint + typecheck 강제
│   # 민감 파일 커밋 차단 hook
│
└── skills/                            ← 재사용 가능한 워크플로우
    ├── code-review/SKILL.md           ← 코드 리뷰 절차
    ├── si-documentation/SKILL.md      ← 공공SI 산출물 작성 절차
    └── db-design/SKILL.md             ← DB 설계 절차
```

**참고**: 각 `rules/*.md` 파일은 YAML frontmatter의 `paths:` 필드로 적용 범위를 지정합니다. 파일 내용은 프로젝트별로 다를 수 있으므로 여기서는 구조와 역할만 제안합니다.

---

## 4. 프로젝트별 `./CLAUDE.md` 포함 항목 체크리스트

글로벌 CLAUDE.md와 함께, 각 프로젝트의 루트에 `./CLAUDE.md`를 생성할 때 아래 항목을 포함하세요.

### 필수 항목

- [ ] **기술 스택 선언**: 사용 언어, 프레임워크, 주요 라이브러리 버전
- [ ] **빌드/실행 명령어**: `npm run dev`, `./gradlew build` 등 프로젝트 고유 명령어
- [ ] **테스트 명령어**: 단위 테스트, 통합 테스트, E2E 테스트 실행 방법
- [ ] **프로젝트 디렉토리 구조**: 주요 디렉토리와 역할 설명
- [ ] **아키텍처 결정 사항**: 선택한 패턴과 그 이유 (예: Hexagonal, MVC, CQRS)
- [ ] **환경 설정**: 개발/스테이징/운영 환경 구분, 환경변수 목록 (값 제외)

### 권장 항목

- [ ] **코딩 컨벤션 오버라이드**: 글로벌 규칙과 다른 프로젝트 고유 규칙
- [ ] **DB 스키마 위치**: ERD 파일 경로, 마이그레이션 도구
- [ ] **API 문서 위치**: Swagger/OpenAPI spec 경로
- [ ] **배포 절차**: CI/CD 파이프라인 정보, 배포 브랜치 전략
- [ ] **알려진 gotchas**: 프로젝트 고유 함정, 주의사항
- [ ] **이해관계자 정보**: 발주처 요구사항 문서 위치, 주요 협의 사항

### 공공기관 SI 특화 항목

- [ ] **보안 등급/요구사항**: 프로젝트별 보안 수준, 인증 방식
- [ ] **감사 로그 규격**: 로그 포맷, 보존 기간, 필수 기록 항목
- [ ] **표준 프레임워크 정보**: 전자정부 프레임워크 버전, 적용 범위
- [ ] **산출물 목록**: 프로젝트에서 요구하는 문서 산출물 리스트
- [ ] **코드 품질 기준**: 정적 분석 도구, 커버리지 목표, 코드 리뷰 절차

---

## 적용 방법

1. `FINAL_GLOBAL_CLAUDE_MD.md` 파일을 `C:\Users\name\.claude\CLAUDE.md` 경로에 복사
2. 기존 `~/.claude/CLAUDE.md`가 있다면 백업 후 교체
3. Claude Code 새 세션 시작 시 자동 로딩 확인
4. 필요에 따라 `~/.claude/rules/` 디렉토리 생성 및 규칙 파일 추가
5. 각 프로젝트에서 위 체크리스트를 참고하여 `./CLAUDE.md` 작성
