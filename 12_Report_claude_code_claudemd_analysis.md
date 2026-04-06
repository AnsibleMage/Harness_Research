# 06_Anthropic Claude Code CLAUDE.md 공식 문서 — 심층 분석 리포트

> **분석 목적**: 글로벌 CLAUDE.md (`~/.claude/CLAUDE.md`) 하네스 구축을 위한 공식 문서 기반 철저 분석
> **분석 관점**: 공공기관 SI PM + 바이브코딩 워크플로우 + 개인 로컬 AI 에이전트 하네스
> **원천 문서**: 06번 문서 + 공식 링크 4개 (memory, best-practices, claude-directory, overview)
> **분석자**: Mir (Ann의 AI 파트너)
> **작성일**: 2026-04-03

---

## 1. CLAUDE.md의 정의와 목적

### 1.1 공식 정의

CLAUDE.md는 Claude Code가 **매 세션 시작 시 자동으로 읽어들이는 마크다운 파일**이다. 사용자가 직접 작성하며, Claude에게 장기적·프로젝트 특화적인 규칙, 코딩 표준, 아키텍처 결정, 워크플로우, 제약사항을 전달하는 **핵심 메커니즘**이다.

공식 문서의 핵심 표현:

- "CLAUDE.md is the most powerful tool for giving Claude persistent context across sessions"
- "Claude reads them at the start of every session"
- "They're context rather than enforced configuration"

### 1.2 핵심 특성 분석

| 특성 | 상세 |
|------|------|
| **작성 주체** | 사용자(You) — Claude가 아닌 인간이 직접 작성 |
| **내용 성격** | 지시(Instructions)와 규칙(Rules) |
| **로딩 시점** | 매 세션 시작 시 전체 내용 로딩 |
| **기술적 위치** | System prompt 이후 user message로 주입됨 |
| **강제성** | **Advisory(권고)** — 설정 강제가 아닌 행동 가이드 |
| **생존 범위** | `/compact` 이후에도 완전 생존 (디스크에서 재로딩) |

### 1.3 앤(Ann) 글로벌 CLAUDE.md 하네스 관점 인사이트

CLAUDE.md는 단순한 "메모 파일"이 아니라 **하네스의 핵심 제어 파일**이다. 공식 문서에서 "the most powerful tool"이라고 표현한 것은, 이것이 Claude의 모든 세션에 걸쳐 일관된 행동을 유도하는 **유일한 영속적 지시 메커니즘**이기 때문이다.

공공기관 SI 프로젝트에서 이것의 의미는:

- **감사 대응**: Claude가 따라야 할 코딩 표준, 보안 규칙, 문서화 규범을 명시적으로 기록 → 감사 시 "AI가 어떤 규칙을 따랐는가"에 대한 증빙
- **일관성 보장**: PM이 여러 프로젝트를 동시에 관리할 때, 글로벌 CLAUDE.md를 통해 **모든 프로젝트에 공통 기준**을 적용
- **하네스 관점**: Anthropic의 harness engineering 문서에서 말하는 "Initializer Agent"의 역할을 CLAUDE.md가 수행 — 매 세션마다 환경 세팅을 자동화

**중요 경고**: "advisory"라는 점에 주의해야 한다. CLAUDE.md 내용이 너무 길거나 모호하면 Claude가 임의로 무시할 수 있다. 따라서 강제 실행이 필요한 규칙은 **Hooks**(deterministic 실행)나 **Permissions**(settings.json)로 분리해야 한다.

---

## 2. CLAUDE.md 로드 방식, 범위(Scope), 우선순위, 글로벌 적용 방법

### 2.1 로딩 메커니즘 상세

Claude Code는 현재 작업 디렉토리에서 **상위 방향으로 트리를 탐색(walk up)**하며 모든 CLAUDE.md를 수집한다.

```
예: /home/ann/projects/si-portal/src/components/ 에서 작업 시

로딩되는 파일 (하위 → 상위 순):
1. /home/ann/projects/si-portal/src/components/CLAUDE.md (있다면)
2. /home/ann/projects/si-portal/src/CLAUDE.md (있다면)
3. /home/ann/projects/si-portal/CLAUDE.md ← 프로젝트 레벨
4. /home/ann/projects/CLAUDE.md (있다면)
5. ~/.claude/CLAUDE.md ← 글로벌 유저 레벨
6. /Library/Application Support/ClaudeCode/CLAUDE.md ← 조직 정책 레벨 (macOS)
```

