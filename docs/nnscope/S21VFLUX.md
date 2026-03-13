# S21VFLUX 任务接口文档

## 概述

S21VFLUX 是 NNScope 中的一个任务，用于对二维频谱数据进行曲线分割。该任务支持多种曲线拟合类型，包括多项式拟合和余弦拟合。

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitNNScopeClient
from qubitclient import NNTaskName


client = QubitNNScopeClient(url=url,api_key=api_key)
```

### 请求参数


| 参数名 | 类型 | 必需 | 描述                                         |
|--------|------|------|-----------|
| file_list | list[str\|dict[str,np.ndarray]\| np.ndarray]  | 是 | 数据文件列表，支持.npy或numpy数组 |
| task_type | NNTaskName | 是 | 任务类型，固定为`NNTaskName.S21VFLUX`|
| curve_type | CurveType | 是 | 任务类型，固定为`CurveType.AUTO(返回poly和cosine的最優解)`|

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

   ```python
    {
        "image": {
            "Q0": [volt,freq,s],   
            "Q1": [volt,freq,s],
            ...
        }
    }
    ```

volt: 一维 np.ndarray,shape(A,),表示电压信息
freq: 一维 np.ndarray,shape(B,),表示频率数据
s: 二维 np.ndarray,shape(B,A),表示二维频谱数据

每个量子比特对应一个键（如 "Q0"），值为 [volt,freq,s] 的列表

#### 调用示例

```python
# 使用文件路径

response = client.request(file_list=["data/singlepath/file1.npy", "data/singlepath/file2.npy"],task_type=NNTaskName.S21VFLUX,curve_type=CurveType.AUTO)


dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

    # 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list,task_type=NNTaskName.S21VFLUX,curve_type=CurveType.AUTO)

```

### 获取结果

```python


results = client.get_result(response=response)
threshold = 0.5
results_filtered = client.get_filtered_result(response, threshold, NNTaskName.S21VFLUX.value)
results_filtered = results_filtered.get("results")
```

## 返回值格式

返回的结果是一个列表，每个字典元素对应一个输入文件的处理结果：

```json
[
  {
     "params_list": [[[float]]],     // 表示拟合参数
     "linepoints_list": [[[[float]]]],     // 表示线点集合
    "confident_list": [[float]],     // 表示线置信度
    "class_ids": [[float]],     // 表示线类型
    "curve_type":[[str]]     // 表示拟合类型
  },
  ...
]
```




### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| params_list | [[[float]]] | 表示拟合参数 |
| linepoints_list | [[[[float]]]] | 表示线点集合 |
| confident_list | [[float]] | 表示线置信度 |
| class_ids | [[float]] | 表示线类型 |
| curve_type | [[float]] | 表示拟合类型 |




### 示例结果

```python
[
  {
     "params_list": [[[-1,-1,-1,-1]],[[-1,-1,-1,-1]]],
     "linepoints_list": [[[[-1,6.843e9],[-0.9,6.844e9],...]],[[[-0.8,6.833e9],[-1,6.847e9],...]]],
    "confident_list": [[0.6],[0.6]]，
    "class_ids": [[1.0],[1.0]],
    "curve_type": [["cosin"],["cosin"]]
  }
]
```


## 可视化

处理结果可以通过内置的绘图工具进行可视化：

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

plot_manager = QuantumPlotPlyManager()
plot_manager.plot_quantum_data(
    data_type='npy',
    task_type=NNTaskName.S21VFLUX.value,
    save_path=save_path_html,
    result=results_filtered,
    dict_param=data_ndarray
)

plot_manager = QuantumPlotPltManager()
plot_manager.plot_quantum_data(
    data_type='npy',
    task_type=NNTaskName.S21VFLUX.value,
    save_path=save_path_png,
    result=results_filtered,
    dict_param=data_ndarray
)

```