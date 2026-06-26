# POWERSHIFT 任务接口文档

## 概述

POWERSHIFT 是 NNScope 中的一个任务，用于对二维频谱数据进行曲线分割。该任务支持多种曲线拟合类型，包括多项式拟合和余弦拟合。

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitNNScopeClient
from qubitclient import NNTaskName


client = QubitNNScopeClient()
```

### 请求参数


| 参数名 | 类型 | 必需 | 描述                                         |
|--------|------|------|-----------|
| file_list | list[str\|dict[str,np.ndarray]\| np.ndarray]  | 是 | 数据文件列表，支持.npy或numpy数组 |
| task_type | NNTaskName | 是 | 任务类型，固定为`NNTaskName.POWERSHIFT`|

### 数据格式

#### 输入格式

NPY文件需要包含一个字典：

```python
{
    "image": {
        "Q0": (x, y, value, ...),   # tuple, length>=3
        "Q1": (x, y, value, ...),
        ...
    }
}
```

每个量子比特对应一个键（如 "Q0"），值为 tuple，至少包含前3个元素：

| 元素 | 类型 | 描述 |
|------|------|------|
| x | np.ndarray, shape=(A,) | 频率数据，dtype=float64 |
| y | np.ndarray, shape=(B,) | 读取强度/功率，dtype=float64 |
| value | np.ndarray, shape=(B, A) | 二维频谱数据，dtype=float32 |
| ... | tuple | 可选的附加元素 |

#### 调用示例

```python
# 使用文件路径
response = client.request(file_list=["data/singlepath/file1.npy", "data/singlepath/file2.npy"], task_type=NNTaskName.POWERSHIFT)
```

或使用加载后的数据：

```python
from qubitclient.scope.utils.data_parser import load_npy_file

dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

# 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=NNTaskName.POWERSHIFT)
```

### 获取结果

```python


response_data = client.get_result(response)
threshold = 0.5
results_filtered = client.get_filtered_result(response, threshold, NNTaskName.POWERSHIFT.value)
results_filtered = results_filtered.get("results")

# response_data 和 response_data_filtered 分别是阈值筛选前和筛选后的结果
```

## 返回值格式

返回的结果是一个列表：

```json
[
  {
    "q_list": [str, ...],                  // 量子的名字列表
    "keypoints_list":[[[float, float], ...]], // 每条线段的端点坐标列表
    "confs": [float, ...],                 // 每条线段的置信度
    "class_num_list": [int, ...],          // 每条线段的分割标签 (1~5共五种)
  },
  ...
]
```

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| q_list | List[str] | 所有量子的名称 |
| keypoints_list | List[List[List[float]]] | 每条线段的端点坐标列表，每个端点包含两个浮点数坐标 |
| confs | List[float] | 每条线段的置信度，表示检测的可靠性 |
| class_num_list | List[int] | 每条线段的分割标签，取值 1~5 共五种 |



### 示例结果

```python
[
  {
    "q_list": ['Q0', 'Q1'],
    "keypoints_list": [[[18.4, 0.7], [24.3, 9.3], [24.3, 21.0], [21.1, 0.1], [21.1, 10.3]]],
    "confs": [0.95, 0.87, 0.65, 0.92, 0.78],
    "class_num_list": [1, 2, 3, 1, 4]
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
    result=result_filter,
    dict_param=dict_param
)

plot_manager = QuantumPlotPltManager()
plot_manager.plot_quantum_data(
    data_type='npy',
    task_type=NNTaskName.POWERSHIFT.value,
    save_path=save_path_png,
    result=result_filter,
    dict_param=dict_param
)

```