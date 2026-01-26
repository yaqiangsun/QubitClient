# QubitClient

## Introduction

**QubitClient** is a Python client library for interacting with Qubit services. It provides rich APIs supporting various quantum computing related tasks, including curve segmentation, parameter fitting, and other functions.

## Features

- **Curve Segmentation**: Supports polynomial (POLY) and cosine (COSINE) type curve fitting
- **Multiple Task Support**: Includes various quantum computing tasks such as S21 peak detection, optimal π pulse, Rabi oscillation, T1/T2 fitting, etc.
- **Flexible Data Input**: Supports multiple data formats as input, including file paths, NumPy arrays, dictionaries, etc.
- **Batch Processing**: Supports processing multiple data files simultaneously
- **Easy Integration**: Provides clean and clear API interfaces for quick integration into existing projects

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

## Supported Task Types

### NNScope Tasks

- `NNTaskName.SPECTRUM2D`: 2D spectrum data curve segmentation, see [SPECTRUM2D Detailed Documentation](docs/nnscope/SPECTRUM2D.md)
- `NNTaskName.POWERSHIFT`: Power shift curve segmentation, see [POWERSHIFT Detailed Documentation](docs/nnscope/POWERSHIFT.md)
- `NNTaskName.S21VFLUX`: S21 vs Flux parameter curve segmentation, see [S21VFLUX Detailed Documentation](docs/nnscope/S21VFLUX.md)
- `NNTaskName.SPECTRUM`: Spectrum analysis, see [SPECTRUM Detailed Documentation](docs/nnscope/SPECTRUM.md)

### Scope Tasks

- `TaskName.S21PEAK`: S21 parameter peak detection, see [S21PEAK Detailed Documentation](docs/scope/S21PEAK.md)
- `TaskName.OPTPIPULSE`: Optimal π pulse calculation, see [OPTPIPULSE Detailed Documentation](docs/scope/OPTPIPULSE.md)
- `TaskName.RABICOS`: Rabi oscillation cosine fitting, see [RABICOS Detailed Documentation](docs/scope/RABICOS.md)
- `TaskName.RAMSEY`: Ramsey decay oscillation cosine fitting, see [RAMSEY Detailed Documentation](docs/scope/RAMSEY.md)
- `TaskName.S21VFLUX`: S21 vs Flux analysis, see [S21VFLUX Detailed Documentation](docs/scope/S21VFLUX.md)
- `TaskName.SINGLESHOT`: Single shot analysis, see [SINGLESHOT Detailed Documentation](docs/scope/SINGLESHOT.md)
- `TaskName.SPECTRUM`: Spectrum analysis, see [SPECTRUM Detailed Documentation](docs/scope/SPECTRUM.md)
- `TaskName.T1FIT`: T1 time fitting, see [T1FIT Detailed Documentation](docs/scope/T1FIT.md)
- `TaskName.T2FIT`: T2 time fitting, see [T2FIT Detailed Documentation](docs/scope/T2FIT.md)
- `TaskName.POWERSHIFT`: Analyze power shift curves, see [POWERSHIFT Detailed Documentation](docs/scope/POWERSHIFT.md)
- `TaskName.SPECTRUM2D`: 2D spectrum data curve segmentation, see [SPECTRUM2D Detailed Documentation](docs/scope/SPECTRUM2D.md)

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
```

## Changelog

Recent updates:

- **Added scope package**: Added multiple task functions (2025-10-22)
- **Added curve types**: Added cosine type curve fitting (2025-06-06)
- **Built basic project**: Basic functions and structure construction

## License

This project is licensed under the GPL-3.0 license. See the [LICENSE](LICENSE) file for details.