**하위 디렉토리 CLAUDE.md**: 세션 시작 시 로딩되지 않음. Claude가 해당 하위 디렉토리의 파일을 읽을 때 **on-demand**로 로딩됨.

### 2.2 4개 Scope와 우선순위

| 우선순위 | Scope | 경로 | 목적 | 공유 범위 |
|----------|-------|------|------|-----------|
| **1 (최상)** | Managed Policy | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br>Linux/WSL: `/etc/claude-code/CLAUDE.md`<br>Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | 조직 전체 강제 지침 (IT/DevOps 관리) | 조직 내 모든 사용자 |
| **2** | Project | `./CLAUDE.md` 또는 `./.claude/CLAUDE.md` | 프로젝트 팀 공유 지침 | 팀원 (git 커밋) |
| **3** | User (글로벌) | `~/.claude/CLAUDE.md` | 개인 전체 프로젝트 공통 선호 | 본인만 (전 프로젝트) |
| **4** | Subdirectory | 하위 폴더의 CLAUDE.md | 특정 모듈/디렉토리 전용 | 프로젝트 내부 |

**핵심**: 더 구체적(specific)한 위치의 지침이 더 넓은 범위의 지침보다 **우선**한다.

### 2.3 글로벌 CLAUDE.md (`~/.claude/CLAUDE.md`) 적용 방법

공식 문서에 따르면:

- **위치**: `~/.claude/CLAUDE.md` (Windows에서는 `C:\Users\name\.claude\CLAUDE.md`)
- **적용 범위**: 해당 사용자의 **모든** Claude Code 세션에 자동 적용
- **사용 용도**: 프로젝트에 무관한 개인 선호도, 개인 툴링 단축키, 코딩 스타일 선호도
- **공유**: 본인만 사용, git에 커밋되지 않음

### 2.4 앤(Ann) 글로벌 CLAUDE.md 하네스 관점 인사이트

글로벌 CLAUDE.md는 앤의 **모든 프로젝트에 걸친 하네스의 뿌리**가 된다. 구체적으로:

- **바이브코딩 워크플로우**: 기획 → 디자인 → 개발 → Git 운영의 전체 흐름을 글로벌에 정의하면, 어떤 프로젝트를 열든 동일한 작업 패턴 유지
- **공공기관 SI 공통 규칙**: 보안 정책, 문서화 규범, 명명 규칙 등 SI 사업 전반에 걸친 규칙은 글로벌에 배치
- **프로젝트 고유 사항은 분리**: 각 SI 프로젝트의 고유 아키텍처, 기술 스택은 프로젝트 레벨 CLAUDE.md에 배치
- **Scope 충돌 방지**: 글로벌에는 "이것을 해라"보다 "이것을 항상 지켜라"(불변 원칙)를 배치하고, 프로젝트 레벨에서 구체 실행 방법을 정의

```
~/.claude/CLAUDE.md          ← 앤의 페르소나, 워크플로우, 불변 원칙
├── 프로젝트A/CLAUDE.md       ← 프로젝트A 고유 기술 스택, 아키텍처
├── 프로젝트B/CLAUDE.md       ← 프로젝트B 고유 사항
└── 프로젝트A/src/api/CLAUDE.md ← API 모듈 전용 규칙 (on-demand 로딩)
```

---

## 3. CLAUDE.md vs Auto Memory 비교와 각각의 역할

### 3.1 공식 비교표 (확장판)

| 항목 | CLAUDE.md | Auto Memory |
|------|-----------|-------------|
| **작성 주체** | 사용자(You) | Claude (자동) |
| **내용 성격** | 지시(Instructions)와 규칙(Rules) | 학습(Learnings)과 패턴(Patterns) |
| **적용 범위** | Project / User / Organization | Per working tree (git repo 기반) |
| **로딩 방식** | 매 세션 시작 시 **전체 내용** 로딩 | 매 세션 시작 시 **MEMORY.md 첫 200줄 또는 25KB** 로딩 |
| **저장 위치** | 프로젝트 루트 또는 `~/.claude/` | `~/.claude/projects/<project>/memory/` |
| **용도** | 코딩 표준, 워크플로우, 아키텍처 결정 | 빌드 명령어, 디버깅 인사이트, Claude가 발견한 선호도 |
| **수정 방법** | 직접 편집 | `/memory` 명령으로 열람/편집 또는 Claude에게 "remember this" 요청 |
| **git 관리** | 프로젝트 레벨은 git 커밋 권장 | machine-local, git에 포함되지 않음 |
| **compaction 생존** | **완전 생존** (디스크에서 재로딩) | MEMORY.md는 생존, 대화 중 학습은 소실 가능 |

