---
name: qubit_analysis
description: "Quantum experiment data NUMERICAL analysis with support for parameter fitting tasks including: (1) S21 peak detection, (2) Optimal π-pulse calibration, (3) Rabi oscillation analysis, (4) T1/T2 relaxation time fitting, (5) DRAG pulse optimization, (6) Power shift characterization, (7) Ramsey fringe analysis, (8) Single-shot readout fidelity, and (9) 2D spectrum analysis. Provides unified API for curve fitting, parameter extraction, and batch processing with matplotlib/plotly visualization support"
license: Proprietary. LICENSE.txt has complete terms
---

## qubit_analysis vs qubit_vlm

**qubit_analysis** (数值分析):
- 输入: **原始数据** (x, y数组) - 测量数据
- 方法: 数值计算、曲线拟合、峰值检测
- 任务: S21峰值检测、T1/T2拟合、DRAG优化、单比特门校准
- 输出: 数值参数、峰值位置、拟合曲线

**qubit_vlm** (视觉分析):
- 输入: **图像** (PNG, JPG等) - 实验结果图
- 方法: VLM多模态模型 (GPT-4o, Claude等)
- 任务: 描述图表、分析数据质量、评估拟合效果、推理科学意义
- 输出: 文本分析、质量评估、参数判断

典型工作流: `qubit_analysis` → 数值拟合 → 绘图 → `qubit_vlm` → 质量评估

## API Reference

### Client Initialization

```python
# Scope tasks (curve fitting & analysis)
from qubitclient import QubitScopeClient, TaskName
client = QubitScopeClient(url="http://server:port", api_key="your-key")

# NNScope tasks (neural network based analysis)
from qubitclient import QubitNNScopeClient, NNTaskName, CurveType
client = QubitNNScopeClient(url="http://server:port", api_key="your-key")
```

### Task Names

#### Scope Tasks (TaskName)
- `S21PEAK` - Single peak detection with confidence score
- `S21PEAKMULTI` - Multi-peak detection across full frequency range
- `OPTPIPULSE` - Optimal π-pulse calculation
- `RABICOS` - Rabi oscillation cosine first peak detection
- `RAMSEY` - Ramsey fringe decay oscillation fitting
- `S21VFLUX` - S21 vs Flux analysis
- `SINGLESHOT` - Single-shot readout analysis
- `SPECTRUM` - Frequency spectrum analysis
- `T1FIT` - T1 relaxation time exponential fitting
- `T2FIT` - T2 coherence time fitting
- `SPECTRUM2D` - 2D spectrum curve segmentation
- `POWERSHIFT` - Power shift curve analysis
- `DRAG` - DRAG anti-crossing point analysis
- `RB` - Randomized benchmarking fidelity test
- `DELTA` - Delta optimization experiment

#### NNScope Tasks (NNTaskName)
- `SPECTRUM2D` - 2D spectrum data segmentation (supports COSINE, POLY curve types)
- `S21VFLUX` - S21 vs Flux parameter curve segmentation
- `POWERSHIFT` - Power shift curve segmentation
- `SPECTRUM` - Spectrum analysis
- `S21PEAK` - S21 peak detection

### Data Input Formats

The input data should be a dictionary or list of dictionaries with the following structure:

```python
dict_list = [{
    "image": {
        "Q0": (x_data, y_data),  # or (x_data, y_data, z_data) for 2D
        "Q1": (x_data, y_data),
    }
}]
```

### Task-Specific Input Formats

#### S21PEAK / S21PEAKMULTI (Scope)
Input format for S21 peak detection:
```python
{
    "image": {
        "Q0": (x_array, amp_array, phi_array),  # (freq, amplitude, phase)
        "Q1": (x_array, amp_array, phi_array),
    }
}
```
- `x_array`: 1D frequency array
- `amp_array`: 1D amplitude array (magnitude of complex S21)
- `phi_array`: 1D phase array (unwrapped, detrended)

