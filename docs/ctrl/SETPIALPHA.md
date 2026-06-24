# Ctrl.SETPIALPHA 任务接口文档

## 概述

Ctrl.SETPIALPHA 是 Ctrl 中的一个任务，用于执行π脉冲幅度优化测量，通过扫描不同π脉冲次数来校准π脉冲幅度参数α。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.SETPIALPHA` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| ms | list[int] | 否 | π脉冲次数列表，默认值[1, 3, 5] |
| gate | str | 否 | 门类型，默认值'X' |

### 调用示例

```python
# 执行π脉冲幅度优化
result = client.run(
    task_type=CtrlTaskName.SETPIALPHA,
    qubits=["Q0", "Q1"],
    ms=[1, 3, 5],
    gate='X'
)

print(result)
```

## 返回值格式

返回的结果包含π脉冲幅度优化数据：

```json
{
  "data": {
    "Q0": {
      "ms": [int, ...],
      "population": [float, ...],
      "optimal_alpha": float
    }
  },
  "parameters": {
    "ms": [1, 3, 5],
    "gate": "X"
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的π脉冲幅度优化数据 |
| ms | List[int] | π脉冲次数 |
| population | List[float] | 对应脉冲次数下的激发态布居数 |
| optimal_alpha | float | 最优的α参数值 |
| parameters | dict | 实验参数信息 |

## 应用场景

π脉冲幅度优化主要用于：
- 校准π脉冲幅度参数α
- 提高单量子比特门的保真度
- 验证脉冲校准的准确性