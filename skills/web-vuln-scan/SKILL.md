---
name: web-vuln-scan
description: >
  행안부/KISA 가이드 기반 한국 공공기관 웹취약점 점검 스킬.
  소프트웨어 보안약점 49개(CWE 매핑), OWASP Top 10 (2021), KISA 웹취약점 28개 항목을
  3단계(Tier 1 정적 분석, Tier 2 에이전트 심화 분석, Tier 3 동적 테스트)로 점검하고
  공공기관 표준 양식 보고서를 생성한다.
  Use this skill when: (1) "웹취약점 점검", "보안점검", "시큐어코딩" 요청 시,
  (2) "web vulnerability scan", "OWASP 점검", "보안약점 진단" 요청 시,
  (3) 공공기관 보안 감리/인증 대응 시,
  (4) 소스코드 보안 취약점 전체 스캔 시,
  (5) KISA/행안부 기준 웹 보안 평가 시,
  (6) 시큐어코딩 가이드 준수 확인 시.
  Trigger aggressively when: 소스코드와 보안, 취약점, 인젝션, XSS, OWASP,
  시큐어코딩, 보안약점, CWE, 웹해킹, 보안감리 등이 함께 언급될 때.
  지원 언어: HTML/JS, Python, Java, PHP. 단일 파일 및 프로젝트 전체 스캔 모두 지원.
---

# 웹 취약점 점검 스킬 (Web Vulnerability Scanner)

## 1. 개요

한국 공공기관 웹 보안 점검을 위한 3축 기준 통합 점검 스킬.

**점검 기준 3축**:
- 행안부 「소프트웨어 보안약점 진단가이드」 — 설계 20개 + 구현 49개 항목 (CWE 기반)
- OWASP Top 10 (2021/2025) — 국제 웹 취약점 표준
- KISA 「주요정보통신기반시설 기술적 취약점 분석·평가 상세가이드」 — 웹 28개 항목

**3-Tier 검사 체계**:
- Tier 1: Python 정적 코드 분석 (외부 의존성 없음)
- Tier 2: AI 에이전트 심화 분석 (security-reviewer + edge-case-reviewer + logic-reviewer)
- Tier 3: Playwright 동적 테스트 (webapp-testing 연동)

**지원 언어**: HTML/JS, Python, Java, PHP

## 2. 실행 흐름

```
사용자 요청 → 대상 파일/디렉토리 확인
    ├─ 단일 파일 → 언어 감지 → Tier 1 → (선택) Tier 2 → 보고서 생성
    ├─ 프로젝트 전체 → Glob 대상 파일 → 파일별 Tier 1 → 집계 → 보고서
    ├─ URL 제공 → Tier 1(코드) + Tier 3(동적) → 보고서
    └─ 체크리스트만 → 수동 점검 체크리스트 생성
```

### 호출 방법
- `/web-vuln-scan` 또는 `/web-vuln-scan <파일경로>`
- 자연어: "이 코드 보안 점검해줘", "웹취약점 검사해줘", "시큐어코딩 검사"

### 스캔 모드 결정

| 사용자 요청 | 모드 | 동작 |
|------------|------|------|
| "간단히 체크" / 빠른 스캔 | Tier 1만 | Python 정적 분석 (의존성 없음) |
| "전체 점검" / 자세히 | Tier 1+2+3 | 정적 + 에이전트 + 동적 |
| "코드 분석만" | Tier 1+2 | 서버 불필요 |
| "동적 테스트" | Tier 3만 | Playwright 동적 테스트 |
| "체크리스트만" | 수동 | 수동 점검 체크리스트 생성 |
| 기본 (모드 미지정) | Tier 1 + 수동 체크리스트 | 기본값 |

## 3. Tier 1 — 정적 분석 (Python, 의존성 없음)

Python 표준 라이브러리(`re`, `json`, `os`, `sys`)로 소스코드를 파싱하여
행안부 보안약점 중 핵심 13개 규칙(7유형 커버)의 패턴을 정적 검출한다.
나머지 약점은 Tier 2 에이전트가 코드 이해 기반으로 보완한다. 외부 패키지 설치 없이 즉시 실행 가능.

### 실행 방법