### 3.2 Auto Memory 작동 방식 상세

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          ← 인덱스 (매 세션 시작 시 첫 200줄 로딩)
├── debugging.md       ← 디버깅 패턴 상세 (on-demand 로딩)
├── api-conventions.md ← API 설계 결정 (on-demand 로딩)
└── ...
```

- MEMORY.md가 인덱스 역할, 상세 토픽은 별도 파일로 분리
- Claude가 세션 중 "Writing memory" / "Recalled memory" 메시지 표시
- 매 세션마다 저장하지 않음 — Claude가 "미래 대화에서 유용할지" 판단 후 선택적 저장
- `autoMemoryEnabled: false`로 비활성화 가능

### 3.3 두 시스템의 상호 보완 관계

```
┌─────────────────────────────────────────────────┐
│                  Claude 세션                      │
│                                                   │
│  ┌──────────────────┐  ┌──────────────────────┐  │
│  │   CLAUDE.md       │  │    Auto Memory        │  │
│  │   (사용자 의도)   │  │   (Claude 학습)       │  │
│  │                   │  │                       │  │
│  │ "이렇게 해라"     │  │ "이전에 이랬더라"     │  │
│  │ = 규범/원칙       │  │ = 경험/패턴           │  │
│  └──────────────────┘  └──────────────────────┘  │
│                    ↓                               │
│           Claude의 행동 결정                       │
└─────────────────────────────────────────────────┘
```

### 3.4 앤(Ann) 글로벌 CLAUDE.md 하네스 관점 인사이트

**역할 분리 전략**:

- **CLAUDE.md** (앤이 직접 통제): 페르소나 정의, 워크플로우 규칙, 보안 정책, 코딩 표준, 아키텍처 원칙 → "이것은 변하지 않는 규범"
- **Auto Memory** (Claude가 자동 축적): 프로젝트별 빌드 명령어, 디버깅에서 발견한 패턴, 앤의 선호도 학습 → "이것은 경험에서 온 노하우"

**공공기관 SI 관점 주의사항**:

- Auto Memory는 machine-local이므로, 여러 머신에서 작업할 경우 학습 내용이 동기화되지 않음
- 민감한 프로젝트 정보가 Auto Memory에 자동 저장될 수 있으므로, 주기적으로 `/memory`로 검토 필요
- CLAUDE.md에는 "감사 대응 가능한 명시적 규칙"을, Auto Memory에는 "일상적 작업 효율화 학습"을 분리

---

## 4. 공식 추천 작성 원칙

### 4.1 길이 (Size)

| 공식 권장 | 상세 |
|-----------|------|
| **200줄 이하** 권장 | 더 긴 파일도 전체 로딩되지만 **준수율(adherence) 저하** |
| 길어지면 분할 | `@path` 임포트 또는 `.claude/rules/` 활용 |
| 토큰 비용 | 매 세션 context window에 전체 주입 → 길수록 대화 가용 토큰 감소 |

**공식 경고**: "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" — 비대한 파일은 실제 지시를 무시하게 만든다.

### 4.2 구조 (Structure)

- **마크다운 헤더**(`#`, `##`)와 **bullet point**로 관련 지시를 그룹핑
- Claude는 인간 독자와 동일하게 구조를 스캔 — 밀집된 단락보다 조직화된 섹션이 더 효과적
- 공식 예시 구조:

```markdown
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, not the whole test suite, for performance
```

### 4.3 구체성 (Specificity)

**공식 원칙**: "Write instructions that are concrete enough to verify"

| 나쁜 예 | 좋은 예 |
|---------|---------|
| "Format code properly" | "Use 2-space indentation" |
| "Test your changes" | "Run `npm test` before committing" |
| "Keep files organized" | "API handlers live in `src/api/handlers/`" |
| "Write clean code" | "Named exports, never default exports" |

### 4.4 일관성 (Consistency)

