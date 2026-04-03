# html2pptx-converter E2E 테스트 최종 보고서

> Version: 1.0 | Date: 2026-03-12
> Tester: 아리 (AI Partner) | Reviewer: 앤 (Project Leader)
> Skill: `~/.claude/skills/html2pptx-converter/`

---

## 1. 테스트 실행 개요

| 항목 | 값 |
|------|-----|
| 테스트 유형 | End-to-End 블라인드 테스트 |
| 실행 일시 | 2026-03-11 23:44 ~ 2026-03-12 00:06 (약 22분) |
| 입력 파일 | test_layout.html, test_layout.png, test_layout_description.md, test_layout_fields.md |
| 최종 PPTX | presentation.pptx (124,432 bytes, 4 슬라이드) |
| 기계적 판정 | PASS (13/13 TC, TC-13 SKIP) |

---

## 2. 테스트 계획 vs 실제 결과 비교

### 2.1 TC별 계획/실행 대조표

| TC | 계획 (E2E_test_plan.md) | 실제 (E2E_test_sheet.md) | 일치 여부 | 차이점 |
|----|------------------------|------------------------|----------|--------|
| TC-01 | 스킬 트리거 → 입력 가이드 텍스트 출력 → 4개 파일 수집 | 스킬 트리거 → SKILL.md 읽기 → 4개 파일 수집 | **부분 일치** | 입력 가이드 텍스트가 간소화됨 (4개 파일이 프롬프트에 이미 명시) |
| TC-02 | AskUserQuestion으로 출력 경로 질문 | 질문 없이 자동 결정 (옵션 b) | **부분 일치** | AskUserQuestion 생략됨 — 테스트 시트에서 경로가 암시적으로 제공 |
| TC-03 | Leader가 4개 파일 존재/인코딩/형식 검증 | Leader가 ls, file, python으로 검증 | **일치** | chardet 미설치 → UTF-8 직접 읽기로 대체 |
| TC-04 | Teammate-A(opus) → spec.json 생성 | Teammate-A 무응답 → Leader 직접 수행 | **불일치** | Teammate-A Agent 무응답 (3분 대기 후 Leader fallback) |
| TC-05 | Leader가 spec.json 스키마 검증 → Phase 2 | 검증 통과 → Phase 2 진행 | **일치** | |
| TC-06 | Teammate-B(opus) → 4개 HTML 생성 | Teammate-B(opus, 동기) → 4개 HTML 생성 | **일치** | 동기 모드로 실행 (백그라운드 아님) |
| TC-07 | validate_html.py → 0 errors | 0 errors, 0 warnings, 전체 PASS | **일치** | 첫 시도에서 통과 (수정 없음) |
| TC-08 | Leader가 html_validation 확인 → Phase 3 | summary.pass=true → Phase 3 | **일치** | |
| TC-09 | Teammate-C(opus) → convert.js + node → PPTX | convert.js 생성 → node 실행 → 124KB PPTX | **일치** | |
| TC-10 | thumbnail.py + compare_slides.py | PowerPoint COM 대체 + compare_slides.py | **부분 일치** | LibreOffice 미설치 → COM 자동화 대체 |
| TC-11 | 시각 검사 → validation.json | 시각 검사 완료 → validation.json (4 low issues) | **일치** | |
| TC-12 | overall_quality 기반 분기 | "pass" → Phase 4 건너뜀 | **일치** | |
| TC-13 | 조건부 실행 | SKIP (overall_quality == "pass") | **일치** | |
| TC-14 | 최종 보고 + 파일 검증 | 필수 파일 12개 모두 존재 | **일치** | |

### 2.2 일치/불일치 통계

| 구분 | TC 수 | 비율 |
|------|------|------|
| **완전 일치** | 10 | 71% |
| **부분 일치** | 3 | 21% |
| **불일치** | 1 | 7% |

### 2.3 예상 실패 시나리오 대비 실제

