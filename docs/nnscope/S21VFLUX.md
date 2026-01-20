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


response_data = client.get_result(response)
threshold = 0.5
results_filtered = client.get_filtered_result(response, threshold, NNTaskName.S21VFLUX.value)


results = client.get_result(response=response_data)  
#results = client.get_result(response=response_data_filtered)
# response_data 和 response_data_filtered 分别是阈值筛选前和筛选后的结果
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
[
  {
    "params_list": [[float, ...], ...],     // 每条线段的多项式参数列表
    "linepoints_list": [[[int, int], ...], ...], // 每条线段的点坐标列表
    "confidence_list": [float, ...],         // 每条线段的置信度
    "class_ids": [float, ...],         // 每条线段的分割标签（{0:"cos_light",1:"cos_dark",2:"line_light",3:"line_dark"}）
    "curve_type": [str, ...],         // 每条线段的拟合方式（cosine,或poly）
  },
  ...
]
```




### 字段说明

| 字段名 | 类型                                 | 描述 |
|--------|------------------------------------|------|
| params_list | List[List[float]]                  | 每条检测到的线段的拟合参数列表 |
| linepoints_list | List[List[[row_index, col_index]]] | 每条线段的点坐标列表，每个点包含行索引和列索引 |
| confidence_list | List[float]                        | 每条线段的置信度，表示检测的可靠性 |
| class_ids | List[float]                        | 每条线段的分割标签 |
| curve_type | List[str]                          | 每条线段的拟合方式（cosine,或poly） |



### 示例结果

```python
[
  {
    "params_list": [
      [1.2, 3.4, 5.6],
      [2.1, 4.3, 6.5]
    ],
    "linepoints_list": [
      [[10, 15], [10, 16], [10, 17]],
      [[20, 30], [20, 31], [20, 32]]
    ],
    "confidence_list": [0.95, 0.87],
    "class_ids": [1.0, 2.0],
    "curve_type": ["cosine", "poly"]
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
    results=results_filtered,
    data_ndarray=data_ndarray
)

plot_manager = QuantumPlotPltManager()
plot_manager.plot_quantum_data(
    data_type='npy',
    task_type=NNTaskName.S21VFLUX.value,
    save_path=save_path_png,
    results=results_filtered,
    data_ndarray=data_ndarray
)

```