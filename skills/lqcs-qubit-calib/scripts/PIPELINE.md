# 测量实验接口文档

本文档以 `pipeline/**_pipeline.py` 脚本和比特 `q3lu7` 为例，讲解所有测量实验任务的接口与调用实例。

---

## 目录

- [基础服务运行步骤](#基础服务运行步骤)
- [测量实验顺序](#测量实验顺序)
- [步骤详解](#步骤详解)
  1. [s21mul](#步骤1-s21mul)
  2. [s21peak](#步骤2-s21peak)
  3. [powershift](#步骤3-powershift)
  4. [s21vflux](#步骤4-s21vflux)
  5. [s21peak (bias_z=-1.5)](#步骤5-s21peak-bias_z-15)
  6. [spectrum](#步骤6-spectrum)
  7. [spectrum2d](#步骤7-spectrum2d)
  8. [singleshot](#步骤8-singleshot)
  9. [rabi](#步骤9-rabi)
  10. [PiPulseF10](#步骤10-pipulsef10)
  11. [ramsey](#步骤11-ramsey)
  12. [optQubitReadFreq](#步骤12-optqubitreadfreq)
  13. [opt_pipulse](#步骤13-opt_pipulse)
  14. [TimingXYZ](#步骤14-timingxyz)
  15. [PulseShape](#步骤15-pulseshape)
  16. [T1](#步骤16-t1)
  17. [T1_2d](#步骤17-t1_2d)
  18. [spinecho_T2](#步骤18-spinecho_t2)
  19. [Ramsey_T2](#步骤19-ramsey_t2)
  20. [xeb](#步骤20-xeb)

---

## 基础服务运行步骤

每一种数据的 Pipeline 含有以下步骤：

1. 初始化 MCP 客户端，用于与后端 MCP 服务通信
2. 运行 Pipeline，总体流程为：
   - 远程执行测量，等待测量成功后返回测量数据标识符
   - 利用返回的标识符，获取测量数据
   - 对测量的数据进行分析
   - 将分析结果画在原始数据上，可视化保存结果
   - 依据结果判断是否更新参数

---

## 测量实验顺序

```
s21mul → s21peak → powershift → s21vflux → s21peak(bias_z=-1.5) → spectrum → spectrum2d →
singleshot → rabi → PiPulseF10 → ramsey → optQubitReadFreq → opt_pipulse(X) →
TimingXYZ → PulseShape → T1 → T1_2d → spinecho_T2 → Ramsey_T2 → xeb
```

---

## 步骤详解

通用初始化代码（所有步骤均需先执行）：

```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

qubit_ctrl_client = QubitCtrlClient()
```

通用数据获取代码（测量后执行）：

```python
data_id = data[0]["text"]
data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)
```

---

### 步骤 1: s21mul

多比特 S21 扫描，用于初步定位比特频率。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]
data = qubit_ctrl_client.run(
    CtrlTaskName.S21PEAKMULTI,
    qubits=qubit_name_list,
    frequency_start=6.5,
    frequency_end=6.9,
    frequency_sample_rate=0.0001
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特
2. 对照图片，确认 `q3lu7` 的频率与图中一致

#### 参数更新

根据扫描结果，更新 `fread = 6.590`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.S21PEAKMULTI
values = "6.590"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 2: s21peak

单比特 S21 峰值扫描，精确测量比特读取频率。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]
fread = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM, key="fread_star")
data = qubit_ctrl_client.run(
    CtrlTaskName.S21,
    qubits=qubit_name_list,
    frequency_center=fread,
    frequency_half_bandwidth=0.005,
    frequency_sample_num=100
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

根据扫描结果，更新 `fread = 6.5898`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.S21PEAK
values = "6.590"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 3: powershift

功率扫描，测量比特读取功率对频率的影响。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]
qname = qubit_name_list[0]
fread = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM, qname=qname, key="fread_star")

data = qubit_ctrl_client.run(
    CtrlTaskName.POWERSHIFT,
    qubits=qubit_name_list,
    frequency_center=fread,
    frequency_half_bandwidth=0.0015,
    frequency_sample_num=16,
    power_start=-40,
    power_end=-16,
    power_sample_num=13
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

根据扫描结果，更新 `ReadIn.power = -30`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.POWERSHIFT
values = "-30"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 4: s21vflux

比特频率随磁通变化扫描（电压-频率关系）。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]
qname = qubit_name_list[0]
fread = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM, qname=qname, key="fread_star")

data = qubit_ctrl_client.run(
    CtrlTaskName.S21VSFLUX,
    qubits_scan=qubit_name_list,
    freq_center=fread,
    freq_half_bandwidth=0.001,
    freq_sample_num=11,
    read_bias_start=-3,
    read_bias_end=3,
    read_bias_sample_num=16
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

根据扫描结果，在余弦曲线上选取一点（通常应避开频率的极值点），例如选择 `zpa = -1.5`，更新 `bias_z = -1.5`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.S21VSFLUX
values = "-1.5"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 5: s21peak (bias_z=-1.5)

在特定偏置点进行 S21 峰值扫描。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]
qname = qubit_name_list[0]
fread = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM, qname=qname, key="fread_star")

data = qubit_ctrl_client.run(
    CtrlTaskName.S21,
    qubits=qubit_name_list,
    frequency_center=fread,
    frequency_half_bandwidth=0.005,
    frequency_sample_num=100
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

根据扫描结果，更新 `fread = 6.5896`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.S21PEAK
values = "6.5896"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 6: spectrum

频谱扫描，测量比特 |0⟩→|1⟩ 和 |1⟩→|2⟩ 跃迁频率。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.SPECTRUM,
    qubits=qubit_name_list,
    freq_start=-3,
    freq_end=3,
    freq_sample_num=200,
    bias=0,
    drive_amp=0.0
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

根据扫描结果，更新 `f10` 和 `f21`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.SPECTRUM
values = "3.193120459017055,3.193120459017055"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 7: spectrum2d

二维频谱扫描，测量比特频率随偏置电压的变化。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.SPECTRUM_2D,
    qubits=qubit_name_list,
    freq_start=-3,
    freq_end=3,
    freq_sample_num=200,
    bias_start=-1,
    bias_end=1,
    bias_sample_num=200,
    drive_amp=0.0
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

根据扫描结果，更新 `f10` 和 `f21`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.SPECTRUM_2D
values = "3.193120459017055,3.193120459017055"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 8: singleshot

单发读取测量，测量比特 |0⟩ 和 |1⟩ 态的区分度。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.SINGLESHOT,
    qubits=qubit_name_list
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

无参数更新

---

### 步骤 9: rabi

Rabi 振荡测量，确定 Pi 脉冲幅度。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.RABI,
    fc=None,
    amp_start=0,
    amp_end=2,
    amp_sample_num=16
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

根据扫描结果，更新 `PiGate.amp`和`PiHalf.amp`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.RABI
values = "1.2,0.6"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 10: PiPulseF10

Pi 脉冲频率校准，测量 |0⟩→|1⟩ 跃迁的精确频率。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.PIPULSEF10,
    qubits=qubit_name_list,
    df_start=0,
    df_end=0.03,
    df_sample_num=21
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

根据扫描结果，更新 `f10` 和 `f21`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.PIPULSEF10
values = "3.193120459017055,3.193120459017055"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 11: ramsey

Ramsey 干涉测量，确定比特退相干时间和频率偏移。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.RAMSEY,
    qubits=qubit_name_list,
    delay_start=0,
    delay_end=100,
    delay_sample_num=100,
    fringeFreq=0.05
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

根据扫描结果，更新 `f10` 和 `f21`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.PIPULSEF10
values = "3.193120459017055,3.193120459017055"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 12: optQubitReadFreq

优化比特读取频率，最大化读取保真度。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]
qname = qubit_name_list[0]
fread = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM, qname=qname, key="fread_star")

data = qubit_ctrl_client.run(
    CtrlTaskName.OPTQUBITREADFREQ,
    qubits=qubit_name_list,
    freq_span_center=fread,
    freq_span_half_bandwidth=0.0055,
    freq_span_sample_num=40
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

根据扫描结果，更新 `fread`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.OPTQUBITREADFREQ
values = "6.590"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 13: opt_pipulse

优化 Pi 脉冲幅度和形状，提高门保真度。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.OPTPIPULSE,
    qubits=qubit_name_list,
    N_list=[1, 4, 8],
    amp_list=None
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

根据扫描结果，更新最新 `m=8` 的 `PiGate.amp` 和 `PiGate.alpha`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.OPTPIPULSE
values = "3.193120459017055,3.193120459017055"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 14: TimingXYZ

XY 脉冲时序校准，优化脉冲序列时序。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.TIMINGXYZ,
    qubits=qubit_name_list,
    delay_start=-60,
    delay_end=60,
    delay_sample_num=31
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

根据扫描结果，更新最新 `timing.xy`：

```python
qname = qubit_name_list[0]
task_type = CtrlTaskName.TIMINGXYZ
values = "3.193120459017055"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, qname=qname, task_type=task_type, values=values)
```

---

### 步骤 15: PulseShape

脉冲形状扫描，优化读取脉冲波形。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.PULSESHAPE,
    qubits=qubit_name_list,
    step_height=0.2
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

无更新

---

### 步骤 16: T1

T1 弛豫时间测量。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.T1,
    qubits=qubit_name_list,
    delay_start=0,
    delay_end=80000,
    delay_sample_num=17
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

无更新

---

### 步骤 17: T1_2d

二维 T1 测量，T1 随偏置电压的变化。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.T1_2D,
    qubits=qubit_name_list,
    bias_start=-1.0,
    bias_end=0.4,
    bias_sample_num=71,
    delay_start=0,
    delay_end=80000,
    delay_sample_num=17
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

无更新

---

### 步骤 18: spinecho_T2

自旋回波 T2 测量，比特相位相干时间。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.SPINECHOT2,
    fringeFreq=0.05,
    delay_start=0,
    delay_end=10000,
    delay_sample_num=200
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

无更新

---

### 步骤 19: Ramsey_T2

Ramsey T2 测量，比特相位相干时间。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.RAMSEYT2,
    fringeFreq=0.05,
    delay_start=0,
    delay_end=10000,
    delay_sample_num=100
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

无更新

---

### 步骤 20: xeb

交叉熵基准测试（XEB），测量量子门保真度。

#### 测量调用示例

```python
qubit_name_list = ["q3lu7"]

data = qubit_ctrl_client.run(
    CtrlTaskName.XEB,
    m_start=0,
    m_end=400,
    m_sample_num=10,
    k=30,
    gate="reference",
    tbuffer=0,
    stats=300
)
```

#### 注意事项

1. `qubit_name_list = ["q3lu7"]` 填写当前测试的比特

#### 参数更新

无更新

#### 参数说明

- `k`：不同的随机门序列的个数，多个随机门序列的平均得到一维数据