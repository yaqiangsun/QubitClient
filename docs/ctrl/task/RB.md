# Ctrl.RB 任务接口文档

## 概述

Ctrl.RB 是 Ctrl 中的一个任务，用于执行随机基准测试（Randomized Benchmarking），用于测量量子门序列的保真度。这是评估量子计算平台性能的核心指标之一。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.RB` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| couplers | tuple | 否 | 耦合器列表，例如("C0",) |
| stage | int | 否 | 随机基准测试的阶段数，默认3 |
| gate | list | 否 | 门序列类型，默认['ref'] |
| cycle | list | 否 | 循环次数列表，例如[1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1000] |
| size | int | 否 | 每个循环次数的样本数量，默认11 |

### 调用示例

```python
# 执行随机基准测试
result = client.run(
    task_type=CtrlTaskName.RB,
    qubits=["Q0"],
    couplers=(),
    stage=3,
    gate=['ref'],
    cycle=[1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1000],
    size=11
)

print(result)
```

## 返回值格式

返回的结果包含随机基准测试数据和保真度信息：

```json
{
  "data": {
    "Q0": {
      "cycle": [int, ...],
      "survival_probability": [float, ...],
      "infidelity": float,
      "error_per_gate": float
    }
  },
  "parameters": {
    "stage": 3,
    "gate": ["ref"],
    "size": 11
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的RB测量数据 |
| cycle | List[int] | 随机门序列的循环次数 |
| survival_probability | List[float] | 对应循环次数下的存活概率 |
| infidelity | float | 失保真度（1 - 门保真度） |
| error_per_gate | float | 每个门的平均错误率 |
| parameters | dict | 实验参数信息 |

## 应用场景

随机基准测试主要用于：
- 评估量子门操作的整体保真度
- 表征量子比特的相干性能和门质量
- 基准测试不同量子处理器
- 监控量子设备随时间的稳定性
- 比较不同门优化策略的效果