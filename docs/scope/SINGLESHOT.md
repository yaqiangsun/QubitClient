# SINGLESHOT 任务接口文档

## 概述

SINGLESHOT 是 Scope 中的一个任务，用于对两组离散复数信号进行分布特征分析和分类。

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitScopeClient
from qubitclient import TaskName


client = QubitScopeClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| file_list | list[np.ndarray] | 是 | 数据列表，支持.npy的numpy数组 |
| task_type | TaskName | 是 | 任务类型，固定为`TaskName.SINGLESHOT` |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": (x,y,z),   
            "Q1": (x,y,z),
            ...
        }
    }
    ```
其中：
- x: np.ndarray, shape (A,), 表示复数信号0 s0_array
- y: np.ndarray, shape (A,), 表示复数信号1 s1_array
- z: bool, False 保留字段无具体含义，可以忽略

每个量子比特对应一个键（如 "Q0"），值为 (x,y,z) 

#### 调用示例

```python
# 使用文件路径

response = client.request(file_list=["data/singlepath/file1.npy", "data/singlepath/file2.npy"], task_type=TaskName.SINGLESHOT)


dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

    # 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=TaskName.SINGLESHOT)

```

### 获取结果

```python

response_data = client.get_result(response)
results = response_data.get("results")
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
[
  {
    "sep_score_list": List[float],        // 分离程度 separation_degree
    "threshold_list": List[float],        // 分类决策阈值
    "threshold_norm_list": List[float],        // 归一化分类决策阈值
    "phi_list": List[float],              // 最佳投影方向角度
    "signal_list": List[List[List[float]]], // 信号投影数据
    "idle_list": List[List[List[float]]],   // 空闲信号投影数据
    "params_list": List[List[List[float]]], // 椭圆拟合参数,列表最后两个索引位置为中心点(实部，虚部)
    "std_list": List[List[Union[float, List[List[float]]]]], // 标准差、方差、协方差信息
    "cdf_list": List[List[List[float]]],   // 累积分布函数数据
    "status": str                          // 处理状态
  },
  ...
]
```
### 字段说明
| 字段名 | 类型 | 描述 |
|--------|------|------|
| sep_score_list | List[float] |分离程度 separation_degree |
| threshold_list | List[float] | 分类决策阈值 |
| threshold_norm_list | List[float] | 归一化分类决策阈值 |
| phi_list | List[float] | 最佳投影方向的角度 |
| signal_list | List[List[List[float]]] | 信号投影 |
| idle_list | List[List[List[float]]] | 空闲信号投影 |
| params_list | List[List[List[float]]] | 椭圆拟合参数,列表最后位置为中心点(实部，虚部) |
| std_list | std_list: List[List[Union[float, List[List[float]]]]] | 数据的标准差、方差、协方差信息 |
| cdf_list | List[List[List[float]]] | 累积分布函数数据 |
| status | str | 处理状态，'success' 表示成功 |


### 示例结果

```python
[
  {
    "sep_score_list": [1.64,2.31],
    "threshold_list": [423.32,3345.32],
    "threshold_norm_list": [0.18,0.24],
    "phi_list": [-2.1, -2.2],
    "signal_list": [[[-3.6,-3.8,...],[-3.5,-3.9,...],...],[[-3.2,-3.4,...],[-3.4,-3.1,...],...]],
    "idle_list": [[[-3.6,-3.8,...],[-3.5,-3.9,...],...],[[-3.2,-3.4,...],[-3.4,-3.1,...],...]],
    "params_list": [[[-3.6,-3.8,...，(1.0,2.0)],[-3.5,-3.9,...，(1.0,2.0)],...],[[-3.2,-3.4,...，(1.0,2.0)],[-3.4,-3.1,...，(1.0,2.0)],...]],
    "std_list": [
      [1.5,1.5,1.2,1.3,1.4,[[1.9,-0.06],[1.1,-0.03]],[[1.9,-0.06],[1.1,-0.03]]],
      [1.5,1.5,1.2,1.3,1.4,[[1.9,-0.06],[1.1,-0.03]],[[1.9,-0.06],[1.1,-0.03]]],
    ],
    "cdf_list": [[[-3.6,-3.8,...],[-3.5,-3.9,...],...],[[-3.2,-3.4,...],[-3.4,-3.1,...],...]],
    "status":'success'
  },  
  ...
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
  save_path_prefix = f"./tmp/client/result_{TaskName.SINGLESHOT.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.SINGLESHOT.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.SINGLESHOT.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )

```