- 두 규칙이 모순되면 Claude가 **임의로 하나를 선택**할 수 있음
- CLAUDE.md, 하위 디렉토리 CLAUDE.md, `.claude/rules/`를 주기적으로 검토하여 모순/구식 규칙 제거
- 모노레포에서는 `claudeMdExcludes`로 다른 팀의 CLAUDE.md 제외

### 4.5 강조 (Emphasis)

- 중요 지시에 **"IMPORTANT"** 또는 **"YOU MUST"** 를 추가하면 준수율 향상
- 단, 남용하면 효과 희석 → 진짜 중요한 규칙에만 사용

### 4.6 유지보수 원칙

공식 문서의 핵심 조언: **"Treat CLAUDE.md like code"**

- 문제 발생 시 CLAUDE.md를 리뷰
- 정기적으로 pruning
- 변경 후 Claude 행동이 실제로 바뀌는지 관찰하여 테스트
- git에 커밋하여 팀 기여 가능 → 시간이 갈수록 가치 축적

### 4.7 앤(Ann) 글로벌 CLAUDE.md 하네스 관점 인사이트

**글로벌 CLAUDE.md 특화 작성 전략**:

- 글로벌은 **모든 프로젝트에 적용**되므로, 프로젝트 특화 내용은 절대 포함하지 않음
- 200줄 제한 내에서 "앤의 페르소나 + 불변 워크플로우 + 언어 규칙 + 핵심 보안 원칙"에 집중
- 프로젝트별 세부 사항은 각 프로젝트의 CLAUDE.md 또는 `.claude/rules/`로 분리
- 각 줄마다 자문: "이 지시를 제거하면 Claude가 실수할 것인가?" — 아니면 삭제

**강조 전략**: 절대 위반하면 안 되는 보안 규칙(예: 민감 데이터 처리)에만 "IMPORTANT" / "YOU MUST" 사용

---

## 5. 포함해야 할 내용과 피해야 할 내용 (공식 체크리스트)

### 5.1 포함해야 할 내용 (✅)

| 항목 | 설명 | 앤의 적용 예시 |
|------|------|----------------|
| **Claude가 추측할 수 없는 Bash 명령** | 빌드, 테스트, 배포 명령 | `npm run build:prod`, `pnpm test --coverage` |
| **기본값과 다른 코드 스타일 규칙** | 프로젝트 고유 컨벤션 | "Use 2-space indentation, semicolons required" |
| **테스트 지침과 선호 테스트 러너** | 테스트 실행 방법 | "Use vitest, run single test files for speed" |
| **레포지토리 에티켓** | 브랜치 명명, PR 규범 | "Branch: feature/JIRA-123-desc, PR template required" |
| **프로젝트 고유 아키텍처 결정** | 설계 원칙 | "Hexagonal architecture, ports-and-adapters" |
| **개발 환경 특이사항** | 필수 환경변수 등 | "Required: NEXT_PUBLIC_API_URL in .env.local" |
| **일반적이지 않은 동작(gotcha)** | 함정, 주의사항 | "DB migration은 반드시 수동 실행, 자동 실행 금지" |

### 5.2 피해야 할 내용 (❌)

| 항목 | 이유 | 대안 |
|------|------|------|
| **Claude가 코드를 읽으면 알 수 있는 것** | 토큰 낭비 | Claude가 코드에서 추론하도록 둠 |
| **표준 언어 컨벤션** | Claude가 이미 앎 | 기본값과 다른 것만 명시 |
| **상세 API 문서** | 너무 김 | 문서 링크를 제공 |
| **자주 변하는 정보** | 구식화 위험 | Auto Memory에 위임 또는 링크 |
| **긴 설명이나 튜토리얼** | context 낭비 | Skills로 분리 (on-demand 로딩) |
| **파일별 코드베이스 설명** | Claude가 직접 탐색 | 필요 시 Claude가 읽도록 유도 |
| **"Write clean code" 같은 자명한 원칙** | 효과 없음 | 구체적 규칙으로 대체 |

### 5.3 앤(Ann) 글로벌 CLAUDE.md 하네스 관점 인사이트

**글로벌 vs 프로젝트 레벨 분배 전략**:

