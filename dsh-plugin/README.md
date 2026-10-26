# QubitClient 结果面板（DSH 插件）

把 QubitClient 的结果页（`qubitclient ui start`，默认 `http://127.0.0.1:8581/`）嵌进 DeepSeek Harness 右侧栏 tab，
并给模型一个读取 pipeline 运行记录的工具 `qubitclient_results`。QubitClient 本体无需改动。

## 1. 启动结果页

```bash
pip install -e ".[ui]"    # 首次
qubitclient ui start      # 仓库根目录执行
```

## 2. 安装

```powershell
dsh plugin add qubitclient-dsh-panel
```

或在 DSH「插件 → 发现」里搜索安装。装完**重启 DSH**（Host 半只有重启才加载），页面再 Ctrl+R。

装好后：

1. 右侧栏「新建 tab」（罗盘）→「QubitClient 结果」
2. 输入框下方出现「QubitClient 结果 · 已连接 …」徽标，点「打开面板」
3. 让模型执行「调用 `qubitclient_results`，只看 s21peakmulti 最近 3 条」

## 3. 自检

```powershell
node dsh-plugin/scripts/check-plugin.mjs      # 子包
node dsh-plugin/scripts/check-plugin.mjs .    # 根目录清单
```

## 4. 卸载

```powershell
dsh plugin remove qubitclient-dsh-panel
```

再从 profile 的 `dsh.profile.bundles` 里删掉 `qubitclient-dsh-panel`（或在 DSH「插件」页取消勾选）；同样要重启 DSH 才生效。

## 常见问题

| 现象 | 处理 |
|---|---|
| 面板显示「结果页服务未连接」 | 先 `qubitclient ui start`；也可在面板里改地址后「保存并重试」 |
| 换了端口 | 改 `qubitclient-panel/cordis.patch.yml` 的 `config.baseUrl`，面板里再改一次地址，重启 DSH |
| 面板里看不到今天的运行 | 服务进程 cwd 要在仓库根（读取侧按 `cwd/tmp/db/result` 取数） |
| 装了但重启没出现 | `dsh.profile.bundles` 里缺 `qubitclient-dsh-panel` |
| 面板不跟随明暗主题 | 有意为之：保持结果页自己的样式 |

