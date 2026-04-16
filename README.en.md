<h1>QubitClient: AI Client for Quantum Systems</h1>

<p align="center">
    <br>
    <img src="asset/qubitclient.png" width="200"/>
    <br>
<p>
<p align="center">
<a href="README.md">中文文档</a> | English Doc
<br>
</p>

## Introduction

**QubitClient** is a Python client library for interacting with Qubit services. It provides rich APIs supporting various quantum computing related tasks, including curve segmentation, parameter fitting, and other functions.

## Features

- **2D Data Analysis**: 2D spectrum analysis, power shift curve analysis, etc.
- **Multiple Task Support**: Includes various quantum computing tasks such as S21 peak detection, optimal π pulse, Rabi oscillation, T1/T2 fitting, etc.
- **Flexible Data Input**: Supports multiple data formats as input, including file paths, NumPy arrays, dictionaries, etc.
- **Batch Processing**: Supports processing multiple data files simultaneously
- **Easy Integration**: Provides clean and clear API interfaces for quick integration into existing projects
- **MCP Protocol Support**: Real-time quantum measurement task control based on MCP protocol
- **LLM/VLM Integration**: Supports large language models and vision-language models for quantum measurement data analysis and decision-making

## Installation

```bash
pip install qubitclient
```

If you need to use plotting features:

```bash
pip install qubitclient[full]
```

Or install from source:

```bash
cd QubitClient
pip install -e .
```

## Quick Start

### Configuration

1. Copy the configuration template:
```bash
cp config.py.example config.py
```

2. Modify the server address and API key in [config.py](config.py):
```python
API_URL = "http://your-server-address:port"
API_KEY = "your-api-key"
```

### Usage Examples
#### NNScope Functions (Curve Segmentation)

```python
from qubitclient import QubitNNScopeClient, NNTaskName, CurveType
import numpy as np

# Initialize the client
client = QubitNNScopeClient(url="http://your-server-address:port", api_key="your-api-key")

# Method 1: Directly using file paths
file_path_list = ["data/file1.npz", "data/file2.npz"]
response = client.request(
    file_list=file_path_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.COSINE
)

# Method 2: Using NumPy array dictionaries
data_ndarray = np.load(file_path, allow_pickle=True)
dict_list = [data_ndarray]

response = client.request(
    file_list=dict_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.POLY
)

# Get results
results = client.get_result(response=response)
```

#### Scope Functions

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

# Initialize the client
client = QubitScopeClient(url="http://your-server-address:port", api_key="your-api-key")

# Prepare data
dict_list = [{
    "some_key": np.ndarray(...)
}]

# Make request
response = client.request(
    file_list=dict_list,
    task_type=TaskName.OPTPIPULSE  # See task types list below for options
)

# Get results
results = client.get_result(response=response)
```

#### Ctrl Functions (MCP Protocol Measurement Tasks)

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

# Initialize the client
client = QubitCtrlClient()

# Execute S21 cavity frequency measurement experiment
result = client.run(
    task_type=CtrlTaskName.S21,
    qubits=["Q0", "Q1"],
    frequency_start=-40e6,
    frequency_end=40e6,
    frequency_sample_num=101
)

print(result)
```

#### LLM Functions (VLM Image Analysis)

```python
from qubitclient.llm import QubitLLM, LLMTaskName

# Initialize client (auto-loads config from qubitclient.json)
llm = QubitLLM()

# Method 1: Direct chat
result = llm.chat([
    {"role": "system", "content": "You are a quantum physics expert."},
    {"role": "user", "content": "Explain quantum entanglement"}
])
print(result)

# Method 2: VLM with image
result = llm.chat(
    [{"role": "user", "content": "Analyze this image"}],
    images="measurement.png"
)
print(result)

# Method 3: Use task prompt (auto-builds messages and JSON schema)
result = llm.run(LLMTaskName.EVALUATE_ANALYSIS, analysis_result={"score": 80})
print(result)
```

## Supported Task Types

### NNScope Tasks

- `NNTaskName.SPECTRUM2D`: 2D spectrum data curve segmentation, see [SPECTRUM2D Detailed Documentation](docs/nnscope/SPECTRUM2D.md)
- `NNTaskName.POWERSHIFT`: Power shift curve segmentation, see [POWERSHIFT Detailed Documentation](docs/nnscope/POWERSHIFT.md)
- `NNTaskName.S21VFLUX`: S21 vs Flux parameter curve segmentation, see [S21VFLUX Detailed Documentation](docs/nnscope/S21VFLUX.md)
- `NNTaskName.SPECTRUM`: Spectrum analysis, see [SPECTRUM Detailed Documentation](docs/nnscope/SPECTRUM.md)

### Scope Tasks