```bash
python ~/.claude/skills/web-vuln-scan/scripts/vuln-static-scan.py <파일_또는_디렉토리> [옵션]
```

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--format` | 출력 형식 (`json`, `md`) | `json` |
| `--severity` | 최소 심각도 (`critical`, `major`, `minor`, `all`) | `all` |
| `--lang` | 언어 지정 (`auto`, `html`, `js`, `python`, `java`, `php`) | `auto` |
| `--category` | 유형 필터 (`all`, `input`, `security`, `time`, `error`, `code`, `encapsulation`, `api`) | `all` |
| `--owasp` | OWASP 필터 (`all`, `A01`~`A10`) | `all` |

### 커버리지 (7유형별)

| 유형 | 구현 규칙 수 | 검출 기법 | 주요 검출 대상 |
|------|------------|----------|-------------|
| 입력데이터 검증 및 표현 | 5 | regex 패턴 | SQL인젝션, XSS, OS명령, CSRF, 경로조작 |
| 보안 기능 | 3 | 하드코딩/평문 패턴 | 약한 암호화, 평문저장, 하드코딩 비밀번호 |
| 에러 처리 | 2 | catch-all/예외 패턴 | 에러 정보노출, 부적절한 예외처리 |
| 코드 오류 | 1 | 역직렬화 패턴 | pickle/yaml 역직렬화 |
| 캡슐화 | 1 | 디버그 코드 패턴 | pdb, console.log, var_dump |
| API 오용 | 1 | 위험 API 패턴 | eval, exec, system |
| **합계** | **13 규칙** | **4개 언어 × 60+ 패턴** | Tier 2 에이전트가 나머지 보완 |

### 출력 JSON 스키마

```json
{
  "file": "target.py",
  "timestamp": "2026-03-20T10:00:00",
  "tier": 1,
  "language": "python",
  "summary": {
    "total_vulnerabilities": 5,
    "by_severity": {"critical": 1, "major": 2, "minor": 1, "info": 1},
    "by_category": {"input_validation": 3, "security_function": 1, "error_handling": 1}
  },
  "vulnerabilities": [
    {
      "vuln_id": "MOIS-IV-01",
      "vuln_name": "SQL 인젝션",
      "category": "입력데이터 검증 및 표현",
      "cwe": "CWE-89",
      "owasp": "A03",
      "kisa_id": "WV-05",
      "severity": "critical",
      "file": "db.py",
      "line": 42,
      "code_snippet": "cursor.execute(f\"SELECT * FROM users WHERE id={user_id}\")",
      "message": "사용자 입력이 SQL 쿼리에 직접 삽입됩니다.",
      "fix": "parameterized query(바인드 변수)를 사용하세요.",
      "fix_example": "cursor.execute(\"SELECT * FROM users WHERE id=?\", (user_id,))"
    }
  ]
}
```

## 3-1. Tier 1 보안 헤더 점검

```bash
python ~/.claude/skills/web-vuln-scan/scripts/vuln-header-check.py --url <URL> [--format json|md]
```

| 점검 헤더 | 권장 설정 |
|----------|----------|
| X-Frame-Options | DENY 또는 SAMEORIGIN |
| X-Content-Type-Options | nosniff |
| Strict-Transport-Security | max-age=31536000; includeSubDomains |
| Content-Security-Policy | default-src 'self' |
| Referrer-Policy | strict-origin-when-cross-origin |
| Permissions-Policy | camera=(), microphone=() |
| Cache-Control | no-store (민감 페이지) |

## 4. Tier 2 — 에이전트 심화 분석

기존 3개 리뷰 에이전트를 **행안부 보안약점 전용 프롬프트**로 병렬 호출한다.

```
Tier 1 결과(JSON) → 에이전트 병렬 호출:
  ├─ security-reviewer [OWASP A01~A10 + MOIS-SF 8개 집중]
  ├─ edge-case-reviewer [경계값 공격 벡터 + MOIS-TS 2개]
  └─ logic-reviewer [인증/인가 논리 결함 + MOIS-SF-01,02]