#### OPTPIPULSE
Input format:
```python
{
    "image": {
        "Q0": (waveforms, x_array),  # (2D waveform data, 1D amp axis)
    }
}
```
- `waveforms`: 2D array of shape (n_rows, n_amps)
- `x_array`: 1D array of amplitude values

Supported data keys: `population`, `iq_avg`, `iq`

#### T1FIT
Input format:
```python
{
    "image": {
        "Q0": (delay_array, population_array),  # (time delays, measured populations)
    }
}
```
- `delay_array`: 1D array of delay times (seconds)
- `population_array`: 1D array of measured population values

Supported data keys: `population`, `iq_avg`, `iq`

#### T2FIT / RAMSEY
Same format as T1FIT:
```python
{
    "image": {
        "Q0": (delay_array, population_array),
    }
}
```

#### DRAG
Input format:
```python
{
    "image": {
        "Q0": (lamb_array, y0y1_array),  # (lambda parameter, 2D population data)
    }
}
```
- `lamb_array`: 1D array of DRAG λ values
- `y0y1_array`: 2D array of shape (2, n_lambda) for both states

#### DELTA
Same as DRAG format, but with inverted amplitude (for valley detection):
```python
{
    "image": {
        "Q0": (amp_array, y0y1_array),
    }
}
```

#### RABICOS
Input format:
```python
{
    "image": {
        "Q0": (x_array, amp_array),  # (drive amplitude, amplitude)
    }
}
```
- `x_array`: 1D array of drive amplitude values
- `amp_array`: 1D array of measured amplitude

#### S21VFLUX (Scope)
Input format:
```python
{
    "image": {
        "Q0": (volt_array, freq_array, s21_matrix),
    }
}
```
- `volt_array`: 1D array of voltage/bias values
- `freq_array`: 1D array of frequency values
- `s21_matrix`: 2D array of S21 values (shape: [n_freq, n_volt])

#### SINGLESHOT
Input format:
```python
{
    "image": {
        "Q0": (s0_complex, s1_complex),  # (ground state IQ, excited state IQ)
    }
}
```
- `s0_complex`: 1D complex array for |0⟩ state
- `s1_complex`: 1D complex array for |1⟩ state

#### SPECTRUM2D (Scope)
Input format:
```python
{
    "image": {
        "Q0": (s_matrix.T, bias_array, freq_array),
    }
}
```
- `s_matrix`: 2D array of shape [n_bias, n_freq]
- `bias_array`: 1D array of bias values
- `freq_array`: 1D array of frequency values

Supported data keys: `iq_avg`, `population`, `iq`

#### SPECTRUM (Scope/NNScope)
Input format:
```python
{
    "image": {
        "Q0": [freq_array, s_array],  # 1D spectrum
    }
}
```
- `freq_array`: 1D array of frequency values
- `s_array`: 1D array of spectral amplitude

#### POWERSHIFT (Scope)
Input format:
```python
{
    "image": {
        "Q0": (freq_array, power_array, s_matrix.T),
    }
}
```
- `freq_array`: 1D array of frequency values
- `power_array`: 1D array of power values
- `s_matrix`: 2D array of shape [n_freq, n_power]

#### RB (Randomized Benchmarking)
Input format:
```python
{
    "image": {
        "Q0": [cycle_array, [y_main, y_ref]],
    }
}
```
- `cycle_array`: 1D array of Clifford cycle numbers
- `y_main`: 1D array of survival probabilities (1 - population)
- `y_ref`: 1D reference array (or zeros if single gate group)

### Getting Results

```python
# Get raw results
results = client.get_result(response=response)

# Get filtered results by confidence threshold (for S21PEAK)
results_filtered = client.get_filtered_result(response, threshold=0.5, task_type=TaskName.S21PEAK.value)
```

### Visualization

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

ply_manager = QuantumPlotPlyManager()
plt_manager = QuantumPlotPltManager()

