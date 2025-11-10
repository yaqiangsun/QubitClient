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

- `NNTaskName.SPECTRUM2D`: 二维频谱数据曲线分割

### Scope任务

- `TaskName.S21PEAK`: S21参数峰值检测
- `TaskName.OPTPIPULSE`: 最优π脉冲计算
- `TaskName.RABI`: Rabi振荡分析
- `TaskName.RABICOS`: Rabi振荡余弦拟合
- `TaskName.S21VFLUX`: S21 vs Flux分析
- `TaskName.SINGLESHOT`: 单次测量分析
- `TaskName.SPECTRUM`: 频谱分析
- `TaskName.T1FIT`: T1时间拟合
- `TaskName.T2FIT`: T2时间拟合

## 数据格式说明

### Scope任务

- `TaskName.S21PEAK`: S21参数峰值检测
- `TaskName.OPTPIPULSE`: 最优π脉冲计算
- `TaskName.RABI`: Rabi振荡分析
- `TaskName.RABICOS`: Rabi振荡余弦拟合
- `TaskName.S21VFLUX`: S21 vs Flux分析
- `TaskName.SINGLESHOT`: 单次测量分析
- `TaskName.SPECTRUM`: 频谱分析
- `TaskName.T1FIT`: T1时间拟合
- `TaskName.T2FIT`: T2时间拟合

## 数据格式说明

### 输入格式

依据功能不同，输入格式有所不同

### 输出格式

依据功能任务不同，输出格式有所不同

## 运行测试示例

```bash
# 运行NNScope测试
python tests/test_nnscope.py

# 运行Scope测试
python tests/test_scope.py
```

## 更新日志

近期更新:

- **增加scope功能包**: 增加多种任务功能(20251022)
- **增加曲线类型**: 增加余弦类型曲线拟合(20250606)
- **构建基础项目**: 基础功能与结构构建

## 功能集合
### 曲线分割功能

#### 运行示例代码
```python
python tests/test_nnscope.py
```

#### 定义实例
```
client = QubitNNScopeClient(url=url,api_key="")
```

#### 请求输入

```python
response = client.request(file_list=file_path_list,\
    task_type=NNTaskName.SPECTRUM2D,curve_type=CurveType.COSINE)
```
- dict_list格式为：
```json
[
    {
        "bias":np.ndarray shape(A),
        "frequency":np.ndarray shape(B),
        "iq_avg":np.ndarray shape(B,A),
    },
    ...
]
```
- curve_type: `CurveType.COSINE`(cosin拟合) or `CurveType.POLY`(多项式拟合)


#### 返回值
返回请求为response
```python
res = response.json()
```
res格式为：
```json
{
    "state":'success',
    "result":result
}
```
其中result格式：
```json
[
    {
        "params_list":List[List[float]],//每条线段的多项式参数列表
        "linepoints_list":List[List[[row_index,col_index]]],//每条线段的点坐标列表
        "confidence_list":List[float],//每条线段的置信度
    },//每一个npz文件的结果
    {
        ...
    },
    ...
]
```

## 许可证

本项目采用GPL-3.0许可证，详见[LICENSE](LICENSE)文件。