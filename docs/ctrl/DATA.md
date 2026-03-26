# Ctrl.DATA 任务接口文档

## 概述

Ctrl.DATA 是 Ctrl 中的一个任务，用于根据运行 ID (rid) 获取已存储的测量数据。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.DATA` |
| rid | int | 是 | 运行 ID，用于指定要获取的测量数据 |

### 调用示例

```python
# 获取指定 run ID 的测量数据
result = client.run(
    task_type=CtrlTaskName.DATA,
    rid=80
)

print(result)
```

## 返回值格式

返回的结果包含指定 run ID 对应的测量数据：

```json
{
  "data": {
    "_ts_": [timestamp1, timestamp2, ...],
    "iq_avg": [[complex, complex], ...]
  },
  "meta": {
    "tid": 7435645518527205376,
    "name": "raw:/s21",
    "user": "xxxxx",
    "priority": 0,
    "system": "xxxxx.json",
    "status": "Finished",
    "other": {
      "shots": 1024,
      "signal": "iq_avg",
      "qubits": ["Q0", "Q1"],
      "qubits_read": ["Q0", "Q1"],
      "waveform_length": 0.000098,
      "shape": [101]
    },
    "axis": {
      "freq": [frequency_array]
    }
  },
  "error": "",
  "committed": "commit_hash",
  "created": "2026-03-26 14:52:20.234058",
  "finished": "2026-03-26 14:52:57.133482"
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 测量原始数据 |
| _ts_ | List[int] | 时间戳数组（纳秒级） |
| iq_avg | List[List[complex]] | IQ 平均数据，二维复数数组 |
| meta | dict | 元数据信息 |
| tid | int | 任务 ID |
| name | str | 任务名称（如 "raw:/s21"） |
| user | str | 用户名 |
| status | str | 任务状态（如 "Finished"） |
| other | dict | 其他参数 |
| shots | int | 采样次数 |
| signal | str | 信号类型（如 "iq_avg"） |
| qubits | List[str] | 量子比特列表 |
| axis | dict | 扫描轴信息 |
| freq | ndarray | 频率扫描范围 |
| error | str | 错误信息（空表示无错误） |
| committed | str | 提交哈希 |
| created | str | 创建时间 |
| finished | str | 完成时间 |

## 应用场景

获取测量数据主要用于：
- 回顾历史测量结果
- 数据分析与二次处理
- 验证实验结果
- 与其他系统共享测量数据