| 계획의 예상 시나리오 | 실제 발생 여부 | 대응 결과 |
|-------------------|-------------|----------|
| pptxgenjs 미설치 | 미발생 (이미 설치됨) | N/A |
| Playwright 미설치 | 미발생 | N/A |
| Pillow 미설치 | 미발생 (이미 설치됨) | N/A |
| spec.json 스키마 불일치 | 미발생 | N/A |
| HTML 검증 에러 | 미발생 | N/A |
| node convert.js 실패 | 미발생 | N/A |
| 테이블 렌더링 복잡도 | 미발생 (low severity만) | N/A |
| 코너 마커 위치 편차 | 미발생 | N/A |
| **[미예상] Teammate-A 무응답** | **발생** | **Leader fallback** |
| **[미예상] LibreOffice 미설치** | **발생** | **PowerPoint COM 대체** |
| **[미예상] chardet 미설치** | **발생** | **UTF-8 직접 읽기** |
| **[미예상] cp949 인코딩 에러** | **발생** | **stdout UTF-8 재설정** |

---

## 3. 아리의 테스트 발견사항 (AI 테스터 관점)

> 아래는 E2E 테스트 실행 중 발견된 기술적 이슈와 개선 필요사항입니다.
> 앤의 의견과 무관하게 독립적으로 기록합니다.

### 3.1 Teammate-A (spec-analyzer) 무응답 이슈 [심각도: 높음]

**현상**:
- Agent tool로 Teammate-A를 `run_in_background=true`로 스폰
- 약 3분 대기 후에도 spec.json 미생성
- CLAUDE.md 규칙(120초 타임아웃)에 따라 Leader 직접 수행으로 전환

**원인 추정**:
- 백그라운드 Agent의 Write 도구 권한 문제 (도구 승인 대기로 블로킹)
- 또는 Agent 실행 자체의 지연/실패

**영향**:
- 파이프라인 전체 지연 (~3분 낭비)
- Leader fallback으로 결과물 품질에는 영향 없음

**수정 권고**:
1. **Teammate-A는 동기 모드(foreground) 우선 사용** — 백그라운드 Agent는 도구 권한 이슈에 취약
2. **SKILL.md에 spawn 모드 명시**: "Teammate-A: 동기 모드 권장, 백그라운드 시 `mode=bypassPermissions` 필수"
3. **Agent 프롬프트에 `mode=bypassPermissions` 추가** — Teammate-B/C는 이 모드로 정상 동작 확인

### 3.2 thumbnail.py LibreOffice 의존성 [심각도: 중간]

**현상**:
- thumbnail.py가 `soffice`(LibreOffice) + `pdftoppm` 의존
- Windows 환경에 LibreOffice 미설치
- Teammate-C가 PowerPoint COM 자동화(`comtypes`)로 대체 수행

**영향**:
- 기능적으로 동등한 결과물 생성 → 테스트 자체에는 영향 없음
- 하지만 재현성 보장 안 됨 (PowerPoint 미설치 환경에서는 둘 다 실패)

**수정 권고**:
1. **thumbnail.py에 Windows 대체 경로 추가**: PowerPoint COM → LibreOffice → Playwright(fallback)
2. **engine/thumbnail.py에 플랫폼 감지 로직 추가**: `sys.platform == 'win32'` 시 COM 자동화 우선
3. **Playwright 기반 PDF→PNG 대체도 고려**: 가장 범용적 (Node.js만 필요)

### 3.3 Python 패키지 의존성 관리 부재 [심각도: 낮음]

**현상**:
- `chardet` 미설치 → UTF-8 직접 읽기로 우회
- `cp949` 인코딩 에러 → `sys.stdout.reconfigure(encoding='utf-8')` 추가
- `comtypes` 별도 설치 필요

**수정 권고**:
1. **requirements.txt 추가**: `scripts/requirements.txt` 또는 `engine/requirements.txt`
2. **필수 패키지 목록 정리**: Pillow, chardet(선택), comtypes(Windows 선택)
3. **SKILL.md "환경 요구사항" 섹션 보강**

### 3.4 HTML 슬라이드 품질 — 기계적 관점 [심각도: 정보]

**validation.json 결과**: overall_quality = "pass", 4개 low severity 이슈

| # | Slide | 이슈 | 원인 |
|---|-------|------|------|
| 1 | 0 | "Contact" nav 링크 줄바꿈 | 텍스트 폭 > 가용 공간 |
| 2 | 1 | Quick Links → 텍스트 전용 | 이모지 아이콘 PPTX 미지원 |
| 3 | 1 | Category 뱃지 → 플레인텍스트 | 색상 pill 뱃지의 PPTX 한계 |
| 4 | 3 | "Terms of Service" 줄바꿈 | 컬럼 폭 부족 |

