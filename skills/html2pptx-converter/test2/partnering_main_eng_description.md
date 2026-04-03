# 바이오코리아 파트너링 시스템 - 메인 대시보드 (영문) 페이지 기능 설명

---

1. 전체 화면 구성

화면 레이아웃
- 상단: 프로모션 배너 (닫기 가능)
- 좌측: 네비게이션 메뉴 (고정)
- 중앙: 메인 대시보드 영역 (8컬럼)
- 우측: 사용자 정보 위젯 모음 (4컬럼)
- 헤더: 시간 표시, 공개 모드 전환, 사용자 프로필

---

1-1. 프로모션 배너
위치: 화면 최상단 전체 영역

기능 설명
- 목적: 할인 혜택 및 중요 공지사항 노출
- 메시지: "Special Promotion! Register now and get 20% discount." (영문 표시)
- 배경: 프로모션 이미지와 반투명 오버레이 적용
- 닫기 기능: 우측 상단 X 버튼으로 배너 숨김 처리
- 시각적 강조: 노란색 "20% discount" 텍스트로 할인 혜택 부각

연결 흐름
- 배너 영역 클릭 → 등록/결제 페이지로 이동
- X 버튼 클릭 → 배너 숨김 처리 (사용자별 설정 저장)
- 세션 유지 시 닫힌 상태 기억

---

1-2. 브랜드 로고 및 네비게이션
위치: 화면 좌측 사이드바 (고정 폭 256px)

기능 설명
- BioKorea 브랜드 로고: 깃발 아이콘과 "BioKorea" 텍스트 조합
- 메뉴 구성 (영문 표시):
  • Home (현재 페이지 - 파란색으로 강조 표시)
  • Profile (개인 프로필 관리)
  • Search (파트너 회사 검색 - 현재 활성화)
  • Agenda (미팅 일정 관리)
  • Messages (메시지 기능)
  • Favorites (관심 회사 목록)
- 현재 페이지 표시: Search 메뉴가 파란색 배경으로 강조

연결 흐름
- 각 메뉴 클릭 → 해당 기능 페이지로 이동
- Home 메뉴 클릭 → partnering_main_eng.html (현재 페이지)
- Profile 메뉴 클릭 → 프로필 관리 페이지
- 활성 메뉴는 시각적 피드백으로 사용자 위치 인식 지원

---

1-3. 개인/회사 공개 모드 전환
위치: 헤더 우측 (시간 표시 옆)

기능 설명
- Personal 토글: 개인 정보 공개 (현재 활성화)
- Company 토글: 회사 정보 공개
- 토글 스위치: 현재 활성화된 모드를 초록색으로 표시

연결 흐름
- Personal 선택 → 시스템내 다른 사용자에게 내 정보 공개, 검색결과에 나오며, 컴퍼니, 개인 페이지등에서 회사 담당자로 나옴
- Company 선택 → 시스템내 다른 사용자에게 내 회사 정보 공개
- 전환 시 → 정보의 공개 비공개 설정

---

1-4. 사용자 정보 영역
위치: 헤더 최우측

기능 설명
- 현재 시간: 한국 시간(KST) 실시간 표시, JavaScript로 1분마다 자동 갱신
- 검색 아이콘: 원형 버튼(40px), 검색 SVG 아이콘으로 빠른 검색 기능 접근
- 알림 아이콘: 원형 버튼(40px), 읽지 않은 알림 개수 빨간 점(8px) 뱃지로 표시
- 프로필 사진: 원형 이미지(80px), 호버 시 primary 색상 링 효과 적용

연결 흐름
- 프로필 사진 클릭 → 프로필 관리 팝업 표시 (우측 하단, z-index: 50)
  • Edit Personal Profile (사용자 아이콘)
  • Edit Company Profile (건물 아이콘)  
  • Go to Messages (채팅 아이콘)
  • Log Out (로그아웃 아이콘)
- 알림 아이콘 클릭 → 알림 목록 드롭다운 표시
- 검색 아이콘 클릭 → 통합 검색 모달 표시
- 외부 클릭 또는 ESC 키로 모든 팝업 자동 닫기

---

1-5. 프로필 관리 팝업 카드
위치: 프로필 사진 클릭 시 우측 하단에 표시 (absolute positioning)

기능 설명
- 팝업 카드 스타일: 
  • 크기: 320px 폭, 백색 배경, 둥근 모서리(rounded-lg)
  • 그림자: shadow-lg, 테두리: border-gray-200
  • 최상위 레이어: z-index 50으로 다른 요소들 위에 표시
- 사용자 정보 표시:
  • 프로필 사진 (원형, 64px, 중앙 정렬)
  • 이름: "Min-jun Kim" (lg 크기, 굵은 글씨, 영문만 표시)
  • 이메일: minjun.kim@biosolutions.com (sm 크기, 회색 텍스트)
- 메뉴 옵션 (전체 폭 버튼, 좌측 정렬, 아이콘과 텍스트 조합):
  • Edit Personal Profile (사용자 아이콘, 20px)
  • Edit Company Profile (건물 아이콘, 20px)
  • Go to Messages (채팅 아이콘, 20px)
  • Log Out (로그아웃 아이콘, 20px) - 상단 구분선 포함

