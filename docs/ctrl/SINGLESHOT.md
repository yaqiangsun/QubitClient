# Ctrl.SINGLESHOT 任务接口文档

## 概述

Ctrl.SINGLESHOT 是 Ctrl 中的一个任务，用于执行单次测量分析，评估量子比特的读出保真度和区分度。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.SINGLESHOT` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| stage | int | 否 | 测量阶段，默认值1 |

### 调用示例

```python
# 执行单次测量分析
result = client.run(
    task_type=CtrlTaskName.SINGLESHOT,
    qubits=["Q0", "Q1"],
    stage=1
)

print(result)
```

## 返回值格式

返回的结果包含单次测量统计数据和读出保真度：

```json
{
  "data": {
    "Q0": {
      "ground_state_samples": [complex, ...],
      "excited_state_samples": [complex, ...],
      "readout_fidelity": float,
      "assignment_fidelity": float,
      "threshold": complex
    },
    "Q1": {
      "ground_state_samples": [complex, ...],
      "excited_state_samples": [complex, ...],
      "readout_fidelity": float,
      "assignment_fidelity": float,
      "threshold": complex
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
| data | dict | 包含每个量子比特的单次测量数据 |
| ground_state_samples | List[complex] | 基态单次测量样本 |
| excited_state_samples | List[complex] | 激发态单次测量样本 |
| readout_fidelity | float | 读出保真度（0-1） |
| assignment_fidelity | float | 分配保真度（0-1） |
| threshold | complex | 最优判别阈值 |
| parameters | dict | 实验参数信息 |

## 应用场景

单次测量分析主要用于：
- 评估量子比特读出系统的性能
- 优化读出脉冲参数
- 计算量子计算中的测量误差
- 为量子纠错提供基础数据