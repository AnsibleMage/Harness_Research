#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
웹 취약점 Tier 1 정적 코드 분석기
==================================
행안부 47개 소프트웨어 보안약점 기반 정적 분석 도구.

사용법:
    python vuln-static-scan.py <path> [옵션]

옵션:
    --format json|md          출력 형식 (기본: json)
    --severity critical|major|minor|all  최소 심각도 (기본: all)
    --lang auto|python|java|php|js|html  언어 (기본: auto)
    --category all|input|security|time|error|code|encapsulation|api  유형 필터
    --owasp all|A01|...|A10   OWASP 필터

의존성: Python 3 표준 라이브러리만 사용 (외부 패키지 없음)
"""

import argparse
import datetime
import json
import os
import re
import sys
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Vulnerability Pattern Definitions
# ---------------------------------------------------------------------------

VULN_PATTERNS: List[Dict] = [
    # === 1. 입력데이터 검증 및 표현 ===
    {
        "vuln_id": "MOIS-IV-01", "vuln_name": "SQL 인젝션",
        "category": "입력데이터 검증 및 표현", "cwe": "CWE-89",
        "owasp": "A03", "kisa_id": "WV-05", "severity": "critical",
        "patterns": {
            "python": [
                (r'\.execute\s*\(\s*f["\']', "f-string SQL 쿼리"),
                (r'\.execute\s*\(\s*["\'].*?\s*\+\s*', "문자열 연결 SQL"),
                (r'\.execute\s*\(\s*["\'].*?%s.*?%\s*\(', "%-포맷 SQL (tuple 아닌 경우)"),
                (r'\.raw\s*\(\s*["\']SELECT', "Django raw SQL"),
            ],
            "java": [
                (r'Statement.*\.execute\w*\s*\(\s*".*?\+', "Statement 문자열 연결 SQL"),
                (r'createQuery\s*\(\s*".*?\+', "JPQL/HQL 인젝션"),
            ],
            "php": [
                (r'mysql_query\s*\(\s*["\'].*?\.\s*\$', "레거시 mysql 함수 연결 SQL"),
                (r'mysqli_query\s*\(.*?,\s*["\'].*?\.\s*\$', "mysqli 연결 SQL"),
                (r'\$\w+->query\s*\(\s*["\'].*?\.\s*\$', "PDO query 연결 SQL"),
            ],
            "js": [
                (r'\.query\s*\(\s*`.*?\$\{', "템플릿 리터럴 SQL"),
                (r'\.query\s*\(\s*["\'].*?\+', "문자열 연결 SQL"),
            ],
        },
        "fix": "Parameterized Query(바인드 변수)를 사용하세요.",
    },
    {
        "vuln_id": "MOIS-IV-03", "vuln_name": "크로스사이트 스크립팅(XSS)",
        "category": "입력데이터 검증 및 표현", "cwe": "CWE-79",
        "owasp": "A03", "kisa_id": "WV-11", "severity": "major",
        "patterns": {
            "python": [
                (r'return\s+f["\']<', "f-string HTML 직접 반환"),
                (r'\|\s*safe\b', "Django |safe 필터 (자동 이스케이프 우회)"),
                (r'Markup\s*\(', "Flask Markup (이스케이프 우회)"),
            ],
            "java": [
                (r'out\.print\w*\s*\(\s*request\.getParameter', "request 파라미터 직접 출력"),
                (r'\.setAttribute\s*\(.*?,\s*request\.getParameter', "request 파라미터 속성 설정"),
            ],
            "php": [
                (r'echo\s+\$_(GET|POST|REQUEST|COOKIE)', "사용자 입력 직접 echo"),
                (r'print\s+\$_(GET|POST|REQUEST|COOKIE)', "사용자 입력 직접 print"),
            ],
            "js": [
                (r'\.innerHTML\s*=', "innerHTML 직접 할당"),
                (r'document\.write\s*\(', "document.write 사용"),
                (r'\.outerHTML\s*=', "outerHTML 직접 할당"),
                (r'\.insertAdjacentHTML\s*\(', "insertAdjacentHTML 사용"),
            ],
            "html": [
                (r'on\w+\s*=\s*["\']', "인라인 이벤트 핸들러"),
            ],
        },
        "fix": "출력 시 HTML 이스케이프 적용. textContent 사용. CSP 헤더 설정.",
    },
    {
        "vuln_id": "MOIS-IV-04", "vuln_name": "운영체제 명령어 삽입",
        "category": "입력데이터 검증 및 표현", "cwe": "CWE-78",
        "owasp": "A03", "kisa_id": "WV-04", "severity": "critical",
        "patterns": {
            "python": [
                (r'os\.system\s*\(', "os.system 사용"),
                (r'os\.popen\s*\(', "os.popen 사용"),
                (r'subprocess\.\w+\(.*?shell\s*=\s*True', "subprocess shell=True"),
                (r'commands\.\w+\s*\(', "commands 모듈 사용"),
            ],
            "java": [
                (r'Runtime\.getRuntime\(\)\.exec\s*\(\s*".*?\+', "Runtime.exec 문자열 연결"),
                (r'ProcessBuilder\s*\(\s*".*?\+', "ProcessBuilder 문자열 연결"),
            ],
            "php": [
                (r'\bsystem\s*\(\s*\$', "system() 변수 사용"),
                (r'\bexec\s*\(\s*\$', "exec() 변수 사용"),
                (r'\bpassthru\s*\(\s*\$', "passthru() 변수 사용"),
                (r'\bshell_exec\s*\(\s*\$', "shell_exec() 변수 사용"),
                (r'`\s*\$', "백틱 명령 실행"),
            ],
        },
        "fix": "subprocess.run(list, shell=False) 사용. 입력값 화이트리스트 검증.",
    },
    {
        "vuln_id": "MOIS-IV-10", "vuln_name": "크로스사이트 요청 위조(CSRF)",
        "category": "입력데이터 검증 및 표현", "cwe": "CWE-352",
        "owasp": "A01", "kisa_id": "WV-15", "severity": "major",
        "patterns": {
            "python": [
                (r'@csrf_exempt', "CSRF 보호 비활성화 (Django)"),
                (r'WTF_CSRF_ENABLED\s*=\s*False', "Flask CSRF 비활성화"),
            ],
            "java": [
                (r'\.csrf\(\)\.disable\(\)', "Spring CSRF 비활성화"),
            ],
            "php": [
                (r'<form\b[^>]*method\s*=\s*["\']post["\'][^>]*>(?:(?!csrf|token|_token).)*?</form>', "CSRF 토큰 없는 POST 폼"),
            ],
            "html": [
                (r'<form\b[^>]*method\s*=\s*["\']post["\'][^>]*>(?:(?!csrf|token|_token).)*?</form>', "CSRF 토큰 없는 POST 폼"),
            ],
        },
        "fix": "프레임워크 CSRF 보호 기능 활성화. SameSite 쿠키 설정.",
    },
    {
        "vuln_id": "MOIS-IV-02", "vuln_name": "경로 조작 및 자원 삽입",
        "category": "입력데이터 검증 및 표현", "cwe": "CWE-22",
        "owasp": "A01", "kisa_id": "WV-25", "severity": "critical",
        "patterns": {
            "python": [
                (r'open\s*\(.*?\+', "파일 경로 문자열 연결"),
                (r'os\.path\.join\s*\(.*?request', "request 기반 경로 조합"),
            ],
            "java": [
                (r'new\s+File\s*\(\s*.*?\+.*?request', "request 파라미터로 File 경로 생성"),
            ],
            "php": [
                (r'(include|require)(_once)?\s*\(\s*\$', "변수 기반 include/require"),
                (r'file_get_contents\s*\(\s*\$', "변수 기반 file_get_contents"),
                (r'fopen\s*\(\s*\$_(GET|POST|REQUEST)', "사용자 입력으로 fopen"),
            ],
        },
        "fix": "경로 정규화(canonicalize) 후 기본 디렉토리 외부 접근 차단.",
    },

    # === 2. 보안 기능 ===
    {
        "vuln_id": "MOIS-SF-04", "vuln_name": "취약한 암호화 알고리즘 사용",
        "category": "보안 기능", "cwe": "CWE-327",
        "owasp": "A02", "kisa_id": "WV-27", "severity": "major",
        "patterns": {
            "python": [
                (r'hashlib\.md5\s*\(', "MD5 해시 사용"),
                (r'hashlib\.sha1\s*\(', "SHA1 해시 사용"),
                (r'DES\.new\s*\(', "DES 암호화 사용"),
            ],
            "java": [
                (r'MessageDigest\.getInstance\s*\(\s*["\']MD5', "MD5 해시 사용"),
                (r'MessageDigest\.getInstance\s*\(\s*["\']SHA-1', "SHA1 해시 사용"),
                (r'Cipher\.getInstance\s*\(\s*["\']DES', "DES 암호화 사용"),
            ],
            "php": [
                (r'\bmd5\s*\(', "md5() 해시 사용"),
                (r'\bsha1\s*\(', "sha1() 해시 사용"),
            ],
        },
        "fix": "SHA-256 이상, bcrypt/PBKDF2 사용. 국정원 검증 암호 모듈 권장.",
    },
    {
        "vuln_id": "MOIS-SF-05", "vuln_name": "중요정보 평문저장",
        "category": "보안 기능", "cwe": "CWE-312",
        "owasp": "A02", "kisa_id": "WV-27", "severity": "major",
        "patterns": {
            "python": [
                (r'["\']password["\']\s*:\s*["\'][^"\']+["\']', "하드코딩된 password 값"),
                (r'["\']secret["\']\s*:\s*["\'][^"\']+["\']', "하드코딩된 secret 값"),
            ],
            "java": [
                (r'String\s+\w*(password|passwd|secret|apikey)\w*\s*=\s*"[^"]+"', "하드코딩된 비밀정보"),
            ],
            "php": [
                (r'\$\w*(password|passwd|secret|api_key)\w*\s*=\s*["\'][^"\']+["\']', "하드코딩된 비밀정보"),
            ],
            "js": [
                (r'(const|let|var)\s+\w*(password|secret|apiKey|api_key)\w*\s*=\s*["\'][^"\']+["\']', "하드코딩된 비밀정보"),
            ],
        },
        "fix": "환경변수 또는 시크릿 매니저 사용. 코드에 비밀정보 미포함.",
    },
    {
        "vuln_id": "MOIS-SF-07", "vuln_name": "하드코드된 비밀번호",
        "category": "보안 기능", "cwe": "CWE-259",
        "owasp": "A07", "kisa_id": "", "severity": "critical",
        "patterns": {
            "python": [
                (r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']{4,}["\']', "하드코딩 패스워드"),
                (r'(?i)(api_key|apikey|secret_key|access_key)\s*=\s*["\'][^"\']{8,}["\']', "하드코딩 API 키"),
            ],
            "java": [
                (r'(?i)(password|passwd|pwd)\s*=\s*"[^"]{4,}"', "하드코딩 패스워드"),
            ],
            "php": [
                (r'(?i)\$\w*(password|passwd|pwd)\s*=\s*["\'][^"\']{4,}["\']', "하드코딩 패스워드"),
            ],
            "js": [
                (r'(?i)(password|passwd|pwd|apiKey|api_key|secret)\s*[:=]\s*["\'][^"\']{4,}["\']', "하드코딩 비밀정보"),
            ],
        },
        "fix": "환경변수(process.env, os.environ)로 대체.",
    },

    # === 3. 에러 처리 ===
    {
        "vuln_id": "MOIS-EH-01", "vuln_name": "오류 메시지를 통한 정보노출",
        "category": "에러 처리", "cwe": "CWE-209",
        "owasp": "A05", "kisa_id": "WV-09", "severity": "major",
        "patterns": {
            "python": [
                (r'except.*:\s*\n\s*return\s+str\s*\(\s*e\s*\)', "예외 메시지 직접 반환"),
                (r'traceback\.format_exc\s*\(', "traceback 직접 출력"),
                (r'DEBUG\s*=\s*True', "Django DEBUG 모드 활성화"),
            ],
            "java": [
                (r'e\.printStackTrace\s*\(\s*\)', "스택 트레이스 출력"),
                (r'e\.getMessage\s*\(\s*\).*response', "에러 메시지 응답에 포함"),
            ],
            "php": [
                (r'display_errors\s*=\s*(On|1|true)', "display_errors 활성화"),
                (r'error_reporting\s*\(\s*E_ALL\s*\)', "모든 에러 표시"),
            ],
        },
        "fix": "커스텀 에러 페이지 사용. 상세 에러는 서버 로그에만 기록.",
    },
    {
        "vuln_id": "MOIS-EH-03", "vuln_name": "부적절한 예외 처리",
        "category": "에러 처리", "cwe": "CWE-396",
        "owasp": "A05", "kisa_id": "", "severity": "minor",
        "patterns": {
            "python": [
                (r'except\s*:\s*\n\s*(pass|\.\.\.)', "bare except + pass (모든 예외 무시)"),
                (r'except\s+Exception\s*:\s*\n\s*pass', "Exception catch + pass"),
            ],
            "java": [
                (r'catch\s*\(\s*Exception\s+\w+\s*\)\s*\{\s*\}', "빈 catch 블록"),
                (r'catch\s*\(\s*Throwable\s+\w+\s*\)\s*\{\s*\}', "Throwable 빈 catch"),
            ],
            "php": [
                (r'catch\s*\(\s*\\?Exception\s+\$\w+\s*\)\s*\{\s*\}', "빈 catch 블록"),
            ],
        },
        "fix": "구체적 예외 타입별 처리. 최소한 로깅은 수행.",
    },

    # === 4. 코드 오류 ===
    {
        "vuln_id": "MOIS-CE-05", "vuln_name": "신뢰할 수 없는 데이터의 역직렬화",
        "category": "코드 오류", "cwe": "CWE-502",
        "owasp": "A08", "kisa_id": "", "severity": "critical",
        "patterns": {
            "python": [
                (r'pickle\.loads?\s*\(', "pickle 역직렬화"),
                (r'yaml\.load\s*\([^)]*\)(?!.*Loader\s*=\s*yaml\.SafeLoader)', "yaml.load (SafeLoader 미사용)"),
                (r'marshal\.loads?\s*\(', "marshal 역직렬화"),
            ],
            "java": [
                (r'ObjectInputStream.*readObject\s*\(', "Java 역직렬화"),
                (r'XMLDecoder.*readObject\s*\(', "XMLDecoder 역직렬화"),
            ],
            "php": [
                (r'unserialize\s*\(\s*\$', "변수 기반 unserialize"),
            ],
        },
        "fix": "JSON 등 안전한 형식 사용. 역직렬화 시 화이트리스트 클래스 제한.",
    },

    # === 5. 캡슐화 ===
    {
        "vuln_id": "MOIS-EC-02", "vuln_name": "제거되지 않고 남은 디버그 코드",
        "category": "캡슐화", "cwe": "CWE-489",
        "owasp": "A05", "kisa_id": "", "severity": "minor",
        "patterns": {
            "python": [
                (r'print\s*\(\s*["\']debug', "debug print문"),
                (r'pdb\.set_trace\s*\(', "pdb 디버거 호출"),
                (r'breakpoint\s*\(', "breakpoint() 호출"),
                (r'import\s+pdb', "pdb import"),
            ],
            "java": [
                (r'System\.out\.println\s*\(', "System.out.println (운영 코드)"),
                (r'System\.err\.println\s*\(', "System.err.println (운영 코드)"),
            ],
            "php": [
                (r'\bvar_dump\s*\(', "var_dump 호출"),
                (r'\bprint_r\s*\(', "print_r 호출"),
                (r'\bphpinfo\s*\(', "phpinfo() 호출"),
            ],
            "js": [
                (r'console\.log\s*\(', "console.log (운영 코드)"),
                (r'debugger\b', "debugger 문"),
                (r'alert\s*\(', "alert() 호출"),
            ],
        },
        "fix": "운영 배포 전 디버그 코드 제거. 로깅 프레임워크 사용.",
    },

    # === 6. API 오용 ===
    {
        "vuln_id": "MOIS-AM-02", "vuln_name": "취약한 API 사용",
        "category": "API 오용", "cwe": "CWE-676",
        "owasp": "A06", "kisa_id": "", "severity": "major",
        "patterns": {
            "python": [
                (r'eval\s*\(', "eval() 사용"),
                (r'exec\s*\(', "exec() 사용 (동적 코드)"),
                (r'__import__\s*\(', "__import__() 동적 임포트"),
            ],
            "java": [
                (r'Runtime\.getRuntime\(\)\.exec', "Runtime.exec 사용"),
            ],
            "php": [
                (r'\beval\s*\(', "eval() 사용"),
                (r'\bassert\s*\(\s*\$', "assert()에 변수 사용"),
                (r'\bcreate_function\s*\(', "create_function 사용"),
                (r'\bpreg_replace\s*\(\s*["\']/.*/e', "preg_replace /e 수정자"),
            ],
            "js": [
                (r'\beval\s*\(', "eval() 사용"),
                (r'new\s+Function\s*\(', "new Function() 동적 코드"),
                (r'setTimeout\s*\(\s*["\']', "setTimeout 문자열 실행"),
            ],
        },
        "fix": "eval/exec 대신 안전한 대안 사용. 동적 코드 실행 금지.",
    },
]

# Language extension mapping
LANG_EXTENSIONS = {
    ".py": "python",
    ".java": "java",
    ".php": "php",
    ".js": "js",
    ".jsx": "js",
    ".ts": "js",
    ".tsx": "js",
    ".html": "html",
    ".htm": "html",
    ".jsp": "java",
    ".vue": "js",
}

SEVERITY_ORDER = {"critical": 0, "major": 1, "minor": 2, "info": 3}

CATEGORY_MAP = {
    "input": "입력데이터 검증 및 표현",
    "security": "보안 기능",
    "time": "시간 및 상태",
    "error": "에러 처리",
    "code": "코드 오류",
    "encapsulation": "캡슐화",
    "api": "API 오용",
}


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

def detect_language(filepath: str) -> Optional[str]:
    ext = os.path.splitext(filepath)[1].lower()
    return LANG_EXTENSIONS.get(ext)


def scan_file(filepath: str, lang: Optional[str] = None,
              min_severity: str = "all",
              category_filter: str = "all",
              owasp_filter: str = "all") -> List[Dict]:
    """Scan a single file for vulnerability patterns."""
    if lang is None or lang == "auto":
        lang = detect_language(filepath)
    if lang is None:
        return []

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.split("\n")
    except (IOError, OSError):
        return []

    vulnerabilities = []

    for vuln_def in VULN_PATTERNS:
        # Filter by severity
        if min_severity != "all":
            if SEVERITY_ORDER.get(vuln_def["severity"], 99) > SEVERITY_ORDER.get(min_severity, 99):
                continue

        # Filter by category
        if category_filter != "all":
            target_cat = CATEGORY_MAP.get(category_filter, "")
            if target_cat and vuln_def["category"] != target_cat:
                continue

        # Filter by OWASP
        if owasp_filter != "all":
            if not vuln_def["owasp"].startswith(owasp_filter):
                continue

        # Get patterns for this language
        lang_patterns = vuln_def.get("patterns", {}).get(lang, [])

        for pattern_str, description in lang_patterns:
            try:
                regex = re.compile(pattern_str, re.IGNORECASE | re.MULTILINE)
            except re.error:
                continue

            for match in regex.finditer(content):
                start = match.start()
                line_no = content[:start].count("\n") + 1
                line_content = lines[line_no - 1].strip() if line_no <= len(lines) else ""

                # Truncate long lines
                code_snippet = line_content[:120] + ("..." if len(line_content) > 120 else "")

                vulnerabilities.append({
                    "vuln_id": vuln_def["vuln_id"],
                    "vuln_name": vuln_def["vuln_name"],
                    "category": vuln_def["category"],
                    "cwe": vuln_def["cwe"],
                    "owasp": vuln_def["owasp"],
                    "kisa_id": vuln_def.get("kisa_id", ""),
                    "severity": vuln_def["severity"],
                    "file": filepath,
                    "line": line_no,
                    "code_snippet": code_snippet,
                    "message": description,
                    "fix": vuln_def["fix"],
                })

    return vulnerabilities


def scan_directory(dirpath: str, lang: Optional[str] = None, **kwargs) -> List[Dict]:
    """Scan all supported files in a directory."""
    all_vulns = []
    for root, dirs, files in os.walk(dirpath):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if d not in (
            "node_modules", ".git", "__pycache__", ".venv", "venv",
            "vendor", "target", "build", "dist", ".next",
        )]
        for fname in files:
            fpath = os.path.join(root, fname)
            file_lang = lang if lang and lang != "auto" else detect_language(fpath)
            if file_lang:
                vulns = scan_file(fpath, file_lang, **kwargs)
                all_vulns.extend(vulns)
    return all_vulns


def build_summary(vulns: List[Dict]) -> Dict:
    """Build summary statistics from vulnerability list."""
    by_severity = {"critical": 0, "major": 0, "minor": 0, "info": 0}
    by_category = {}
    by_owasp = {}

    for v in vulns:
        sev = v["severity"]
        by_severity[sev] = by_severity.get(sev, 0) + 1

        cat = v["category"]
        by_category[cat] = by_category.get(cat, 0) + 1

        owasp = v["owasp"]
        by_owasp[owasp] = by_owasp.get(owasp, 0) + 1

    return {
        "total_vulnerabilities": len(vulns),
        "by_severity": by_severity,
        "by_category": by_category,
        "by_owasp": by_owasp,
    }


def compute_grade(summary: Dict) -> str:
    """Compute overall grade based on severity counts."""
    crit = summary["by_severity"].get("critical", 0)
    major = summary["by_severity"].get("major", 0)
    if crit >= 3:
        return "F"
    elif crit >= 1:
        return "D"
    elif major >= 3:
        return "C"
    elif major >= 1:
        return "B"
    else:
        return "A"


# ---------------------------------------------------------------------------
# Output Formatters
# ---------------------------------------------------------------------------

def format_json(target: str, vulns: List[Dict], lang: str) -> str:
    summary = build_summary(vulns)
    result = {
        "target": target,
        "timestamp": datetime.datetime.now().isoformat(),
        "tier": 1,
        "language": lang or "auto",
        "grade": compute_grade(summary),
        "summary": summary,
        "vulnerabilities": vulns,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def format_markdown(target: str, vulns: List[Dict], lang: str) -> str:
    summary = build_summary(vulns)
    grade = compute_grade(summary)
    lines = [
        f"# Tier 1 정적 분석 결과",
        f"",
        f"| 항목 | 값 |",
        f"|------|-----|",
        f"| 대상 | `{target}` |",
        f"| 시간 | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} |",
        f"| 언어 | {lang or 'auto'} |",
        f"| 종합 등급 | **{grade}** |",
        f"| 총 취약점 | **{summary['total_vulnerabilities']}건** |",
        f"| Critical | {summary['by_severity'].get('critical', 0)}건 |",
        f"| Major | {summary['by_severity'].get('major', 0)}건 |",
        f"| Minor | {summary['by_severity'].get('minor', 0)}건 |",
        f"",
    ]

    if vulns:
        lines.append("## 상세 결과")
        lines.append("")

        # Sort by severity
        sorted_vulns = sorted(vulns, key=lambda v: SEVERITY_ORDER.get(v["severity"], 99))

        for v in sorted_vulns:
            lines.append(f"### [{v['severity'].upper()}] {v['vuln_id']} {v['vuln_name']} ({v['cwe']})")
            lines.append(f"- **위치**: `{v['file']}:{v['line']}`")
            lines.append(f"- **OWASP**: {v['owasp']}")
            if v.get("kisa_id"):
                lines.append(f"- **KISA**: {v['kisa_id']}")
            lines.append(f"- **코드**: `{v['code_snippet']}`")
            lines.append(f"- **설명**: {v['message']}")
            lines.append(f"- **수정**: {v['fix']}")
            lines.append("")
    else:
        lines.append("> 발견된 취약점이 없습니다.")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="웹 취약점 Tier 1 정적 코드 분석기 (행안부 47개 보안약점 기반)"
    )
    parser.add_argument("path", help="분석 대상 파일 또는 디렉토리")
    parser.add_argument("--format", choices=["json", "md"], default="json", help="출력 형식")
    parser.add_argument("--severity", choices=["critical", "major", "minor", "all"], default="all")
    parser.add_argument("--lang", choices=["auto", "python", "java", "php", "js", "html"], default="auto")
    parser.add_argument("--category", choices=["all", "input", "security", "time", "error", "code", "encapsulation", "api"], default="all")
    parser.add_argument("--owasp", default="all", help="OWASP 필터 (예: A03)")

    args = parser.parse_args()
    target = args.path

    if not os.path.exists(target):
        print(f"Error: '{target}' not found.", file=sys.stderr)
        sys.exit(1)

    scan_kwargs = {
        "min_severity": args.severity,
        "category_filter": args.category,
        "owasp_filter": args.owasp,
    }

    if os.path.isfile(target):
        vulns = scan_file(target, args.lang, **scan_kwargs)
    else:
        vulns = scan_directory(target, args.lang, **scan_kwargs)

    if args.format == "json":
        output = format_json(target, vulns, args.lang)
    else:
        output = format_markdown(target, vulns, args.lang)

    print(output)


if __name__ == "__main__":
    main()
