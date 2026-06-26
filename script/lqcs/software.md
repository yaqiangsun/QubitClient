# 🛠️ 量子测控软件 全流程操作手册

本文档讲解了测控软件的使用，包括如何启动、如何用sq命令采集数据、如何用图形界面查看数据、如何更新参数等详细步骤。


---

## 📑 快速目录
- [🚀 软件启动](#软件启动)
- [⌨️ 数据采集窗口](#数据采集窗口)
- [📊 数据分析窗口](#数据分析窗口)
- [📈 图形查看界面](#图形查看界面)
- [⚙️ 参数修改方法](#参数修改方法)
- [🧪 全套测控实验流程](#全套测控实验流程)



---

## 软件启动
1. 打开终端进入IPython
```bash
ipython
```

2、启动测控服务
```
from lqcs.servers_control import run_server_control
run_server_control()

```

2.触发功能窗口
逐步点开Labrad On等按钮，并观察终端是否报出错误 或 成功提示

## 数据采集窗口
```
cd scriptslqcs/measure_scripts
ipython -i config.py
```

## 数据分析窗口
```
cd lqcs/measure_scripts
ipython -i dp_config.py
```

## 图形查看界面

在功能界面按钮中，点击“Grapher Ready”，可以查看每个hdf5文件中amp、time等信息

## 参数修改方法
方式 1：图形界面

在 retristry 面板直接编辑参数

方式 2：代码指令
```
qobj.regs.fread = 6.661
```
---

## 全套测控实验流程

统一说明：所有实验中 qobj = q3lu7 请替换为当前测试比特

### 1.s21mul
量子比特正式开展实验初始化工作时，首要任务便是精准读取谐振腔的固有共振频率。
我们以器件预设的理论设计频率为中心，划定较宽的频率区间完成全域扫频测试。
测试完成后可得到对应的幅频特性曲线，该曲线能够直观反映信号幅值随扫描频率的变化规律。
由于每一个独立谐振腔都会在曲线上形成明显的吸收波谷，因此波谷与谐振腔一一对应。

#### 数据采集脚本
在数据采集窗口：
```python
sq.s21(qobj, freq=np.arange(6.5, 7.1, 0.001), update=False)
```
#### 数据分析脚本
```python
dataset = 4 # 填写上方产生的hdf5文件编号
dp.findPhaseDiff(data, dataset, qubitNum=12, medfilt_para=15)
```


### 2.s21peak
单比特 S21 扫描，用于“精确”定位比特频率。

#### 数据采集脚本
```python
# 选取更窄的范围，精确定位比特
sq.s21(qobj, freq=np.arange(6.5, 6.6, 0.001), update=False)
```
#### 数据分析脚本
```python
dataset = 5 # 填写上方产生的hdf5文件编号
dp.findPhaseDiff(data, dataset, qubitNum=1, medfilt_para=15)
```


#### ⚡参数更新
```python
qobj.regs.fread = 6.661 或在retristry界面中更改
```

---

### 3.powershift

接下来需开展功率扫描实验，以此确定适配的读取功率参数。
若设置较高的读取功率，读取谐振腔与量子比特之间的耦合作用会大幅减弱，二者近乎处于解耦状态。
该工况下采集到的频率信号，仅能反映读取谐振腔本身的固有裸共振频率。
逐步下调读取功率，实验系统将过渡至典型的色散工作区间，腔与比特的耦合效应开始凸显。
受量子比特能级耦合作用的影响，读取谐振腔的谐振频率会随之产生明显偏移。

#### 数据采集脚本

```python
sq.s21_power2d(qobj, update=False)
```

还需要检查fc_read，|fc_read - fc| < 250 MHz为合适的范围
 

#### ⚡参数更新

若update=True，更新 `ReadIn.power = xx`

---

### 4.s21vflux

比特频率随磁通变化扫描（电压-频率关系）。
目标是测量量子比特频率与外加高速Z控制电压之间的关系。测量完成后可以查看
频率-zpa拟合图。在该拟合曲线上选一点，将该点的读取频率和zpa输出到比特参数的fread和bias_z中。如果zpa2d的测量
结果为直线，则应检查接线和channels，或更换读取腔后重新测量。

#### 数据采集脚本

```python
sq.s21_zpa2d(qobj)
```


#### ⚡参数更新

根据扫描结果，在余弦曲线上选取一点（通常应避开频率的极值点），例如选择 `zpa = -1.5`，更新 `bias_z = -1.5`：

```python
s[qobj.qname]['bias_z'] = -1.5
```


### 5.s21peak

在特定偏置点 (bias_z=-1.5)进行 S21 峰值扫描。

#### 数据采集脚本

```python
sq.s21(qobj, freq=np.arange(6.5, 6.6, 0.001), update=False)
```


#### ⚡参数更新
```python
qobj.regs.fread = 6.661 或在retristry界面中更改
```


---

### 6.spectrum

频谱扫描，测量比特 |0⟩→|1⟩和 |1⟩→|2⟩跃迁频率。
通过XY线给量子比特施加一个特定时长和幅度的微波信号。当微波频率与量子比特频
率共振时，微波信号的振幅、相位等会发生突变。此时将突变点对应的频率
填入比特参数的f10即可

#### 数据采集脚本

```python
sq.spectroscopy(qobj, freq=np.arange(4.0, 3.0, -0.002))
```

#### ⚡参数更新

根据扫描结果，更新 `f10` 和 `f21`：

在数据采集窗口：
```python
设置⽐特的频率为3.5 GHz,⾮线性-0.2 GHz，fc频率为3.65 GHz
qobj.set_f10(3.5, non=-0.2, sb_freq=-0.15)
```

---


### 7.spectrum2d

二维频谱扫描，测量比特频率随偏置电压的变化。

#### 数据采集脚本

```python
sq.spectroscopy(qobj, freq=np.arange(4.0, 3.0, -0.002), zpa=zpa_array, spec_amp=spec_amp, sb_freq=sb_freq,update=False)
```

#### ⚡参数更新

暂不更新参数

---

### 8.singleshot

单发读取测量，测量比特 |0）和 |1） 态的区分度。
设置f10后，可以运行IQ分隔实验查看是否可以区分比特的0态与1态。理想情况下0态与1态的
点云可以很好地分开。

#### 数据采集脚本

```python
sq.iqraw(qobj)
```

#### ⚡参数更新

无参数更新

---


### 9.rabi

Rabi 振荡测量，确定确定将量子比特激发到1态的最佳pi脉冲振幅

#### 数据采集脚本

```python
sq.piamp(qubit, fc=None, amp=amp_array, update=False)
```


#### ⚡参数更新

根据扫描结果，更新 `PiGate.amp`和`PiHalf.amp`

```python
update=True时自动更新
```

---


### 10.PiPulseF10

Pi 脉冲频率校准，测量 |0⟩→|1⟩ 跃迁的精确频率。

#### 数据采集脚本

```python
sq.pidf(qubit, df=df_array, update=False)
```


#### ⚡参数更新

根据扫描结果，更新 `f10` 和 `f21`：

```python
update=True时自动更新
```

---

### 11.ramsey

Ramsey 干涉测量，确定比特退相干时间和频率偏移。和pi脉冲实验相⽐，Ramsey实验可以更精细地调节f10。
在默认的5MHz条纹频率(fringe frequency)下，多次进行Ramsey实验后，得到的震荡周期接近于200ns，即完成f10校准

#### 数据采集脚本

```python
sq.ramsey_df(qubit, 
            delay=delay_array,
            fringeFreq=fringeFreq,
            update=False)

```


#### ⚡参数更新

根据扫描结果，更新 `f10` 和 `f21`：

```python
update=True时自动更新
```

---

### 12.optQubitReadFreq

优化比特读取频率，最大化读取保真度。
在色散区间，当量子比特处于不同能量本征态时，谐振腔的频率会发生相应变化。通过扫描两条
S21曲线，计算二者的复数差值模，本实验的目标参数是曲线最高点对
应的读取频率，在此处可以得到最大的IQ分隔。

#### 数据采集脚本

```python
sq.s21_dis(qubit, freq_span=freq_span, update=False)
```

#### ⚡参数更新

根据扫描结果，更新 `fread`：

```python
update=True时自动更新
```


---

### 13.setPiAlpha

优化 Pi 脉冲幅度和形状，提高门保真度。
多次重复施加pi脉冲是微调pi脉冲振幅和相位参数的有效方法。

#### 数据采集脚本

```python
sq.set_pi(qobj, gate='X') # Pi 脉冲（对应X⻔操作）参数调整
 
sq.set_pi(qobj, gate='X/2') # Pi/2 脉冲（对应X/2⻔操作）参数调整

```

#### ⚡参数更新

根据扫描结果，更新最新 `m=8` 的 `PiGate.amp` 和 `PiGate.alpha`：

```python
update=True时自动更新
```


---

### 14.TimingXYZ

XY 脉冲时序校准，优化脉冲序列时序。
由不同的微波设备发出的控制信号在抵达量子比特时可能存在时间差。为了增强多量子比特系统调控的
同步性，需要调整微波设备发射信号的延迟时间。本实验在单个量子比特上分别施加一个pi脉冲和一个相
等时长的Z偏置电压脉冲，调节后者的起始时间并测量1态概率。当两脉冲重合时，量子比特无法激
发，由此可调节它们的时间差。将update项设置为xy和z，可以分别更新timing-xy和timing-z两个参
数。

#### 数据采集脚本

```python
sq.test_timing_xyz(qubit, delay=delay_array, zpa=zpa, update=False)
```

#### ⚡参数更新

根据扫描结果，更新最新 `timing.xy` 和 `timing.z`：

```python
update=True时自动更新
```

---

### 15.PulseShape

脉冲形状扫描，优化读取脉冲波形。在进行CZXEB实验前需要进行脉冲形状实验。

#### 数据采集脚本

```python
step_height = 0.2 
# 进行脉冲形状测试的时候，所用脉冲幅度。最好与之后进行CZ实验的值接近
sq.pulse_shape(qubit, step_height=step_height, update=False)
```

#### ⚡参数更新

在数据分析窗口中：
```python
from lqms.data_process.pulse_shape import process_pulse_shape
dataset = 4 # 实验结果对应数据编号
data.loadDataset(dataset)
process_pulse_shape.pulse_shape(data)

```

---

### 16.T1

T1 弛豫时间测量。先将比特激发到1态，然后等待不同的时间后测量其处于1态的概率。比特处于1态的概率会呈指数衰减

#### 数据采集脚本

```python
sq.t1(qubit,
      delay=delay_array,
      update=False)
```


#### ⚡参数更新

无更新

---

### 17.T1_2d

二维 T1 测量，T1 随偏置电压的变化。

#### 数据采集脚本

```python
sq.t1(qubit, 
      zpa=zpa_array,
      delay=delay_array,
      update=False)
```


#### ⚡参数更新

在数据分析窗口中：
```python
dataset = 4 # 对应数据编号
 
qter.fitData(dataset, update=True)

#如果是⼀维改变频率
data.load(dataset)
dp.T1_snake_error_model(data,info)

```
---

### 18.spinecho_T2

自旋回波 T2 测量，比特相位相干时间。自旋回波(spin echo)方法同Ramsey方法相比，排除了静态不均匀展宽效应，可以测得更长的
T2。如果设置π脉冲的数量m>1，可进行CPMG实验，更有效地抑制低频噪声，延长相干时间。

#### 数据采集脚本

```python
sq.spinecho_t2(qubit, 
              delay=delay_array,
              fringeFreq=fringeFreq,
              ms=ms,
              update=False)
```


#### ⚡参数更新

无更新

---

### 19.Ramsey_T2

Ramsey T2 测量，比特相位相干时间。实验首先先将量子比特制备到|0>-i|1>态，等待特定时间后，绕与X轴成θ角的轴将量子态旋转π/2角
度，最后测量|1>态概率。另外设置θ角对等待时间的变化而线性变化。将实验数据的包络曲线进行拟合，可以推算出T2*的大小。

#### 数据采集脚本

```python
sq.ramsey_t2(qubit, 
                    delay=delay_array,
                    fringeFreq=fringeFreq,
                    update=False)
```


#### ⚡参数更新

无更新


---

### 20.xeb

交叉熵基准测试（XEB），测量量子门保真度。它通过执行随机的单比特门序列，比较实验测量结果与理论预测之间的交叉熵，计算随机门的平
均保真度。如果在实验参数的gate选项中选择reference以外的其他门，则计算随机门+特定门的平均
保真度。实验参数中的k表示不同的随机⻔序列的个数，m表示电路深度，tbuffer表示在量子们操作之
间插入的延迟时间。

#### 数据采集脚本

```python
sq.xeb(qubit, m=m_array, k=k, gate=gate, tbuffer=tbuffer, stats=stats)
```

#### ⚡参数更新
在数据分析窗口中：
```python
dataset = 4 # 对应数据编号
px.XEB(data, [dataset])
# 如需检查退相⼲，T2等造成的影响，可以运⾏
px.XEB_and_SPB(data, [dataset])
```

#### 参数说明

- `k`：不同的随机门序列的个数，多个随机门序列的平均得到一维数据