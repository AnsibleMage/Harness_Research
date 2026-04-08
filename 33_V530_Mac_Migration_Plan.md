---
title: "V5.3.0 맥 환경 마이그레이션 작업계획서 — WE 기법 적용 + 충돌 해소"
version: "1.0.0"
created: "2026-04-07"
updated: "2026-04-07"
tags: [claude-code, V5.3.0, mac-migration, conflict-resolution, roadmap]
status: completed
type: roadmap
source: 28~32_ WE 파이프라인 + Mac V5.2.0 전수 분석
---

## Next Session Handoff

### 현재 상태
- 이 문서의 완성도: completed (3 Phase 12 Step 전수 실행 완료)
- 마지막 작업: Phase 1~3 실행 + 플로어 검증 통과

### 다음 작업 (TODO)
- [ ] 스킬 description 250자 감사 (52개 스킬 — 별도 세션)
- [ ] 실사용 1~2주 후 행동 변화 모니터링

### 작업 조언
> [!tip] 다음 Claude Code에게
> - 이 문서는 WE(윈도우)에서 적용된 V5.3.0을 **맥 환경에 맞게 변환**하여 적용하는 계획서
> - WE와 맥의 구조적 차이가 있으므로 **WE 문서(29~32)를 그대로 복사하면 안 됨**
> - 각 Phase의 체크박스를 순서대로 진행하고, 완료 시 `[x]`로 마킹
> - [[29_Source_Code_Techniques_Application.md]]의 적용 문구를 참고하되 맥 구조에 맞게 변환

---

# V5.3.0 맥 환경 마이그레이션 작업계획서

## 개요

### 배경

28~32번 문서에서 Anthropic 소스코드 7가지 기법을 분석하고 V5.3.0-WE로 업그레이드했다. 이는 **윈도우(WE) 환경**에서 수행되었으며, 맥 환경과 구조적 차이가 존재한다. 이 문서는 WE 업그레이드를 맥 환경에 최적화하여 적용하기 위한 작업계획서다.

### 목표

| 지표 | 현재 (Mac V5.2.0) | 목표 (Mac V5.3.0) |
|------|-------------------|-------------------|
| CLAUDE.md 버전 | 5.2.0 | **5.3.0** |
| Rules 파일 수 | 3개 | **4개** (+behavioral-standards.md) |
| CLAUDE.md 줄 수 | 139줄 | ~160줄 (+~21줄) |
| 7가지 기법 적용 | 0/7 | **7/7** |
| 3중 반복 규칙 | 0개 | **3개** |
| Teammate 행동 규칙 | 6개 | **9개** |

### 28~33 파이프라인

```
28_ 기법 정리 (7가지 분류)
    ↓ "무엇이 있는가"
29_ 적용 방안 v1.2.0 (WE 기준)
    ↓ "어디에 어떻게 넣는가"
30_ WE 적용 결과 보고서
    ↓ "WE에서 어떻게 됐는가"
31_ WE 시니어 검증 (8/10)
    ↓ "WE에서 무엇이 문제인가"
32_ WE 수정 작업계획서
    ↓ "WE에서 어떻게 고쳤는가"
33_ Mac 마이그레이션 ← 이 문서
    "Mac에서 어떻게 적용하는가"
```

---

## §1. 환경 차이 분석 (Mac vs WE)

### 1.1 구조적 차이

| 항목 | Mac (V5.2.0) | WE (V5.2.0-WE → V5.3.0-WE) | 차이 영향 |
|------|-------------|---------------------------|---------|
| **CLAUDE.md 섹션** | §1~5 (139줄) | §1~5 (~90줄) → §1~7 (~105줄) | Mac이 더 김. 섹션 번호 다름 |
| **CLAUDE.md 제목줄** | "V5.1.0" (본문은 5.2.0) | 일치 | **맥 버그** — 제목 수정 필요 |
| **Rules 파일** | 3개 | 4개 (template-protocol.md 포함) | Mac에 template-protocol.md **없음** |
| **에이전트 수** | 28개 (§2.3에 등록) | 23개 → 31개 | Mac이 이미 28개 보유 |
| **스킬 수** | 52개 | 49개 | Mac이 더 많음 (3개+) |
| **메모리 수** | 218개 | 439+개 | 차이만 있고 충돌 없음 |
| **Settings** | 11 allow, 20 deny | 다를 수 있음 | 개별 확인 불필요 |

