# post-tool-use.ps1 — PostToolUse Hook
# 도구 호출 직후 실행 — 결과 검증 및 감사 로깅
# 종료 코드 0: 통과
# 종료 코드 2: 재검토 요청

param(
    [string]$Tool,
    [string]$Args,
    [string]$Result,
    [int]$ExitCode,
    [string]$AgentName
)

$LogFile = ".claude/hooks/audit.log"

function Write-AuditLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp | PostToolUse | $AgentName | $Tool | $Message" | Out-File -Append -FilePath $LogFile -Encoding UTF8
}

# === 파일 수정 감사 ===
if ($Tool -eq "file_edit" -or $Tool -eq "file_create") {
    Write-AuditLog "FILE_CHANGE: $Args"

    # 파일 크기 이상 증가 감지
    if (Test-Path $Args) {
        $fileSize = (Get-Item $Args).Length
        if ($fileSize -gt 1MB) {
            Write-AuditLog "WARN: 파일 크기 1MB 초과 ($Args)"
            Write-Host "경고: $Args 파일 크기가 1MB를 초과합니다."
            # 경고만, 차단하지 않음
        }
    }
}

# === bash 명령 실패 감지 ===
if ($Tool -eq "bash" -and $ExitCode -ne 0) {
    Write-AuditLog "COMMAND_FAILED: $Args (exit $ExitCode)"
    Write-Host "경고: 명령 실패 (exit code: $ExitCode)"
    Write-Host "명령: $Args"
    # 실패 로깅만, 차단 안 함
}

# === 결과에 민감 정보 노출 검사 ===
if ($Result -match "(password|secret|api_key|token)\s*[:=]\s*\S{8,}") {
    Write-AuditLog "SECURITY_WARN: 결과에 민감 정보 가능성"
    Write-Host "보안 경고: 결과에 민감 정보가 포함되어 있을 수 있습니다."
}

# === 정상 로깅 ===
Write-AuditLog "OK: $Tool completed (exit $ExitCode)"

exit 0
