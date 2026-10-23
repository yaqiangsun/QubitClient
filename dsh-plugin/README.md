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
