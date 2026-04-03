# 바이오코리아 파트너링 시스템 - 메인 대시보드 (영문) 입력 항목 정의

---

0. 사용자 인터페이스 상호작용 요소

항목명: User Interface Elements  
역할 설명: 사용자가 직접 조작할 수 있는 모든 인터페이스 요소들
표시 위치: 화면 전체에 분산 배치
입력 형식: 클릭, 토글, 드롭다운, 팝업 등 다양한 상호작용
필수 여부: ✅ 사용자 경험에 필수적인 요소들
기능 범위: 정보 조회, 설정 변경, 페이지 이동, 데이터 관리

---

1. 프로모션 배너 상호작용 영역

항목명: Promotion Banner Controls
역할 설명: 할인 혜택 공지 배너의 사용자 제어 기능
표시 위치: 화면 최상단 전체 영역
입력 형식: 클릭 이벤트 (배너 영역, 닫기 버튼)
필수 여부: ❌ 선택적 상호작용
배너 메시지: "Special Promotion! Register now and get 20% discount."
제어 옵션:
- 배너 전체 영역 클릭 → 등록/결제 페이지 이동
- 우측 상단 X 버튼 클릭 → 배너 숨김 처리

연결 흐름
- 배너 클릭 시 → 프로모션 상세 페이지 또는 결제 페이지로 이동
- X 버튼 클릭 시 → 배너 display: none 처리, 사용자별 숨김 설정 저장
- 세션 지속 시 → 닫힌 상태 유지

---

2. 네비게이션 메뉴 선택 영역

항목명: Navigation Menu Selection
역할 설명: 주요 기능 페이지 간 이동을 위한 메뉴 시스템
표시 위치: 좌측 사이드바 (고정 폭 256px)
입력 형식: 메뉴 항목 클릭 선택
필수 여부: ✅ 시스템 네비게이션 필수
메뉴 구성 (영문 표시):
- Home: 메인 대시보드 (현재 페이지)
- Profile: 개인 프로필 관리
- Search: 파트너 회사 검색 (현재 활성화)
- Agenda: 미팅 일정 관리
- Messages: 메시지 기능
- Favorites: 관심 회사 목록

시각적 피드백
- 현재 페이지: Search 메뉴가 파란색 배경으로 강조 표시
- 호버 효과: 마우스 오버 시 배경색 변경
- 아이콘과 텍스트 조합: 직관적인 기능 인식

연결 흐름
- Home 클릭 → partnering_main_eng.html로 이동
- Profile 클릭 → 프로필 관리 페이지로 이동
- Search 클릭 → 파트너 검색 페이지로 이동
- 각 메뉴 클릭 시 → 해당 기능 페이지로 라우팅

---

3. 공개 모드 전환 토글

항목명: Visibility Mode Toggle
역할 설명: 개인/회사 정보 공개 범위 설정
표시 위치: 헤더 우측 (시간 표시와 프로필 사진 사이)
입력 형식: 토글 스위치 (상호 배타적 선택)
필수 여부: ✅ 개인정보 공개 설정 필수
토글 옵션:
- Personal: 개인 정보 공개 모드 (현재 활성화)
- Company: 회사 정보 공개 모드 (비활성화)

UI 동작
- 활성 토글: 초록색 배경, 원형 버튼 우측 위치
- 비활성 토글: 회색 배경, 원형 버튼 좌측 위치
- 전환 애니메이션: 부드러운 슬라이드 이동 (1.25rem)

연결 흐름
- Personal 활성화 → 검색 결과에 개인 담당자로 노출
- Company 활성화 → 검색 결과에 회사 대표로 노출
- 모드 전환 시 → 프로필 가시성 및 매칭 우선순위 즉시 변경

---

4. 사용자 프로필 접근 영역

항목명: User Profile Access Area
역할 설명: 개인 정보 및 계정 관리 기능 접근
표시 위치: 헤더 최우측
입력 형식: 아이콘 버튼 클릭
필수 여부: ✅ 계정 관리 필수 기능
구성 요소:
- 시간 표시: "2023-10-27 10:30 (KST)" (읽기 전용)
- 검색 아이콘: 통합 검색 기능 접근
- 알림 아이콘: 읽지 않은 알림 표시 (빨간 점 뱃지)
- 프로필 사진: 사용자 이미지 (클릭 가능)

상호작용 기능
- 검색 아이콘 클릭 → 통합 검색 모달 표시
- 알림 아이콘 클릭 → 알림 목록 드롭다운 표시
- 프로필 사진 클릭 → 프로필 관리 팝업 표시

