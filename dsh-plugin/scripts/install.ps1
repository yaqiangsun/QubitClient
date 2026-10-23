# 把 qubitclient-panel 安装进指定 DSH profile（默认 desktop）。
#
# 等价于在 Web UI「插件」页里安装并勾选组合包，做两件事：
#   1) dsh plugin add "link:<插件目录>"  —— 把包链进 profile 的 node_modules；
#   2) 把包名追加进 profile package.json 的 dsh.profile.bundles —— 让它成为一层补丁。
# 安装后需要重启 DSH 主机进程才会加载（页面 Ctrl+R 只刷新浏览器半）。
#
# 用法（仓库根目录）：
#   pwsh -NoProfile -ExecutionPolicy Bypass -File dsh-plugin/scripts/install.ps1
#   pwsh ... -File dsh-plugin/scripts/install.ps1 -Profile desktop
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

# ---- 定位 dsh 启动器 ------------------------------------------------------
$dshCmd = (Get-Command dsh -ErrorAction SilentlyContinue).Source
if (-not $dshCmd) {
  foreach ($candidate in @(
      'D:\Programs\DeepSeek Harness\resources\runtime\cli\bin\dsh.cmd',
      'C:\Program Files\DeepSeek Harness\resources\runtime\cli\bin\dsh.cmd'
    )) {
    if (Test-Path $candidate) { $dshCmd = $candidate; break }
  }
}
if (-not $dshCmd) { throw '找不到 dsh 命令：请把 DSH 的 runtime\cli\bin 加入 PATH，或用完整路径调用本脚本。' }

# ---- 确保 pnpm 可用（DSH 自带 pnpm，但默认不一定在 PATH 里） --------------
if (-not (Get-Command pnpm -ErrorAction SilentlyContinue)) {
  $node = (Get-Command node -ErrorAction SilentlyContinue).Source
  $bundledPnpm = @(
    'D:\Programs\DeepSeek Harness\resources\runtime\primary-runtime\dependencies\pnpm\bin\pnpm.cjs',
    'C:\Program Files\DeepSeek Harness\resources\runtime\primary-runtime\dependencies\pnpm\bin\pnpm.cjs'
  ) | Where-Object { Test-Path $_ } | Select-Object -First 1
  if ($bundledPnpm -and $node) {
    $shimDir = Join-Path $env:TEMP 'dsh-plugin-bin'
    New-Item -ItemType Directory -Force -Path $shimDir | Out-Null
    Set-Content -Path (Join-Path $shimDir 'pnpm.cmd') -Encoding ascii -Value @"
@echo off
"$node" "$bundledPnpm" %*
"@
    $env:PATH = "$shimDir;$env:PATH"
    Write-Host "已为本次安装临时准备 pnpm shim: $shimDir"
  } else {
    throw '找不到 pnpm，也找不到 DSH 自带的 pnpm：请先安装 pnpm 或 Node.js。'
  }
}

# ---- 备份 profile 清单 ----------------------------------------------------
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

# ---- 1) 安装依赖 ----------------------------------------------------------
Write-Host "`n[1/2] 安装依赖: $pkgName <- $pkgDir"
& $dshCmd plugin --profile $Profile add "link:$pkgDir"
if ($LASTEXITCODE -ne 0) { throw "插件安装失败（exit $LASTEXITCODE），profile 清单未改动。" }

# ---- 2) 选中组合包（写入 dsh.profile.bundles） ----------------------------
Write-Host "`n[2/2] 选中组合包: $pkgName"
$manifest = Get-Content $profilePkgPath -Raw | ConvertFrom-Json
$bundles = @()
if ($manifest.dsh -and $manifest.dsh.profile -and $manifest.dsh.profile.bundles) {
  $bundles = @($manifest.dsh.profile.bundles)
}
if ($bundles -contains $pkgName) {
  Write-Host "  $pkgName 已在 dsh.profile.bundles 中，跳过。"
} else {
  if (-not $manifest.dsh) { $manifest | Add-Member -NotePropertyName dsh -NotePropertyValue ([pscustomobject]@{}) }
  if (-not $manifest.dsh.profile) { $manifest.dsh | Add-Member -NotePropertyName profile -NotePropertyValue ([pscustomobject]@{}) }
  if (-not $manifest.dsh.profile.bundles) { $manifest.dsh.profile | Add-Member -NotePropertyName bundles -NotePropertyValue @() }
  $manifest.dsh.profile.bundles = @($bundles + $pkgName)
  Write-JsonNoBom $profilePkgPath $manifest
  Write-Host "  已追加到 dsh.profile.bundles 末尾（最后一层，优先级最高）。"
}

Write-Host "`n安装完成。下一步：" -ForegroundColor Green
Write-Host "  0) 先启动结果服务（仓库根目录）：qubitclient ui start   # 默认 http://127.0.0.1:8581/"
Write-Host "  1) 重启 DSH（退出后重新打开桌面端；Host 半只有重启才会加载）"
Write-Host "  2) 页面 Ctrl+R 刷新"
Write-Host "  3) 右侧栏 → 新建 tab（罗盘）→「QubitClient 结果」"
Write-Host "  4) 输入框下方应出现「QubitClient 结果」状态徽标"
Write-Host "  5) 让模型执行「调用 qubitclient_results 看看最近的任务」验证 Host 半"
