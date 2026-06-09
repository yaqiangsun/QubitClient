# 测量实验接口文档
本文档以pipeline/**_pipeline.py脚本，以及比特q3lu7为例，讲解所有任务的测量实验部分接口与调用实例，分析与绘图部分参考docs/nnscope docs/nnscope
## 测量实验顺序

s21mul s21peak powershift s21vflux s21peak(bias_z=-1.5) spectrum spectrum2d singleshot rabi PiPulseF10 
ramsey optQubitReadFreq opt_pipulse(X) TimingXYZ PulseShape T1 T1_2d spinecho_T2 Ramsey_T2 xeb

## 测量实验步骤1 s21mul
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```

### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]
  data = qubit_ctrl_client.run(CtrlTaskName.S21MULTI,
                                  qubits=qubit_name_list,
                                  frequency_start=6.5,
                                  frequency_end=6.9,
                                  frequency_sample_rate=0.0001)
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特
2. 对照图片，确认q3lu7的频率与图中一致


### 参数更新

根据扫描结果，更新fread = 6.590  
```python                                  
    qname=qubit_name_list[0]
    task_type=CtrlTaskName.S21MULTI
    values="6.590"
    qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)
```




## 测量实验步骤2 s21peak
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]
  fread = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM, key="fread_star")
  data = qubit_ctrl_client.run(CtrlTaskName.S21,
                                    qubits=qubit_name_list,
                                    frequency_center=fread,
                                    frequency_half_bandwidth=0.005,
                                    frequency_sample_num=100)
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特

### 参数更新

根据扫描结果，更新fread = 6.5898  
```python                                  
qname=qubit_name_list[0]
    task_type=CtrlTaskName.S21PEAK
    values="6.590"   
    qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)
```

qobj.regs.fread = 6.5898


## 测量实验步骤3 powershift
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]
  qname=qubit_name_list[0]
  task_type=CtrlTaskName.POWERSHIFT
  fread = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM,qname=qname, key="fread_star")
    
  data = qubit_ctrl_client.run(CtrlTaskName.POWERSHIFT,
                                qubits=qubit_name_list,
                                frequency_center=fread,
                                frequency_half_bandwidth=0.0015,
                                frequency_sample_num=16，
                                power_start=-40,
                                power_end=-16,
                                power_sample_num=13
                                )
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特

### 参数更新

根据扫描结果，更新ReadIn.power=-30  
```python                                  
qname=qubit_name_list[0]
    task_type=CtrlTaskName.POWERSHIFT
    values="-30"   
    qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)
```


## 测量实验步骤4 s21vflux
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]
  
    qname=qubit_name_list[0]
    task_type=CtrlTaskName.S21VSFLUX
    fread = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM,qname=qname, key="fread_star")
    
  data = qubit_ctrl_client.run(CtrlTaskName.S21VSFLUX,
                                    qubits_scan=qubit_name_list,
                                    freq_center=fread,
                                    freq_half_bandwidth=0.001,
                                    freq_sample_num=11，
                                    read_bias_start=-3,
                                    read_bias_end=3,
                                    read_bias_sample_num=16)
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特

### 参数更新

根据扫描结果，在余弦曲线上选⼀点,通常应避开频率的极值点，例如选择zpa=-1.5，更新bias_z = -1.5 
```python                                  
qname=qubit_name_list[0]
    task_type=CtrlTaskName.S21VSFLUX
    values="-1.5"   
    qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values) 
    ```


## 测量实验步骤5 s21peak
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]
  fread = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM,qname=qname, key="fread_star")

  data = qubit_ctrl_client.run(CtrlTaskName.S21,
                                    qubits=qubit_name_list,
                                    frequency_center=fread,
                                    frequency_half_bandwidth=0.005,
                                    frequency_sample_num=100)
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新

根据扫描结果，更新fread = 6.5896 
```python                                  
qname=qubit_name_list[0]
task_type=CtrlTaskName.S21PEAK
values="6.5896"  
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)

```





## 测量实验步骤6 spectrum
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]

  data = qubit_ctrl_client.run(CtrlTaskName.SPECTRUM,
                                   qubits=qubit_name_list,
                                   freq_start=-3,
                                   freq_end=3,
                                   freq_sample_num=200,
                                   bias=0,
                                   drive_amp=0.0)
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新

根据扫描结果，更新f10,f21
```python                                  
qname=qubit_name_list[0]
task_type=CtrlTaskName.SPECTRUM
values="3.193120459017055,3.193120459017055"   
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)

```



## 测量实验步骤7 spectrum2d
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]
  data = qubit_ctrl_client.run(CtrlTaskName.SPECTRUM_2D,
                                   qubits=qubit_name_list,
                                   freq_start=-3,
                                   freq_end=3,
                                   freq_sample_num=200,
                                   bias_start=-1,
                                   bias_end=1,
                                   bias_sample_num=200,
                                   drive_amp=0.0)
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新

根据扫描结果，更新f10,f21
```python                                  
qname=qubit_name_list[0]
task_type=CtrlTaskName.SPECTRUM_2D
values="3.193120459017055,3.193120459017055"   
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)

```


## 测量实验步骤8 singleshot
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]

  data = qubit_ctrl_client.run(CtrlTaskName.SINGLESHOT,
                                   qubits=qubit_name_list
                                   )
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新

无参数更新




## 测量实验步骤9 rabi
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]
 16
  data = qubit_ctrl_client.run(CtrlTaskName.RABI,
                                  fc=None, 
                                  amp_start=0,
                                  amp_end=2,
                                  amp_sample_num=16)
                              
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新


根据扫描结果，更新PiGate.amp
```python                                  
 qname=qubit_name_list[0]
  task_type=CtrlTaskName.RABI
  values="1.0670387859748918"   
  qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)

```






## 测量实验步骤10 PiPulseF10
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]
 
  data = qubit_ctrl_client.run(CtrlTaskName.PIPULSEF10,
                                   qubits=qubit_name_list,
                                   df_start=0,
                                   df_end=0.03,
                                   df_sample_num=21)
                              
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新


根据扫描结果，更新f10,f21
```python                                  
qname=qubit_name_list[0]
task_type=CtrlTaskName.PIPULSEF10
values="3.193120459017055,3.193120459017055"   
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)

```

## 测量实验步骤11 ramsey
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```pythonW
  qubit_name_list = ["q3lu7"]




  data = qubit_ctrl_client.run(CtrlTaskName.RAMSEY,
                                   qubits=qubit_name_list,
                                   delay_start=0,
                                  delay_end=100,
                                  delay_sample_num=100,
                                  fringeFreq=0.05
                                   )
                              
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新


根据扫描结果，更新f10,f21
```python                                  
qname=qubit_name_list[0]
task_type=CtrlTaskName.PIPULSEF10
values="3.193120459017055,3.193120459017055"   
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)

```




## 测量实验步骤12 optQubitReadFreq
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]


  fread = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM,qname=qname,key="fread_star")
    
  data = qubit_ctrl_client.run(CtrlTaskName.OPTQUBITREADFREQ,
                                  qubits=qubit_name_list,
                                  freq_span_center=fread,
                                  freq_span_half_bandwidth=0.0055,
                                  freq_span_sample_num=40) 

                              
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新


根据扫描结果，更新fread
```python                                  
qname=qubit_name_list[0]
task_type=CtrlTaskName.OPTQUBITREADFREQ
values="6.590"   
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)

```



## 测量实验步骤13 opt_pipulse
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]

 data = qubit_ctrl_client.run(CtrlTaskName.OPTPIPULSE,
                                   qubits=qubit_name_list,
                                   N_list=[1,4,8],
                                   amp_list=None)
                              
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新


根据扫描结果，更新最新m=8的，PiGate.amp  PiGate.alpha
```python                                  
qname=qubit_name_list[0]
task_type=CtrlTaskName.OPTPIPULSE
values="3.193120459017055,3.193120459017055"   
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)
```



## 测量实验步骤14 TimingXYZ
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]



  data = qubit_ctrl_client.run(CtrlTaskName.TIMINGXYZ,
                                   qubits=qubit_name_list,
                                   delay_start=-60,
                                   delay_end=60,
                                   delay_sample_num=31)
                              
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新


根据扫描结果，更新最新timing.xy
```python                                  
qname=qubit_name_list[0]
task_type=CtrlTaskName.TIMINGXYZ
values="3.193120459017055"
qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)
```





## 测量实验步骤15 PulseShape
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]



  data = qubit_ctrl_client.run(CtrlTaskName.PULSESHAPE,
                                   qubits=qubit_name_list,
                                   step_height=0.2
                                   )
                              
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新

无更新




## 测量实验步骤16 T1
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]



 data = qubit_ctrl_client.run(CtrlTaskName.T1,
                                   qubits=qubit_name_list,
                                   delay_start=0,
                                   delay_end=80000,
                                   delay_sample_num=17)
                              
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新

无更新



## 测量实验步骤16 T1_2d
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]

 data = qubit_ctrl_client.run(CtrlTaskName.T1_2D,
                                   qubits=qubit_name_list,
                                   bias_start=-1.0,
                                   bias_end=0.4,
                                   bias_sample_num=71,
                                   delay_start=0,
                                   delay_end=80000,
                                   delay_sample_num=17)
                              
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新

无更新


## 测量实验步骤17 spinecho_t2
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]


  data = qubit_ctrl_client.run(CtrlTaskName.SPINECHOT2,
                                  fringeFreq=0.05
                                   delay_start=0,
                                   delay_end=10000,
                                   delay_sample_num=200
                                   )
                              
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新

无更新



## 测量实验步骤18 Ramsey_T2
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]


  data = qubit_ctrl_client.run(CtrlTaskName.RAMSEYT2,
                                  fringeFreq=0.05
                                   delay_start=0,
                                   delay_end=10000,
                                   delay_sample_num=100
                                   )
                              
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新

无更新







## 测量实验步骤19 xeb
### 测量初始化
```python
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
qubit_ctrl_client = QubitCtrlClient()
```
调用示例
### 测量调用示例
```python
  qubit_name_list = ["q3lu7"]


  data = qubit_ctrl_client.run(CtrlTaskName.XEB,
                                   m_start=0,
                                   m_end=400,
                                   m_sample_num=10,
                                    k=30, 
                                    gate='reference', 
                                    tbuffer=0, 
                                    stats=300
                                   )
                              
  data_id = data[0]["text"]
  data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)
```

### 注意事项
1. qubit_name_list = ["q3lu7"] 填写当前测试的比特，切勿填写其他比特


### 参数更新

无更新

参数中的k表⽰不同的随机⻔序列的个数,多个随机门序列的平均得到1维数据
