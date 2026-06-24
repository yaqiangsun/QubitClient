# Ctrl.S21MULTI 任务接口文档

## 概述

Ctrl.S21MULTI 是 Ctrl 中的一个任务，用于执行多频点S21测量，在给定的频率范围内进行连续的S21响应测量。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.S21MULTI` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| frequency_start | float | 否 | 频率起始点（GHz），默认值6.3 |
| frequency_end | float | 否 | 频率结束点（GHz），默认值6.9 |
| frequency_sample_rate | float | 否 | 频率采样率（GHz），默认值0.0001 |

### 调用示例

```python
# 执行多频点S21测量
result = client.run(
    task_type=CtrlTaskName.S21MULTI,
    qubits=["Q0", "Q1"],
    frequency_start=6.3,
    frequency_end=6.9,
    frequency_sample_rate=0.0001
)

print(result)
```

## 返回值格式

返回的结果包含S21测量数据：

```json
{
  "data": {
    "Q0": {
      "frequency": [float, ...],
      "s21_real": [float, ...],
      "s21_imag": [float, ...]
    },
    "Q1": {
      "frequency": [float, ...],
      "s21_real": [float, ...],
      "s21_imag": [float, ...]
    }
  },
  "parameters": {
    "frequency_start": 6.3,
    "frequency_end": 6.9,
    "frequency_sample_rate": 0.0001
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的S21测量数据 |
| frequency | List[float] | 频率扫描点 |
| s21_real | List[float] | S21响应的实部 |
| s21_imag | List[float] | S21响应的虚部 |
| parameters | dict | 实验参数信息 |

## 应用场景

S21MULTI测量主要用于：
- 宽带S21频谱测量
- 快速扫描谐振腔响应
- 表征量子比特与谐振腔的耦合特性