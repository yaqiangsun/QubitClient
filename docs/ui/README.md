# Pipeline Result Web UI

实时瀑布流展示 pipeline 任务结果，支持 SSE 实时推送。

## 安装依赖

```bash
pip install -e ".[ui]"
```

依赖：`fastapi`、`uvicorn`、`python-multipart`

## 启动 Web 服务

```bash
qubitclient ui start
# 或者指定端口
qubitclient ui start --port 9000
# 开发模式热重载
qubitclient ui start --reload
```

然后浏览器打开 http://localhost:8000/

## 模拟 Pipeline 数据

另开一个终端：

```bash
python -m tests.ui.demo_pipeline
# 自定义数量和间隔
python -m tests.ui.demo_pipeline -n 50 -i 1.0
```

数据写入 `tmp/db/result/pipeline/` 目录，serve 每 2 秒扫描该目录，通过 SSE 实时推送到浏览器，无需刷新页面即可看到新数据。

## 命令行接口

| 命令 | 说明 |
|------|------|
| `qubitclient ui start` | 启动 Web 服务 |
| `qubitclient ui start --port 9000` | 指定端口 |
| `qubitclient ui start --reload` | 热重载模式 |

## API 接口

| 路径 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 主页面 |
| `/api/runs` | GET | 列出所有记录，支持 `?task_name=&limit=&offset=` |
| `/api/runs/{id}` | DELETE | 删除一条记录 |
| `/api/stream` | GET | SSE 实时推送新记录 |
| `/api/task-names` | GET | 所有任务类型列表 |

## 数据存储

默认路径：`tmp/db/result/pipeline/{run_id}.json`

记录结构：
```json
{
  "id": "uuid",
  "task_name": "t1",
  "task_type": "t1_pipeline",
  "qubits": ["q1lu7"],
  "params": { ... },
  "raw_data": null,
  "analysis_result": { "T1": 50000.0 },
  "plot_paths": ["tmp/demo_plots/xxx.png"],
  "status": "completed",
  "error": null,
  "created_at": "2026-06-10T...",
  "completed_at": "2026-06-10T..."
}
```

## 与真实 Pipeline 集成

在 pipeline 文件中写入结果时，使用 `PipelineResultStore` 保存记录即可自动出现在 UI 中：

```python
from qubitclient.storage.result_store import PipelineResultRecord, PipelineResultStore
from qubitclient.storage.storage import StorageBackend
from datetime import datetime

store = PipelineResultStore(backend=StorageBackend.LOCAL)

record = PipelineResultRecord(
    task_name="t1",
    task_type="t1_pipeline",
    qubits=["q3lu7"],
    params={"delay_start": 0, "delay_end": 80000},
    status="running",
    created_at=datetime.now(),
)
run_id = store.save_run(record)

# ... 执行测量和分析 ...

store.update_run(run_id,
    status="completed",
    analysis_result={"T1": 50000.0},
    completed_at=datetime.now(),
)
```

新记录写入后，UI 会在 2 秒内自动显示。