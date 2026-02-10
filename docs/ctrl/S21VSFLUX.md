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
| qubits_scan | list[str] | 是 | 要扫描的量子比特列表，例如["Q0", "Q1"] |
| read_bias | list[float] | 是 | 读出偏置（磁通量）扫描范围，例如[-0.5, -0.4, ..., 0.5] |
| freq | list[float] | 是 | 频率扫描范围，例如[4.5e9, 4.6e9, ..., 5.5e9] (Hz) |
| qubits_read | list[str] | 是 | 用于读出的量子比特列表，例如["Q0", "Q1"] |

### 调用示例

```python
# 执行S21 vs Flux测量
result = client.run(
    task_type=CtrlTaskName.S21VSFLUX,
    qubits_scan=["Q0"],
    read_bias=[-0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
    freq=[4.8e9, 4.9e9, 5.0e9, 5.1e9, 5.2e9],
    qubits_read=["Q0"]
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