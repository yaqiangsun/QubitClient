# 从指定 DSH profile 卸载 qubitclient-panel。
# 卸载后同样需要重启 DSH 主机进程才会生效。
#
# 用法（仓库根目录）：
#   pwsh -NoProfile -ExecutionPolicy Bypass -File dsh-plugin/scripts/uninstall.ps1
param(
  [string]$Profile = 'desktop'
)

$ErrorActionPreference = 'Stop'

$pkgDir = (Resolve-Path (Join-Path $PSScriptRoot '..\qubitclient-panel')).Path
$pkgJson = Get-Content (Join-Path $pkgDir 'package.json') -Raw | ConvertFrom-Json
$pkgName = $pkgJson.name

$dshHome = if ($env:DSH_HOME) { $env:DSH_HOME } else { Join-Path $env:USERPROFILE '.dsh' }
$profileDir = Join-Path $dshHome "profiles\$Profile"
if (-not (Test-Path $profileDir)) { throw "找不到 profile 目录: $profileDir" }

$dshCmd = (Get-Command dsh -ErrorAction SilentlyContinue).Source
if (-not $dshCmd) {
  foreach ($candidate in @(
      'D:\Programs\DeepSeek Harness\resources\runtime\cli\bin\dsh.cmd',
      'C:\Program Files\DeepSeek Harness\resources\runtime\cli\bin\dsh.cmd'
    )) {
    if (Test-Path $candidate) { $dshCmd = $candidate; break }
  }
}
if (-not $dshCmd) { throw '找不到 dsh 命令。' }

$profilePkgPath = Join-Path $profileDir 'package.json'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
Copy-Item $profilePkgPath "$profilePkgPath.bak-$stamp"
Write-Host "已备份 profile 清单 -> $profilePkgPath.bak-$stamp"

# 写回 profile package.json 时不带 BOM（带 BOM 会让 Node 的 JSON.parse 报错）。
function Write-JsonNoBom([string]$Path, $Object) {
  $json = $Object | ConvertTo-Json -Depth 20
  $utf8 = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($Path, $json, $utf8)
}

# ---- 1) 从 dsh.profile.bundles 移除 --------------------------------------
$manifest = Get-Content $profilePkgPath -Raw | ConvertFrom-Json
$bundles = @()
if ($manifest.dsh -and $manifest.dsh.profile -and $manifest.dsh.profile.bundles) {
  $bundles = @($manifest.dsh.profile.bundles)
}
if ($bundles -contains $pkgName) {
  $manifest.dsh.profile.bundles = @($bundles | Where-Object { $_ -ne $pkgName })
  Write-JsonNoBom $profilePkgPath $manifest
  Write-Host "已从 dsh.profile.bundles 移除 $pkgName"
} else {
  Write-Host "$pkgName 不在 dsh.profile.bundles 中，跳过。"
}

# ---- 2) 移除依赖 ----------------------------------------------------------
Write-Host "`n移除依赖: $pkgName"
& $dshCmd plugin --profile $Profile remove $pkgName
if ($LASTEXITCODE -ne 0) { Write-Warning "dsh plugin remove 返回 exit $LASTEXITCODE（可能本来就没装）。" }

Write-Host "`n卸载完成，重启 DSH 后生效。" -ForegroundColor Green
