# Ctrl.SPECTRUM_2D 任务接口文档

## 概述

Ctrl.SPECTRUM_2D 是 Ctrl 中的一个任务，用于执行二维频谱测量，同时扫描频率和偏置参数，获得量子比特的二维能级图。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.SPECTRUM_2D` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| freq_start | float | 否 | 频率起始点（GHz），默认值-3 |
| freq_end | float | 否 | 频率结束点（GHz），默认值3 |
| freq_sample_num | int | 否 | 频率采样点数，默认值200 |
| zpa_start | float | 否 | Z脉冲幅度起始点，默认值-1 |
| zpa_end | float | 否 | Z脉冲幅度结束点，默认值1 |
| zpa_sample_num | int | 否 | Z脉冲幅度采样点数，默认值100 |
| spec_amp | float | 否 | 谱仪幅度，默认值0.0 |
| sb_freq | float | 否 | 边带频率（GHz），默认值-0.15 |

### 调用示例

```python
# 执行二维频谱测量
result = client.run(
    task_type=CtrlTaskName.SPECTRUM_2D,
    qubits=["Q0"],
    freq_start=-3,
    freq_end=3,
    freq_sample_num=200,
    zpa_start=-1,
    zpa_end=1,
    zpa_sample_num=100,
    spec_amp=0.0,
    sb_freq=-0.15
)

print(result)
```

## 返回值格式

返回的结果包含二维频谱数据和能级结构信息：

```json
{
  "data": {
    "Q0": {
      "bias": [float, ...],
      "frequency": [float, ...],
      "response": [[complex, ...], ...],
      "energy_levels": [[float, ...], ...]
    }
  },
  "parameters": {
    "drive_amp": 0.05,
    "duration": 4e-5,
    "from_idle": false,
    "absolute": true
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的二维频谱测量数据 |
| bias | List[float] | 偏置参数扫描点 |
| frequency | List[float] | 频率扫描点（Hz） |
| response | List[List[complex]] | 二维响应矩阵，每个元素为复数 |
| energy_levels | List[List[float]] | 提取的能级结构 |
| parameters | dict | 实验参数信息 |

## 应用场景

二维频谱测量主要用于：
- 绘制量子比特的能级图
- 研究能级间的相互作用和耦合
- 表征可调谐量子系统的特性
- 识别避免交叉点（anti-crossing points）