---

5. 프로필 관리 팝업 메뉴

항목명: Profile Management Popup
역할 설명: 계정 및 프로필 관리 옵션 제공
표시 위치: 프로필 사진 클릭 시 우측 하단 팝업
입력 형식: 메뉴 옵션 선택 (클릭)
필수 여부: ✅ 계정 관리 필수
팝업 정보 표시:
- 프로필 사진: 원형 이미지 (64px)
- 사용자명: "Min-jun Kim" (영문만 표시)
- 이메일: "minjun.kim@biosolutions.com"

메뉴 옵션 (아이콘 + 텍스트):
- Edit Personal Profile: 개인 프로필 편집
- Edit Company Profile: 회사 프로필 편집
- Go to Messages: 메시지 관리
- Log Out: 계정 로그아웃

연결 흐름
- Edit Personal Profile → 개인 프로필 편집 페이지
- Edit Company Profile → 회사 프로필 편집 페이지
- Go to Messages → 메시지 관리 페이지
- Log Out → 로그아웃 처리 후 로그인 페이지
- 외부 클릭 또는 ESC → 팝업 닫기

---

6. 미팅 요청 현황 탭 선택

항목명: Meeting Request Summary Tabs
역할 설명: 미팅 요청 데이터 필터링 및 조회
표시 위치: 메인 콘텐츠 좌측 상단
입력 형식: 탭 버튼 클릭 선택
필수 여부: ✅ 데이터 필터링 필수
탭 구성:
- All: 전체 요청 통계 (기본 선택)
- Incoming: 받은 요청만 표시
- Outgoing: 보낸 요청만 표시

데이터 표시 (탭별):
- All 탭: Pending 5건, Confirmed 2건, Declined/Canceled 3건
- Incoming 탭: Pending 3건, Confirmed 1건, Declined/Canceled 2건
- Outgoing 탭: Pending 2건, Confirmed 1건, Declined/Canceled 1건

시각적 피드백
- 선택된 탭: 파란색 텍스트, 하단 파란색 밑줄
- 비선택 탭: 회색 텍스트, 호버 시 진한 회색

연결 흐름
- 탭 클릭 → 해당 범위 데이터로 필터링 표시
- 통계 숫자 클릭 → 상세 미팅 요청 목록 페이지 이동

---

7. 오늘의 미팅 일정 관리

항목명: Today's Meeting Schedule
역할 설명: 당일 확정 미팅 일정 조회 및 관리
표시 위치: 메인 콘텐츠 좌측 중앙
입력 형식: 미팅 항목 클릭, View All 링크 클릭
필수 여부: ✅ 일정 관리 필수
미팅 목록 표시:
- 11:00 - 11:30: PharmaCorp (Kim Minjun) - Meeting Room 3
- 14:00 - 14:30: Gentech Solutions (Lee Seoyeon) - Meeting Room 7
- 16:30 - 17:00: NextGen Pharma (Park Jihun) - Meeting Room 1

상호작용 요소
- View All 링크: 전체 미팅 일정 페이지 이동
- 각 미팅 항목: 클릭 시 상세 정보 표시
- 화살표 버튼: 미팅별 관리 옵션 메뉴

연결 흐름
- View All → 전체 미팅 캘린더 페이지
- 미팅 항목 클릭 → 미팅 상세 정보 및 준비사항
- 화살표 버튼 → 미팅 수정/취소/메모 옵션

---

8. 중요 일정 정보 조회

항목명: Important Dates Information
역할 설명: 시스템 운영 관련 주요 일정 안내
표시 위치: 메인 콘텐츠 좌측 하단
입력 형식: 일정 항목 클릭 (조회)
필수 여부: ✅ 시스템 일정 인지 필수
일정 정보:
- March 3 (Mon), 2025: "Partnering Center opens"
- March 10 (Mon), 2025: "Meeting Schedule Finalization"

시각적 표현
- 날짜: 파란색 배경 박스로 강조
- 제목: "Important Dates" 파란색 텍스트
- 설명: 각 일정의 의미와 사용자 액션 가이드

연결 흐름
- 일정 클릭 → 해당 이벤트 상세 정보 페이지
- 개인 캘린더 연동 → 중요 일정 추가 가능
- 알림 설정 → 일정 전 사전 알림 수신

---

9. 회사 프로필 관리

