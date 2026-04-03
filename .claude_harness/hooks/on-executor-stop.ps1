# on-executor-stop.ps1 — SubagentStop Hook (Executor 전용)
# Executor 팀원이 종료될 때 실행
# 산출물 정리 및 Verifier 전달 준비

param(
    [string]$AgentName,
    [string]$ExitReason
)

$LogFile = ".claude/hooks/audit.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

"$timestamp | SubagentStop | $AgentName | 종료 이유: $ExitReason" | Out-File -Append -FilePath $LogFile -Encoding UTF8

Write-Host ""
Write-Host "=== Executor 종료 ==="
Write-Host "에이전트: $AgentName"
Write-Host "종료 이유: $ExitReason"
Write-Host ""

# 산출물 존재 확인
$outputs = @(
    "E-1_implementation.md",
    "E-2_unit_tests.md",
    "E-3_integration_tests.md",
    "E-4_performance_metrics.md"
)

foreach ($output in $outputs) {
    if (Test-Path $output) {
        Write-Host "[OK] $output 존재"
    } else {
        Write-Host "[WARN] $output 미발견"
    }
}

# Metadata 제거 (Verifier에게 전달 준비)
if (Test-Path ".claude/hooks/strip-metadata.py") {
    Write-Host ""
    Write-Host "Metadata 제거 중 (Verifier 전달 준비)..."
    foreach ($output in $outputs) {
        if (Test-Path $output) {
            $cleanName = $output -replace "\.md$", "_clean.md"
            python .claude/hooks/strip-metadata.py $output $cleanName --phase execute
        }
    }
    Write-Host "Metadata 제거 완료."
}

Write-Host ""
Write-Host "→ Verifier에게 전달 준비 완료"

exit 0
