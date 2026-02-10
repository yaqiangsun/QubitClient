# Ctrl.OPT_PIPULSE 任务接口文档

## 概述

Ctrl.OPT_PIPULSE 是 Ctrl 中的一个任务，用于执行最优π脉冲测量，寻找最佳的π脉冲幅度以实现高保真度的单量子比特旋转门。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.OPT_PIPULSE` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| stage | int | 否 | 测量阶段，默认值1 |

### 调用示例

```python
# 执行最优π脉冲测量
result = client.run(
    task_type=CtrlTaskName.OPT_PIPULSE,
    qubits=["Q0", "Q1"],
    stage=1
)

print(result)
```

## 返回值格式

返回的结果包含π脉冲幅度扫描数据和最优参数：

```json
{
  "data": {
    "Q0": {
      "drive_amp": [float, ...],
      "population": [float, ...],
      "optimal_drive_amp": float
    },
    "Q1": {
      "drive_amp": [float, ...],
      "population": [float, ...],
      "optimal_drive_amp": float
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
| data | dict | 包含每个量子比特的π脉冲测量数据 |
| drive_amp | List[float] | 驱动幅度的扫描值 |
| population | List[float] | 对应驱动幅度下的目标态布居数 |
| optimal_drive_amp | float | 最优的π脉冲驱动幅度 |
| parameters | dict | 实验参数信息 |

## 应用场景

最优π脉冲测量主要用于：
- 校准单量子比特X门的幅度
- 提高量子门操作的保真度
- 为后续的量子算法提供精确的基础门操作