| 글로벌 (`~/.claude/CLAUDE.md`) | 프로젝트 레벨 (`./CLAUDE.md`) |
|-------------------------------|-------------------------------|
| 페르소나 (앤 + 미르) | 프로젝트 기술 스택 |
| 언어 규칙 (한국어/영어) | 빌드/테스트 명령어 |
| 5단계 사고 과정 | 프로젝트 아키텍처 결정 |
| 바이브코딩 워크플로우 원칙 | 브랜치 전략, PR 규범 |
| 공통 보안 규범 | 프로젝트 고유 환경변수 |
| 응답 규칙 (간결/복잡도별) | 프로젝트 고유 gotcha |
| PARALLEL-FIRST / CLEAR Framework | DB 스키마 규칙 등 |

---

## 6. 고급 기능

### 6.1 Import 문법 (`@path/to/import`)

CLAUDE.md 내에서 `@` 문법으로 외부 파일을 참조할 수 있다.

**동작 방식**:
- 세션 시작 시 CLAUDE.md와 함께 import된 파일이 context에 확장·로딩
- 상대 경로: import를 포함한 파일 기준으로 해석 (작업 디렉토리가 아님)
- 재귀 import 지원: 최대 **5홉** 깊이
- 절대 경로 및 `~` 경로 모두 허용

**사용 예시**:
```markdown
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

**개인 설정을 git에 커밋하지 않고 사용하는 방법**:
```markdown
# Individual Preferences
- @~/.claude/my-project-instructions.md
```

**보안 주의**: 외부 import을 처음 만나면 Claude Code가 승인 다이얼로그를 표시. 거부 시 import 비활성화.

**AGENTS.md 호환**: 다른 AI 도구용 AGENTS.md가 이미 있는 경우:
```markdown
@AGENTS.md

## Claude Code
Use plan mode for changes under `src/billing/`.
```

### 6.2 `.claude/rules/` 디렉토리

CLAUDE.md가 커지면 토픽별 규칙 파일로 분할할 수 있다.

**구조**:
```
your-project/
├── .claude/
│   ├── CLAUDE.md           # 메인 프로젝트 지침
│   └── rules/
│       ├── code-style.md   # 코드 스타일 가이드라인
│       ├── testing.md      # 테스트 컨벤션
│       ├── security.md     # 보안 요구사항
│       └── frontend/
│           └── react.md    # 프론트엔드 전용 규칙
```

**Path-specific Rules (조건부 로딩)**:

YAML frontmatter의 `paths:` 필드로 특정 파일 패턴에만 적용되는 규칙 설정 가능:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules
- All API endpoints must include input validation
- Use the standard error response format
```

**glob 패턴 지원**:

| 패턴 | 매칭 |
|------|------|
| `**/*.ts` | 모든 디렉토리의 TypeScript 파일 |
| `src/**/*` | src/ 하위 모든 파일 |
| `*.md` | 프로젝트 루트의 마크다운 파일 |
| `src/components/*.tsx` | 특정 디렉토리의 React 컴포넌트 |
| `src/**/*.{ts,tsx}` | 중괄호 확장으로 다중 확장자 매칭 |

**동작 원리**:
- `paths:` 없는 규칙: 세션 시작 시 무조건 로딩 (CLAUDE.md와 동일 우선순위)
- `paths:` 있는 규칙: Claude가 매칭되는 파일을 읽을 때만 로딩 → **context 절약**
- 하위 디렉토리 재귀 탐색 지원

**Symlink를 통한 프로젝트 간 규칙 공유**:
```bash
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

**User-level Rules** (`~/.claude/rules/`):
- 모든 프로젝트에 적용되는 개인 규칙
- User-level rules → Project rules 순으로 로딩 (프로젝트가 우선)

### 6.3 `claudeMdExcludes` 설정

모노레포에서 다른 팀의 CLAUDE.md를 제외하는 설정:

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

- `.claude/settings.local.json`에 설정하여 개인 머신에만 적용 가능
- 절대 경로 기반 glob 패턴 매칭
- User, Project, Local, Managed Policy 모든 레이어에서 설정 가능 (배열 병합)
- **Managed Policy CLAUDE.md는 제외 불가** — 조직 전체 지침은 항상 적용

### 6.4 HTML 주석 처리

```markdown
<!-- 이 주석은 context에 주입되지 않으므로 토큰 소비 없음 -->
<!-- 유지보수자를 위한 메모로 활용 가능 -->

# Actual Instructions
- This line is loaded into context
```

- block-level HTML 주석은 context 주입 전 제거됨
- 코드 블록 내부 주석은 보존
- Read 도구로 직접 열면 주석이 보임

### 6.5 `--add-dir` 플래그와 추가 디렉토리

```bash
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

