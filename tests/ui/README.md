# QubitClient Pipeline UI

实时瀑布流展示 pipeline 任务结果。

## 依赖

```bash
pip install -e ".[ui]"
```

## 启动

**终端 1 — Web 服务：**
```bash
python -m tests.ui.serve
```
浏览器打开 http://localhost:8581/

**终端 2 — 模拟 pipeline 数据写入：**
```bash
python -m tests.ui.demo_pipeline -n 20 -i 2
```

`-n` 数量，`-i` 间隔秒数。数据写入 `tmp/db/result/pipeline/`，
serve 每 2 秒扫描该目录，通过 SSE 推送到浏览器，页面无需刷新自动显示新数据。

## 文件结构

```
tests/ui/
├── __init__.py
├── serve.py          # 启动 FastAPI Web 服务
├── demo_pipeline.py  # 模拟 pipeline 写入 storage
├── test_server.py    # 单元测试
└── README.md
```

## 接口

| 路径 | 说明 |
|------|------|
| `GET /` | 主页面 |
| `GET /api/runs?task_name=&limit=&offset=` | 列出所有记录 |
| `DELETE /api/runs/{id}` | 删除一条记录 |
| `GET /api/stream` | SSE 实时推送新记录 |
| `GET /api/task-names` | 所有任务类型列表 |