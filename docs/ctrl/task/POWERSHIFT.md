# Ctrl.POWERSHIFT 任务接口文档

## 概述

Ctrl.POWERSHIFT 是 Ctrl 中的一个任务，用于执行功率偏移曲线测量，分析不同驱动功率下的量子比特响应特性。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.POWERSHIFT` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| freq_center | float | 否 | 频率中心点（GHz），默认值6.539 |
| freq_half_bandwidth | float | 否 | 频率半带宽（GHz），默认值0.0015 |
| freq_sample_num | int | 否 | 频率采样点数，默认值16 |
| power_start | float | 否 | 功率起始点（dBm），默认值-40 |
| power_end | float | 否 | 功率结束点（dBm），默认值-16 |
| power_sample_num | int | 否 | 功率采样点数，默认值13 |

### 调用示例

```python
# 执行功率偏移曲线测量
result = client.run(
    task_type=CtrlTaskName.POWERSHIFT,
    qubits=["Q0"],
    freq_center=6.539,
    freq_half_bandwidth=0.0015,
    freq_sample_num=16,
    power_start=-40,
    power_end=-16,
    power_sample_num=13
)

print(result)
```

## 返回值格式

返回的结果包含功率-频率二维扫描数据：

```json
{
  "data": {
    "Q0": {
      "power": [float, ...],
      "frequency": [float, ...],
      "response": [[complex, ...], ...]
    }
  },
  "parameters": {
    "power_range": [-20, 20],
    "frequency_range": [4800000000.0, 5200000000.0]
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的功率偏移测量数据 |
| power | List[float] | 功率扫描点（dBm） |
| frequency | List[float] | 频率扫描点（Hz） |
| response | List[List[complex]] | 二维响应矩阵，每个元素为复数 |
| parameters | dict | 实验参数信息 |

## 应用场景

功率偏移曲线测量主要用于：
- 确定量子比特的最佳工作功率
- 分析功率对量子比特相干性的影响
- 优化量子门操作的驱动功率