**평가**: HTML→PPTX 변환의 일반적 한계 범위 내. 기계적으로는 PASS.

### 3.5 테스트 계획의 미비점 [심각도: 정보]

| 미비 항목 | 설명 |
|----------|------|
| **Agent spawn 모드 미명시** | 계획에서 동기/비동기 모드 미지정 → 실행 시 불일치 발생 |
| **Windows 환경 의존성** | 계획에 chardet, LibreOffice, comtypes 등 실패 시나리오 미포함 |
| **Teammate 무응답 시나리오** | 계획의 "잠재 실패 시나리오"에 Agent 무응답 미포함 |
| **인코딩 이슈 시나리오** | Windows cp949 stdout 에러 미예상 |

---

## 4. 앤의 결과물 검토 의견 (프로젝트 리더 관점)

> 아래는 앤이 직접 결과물을 검토한 후 제시한 핵심 수정 방향입니다.
> 이 의견은 스킬의 근본적 설계 방향에 관한 것으로, 아리의 기계적 테스트 결과와 별개로 반영되어야 합니다.

### 4.1 핵심 피드백: 출력물의 디자인 방향 불일치 [심각도: 최고]

**현재 출력물** (slide_00~03.html + presentation.pptx):
```
- 컬러풀한 원본 재현 (파란 배경 #2B6CB0, 빨간 버튼 #E53E3E, 진녹 #38A169 등)
- 원본 HTML의 시각적 충실도(fidelity) 최대화 목표
- 디스크립션 영역 없음
```

**기대 출력물** (partnering_main_eng_wireframe.html/pptx 참조):
```
- 흑백 와이어프레임 스타일 (#000000, #808080, #E0E0E0, #FFFFFF만 사용)
- 선(border)과 면(background)으로 UI 구조를 표현
- 오른쪽에 디스크립션(화면 구성 설명) 패널 포함
- 번호 배지(1~N)로 각 영역을 식별
```

**불일치의 근본 원인**:

| 관점 | 현재 스킬 | 기대 방향 |
|------|----------|----------|
| **목적** | 원본 UI의 시각적 복제 | 원본 UI의 구조적 표현 (와이어프레임) |
| **색상** | 원본 색상 유지 (full_design 모드) | 흑백 팔레트만 사용 |
| **구성** | 슬라이드당 1개 컨텐츠 영역 | 컨텐츠 + 오른쪽 디스크립션 패널 |
| **표현** | 도형 = 실제 UI 요소 재현 | 도형 = 와이어프레임 블록 + 텍스트 라벨 |
| **참조 표기** | 없음 | 번호 배지(badge)로 영역 식별 |
| **설명 텍스트** | 없음 | 각 영역의 기능/역할 설명 텍스트 |

### 4.2 참조 파일 상세 분석

#### 참조: partnering_main_eng_wireframe.html

```
┌──────────────────────────────┬────────────┐
│                              │            │
│   [1] 광고 배너 (#808080)     │  화면 구성  │
│                              │  설명       │
│ ┌────┐                       │            │
│ │[2] │ 사이드바               │  1. 광고배너 │
│ │NAV │         [3] 헤더 바     │  2. 네비    │
│ │    │                       │  3. 헤더    │
│ │    │  [4] Requests Summary │  4. 요약    │
│ │    │  [5] Today's Meetings │  5. 미팅    │
│ │    │  [6] Important Dates  │  ...       │
│ │    │  [7][8][9][10] 카드들   │  10. 문의  │
│ └────┘                       │            │
│                              │            │
└──────────────────────────────┴────────────┘
```

**핵심 특성**:
- body 크기: `1684pt x 1191pt` (표준 16:9가 아닌 대형 레이아웃)
- 색상: `#000000`(선/배지), `#808080`(영역 구분), `#E0E0E0`(배경 음영), `#FFFFFF`(기본)
- 디스크립션 패널: 오른쪽 `275pt` 폭, `화면 구성 설명` 제목 + 10개 항목 설명
- 번호 배지: 20pt 검정 원형, 흰색 숫자, 각 영역 좌상단에 배치

#### 참조: partnering_main_eng_wireframe.pptx

- 위 HTML을 html2pptx 엔진으로 변환한 결과물
- 1 슬라이드에 전체 레이아웃 + 디스크립션 패널 포함
- 흑백으로 선과 면만 사용한 구조적 표현

