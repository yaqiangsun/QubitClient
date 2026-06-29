# Ctrl 模块文档索引

## 概述

QubitCtrlClient 是基于 MCP 协议的量子比特实时测控客户端，支持多种校准和表征任务。

## 客户端初始化

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()
```

## 调用方式

### 1. 通过 `client.run()` 调用

```python
result = client.run(
    task_type=CtrlTaskName.S21,
    qubits=["Q0", "Q1"],
    frequency_center=6.5,
    frequency_half_bandwidth=0.0005
)
```

### 2. 直接调用任务函数

```python
from qubitclient.ctrl.task import s21, t1, rabi, ramsey

result = s21(qubits=["Q0", "Q1"], frequency_center=6.5, frequency_half_bandwidth=0.0005)
result = t1(qubits=["Q0"], delay_start=0, delay_end=80000)
```

### 3. 客户端实例方法

```python
result = client.get_data(rid=80)                              # 获取历史数据
result = client.query_param(qname="Q0", key="frequency")     # 查询参数
result = client.update_param(qname="Q0", task_type="rabi", values={"pi_amp": 0.5})  # 更新参数
```

## 任务列表

### 基础测量任务

| 任务名称 | 文档 | 描述 |
|----------|------|------|
| S21 | [S21.md](task/S21.md) | S21腔频测量 |
| S21PEAKMULTI | [S21PEAKMULTI.md](task/S21PEAKMULTI.md) | 多频点S21测量 |
| SINGLESHOT | [SINGLESHOT.md](task/SINGLESHOT.md) | 单次测量分析 |
| SPECTRUM | [SPECTRUM.md](task/SPECTRUM.md) | 频谱分析测量 |
| SPECTRUM_2D | [SPECTRUM_2D.md](task/SPECTRUM_2D.md) | 二维频谱测量 |

### 弛豫时间测量

| 任务名称 | 文档 | 描述 |
|----------|------|------|
| T1 | [T1.md](task/T1.md) | T1能量弛豫时间测量 |
| T1_2D | [T1_2D.md](task/T1_2D.md) | 二维T1测量 |
| SPINECHO_T2 | [SPINECHO_T2.md](task/SPINECHO_T2.md) | 自旋回波T2测量 |
| RAMSEY_T2 | [RAMSEY_T2.md](task/RAMSEY_T2.md) | Ramsey T2*测量 |

### 量子门校准

| 任务名称 | 文档 | 描述 |
|----------|------|------|
| RABI | [RABI.md](task/RABI.md) | Rabi振荡测量 |
| RAMSEY | [RAMSEY.md](task/RAMSEY.md) | Ramsey干涉测量 |
| DRAG | [DRAG.md](task/DRAG.md) | DRAG免交叉点测量 |
| OPT_PIPULSE | [OPT_PIPULSE.md](task/OPT_PIPULSE.md) | 最优π脉冲测量 |
| PIPULSEF10 | [PIPULSEF10.md](task/PIPULSEF10.md) | π脉冲频率扫描 |
| SETPIALPHA | [SETPIALPHA.md](task/SETPIALPHA.md) | π脉冲幅度参数校准 |

### 频率/功率扫描

| 任务名称 | 文档 | 描述 |
|----------|------|------|
| POWERSHIFT | [POWERSHIFT.md](task/POWERSHIFT.md) | 功率偏移曲线测量 |
| S21VSFLUX | [S21VSFLUX.md](task/S21VSFLUX.md) | S21随磁通变化测量 |

### 基准测试

| 任务名称 | 文档 | 描述 |
|----------|------|------|
| RB | [RB.md](task/RB.md) | 随机基准测试 |
| XEB | [XEB.md](task/XEB.md) | Cross-Entropy Benchmarking |

### 高级任务

| 任务名称 | 文档 | 描述 |
|----------|------|------|
| DELTA | [DELTA.md](task/DELTA.md) | 频率偏移校准 |
| OPTQUBITREADFREQ | [OPTQUBITREADFREQ.md](task/OPTQUBITREADFREQ.md) | 读出频率优化 |
| TIMINGXYZ | [TIMINGXYZ.md](task/TIMINGXYZ.md) | 时序校准 |
| PULSESHAPE | [PULSESHAPE.md](task/PULSESHAPE.md) | 脉冲形状扫描 |
| BASESLOPE | [BASESLOPE.md](task/BASESLOPE.md) | 基线斜率测量 |

### 客户端实例方法

| 方法名 | 文档 | 描述 |
|--------|------|------|
| get_data | [DATA.md](DATA.md) | 根据RID获取历史数据 |
| query_param | [QUERY_PARAM.md](QUERY_PARAM.md) | 查询量子比特参数 |
| update_param | [UPDATE_PARAM.md](UPDATE_PARAM.md) | 更新量子比特参数 |

## CtrlTaskName 枚举值

```python
class CtrlTaskName(Enum):
    S21 = "s21"
    S21PEAKMULTI = "s21peakmulti"
    DRAG = "drag"
    DELTA = "delta"
    OPTPIPULSE = "opt_pipulse"
    POWERSHIFT = "powershift"
    RABI = "rabi"
    RAMSEY = "ramsey"
    S21VSFLUX = "s21vsflux"
    SINGLESHOT = "singleshot"
    SPECTRUM = "spectrum"
    SPECTRUM_2D = "spectrum_2d"
    T1 = "t1"
    RB = "rb"
    DATA = "get_data"
    # 额外任务
    T1_2D = "t1_2d"
    SPINECHO_T2 = "spinecho_t2"
    RAMSEY_T2 = "ramsey_t2"
    XEB = "xeb"
    PIPULSEF10 = "pipulsef10"
    OPTQUBITREADFREQ = "optqubitreadfreq"
    TIMINGXYZ = "timingxyz"
    PULSESHAPE = "pulseshape"
    SETPIALPHA = "setpialpha"
    BASESLOPE = "baseslope"
```