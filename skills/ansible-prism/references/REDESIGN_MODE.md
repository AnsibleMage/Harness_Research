# REDESIGN MODE v1.0 — 와이어프레임 → 창의적 시각 변환

> 기존 와이어프레임의 콘텐츠를 100% 보존하면서 시각적으로 완전히 다른 결과물 생성.
> CREATIVE_GENERATION_FRAMEWORK의 원래 작동 모드.

---

## 트리거 조건

```
다음 중 하나라도 해당하면 REDESIGN 모드:
- 와이어프레임/HTML 파일이 입력됨
- "리디자인", "redesign", "다시 만들어줘" 키워드
- "이 와이어프레임으로", "이 파일 기반으로" 키워드
- 참조 HTML/URL이 제공됨
```

---

## 입력

```yaml
required:
  wireframe: HTML 파일 (opt1.html 등)
    → 모든 텍스트, 링크, 섹션 구조를 읽어서 보존

optional:
  design_system: HTML/URL (디자인 토큰 추출)
    → 없으면 SLOT_ENGINE에서 자동 생성
  user_direction: "밝게", "어둡게", "YouTube 스타일" 등
    → SLOT 선택에 영향
```

---

## 와이어프레임 파싱 규칙

### 1. 콘텐츠 추출

```yaml
extract:
  - 모든 텍스트 노드 (제목, 본문, 링크 텍스트, 버튼 텍스트)
  - 모든 href 링크
  - 모든 데이터 (숫자, 통계, 전화번호, 이메일)
  - 섹션 구조 (<!-- S01: Header --> 주석 또는 <section> 태그)
  - 이미지 alt 텍스트 (있으면)
  - 탭/아코디언 구조 (상태 전환 UI)
```

### 2. 콘텐츠 보존 규칙

```
ABSOLUTE:
  - 텍스트 내용 변경 금지 (오타 수정도 금지)
  - 섹션 삭제 금지
  - 데이터 값 변경 금지
  - 링크 href 변경 금지

ALLOWED:
  - 섹션 순서 변경 (SLOT_3 구조에 따라)
  - 섹션 내부 레이아웃 변경 (좌→우, 수직→수평 등)
  - 컴포넌트 위치 재배치 (nav를 sidebar로 이동 등)
  - 시각적 표현 완전 변경 (색, 폰트, 레이아웃, 모션)
```

### 3. 섹션 매핑

```
와이어프레임 섹션 → 결과물 섹션 1:1 매핑

예: opt1.html
  S01: Header → nav 컴포넌트
  S02: Banner + Library → hero/검색 + 도서관 배너
  S03: Learning Status → 학습 현황 (도넛차트+교육과목)
  S04: CLASSROOM → 코스 카드 (탭 UI 포함)
  S05: Continue Learning → 이어서 학습하기 (진행 바)
  S06: Channels + Books → 채널 목록 + 도서 목록
  S07: Contact → 연락처 정보
  S08: Footer → 푸터
```

---

## REDESIGN 모드 전체 플로우

```
사용자: "이 와이어프레임으로 리디자인해줘" + opt1.html
    ↓
[파싱] 와이어프레임 읽기 → 콘텐츠 추출 + 섹션 매핑
    ↓
[STEP 1] RLHF SCAN (와이어프레임의 기존 패턴 분석)
    ↓
[STEP 2] OL 결정 (기본 10)
    ↓
[STEP 3] SLOT 선택 + 세계관 구축 → SLOT_ENGINE.md
    ↓
[STEP 4] 섹션별 PR 리프레이밍
    ↓
[STEP 5] 패턴 선택 (2~3개)
    ↓
[STEP 6] HTML 생성 (콘텐츠 100% 보존 + 시각 완전 변환)
         → IMAGE_ENGINE + MOTION_RULES + CSS_PRECISION + VISUAL_DENSITY 적용
    ↓
[STEP 7] SELF-AUDIT (wireframe_check: 텍스트 100% 보존 확인)
```

---

## 디자인 시스템 입력 시 추가 규칙

```yaml
design_system_provided:
  - DS의 color token을 SLOT_2 대신 사용 (또는 혼합)
  - DS의 font-family를 SLOT_4 대신 사용
  - DS의 spacing/radius 값 존중
  - DS와 SLOT의 충돌 시: DS가 우선 (브랜드 일관성)
  - SLOT은 DS가 정의하지 않은 영역에서만 자유

design_system_not_provided:
  - SLOT_ENGINE.md에서 모든 시각 결정
  - 완전한 자유도
```

---

## 사용자 방향 지시 처리

```yaml
user_direction_mapping:
  "밝게/깔끔하게/화이트":
    → SLOT_2 중 밝은 계열 강제 (순백, 쿨그레이, 민트)
  "어둡게/다크/프리미엄":
    → SLOT_2 중 어두운 계열 강제 (딥네이비, 차콜, 미드나잇, 카카오)
  "YouTube/넷플릭스 스타일":
    → SLOT_3을 섹션스택 또는 대시보드로 파생
    → 나머지 SLOT은 자유
  "미니멀/심플":
    → SLOT_1 중 절제된 스타일 (무인양품, 갤러리, 일본정원)
  "대담한/임팩트":
    → SLOT_1 중 강한 스타일 (네온사인, 빈티지포스터, 공사현장)
  "따뜻한/감성":
    → SLOT_2 중 따뜻한 계열 (웜크림, 양피지, 오크, 앰버)
```
