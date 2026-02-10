# Ctrl.RAMSEY 任务接口文档

## 概述

Ctrl.RAMSEY 是 Ctrl 中的一个任务，用于执行Ramsey干涉测量，测量量子比特的退相干时间T2*和频率偏移。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.RAMSEY` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| delta | float | 否 | 频率偏移量，默认值20e6 Hz |
| delay | float | 否 | 最大延迟时间，默认值10e-6秒 |
| stage | int | 否 | 测量阶段，默认值1 |
| scale | int | 否 | 延迟时间缩放因子，默认值15 |

### 调用示例

```python
# 执行Ramsey干涉测量
result = client.run(
    task_type=CtrlTaskName.RAMSEY,
    qubits=["Q0"],
    delta=20e6,
    delay=10e-6,
    stage=1,
    scale=15
)

print(result)
```

## 返回值格式

返回的结果包含Ramsey干涉数据和拟合参数：

```json
{
  "data": {
    "Q0": {
      "delay_time": [float, ...],
      "population": [float, ...],
      "t2_star": float,
      "frequency_offset": float,
      "decay_rate": float
    }
  },
  "parameters": {
    "delta": 20000000.0,
    "delay": 1e-5,
    "stage": 1,
    "scale": 15
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的Ramsey测量数据 |
| delay_time | List[float] | 延迟时间扫描点（秒） |
| population | List[float] | 对应延迟时间下的布居数振荡 |
| t2_star | float | 退相干时间T2*（秒） |
| frequency_offset | float | 频率偏移量（Hz） |
| decay_rate | float | 衰减率 |
| parameters | dict | 实验参数信息 |

## 应用场景

Ramsey干涉测量主要用于：
- 测量量子比特的退相干时间T2*
- 校准量子比特的工作频率
- 表征环境噪声对量子比特的影响