상호작용 효과
- 각 메뉴 항목: 호버 시 회색 배경(hover:bg-gray-50) 적용
- 전환 효과: transition-colors로 부드러운 색상 변화
- 키보드 지원: Tab 키로 포커스 이동, Enter 키로 선택

연결 흐름
- Edit Personal Profile → partnering_profile_edit.html 개인 프로필 편집 페이지
- Edit Company Profile → partnering_company_edit.html 회사 프로필 편집 페이지
- Go to Messages → partnering_messages_list_eng.html 메시지 관리 페이지
- Log Out → 세션 종료 후 로그인 페이지로 리다이렉트
- 팝업 닫기: 외부 클릭, ESC 키, 또는 메뉴 선택 시 자동 닫기

---

1-6. 미팅 요청 현황 대시보드
위치: 메인 콘텐츠 좌측 상단

기능 설명
- 섹션 제목: "Requests Summary" (영문 표시)
- 탭 구성:
  • All: 전체 미팅 요청 통계 (기본 활성화)
  • Incoming: 받은 미팅 요청만 표시
  • Outgoing: 보낸 미팅 요청만 표시
- 상태별 통계 (All 탭 기준):
  • Pending Requests: 5건 (대기 중)
  • Confirmed: 2건 (확정)
  • Declined / Canceled: 3건 (거절/취소)

연결 흐름
- 탭 클릭 → 해당 범위의 데이터로 필터링 표시
- Incoming 탭: 3건 대기, 1건 확정, 2건 거절/취소
- Outgoing 탭: 2건 대기, 1건 확정, 1건 거절/취소
- 각 숫자 클릭 → 상세 미팅 요청 관리 페이지로 이동

---

1-7. 오늘의 미팅 일정
위치: 메인 콘텐츠 좌측 중앙

기능 설명
- 섹션 제목: "Today's Meetings" (영문 표시)
- View All 링크: 전체 미팅 일정 보기
- 당일 미팅 목록 (확정된 미팅만 표시):
  • 11:00 - 11:30: PharmaCorp (Kim Minjun) - Meeting Room 3
  • 14:00 - 14:30: Gentech Solutions (Lee Seoyeon) - Meeting Room 7  
  • 16:30 - 17:00: NextGen Pharma (Park Jihun) - Meeting Room 1
- 각 미팅 항목에 화살표 버튼으로 추가 옵션 접근

연결 흐름
- View All 클릭 → 전체 미팅 캘린더/일정 관리 페이지로 이동
- 각 미팅 항목 클릭 → 미팅 상세 정보 및 준비사항 표시
- 화살표 버튼 → 미팅 수정/취소/메모 등 관리 옵션
- 시간대별 자동 정렬 표시

---

1-8. 중요 일정 공지
위치: 메인 콘텐츠 좌측 하단

기능 설명
- 섹션 제목: "Important Dates" (파란색으로 강조)
- 시스템 운영 관련 주요 일정:
  • March 3 (Mon), 2025: "Partnering Center opens" - 미팅 요청 및 응답 시작
  • March 10 (Mon), 2025: "Meeting Schedule Finalization" - 모든 미팅 일정 확정 및 참가자 알림 발송
- 날짜 표시: 파란색 배경 박스로 시각적 강조
- 상세 설명: 각 일정의 의미와 사용자 액션 가이드 제공

연결 흐름
- 각 일정 항목 클릭 → 해당 이벤트 상세 정보 및 준비사항 안내
- 개인 캘린더 연동 기능으로 일정 추가 가능
- 중요 일정 알림 설정 가능

---

1-9. 내 회사 프로필 카드
위치: 우측 사이드바 최상단

기능 설명
- 섹션 제목: "My Company Profile" (영문 표시)
- 회사 정보 표시:
  • 회사 아이콘: 집 모양 아이콘 (회사를 상징)
  • 회사명: "BioSolutions"
  • 업종: "Biotechnology"
- Edit Profile 버튼: 회사 정보 수정 기능 (회색 배경)

연결 흐름
- Edit Profile 버튼 클릭 → 회사 프로필 편집 페이지로 이동
- 회사명 클릭 → 회사 상세 프로필 보기
- Personal/Company 모드 전환에 따라 표시 내용 동적 변경
- 회사 정보 완성도에 따른 프로필 강화 가이드 제공

---

1-10. 미팅 알림 위젯
위치: 우측 사이드바 중앙

기능 설명
- 섹션 제목: "Meeting Notifications" (영문 표시)
- 최근 알림 목록 (시간순 정렬):
  • "Meeting request from PharmaCorp" (2 hours ago)
  • "Meeting accepted with Gentech Solutions" (4 hours ago)
- 알림 형태: 회사명을 굵은 글씨로 강조
- 상대적 시간 표시: "2 hours ago", "4 hours ago" 형식

연결 흐름
- 각 알림 클릭 → 해당 미팅 요청 상세 페이지로 이동
- 실시간 알림 업데이트 (새로운 요청 시 즉시 반영)
- 읽지 않은 알림은 시각적으로 구분 표시
- 알림 설정 관리 기능 접근

