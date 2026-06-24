# Ctrl.BASESLOPE 任务接口文档

## 概述

Ctrl.BASESLOPE 是 Ctrl 中的一个任务，用于执行基线斜率测量，表征量子比特响应的直流偏置特性。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.BASESLOPE` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| delay_start | float | 否 | 延迟时间起始点（ns），默认值0 |
| delay_end | float | 否 | 延迟时间结束点（ns），默认值1000 |
| delay_sample_num | int | 否 | 延迟时间采样点数，默认值100 |
| step_height | float | 否 | 阶跃高度，默认值0 |

### 调用示例

```python
# 执行基线斜率测量
result = client.run(
    task_type=CtrlTaskName.BASESLOPE,
    qubits=["Q0", "Q1"],
    delay_start=0,
    delay_end=1000,
    delay_sample_num=100,
    step_height=0
)

print(result)
```

## 返回值格式

返回的结果包含基线斜率测量数据：

```json
{
  "data": {
    "Q0": {
      "delay": [float, ...],
      "response": [float, ...],
      "slope": float
    }
  },
  "parameters": {
    "delay_start": 0,
    "delay_end": 1000,
    "delay_sample_num": 100,
    "step_height": 0
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的基线斜率数据 |
| delay | List[float] | 延迟时间扫描点（ns） |
| response | List[float] | 响应信号 |
| slope | float | 估计的基线斜率 |
| parameters | dict | 实验参数信息 |

## 应用场景

基线斜率测量主要用于：
- 表征量子比特响应的直流偏置特性
- 测量系统基线漂移
- 校准测量系统的直流响应