→ 결과 병합 → 통합 JSON
```

### 에이전트별 보안 점검 프롬프트

**security-reviewer**:
> 행안부 49개 보안약점 기준으로 이 코드를 점검하세요.
> Tier 1에서 발견된 취약점 목록을 검증하고, 미발견 항목을 추가 탐지하세요.
> 특히 OWASP A01~A10 전항목과 MOIS-SF(보안기능) 8개에 집중하세요.

**edge-case-reviewer**:
> 보안 관점의 경계값 테스트를 수행하세요.
> null/빈값/초과값 입력이 보안 우회로 이어지는지 확인하세요.
> MOIS-IV(입력검증) 15개와 MOIS-TS(시간/상태) 2개 항목 관련 공격 벡터를 분석하세요.

**logic-reviewer**:
> 인증/인가 로직의 논리적 결함을 분석하세요.
> MOIS-SF-01(인증 없는 중요기능), MOIS-SF-02(부적절한 인가) 중심으로
> 로그인 우회, 권한 상승 가능 경로를 식별하세요.

### 추가 커버리지
Tier 2를 통해 비즈니스 로직, 인가, 세션 관리, 경쟁조건 등 정적 분석으로 미검출되는 취약점을 보완한다.

## 5. Tier 3 — 동적 테스트 (Playwright)

대상 웹 앱이 실행 중이거나 실행 가능한 경우, 비파괴적 동적 테스트를 수행한다.

### 실행 조건
```
서버 실행 중 → 직접 동적 테스트
서버 실행 가능 → webapp-testing의 with_server.py 연동
서버 없음 → Tier 3 스킵 (Tier 1+2만)
```

### 동적 테스트 항목 (10개)

| # | 테스트 | KISA 대응 | 방법 |
|---|--------|----------|------|
| 1 | Reflected XSS | WV-11 | 입력 필드에 XSS 페이로드 → DOM 확인 |
| 2 | SQL 인젝션 응답 | WV-05 | `' OR 1=1--` → 에러/응답 차이 분석 |
| 3 | CSRF 토큰 | WV-15 | 폼에 CSRF 토큰 존재 + 토큰 없이 제출 |
| 4 | 세션 쿠키 속성 | WV-18,19 | HttpOnly/Secure/SameSite 확인 |
| 5 | 디렉토리 리스팅 | WV-08 | 알려진 경로에 GET 요청 |
| 6 | 정보 노출 | WV-09 | 에러 유발 → 스택 트레이스 확인 |
| 7 | 보안 헤더 | - | HTTP 응답 헤더 전체 점검 |
| 8 | HTTPS | WV-27 | HTTP→HTTPS 리다이렉트, HSTS |
| 9 | 경로 추적 | WV-25 | `../../../etc/passwd` 요청 |
| 10 | 인증 테스트 | WV-13 | 비인가 페이지 직접 접근 |

**안전장치**: 모든 동적 테스트는 비파괴적(read-only). 데이터 변조/삭제 수행하지 않음.

## 6. 보고서 생성

스캔 완료 후 2종 보고서를 생성한다. 사용자가 보고서 유형을 지정하지 않으면 기본으로 둘 다 생성한다.

### 2종 보고서

| 보고서 | 템플릿 | 대상 | 내용 |
|--------|--------|------|------|
| **요약 보고서** | `templates/report-full.md` | PM, 감리인, 보안 담당자 | 종합등급, 유형별 현황, 수정 우선순위, 수동 체크리스트 |
| **디테일 보고서** | `templates/report-detail.md` | 개발자 | 건별 파일:라인, 취약 코드, 수정 방안, 안전한 코드 예시 |

### 보고서 유형 선택

| 사용자 요청 | 생성 보고서 |
|------------|-----------|
| "요약만", "간단히" | 요약 보고서만 |
| "디테일", "상세", "건별", "코드 포함" | 디테일 보고서만 |
| "전체", "둘 다", 기본(미지정) | 요약 + 디테일 모두 |

### 디테일 보고서 건별 형식

각 취약점 건마다 아래 구조로 작성한다. 개발자가 보고서를 열어 바로 수정할 수 있도록
취약 코드와 안전한 코드 예시를 반드시 포함한다.

```
### [#번호] [심각도] MOIS-XX-00 약점명

| 항목 | 내용 |
|------|------|
| CWE | CWE-XXX |
| OWASP | A0X |
| 파일 | `전체 파일 경로` |
| 라인 | 42 |

#### 취약 코드
(해당 라인의 코드 스니펫 — 전후 컨텍스트 포함)

#### 취약점 설명
(왜 위험한지, 어떤 공격이 가능한지)

#### 수정 방안
(구체적 수정 방향)

#### 안전한 코드 예시
(수정된 코드)
```

### 파일명 규칙

보고서 파일명은 아래 규칙을 따른다. 프로젝트명과 날짜로 2종 보고서를 묶어 식별하기 쉽게 한다.