---

1-11. 추천 회사 위젯
위치: 우측 사이드바 하단

기능 설명
- 섹션 제목: "Recommended Companies" (영문 표시)
- AI 기반 추천 시스템: 사용자 프로필, 관심 분야, 활동 기록을 바탕으로 매칭
- 추천 회사 목록:
  • NextGen Pharma - Interest: AI Drug Development
  • MediFuture - Interest: Digital Therapeutics
  • CellBioTech - Interest: Cell Therapy
- Request Meeting 버튼: 각 회사별 즉시 미팅 요청 (파란색 버튼)

연결 흐름
- Request Meeting 버튼 클릭 → 미팅 요청 폼 모달 표시
- 회사명 클릭 → 해당 회사 상세 프로필 페이지로 이동
- Interest 정보 클릭 → 관련 분야 회사들 검색 결과 표시
- 추천 알고리즘은 사용자 활동과 피드백에 따라 지속 학습

---

1-12. 고객 지원 연락처
위치: 우측 사이드바 최하단

기능 설명
- 섹션 제목: "Contact for Help" (영문 표시)
- 지원 분야별 연락처:
  • Partnering (미팅, 기술 이슈): bizforum@biokorea.org
  • Registration (일반 문의): registration@biokorea.org
  • Sponsor for Private Meeting Booth (프라이빗 미팅룸 후원):
    - sponsor@biokorea.org
    - bizforum@biokorea.org
- 각 이메일 주소는 클릭 가능한 링크로 처리

연결 흐름
- 이메일 주소 클릭 → 기본 메일 클라이언트에서 새 메일 작성
- 각 지원 분야에 따른 적절한 담당 부서 연결
- 긴급 상황 시 빠른 지원 요청 가능

---

1-13. 시간 업데이트 시스템
위치: 헤더 시간 표시 영역 (id="korea-time")

기능 설명
- 실시간 시간 업데이트: setInterval을 사용해 60초(60000ms)마다 자동 갱신
- 한국 시간 기준: Intl.DateTimeFormat과 Asia/Seoul 타임존 적용
- 표시 형식: "YYYY-MM-DD HH:MM (KST)" (24시간 형식)
- JavaScript 구현:
  • formatToParts() 메서드로 년월일시분 개별 추출
  • sv-SE 로케일 사용으로 YYYY-MM-DD 형식 보장
  • hour12: false 설정으로 24시간 형식 적용

기술적 세부사항
- updateTime() 함수: DOM 요소 직접 업데이트
- 초기화: 페이지 로드 즉시 실행 후 타이머 시작
- 성능 최적화: 초 단위 업데이트 없이 분 단위만 갱신
- 브라우저 호환성: 모든 모던 브라우저에서 Intl API 지원

연결 흐름
- 페이지 로드 시 → updateTime() 즉시 실행으로 현재 한국 시간 표시
- 1분마다 → setInterval(updateTime, 60000)로 자동 갱신
- 사용자의 로컬 시간대와 관계없이 한국 시간 고정 표시
- 미팅 일정과의 시간 동기화 기준 제공
- 탭 백그라운드 상태에서도 지속적인 업데이트 유지

---

1-14. JavaScript 상호작용 시스템
위치: 전체 페이지에 적용되는 동적 기능들

기능 설명

**프로필 팝업 제어 시스템**
- 이벤트 리스너: DOMContentLoaded 이후 초기화
- 아바타 버튼 클릭: stopPropagation()으로 이벤트 버블링 방지
- 팝업 토글: classList.toggle('hidden')으로 표시/숨김 제어
- 외부 클릭 감지: document 레벨 클릭 이벤트로 자동 닫기
- 키보드 지원: ESC 키 감지로 팝업 닫기 (keydown 이벤트)

**미팅 요청 탭 전환 시스템**
- showTab(tabName) 함수: 탭별 컨텐츠 동적 표시
- 탭 숨김: 모든 탭 컨텐츠에 'hidden' 클래스 추가
- 스타일 초기화: 모든 버튼에서 활성 상태 클래스 제거
- 선택된 탭 표시: 해당 탭 컨텐츠 'hidden' 클래스 제거
- 버튼 상태 업데이트: 활성 버튼에 primary 색상 클래스 적용

**토글 스위치 CSS 애니메이션**
- CSS 기반 토글 원형 이동: transform translateX(-1.25rem)
- :checked 가상 선택자로 상태별 스타일 적용
- transition 속성으로 부드러운 애니메이션 효과

기술적 구현
- 이벤트 위임: 효율적인 이벤트 관리
- DOM 조작 최적화: 클래스 기반 상태 변경
- 메모리 누수 방지: 적절한 이벤트 리스너 관리
- 크로스 브라우저 호환성: 표준 Web API 사용

연결 흐름
- 사용자 액션 → 이벤트 발생 → 상태 변경 → UI 업데이트
- 팝업 표시 → z-index 우선순위 적용 → 포커스 관리
- 탭 전환 → 컨텐츠 필터링 → 시각적 피드백 제공
- 키보드 인터랙션 → 접근성 지원 → 사용자 편의성 향상

---