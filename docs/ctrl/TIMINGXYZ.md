# Ctrl.TIMINGXYZ 任务接口文档

## 概述

Ctrl.TIMINGXYZ 是 Ctrl 中的一个任务，用于执行时序校准测量，测量XYZ控制脉冲的时序偏移特性。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.TIMINGXYZ` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| delay_start | float | 否 | 延迟时间起始点（ns），默认值-60 |
| delay_end | float | 否 | 延迟时间结束点（ns），默认值60 |
| delay_sample_num | int | 否 | 延迟时间采样点数，默认值31 |
| zpa | float | 否 | Z脉冲幅度，默认值0.5 |

### 调用示例

```python
# 执行时序校准测量
result = client.run(
    task_type=CtrlTaskName.TIMINGXYZ,
    qubits=["Q0", "Q1"],
    delay_start=-60,
    delay_end=60,
    delay_sample_num=31,
    zpa=0.5
)

print(result)
```

## 返回值格式

返回的结果包含时序校准数据：

```json
{
  "data": {
    "Q0": {
      "delay": [float, ...],
      "population": [float, ...],
      "timing_offset": float
    }
  },
  "parameters": {
    "delay_start": -60,
    "delay_end": 60,
    "delay_sample_num": 31,
    "zpa": 0.5
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的时序校准数据 |
| delay | List[float] | 延迟时间扫描点（ns） |
| population | List[float] | 对应延迟时间下的布居数 |
| timing_offset | float | 时序偏移量 |
| parameters | dict | 实验参数信息 |

## 应用场景

时序校准测量主要用于：
- 校准XYZ控制脉冲的时序
- 测量控制信号的传播延迟
- 优化多量子比特门操作的时序同步