항목명: Company Profile Management
역할 설명: 소속 회사 정보 조회 및 편집
표시 위치: 우측 사이드바 최상단
입력 형식: Edit Profile 버튼 클릭
필수 여부: ✅ 회사 정보 관리 필수
표시 정보:
- 회사 아이콘: 집 모양 아이콘
- 회사명: "BioSolutions"
- 업종: "Biotechnology"

관리 기능
- Edit Profile 버튼: 회사 정보 수정 페이지 이동
- 회색 배경 버튼으로 편집 기능 강조

연결 흐름
- Edit Profile → 회사 프로필 편집 페이지
- 회사명 클릭 → 회사 상세 프로필 조회
- Personal/Company 모드에 따른 표시 내용 동적 변경

---

10. 미팅 알림 관리

항목명: Meeting Notifications Management
역할 설명: 미팅 관련 실시간 알림 조회 및 관리
표시 위치: 우측 사이드바 중앙
입력 형식: 알림 항목 클릭
필수 여부: ✅ 미팅 소통 필수
알림 목록:
- "Meeting request from PharmaCorp" (2 hours ago)
- "Meeting accepted with Gentech Solutions" (4 hours ago)

표시 형식
- 상대방 회사명: 굵은 글씨로 강조
- 시간 표시: "2 hours ago" 상대적 시간
- 실시간 업데이트: 새 알림 즉시 반영

연결 흐름
- 알림 클릭 → 해당 미팅 요청 상세 페이지
- 읽은 알림 → 시각적 구분 표시
- 알림 설정 → 수신 범위 및 방식 관리

---

11. 추천 회사 매칭 시스템

항목명: Recommended Companies Matching
역할 설명: AI 기반 파트너 회사 추천 및 미팅 요청
표시 위치: 우측 사이드바 하단
입력 형식: Request Meeting 버튼 클릭, 회사명 클릭
필수 여부: ✅ 파트너 매칭 핵심 기능
추천 목록:
- NextGen Pharma - Interest: AI Drug Development
- MediFuture - Interest: Digital Therapeutics  
- CellBioTech - Interest: Cell Therapy

상호작용 기능
- Request Meeting 버튼: 파란색 버튼으로 즉시 미팅 요청
- 회사명 클릭: 상세 프로필 조회
- Interest 클릭: 관련 분야 회사 검색

연결 흐름
- Request Meeting → 미팅 요청 폼 모달 표시
- 회사명 → 해당 회사 상세 프로필 페이지
- Interest → 관련 분야 회사 검색 결과
- AI 학습 → 사용자 활동 기반 추천 정확도 향상

---

12. 고객 지원 연락처 접근

항목명: Customer Support Contact Access
역할 설명: 분야별 고객 지원 연락처 제공
표시 위치: 우측 사이드바 최하단
입력 형식: 이메일 주소 클릭
필수 여부: ✅ 고객 지원 필수
지원 분야:
- Partnering (미팅, 기술 이슈): bizforum@biokorea.org
- Registration (일반 문의): registration@biokorea.org
- Sponsor for Private Meeting Booth:
  • sponsor@biokorea.org
  • bizforum@biokorea.org

상호작용 기능
- 이메일 주소 클릭 → 기본 메일 클라이언트 실행
- 클릭 가능한 링크 스타일: 파란색 텍스트, 호버 시 밑줄

연결 흐름
- 이메일 클릭 → 기본 메일 앱에서 새 메일 작성
- 지원 분야별 → 적절한 담당 부서 자동 연결
- 긴급 지원 → 실시간 고객 서비스 접근

---

13. 실시간 시간 정보 시스템

항목명: Real-time Clock Information
역할 설명: 한국 시간 기준 실시간 시간 표시
표시 위치: 헤더 우측 (토글 스위치 좌측), DOM ID: "korea-time"
입력 형식: 읽기 전용 정보 표시 (textContent 업데이트)
필수 여부: ✅ 시간 동기화 필수
표시 형식: "YYYY-MM-DD HH:MM (KST)" (예: "2023-10-27 10:30 (KST)")
업데이트 주기: 60초(60000ms)마다 자동 갱신

기능 특성
- JavaScript Intl.DateTimeFormat API 기반 실시간 업데이트
- 옵션 설정: year, month, day, hour, minute (numeric/2-digit)
- sv-SE 로케일 사용으로 YYYY-MM-DD 형식 보장
- hour12: false 설정으로 24시간 형식 적용
- Asia/Seoul 타임존 고정 적용
- formatToParts() 메서드로 개별 시간 요소 추출 및 조합