기본적으로 추가 디렉토리의 CLAUDE.md는 로딩되지 않으나, 환경변수 설정으로 활성화 가능.

### 6.6 앤(Ann) 글로벌 CLAUDE.md 하네스 관점 인사이트

**고급 기능 활용 전략**:

1. **Import 활용**: 글로벌 CLAUDE.md를 200줄 이내로 유지하면서, 상세 규칙은 `@~/.claude/rules/` 하위 파일로 분리
   ```markdown
   # ~/.claude/CLAUDE.md
   @~/.claude/rules/persona.md
   @~/.claude/rules/workflow.md
   @~/.claude/rules/security.md
   ```

2. **Path-specific Rules**: 바이브코딩에서 다루는 다양한 파일 유형별 규칙 자동 적용
   ```markdown
   # ~/.claude/rules/frontend.md
   ---
   paths:
     - "**/*.tsx"
     - "**/*.css"
   ---
   # 프론트엔드 규칙 (이 파일들을 다룰 때만 로딩)
   ```

3. **HTML 주석**: 유지보수 메모를 토큰 비용 없이 기록
   ```markdown
   <!-- 2026-04-03: Ann이 추가. 공공SI 보안 감사 요구사항 반영 -->
   - YOU MUST never hardcode credentials
   ```

4. **Symlink**: 여러 SI 프로젝트에서 공통 보안/품질 규칙을 공유
   ```bash
   ln -s ~/.claude/rules/si-security.md projects/A/.claude/rules/security.md
   ln -s ~/.claude/rules/si-security.md projects/B/.claude/rules/security.md
   ```

---

## 7. 베스트 프랙티스와 공식 예시

### 7.1 Best Practices 문서 핵심 패턴

Best Practices 공식 문서에서 추출한 핵심 작업 패턴:

#### 7.1.1 검증 우선 (Give Claude a way to verify its work)

> "This is the single highest-leverage thing you can do."

| 전략 | Before | After |
|------|--------|-------|
| 검증 기준 제공 | "implement email validation" | "write validateEmail function. test cases: user@example.com → true, invalid → false. run tests after implementing" |
| UI 변경 시각 검증 | "make the dashboard look better" | "[screenshot] implement this design. screenshot result and compare. list differences and fix them" |
| 근본 원인 해결 | "the build is failing" | "build fails with this error: [error]. fix it and verify build succeeds. address root cause" |

#### 7.1.2 탐색 → 계획 → 실행 → 커밋 (4단계 워크플로우)

```
1. Explore (Plan Mode): 코드 읽기, 질문 답변, 변경 없음
2. Plan (Plan Mode): 상세 구현 계획 작성, Ctrl+G로 편집
3. Implement (Normal Mode): 코드 작성, 테스트, 수정
4. Commit (Normal Mode): 커밋 + PR 생성
```

#### 7.1.3 Context 관리

- **`/clear`**: 무관한 작업 간 context 리셋 — 가장 중요한 습관
- **`/compact <instructions>`**: 특정 부분 보존하며 압축
- **`/rewind` → Summarize from here**: 특정 지점부터 요약
- **`/btw`**: context에 남기지 않는 일회성 질문
- **CLAUDE.md에 compaction 지시 가능**: "When compacting, always preserve the full list of modified files"

#### 7.1.4 Subagent 활용

```text
Use subagents to investigate how our authentication system handles token
refresh, and whether we have any existing OAuth utilities I should reuse.
```

- 별도 context window에서 탐색 → 메인 대화 오염 방지
- 구현 후 검증에도 활용: "use a subagent to review this code for edge cases"

#### 7.1.5 Common Failure Patterns (공식 안티패턴)

| 안티패턴 | 설명 | 해결책 |
|----------|------|--------|
| **Kitchen Sink Session** | 하나의 세션에서 무관한 작업 혼합 | `/clear` between tasks |
| **반복 수정** | 같은 실수 2회 이상 수정 시도 | `/clear` 후 더 나은 프롬프트로 재시작 |
| **비대한 CLAUDE.md** | 너무 길어서 핵심 규칙 묻힘 | ruthless pruning, hook으로 전환 |
| **검증 없는 신뢰** | 그럴듯해 보이지만 edge case 미처리 | 항상 테스트/스크립트/스크린샷으로 검증 |
| **무한 탐색** | 범위 없는 조사로 context 가득 참 | 범위 좁히기 또는 subagent 위임 |

