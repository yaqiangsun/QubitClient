# Ctrl.XEB 任务接口文档

## 概述

Ctrl.XEB 是 Ctrl 中的一个任务，用于执行Cross-Entropy Benchmarking（XEB）测量，评估量子门序列的保真度。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.XEB` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| m_start | int | 否 | 门序列长度起始值，默认值0 |
| m_end | int | 否 | 门序列长度结束值，默认值400 |
| m_sample_num | int | 否 | 门序列长度采样点数，默认值10 |
| k | int | 否 | 每组随机门的数量，默认值30 |
| gate | str | 否 | 门类型，默认值'reference' |
| tbuffer | float | 否 | 缓冲区时间（秒），默认值0 |
| stats | int | 否 | 统计次数，默认值300 |

### 调用示例

```python
# 执行XEB测量
result = client.run(
    task_type=CtrlTaskName.XEB,
    qubits=["Q0", "Q1"],
    m_start=0,
    m_end=400,
    m_sample_num=10,
    k=30,
    gate='reference',
    tbuffer=0,
    stats=300
)

print(result)
```

## 返回值格式

返回的结果包含XEB测量数据和保真度信息：

```json
{
  "data": {
    "Q0": {
      "m": [int, ...],
      "fidelity": [float, ...],
      "error_rate": float
    }
  },
  "parameters": {
    "m_start": 0,
    "m_end": 400,
    "m_sample_num": 10,
    "k": 30,
    "gate": "reference",
    "stats": 300
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的XEB测量数据 |
| m | List[int] | 门序列长度 |
| fidelity | List[float] | 对应序列长度的保真度 |
| error_rate | float | 估计的错误率 |
| parameters | dict | 实验参数信息 |

## 应用场景

XEB测量主要用于：
- 高精度量子门保真度评估
- 量子处理器性能基准测试
- 量子纠错码的保真度验证
- 量子算法保真度预测