### 1.2 WE와의 매핑 테이블 차이

| WE §2.3 매핑 | Mac §2.3 매핑 | 상태 |
|-------------|-------------|------|
| 에이전트 23개 → 31개 | 28개 이미 등록 | Mac이 3개 부족 (quality-manager, context-manager, plan-verifier) |
| 스킬 22개 → 49개 | 25개 등록 (§2.3 테이블 기준) | Mac 테이블에 누락 스킬 있음 |

---

## §2. 충돌 지점 분석 (11건)

### 충돌 요약 매트릭스

| # | 충돌 지점 | 심각도 | WE 적용 내용 | Mac 해결 전략 |
|---|----------|--------|-------------|-------------|
| C-1 | CLAUDE.md 섹션 번호 | **중** | §6(변경이력), §7(REMINDER) 신설 | Mac은 §5가 변경이력 → §6(REMINDER)으로 배치 |
| C-2 | CLAUDE.md 제목 버전 불일치 | **낮** | 해당 없음 (WE 자체 버그 아님) | Mac 고유 버그 — 제목 "V5.1.0" → "V5.3.0" 수정 |
| C-3 | Rules 파일 수 | **중** | 4→5개 (template-protocol 존재) | Mac은 3→4개. Rules 테이블에 1행 추가 |
| C-4 | §2.3 에이전트 매핑 | **낮** | 23→31개 (+8) | Mac 28개 기준으로 갱신. 부족분 3개만 추가 |
| C-5 | §2.3 스킬 매핑 | **낮** | 22→49개 (+27) | Mac 52개 기준. 테이블에 누락된 스킬 추가 |
| C-6 | §2.4 축약 금지 형식 | **중** | blockquote → Do/Don't 테이블 전환 | 기존 blockquote 교체 → Do/Don't 테이블 |
| C-7 | §2.5 Teammate 규칙 추가 | **없음** | 규칙 7/8/9 추가 | 순수 추가 — 충돌 없음 |
| C-8 | §2.5 동시성 보호 추가 | **없음** | +1행 (컨텍스트 오염) | 순수 추가 — 충돌 없음 |
| C-9 | memory-protocol.md 섹션 번호 | **낮** | §3.6 추가 | Mac은 번호 없는 헤딩 사용 → 적절한 위치에 추가 |
| C-10 | behavioral-standards.md 신규 | **없음** | 71줄 신규 생성 | 동일하게 생성 — 충돌 없음 |
| C-11 | 3중 반복 위치 A/C | **중** | §2 CRITICAL + §7 REMINDER | Mac §2 CRITICAL + §6 REMINDER |

### 충돌 상세 및 해결 전략

#### C-1: CLAUDE.md 섹션 번호 (심각도: 중)

**WE 구조**: §1(Identity) → §2(Rules) → §3(Settings) → §4(Repo) → §5(Component) → §6(Change History) → §7(REMINDER)

**Mac 현재 구조**: §1(Identity) → §2(Rules) → §3(Settings) → §4(Repo) → §5(Change History)

**해결**: Mac은 §5(Change History) 유지, §6(REMINDER) 신설. WE의 §5(Component Catalog)는 Mac에 불필요하므로 생략.

```
Mac V5.3.0 최종 구조:
§1 Identity & Principles (+ 비위맞추기 금지)
§2 Rules (+ CRITICAL 블록 + behavioral-standards 포인터)
§3 Settings Reference (+ 스킬 예산 인식)
§4 Repository & Review (변경 없음)
§5 Change History (+ V5.3.0 항목)
§6 REMINDER (신설 — 3중 반복 위치 C)
```

#### C-2: CLAUDE.md 제목 버전 불일치 (심각도: 낮)

**현재**: 1행 `V5.1.0` / 3행 `Version: 5.2.0` — 불일치
**해결**: V5.3.0 적용 시 1행과 3행 모두 `V5.3.0`으로 통일

#### C-3: Rules 파일 수 (심각도: 중)

**WE**: orchestration + memory-protocol + lessons-learned + **template-protocol** + behavioral-standards = 5개
**Mac**: orchestration + memory-protocol + lessons-learned + behavioral-standards = **4개**

**해결**: template-protocol.md는 Mac에서 orchestration.md §2.7에 이미 통합되어 있으므로 별도 파일 불필요. Mac은 4개 파일 체제로 진행.

