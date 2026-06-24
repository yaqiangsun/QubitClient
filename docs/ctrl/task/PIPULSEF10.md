# Ctrl.PIPULSEF10 任务接口文档

## 概述

Ctrl.PIPULSEF10 是 Ctrl 中的一个任务，用于执行π脉冲频率扫描测量，校准π脉冲在不同频率下的响应特性。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.PIPULSEF10` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| freq_half_bandwidth | float | 否 | 频率半带宽（GHz），默认值0.015 |
| freq_sample_num | int | 否 | 频率采样点数，默认值30 |

### 调用示例

```python
# 执行π脉冲频率扫描测量
result = client.run(
    task_type=CtrlTaskName.PIPULSEF10,
    qubits=["Q0", "Q1"],
    freq_half_bandwidth=0.015,
    freq_sample_num=30
)

print(result)
```

## 返回值格式

返回的结果包含π脉冲频率扫描数据：

```json
{
  "data": {
    "Q0": {
      "frequency": [float, ...],
      "population": [float, ...]
    }
  },
  "parameters": {
    "freq_half_bandwidth": 0.015,
    "freq_sample_num": 30
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的π脉冲频率扫描数据 |
| frequency | List[float] | 频率扫描点 |
| population | List[float] | 对应频率下的激发态布居数 |
| parameters | dict | 实验参数信息 |

## 应用场景

π脉冲频率扫描测量主要用于：
- 校准π脉冲的最佳频率
- 表征量子比特的频率响应
- 优化量子门操作的频率参数