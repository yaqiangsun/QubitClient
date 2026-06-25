# S21VSFLUX 任务接口文档

## 概述

S21VSFLUX 是 NNScope 中的一个任务，用于对二维频谱数据进行曲线分割。该任务支持多种曲线拟合类型，包括多项式拟合和余弦拟合。

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitNNScopeClient
from qubitclient import NNTaskName


client = QubitNNScopeClient()
```

### 请求参数


| 参数名 | 类型 | 必需 | 描述                                         |
|--------|------|------|------|---------|
| file_list | list[str\|dict[str,np.ndarray]\| np.ndarray]  | 是 | 数据文件列表，支持.npy或numpy数组 |
| task_type | NNTaskName | 是 | 任务类型，固定为`NNTaskName.S21VSFLUX`|

### 数据格式

#### 输入格式

NPY文件需要包含一个字典：

```python
{
    "image": {
        "Q0": (freq, volt, s, ...),   # tuple, length>=3
        "Q1": (freq, volt, s, ...),
        ...
    }
}
```

每个量子比特对应一个键（如 "Q0"），值为 tuple，至少包含前3个元素：

| 元素 | 类型 | 描述 |
|------|------|------|
| freq | np.ndarray, shape=(A,) | 频率数据，dtype=float64 |
| volt | np.ndarray, shape=(B,) | 电压信息，dtype=float64 |
| s | np.ndarray, shape=(B, A) | 二维频谱数据，dtype=float32 |
| ... | tuple | 可选的附加元素 |

#### 调用示例

```python
# 使用文件路径
response = client.request(file_list=["data/singlepath/file1.npy", "data/singlepath/file2.npy"], task_type=NNTaskName.S21VSFLUX)
```

或使用加载后的数据：

```python
from qubitclient.scope.utils.data_parser import load_npy_file

dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

# 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=NNTaskName.S21VSFLUX)
```

### 获取结果

```python


results = client.get_result(response=response)
threshold = 0.5
results_filtered = client.get_filtered_result(response, threshold, NNTaskName.S21VSFLUX.value)
results_filtered = results_filtered.get("result")

```

## 返回值格式

返回的结果是一个列表，每个字典元素对应一个输入文件的处理结果：

```json
[
  {
    "params_list": [[[float]]],        // 表示拟合参数
    "linepoints_list": [[[[float]]]],  // 表示线点集合
    "confidence_list": [[float]],      // 表示线置信度
    "class_ids": [[float]],            // 表示线类型
    "curve_type": [[str]],             // 表示拟合类型
    "status": "success" | "failed"
  },
  ...
]
```

其中，当拟合类型 curve_type 为 "cosin" 时，拟合参数列表 params_list 为 [A, freq, phi, offset]，拟合公式为：
```
pred_y = A * np.sin(freq * pred_x + phi) + offset
```

其中，当拟合类型 curve_type 为 "poly" 时，拟合参数列表 params_list 为 [A, B, C, D]，拟合公式为：
```
pred_y = A * pred_x**3 + B * pred_x**2 + C * pred_x**1 + D
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| params_list | [[[float]]] | 表示拟合参数 |
| linepoints_list | [[[[float]]]] | 表示线点集合 |
| confidence_list | [[float]] | 表示线置信度 |
| class_ids | [[float]] | 表示线类型 |
| curve_type | [[str]] | 表示拟合类型 ("cosin" 或 "poly") |
| status | str | 处理状态 |



### 示例结果

```python
[
  {
    "params_list": [[[-1, -1, -1, -1]], [[-1, -1, -1, -1]]],
    "linepoints_list": [[[[-1, 6.843e9], [-0.9, 6.844e9], ...]], [[[-0.8, 6.833e9], [-1, 6.847e9], ...]]],
    "confidence_list": [[0.6], [0.6]],
    "class_ids": [[1.0], [1.0]],
    "curve_type": [["cosin"], ["cosin"]],
    "status": "success"
  }
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

plot_manager = QuantumPlotPlyManager()
plot_manager.plot_quantum_data(
    data_type='npy',
    task_type=NNTaskName.S21VSFLUX.value,
    save_path=save_path_html,
    result=results,
    dict_param=data_ndarray
)

plot_manager = QuantumPlotPltManager()
plot_manager.plot_quantum_data(
    data_type='npy',
    task_type=NNTaskName.S21VSFLUX.value,
    save_path=save_path_png,
    result=results,
    dict_param=data_ndarray
)

```