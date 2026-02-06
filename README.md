# QubitClient

## 介绍

**QubitClient** 是一个用于与Qubit服务进行交互的Python客户端库。它提供了丰富的API接口，支持多种量子计算相关的任务，包括曲线分割、参数拟合等功能。

## 功能特性

- **曲线分割功能**: 支持多项式(POLY)和余弦(COSINE)类型的曲线拟合
- **多种任务支持**: 包括S21峰值检测、最优π脉冲、Rabi振荡、T1/T2拟合等多种量子计算任务
- **灵活的数据输入**: 支持文件路径、NumPy数组、字典等多种数据格式作为输入
- **批量处理**: 支持同时处理多个数据文件
- **易于集成**: 提供简洁明了的API接口，方便快速集成到现有项目中

## 安装

```bash
pip install qubitclient
```
如果需要使用绘图等功能
```bash
pip install qubitclient[full]
```

或者从源码安装：

```bash
cd QubitClient
pip install -e .
```

## 快速开始

### 配置

1. 拷贝配置文件模板：
```bash
cp config.py.example config.py
```

2. 修改 [config.py]() 文件中的服务器地址和API密钥：
```python
API_URL = "http://your-server-address:port"
API_KEY = "your-api-key"
```

### 使用示例
#### NNScope功能（曲线分割）

```python
from qubitclient import QubitNNScopeClient, NNTaskName, CurveType
import numpy as np

# 初始化客户端
client = QubitNNScopeClient(url="http://your-server-address:port", api_key="your-api-key")

# 方式1: 直接使用文件路径
file_path_list = ["data/file1.npz", "data/file2.npz"]
response = client.request(
    file_list=file_path_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.COSINE
)

# 方式2: 使用NumPy数组字典
data_ndarray = np.load(file_path, allow_pickle=True)
dict_list = [data_ndarray]

response = client.request(
    file_list=dict_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.POLY
)

# 获取结果
results = client.get_result(response=response)
```

#### Scope功能

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

# 初始化客户端
client = QubitScopeClient(url="http://your-server-address:port", api_key="your-api-key")

# 准备数据
dict_list = [{
    "some_key": np.ndarray(...)
}]

# 发起请求
response = client.request(
    file_list=dict_list,
    task_type=TaskName.OPTPIPULSE  # 可选任务见下方任务类型列表
)

# 获取结果
results = client.get_result(response=response)
```

## 支持的任务类型

### NNScope任务

- `NNTaskName.SPECTRUM2D`: 二维频谱数据曲线分割，详见 [SPECTRUM2D详细文档](docs/nnscope/SPECTRUM2D.md)
- `NNTaskName.POWERSHIFT`: 功率偏移曲线分割，详见 [POWERSHIFT详细文档](docs/nnscope/POWERSHIFT.md)
- `NNTaskName.S21VFLUX`: S21 vs Flux参数曲线分割，详见 [S21VFLUX详细文档](docs/nnscope/S21VFLUX.md)
- `NNTaskName.SPECTRUM`: 频谱分析，详见 [SPECTRUM详细文档](docs/nnscope/SPECTRUM.md)

### Scope任务

- `TaskName.S21PEAK`: S21参数峰值检测，详见 [S21PEAK详细文档](docs/scope/S21PEAK.md)
- `TaskName.OPTPIPULSE`: 最优π脉冲计算，详见 [OPTPIPULSE详细文档](docs/scope/OPTPIPULSE.md)
- `TaskName.RABICOS`: Rabi振荡余弦拟合，详见 [RABICOS详细文档](docs/scope/RABICOS.md)
- `TaskName.RAMSEY`: RAMSY衰减震荡余弦拟合，详见 [RAMSEY详细文档](docs/scope/RABICOS.md)
- `TaskName.S21VFLUX`: S21 vs Flux分析，详见 [S21VFLUX详细文档](docs/scope/S21VFLUX.md)
- `TaskName.SINGLESHOT`: 单次测量分析，详见 [SINGLESHOT详细文档](docs/scope/SINGLESHOT.md)
- `TaskName.SPECTRUM`: 频谱分析，详见 [SPECTRUM详细文档](docs/scope/SPECTRUM.md)
- `TaskName.T1FIT`: T1时间拟合，详见 [T1FIT详细文档](docs/scope/T1FIT.md)
- `TaskName.T2FIT`: T2时间拟合，详见 [T2FIT详细文档](docs/scope/T2FIT.md)
- `TaskName.POWERSHIFT`: 分析功率偏移曲线，详见 [POWERSHIFT详细文档](docs/scope/POWERSHIFT.md)
- `TaskName.SPECTRUM2D`: 二维频谱数据曲线分割，详见 [SPECTRUM2D详细文档](docs/scope/SPECTRUM2D.md)
- `TaskName.DRAG`: DRAG免交叉点，详见 [DRAG详细文档](docs/scope/DRAG.md)

### Ctrl任务
- `CtrlTaskName.S21`: S21腔频测量实验.

## 数据格式说明

### 输入格式

依据功能不同，输入格式有所不同

### 输出格式

依据功能任务不同，输出格式有所不同

## 运行测试示例
测试示例包含在 [tests](tests) 目录下，可依据文件名运行对应的测试代码

```bash
# 运行NNScope测试
python tests/test_nnscope.py

# 运行Scope测试
python tests/test_scope.py
```

## 更新日志

近期更新:
- **增加Ctrl功能包**: 基于MCP协议的测量任务(20260206)
- **增加DRAG分析功能**: 增加DRAG任务数据分析(20260205)
- **增加scope功能包**: 增加多种任务功能(20251022)
- **增加曲线类型**: 增加余弦类型曲线拟合(20250606)
- **构建基础项目**: 基础功能与结构构建

## 许可证

本项目采用GPL-3.0许可证，详见[LICENSE](LICENSE)文件。