#### C-6: §2.4 축약 금지 형식 전환 (심각도: 중)

**현재 (Mac)**: blockquote 4줄 (139~142행)
```
> ⚠️ **임의 축약 금지**: 체인 선택 후, 정의된 모든 에이전트를 순서대로 실행한다.
> - "충분하다"는 자의적 판단으로 후반부 에이전트를 생략하지 않는다
> - 체인 축소가 필요하면 앤이 체인 정의 자체를 수정한다
> - 아리는 체인을 선택할 자율권은 있지만, 선택한 체인의 단계를 생략할 권한은 없다
```

**목표 (V5.3.0)**: Do/Don't 테이블로 전환 + 검증 정직성 추가

**해결**: 기존 blockquote를 Do/Don't 테이블로 교체. 의미는 동일하게 유지하되 형식만 변경.

#### C-11: 3중 반복 위치 (심각도: 중)

**WE**: CLAUDE.md §2(위치 A) + rules/ 원본(위치 B) + §7(위치 C)
**Mac**: CLAUDE.md §2(위치 A) + rules/ 원본(위치 B) + **§6**(위치 C)

**해결**: Mac에서는 §6 REMINDER로 배치. 내용은 동일.

---

## §3. 적용 계획 (3 Phase)

### Phase 1: 신규 파일 생성 + SSOT 기반 확보 (의존성 없음)

> 다른 파일 수정의 전제 조건이 되는 기반 작업

- [x] **P1-1**: `rules/behavioral-standards.md` 신규 생성 ✅
  - 출력 기준 Do/Don't (Effort Level 연동)
  - 검증 정직성 (금지 행동 5종 + 대안 행동)
  - 턴 예산 (Turn 정의 + Read/Write 분리)
  - 컨텍스트 경계 (Teammate 완료 메시지만 수신)
  - **검증**: 파일 존재 + 5개 섹션 확인 ✅

- [x] **P1-2**: CLAUDE.md 버전 통일 ✅
  - 1행: `V5.1.0` → `V5.3.0`
  - 3행: `Version: 5.2.0` → `Version: 5.3.0`
  - 푸터: `V5.2.0` → `V5.3.0`
  - **검증**: 1행(1), 3행(3), 푸터(176) 버전 일치 ✅

- [x] **P1-3**: CLAUDE.md §2 Rules 테이블 포인터 추가 ✅
  - behavioral-standards.md 행 추가 (4번째 행)
  - **검증**: Rules 테이블 4행, `ls rules/ | wc -l` = 4 ✅

### Phase 2: orchestration.md 확장 (핵심 변경)

> 기존 규칙 형식 변환 + 신규 규칙 추가

- [x] **P2-1**: §2.4 축약 금지 → Do/Don't 테이블 전환 ✅
  - 기존 blockquote → Do/Don't 테이블 3행 교체
  - **검증**: Do/Don't 테이블 3행 존재 ✅

- [x] **P2-2**: §2.4 검증 정직성 규칙 추가 ✅
  - 검증 루프 프로토콜 하단에 5줄 추가
  - **검증**: "검증 정직성" 헤딩 존재 ✅

- [x] **P2-3**: §2.5 Teammate 규칙 7/8/9 추가 ✅
  - 7: 턴 예산 준수, 8: 출력 정제, 9: 중간 결과 격리
  - **검증**: 규칙 9번까지 존재 ✅

- [x] **P2-4**: §2.5 동시성 보호 테이블 +1행 ✅
  - 컨텍스트 오염 행 추가
  - **검증**: 동시성 보호 6행 ✅

### Phase 3: CLAUDE.md + memory-protocol.md 마무리

> 3중 반복 배치 + 스킬 예산 + 변경이력 + 메모리 Do/Don't

- [x] **P3-1**: CLAUDE.md §1 비위맞추기 금지 추가 ✅
  - Language 하단 41행에 배치
  - **검증**: §1에 "비위맞추기" 존재 ✅

- [x] **P3-2**: CLAUDE.md §2 CRITICAL 블록 추가 ✅
  - Rules 포인터 하단 56행에 배치
  - **검증**: §2에 "CRITICAL" 존재 ✅

- [x] **P3-3**: CLAUDE.md §3 스킬 예산 인식 추가 ✅
  - §3 Settings Reference 하단 76행에 배치
  - **검증**: §3에 "Skills Budget" 존재 ✅

