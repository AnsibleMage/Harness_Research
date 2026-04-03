# check-idle-reason.ps1 — TeammateIdle Hook
# 팀원이 유휴 상태가 되기 직전에 실행
# 종료 코드 0: 유휴 허용 (팀원 종료)
# 종료 코드 2: 유휴 거부 + 피드백 → 팀원 계속 작동

param(
    [string]$TeammateName,
    [string]$Reason,
    [string]$LastTask
)

$LogFile = ".claude/hooks/audit.log"

function Write-AuditLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp | TeammateIdle | $TeammateName | $Message" | Out-File -Append -FilePath $LogFile -Encoding UTF8
}

Write-AuditLog "유휴 감지 - 이유: $Reason, 마지막 작업: $LastTask"

# === 미완료 작업 확인 ===
# 팀원이 유휴 상태인데 아직 할당된 작업이 남아있으면 재활성화

if ($Reason -eq "no_tasks") {
    Write-AuditLog "OK: 모든 작업 완료, 유휴 허용"
    Write-Host "$TeammateName - 모든 작업 완료. 유휴 허용."
    exit 0
}

if ($Reason -eq "blocked") {
    Write-AuditLog "WARN: 종속성 차단으로 유휴. 재확인 필요."
    Write-Host "$TeammateName - 종속성 차단. 리더에게 확인 요청."
    # 리더가 판단할 수 있도록 유휴 허용
    exit 0
}

if ($Reason -eq "error") {
    Write-AuditLog "ERROR: 에러로 유휴. 재시도 요청."
    Write-Host "$TeammateName - 에러 발생. 다시 시도해 주세요."
    exit 2  # 팀원 계속 작동
}

# 기타 경우: 유휴 허용
Write-AuditLog "OK: 유휴 허용 (이유: $Reason)"
exit 0