- `TaskName.S21PEAK`: S21 parameter peak detection, see [S21PEAK Detailed Documentation](docs/scope/S21PEAK.md)
- `TaskName.OPTPIPULSE`: Optimal π pulse calculation, see [OPTPIPULSE Detailed Documentation](docs/scope/OPTPIPULSE.md)
- `TaskName.RABICOS`: Rabi oscillation cosine first peak detection, see [RABICOS Detailed Documentation](docs/scope/RABICOS.md)
- `TaskName.RAMSEY`: Ramsey decay oscillation cosine fitting, see [RAMSEY Detailed Documentation](docs/scope/RAMSEY.md)
- `TaskName.S21VFLUX`: S21 vs Flux analysis, see [S21VFLUX Detailed Documentation](docs/scope/S21VFLUX.md)
- `TaskName.SINGLESHOT`: Single shot analysis, see [SINGLESHOT Detailed Documentation](docs/scope/SINGLESHOT.md)
- `TaskName.SPECTRUM`: Spectrum analysis, see [SPECTRUM Detailed Documentation](docs/scope/SPECTRUM.md)
- `TaskName.T1FIT`: T1 time fitting, see [T1FIT Detailed Documentation](docs/scope/T1FIT.md)
- `TaskName.T2FIT`: T2 time fitting, see [T2FIT Detailed Documentation](docs/scope/T2FIT.md)
- `TaskName.POWERSHIFT`: Analyze power shift curves, see [POWERSHIFT Detailed Documentation](docs/scope/POWERSHIFT.md)
- `TaskName.SPECTRUM2D`: 2D spectrum data curve segmentation, see [SPECTRUM2D Detailed Documentation](docs/scope/SPECTRUM2D.md)
- `TaskName.DRAG`: DRAG cross-point avoidance, see [DRAG Detailed Documentation](docs/scope/DRAG.md)

### Ctrl Tasks

- `CtrlTaskName.S21`: S21 cavity frequency measurement experiment, measuring S21 response of specified qubits within frequency range, see [S21 Detailed Documentation](docs/ctrl/S21.md)
- `CtrlTaskName.DRAG`: DRAG cross-point avoidance measurement, optimizing DRAG parameters for qubits, see [DRAG Detailed Documentation](docs/ctrl/DRAG.md)
- `CtrlTaskName.DELTA`: Frequency offset calibration measurement, determining optimal working frequency offset for qubits, see [DELTA Detailed Documentation](docs/ctrl/DELTA.md)
- `CtrlTaskName.OPTPIPULSE`: Optimal π pulse measurement, finding best π pulse amplitude, see [OPTPIPULSE Detailed Documentation](docs/ctrl/OPTPIPULSE.md)
- `CtrlTaskName.POWERSHIFT`: Power shift curve measurement, analyzing qubit response under different power levels, see [POWERSHIFT Detailed Documentation](docs/ctrl/POWERSHIFT.md)
- `CtrlTaskName.RABI`: Rabi oscillation measurement, observing qubit oscillation behavior under driving field, see [RABI Detailed Documentation](docs/ctrl/RABI.md)
- `CtrlTaskName.RAMSEY`: Ramsey interference measurement, measuring qubit decoherence time, see [RAMSEY Detailed Documentation](docs/ctrl/RAMSEY.md)
- `CtrlTaskName.S21VSFLUX`: S21 vs Flux measurement, analyzing flux impact on qubit frequency, see [S21VSFLUX Detailed Documentation](docs/ctrl/S21VSFLUX.md)
- `CtrlTaskName.SINGLESHOT`: Single shot measurement analysis, evaluating qubit readout fidelity, see [SINGLESHOT Detailed Documentation](docs/ctrl/SINGLESHOT.md)
- `CtrlTaskName.SPECTRUM`: Spectrum analysis measurement, scanning qubit energy level structure, see [SPECTRUM Detailed Documentation](docs/ctrl/SPECTRUM.md)
- `CtrlTaskName.SPECTRUM_2D`: 2D spectrum measurement, simultaneously scanning frequency and bias parameters, see [SPECTRUM_2D Detailed Documentation](docs/ctrl/SPECTRUM_2D.md)
- `CtrlTaskName.T1`: T1 relaxation time measurement, measuring qubit energy relaxation time, see [T1 Detailed Documentation](docs/ctrl/T1.md)

### LLM Tasks

- `LLMTaskName.VLM_ANALYZE`: VLM image analysis
- `LLMTaskName.EVALUATE_ANALYSIS`: Evaluate analysis results
- `LLMTaskName.DECIDE_NEXT_ACTION`: Decide next action
- `LLMTaskName.SUGGEST_PARAMS`: Suggest measurement parameters

## Data Format Specification

### Input Format

Depending on the functionality, input formats may vary.

### Output Format

Depending on the task, output formats may vary.

## Running Test Examples

Test examples are located in the [tests](tests) directory, and you can run corresponding test code according to the filename:

```bash
# Run NNScope tests
python tests/test_nnscope.py

# Run Scope tests
python tests/test_scope.py

# Run Ctrl tests
python tests/test_ctrl_mcp.py

# Run LLM tests
python tests/test_llm.py
```

## LLM Configuration

Configure LLM in `qubitclient.json` (create or edit this file):

```json
{
  "llm": {
    "api_key": "your-api-key",
    "base_url": "https://your-llm-endpoint.com/v1",
    "model": "gpt-4o"
  }
}
```

Supported configuration methods (priority from low to high):
1. Default values (gpt-4o)
2. User directory `~/qubitclient.json`
3. Environment variables `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`
4. Runtime directory `./qubitclient.json`
5. Constructor parameters (highest priority)

## Format Conversion and Other Tool Integration

Refer to the code in the [resources](resources) directory for different tools.

## Changelog

Recent updates:

- **Added LLM module**: Integrated large language models and vision-language models for quantum measurement data analysis and decision-making (2026-04-16)
- **Added Ctrl package**: MCP protocol-based measurement tasks (2026-02-06)
- **Added DRAG analysis function**: Added DRAG task data analysis (2026-02-05)
- **Added scope package**: Added multiple task functions (2025-10-22)
- **Added curve types**: Added cosine type curve fitting (2025-06-06)
- **Built basic project**: Basic functions and structure construction

## License

This project is licensed under the GPL-3.0 license. See the [LICENSE](LICENSE) file for details.