- [x] **P3-4**: CLAUDE.md §5 변경이력 V5.3.0 항목 추가 ✅
  - V5.2.0 위에 V5.3.0 항목 삽입 (7가지 기법 + Mac 최적화)
  - **검증**: "V5.3.0" 항목 존재 ✅

- [x] **P3-5**: CLAUDE.md §6 REMINDER 신설 ✅
  - 푸터 직전에 §6 추가 (3개 규칙)
  - **검증**: `## 6. REMINDER` 존재 + 3개 규칙 ✅

- [x] **P3-6**: memory-protocol.md 메모리 작성 Do/Don't 추가 ✅
  - "메모리 생명주기" 다음에 3행 Do/Don't 테이블 추가
  - **검증**: "메모리 작성 Do & Don't" 헤딩 존재 ✅

---

## §4. 적용 제외 항목 (Mac에서 불필요)

| 항목 | 이유 |
|------|------|
| template-protocol.md 생성 | Mac은 orchestration.md §2.7에 통합됨 |
| §2.3 에이전트 31개 갱신 | Mac 28개가 실 에이전트 수. WE의 3개(quality-manager, context-manager, plan-verifier)는 Mac에 미설치 |
| §2.3 스킬 49개 갱신 | Mac 52개가 실 스킬 수. WE 기준이 아닌 Mac 기준 유지 |
| CLAUDE.md §5 Component Catalog | WE 전용 섹션 (Mac 불필요) |
| D-3 레포 목록 확장 | 앤 별도 판단 사항 |
| A-3 스킬 description 감사 | 별도 세션에서 수행 (52개 스킬 개별 점검) |

---

## §5. 적용 순서 의존성 그래프

```
Phase 1 (기반)
    P1-1 behavioral-standards.md ─────────────────────────────────┐
    P1-2 CLAUDE.md 버전 수정 ──────────────────────┐              │
    P1-3 CLAUDE.md Rules 포인터 ───────────────────┤              │
                                                   │              │
Phase 2 (orchestration.md)                         │              │
    P2-1 §2.4 Do/Don't ───────────────────────┐    │              │
    P2-2 §2.4 검증 정직성 ─────────────────────┤    │              │
    P2-3 §2.5 규칙 7/8/9 ─────────────────────┤    │              │
    P2-4 §2.5 동시성 +1행 ─────────────────────┤    │              │
                                               │    │              │
Phase 3 (CLAUDE.md 마무리)                      │    │              │
    P3-1 §1 비위맞추기 ───────────────────── depends P1-2          │
    P3-2 §2 CRITICAL ─────────────────────── depends P1-3          │
    P3-3 §3 스킬 예산 ────────────────────── depends P1-2          │
    P3-4 §5 변경이력 ─────────────────────── depends all Phase 2   │
    P3-5 §6 REMINDER ─────────────────────── depends P3-1,P3-2    │
    P3-6 memory Do/Don't ──────────────────── depends P1-1 ────────┘
```

**규칙**: Phase 내 항목은 병렬 가능, Phase 간은 순차.

---

## §6. 플로어 검증 체크리스트 (전체 완료 후)

### 파일 존재 검증

- [x] `~/.claude/rules/behavioral-standards.md` 존재 (71줄±) ✅
- [x] `~/.claude/rules/orchestration.md` 갱신됨 ✅
- [x] `~/.claude/rules/memory-protocol.md` 갱신됨 ✅
- [x] `~/.claude/CLAUDE.md` V5.3.0 ✅

### CLAUDE.md 검증 (9항목)

- [x] 1행: 제목에 `V5.3.0` 포함 ✅
- [x] 3행: `Version: 5.3.0` ✅
- [x] §1: "비위맞추기 금지" 존재 (41행) ✅
- [x] §2: Rules 테이블 4행 (behavioral-standards 포함) ✅
- [x] §2: "CRITICAL" 블록 존재 (56행) ✅
- [x] §3: "Skills Budget" 존재 (76행) ✅
- [x] §5: "V5.3.0" 변경이력 존재 (112행) ✅
- [x] §6: "REMINDER" 섹션 존재 + 3개 규칙 (168~172행) ✅
- [x] 푸터: `V5.3.0` 포함 (176행) ✅

### orchestration.md 검증 (4항목)

