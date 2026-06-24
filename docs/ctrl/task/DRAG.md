# Ctrl.DRAG 任务接口文档

## 概述

Ctrl.DRAG 是 Ctrl 中的一个任务，用于执行DRAG免交叉点测量，优化量子比特的DRAG参数以减少泄漏到非计算态的概率。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.DRAG` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| lamb | list[float] | 是 | DRAG参数λ的扫描范围，例如[0.0, 0.1, 0.2, ..., 1.0] |
| stage | int | 否 | 测量阶段，默认值1 |
| N_repeat | int | 否 | 重复次数，默认值1 |
| pulsePair | list[int] | 否 | 脉冲对配置，默认值[0, 1] |

### 调用示例

```python
# 执行DRAG免交叉点测量
result = client.run(
    task_type=CtrlTaskName.DRAG,
    qubits=["Q0"],
    lamb=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    stage=1,
    N_repeat=1,
    pulsePair=[0, 1]
)

print(result)
```

## 返回值格式

返回的结果包含DRAG参数扫描数据和最优参数：

```json
{
  "data": {
    "Q0": {
      "lamb": [float, ...],
      "population": [float, ...],
      "optimal_lamb": float
    }
  },
  "parameters": {
    "stage": 1,
    "N_repeat": 1,
    "pulsePair": [0, 1]
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的DRAG测量数据 |
| lamb | List[float] | DRAG参数λ的扫描值 |
| population | List[float] | 对应λ值下的目标态布居数 |
| optimal_lamb | float | 最优的DRAG参数值 |
| parameters | dict | 实验参数信息 |

## 应用场景

DRAG免交叉点测量主要用于：
- 优化单量子比特门的保真度
- 减少量子比特操作中的泄漏误差
- 提高量子算法的执行精度