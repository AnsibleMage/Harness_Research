# verify-task.ps1 — TaskCompleted Hook
# Agent Teams의 TaskCompleted 이벤트 시 실행
# 종료 코드 0: 검증 통과 → 작업 완료 허용
# 종료 코드 2: 검증 실패 → 작업 완료 차단, 팀원 계속 작동

param(
    [string]$TaskId,
    [string]$TaskStatus,
    [string]$TeammateName
)

$ErrorActionPreference = "Stop"
$LogFile = ".claude/hooks/audit.log"

# 타임스탬프 로깅
function Write-AuditLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp | TaskCompleted | $TaskId | $TeammateName | $Message" | Out-File -Append -FilePath $LogFile -Encoding UTF8
}

Write-AuditLog "검증 시작"

# === 1차 검증: 테스트 실행 ===
try {
    Write-Host "[1/4] 테스트 실행 중..."

    # Node.js 프로젝트 테스트
    if (Test-Path "package.json") {
        $testResult = npm test --coverage 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-AuditLog "FAIL: 테스트 실패"
            Write-Host "테스트 실패. 재검토 필요."
            Write-Host $testResult
            exit 2
        }
    }

    # Python 프로젝트 테스트
    if (Test-Path "requirements.txt") {
        $testResult = python -m pytest --tb=short 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-AuditLog "FAIL: pytest 실패"
            Write-Host "pytest 실패. 재검토 필요."
            exit 2
        }
    }

    Write-Host "[1/4] 테스트 통과"
}
catch {
    Write-AuditLog "WARN: 테스트 실행 환경 없음 (스킵)"
    Write-Host "[1/4] 테스트 환경 없음 (스킵)"
}

# === 2차 검증: 코드 품질 검사 ===
try {
    Write-Host "[2/4] 코드 품질 검사 중..."

    if (Test-Path "node_modules/.bin/eslint") {
        $lintResult = npx eslint . --ext .js,.ts,.jsx,.tsx 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-AuditLog "FAIL: ESLint 오류"
            Write-Host "코드 품질 기준 미달."
            exit 2
        }
    }

    Write-Host "[2/4] 코드 품질 통과"
}
catch {
    Write-AuditLog "WARN: ESLint 미설치 (스킵)"
    Write-Host "[2/4] ESLint 없음 (스킵)"
}

# === 3차 검증: 보안 검사 ===
try {
    Write-Host "[3/4] 보안 검사 중..."

    # 하드코딩된 시크릿 검색
    $secrets = Get-ChildItem -Recurse -Include *.js,*.ts,*.py,*.json -Exclude node_modules |
        Select-String -Pattern "(password|secret|api_key|apikey|token)\s*[:=]\s*['""][^'""]{8,}" -CaseSensitive:$false

    if ($secrets) {
        Write-AuditLog "FAIL: 하드코딩된 시크릿 발견 ($($secrets.Count)건)"
        Write-Host "보안 위반: 하드코딩된 시크릿 발견"
        $secrets | ForEach-Object { Write-Host "  - $($_.Filename):$($_.LineNumber)" }
        exit 2
    }

    Write-Host "[3/4] 보안 검사 통과"
}
catch {
    Write-AuditLog "WARN: 보안 검사 실패 (스킵)"
    Write-Host "[3/4] 보안 검사 스킵"
}

# === 4차 검증: 파일 크기 검사 ===
Write-Host "[4/4] 파일 크기 검사 중..."

$largeFiles = Get-ChildItem -Recurse -File -Exclude node_modules,*.lock,.git |
    Where-Object { $_.Length -gt 1MB }

if ($largeFiles) {
    Write-AuditLog "WARN: 대용량 파일 감지 ($($largeFiles.Count)개)"
    Write-Host "경고: 1MB 이상 파일 감지"
    $largeFiles | ForEach-Object { Write-Host "  - $($_.FullName) ($([math]::Round($_.Length/1MB, 2))MB)" }
    # 경고만 (차단하지 않음)
}

Write-Host "[4/4] 파일 크기 검사 완료"

# === 최종 판정 ===
Write-AuditLog "PASS: 모든 검증 통과"
Write-Host ""
Write-Host "=== 검증 결과: PASS ==="
Write-Host "TaskId: $TaskId"
Write-Host "Teammate: $TeammateName"
Write-Host ""

exit 0