구현 세부사항
- updateTime() 함수: 시간 업데이트 로직
- setInterval(updateTime, 60000): 1분 간격 자동 실행
- 페이지 로드 시 즉시 초기화: updateTime() 직접 호출
- 성능 최적화: 분 단위 업데이트로 불필요한 DOM 조작 방지

연결 흐름
- 페이지 로드 → updateTime() 즉시 실행 → 현재 한국 시간 표시
- 1분 간격 → setInterval 콜백 → DOM textContent 업데이트
- 미팅 일정 → 시간 기준 통일성 보장
- 백그라운드 탭 → 지속적인 시간 업데이트 유지

---

14. 팝업 및 모달 제어 시스템

항목명: Popup and Modal Control System
역할 설명: 사용자 인터페이스 팝업/모달 관리
표시 위치: 화면 전체에 오버레이
입력 형식: 키보드 및 마우스 이벤트
필수 여부: ✅ UI/UX 핵심 기능
제어 방식:
- 외부 클릭: 팝업 자동 닫기
- ESC 키: 키보드로 팝업 닫기
- 명시적 닫기 버튼: X 버튼 클릭

적용 대상
- 프로필 관리 팝업
- 미팅 요청 모달
- 검색 결과 모달
- 알림 드롭다운

연결 흐름
- 팝업 표시 → z-index 50으로 최상위 표시
- 외부 클릭 감지 → 자동 닫기 처리
- ESC 키 감지 → 즉시 팝업 닫기
- 사용자 편의성 → 직관적인 팝업 제어

---

15. 데이터 동기화 및 상태 관리

항목명: Data Synchronization and State Management
역할 설명: 실시간 데이터 업데이트 및 상태 유지
표시 위치: 화면 전체 시스템
입력 형식: 자동 백그라운드 처리
필수 여부: ✅ 시스템 동작 필수
관리 대상:
- 미팅 요청 카운트 실시간 업데이트
- 알림 상태 동기화
- 프로필 정보 즉시 반영
- 공개 모드 설정 저장

처리 방식
- 실시간 데이터 폴링
- 웹소켓 기반 푸시 알림
- 로컬 스토리지 상태 저장
- 세션 기반 사용자 설정 유지

연결 흐름
- 데이터 변경 → 즉시 UI 반영
- 사용자 설정 → 브라우저 저장소에 유지
- 실시간 알림 → 백그라운드 업데이트
- 세션 관리 → 로그인 상태 유지

---

16. JavaScript 이벤트 관리 시스템

항목명: JavaScript Event Management System
역할 설명: 사용자 인터랙션 및 동적 UI 제어
표시 위치: 전체 페이지 JavaScript 영역
입력 형식: 이벤트 리스너 기반 처리
필수 여부: ✅ 인터랙티브 UI 필수

**프로필 팝업 이벤트 핸들링**
- DOM 요소 ID: "profile-avatar-btn", "profile-popup"
- 이벤트 유형: click, keydown
- 초기화: DOMContentLoaded 이벤트 후 실행
- 클릭 처리: stopPropagation() + classList.toggle('hidden')
- 외부 클릭: document 레벨 이벤트로 자동 닫기 감지
- 키보드 지원: ESC 키(e.key === 'Escape') 감지

**탭 전환 시스템**
- 함수명: showTab(tabName)
- 대상 탭: 'all-tab', 'incoming-tab', 'outgoing-tab'
- 초기화 과정: 모든 탭 hidden 클래스 추가
- 스타일 리셋: querySelectorAll('[onclick^="showTab"]')로 버튼 선택
- 활성화: 선택된 탭만 hidden 제거, 버튼 스타일 업데이트
- 상태 클래스: 'text-primary-600', 'border-b-2', 'border-primary-600'

**CSS 토글 애니메이션**
- 선택자: input[type="checkbox"]:checked + label .toggle-circle
- 변환: transform translateX(-1.25rem)
- 전환: transition 속성으로 부드러운 애니메이션
- 상태 관리: :checked 가상 클래스 기반

구현 특징
- 메모리 효율성: 이벤트 위임 패턴 사용
- 성능 최적화: 필요한 경우에만 DOM 조작
- 접근성: 키보드 네비게이션 지원
- 브라우저 호환성: 표준 Web API 활용

연결 흐름
- 사용자 액션 → 이벤트 발생 → 핸들러 실행 → DOM 업데이트
- 상태 변경 → 시각적 피드백 → 사용자 인식
- 키보드 입력 → 접근성 지원 → 대체 조작 방법 제공
- 이벤트 버블링 → 적절한 제어 → 의도하지 않은 동작 방지

---