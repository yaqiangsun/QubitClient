# 参数更新列表

本文件汇总了所有的参数更新和查询操作。

---

## 一、更新参数列表

### 1. gate.Measure.* 参数

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `gate.Measure.{q}.params.frequency` | float | 测量频率 | S21_template.py, S21_template_2d.py, S21_optf.py, opt_readf_bias.py, opt_read_power_freq.py |
| `gate.Measure.{q}.params.amp` | float | 测量幅度 | opt_read_power.py, opt_read_power_freq.py |
| `gate.Measure.{q}.params.bias` | float | 测量偏置 | opt_readf_bias.py, initialization.py |
| `gate.Measure.{q}.params.duration` | float | 测量脉宽 | initialization.py |
| `gate.Measure.{q}.params.space` | float | 测量间隔 | initialization.py |
| `gate.Measure.{q}.params.ring_up_amp` | float | 环振幅 | initialization.py |
| `gate.Measure.{q}.params.ring_up_time` | float | 环时间 | initialization.py |
| `gate.Measure.{q}.params.buffer` | float | 缓冲 | initialization.py |
| `gate.Measure.{qubit}.params.threshold` | float | 阈值 | singleshot_after_read.py, singleshot_check.py, singleshot_single_pulse.py, singleshot_template.py |
| `gate.Measure.{qubit}.params.phi` | float | 相位 | singleshot_after_read.py, singleshot_check.py, singleshot_single_pulse.py, singleshot_template.py |
| `gate.Measure.{qubit}.params.signal` | str | 信号类型 | singleshot_after_read.py, singleshot_check.py, singleshot_single_pulse.py, singleshot_template.py |
| `gate.Measure.{qubit}.params.PgPe` | list | PgPe | singleshot_after_read.py, singleshot_check.py, singleshot_single_pulse.py, singleshot_template.py |

### 2. gate.R.* 参数

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `gate.R.{q}.params.frequency` | float | 驱动频率 | spectrum.py, spectrum_amplist.py, spectrum_drive_amp.py, ramsey_template.py, spin_echo.py |
| `gate.R.{q}.params.amp` | float | 驱动幅度 | G3/Rabi.py, opt_pipulse.py, rabi_coupler_bias.py, rabi_in_group.py, rabi_in_group_time.py, rabi_population.py, rabi_single_pulse.py |
| `gate.R.{q}.params.width` | float | 脉宽 | G3/Rabi.py, rabi_coupler_bias.py, rabi_in_group.py, rabi_in_group_time.py, rabi_population.py, rabi_single_pulse.py |
| `gate.R.{q}.params.beta` | float | DRAG beta | allxy_drag.py |
| `gate.R.{q}.params.delta` | float | delta | opt_delta.py |
| `gate.R.{q}.fidelity` | float | 门保真度 | rb_1q.py |

### 3. gate.CZ.* 参数

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `gate.CZ.{q}_{q1}.fidelity` | float | CZ门保真度 | rb_CZ.py |

### 4. gate.{gateType}.* 参数 (双比特门)

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `gate.{gateType}.{q}_{q1}.params.{arg}` | float | 双比特门参数 | cphase_2d.py, cphase_2d_amp.py |
| `gate.iSWAP.{q}_{q1}.params.{args}` | float | iSWAP门参数 | iSWAP_align.py |

### 5. measure.* 参数

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `measure.caliMatrix.{arg}` | array | 校准矩阵 | coread.py, coread_all.py |
| `measure.all_qubits` | list | 所有量子比特 | initialization.py |
| `measure.all_couplers` | list | 所有耦合器 | initialization.py |
| `measure.qubits_use` | list | 使用中的量子比特 | initialization.py |
| `measure.couplers_use` | list | 使用中的耦合器 | initialization.py |

### 6. {q} 类参数

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `{q}.biaslst.idle_bias` | float | 空闲偏置 | initialization.py, zz_coupling.py |
| `{q}.biaslst.iso_bias` | float | 隔离偏置 | initialization.py, zz_coupling.py |
| `{q}.biaslst.read_bias` | float | 读取偏置 | initialization.py |
| `{q}.waveform.LEN` | int | 波形长度 | initialization.py |
| `{q}.params.fread_idle` | float | 空闲读取频率 | fread_idle.py |
| `{q}.params.T1` | float | T1时间 | t1_1d.py |
| `{q}.params.T2_star` | float | T2*时间 | ramsey_template.py, spin_echo.py |
| `{q}.s21params` | dict | S21参数 | S21vsflux.py, S21vsflux_c.py, S21vsflux_scan.py, powershift.py |
| `{q}.calibration.Z.distortion.expfit` | dict | Z失真拟合 | distortion_q.py |

