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
| freq_start | float | 否 | 频率起始点（GHz），默认值1.0 |
| freq_end | float | 否 | 频率结束点（GHz），默认值3.0 |
| freq_sample_num | int | 否 | 频率采样点数，默认值200 |
| zpa | float | 否 | Z脉冲幅度，默认值0 |
| spec_amp | float | 否 | 谱仪幅度，默认值0.0 |
| sb_freq | float | 否 | 边带频率（GHz），默认值0 |

### 调用示例

```python
# 执行频谱分析测量
result = client.run(
    task_type=CtrlTaskName.SPECTRUM,
    qubits=["Q0"],
    freq_start=1.0,
    freq_end=3.0,
    freq_sample_num=200,
    zpa=0,
    spec_amp=0.0,
    sb_freq=0
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