### 7.2 공식 CLAUDE.md 예시 (확장판)

```markdown
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

.claude directory 문서에서의 확장 예시:

```markdown
# Project conventions

## Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

## Stack
- TypeScript with strict mode
- React 19, functional components only

## Rules
- Named exports, never default exports
- Tests live next to source: `foo.ts` -> `foo.test.ts`
- All API routes return `{ data, error }` shape
```

### 7.3 앤(Ann) 글로벌 CLAUDE.md 하네스 관점 인사이트

**4단계 워크플로우와 바이브코딩 매핑**:

```
공식 4단계          앤의 바이브코딩 워크플로우
─────────          ────────────────────────
1. Explore     →   기획/분석 (요구사항 파악, 코드 탐색)
2. Plan        →   설계 (아키텍처, 디자인 시안, DB 설계)
3. Implement   →   개발 (프론트엔드, 백엔드, Git 운영)
4. Commit      →   배포/리뷰 (PR, 코드리뷰, 문서화)
```

**공공기관 SI 관점 안티패턴 대응**:

- **Kitchen Sink**: SI 프로젝트는 범위가 넓으므로 모듈별로 세션 분리가 필수
- **비대한 CLAUDE.md**: 공공기관 규범은 많지만, 글로벌에는 핵심만, 나머지는 rules/로 분산
- **검증 없는 신뢰**: 공공기관은 감사 대상이므로, 모든 구현에 테스트 검증 의무화

---

## 8. 공공기관 SI 프로젝트 + 바이브코딩 스타일 적용 시 강점과 고려사항

### 8.1 강점

#### 8.1.1 일관성과 표준화

- **CLAUDE.md 하네스를 통한 규범 강제**: 공공기관 SI는 전자정부 표준프레임워크, 보안 가이드라인, 접근성 기준 등 다수의 표준을 준수해야 함. 글로벌 CLAUDE.md에 핵심 표준을 명시하면 **어떤 프로젝트에서든 동일한 수준의 준수** 가능
- **바이브코딩 워크플로우 고정**: 기획 → 디자인 → 개발 → 배포의 일관된 흐름을 CLAUDE.md에 정의하면, Claude가 매번 동일한 절차를 따름

#### 8.1.2 감사 대응력

- CLAUDE.md 자체가 **"AI에게 부여한 지침의 문서화"** 역할
- git에 커밋하면 **지침 변경 이력**도 추적 가능
- "AI가 어떤 규칙 아래서 작업했는가"에 대한 증빙 확보

#### 8.1.3 다중 프로젝트 관리 효율

- PM으로서 여러 SI 프로젝트를 동시에 관리할 때, 글로벌 CLAUDE.md로 **공통 기준 유지**
- 프로젝트별 CLAUDE.md로 **개별 특성 반영**
- `.claude/rules/`로 모듈별 세분화 → 대규모 프로젝트에서도 context 낭비 최소화

#### 8.1.4 지식 축적과 전파

- Auto Memory가 프로젝트별 디버깅 패턴, 빌드 노하우를 자동 축적
- CLAUDE.md를 팀원과 공유 → AI 활용 팀 전체 역량 상향 평준화
- Skills와 Hooks 결합으로 반복 작업 자동화

#### 8.1.5 바이브코딩 가속

- Plan Mode로 안전한 탐색/설계 → Normal Mode로 빠른 구현
- Subagent 활용으로 코드 리뷰, 보안 검토를 별도 context에서 병렬 수행
- `/compact` 생존성으로 장시간 작업에서도 지침 유지

### 8.2 고려사항과 위험

#### 8.2.1 Advisory 한계

| 위험 | 상세 | 대응 |
|------|------|------|
| **규칙 무시** | CLAUDE.md는 권고사항이므로 Claude가 무시할 수 있음 | 강제 필요한 규칙은 Hooks/Permissions로 분리 |
| **모순 발생** | 글로벌 + 프로젝트 + rules 간 모순 시 임의 선택 | 정기적 일관성 검토, 명확한 scope 분리 |
| **길이 초과** | 200줄 초과 시 준수율 저하 | ruthless pruning, import/rules 분산 |

#### 8.2.2 보안 위험

| 위험 | 상세 | 대응 |
|------|------|------|
| **Auto Memory 민감 정보** | 프로젝트 구조, API 엔드포인트 등이 자동 저장될 수 있음 | 주기적 `/memory` 검토, 민감 프로젝트에서 비활성화 고려 |
| **Import 외부 파일** | `@path` 임포트로 의도치 않은 파일 노출 가능 | 첫 import 시 승인 다이얼로그 활용, 경로 검증 |
| **글로벌 CLAUDE.md 노출** | 개인 워크플로우/규칙이 모든 세션에 노출 | 민감 정보는 CLAUDE.md가 아닌 환경변수로 관리 |

#### 8.2.3 공공기관 특화 고려사항

| 고려사항 | 상세 | 대응 |
|----------|------|------|
| **망분리 환경** | 폐쇄망에서 Claude Code 사용 제한 가능 | Managed Policy로 조직 규칙 배포, 로컬 모드 활용 |
| **보안 감사** | AI 생성 코드의 감사 추적 필요 | CLAUDE.md git 이력 + Auto Memory 정기 백업 |
| **다수 이해관계자** | 기관 담당자, 개발팀, PM 등 역할별 규칙 필요 | Scope별 CLAUDE.md 분리 + Managed Policy 활용 |
| **문서화 의무** | 산출물 표준 서식 준수 필요 | Skills에 문서 템플릿 정의, CLAUDE.md에 문서화 규칙 명시 |
| **코드 품질 기준** | 정적 분석, 코드 커버리지 등 의무 사항 | Hooks로 lint/test 자동 실행 강제 |

#### 8.2.4 바이브코딩 특화 고려사항

| 고려사항 | 상세 | 대응 |
|----------|------|------|
| **디자인 시안 → 코드** | 시각적 검증이 필요한 워크플로우 | Chrome 확장 + 스크린샷 비교 규칙을 CLAUDE.md에 명시 |
| **다기능 작업** | PM이 기획부터 개발까지 전부 수행 | 역할별 rules 파일 분리 (planning.md, design.md, coding.md) |
| **Git 운영** | 브랜치 전략, 커밋 메시지 규범 | 글로벌에 기본 Git 규칙, 프로젝트에 고유 브랜치 전략 |
| **장시간 세션** | 복잡한 기능 개발 시 context 고갈 | CLAUDE.md에 compaction 보존 규칙 명시, subagent 적극 활용 |

### 8.3 앤(Ann) 글로벌 CLAUDE.md 하네스 최종 인사이트

**글로벌 CLAUDE.md가 하네스로서 가지는 핵심 가치**:

```
하네스엔지니어링 관점에서 CLAUDE.md의 위치:

