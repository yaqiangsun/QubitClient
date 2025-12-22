# S21VFLUX 任务接口文档

## 概述

S21VFLUX 是 Scope 中的一个任务，用于对二维频谱数据进行曲线分割。该任务支持多种曲线拟合类型，包括多项式拟合和余弦拟合。

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitScopeClient
from qubitclient import TaskName


client = QubitScopeClient(url=url, api_key=api_key)
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| file_list | list[np.ndarray] | 是 | 数据列表，支持.npy的numpy数组 |
| task_type | TaskName | 是 | 任务类型，固定为`TaskName.S21VFLUX` |

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

response = client.request(file_list=["data/singlepath/file1.npy", "data/singlepath/file2.npy"], task_type=TaskName.S21VFLUX)


dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

    # 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=TaskName.S21VFLUX)

```

### 获取结果

```python


response_data = client.get_result(response)
threshold = 0.5
response_data_filtered = client.get_filtered_result(response,threshold,TaskName.S21VFLUX.value)

results = client.get_result(response=response_data)  
#results = client.get_result(response=response_data_filtered)
# response_data 和 response_data_filtered 分别是阈值筛选前和筛选后的结果
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
[
  {
    "coscurves_list": [[[[float]]]],     // 表示余弦曲线点集合
    "cosconfs_list": [[float]],     // 表示余弦曲线置信度
    "lines_list": [[[[float]]]],     // 表示直线点集合
    "lineconfs_list":[[float]]     // 表示直线置信度
  },
  ...
]
```




### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| coscurves_list | [[[[float]]]] | 表示余弦曲线点集合 |
| cosconfs_list | [[float]] | 表示余弦曲线置信度 |
| lines_list | [[[[float]]]] | 表示直线点集合 |
| lineconfs_list | [[float]] | 表示直线置信度 |




### 示例结果

```python
[
  {
    "coscurves_list": [[[[-1,6.843e9],[-0.9,6.844e9],...]],[[[-0.8,6.833e9],[-1,6.847e9],...]]],
    "cosconfs_list": [[0.6],[0.6]]，
    "lines_list": [[[[-1,6.943e9],[-0.9,6.94e9],...]],[[[-0.8,6.933e9],[-1,6.847e9],...]]],
    "lineconfs_list": [[0.5],[0.6]]
  }
]
```

## 可视化

处理结果可以通过内置的绘图工具进行可视化：

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

ply_plot_manager = QuantumPlotPlyManager()
plt_plot_manager = QuantumPlotPltManager()
for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
  save_path_prefix = f"./tmp/client/result_{TaskName.S21VFLUX.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.S21VFLUX.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.S21VFLUX.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )

```