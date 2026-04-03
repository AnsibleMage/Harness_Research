# Design System Extractor

웹사이트 URL에서 디자인 시스템을 통째로 추출하여 브라우저에서 볼 수 있는 HTML 문서로 만들어줍니다.

## 기능

웹사이트 URL을 입력하면, 해당 사이트의 디자인 시스템을 역분석하여 하나의 HTML 파일로 정리합니다:

- **색상** — 핵심 팔레트, CSS 변수, hover/focus 상태별 색상 (신뢰도 포함)
- **타이포그래피** — 폰트 패밀리, 크기 체계, 굵기, 행간
- **간격** — 자주 사용되는 spacing 값과 사용 빈도
- **테두리 & 라운드** — 보더 스타일과 border-radius 패턴
- **그림자** — box-shadow 정의
- **컴포넌트** — 버튼 (hover 인터랙션 포함), 링크
- **CSS 변수 내보내기** — 바로 복사해서 쓸 수 있는 `:root` 블록

출력 HTML에는 다크 모드 토글과 클릭 복사 기능이 포함됩니다.

## 사전 요구사항

| 프로그램 | 버전 | 확인 방법 | 설치 방법 |
|---------|------|----------|----------|
| Node.js | v18 이상 | `node --version` | `brew install node` (macOS) |
| npm | (Node.js에 포함) | `npm --version` | Node.js 설치 시 자동 포함 |
| Dembrandt | 최신 | `npx dembrandt --version` | `npm i -g dembrandt` |

> Claude Code가 스킬 실행 시 누락된 의존성을 자동으로 확인하고 설치합니다.

## 사용법

Claude Code에서 호출:

```
/design-extractor
```

또는 자연어로 요청:

```
"이 사이트의 디자인 시스템 추출해줘: https://example.com"
"https://example.com 디자인 토큰 분석해줘"
```

### 출력 파일

```
{사이트명}_design-system.html
```

브라우저에서 열면 전체 디자인 시스템을 확인할 수 있습니다.

## 동작 원리

```
URL ─→ Dembrandt (헤드리스 브라우저)
       ├─ DOM 순회 + getComputedStyle 수집
       ├─ Hover/Focus 상태 시뮬레이션
       └─ 구조화된 JSON 출력
                │
                ▼
       Claude Code (템플릿 엔진)
       ├─ JSON 파싱 + 필터링
       ├─ HTML 템플릿에 데이터 매핑
       └─ 단일 HTML 파일 출력
```

## 엔진

[Dembrandt](https://www.npmjs.com/package/dembrandt) — 헤드리스 브라우저 기반 디자인 토큰 추출 도구. 웹사이트를 크롤링하여 색상, 타이포그래피, 간격, 그림자, 테두리, 컴포넌트 스타일을 구조화된 JSON으로 추출합니다.

## 제작자

**An (Ansible)** — [github.com/AnsibleMage](https://github.com/AnsibleMage)

## 라이센스

MIT License

Copyright (c) 2026 An (Ansible)

본 소프트웨어의 복제본을 취득하는 모든 사람에게 무상으로 소프트웨어를
제한 없이 사용, 복제, 수정, 병합, 출판, 배포, 서브라이센스, 판매할 수 있는
권리를 부여합니다. 단, 위 저작권 표시와 본 허가 표시를 소프트웨어의 모든
복제본 또는 주요 부분에 포함해야 합니다.

본 소프트웨어는 "있는 그대로" 제공되며, 어떠한 종류의 보증도 하지 않습니다.
