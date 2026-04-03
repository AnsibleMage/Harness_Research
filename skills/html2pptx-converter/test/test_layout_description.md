# TestCorp Portal — 페이지 기능 설명서

## 개요

TestCorp Portal은 html2pptx 변환 정확도를 검증하기 위한 테스트 페이지입니다. 일반적인 웹 포탈 구조(헤더→히어로→콘텐츠→푸터)를 갖추고 있으며, 좌표 검증용 코너 마커, 도형/라인 렌더링 테스트 영역을 포함합니다.

---

## 영역 구성 (7개 영역)

### 영역 1: 코너 마커 (Corner Markers)

**목적**: PPTX 변환 시 좌표 정확도 검증

| 마커 | 위치 | 색상 | 텍스트 |
|------|------|------|--------|
| TL | 좌상단 (top:0, left:0) | #E53E3E (빨강) | "TL" |
| TR | 우상단 (top:0, right:0) | #3182CE (파랑) | "TR" |
| BL | 좌하단 (bottom:0, left:0) | #38A169 (초록) | "BL" |
| BR | 우하단 (bottom:0, right:0) | #D69E2E (금색) | "BR" |
| CENTER | 정중앙 (50%, 50%) | #805AD5 (보라) | "CENTER" |

- 각 코너 마커는 40x40px 정사각형 (CENTER는 60x60px 원형)
- PPTX에서 각 마커가 슬라이드의 정확한 꼭짓점 및 중앙에 위치하는지 확인
- 라운드 처리: TL은 우하단만, TR은 좌하단만, BL은 우상단만, BR은 좌상단만

### 영역 2: 헤더 네비게이션 (Header Nav)

**목적**: 상단 고정 메뉴 바의 레이아웃, 배경색, 텍스트 정렬 검증