```
01_[프로젝트명]_웹취약점_요약보고서_[YYYYMMDD].md
02_[프로젝트명]_웹취약점_디테일보고서_[YYYYMMDD].md
```

**예시**:
```
01_gil-seoul_bo_웹취약점_요약보고서_20260320.md
02_gil-seoul_bo_웹취약점_디테일보고서_20260320.md
```

**규칙**:
- `01_` = 요약 보고서 (먼저 읽을 것)
- `02_` = 디테일 보고서 (수정 작업 시 참조)
- 프로젝트명은 대상 폴더명 또는 사용자 지정 이름
- 날짜는 점검일 기준 YYYYMMDD

### md-template 문서 표준 준수

보고서 생성 시 `~/.claude/rules/md-template.md` 표준을 따른다. 필수 구조:

1. **YAML Frontmatter** — title, version, created, updated, tags, status, type
2. **Next Session Handoff** — 현재 상태, 다음 작업 TODO, 작업 조언
3. **제목** (`# 프로젝트명 웹 취약점 [요약/디테일] 보고서`)
4. **개요** — 문서 목적과 범위
5. **본문** — 점검 결과 (research 유형)
6. **관련 문서** — 직접 참조, 관련 주제 (상대 보고서 교차 링크 포함)
7. **Release Notes** — 버전 + 날짜 + 원본 프롬프트

### 참고 자료
- 취약점별 언어별 수정 예시: `templates/remediation-guide.md`

## 7. 심각도 분류

| 등급 | 기준 | 예시 |
|------|------|------|
| Critical | 즉시 악용 가능, 시스템 전체 영향 | SQL 인젝션, RCE, 인증 우회 |
| Major | 추가 조건 필요하나 위험도 높음 | XSS, CSRF, 세션 고정 |
| Minor | 직접 악용 어렵지만 공격 표면 노출 | 보안 헤더 누락, 디버그 코드 |
| Info | 자동 판단 불가, Best Practice | 수동 확인 필요 |

상세: `references/severity-levels.md`

## 8. Claude Code 통합 가이드

### 오케스트레이션 연동
- DevChain(D), WebDevChain+(G) 리뷰 단계에서 선택적 트리거
- 사용자가 "보안 점검도 해줘" 요청 시 자동 연동
- kwcag-a11y와 동시 실행 시 결과 병합 가능

### 트리거 키워드
웹취약점, 보안점검, 시큐어코딩, OWASP, CWE, 보안약점, 보안감리, 침투테스트, 취약점 진단

## 9. 제한 사항

- 실제 침투 테스트(ZAP/Burp) **대체 불가** — 코드 분석 + 비파괴적 동적 테스트
- 서버 설정(Apache/Nginx/IIS), SSL/TLS 인증서, DB 보안, 네트워크 수준 **미지원**
- Tier 1 정적 분석은 패턴 기반 → **오탐 가능** (Tier 2 에이전트가 보완)
- 바이너리/컴파일 코드 **미지원** (소스코드만 분석)

## 10. 참조 파일

| 파일 | 설명 |
|------|------|
| `references/mois-47-cwe-mapping.md` | 행안부 보안약점 ↔ CWE ↔ OWASP ↔ KISA 매핑 |
| `references/owasp-top10-mapping.md` | OWASP Top 10 역매핑 |
| `references/kisa-15-checklist.md` | KISA 웹취약점 상세 체크리스트 |
| `references/severity-levels.md` | 심각도 분류 기준 |
| `references/manual-checklist-template.md` | 수동 점검 체크리스트 |
| `references/tier1-patterns/` | 언어별 정적 검출 패턴 (5개 파일) |
| `templates/report-full.md` | Type 1: 요약 보고서 템플릿 (통계+우선순위) |
| `templates/report-detail.md` | Type 2: 디테일 보고서 템플릿 (건별 코드+수정 예시) |
| `templates/remediation-guide.md` | 취약점별 수정 가이드 (언어별 참조) |
| `scripts/vuln-static-scan.py` | Tier 1 정적 분석 스크립트 |
| `scripts/vuln-header-check.py` | Tier 1 보안 헤더 점검 스크립트 |
| `scripts/vuln-dynamic-test.py` | Tier 3 동적 테스트 스크립트 |
| `scripts/vuln-report-gen.py` | 통합 보고서 생성기 |
