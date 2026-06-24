# Ctrl.SPINECHO_T2 任务接口文档

## 概述

Ctrl.SPINECHO_T2 是 Ctrl 中的一个任务，用于执行自旋回波（Spin Echo）T2测量，通过自旋回波技术测量量子比特的相位弛豫时间T2，可以有效抑制低频噪声的影响。

## 接口使用方式

### 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| task_type | CtrlTaskName | 是 | 任务类型，固定为`CtrlTaskName.SPINECHO_T2` |
| qubits | list[str] | 是 | 要测量的量子比特列表，例如["Q0", "Q1"] |
| delay_start | float | 否 | 延迟时间起始点（秒），默认值0 |
| delay_end | float | 否 | 延迟时间结束点（秒），默认值10000 |
| delay_sample_num | int | 否 | 延迟时间采样点数，默认值200 |
| fringeFreq | float | 否 | 拍频频率（MHz），默认值0.05 |
| pipulse_num | int | 否 | π脉冲数量，默认值None |

### 调用示例

```python
# 执行自旋回波T2测量
result = client.run(
    task_type=CtrlTaskName.SPINECHO_T2,
    qubits=["Q0"],
    delay_start=0,
    delay_end=10000,
    delay_sample_num=200,
    fringeFreq=0.05,
    pipulse_num=None
)

print(result)
```

## 返回值格式

返回的结果包含自旋回波T2测量数据和拟合参数：

```json
{
  "data": {
    "Q0": {
      "delay_time": [float, ...],
      "population": [float, ...],
      "t2_time": float,
      "decay_rate": float
    }
  },
  "parameters": {
    "delay_start": 0,
    "delay_end": 10000,
    "delay_sample_num": 200,
    "fringeFreq": 0.05
  }
}
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| data | dict | 包含每个量子比特的自旋回波T2测量数据 |
| delay_time | List[float] | 延迟时间扫描点（秒） |
| population | List[float] | 对应延迟时间下的激发态布居数 |
| t2_time | float | 相位弛豫时间T2（秒） |
| decay_rate | float | 退相干衰减率（1/秒） |
| parameters | dict | 实验参数信息 |

## 应用场景

自旋回波T2测量主要用于：
- 表征量子比特的相位相干特性（对低频噪声不敏感）
- 区分T1和T2贡献
- 评估量子比特的退相干性能
- 优化量子门操作的保真度
- 研究环境噪声对量子比特相位的影响