### 4.3 현재 출력물과 참조 출력물의 구체적 차이

| 속성 | 현재 slide_00.html | 참조 wireframe.html | 차이 |
|------|-------------------|-------------------|------|
| **body 크기** | 720pt x 405pt | 1684pt x 1191pt | 크기 체계 다름 |
| **배경색** | `#2B6CB0` (파란색) | `#FFFFFF` (흰색) | 컬러 vs 흑백 |
| **텍스트 색상** | `#FFFFFF`, `#BEE3F8`, `#CBD5E0` | `#000000`, `#FFFFFF` | 다색 vs 흑백 |
| **도형 색상** | `#E53E3E`, `#3182CE`, `#38A169`, `#D69E2E`, `#805AD5` | `#808080`, `#E0E0E0` | 5+ 색상 vs 2 중립색 |
| **디스크립션** | 없음 | 오른쪽 275pt 패널 | 구조 설명 부재 |
| **번호 배지** | 없음 | 1~10번 검정 원형 | 영역 식별 부재 |
| **border 스타일** | 컬러 (2pt solid #2B6CB0 등) | 흑백 (0.5~2pt solid #000000) | 컬러 vs 흑백 |

---

## 5. 종합 수정사항 목록

> 아리의 테스트 발견사항 + 앤의 결과물 검토 의견을 통합한 전체 수정 목록입니다.
> 두 관점의 발견사항을 동등하게 반영합니다.

### 5.1 설계 방향 수정 (앤 의견 기반) [Priority: P0 — 필수]

| # | 수정 항목 | 현재 | 목표 | 영향 범위 |
|---|----------|------|------|----------|
| D-1 | **출력 스타일을 와이어프레임으로 전환** | 원본 색상 재현 (full_design) | 흑백 와이어프레임 (#000/#808080/#E0E0E0/#FFF) | SKILL.md, spec-analyzer, html-slide-builder |
| D-2 | **디스크립션 패널 추가** | 슬라이드 = 컨텐츠만 | 컨텐츠 + 오른쪽 디스크립션 패널 | html-slide-builder, spec-analyzer |
| D-3 | **번호 배지 시스템 추가** | 영역 식별 없음 | 각 영역에 검정 원형 번호 배지 배치 | spec-analyzer, html-slide-builder |
| D-4 | **body 크기 체계 재검토** | 720pt x 405pt (표준 16:9) | 입력 HTML에 맞는 유동적 크기 또는 대형 레이아웃 | SKILL.md, html2pptx.md |
| D-5 | **spec.json에 wireframe 모드 추가** | design.mode = "full_design" | design.mode = "wireframe" 추가 | spec-analyzer, spec.json schema |
| D-6 | **색상 팔레트 변환 로직 추가** | 원본 색상 그대로 사용 | wireframe 모드: 자동으로 흑백 팔레트 매핑 | spec-analyzer |

### 5.2 기술적 이슈 수정 (아리 발견 기반) [Priority: P1 — 중요]

| # | 수정 항목 | 현재 | 목표 | 영향 범위 |
|---|----------|------|------|----------|
| T-1 | **Teammate-A spawn 모드 변경** | run_in_background=true (불안정) | 동기 모드 또는 mode=bypassPermissions 필수 | SKILL.md |
| T-2 | **thumbnail.py Windows 호환** | LibreOffice 전용 | PowerPoint COM → LibreOffice → Playwright 3단 fallback | engine/thumbnail.py |
| T-3 | **requirements.txt 추가** | 없음 | Pillow, chardet, comtypes(win) 명시 | scripts/requirements.txt |
| T-4 | **Windows 인코딩 처리** | cp949 stdout 에러 발생 | UTF-8 강제 설정 가이드 추가 | SKILL.md, scripts/ |

### 5.3 테스트 인프라 개선 (양쪽 통합) [Priority: P2 — 개선]

| # | 수정 항목 | 현재 | 목표 | 영향 범위 |
|---|----------|------|------|----------|
| I-1 | **E2E_test_plan에 Agent 무응답 시나리오 추가** | 미포함 | "잠재 실패 시나리오"에 추가 | E2E_test_plan.md |
| I-2 | **E2E_test_plan에 Windows 의존성 시나리오 추가** | 미포함 | LibreOffice, chardet, cp949 추가 | E2E_test_plan.md |
| I-3 | **Agent spawn 모드 명시** | 미지정 | 각 TC에 동기/비동기 모드 명시 | E2E_test_plan.md |
| I-4 | **와이어프레임 검증 TC 추가** | 없음 | 흑백 팔레트 검증, 디스크립션 패널 존재 확인 | E2E_test_sheet.md |

---

## 6. 스킬 수정 권고안 — 파일별 상세

### 6.1 SKILL.md 수정

```
변경 내용:
1. "출력 스타일" 섹션 추가
   - wireframe 모드: 흑백 (#000/#808/#E0E0E0/#FFF), 디스크립션 패널, 번호 배지
   - full_design 모드: 원본 색상 유지 (기존 방식, 옵션으로 유지 가능)
   - 기본값: wireframe

2. Teammate-A spawn 규칙
   - "동기 모드 우선 사용"
   - 백그라운드 시 mode=bypassPermissions 필수

3. 환경 요구사항
   - Node.js: pptxgenjs
   - Python: Pillow, chardet(선택)
   - Windows 추가: comtypes(선택)
```

### 6.2 agents/01-spec-analyzer.md 수정

```
변경 내용:
1. wireframe 모드 분석 로직 추가
   - 입력 HTML의 색상 → 흑백 매핑 테이블 생성
   - 원본 색상 #RRGGBB → wireframe 대체색 결정 규칙:
     * 배경색 → #FFFFFF 또는 #E0E0E0
     * 텍스트색 → #000000
     * 강조색 → #808080
     * 구분선 → #000000 (0.5~2pt)

2. 디스크립션 패널 데이터 생성
   - spec.json에 "description_panel" 필드 추가:
     * 패널 제목: "화면 구성 설명"
     * 각 영역: {번호, 이름, 설명 텍스트}
   - 기존 elements에 badge 요소 추가

3. 번호 배지 요소 자동 생성
   - 각 영역의 좌상단에 badge shape 추가
   - badge: 20pt 검정 원형, 흰색 숫자
```

### 6.3 agents/02-html-slide-builder.md 수정

```
변경 내용:
1. wireframe HTML 템플릿 추가
   - body 크기: 입력에 따라 유동적 (또는 대형 레이아웃)
   - 색상: #000000, #808080, #E0E0E0, #FFFFFF만 사용
   - border: 0.5pt~2pt solid #000000
   - font-weight: bold (제목), normal (설명)

2. 디스크립션 패널 HTML 생성 로직
   - 오른쪽 영역 (전체 높이의 ~16% 폭)
   - 패널 제목 (12pt Bold + 하단 2pt 검정선)
   - 항목별: 번호 + 이름(Bold) + 설명 텍스트

3. 번호 배지 CSS 클래스
   - .badge { position:absolute; width:20pt; height:20pt; background:#000000; border-radius:50%; }
   - .badge p { color:#ffffff; font-size:9.75pt; font-weight:bold; }

4. 와이어프레임 도형 규칙
   - 카드/섹션: background:#FFFFFF, border:0.5pt solid #000000
   - 비활성 영역: background:#E0E0E0
   - 버튼/액션: background:#808080 + 흰색 텍스트
   - 구분선: border-bottom:0.5pt solid #000000
```

### 6.4 agents/03-executor-validator.md 수정

```
변경 내용:
1. validation.json에 wireframe 검증 항목 추가
   - 흑백 팔레트 준수 확인 (#000/#808/#E0E0E0/#FFF 외 색상 검출 시 이슈)
   - 디스크립션 패널 존재 확인
   - 번호 배지 존재/위치 확인

2. thumbnail.py 호출 시 fallback 체인 안내
```

### 6.5 engine/html2pptx.md 수정

```
변경 내용:
1. 와이어프레임 모드 섹션 추가
   - 지원 색상: #000000, #808080, #E0E0E0, #FFFFFF
   - border 스타일: solid만 (dashed/dotted 제한)
   - font: 1종 (Arial)
   - 가이드: body 크기가 720x405pt가 아닐 수 있음 → defineLayout 필요

2. 디스크립션 패널 변환 가이드
   - body position:relative + 패널 position:absolute
   - PptxGenJS: addText로 패널 내용 렌더링
```

### 6.6 scripts/validate_html.py 수정

```
변경 내용:
1. wireframe 모드 검증 규칙 추가
   - --mode wireframe 플래그
   - 허용 색상 목록 체크: #000000, #808080, #E0E0E0, #FFFFFF만
   - CSS gradient 금지 (기존과 동일)
   - 비허용 색상 사용 시 error 또는 warning

2. Windows 호환성
   - chardet 없을 때 graceful fallback
   - stdout encoding 가이드
```

### 6.7 engine/thumbnail.py 수정

```
변경 내용:
1. 3단 fallback 체인:
   try: PowerPoint COM (Windows)
   except: try: LibreOffice (soffice)
   except: try: Playwright (브라우저 기반)
   except: error

2. 플랫폼 감지:
   if sys.platform == 'win32': COM 우선
   else: LibreOffice 우선
```

---

## 7. 참조 파일 vs 현재 출력 — 시각 비교 요약

### 와이어프레임 HTML (참조: partnering_main_eng_wireframe.html)

```
┌─────────────────────────────────────────────────────────┐
│ 특성                                                     │
│ - 단색 계열: #000, #808080, #E0E0E0, #FFF               │
│ - 전체 1 페이지에 모든 영역 배치 (분할 없음)               │
│ - 오른쪽 275pt 디스크립션 패널                             │
│ - 10개 번호 배지 (20pt 검정 원형)                         │
│ - border 기반 영역 구분                                   │
│ - 텍스트: 실제 데이터 (lorem ipsum 아님)                   │
│ - body: 1684pt x 1191pt (비표준 크기)                     │
└─────────────────────────────────────────────────────────┘
```

### 현재 슬라이드 HTML (slide_00~03.html)

```
┌─────────────────────────────────────────────────────────┐
│ 특성                                                     │
│ - 다색: #2B6CB0, #E53E3E, #38A169, #805AD5, #D69E2E 등  │
│ - 4개 슬라이드로 분할                                     │
│ - 디스크립션 패널 없음                                     │
│ - 번호 배지 없음 (코너 마커는 테스트용)                     │
│ - 원본 UI 시각적 충실도(fidelity) 우선                     │
│ - body: 720pt x 405pt (표준 16:9)                        │
└─────────────────────────────────────────────────────────┘
```

---

## 8. 최종 판정

### 8.1 기계적 테스트 결과 (아리)

| 판정 | PASS (13/13 TC, TC-13 SKIP) |
|------|----------------------------|
| 근거 | 파이프라인 전 단계 정상 작동, 필수 파일 전체 생성, overall_quality="pass" |

### 8.2 결과물 품질 판정 (앤)

| 판정 | **FAIL — 설계 방향 불일치** |
|------|---------------------------|
| 근거 | 출력물이 와이어프레임이 아닌 컬러풀한 원본 재현임. 디스크립션 패널 부재. 번호 배지 부재. |
| 참조 | partnering_main_eng_wireframe.html/pptx가 올바른 출력 형태 |

### 8.3 종합 판정

| 판정 | **조건부 PASS — 스킬 설계 수정 필요** |
|------|-------------------------------------|
| 사유 | 파이프라인 엔진(html2pptx.js)과 실행 인프라는 정상 작동 확인. 단, 스킬의 출력 방향(full_design vs wireframe)이 기대와 불일치하므로, 6장의 수정 권고안에 따라 스킬 전체 수정 필요. |

---

## 9. 수정 우선순위 요약

| 우선순위 | 항목 | 수정 파일 |
|---------|------|----------|
| **P0** | 와이어프레임 모드 도입 (D-1~D-6) | SKILL.md, 01-spec-analyzer.md, 02-html-slide-builder.md |
| **P1** | Teammate-A spawn 안정화 (T-1) | SKILL.md |
| **P1** | thumbnail.py Windows 호환 (T-2) | engine/thumbnail.py |
| **P2** | requirements.txt 추가 (T-3) | scripts/requirements.txt |
| **P2** | Windows 인코딩 처리 (T-4) | SKILL.md, scripts/ |
| **P2** | 테스트 인프라 개선 (I-1~I-4) | E2E_test_plan.md, E2E_test_sheet.md |

---

*End of E2E Test Final Report — 아리의 기술적 발견사항과 앤의 결과물 검토 의견을 동등하게 반영합니다*
