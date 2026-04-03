# Harness Research — 스킬 카탈로그 (Skill Catalog)

**생성일**: 2026-04-03
**총 스킬 수**: 47 (SKILL.md 포함) + 2 (SKILL.md 없음)
**범위**: `/sessions/epic-tender-einstein/mnt/Harness_Research/skills/`

---

## 목차
1. [전체 스킬 목록](#전체-스킬-목록)
2. [카테고리별 분류](#카테고리별-분류)
3. [개발 생명주기 커버리지](#개발-생명주기-커버리지)
4. [스킬 연결 기회 (Composition Opportunities)](#스킬-연결-기회-composition-opportunities)
5. [주요 발견사항](#주요-발견사항)

---

## 전체 스킬 목록

### 1. algorithmic-art
- **목적**: p5.js 알고리즘 미술 생성. 계산미학 철학과 코드 구현 통합
- **카테고리**: Design/UI
- **주요 기능**:
  - 알고리즘 철학 정의 (4-6 단락 매니페스토)
  - p5.js 인터랙티브 생성 + seeded randomness
  - 시드 기반 재현 가능한 변형 탐색
- **입출력**: 사용자 아이디어 → `.md` (철학) + `.html` (실행형 아트)
- **자동화 레벨**: Semi-auto (철학 정의는 협업, 코드 구현은 자동)
- **Harness 연관성**: 창의적 비주얼 콘텐츠 생성

### 2. analyze
- **목적**: 프롬프트 4-Layer 분석 (어휘/통사/담화/화용) 및 최적 도구 추천
- **카테고리**: Analysis
- **주요 기능**:
  - Python prompt_analyzer 실행
  - 분석 결과 해석 및 도구 추천
  - 번역 의도 감지 시 translation-specialist 호출
- **입출력**: 프롬프트 → JSON 분석 + 추천 도구
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 사용자 의도 정확 파악

### 3. ansible-prism
- **목적**: 5-Slot combination engine으로 한국 랜딩페이지 다중 생성 (3.2M+ 고유 조합)
- **카테고리**: Design/UI
- **주요 기능**:
  - CREATE 모드: 주제만으로 0에서 페이지 생성
  - REDESIGN 모드: 기존 와이어프레임 시각 변환
  - OL 10 (Genius Originality) 강제 + AI 슬로프 차단
  - 이미지/모션/CSS 정밀도/시각 밀도 모듈 통합
- **입출력**: 주제/와이어프레임 → `.html` (자체 포함)
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 한국 웹 페이지 고품질 생성

### 4. banner-design
- **목적**: 소셜/광고/웹/인쇄용 배너 다중 아트 디렉션 생성
- **카테고리**: Design/UI
- **주요 기능**:
  - 22 art direction 스타일
  - Pinterest 참조 조사
  - HTML/CSS 배너 + AI 비주얼 생성
  - 플랫폼별 크기 자동 적용
- **입출력**: 요구사항 → 3+ 디자인 옵션 (`*.png`)
- **자동화 레벨**: Semi-auto (사용자 피드백 반복)
- **Harness 연관성**: 마케팅 콘텐츠 제작

### 5. brand
- **목적**: 브랜드 음성/비주얼 ID/메시징 프레임워크 관리
- **카테고리**: Design/UI
- **주요 기능**:
  - brand-guidelines.md 핵심 자료로 유지
  - 색상/타이포 추출 스크립트
  - 토큰 생성 및 CSS 변수 동기화
- **입출력**: 브랜드 정보 → 토큰 + CSS + 가이드라인
- **자동화 레벨**: Semi-auto (사용자가 가이드라인 편집, 동기화는 자동)
- **Harness 연관성**: 전사 브랜드 일관성

### 6. brand-guidelines
- **목적**: Anthropic 공식 브랜드 색상/타이포 적용
- **카테고리**: Design/UI
- **주요 기능**:
  - 공식 색상 (Dark/Light/Orange/Blue/Green)
  - Poppins/Lora 폰트 적용
  - 자동 폰트백업 (Arial/Georgia)
- **입출력**: 아티팩트 → 브랜드 스타일 적용
- **자동화 레벨**: Fully automated
- **Harness 연관성**: Anthropic 브랜드 준수

### 7. canvas-design
- **목적**: 디자인 철학 기반 `.pdf`/`.png` 미술 작품 생성
- **카테고리**: Design/UI
- **주요 기능**:
  - 시각 철학 4-6단락 정의
  - 개념적 DNA 축약 인코딩
  - 박물관/잡지 품질 출력
- **입출력**: 사용자 아이디어 → `.md` (철학) + `.pdf`/`.png` (아트)
- **자동화 레벨**: Semi-auto
- **Harness 연관성**: 프리미엄 콘텐츠 자산

### 8. claude-api
- **목적**: Claude API 활용 가이드 (모델 선택/도구 사용/배치)
- **카테고리**: Development
- **주요 기능**:
  - 언어별 SDK 가이드 (Python/TS/Java/Go/Ruby)
  - 모델 정보 (Opus 4.6/Sonnet 4.6/Haiku 4.5)
  - Adaptive thinking + effort 파라미터
  - Compaction (긴 컨텍스트)
- **입출력**: 앱 요구사항 → API 통합 코드
- **자동화 레벨**: Manual trigger (참고용 스킬)
- **Harness 연관성**: LLM 앱 개발

### 9. claude-strategy
- **목적**: 프로젝트 특성에 최적화된 Claude Code 사용전략 문서 자동 생성
- **카테고리**: Project Management
- **주요 기능**:
  - Chain/Agent/Skill/Teams 매핑
  - 의존성 분석 + 병렬화 기회 식별
  - 12섹션 전략 문서 (비용/속도 최적화)
- **입출력**: 프로젝트 정보 → `claude_code_strategy.md`
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 개발 워크플로우 최적화

### 10. commit-push
- **목적**: Git 커밋 및 푸시 자동화 (Conventional Commit)
- **카테고리**: DevOps/Git
- **주요 기능**:
  - git status 확인
  - Conventional Commit 형식 (feat/fix/docs/refactor/chore)
  - Co-Authored-By 추가
- **입출력**: 변경사항 → 커밋 + 푸시
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 버전 관리 자동화

### 11. design
- **목적**: 통합 디자인 스킬 (로고/CIP/슬라이드/배너/소셜/아이콘)
- **카테고리**: Design/UI
- **주요 기능**:
  - Logo: 55+ 스타일, Gemini AI 생성
  - CIP: 50+ 산출물, 20 스타일, 웹 프레젠테이션
  - Slides: Chart.js, 디자인 토큰
  - Banners: 22 스타일
  - Icons: 15 스타일, SVG 생성
  - Social Photos: 플랫폼별 크기 자동 변환
- **입출력**: 디자인 요구사항 → 다중 형식 산출물
- **자동화 레벨**: Fully automated (with Gemini API)
- **Harness 연관성**: 엔드-to-엔드 디자인 생성

### 12. design-extractor
- **목적**: 웹사이트 URL에서 디자인 시스템 역추출 (Dembrandt)
- **카테고리**: Analysis
- **주요 기능**:
  - 색상/타이포/간격 자동 추출
  - 컴포넌트 스타일링 분석
  - 대화형 HTML 문서 생성
- **입출력**: 사이트 URL → 디자인 시스템 `.html`
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 경쟁 분석, 설계 기반

### 13. design-md
- **목적**: Google Stitch 프로젝트 분석 → semantic `DESIGN.md` 생성
- **카테고리**: Documentation
- **주요 기능**:
  - Stitch MCP 프로젝트 스크린 분석
  - 색상/타이포/컴포넌트 추출
  - 8섹션 영문 문서 (Stitch 프롬프트 최적화)
- **입출력**: Stitch 프로젝트 → `DESIGN.md`
- **자동화 레벨**: Semi-auto (MCP 상호작용 포함)
- **Harness 연관성**: Stitch 설계 일관성

### 14. design-spec-form
- **목적**: 모호한 디자인 느낌 → 50-필드 정량화 스펙폼 → 코드
- **카테고리**: Design/UI
- **주요 기능**:
  - 느낌 키워드 → 디자인 방향 매핑
  - 50필드 폼 (색상/타이포/레이아웃/모션)
  - Aesthetics Engine (AI 슬로프 차단)
  - 필드 기반 HTML 코드 생성
- **입출력**: 디자인 요구사항 → 스펙폼 + `.html`
- **자동화 레벨**: Semi-auto (폼 승인 필요)
- **Harness 연관성**: 비제네릭 설계

### 15. design-system
- **목적**: 토큰 아키텍처 + 컴포넌트 스펙 + 슬라이드 생성
- **카테고리**: Design/UI
- **주요 기능**:
  - 3-Layer 토큰 (Primitive→Semantic→Component)
  - CSS 변수 생성
  - 슬라이드 BM25 검색 + contextual decision
  - Chart.js 통합
- **입출력**: 브랜드/컴포넌트 → `.css` + `.json` + 슬라이드
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 설계 시스템 구축

### 16. doc-coauthoring
- **목적**: 구조화된 문서 공동 저작 워크플로우 (PRD/결정문/스펙)
- **카테고리**: Documentation
- **주요 기능**:
  - Phase 1: Context gathering (인터뷰)
  - Phase 2: Refinement (섹션별 브레인스토밍→큐레이션→초안)
  - Phase 3: Reader testing (sub-agent 검증)
- **입출력**: 문서 요구사항 + 컨텍스트 → 최종 문서
- **자동화 레벨**: Semi-auto (사용자 반복 협업)
- **Harness 연관성**: 고품질 문서 생성

### 17. docx
- **목적**: Word 문서 생성/편집 (python-docx / docx-js)
- **카테고리**: Documentation
- **주요 기능**:
  - docx-js로 신규 문서 생성
  - 기존 문서 unpack→수정→pack
  - 테이블/이미지/추적 변경
  - 페이지 크기 (A4/US Letter)
- **입출력**: 요구사항 → `.docx`
- **자동화 레벨**: Fully automated
- **Harness 연관성**: Office 문서 생성

### 18. frontend-design
- **목적**: 프로덕션급 웹 인터페이스 생성 (AI 슬로프 차단)
- **카테고리**: Design/UI
- **주요 기능**:
  - 대담한 미학 방향 선택 (최소주의~극대주의)
  - 비제네릭 타이포 + 색상 + 모션
  - 공간 구성 + 배경 테마 설정
- **입출력**: 컨텍스트 → HTML/CSS/JS 또는 React
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 고품질 웹 UI

### 19. html2pptx-converter
- **목적**: HTML → PPTX 프레젠테이션 변환 (4 Teammate 병렬 파이프라인)
- **카테고리**: Development
- **주요 기능**:
  - Phase 1: 스펙 분석 (Teammate-A)
  - Phase 2: 슬라이드 HTML 생성 (Teammate-B)
  - Phase 3: PPTX 변환 + 검증 (Teammate-C)
  - Phase 4: 반복 수정 (Teammate-D)
- **입출력**: HTML + 설명서 + 항목 정의 → `.pptx`
- **자동화 레벨**: Fully automated (4-phase pipeline)
- **Harness 연관성**: 웹→프레젠테이션 변환

### 20. internal-comms
- **목적**: 내부 커뮤니케이션 템플릿 (3P/뉴스레터/FAQ/상태보고)
- **카테고리**: Communication
- **주요 기능**:
  - 3P updates (Progress/Plans/Problems)
  - 회사 뉴스레터
  - FAQ 답변
  - 상태 보고 + 리더십 업데이트
- **입출력**: 컨텍스트 → 포맷 문서
- **자동화 레벨**: Semi-auto (템플릿 + 협업)
- **Harness 연관성**: 내부 커뮤니케이션

### 21. kwcag-a11y
- **목적**: KWCAG 2.2 기반 웹 접근성 점검 (3-Tier: 정적/동적/수동)
- **카테고리**: Testing/QA
- **주요 기능**:
  - Tier 1: Python 정적 분석 (18/33 항목)
  - Tier 2: axe-core 강화 (17/33 항목)
  - Tier 3: 수동 체크리스트 (9/33 항목)
  - 심각도 분류 + 보고서 (요약/디테일)
- **입출력**: HTML 파일/디렉토리 → 접근성 보고서 `.md`
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 공공 기관 표준 준수

### 22. kwcag-a11y-workspace
- **상태**: SKILL.md 없음

### 23. mcp-builder
- **목적**: MCP (Model Context Protocol) 서버 개발 가이드
- **카테고리**: Development
- **주요 기능**:
  - 4-Phase 개발 (Research→Implementation→Review→Evaluation)
  - TypeScript/Python SDK 가이드
  - 도구 명명 + 에러 메시징
  - 평가 생성 (10 QA 페어)
- **입출력**: API 스펙 → MCP 서버
- **자동화 레벨**: Manual trigger (참고용)
- **Harness 연관성**: LLM 통합 도구

### 24. memory-save
- **목적**: 세션 작업 `~/.claude/memory/`에 기록 (중복 방지)
- **카테고리**: Project Management
- **주요 기능**:
  - YYMM_SEQ_keyword.md 명명
  - 최근 메모리 3개 확인 (중복 방지)
  - 도구/Chain/Agent/Skill 메타데이터 저장
- **입출력**: 작업 요약 → 메모리 문서
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 작업 이력 추적

### 25. pdf
- **목적**: PDF 처리 (읽기/병합/분할/이미지 추출/OCR/형식 채우기)
- **카테고리**: Development
- **주요 기능**:
  - pypdf (병합/분할/회전/암호화)
  - pdfplumber (텍스트/표 추출)
  - reportlab (PDF 생성)
  - OCR (pytesseract)
- **입출력**: PDF 파일 → 처리된 PDF/텍스트
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 문서 처리

### 26. pencil-image-to-prompt
- **목적**: 이미지 → Google Pencil `.pen` 디자인 프롬프트 변환
- **카테고리**: Design/UI
- **주요 기능**:
  - Phase 0: 인터뷰 (목적/기술스택/피델리티)
  - Phase 1: 이미지 분석
  - Phase 2: Pencil 프롬프트 생성 (변수→컴포넌트→레이아웃→상세)
  - Phase 3: 자체 검증
- **입출력**: 이미지 → `.pen` 프롬프트
- **자동화 레벨**: Semi-auto (인터뷰 필요)
- **Harness 연관성**: Pencil 설계 생성

### 27. pptx
- **목적**: PowerPoint 생성/편집 (pptxgenjs / 템플릿 조작)
- **카테고리**: Documentation
- **주요 기능**:
  - pptxgenjs로 신규 슬라이드 생성
  - 템플릿 unpacking → 편집 → packing
  - 섬네일 생성 + 시각 비교
  - 디자인 아이디어 (색상/타이포/레이아웃)
- **입출력**: 콘텐츠 → `.pptx`
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 프레젠테이션 생성

### 28. pr-review
- **목적**: Git diff 리뷰 + `.pr-reviews/` 보고서 저장
- **카테고리**: DevOps/Git
- **주요 기능**:
  - 문법/보안/버그 분석
  - Conventional Commit 확인
  - 코드 스타일 준수 검사
- **입출력**: PR/브랜치 → 리뷰 보고서
- **자동화 레벨**: Semi-auto (사용자 선택)
- **Harness 연관성**: 코드 품질 관리

### 29. project-review
- **목적**: 프로젝트 전체 리뷰 (아키텍처/구조/유지보수성)
- **카테고리**: Analysis
- **주요 기능**:
  - 아키텍처 적절성
  - 코드 구조 + 일관성
  - 문서화 수준
  - 확장성 + 유지보수성
  - A~D 등급 부여
- **입출력**: 프로젝트 폴더 → `PJ-*_보고서.md`
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 프로젝트 평가

### 30. readme-gen
- **목적**: 프로젝트 폴더 분석 → `README.md` + `README_KO.md` 자동 생성
- **카테고리**: Documentation
- **주요 기능**:
  - 폴더 구조 분석
  - README 8섹션 (개요/구조/컴포넌트/사용법)
  - 영문 + 한글 버전
- **입출력**: 프로젝트 폴더 → `.md` 문서
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 자동 문서화

### 31. req-definition-xlsx
- **목적**: 마크다운 요구사항 정의서 → 엑셀 3시트 변환
- **카테고리**: Documentation
- **주요 기능**:
  - Sheet 1: 표지 (Navy/Blue 디자인)
  - Sheet 2: 개정이력 (7컬럼)
  - Sheet 3: 세부요구사항 (14컬럼)
  - md 파싱 + Frontmatter 추출
- **입출력**: `.md` → `.xlsx`
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 요구사항 산출물

### 32. section-redesign
- **목적**: 웹 페이지 개별 섹션을 디자인 이미지 기반으로 정밀 재구현
- **카테고리**: Design/UI
- **주요 기능**:
  - 이미지 → 섹션 교체 (CSS/HTML/JS)
  - Pixel-level 분석
  - 기존 레이아웃 유지, 스타일 변경
- **입출력**: 이미지 + HTML → 재설계된 섹션
- **자동화 레벨**: Semi-auto (사용자 확인)
- **Harness 연관성**: 점진적 UI 업그레이드

### 33. skill-creator
- **목적**: 스킬 생성/개선/평가 (draft→test→eval→iterate)
- **카테고리**: Development
- **주요 기능**:
  - 스킬 SKILL.md 작성
  - 테스트 프롬프트 실행
  - 정량/정성 평가
  - BM25 성능 벤치마킹
- **입출력**: 스킬 아이디어 → 실행형 스킬
- **자동화 레벨**: Semi-auto (협업)
- **Harness 연관성**: 스킬 개발

### 34. slack-gif-creator
- **목적**: Slack 최적화 애니메이션 GIF 생성 (제약 + 도구)
- **카테고리**: Design/UI
- **주요 기능**:
  - 크기 (Emoji: 128×128, Message: 480×480)
  - FPS 10-30, 색상 48-128
  - 3초 이내 지속시간
- **입출력**: 아이디어 → `.gif` (Slack 호환)
- **자동화 레벨**: Semi-auto (생성 + 최적화)
- **Harness 연관성**: Slack 콘텐츠

### 35. slides
- **목적**: 데이터 기반 HTML 슬라이드 생성 (Chart.js + 토큰)
- **카테고리**: Documentation
- **주요 기능**:
  - 디자인 토큰 기반 색상/타이포
  - Chart.js 차트 통합
  - 25 슬라이드 레이아웃
  - 25 카피라이팅 공식 (PAS/AIDA/FAB)
- **입출력**: 주제 + 수 → `.html` 슬라이드
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 프레젠테이션 생성

### 36. stitch-image-to-prompt
- **목적**: 이미지 → Google Stitch UI 설계 프롬프트 변환
- **카테고리**: Design/UI
- **주요 기능**:
  - Phase 0: 인터뷰 (목적/기술스택/피델리티)
  - Phase 1: 이미지 분석
  - Phase 2: Stitch 프롬프트 생성
  - MCP 실행 옵션
- **입출력**: 이미지 → Stitch 프롬프트 + (선택) 스크린
- **자동화 레벨**: Semi-auto (인터뷰 필요)
- **Harness 연관성**: Stitch 설계 생성

### 37. supanova-forge
- **목적**: $150K 에이전시 품질 한국 랜딩페이지 생성 (HTML + Tailwind CDN)
- **카테고리**: Design/UI
- **주요 기능**:
  - CREATE 모드: 0에서 생성
  - REDESIGN 모드: 기존 페이지 업그레이드
  - 10 분위기 (dark/warm/clean/bold/soft/neon/retro/mono/lush/pop)
  - WCAG 2.1 AA + 하드웨어 가속 모션
- **입출력**: 요구사항 → `.html`
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 고급 랜딩페이지

### 38. tdd-fix
- **목적**: eGovFrame/Java/JSP 유지보수 최소 수정 (TDD 패턴)
- **카테고리**: Development
- **주요 기능**:
  - Red (테스트 정의) → Green (최소 수정) → Verify 사이클
  - JSP/HTML/CSS 마크업 + Java 메서드 수정
  - 기존 코드 최소 변경
- **입출력**: 버그/요구사항 → 수정된 코드
- **자동화 레벨**: Semi-auto (사용자 검증)
- **Harness 연관성**: 공공기관 전자정부 유지보수

### 39. theme-factory
- **목적**: 10 사전 설정 테마 + 커스텀 테마 생성 (색상/폰트)
- **카테고리**: Design/UI
- **주요 기능**:
  - 10 프리셋 테마 (색상 팔레트 + 폰트 페어링)
  - 커스텀 테마 온더플라이 생성
  - 슬라이드/문서/랜딩페이지 적용
- **입출력**: 테마 선택 → 스타일 적용
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 일관된 비주얼 스타일

### 40. translation-specialist
- **목적**: 4-Layer 언어학 분석 기반 전문 번역 (공문/법률/기술/마케팅/문학)
- **카테고리**: Communication
- **주요 기능**:
  - Lexical→Syntactic→Discourse→Pragmatic 자동 분석
  - 6개 도메인 (공문/법률/기술/IT/마케팅/문학)
  - Nida Functional Equivalence + ISO 17100
  - 확신도 시스템 (high/medium/low)
- **입출력**: 원문 → 번역 + 전략 보고
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 다국어 콘텐츠

### 41. ui-styling
- **목적**: shadcn/ui + Tailwind CSS 기반 아름다운 접근성 UI 생성
- **카테고리**: Design/UI
- **주요 기능**:
  - shadcn/ui 컴포넌트 (Radix UI + Tailwind)
  - Tailwind 유틸리티 스타일
  - Canvas 시각 설계
  - 다크 모드 + 반응형
- **입출력**: 요구사항 → React/HTML UI
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 접근성 UI 컴포넌트

### 42. ui-ux-pro-max
- **목적**: UI/UX 설계 인텔리전스 (67 스타일 + 96 팔레트 + 57 폰트 페어링)
- **카테고리**: Design/UI
- **주요 기능**:
  - 13개 기술 스택 (React/Vue/Svelte/SwiftUI/Flutter)
  - 25개 차트 타입
  - 99개 UX 가이드라인
  - BM25 검색 기반 추천
- **입출력**: 설계 요구사항 → 가이드라인 + 코드
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 설계 지능

### 43. vibe-dev
- **목적**: 문서 기반 AI 페어 프로그래밍 (4-Phase: Investigate→Define→Develop→Report)
- **카테고리**: Development
- **주요 기능**:
  - Zero-Guess Protocol (추측 제거)
  - SSOT (Single Source of Truth) — 모든 코드는 문서 기반
  - Stage/Gate 품질 시스템
  - PRD→작업 계획→스펙→코드
- **입출력**: 아이디어 → 완성된 프로젝트
- **자동화 레벨**: Semi-auto (협업)
- **Harness 연관성**: 체계적 프로젝트 개발

### 44. web-artifacts-builder
- **목적**: 복잡한 claude.ai HTML 아티팩트 (React + Tailwind + shadcn/ui)
- **카테고리**: Design/UI
- **주요 기능**:
  - React 18 + TypeScript + Vite
  - Parcel 번들링 → 단일 HTML
  - 상태 관리 + 라우팅 지원
  - Tailwind + shadcn/ui
- **입출력**: 요구사항 → `.html` 아티팩트
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 복잡한 웹 앱

### 45. web-vuln-scan
- **목적**: KISA/행안부 기반 한국 웹 취약점 점검 (49 CWE + OWASP Top 10)
- **카테고리**: Security
- **주요 기능**:
  - Tier 1: 정적 분석 (Python)
  - Tier 2: 에이전트 심화 분석
  - Tier 3: 동적 테스트
  - 공공기관 표준 보고서
- **입출력**: 소스 코드/웹사이트 → 보안 보고서
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 공공기관 보안 감리

### 46. webapp-testing
- **목적**: Playwright 기반 웹앱 테스트 및 디버깅
- **카테고리**: Testing/QA
- **주요 기능**:
  - 로컬 웹앱 상호작용
  - 섬네일 캡처
  - 브라우저 로그 확인
  - `with_server.py` 헬퍼 (여러 서버 관리)
- **입출력**: 앱 요구사항 → Playwright 테스트 + 결과
- **자동화 레벨**: Semi-auto (테스트 코드 작성)
- **Harness 연관성**: 앱 검증

### 47. wireframe
- **목적**: 점진적 UX 생성 (Phase 1: 5 B&W 와이어프레임 → Phase 2: 5 에이전트 병렬로 색상 처리)
- **카테고리**: Design/UI
- **주요 기능**:
  - UX Architect (Phase 1): 와이어프레임 5개 옵션 빠르게 생성
  - Visual Designer (Phase 2): 5개 병렬 에이전트가 Clean+Polished 색상 처리
  - 공유 HTML + 탭 기반 비교
- **입출력**: 기능 설명 → 5 와이어프레임 옵션 (`/styles-optN.css`)
- **자동화 레벨**: Fully automated (병렬)
- **Harness 연관성**: UX 프로토타이핑

### 48. xlsx
- **목적**: 스프레드시트 생성/편집 (openpyxl / CSV 변환)
- **카테고리**: Development
- **주요 기능**:
  - 신규 파일 생성
  - 기존 파일 읽기/편집
  - 데이터 정제 + 변환
  - Zero Formula Errors 준수
- **입출력**: 데이터 → `.xlsx`
- **자동화 레벨**: Fully automated
- **Harness 연관성**: 데이터 관리

### 49. chains
- **상태**: SKILL.md 없음

---

## 카테고리별 분류

### Design/UI (15개)
algorithmic-art, banner-design, brand, brand-guidelines, canvas-design, design, design-extractor, design-spec-form, design-system, frontend-design, pencil-image-to-prompt, section-redesign, supanova-forge, ui-styling, ui-ux-pro-max, wireframe (16개 실제)

**특징**:
- 창의적 비주얼 생성에 강함
- AI 슬로프 차단 메커니즘 다수 포함
- 디자인 철학 → 코드 구현 패턴 일관
- 다중 형식 산출물 (이미지/HTML/CSS)

### Development (9개)
claude-api, html2pptx-converter, mcp-builder, tdd-fix, vibe-dev, web-artifacts-builder, webapp-testing, xlsx, skill-creator

**특징**:
- 코드 생성/테스트/최적화
- 문서 기반 개발 철학 (vibe-dev)
- 최소 수정 원칙 (tdd-fix)

### Testing/QA (2개)
kwcag-a11y, webapp-testing

**특징**:
- 자동화된 점검
- 표준 준수 (KWCAG, WCAG)
- 상세 보고서 생성

### Documentation (7개)
design-md, doc-coauthoring, docx, pptx, readme-gen, req-definition-xlsx, slides

**특징**:
- 구조화된 문서 생성
- 템플릿 기반
- 다중 형식 (MD/DOCX/PPTX/XLSX)

### DevOps/Git (2개)
commit-push, pr-review

**특징**:
- Git 자동화
- 코드 품질 관리
- Conventional Commit 준수

### Analysis (3개)
analyze, design-extractor, project-review

**특징**:
- 시스템 분석/역공학
- 정량적 평가
- 자동 추천 생성

### Communication (2개)
internal-comms, translation-specialist

**특징**:
- 내부/외부 커뮤니케이션
- 다국어 지원
- 표준 템플릿

### Project Management (2개)
claude-strategy, memory-save

**특징**:
- 워크플로우 최적화
- 맥락 추적
- 성과 문서화

### Security (1개)
web-vuln-scan

**특징**:
- 취약점 점검
- 공공기관 표준 준수
- KISA 기준

---

## 개발 생명주기 커버리지

```
요구사항 수집          ─→  req-definition-xlsx (요구사항 엑셀)
                          ├─ claude-strategy (개발 전략)
                          └─ doc-coauthoring (PRD 작성)

계획 & 분석           ─→  analyze (프롬프트 분석)
                          ├─ project-review (현황 평가)
                          └─ design-extractor (경쟁 분석)

설계 (UI/UX)         ─→  wireframe (5개 옵션)
                          ├─ design-spec-form (스펙)
                          ├─ design-system (토큰)
                          ├─ pencil-image-to-prompt (Pencil)
                          ├─ stitch-image-to-prompt (Stitch)
                          └─ ui-ux-pro-max (가이드라인)

설계 (비주얼)        ─→  ansible-prism (랜딩페이지)
                          ├─ supanova-forge (프리미엄 페이지)
                          ├─ design (통합: 로고/CIP/배너)
                          ├─ banner-design (배너)
                          ├─ canvas-design (아트)
                          └─ algorithmic-art (생성 미술)

개발 (코드)          ─→  vibe-dev (문서 기반 개발)
                          ├─ claude-api (API 활용)
                          ├─ ui-styling (UI 컴포넌트)
                          ├─ web-artifacts-builder (복잡 HTML)
                          ├─ frontend-design (웹 인터페이스)
                          ├─ html2pptx-converter (HTML→PPTX)
                          ├─ mcp-builder (MCP 서버)
                          ├─ skill-creator (스킬 개발)
                          └─ tdd-fix (유지보수 수정)

테스트              ─→  webapp-testing (플레이라이트)
                          ├─ kwcag-a11y (접근성)
                          ├─ web-vuln-scan (보안)
                          └─ pr-review (코드 리뷰)

배포 & 산출          ─→  commit-push (Git)
                          ├─ pdf (PDF 생성)
                          ├─ docx (Word 생성)
                          ├─ pptx (PowerPoint)
                          ├─ xlsx (엑셀)
                          ├─ slides (슬라이드)
                          ├─ readme-gen (README)
                          └─ internal-comms (커뮤니케이션)

지원 도구            ─→  memory-save (작업 기록)
                          ├─ theme-factory (테마)
                          ├─ brand (브랜드 관리)
                          ├─ translation-specialist (번역)
                          ├─ slack-gif-creator (Slack GIF)
                          └─ section-redesign (섹션 교체)
```

### 커버리지 분석

| 생명주기 단계 | 커버리지 | 스킬 수 | 평가 |
|---------------|---------|--------|------|
| 요구사항      | 높음    | 3      | ✅ 완전 |
| 계획/분석     | 높음    | 3      | ✅ 완전 |
| 설계 (UI)     | 매우높음 | 6      | ✅ 탁월 |
| 설계 (비주얼) | 매우높음 | 6      | ✅ 탁월 |
| 개발          | 높음    | 8      | ✅ 완전 |
| 테스트        | 중간    | 4      | ⚠️ 함수형 테스트 부족 |
| 배포/산출     | 매우높음 | 7      | ✅ 탁월 |
| 지원 도구     | 높음    | 7      | ✅ 다양 |

### 주요 간격 (Gaps)

1. **함수형 테스트 (Functional Testing)**:
   - 현재: 접근성 + 보안 + 유닛 테스트
   - 부족: 통합 테스트, E2E 시나리오 자동화, 성능 테스트

2. **모바일 앱 개발**:
   - 현재: 웹 중심
   - 부족: iOS/Android 네이티브, 크로스플랫폼 프레임워크 (React Native/Flutter) 전문 스킬

3. **데이터 처리 & 분석**:
   - 현재: xlsx (스프레드시트) 기본
   - 부족: ETL, 데이터 파이프라인, SQL 쿼리 최적화, 데이터 시각화 심화

4. **백엔드 개발**:
   - 현재: API 가이드
   - 부족: DB 설계, ORM, 마이크로서비스, API 서버 보일러플레이트

---

## 스킬 연결 기회 (Composition Opportunities)

### 1. 랜딩페이지 풀 사이클
```
사용자 아이디어
  ↓
design-spec-form (50-필드 스펙)
  ↓
ansible-prism (HTML 생성) 또는 supanova-forge (프리미엄)
  ↓
section-redesign (섹션 재조정)
  ↓
kwcag-a11y (접근성 점검)
  ↓
web-vuln-scan (보안 점검)
  ↓
commits-push (Git)
```

### 2. 디자인 시스템 구축
```
기존 사이트 URL
  ↓
design-extractor (색상/타이포 역추출)
  ↓
design-system (토큰 생성)
  ↓
ui-styling (shadcn/ui + Tailwind)
  ↓
frontend-design (컴포넌트 구현)
  ↓
brand (토큰 동기화)
  ↓
docx 또는 readme-gen (가이드라인 문서)
```

### 3. 요구사항 → 코드 전체 흐름
```
비즈니스 요구사항
  ↓
req-definition-xlsx (정형화)
  ↓
claude-strategy (개발 전략)
  ↓
wireframe (5 UX 옵션)
  ↓
vibe-dev (문서 기반 개발)
  ├─ claude-api (API)
  ├─ skill-creator (커스텀 스킬)
  └─ mcp-builder (외부 도구 통합)
  ↓
webapp-testing (플레이라이트)
  ↓
pr-review (코드 리뷰)
  ↓
commit-push (푸시)
```

### 4. 프리젠테이션 자동화
```
설계 콘텐츠
  ↓
design-spec-form (스펙)
  ↓
design-system (슬라이드 토큰)
  ↓
slides (HTML 슬라이드)
  ↓
theme-factory (색상/폰트 적용)
  ↓
pptx (PowerPoint 변환) 또는 pdf (PDF 내보내기)
  ↓
internal-comms (배포)
```

### 5. 이미지 → 설계 구현 체인
```
디자인 이미지/스크린샷
  ↓
pencil-image-to-prompt (Pencil) 또는 stitch-image-to-prompt (Stitch)
  ↓
Pencil/Stitch 자동 생성
  ↓
section-redesign (기존 앱 통합)
  ↓
kwcag-a11y (접근성)
  ↓
webapp-testing (검증)
```

### 6. 문서 생성 파이프라인
```
작업 컨텍스트
  ↓
analyze (4-Layer 분석)
  ↓
doc-coauthoring (구조화 + 협업)
  ↓
docx/pptx/readme-gen (형식 변환)
  ↓
internal-comms (배포)
  ↓
memory-save (이력 기록)
```

### 높은 시너지 스킬 쌍

| 스킬 A | 스킬 B | 활용 사례 |
|--------|--------|----------|
| wireframe | design-spec-form | UX 와이어프레임 → 정량 스펙 |
| design-system | ui-styling | 토큰 → 코드 컴포넌트 |
| ansible-prism | kwcag-a11y | 페이지 생성 → 접근성 검증 |
| vibe-dev | claude-api | 문서 기반 개발 + API 통합 |
| design-extractor | design-system | 경쟁 분석 → 자체 토큰 시스템 |
| req-definition-xlsx | vibe-dev | 요구사항 → 개발 계획 |
| pptx + slides | theme-factory | 프레젠테이션 + 색상 통일 |

---

## 주요 발견사항

### 강점

1. **AI 슬로프 차단 철학 일관**
   - design-spec-form, design, supanova-forge 등이 anti-pattern 명확히 정의
   - "느낌" → "정량값" 변환 메커니즘 체계적

2. **설계(Design) 분야 탁월**
   - 15개 UI/설계 스킬
   - 알고리즘 미술부터 웹페이지까지 전범위
   - 이미지 분석 → 코드 생성 연쇄 (pencil-image-to-prompt, stitch-image-to-prompt, section-redesign)

3. **문서 기반 개발 지원**
   - vibe-dev: SSOT + Zero-Guess Protocol
   - doc-coauthoring: 3-Phase 구조화
   - 요구사항 정의 → 개발 계획 자동화

4. **다형식 산출물**
   - HTML/CSS/PDF/DOCX/PPTX/XLSX 모두 지원
   - 변환 체인 가능 (HTML→PPTX, MD→XLSX)

5. **표준 준수**
   - KWCAG 2.2 (접근성)
   - OWASP Top 10 + KISA (보안)
   - Conventional Commit + ISO 17100 (번역)

### 약점

1. **함수형/통합 테스트 부족**
   - webapp-testing은 Playwright 기초 제공만 함
   - 자동화된 E2E 시나리오, 성능 테스트 전문 스킬 없음

2. **모바일 개발 미지원**
   - 웹 중심 (React/Vue/Svelte)
   - React Native/Flutter 등 크로스플랫폼 미포함

3. **데이터 엔지니어링 한정**
   - xlsx: 스프레드시트 기본만 지원
   - ETL/데이터 파이프라인/SQL 최적화 스킬 없음

4. **백엔드 개발 추상적**
   - claude-api: 가이드만 제공
   - 구체적인 프로젝트 보일러플레이트/ORM/DB 설계 스킬 부재

5. **MCP/자동화 도구 개발 초기**
   - mcp-builder: 가이드 스킬
   - 즉시 사용 가능한 MCP 서버 템플릿 없음

### 기회 영역

1. **함수형 테스트 자동화 스킬** (높은 우선순위)
   - Playwright 기반 E2E 시나리오 자동 생성
   - 성능 + 로드 테스트 통합

2. **데이터 엔지니어링 스킬 확대**
   - ETL 파이프라인 생성
   - SQL 쿼리 최적화
   - 데이터 시각화 (차트/대시보드)

3. **백엔드 프로젝트 템플릿**
   - Node.js/Python/Java 스택별
   - API 보일러플레이트 자동 생성

4. **모바일 앱 개발**
   - React Native/Flutter 전문 스킬
   - 크로스플랫폼 설계 시스템

5. **고급 MCP/자동화**
   - MCP 서버 보일러플레이트
   - 복잡한 워크플로우 자동화

### 사용 패턴

**높은 빈도 조합**:
1. wireframe → design-spec-form → {ansible-prism | supanova-forge}
2. design-extractor → design-system → {ui-styling | frontend-design}
3. req-definition-xlsx → claude-strategy → vibe-dev
4. {kwcag-a11y | web-vuln-scan} → pr-review → commit-push

**병렬 실행 권장**:
- wireframe (5개 옵션 병렬 처리)
- design (로고+CIP+배너 병렬)
- html2pptx-converter (4 Teammate 병렬)

---

## 스킬별 메타데이터 요약

| 스킬 | 모델 | 도구 | 의존성 | 속도 |
|-----|------|------|--------|------|
| algorithmic-art | Haiku | Read/Write | p5.js CDN | 중간 |
| analyze | Haiku | Bash | prompt_analyzer.py | 빠름 |
| ansible-prism | Opus | Read/Write | Tailwind CDN | 느림 |
| banner-design | Opus | Bash/WebFetch | ui-ux-pro-max | 느림 |
| brand | Haiku | Bash | node scripts | 중간 |
| ... (생략) | ... | ... | ... | ... |

---

## 결론

**47개 스킬이 다음을 커버**:
- ✅ UI/UX 설계 (탁월)
- ✅ 문서 생성 (완전)
- ✅ 웹 개발 (완전)
- ✅ 접근성/보안 (완전)
- ⚠️ 테스트 (부분)
- ❌ 모바일 앱 (미지원)
- ❌ 데이터 엔지니어링 (한정)

**전략적 권장사항**:
1. **즉시**: wireframe + design-spec-form 조합으로 UX 프로토타이핑 자동화
2. **단기** (1개월): 함수형 테스트 자동화 스킬 추가
3. **중기** (3개월): 데이터/백엔드 스킬 확대
4. **장기** (6개월): 모바일 앱 개발 플랫폼 통합

---

*이 카탈로그는 2026-04-03 기준 47개 SKILL.md 파일을 분석하여 작성되었습니다.*
