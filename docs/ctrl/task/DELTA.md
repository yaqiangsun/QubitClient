# Ctrl.DELTA 任务接口文档

## 概述

Ctrl.DELTA 是 Ctrl 中的一个任务，用于执行频率偏移校准测量，确定量子比特的最佳工作频率偏移量。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.DELTA` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| stage | int | 否 | 测量阶段，默认值1 |

### 调用示例

```python
# 执行频率偏移校准测量
result = client.run(
    task_type=CtrlTaskName.DELTA,
    qubits=["Q0", "Q1"],
    stage=1
)

print(result)
```

## 返回值格式

返回的结果包含频率偏移校准数据和最优偏移量：

```json
{
  "data": {
    "Q0": {
      "frequency_offset": float,
      "calibration_data": [float, ...],
      "optimal_frequency": float
    },
    "Q1": {
      "frequency_offset": float,
      "calibration_data": [float, ...],
      "optimal_frequency": float
    }
  },
  "parameters": {
    "stage": 1
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的频率偏移校准数据 |
| frequency_offset | float | 频率偏移量（Hz） |
| calibration_data | List[float] | 校准过程中的测量数据 |
| optimal_frequency | float | 最优工作频率（Hz） |
| parameters | dict | 实验参数信息 |

## 应用场景

频率偏移校准测量主要用于：
- 校准量子比特的工作频率
- 补偿环境漂移对量子比特频率的影响
- 优化量子门操作的频率精度
- 提高量子算法的执行稳定性