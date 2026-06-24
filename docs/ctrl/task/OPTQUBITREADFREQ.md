# Ctrl.OPTQUBITREADFREQ 任务接口文档

## 概述

Ctrl.OPTQUBITREADFREQ 是 Ctrl 中的一个任务，用于自动优化量子比特的读出频率，以获得最佳的读出保真度。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.OPTQUBITREADFREQ` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| freq_span | float | 否 | 频率扫描范围（GHz），默认值0.0055 |

### 调用示例

```python
# 执行读出频率优化
result = client.run(
    task_type=CtrlTaskName.OPTQUBITREADFREQ,
    qubits=["Q0", "Q1"],
    freq_span=0.0055
)

print(result)
```

## 返回值格式

返回的结果包含优化后的读出频率：

```json
{
  "data": {
    "Q0": {
      "optimal_freq": float,
      "readout_fidelity": float
    }
  },
  "parameters": {
    "freq_span": 0.0055
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的优化结果 |
| optimal_freq | float | 最优读出频率 |
| readout_fidelity | float | 读出保真度 |
| parameters | dict | 实验参数信息 |

## 应用场景

读出频率优化主要用于：
- 自动寻找最佳读出频率
- 提高量子比特读出保真度
- 优化量子测量操作