- **구조**: 좌측 로고 텍스트 + 우측 네비게이션 링크 5개
- **배경**: #1E3A5F (다크 네이비)
- **높이**: 64px
- **하단 테두리**: 3px solid #2B6CB0
- **로고**: "TestCorp Portal" — 22px, bold, 흰색
- **메뉴 항목**: Home(활성), Services, Board, About, Contact
- **활성 상태**: Home 링크에 하단 파란 밑줄 (#63B3ED)
- **정렬**: flex, space-between (로고 좌측, 메뉴 우측)

### 영역 3: 히어로 섹션 (Hero Section)

**목적**: 큰 텍스트, 중앙 정렬, 버튼 2개의 렌더링 검증

- **배경**: #2B6CB0 (파란색)
- **패딩**: 상하 80px, 좌우 60px
- **제목**: "Welcome to TestCorp Portal" — 42px, 800 weight, 흰색
- **부제목**: 설명 텍스트 — 18px, #BEE3F8, 최대 640px, 중앙 정렬
- **CTA 버튼 2개**:
  - "Get Started" — #E53E3E 배경, 흰색 텍스트, 8px 라운드
  - "Learn More" — 투명 배경, 흰색 테두리, 흰색 텍스트
- **버튼 간격**: 16px gap, 수평 중앙 정렬

### 영역 4: 통계 바 (Stats Bar)

**목적**: 수치 데이터의 수평 정렬, 폰트 크기 차이, 색상 검증

- **배경**: #FFFFFF
- **구조**: 4개 통계 항목 수평 배열 (60px gap)
- **항목**:
  - 1,247 / Active Users
  - 358 / Projects
  - 99.9% / Uptime
  - 24/7 / Support
- **숫자**: 32px, 800 weight, #2B6CB0
- **라벨**: 13px, 대문자, #718096
- **하단 테두리**: 1px solid #E2E8F0

### 영역 5: 게시판 + 사이드바 (Board + Sidebar)

**목적**: 테이블 렌더링, 태그 색상, 2단 레이아웃, 리스트, 그리드 검증

#### 메인 게시판 (좌측, flex: 2)
- **헤더**: "Notice Board" + "5 New" 빨간 뱃지, #2D3748 배경
- **테이블 구조**: 5열 (No, Category, Title, Date, Views)
- **5개 행**:
  - #125: Notice (빨강 태그) — System maintenance
  - #124: Event (초록 태그) — Developer conference
  - #123: Update (파랑 태그) — Platform v3.2
  - #122: FAQ (노랑 태그) — Password reset
  - #121: Notice (빨강 태그) — Privacy policy
- **태그 색상**:
  - Notice: #FED7D7 배경, #C53030 텍스트
  - Event: #C6F6D5 배경, #276749 텍스트
  - Update: #BEE3F8 배경, #2A4365 텍스트
  - FAQ: #FEFCBF 배경, #744210 텍스트

#### 사이드바 (우측, flex: 1)
- **카드 1: Recent Updates** — 4개 항목 리스트 (항목명 + 날짜)
- **카드 2: Quick Links** — 2x2 그리드, 4개 링크 (Docs, Support, Reports, Settings)
- **카드 스타일**: 흰 배경, 12px 라운드, 1px 테두리

### 영역 6: 도형 & 라인 테스트 (Shape & Line Test)

**목적**: PPTX에서 도형과 라인이 정확히 렌더링되는지 검증

#### 도형 5종
| 도형 | 크기 | 색상 | 특징 |
|------|------|------|------|
| Rectangle | 100x60px | #2B6CB0 | border-radius: 4px |
| Rounded Rect | 100x60px | #38A169 | border-radius: 16px |
| Circle | 70x70px | #E53E3E | border-radius: 50% |
| Border Only | 100x60px | #FFFFFF + #D69E2E 3px | 배경 없음, 테두리만 |
| Box Shadow | 100x60px | #805AD5 | box-shadow: 4px 4px 12px |

#### 라인(테두리) 4종
| 라인 | 방향 | 색상 | 두께 |
|------|------|------|------|
| Top Border | 상단만 | #E53E3E | 4px |
| Left Border | 좌측만 | #2B6CB0 | 4px |
| Bottom Border | 하단만 | #38A169 | 4px |
| Full Border | 전체 | #D69E2E | 2px, 6px radius |

### 영역 7: 푸터 (Footer)

**목적**: 다단 레이아웃, 링크 리스트, 하단 구분선 검증

- **배경**: #1A202C (매우 어두운 회색)
- **구조**: 4단 그리드 (2fr + 1fr + 1fr + 1fr)
- **컬럼**:
  1. 회사 소개 텍스트 (2fr)
  2. Company 링크 4개
  3. Resources 링크 4개
  4. Legal 링크 4개
- **하단 바**: 저작권 텍스트 + 소셜 링크 3개 (GitHub, Twitter, LinkedIn)
- **구분선**: 1px solid #2D3748
- **제목**: 16px, 700 weight, #FFFFFF
- **본문/링크**: 14px, #A0AEC0

---

## 색상 팔레트 요약

| 용도 | 색상 코드 | 설명 |
|------|----------|------|
| Primary | #2B6CB0 | 메인 파란색 (히어로, 통계, 링크) |
| Dark Nav | #1E3A5F | 헤더 배경 |
| Dark Footer | #1A202C | 푸터 배경 |
| Accent Red | #E53E3E | CTA 버튼, Notice 태그, 원형 도형 |
| Success Green | #38A169 | Event 태그, 둥근 도형, 하단 라인 |
| Warning Gold | #D69E2E | FAQ 태그, 테두리 도형, 전체 라인 |
| Purple | #805AD5 | 센터 마커, 그림자 도형 |
| Text Primary | #1F2937 | 기본 텍스트 |
| Text Secondary | #718096 | 보조 텍스트, 라벨 |
| Background | #F5F5F5 | 페이지 배경 |
| Card BG | #FFFFFF | 카드/테이블 배경 |

---

## 검증 포인트

1. **좌표 정확도**: 5개 코너 마커가 슬라이드의 정확한 위치에 배치되는가
2. **배경색**: 각 영역의 배경색이 정확히 재현되는가 (#1E3A5F, #2B6CB0, #1A202C 등)
3. **텍스트**: 제목, 본문, 라벨, 링크 텍스트가 잘림 없이 표시되는가
4. **테이블**: 5열 5행 테이블의 정렬과 테두리가 정확한가
5. **도형**: 5종 도형의 모양, 색상, 라운드, 그림자가 정확한가
6. **라인**: 4종 부분 테두리가 올바른 방향과 색상으로 표시되는가
7. **레이아웃**: 2단(게시판+사이드바), 4단(푸터) 레이아웃이 유지되는가
8. **폰트 크기**: 42px 타이틀 ~ 11px 라벨까지 크기 차이가 구분되는가
