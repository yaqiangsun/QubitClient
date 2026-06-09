# 参数更新列表

本文件汇总了所有的参数更新和查询操作。

---
## 一、更新参数列表

### 1. {qname}.regs.* 参数

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `{qname}.regs.fread` | float | 测量⽐特频率 | s21.py, s21mul.py, optqubitreadfreq.py, opt_readf_bias.py, opt_read_power_freq.py |
| `{qname}.regs.bias_z` | float | ⾼速偏置 | s21vflux.py |
| `{qname}.regs.f10` | float | |0⟩ → |1⟩ 的共振频率，即量子比特的工作频率 | spectrum.py, spectrum_2d.py, pipulsef10.py, ramsey.py |
| `{qname}.regs.f21` | float | |1⟩ → |2⟩ 的共振频率，用于表征能级非谐性 | spectrum.py, spectrum_2d.py, pipulsef10.py, ramsey.py |


### 2. {qname}.regs.PiGate.* 参数

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `{qname}.regs.PiGate.amp` | float | π脉冲幅度 | rabi.py, opt_pipulse.py |
| `{qname}.regs.PiGate.alpha` | float | 脉冲包络参数（或 DRAG 系数） | opt_pipulse.py |


### 2. {qname}.regs.timing.* 参数

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `{qname}.regs.timing.xy` | float | XY 门脉冲时长 | timingxyz.py |

---

## 二、查询参数注册表

### 1. {qname}.regs.* 查询

| 查询代码 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `{qname}.regs.fread` | float | 测量⽐特频率 | s21.py, s21mul.py, optqubitreadfreq.py, opt_readf_bias.py, opt_read_power_freq.py |
| `{qname}.regs.bias_z` | float | ⾼速偏置 | s21vflux.py |
| `{qname}.regs.f10` | float | |0⟩ → |1⟩ 的共振频率，即量子比特的工作频率 | spectrum.py, spectrum_2d.py, pipulsef10.py, ramsey.py |
| `{qname}.regs.f21` | float | |1⟩ → |2⟩ 的共振频率，用于表征能级非谐性 | spectrum.py, spectrum_2d.py, pipulsef10.py, ramsey.py |


### 2. {qname}.regs.PiGate.* 查询

| 查询代码 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `{qname}.regs.PiGate.amp` | float | π脉冲幅度 | rabi.py, opt_pipulse.py |
| `{qname}.regs.PiGate.alpha` | float | 脉冲包络参数（或 DRAG 系数） | opt_pipulse.py |


### 2. {qname}.regs.timing.* 查询

| 查询代码 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `{qname}.regs.timing.xy` | float | XY 门脉冲时长 | timingxyz.py |
---

## 三、参数模式汇总
### 固定格式参数
```
{qname}.regs.fread
{qname}.regs.bias_z
{qname}.regs.f10
{qname}.regs.f21
{qname}.regs.PiGate.amp
{qname}.regs.PiGate.alpha
{qname}.regs.timing.xy
```