┌─────────────────────────────────────────────────┐
│           Anthropic 3-Agent GAN-style            │
│     (Planner + Generator + Evaluator)            │
│                                                   │
│  ┌───────────────────────────────────────┐       │
│  │    CLAUDE.md = Initializer의 역할      │       │
│  │    매 세션마다 환경/규칙/페르소나 주입   │       │
│  └───────────────────────────────────────┘       │
│                                                   │
│  ┌───────────────────┐ ┌───────────────────────┐ │
│  │ Auto Memory        │ │ Skills / Hooks         │ │
│  │ = 경험 축적 레이어  │ │ = 실행 자동화 레이어   │ │
│  └───────────────────┘ └───────────────────────┘ │
└─────────────────────────────────────────────────┘
```

- CLAUDE.md는 하네스의 **"지휘 센터"** — 모든 세션의 출발점
- Auto Memory는 **"경험 데이터베이스"** — 시간이 갈수록 풍부해짐
- Skills/Hooks는 **"자동화 레이어"** — 반복 작업의 결정론적 실행
- `.claude/rules/`는 **"조건부 지식"** — 필요할 때만 로딩되는 전문 규칙

이 4가지 레이어를 체계적으로 설계하면, 앤의 바이브코딩 워크플로우 전체를 감싸는 **production-grade 개인 하네스**가 완성된다.

---

## 조사·분석 완료

위 8개 항목은 06번 문서와 공식 링크 4개(memory, best-practices, claude-directory, overview)의 내용을 앤(Ann)의 페르소나와 글로벌 CLAUDE.md 하네스 구축 관점에서 분석한 결과입니다. 실제 CLAUDE.md 작성은 포함하지 않았습니다.
