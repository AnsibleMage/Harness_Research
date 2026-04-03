# pre-tool-use.ps1 — PreToolUse Hook
# 도구 호출 직전 실행 — 위험한 작업 사전 차단
# 종료 코드 0: 허용
# 종료 코드 2: 차단 + 피드백

param(
    [string]$Tool,
    [string]$Args,
    [string]$AgentName
)

$LogFile = ".claude/hooks/audit.log"

function Write-AuditLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp | PreToolUse | $AgentName | $Tool | $Message" | Out-File -Append -FilePath $LogFile -Encoding UTF8
}

# === 위험 명령 차단 ===

# 1. rm -rf 패턴 감지
if ($Tool -eq "bash" -and $Args -match "rm\s+(-rf|-r\s+-f|-f\s+-r)") {
    Write-AuditLog "BLOCKED: rm -rf 감지"
    Write-Host "차단: 재귀 삭제 명령은 수동 승인이 필요합니다."
    exit 2
}

# 2. 시스템 디렉토리 접근 차단
if ($Args -match "(\/etc\/|\/usr\/|C:\\Windows|C:\\Program Files)") {
    Write-AuditLog "BLOCKED: 시스템 디렉토리 접근"
    Write-Host "차단: 시스템 디렉토리 접근은 허용되지 않습니다."
    exit 2
}

# 3. 패키지 전역 설치 차단 (보안)
if ($Tool -eq "bash" -and $Args -match "npm install -g|pip install(?!.*--break-system)") {
    Write-AuditLog "BLOCKED: 전역 패키지 설치"
    Write-Host "차단: 전역 패키지 설치는 수동 승인이 필요합니다."
    exit 2
}

# 4. git force push 차단
if ($Tool -eq "bash" -and $Args -match "git push.*--force|git push.*-f") {
    Write-AuditLog "BLOCKED: force push"
    Write-Host "차단: force push는 수동 승인이 필요합니다."
    exit 2
}

# 5. 민감 파일 수정 차단
if ($Tool -eq "file_edit" -and $Args -match "\.(env|pem|key|crt|credentials)$") {
    Write-AuditLog "BLOCKED: 민감 파일 수정 시도"
    Write-Host "차단: 민감 파일(.env, .pem 등) 수정은 수동 승인이 필요합니다."
    exit 2
}

# === 로깅 (허용된 작업) ===
Write-AuditLog "ALLOWED: $Tool $Args"

exit 0
