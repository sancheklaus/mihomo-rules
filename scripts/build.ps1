$Mihomo = "C:\mihomo\mihomo.exe"

$SourceDir = ".\sources"
$RuleDir = ".\ruleset"

if (!(Test-Path $Mihomo)) {
    Write-Error "Mihomo not found: $Mihomo"
    exit 1
}

Get-ChildItem $SourceDir -Filter *.txt | ForEach-Object {

    $name = $_.BaseName
    $source = $_.FullName
    $target = Join-Path $RuleDir "$name.mrs"

    Write-Host "Building $name.mrs..."

    & $Mihomo convert-ruleset domain text $source $target

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed: $name"
        exit 1
    }
}

Write-Host "All rulesets built successfully."