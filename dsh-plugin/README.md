# QubitClient 结果面板（DSH 插件）

把 QubitClient 的结果页（`qubitclient ui start`，默认 `http://127.0.0.1:8581/`）嵌进 DeepSeek Harness（DSH）的右侧栏，
并给模型一个读取 pipeline 运行记录的工具。QubitClient 本体无需改动。

## 使用前：启动结果页

```bash
pip install -e ".[ui]"          # 首次
qubitclient ui start            # 仓库根目录执行，默认 http://localhost:8581/
```

## 安装

```powershell
# 仓库根目录
powershell -NoProfile -ExecutionPolicy Bypass -File dsh-plugin/scripts/install.ps1
```

装完**重启 DSH**（Host 半只有重启才加载）。之后：

1. 右侧栏「新建 tab」（罗盘）→「QubitClient 结果」；
2. 输入框下方出现「QubitClient 结果 · 已连接 …」徽标，点「打开面板」可直接打开；
3. 让模型执行「调用 `qubitclient_results`，只看 s21peakmulti 最近 3 条」。

面板里就是原样的结果页：卡片瀑布流、SSE 实时新增、点卡片看参数与图。

## 从 GitHub 安装（不发布 npm）

本插件是纯 JS，没有构建产物与 `prepare` 脚本，因此不需要 pnpm 的 `allowBuilds` 授权。

```powershell
# 精确到 commit，装的就是校验过的那份代码（推荐）
dsh plugin --profile desktop add "git+https://github.com/yaqiangsun/QubitClient.git#<commit-sha>&path:/dsh-plugin/qubitclient-panel"

# 也可以跟分支（内容会随推送变化）
dsh plugin --profile desktop add "git+https://github.com/yaqiangsun/QubitClient.git#main&path:/dsh-plugin/qubitclient-panel"
```

同样的 spec 也可以粘贴到 DSH「插件 → 已安装 → 安装」里。装完重启 DSH。

## 让插件被市场收录

DSH **没有官方插件市场，也没有仓库爬虫**：发现页只列用户自己添加的索引源。所以"被索引到"= 你发布一份索引 JSON，别人把它的 URL 加进来。

本仓库自带一份符合 format 1 的索引：

```
https://raw.githubusercontent.com/yaqiangsun/QubitClient/main/dsh-plugin/market-index.json
```

别人的操作路径：插件页 →「实验性插件」旁「更多」→ 启用**自定义插件市场** → 「发现」→ 添加索引源 → 粘贴上面的 URL → 安装。

索引由脚本生成，固定到当前 git commit（内容不会随推送漂移）：

```powershell
node dsh-plugin/scripts/make-market-index.mjs
# 可选：--repo https://github.com/<you>/<repo>
```

每次发版/推送后重跑一次并提交 `market-index.json` 即可。索引里的 `source` 是
`git+https://…/QubitClient.git#<commit>&path:/dsh-plugin/qubitclient-panel`，与上面的安装命令一致。

想进一步提高命中率（可选，按投入排序）：

| 动作 | 效果 |
|---|---|
| 仓库 About 写清楚「DSH plugin: QubitClient results panel」，加 topics `dsh-plugin` `deepseek-harness` | 第三方 hub / GitHub 搜索能命中；topic 是社区约定，DSH 自身不爬 |
| 发布到 npm（`npm publish --access public`）并把索引 `source` 改成 `{"type":"npm"}` | 用户可 `dsh plugin add @qubitclient/dsh-panel@0.1.0`，不依赖 git 与 commit 固定 |
| 把索引托管在 GitHub Pages / 自己的域名 | 索引 URL 更稳定，也方便以后放多个插件（一份索引可列多个） |
| 把插件拆成独立仓库 | 仓库根就是插件，`dsh plugin add github:you/repo` 更直观；当前 monorepo 必须带 `path:` |


## 卸载

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File dsh-plugin/scripts/uninstall.ps1
```

重启 DSH 后生效。安装/卸载脚本都会先备份 profile 的 `package.json`。

## 常见问题

| 现象 | 处理 |
|---|---|
| 面板显示「结果页服务未连接」 | 先 `qubitclient ui start`；直接在面板里改地址再点「保存并重试」也可以 |
| 换了端口 | 改 `qubitclient-panel/cordis.patch.yml` 的 `config.baseUrl`（模型工具用），再在面板离线提示里改一次地址（面板用），然后重启 DSH |
| 面板里看不到今天的运行 | 服务进程的 cwd 要在仓库根（读取侧固定按 `cwd/tmp/db/result` 取数），且 `--storage-root` 目前只影响 SSE 监听目录 |
| 想直接打开某次运行 | 结果页暂无 `?run=` 深链，只能在面板里点卡片 |
| 面板不跟随明暗主题 | 有意为之：保持结果页自己的样式 |
| 复查配置是否装对 | `node dsh-plugin/scripts/check-plugin.mjs` |
