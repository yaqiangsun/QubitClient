# Ctrl.RABI 任务接口文档

## 概述

Ctrl.RABI 是 Ctrl 中的一个任务，用于执行Rabi振荡测量，观察量子比特在驱动场下的振荡行为，用于校准单量子比特门。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.RABI` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| piamp_start | float | 否 | π脉冲幅度起始值，默认值0 |
| piamp_end | float | 否 | π脉冲幅度结束值，默认值2 |
| piamp_sample_num | int | 否 | π脉冲幅度采样点数，默认值16 |

### 调用示例

```python
# 执行Rabi振荡测量
result = client.run(
    task_type=CtrlTaskName.RABI,
    qubits=["Q0"],
    piamp_start=0,
    piamp_end=2,
    piamp_sample_num=16
)

print(result)
```

## 返回值格式

返回的结果包含Rabi振荡数据和拟合参数：

```json
{
  "data": {
    "Q0": {
      "drive_amp": [float, ...],
      "population": [float, ...],
      "rabi_frequency": float,
      "pi_pulse_amp": float
    }
  },
  "parameters": {
    "width": 3e-8
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的Rabi测量数据 |
| drive_amp | List[float] | 驱动幅度扫描值 |
| population | List[float] | 对应驱动幅度下的激发态布居数 |
| rabi_frequency | float | Rabi振荡频率（Hz） |
| pi_pulse_amp | float | π脉冲对应的驱动幅度 |
| parameters | dict | 实验参数信息 |

## 应用场景

Rabi振荡测量主要用于：
- 校准单量子比特门的幅度
- 测量量子比特与驱动场的耦合强度
- 确定π脉冲和π/2脉冲的操作参数