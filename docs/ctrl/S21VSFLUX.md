# Ctrl.S21VSFLUX 任务接口文档

## 概述

Ctrl.S21VSFLUX 是 Ctrl 中的一个任务，用于执行S21 vs Flux测量，分析磁通量对量子比特频率的影响，常用于表征可调谐量子比特。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.S21VSFLUX` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| freq_center | float | 否 | 频率中心点（GHz），默认值6.5 |
| freq_half_bandwidth | float | 否 | 频率半带宽（GHz），默认值0.03 |
| freq_sample_num | int | 否 | 频率采样点数，默认值11 |
| read_bias_start | float | 否 | 读出偏置起始点，默认值-3 |
| read_bias_end | float | 否 | 读出偏置结束点，默认值3 |
| read_bias_sample_num | int | 否 | 读出偏置采样点数，默认值16 |

### 调用示例

```python
# 执行S21 vs Flux测量
result = client.run(
    task_type=CtrlTaskName.S21VSFLUX,
    qubits=["Q0", "Q1"],
    freq_center=6.5,
    freq_half_bandwidth=0.03,
    freq_sample_num=11,
    read_bias_start=-3,
    read_bias_end=3,
    read_bias_sample_num=16
)

print(result)
```

## 返回值格式

返回的结果包含磁通量-频率二维扫描数据：

```json
{
  "data": {
    "Q0": {
      "flux_bias": [float, ...],
      "frequency": [float, ...],
      "s21_response": [[complex, ...], ...]
    }
  },
  "parameters": {
    "flux_range": [-0.5, 0.5],
    "frequency_range": [4800000000.0, 5200000000.0]
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的S21 vs Flux测量数据 |
| flux_bias | List[float] | 磁通量偏置扫描点 |
| frequency | List[float] | 频率扫描点（Hz） |
| s21_response | List[List[complex]] | 二维S21响应矩阵，每个元素为复数 |
| parameters | dict | 实验参数信息 |

## 应用场景

S21 vs Flux测量主要用于：
- 表征可调谐量子比特的频率-磁通关系
- 确定量子比特的工作点（sweet spot）
- 测量量子比特的非谐性
- 分析磁通噪声对量子比特的影响