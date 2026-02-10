# Ctrl.SPECTRUM 任务接口文档

## 概述

Ctrl.SPECTRUM 是 Ctrl 中的一个任务，用于执行频谱分析测量，扫描量子比特的能级结构，识别共振频率和跃迁。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.SPECTRUM` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| freq | list[float] | 是 | 频率扫描范围，例如[4.5e9, 4.6e9, ..., 5.5e9] (Hz) |
| drive_amp | float | 否 | 驱动幅度，默认值0.04 |
| duration | float | 否 | 脉冲持续时间，默认值40e-6秒 |
| from_idle | bool | 否 | 是否从空闲状态开始，默认值True |
| absolute | bool | 否 | 是否使用绝对频率，默认值True |
| signal | str | 否 | 信号类型，默认值"iq_avg" |
| build_dependencies | bool | 否 | 是否构建依赖关系，默认值False |

### 调用示例

```python
# 执行频谱分析测量
result = client.run(
    task_type=CtrlTaskName.SPECTRUM,
    qubits=["Q0"],
    freq=[4.8e9, 4.9e9, 5.0e9, 5.1e9, 5.2e9],
    drive_amp=0.04,
    duration=40e-6,
    from_idle=True,
    absolute=True,
    signal="iq_avg",
    build_dependencies=False
)

print(result)
```

## 返回值格式

返回的结果包含频谱扫描数据和共振峰信息：

```json
{
  "data": {
    "Q0": {
      "frequency": [float, ...],
      "amplitude": [float, ...],
      "phase": [float, ...],
      "resonance_peaks": [float, ...],
      "peak_widths": [float, ...]
    }
  },
  "parameters": {
    "drive_amp": 0.04,
    "duration": 4e-5,
    "from_idle": true,
    "absolute": true,
    "signal": "iq_avg"
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的频谱测量数据 |
| frequency | List[float] | 频率扫描点（Hz） |
| amplitude | List[float] | 幅度响应 |
| phase | List[float] | 相位响应 |
| resonance_peaks | List[float] | 检测到的共振峰频率 |
| peak_widths | List[float] | 共振峰宽度 |
| parameters | dict | 实验参数信息 |

## 应用场景

频谱分析测量主要用于：
- 识别量子比特的共振频率
- 测量能级间的跃迁强度
- 表征多能级量子系统的结构
- 校准量子门操作的频率参数