for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
    save_path = f"./result_{idx}"
    plt_manager.plot_quantum_data(
        data_type='npy',
        task_type=TaskName.S21PEAK.value,
        save_path=save_path + ".png",
        result=result,
        dict_param=dict_param
    )
```

### Curve Types (for NNScope)

```python
from qubitclient import CurveType

# Available curve types:
CurveType.COSINE  # Cosine curve fitting
CurveType.POLY    # Polynomial curve fitting
```

### Examples

#### S21 Peak Detection

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient(url="http://server:port", api_key="key")

# Prepare data: frequency, amplitude, phase
freq = np.linspace(4e9, 6e9, 201)
iq_avg = np.random.randn(201) + 1j * np.random.randn(201)
amp = np.abs(iq_avg)
phi = np.unwrap(np.angle(iq_avg))

dict_list = [{
    "image": {
        "Q0": (freq, amp, phi)
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.S21PEAK)
results = client.get_result(response)
# Returns: [{"peaks": [[10,41,20]], "confs": [[0.3,0.4,0.1]], "freqs_list": [[0.3e9,0.4e9,0.1e9]]}]
```

#### T1 Fitting

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient(url="http://server:port", api_key="key")

# T1 decay data
delay = np.array([0, 1e-6, 2e-6, 5e-6, 10e-6, 20e-6, 50e-6])
population = np.array([1.0, 0.85, 0.72, 0.45, 0.20, 0.04, 0.01])

dict_list = [{
    "image": {
        "Q0": (delay, population)
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.T1FIT)
results = client.get_result(response)
# Returns fitted T1 time and parameters
```

#### DRAG Analysis

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient(url="http://server:port", api_key="key")

# DRAG lambda scan data
lamb = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
# y0y1: 2D array [2, n_lambda] - population for both states
y0y1 = np.array([
    [0.95, 0.92, 0.88, 0.85, 0.82, 0.80, 0.82, 0.85, 0.88, 0.91, 0.94],  # state 0
    [0.05, 0.08, 0.12, 0.15, 0.18, 0.20, 0.18, 0.15, 0.12, 0.09, 0.06]   # state 1
])

dict_list = [{
    "image": {
        "Q0": (lamb, y0y1)
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.DRAG)
results = client.get_result(response)
# Returns optimal lambda value and fitted curve
```

#### 2D Spectrum Analysis (NNScope)

```python
from qubitclient import QubitNNScopeClient, NNTaskName, CurveType
import numpy as np

client = QubitNNScopeClient(url="http://server:port", api_key="key")

# 2D spectrum data
bias = np.linspace(-0.5, 0.5, 51)
freq = np.linspace(4e9, 6e9, 101)
iq_avg = np.random.randn(51, 101) + 1j * np.random.randn(51, 101)

dict_list = [{
    "image": {
        "Q0": (iq_avg.T, bias, freq)  # Note: transpose for correct shape
    }
}]

response = client.request(
    file_list=dict_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.COSINE
)

results = client.get_result(response=response)
```

#### Single-Shot Readout

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient(url="http://server:port", api_key="key")

# Single-shot IQ data for |0> and |1> states
s0 = np.random.randn(1000) + 1j * np.random.randn(1000)  # ground state
s1 = np.random.randn(1000) + 1j * np.random.randn(1000)  # excited state

dict_list = [{
    "image": {
        "Q0": (s0, s1)
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.SINGLESHOT)
results = client.get_result(response)
```

### Data Format Conversion (from Quark)

Use the conversion functions in `resources/quark/analysis/format.py` to convert Quark format data:

```python
from resources.quark.analysis.format import (
    s21_convert,
    optpipulse_convert,
    t1fit_convert,
    drag_convert,
    spectrum2d_convert,
    # ... etc
)

# Convert Quark format to qubitclient format
quark_data = {"meta": {...}, "data": {...}}
converted = s21_convert(quark_data)

# Use converted data
response = client.request(file_list=[converted], task_type=TaskName.S21PEAK)
```