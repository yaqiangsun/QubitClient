# NNScope.SPECTRUM2D 任务接口文档

## 概述

NNScope.SPECTRUM2D 是 NNScope 中的一个任务，用于对二维频谱数据进行曲线分割。该任务支持多种曲线拟合类型，包括多项式拟合和余弦拟合。

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitNNScopeClient, NNTaskName
from qubitclient.nnscope.nnscope_api.curve.curve_type import CurveType

client = QubitNNScopeClient(url="http://your-server-address:port", api_key="your-api-key")
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| file_list | list[str\|dict[str,np.ndarray]\|np.ndarray] | 是 | 数据文件列表，支持.npy、.npz文件路径或numpy数组 |
| task_type | NNTaskName | 是 | 任务类型，固定为`NNTaskName.SPECTRUM2D` |
| curve_type | CurveType | 否 | 曲线拟合类型，可选`CurveType.POLY`(多项式)或`CurveType.COSINE`(余弦) |

### 数据格式

#### 输入格式

1. **NPZ 文件格式**：
   ```python
   dict_list = [{
       "bias": np.ndarray,        # 偏置数组，shape(A,)
       "frequency": np.ndarray,   # 频率数组，shape(B,)
       "iq_avg": np.ndarray       # IQ平均值，shape(B,A)
   }]
   ```

2. **NPY 文件格式**：
   NPY文件需要包含一个字典，字典结构与NPZ格式相同。

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
data_ndarray = np.load("file.npz", allow_pickle=True)
dict_list=[data_ndarray]
response = client.request(
    file_list=dict_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.COSINE
)

# 使用字典列表
dict_list = [{
    "bias": bias_array,
    "frequency": frequency_array,
    "iq_avg": iq_avg_array
}]
response = client.request(
    file_list=dict_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.COSINE
)
```

### 获取结果

```python
results = client.get_result(response=response)
threshold = 0.5
results_filtered = client.get_filtered_result(response, threshold, NNTaskName.SPECTRUM2D.value)
results_filtered = results_filtered.get("results")



## 返回值格式

返回的结果是一个列表，每个字典元素对应一个输入文件的处理结果：

```json
[
  {
     "params_list": [[[float]]],     // 表示拟合参数
     "linepoints_list": [[[[float]]]],     // 表示线点集合
    "confidents_list": [[float]],     // 表示线置信度
    "class_ids_list": [[float]],     // 表示线类型
    "curve_type_list":[[str]]     // 表示拟合类型
  },
  ...
]
```




### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| params_list | [[[float]]] | 表示拟合参数 |
| linepoints_list | [[[[float]]]] | 表示线点集合 |
| confidents_list | [[float]] | 表示线置信度 |
| class_ids_list | [[float]] | 表示线类型 |
| curve_type_list | [[float]] | 表示拟合类型 |




### 示例结果

```python
[
  {
     "params_list": [[[-1,-1,-1,-1]],[[-1,-1,-1,-1]]],
     "linepoints_list": [[[[-1,6.843e9],[-0.9,6.844e9],...]],[[[-0.8,6.833e9],[-1,6.847e9],...]]],
    "confidents_list": [[0.6],[0.6]]，
    "class_ids_list": [[1.0],[1.0]],
    "curve_type_list": [["cosin"],["cosin"]]
  }
]
```

## 可视化

处理结果可以通过内置的绘图工具进行可视化：

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

save_path_prefix = f"./tmp/client/result_{NNTaskName.SPECTRUM2D.value}_{savename}"
save_path_png = save_path_prefix + ".png"
save_path_html = save_path_prefix + ".html"
plot_manager = QuantumPlotPlyManager()
plot_manager.plot_quantum_data(
  data_type='npy',
  task_type=NNTaskName.SPECTRUM2D.value,
  save_path=save_path_png,
  result=results,
  dict_param=data_ndarray
)

plot_manager = QuantumPlotPltManager()
plot_manager.plot_quantum_data(
  data_type='npy',
  task_type=NNTaskName.SPECTRUM2D.value,
  save_path=save_path_html,
  result=results,
  dict_param=data_ndarray
)
```