# S21VFLUX 任务接口文档

## 概述

DRAG 是 Scope 中的一个任务，用于对两组一维数据进行多项时拟合,交叉点检测及其置信度分析。

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitScopeClient
from qubitclient import TaskName


client = QubitScopeClient(url=url, api_key=api_key)
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述                      |
|--------|------|------|-------------------------|
| file_list | list[np.ndarray] | 是 | 数据列表，支持.npy的numpy数组     |
| task_type | TaskName | 是 | 任务类型，固定为`TaskName.DRAG` |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": [*,*,x,[y0,y1]],   
            "Q1": [*,*,x,[y0,y1]],
            ...
        }
    }
    ```

x: 一维 np.ndarray,shape(A,),表示横坐标
y0: 一维 np.ndarray,shape(A,),表示第一组数据纵坐标
y1: 一维 np.ndarray,shape(A,),表示第二组数据纵坐标

每个量子比特对应一个键（如 "Q0"），值为 [*,*,x,[y0,y1]] 的列表

#### 调用示例

```python
# 使用文件路径

response = client.request(file_list=["data/singlepath/file1.npy", "data/singlepath/file2.npy"], task_type=TaskName.DRAG)


dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

    # 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=TaskName.DRAG)

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
    "x_pred_list": [[float]],     // 表示拟合曲线的横坐标
    "y0_pred_list": [[float]],     // 表示拟合曲线0的纵坐标
    "y1_pred_list": [[float]],     // 表示拟合曲线1的纵坐标
    "intersections_list":[[[float]]],     // 表示曲线交点坐标
     "intersections_confs_list": [[float]],// 表示曲线交点置信度
  },
  ...
]
```
### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| x_pred_list | [[float]] | 表示拟合曲线的横坐标 |
| y0_pred_list | [[float]] | 表示拟合曲线0的纵坐标 |
| y1_pred_list | [[float]] | 表示拟合曲线1的纵坐标 |
| intersections_list | [[[float]]] | 表示曲线交点坐标 |
| intersections_confs_list | [[float]] | 表示曲线交点置信度 |




### 示例结果

```python
[
  {
    "x_pred_list": [[0.1,0.2,0.3],[0.1,0.2,0.3]],
    "y0_pred_list": [[0.1,0.2,0.3],[0.1,0.2,0.3]]，
    "y1_pred_list": [[0.1,0.2,0.3],[0.1,0.2,0.3]],
    "intersections_list":[[[0.1,0.2],[0.3,0.2]]],
    "intersections_confs_list": [[0.6],[0.6]]
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
  save_path_prefix = f"./tmp/client/result_{TaskName.DRAG.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.DRAG.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.DRAG.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )

```