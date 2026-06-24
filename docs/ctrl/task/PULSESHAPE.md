# Ctrl.PULSESHAPE 任务接口文档

## 概述

Ctrl.PULSESHAPE 是 Ctrl 中的一个任务，用于执行脉冲形状扫描测量，表征脉冲参数对量子比特响应的影响。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.PULSESHAPE` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| zpa_height | float | 否 | Z脉冲幅度高度，默认值0.2 |
| delay_start | float | 否 | 延迟时间起始点（ns），默认值0 |
| delay_end | float | 否 | 延迟时间结束点（ns），默认值1000 |
| delay_sample_num | int | 否 | 延迟时间采样点数，默认值100 |
| z_offset_half_bandwidth | float | 否 | Z偏移半带宽，默认值0.01 |
| z_offset_num | float | 否 | Z偏移采样数，默认值1.0 |

### 调用示例

```python
# 执行脉冲形状扫描测量
result = client.run(
    task_type=CtrlTaskName.PULSESHAPE,
    qubits=["Q0", "Q1"],
    zpa_height=0.2,
    delay_start=0,
    delay_end=1000,
    delay_sample_num=100,
    z_offset_half_bandwidth=0.01,
    z_offset_num=1.0
)

print(result)
```

## 返回值格式

返回的结果包含脉冲形状扫描数据：

```json
{
  "data": {
    "Q0": {
      "delay": [float, ...],
      "z_offset": [float, ...],
      "response": [[float, ...], ...]
    }
  },
  "parameters": {
    "zpa_height": 0.2,
    "delay_start": 0,
    "delay_end": 1000,
    "delay_sample_num": 100,
    "z_offset_half_bandwidth": 0.01,
    "z_offset_num": 1.0
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的脉冲形状扫描数据 |
| delay | List[float] | 延迟时间扫描点（ns） |
| z_offset | List[float] | Z偏移扫描点 |
| response | List[List[float]] | 二维响应矩阵 |
| parameters | dict | 实验参数信息 |

## 应用场景

脉冲形状扫描测量主要用于：
- 表征脉冲参数对量子比特的影响
- 优化脉冲形状以提高门保真度
- 研究Z脉冲的时序特性