### 7. {c} 类参数 (耦合器)

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `{c}.biaslst.idle_bias` | float | 空闲偏置 | initialization.py |
| `{c}.biaslst.iso_bias` | float | 隔离偏置 | initialization.py |
| `{c}.biaslst.read_bias` | float | 读取偏置 | initialization.py |
| `{c}.waveform.LEN` | int | 波形长度 | initialization.py |
| `{cpls}.calibration.Z.distortion.expfit` | dict | Z失真拟合 | distortion_c.py |
| `{cpls}.specparams.voffset` | float | 频谱偏移 | qc_iSWAP.py |

### 8. {k} 类参数 (通用键)

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `{k}.calibration.Z.delay` | float | Z延迟 | qc_timing_compute.py, XYZ_Timing.py |
| `{k}.calibration.DDS.delay` | float | DDS延迟 | qc_timing_compute.py |

### 9. M{m} 类参数

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `M{m}.waveform.LEN` | int | 波形长度 | initialization.py |

### 10. legacy.* 参数

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `legacy.rabi[{q}]` | dict | Rabi校准状态 | G3/Rabi.py, rabi_coupler_bias.py, rabi_in_group.py, rabi_in_group_time.py, rabi_population.py, rabi_single_pulse.py |
| `legacy.rb_sq.{q}.err` | float | 单比特RB误差 | rb_1q.py |
| `legacy.rb_sq.{q}.A` | float | 单比特RB参数A | rb_1q.py |
| `legacy.rb_sq.{q}.B` | float | 单比特RB参数B | rb_1q.py |
| `legacy.rb_sq.{q}_{q1}.err` | float | 双比特RB误差 | rb_CZ.py |
| `legacy.rb_sq.{q}_{q1}.A` | float | 双比特RB参数A | rb_CZ.py |
| `legacy.rb_sq.{q}_{q1}.B` | float | 双比特RB参数B | rb_CZ.py |
| `legacy.rb_tq.{q}_{q1}.err` | float | 双比特RB误差(真) | rb_CZ.py |
| `legacy.rb_tq.{q}_{q1}.ref` | float | 双比特RB参考值 | rb_CZ.py |
| `legacy.singleshot.{qubit}.v` | float | 单发测量v | singleshot_check.py, singleshot_single_pulse.py, singleshot_template.py |
| `legacy.singleshot.{qubit}.ready` | bool | 单发测量就绪 | singleshot_check.py, singleshot_single_pulse.py, singleshot_template.py |
| `legacy.spectrum[{q}]` | dict | 频谱校准 | spectrum.py, spectrum_amplist.py, spectrum_drive_amp.py |

### 11. results.* 参数

| 参数路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `results.{name}.{couplers[i]}.z_leakage` | float | Z泄漏 | leakage_CZ.py, leakage_CZ_amp.py |
| `results.{name}.{q}_{cpls}.others` | list | 其他结果 | phase_mapping_c.py, phase_mapping_distortion.py |
| `results.{name}.{q}_{cpls}.func` | list | 函数参数 | phase_mapping_c.py, phase_mapping_distortion.py |
| `results.{name}.{q}.others` | list | 其他结果 | phase_mapping_q.py |
| `results.{name}.{q}.func` | list | 函数参数 | phase_mapping_q.py |
| `results.{name}.{(q,c)}` | float | (q,c)结果 | qc_timing.py |

---

## 二、查询参数列表 (config['gate'][...]['params'][...])

### 1. gate.Measure.* 查询

| 查询路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `config['gate']['Measure'][q]['params']['frequency']` | float | 测量频率 | S21_template.py, S21_template_2d.py, S21_optf.py, S21vsflux.py, S21vsflux_c.py, S21vsflux_scan.py, powershift.py, opt_readf_bias.py, opt_read_power.py, opt_read_power_freq.py, G3/S21.py, G3/S21_flux.py, fread_idle.py |
| `config['gate']['Measure'][q]['params']['amp']` | float | 测量幅度 | S21vsflux.py, S21vsflux_c.py, S21vsflux_scan.py, powershift.py, opt_read_power.py |
| `config['gate']['Measure'][q]['params']['bias']` | float | 测量偏置 | opt_readf_bias.py |
| `config['gate']['Measure'][q]['params']['PgPe']` | list | PgPe值 | factoring_143_391_yhs_get_energy.py, factoring_yhs_get_energy.py, factoring_yhs_repeat.py, factoring_143_391_yhs_repeat.py, jpa/jpa_opt.py |

### 2. gate.R.* 查询

