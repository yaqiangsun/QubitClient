# NNScope.SPECTRUM2D 任务接口文档

## 概述

NNScope.SPECTRUM2D 是 NNScope 中的一个任务，用于对二维频谱数据进行曲线分割。该任务支持多种曲线拟合类型，包括多项式拟合和余弦拟合。
不提取量子比特参数。

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitNNScopeClient, NNTaskName
from qubitclient.nnscope.nnscope_api.curve.curve_type import CurveType
client = QubitNNScopeClient()
```

### 请求参数
| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| file_list | list[str\|dict[str,np.ndarray]\|np.ndarray] | 是 | 数据文件列表，支持.npy、.npz文件路径或numpy数组 |
| task_type | NNTaskName | 是 | 任务类型，固定为`NNTaskName.SPECTRUM2D` |
| curve_type | CurveType | 否 | 曲线拟合类型，可选`CurveType.POLY`(多项式)或`CurveType.COSINE`(余弦)，默认`CurveType.COSINE` |

### 数据格式

#### 输入格式

1. **NPZ 文件格式**：
   ```python
   dict_list = [{
       "bias": np.ndarray,        # 偏置数组，shape=(A,)
       "frequency": np.ndarray,   # 频率数组，shape=(B,)
       "iq_avg": np.ndarray       # IQ平均值，shape=(B, A)，dtype=complex64
   }]
   ```

2. **NPY 文件格式**：
   NPY文件需要包含一个字典：

   ```python
   {
       "image": {
           "Q0": (iq_avg, bias, frequency),   # tuple, length=3
           "Q1": (iq_avg, bias, frequency),
           ...
       }
   }
   ```
每个量子比特对应一个键（如 "Q0"），值为 (iq_avg, bias, frequency)，至少包含前3个元素：
| 元素 | 类型 | 描述 |
|------|------|------|
| iq_avg | np.ndarray,  shape=(B, A) | IQ平均值，dtype=complex64 |
| bias | np.ndarray, shape=(A,) | 偏置数组，dtype=float64 |
| frequency | np.ndarray,  shape=(B,) | 频率数组，dtype=float64 |

#### 调用示例

```python
# 使用文件路径
response = client.request(
    file_list=["file1.npz", "file2.npz"],
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.COSINE
)

# 使用numpy数组
import numpy as np
data_ndarray = np.load("file.npy", allow_pickle=True)
dict_list = [data_ndarray]
response = client.request(
    file_list=dict_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.COSINE
)

# 使用字典列表
dict_list = [{
    "iq_avg": iq_avg_array,
    "bias": bias_array,
    "frequency": frequency_array
}]
response = client.request(
    file_list=dict_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.COSINE
)
```

### 获取结果

```python
# 不过滤的结果
results = client.get_result(response)

# 或过滤后的结果
threshold = 0.5
results = client.get_result(response, threshold=threshold, task_type=NNTaskName.SPECTRUM2D.value)
```

## 返回值格式

返回的结果是一个列表，每个字典元素对应一个输入文件的处理结果：

```json
[
  {
    "params_list": List[List[List[float]]],       // 表示拟合参数
    "linepoints_list": List[List[List[List[float]]]], // 表示线点集合
    "confidences_list": List[List[float]],    // 表示线置信度
    "class_ids_list": List[List[float]],      // 表示线类型
    "curve_type_list": List[List[str]],       // 表示拟合类型
    "status": str
  },
  ...
]
```

其中，当拟合类型 curve_type_list 为 "cosin" 时，拟合参数列表 params_list 为 [A, freq, phi, offset]，拟合公式为：
```
pred_y = A * np.sin(freq * pred_x + phi) + offset
```

其中，当拟合类型 curve_type_list 为 "poly" 时，拟合参数列表 params_list 为 [A, B, C, D]，拟合公式为：
```
pred_y = A * pred_x**3 + B * pred_x**2 + C * pred_x**1 + D
```
### 字段说明
| 字段名 | 类型 | 描述                                             |
|--------|------|------------------------------------------------|
| params_list | List[List[List[float]]] | 拟合参数|
| linepoints_list | List[List[List[List[float]]]] | 线点集合|
| confidences_list | List[List[float]] | 线置信度 |
| class_ids_list | List[List[float]] | 线类型 |
| curve_type_list | List[List[str]] | 拟合类型|
| status | str | 处理状态，'success' 表示成功 |

### 示例结果

```python
[
  {
    "params_list": [[[-1, -1, -1, -1]], [[-1, -1, -1, -1]]],
    "linepoints_list": [[[[-1, 6.843e9], [-0.9, 6.844e9], ...]], [[[-0.8, 6.833e9], [-1, 6.847e9], ...]]],
    "confidences_list": [[0.6], [0.6]],
    "class_ids_list": [[1.0], [1.0]],
    "curve_type_list": [["cosin"], ["cosin"]],
    "status": "success"
  },  
  ...
]
```

## 可视化

处理结果可以通过内置的绘图工具进行可视化：

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

if type(results) == dict:
    if "results" not in results.keys():
        results = results.get("results")
    elif "result" in results.keys():
        results = results.get("result")

save_path_prefix = f"./tmp/client/result_{NNTaskName.SPECTRUM2D.value}_{savename}"
save_path_png = save_path_prefix + ".png"
save_path_html = save_path_prefix + ".html"

plot_manager = QuantumPlotPlyManager()
plot_manager.plot_quantum_data(
    task_type=NNTaskName.SPECTRUM2D.value,
    save_path=save_path_html,
    data_type='npy',
    result=results,
    dict_param=data_ndarray
)

plot_manager = QuantumPlotPltManager()
plot_manager.plot_quantum_data(
    task_type=NNTaskName.SPECTRUM2D.value,
    save_path=save_path_png,
    data_type='npy',
    result=results,
    dict_param=data_ndarray
)
```