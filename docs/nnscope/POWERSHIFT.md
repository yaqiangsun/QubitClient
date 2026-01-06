# POWERSHIFT 任务接口文档

## 概述

POWERSHIFT 是 NNScope 中的一个任务，用于对二维频谱数据进行曲线分割。该任务支持多种曲线拟合类型，包括多项式拟合和余弦拟合。

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
| task_type | NNTaskName | 是 | 任务类型，固定为`NNTaskName.POWERSHIFT`|
| curve_type | CurveType | 是 | 任务类型，固定为`CurveType.AUTO(返回poly和cosine的最优解)`|

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

   ```python
    {
        "image": {
            "Q0": [x, y, value...],    # len=10
            "Q1": [x, y, value...],    # len=10
            ...
        }
    }
    ```
x: 一维 np.ndarray,shape(A,),表示频率数据
y: 一维 np.ndarray,shape(B,),表示读取强度amp
value: 二维 np.ndarray,shape(B,A),每个点表示强度

每个量子比特对应一个键（如 "Q0"），值为 [x, y, value...] 的列表，列表长度一共为10

#### 调用示例

```python
# 使用文件路径

response = client.request(file_list=["data/singlepath/file1.npy", "data/singlepath/file2.npy"],task_type=NNTaskName.POWERSHIFT,curve_type=CurveType.AUTO)

dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

# 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=NNTaskName.POWERSHIFT, curve_type=CurveType.AUTO)

```

### 获取结果

```python


response_data = client.get_result(response)
threshold = 0.5
results_filtered = client.get_filtered_result(response, threshold, NNTaskName.POWERSHIFT.value)

results = client.get_result(response=response_data)  

# response_data 和 response_data_filtered 分别是阈值筛选前和筛选后的结果
```

## 返回值格式

返回的结果是一个字典：

```json
[
  {
    "q_list": [str, ...],     // 量子的名字列表
    "linepoints_list": [[[int, int], ...], ...], // 每条线段的点坐标列表
    "confs": [float, ...],         // 每条线段的置信度
    "class_num_list": [float, ...],         // 每条线段的分割标签class 1~5共五种
  },
  ...
]
```




### 字段说明

| 字段名 | 类型                                 | 描述 |
|--------|------------------------------------|------|
| q_list | List[str]                        | 所有量子的名称 |
| linepoints_list | List[List[[row_index, col_index]]] | 每条线段的点坐标列表，每个点包含行索引和列索引 |
| confs | List[float]                        | 每条线段的置信度，表示检测的可靠性 |
| class_num_list | List[float]                        | 每条线段的分割标签 |



### 示例结果

```python
[
  {
    "q_list":  ['Q0', 'Q1'],
    "linepoints_list": [[[18.4, 0.7], [24.3, 9.3], [24.3, 21.0]],
						[[21.1, 0.1], [21.1, 10.3]]],
    "confs": [0.95, 0.87],
    "class_num_list": [1, 2],
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
    task_type=NNTaskName.POWERSHIFT.value,
    save_path=save_path_html,
    results=results_filtered,
    data_ndarray=data_ndarray
)

plot_manager = QuantumPlotPltManager()
plot_manager.plot_quantum_data(
    data_type='npy',
    task_type=NNTaskName.POWERSHIFT.value,
    save_path=save_path_png,
    results=results_filtered,
    data_ndarray=data_ndarray
)

```