| 查询路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `config['gate']['R'][q]['params']['frequency']` | float | 驱动频率 | spectrum.py, spectrum_2d.py, spectrum_2d_ai.py, spectrum_2d_amplist.py, spectrum_2d_cq_tmplt.py, spectrum_2d_c_bias.py, spectrum_amplist.py, spectrum_drive_amp.py, ramsey_template.py, spin_echo.py, zz_coupling.py, G3/spectrum1d.py |
| `config['gate']['R'][q]['params']['amp']` | float | 驱动幅度 | opt_pipulse.py |
| `config['gate']['R'][q]['params']['delta']` | float | delta | opt_delta.py |
| `config['gate']['R'][q]['params']['beta']` | float | DRAG beta | allxy_drag.py |

### 3. gate.{gateType}.* 查询 (双比特门)

| 查询路径 | 类型 | 说明 | 使用模板 |
|---------|------|------|---------|
| `config['gate'][gateType][f'{q}_{q1}']['params'][...]` | float | 双比特门参数 | cphase_2d.py, cphase_2d_amp.py, opt_ampc_CZ_pt.py, opt_dphase_CZ_pt.py, qpt_CZ.py, iSWAP_align.py |

---

## 三、参数模式汇总

### 固定格式参数
```
gate.Measure.{q}.params.frequency
gate.Measure.{q}.params.amp
gate.Measure.{q}.params.bias
gate.Measure.{q}.params.duration
gate.Measure.{q}.params.space
gate.Measure.{q}.params.ring_up_amp
gate.Measure.{q}.params.ring_up_time
gate.Measure.{q}.params.buffer
gate.Measure.{qubit}.params.threshold
gate.Measure.{qubit}.params.phi
gate.Measure.{qubit}.params.signal
gate.Measure.{qubit}.params.PgPe

gate.R.{q}.params.frequency
gate.R.{q}.params.amp
gate.R.{q}.params.width
gate.R.{q}.params.beta
gate.R.{q}.params.delta
gate.R.{q}.fidelity

gate.CZ.{q}_{q1}.fidelity
gate.iSWAP.{q}_{q1}.params.{args}
gate.{gateType}.{q}_{q1}.params.{arg}

measure.caliMatrix.{arg}
measure.all_qubits
measure.all_couplers
measure.qubits_use
measure.couplers_use

{q}.biaslst.idle_bias
{q}.biaslst.iso_bias
{q}.biaslst.read_bias
{q}.waveform.LEN
{q}.params.fread_idle
{q}.params.T1
{q}.params.T2_star
{q}.s21params
{q}.calibration.Z.distortion.expfit

{c}.biaslst.idle_bias
{c}.biaslst.iso_bias
{c}.biaslst.read_bias
{c}.waveform.LEN
{cpls}.calibration.Z.distortion.expfit
{cpls}.specparams.voffset

{k}.calibration.Z.delay
{k}.calibration.DDS.delay

M{m}.waveform.LEN

legacy.rabi[{q}]
legacy.rb_sq.{q}.err
legacy.rb_sq.{q}.A
legacy.rb_sq.{q}.B
legacy.rb_sq.{q}_{q1}.err
legacy.rb_sq.{q}_{q1}.A
legacy.rb_sq.{q}_{q1}.B
legacy.rb_tq.{q}_{q1}.err
legacy.rb_tq.{q}_{q1}.ref
legacy.singleshot.{qubit}.v
legacy.singleshot.{qubit}.ready
legacy.spectrum[{q}]

results.{name}.{couplers[i]}.z_leakage
results.{name}.{q}_{cpls}.others
results.{name}.{q}_{cpls}.func
results.{name}.{q}.others
results.{name}.{q}.func
results.{name}.{(q,c)}
```

### 查询配置对应关系
```
config['gate']['Measure'][q]['params']['frequency']  <->  gate.Measure.{q}.params.frequency
config['gate']['Measure'][q]['params']['amp']        <->  gate.Measure.{q}.params.amp
config['gate']['Measure'][q]['params']['bias']       <->  gate.Measure.{q}.params.bias
config['gate']['Measure'][q]['params']['PgPe']       <->  gate.Measure.{q}.params.PgPe

config['gate']['R'][q]['params']['frequency']        <->  gate.R.{q}.params.frequency
config['gate']['R'][q]['params']['amp']              <->  gate.R.{q}.params.amp
config['gate']['R'][q]['params']['delta']            <->  gate.R.{q}.params.delta
config['gate']['R'][q]['params']['beta']             <->  gate.R.{q}.params.beta

config['gate'][gateType][f'{q}_{q1}']['params'][...] <->  gate.{gateType}.{q}_{q1}.params.{...}
```