- [x] §2.4: Do/Don't 테이블 존재 (3행) ✅
- [x] §2.4: "검증 정직성" 헤딩 존재 ✅
- [x] §2.5: Teammate 규칙 9개 (7/8/9 추가) ✅
- [x] §2.5: 동시성 보호 6행 (컨텍스트 오염 추가) ✅

### memory-protocol.md 검증 (1항목)

- [x] "메모리 작성 Do & Don't" 헤딩 + 3행 테이블 존재 ✅

### behavioral-standards.md 검증 (5항목)

- [x] "출력 기준" 섹션 존재 ✅
- [x] "Effort Level 연동" 테이블 존재 ✅
- [x] "검증 정직성" 섹션 존재 (금지 5종) ✅
- [x] "턴 예산" 섹션 존재 ✅
- [x] "컨텍스트 경계" 섹션 존재 ✅

### 3중 반복 배치 검증 (3규칙 × 3위치)

| 규칙 | 위치 A (CLAUDE.md §2) | 위치 B (rules/ 원본) | 위치 C (CLAUDE.md §6) |
|------|----------------------|---------------------|----------------------|
| 체인 축약 금지 | ✅ CRITICAL 56행 | ✅ orchestration §2.4 Do/Don't | ✅ REMINDER 170행 |
| 메모리 격리 | (CRITICAL 미포함) | ✅ memory-protocol "Teammate 세션" | ✅ REMINDER 171행 |
| 비위맞추기 금지 | ✅ CRITICAL 57행 | ✅ lessons-learned #4 | ✅ REMINDER 172행 |

### 정합성 검증 (3항목)

- [x] CLAUDE.md 1행/3행/푸터 버전 **3곳 일치** (V5.3.0) ✅
- [x] Rules 테이블 행 수 (4) = `ls rules/ | wc -l` (4) 일치 ✅
- [x] behavioral-standards.md의 규칙이 CLAUDE.md CRITICAL/REMINDER와 **의미 일관** ✅

---

## §7. 리스크 및 롤백

### 리스크 매트릭스

| 리스크 | 확률 | 영향 | 완화 |
|--------|------|------|------|
| 기존 Hook이 새 rules/ 파일 인식 못함 | 낮 | 낮 | rules/는 auto-loaded — 추가 설정 불필요 |
| 3중 반복이 컨텍스트 과소비 | 중 | 낮 | 5줄 미만 × 3위치 = ~15줄 증가 (전체 대비 미미) |
| Do/Don't 테이블이 기존 축약 금지 의미 훼손 | 낮 | 중 | 의미 1:1 대응 확인 + 기존 3개 조건 모두 포함 |
| memory-protocol.md 청크 분할 영향 | 낮 | 낮 | 새 ## 헤딩 1개 추가 — Qdrant 청크 1개 증가뿐 |

### 롤백 계획

모든 변경 전 Git 상태 확인. 롤백 필요 시:
```bash
cd ~/.claude && git diff  # 변경 확인
cd ~/.claude && git checkout -- .  # 전체 롤백
```

> ⚠️ ~/.claude가 Git 레포가 아닌 경우, Phase 1 시작 전 수동 백업:
> `cp -r ~/.claude ~/.claude_backup_v520`

---

## 관련 문서

### Direct Links
- [[28_Claude_Code_Source_Code_Analysis.md]] — 7가지 기법 정리 (소스)
- [[29_Source_Code_Techniques_Application.md]] — WE 적용 방안 v1.2.0 (적용 문구 참조)
- [[30_V530_Application_Report.md]] — WE 적용 결과 (23/23 PASS)
- [[31_V530_Senior_Verification_Report.md]] — WE 시니어 검증 (8/10)
- [[32_V530_Remediation_Plan.md]] — WE 수정 작업계획서

### Backlinks
- [[24_Current_System_Analysis.md]] — V5.2.0 현황 분석 (72/100)

---

## Release Notes

### v1.0.0 (2026-04-07)
- 초기 작성: Mac vs WE 환경 차이 11건, 3 Phase 적용 계획, 플로어 검증 26항목
- 앤 원본 프롬프트: "맥용으로 변경해야해. 맥용 적용 계획에 대해 충돌지점등을 검토하고 최적화해야해, 해당 작업을 진행해서 작업계획서를 33번 문서로 작성해줘 계획서는 체크박스 달아서 검증도 하게 해주고 진행해줘"
