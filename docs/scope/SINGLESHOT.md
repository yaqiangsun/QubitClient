# SINGLESHOT 任务接口文档

## 概述

SINGLESHOT 是 Scope 中的一个任务，用于对两组离散复数信号进行分布特征分析和分类。

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
| task_type | TaskName | 是 | 任务类型，固定为`TaskName.SINGLESHOT` |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": [s0_array, s1_array],   
            "Q1": [s0_array, s1_array],
            ...
        }
    }
    ```

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
if hasattr(response, 'parsed'):
    response_data = response.parsed
elif isinstance(response, dict):
    response_data = response
else:
    response_data = {}
results = client.get_result(response=response_data)
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
[
   {
    "threshold_list": [float],     // 分类决策阈值，在投影轴上的分类阈值以最小化分类误差
    "sep_score_list": [float], // 分离程度 separation_degree
    "phi_list": [float],         // 最佳投影方向的角度，使两组信号在该方向上具有最大可区分性，给出投影轴
    "signal_list": [[[float]]],         // 信号投影，复数信号投影到一维实轴（投影轴）
    "idle_list": [[[float]]],         // 空闲信号投影，复数信号投影到一维实轴（投影轴）
    "params_list": [[[float]]],         //  椭圆拟合参数
    "std_list": [[float,float,float,float,[[float]],[[float]]]], // 数据的标准差，方差，协方差信息
    "cdf_list": [[[float]]],         // 累积分布函数数据
  },
  ...
]
```






### 字段说明

| 字段名 | 类型 | 描述                                 |
|--------|------|------------------------------------|
| threshold_list | [float] | 分类决策阈值，在投影轴上的分类阈值以最小化分类误差          |
| sep_score_list | [float] | 分离程度 separation_degree             |
| phi_list | [float] | 最佳投影方向的角度，使两组信号在该方向上具有最大可区分性，给出投影轴 |
| signal_list | [[[float]]] | 信号投影，复数信号投影到一维实轴（投影轴）              |
| idle_list | [[[float]]] | 空闲信号投影，复数信号投影到一维实轴（投影轴）            |
| params_list | [[[float]]] | 椭圆拟合参数                             |
| std_list | [[float,float,float,float,[[float]],[[float]]]] | 数据的标准差，方差，协方差信息                    |
| cdf_list | [[[float]]] | 累积分布函数数据                           |

### 示例结果

```python
[
  {
    "params_list": [1.64,2.31],
    "sep_score_list": [0.18,0.24],
    "phi_list": [-2.1, -2.2]
    "signal_list": [
      [[-3.6,-3.8,...]，
        [-3.5,-3.9,...]，]
      [[-3.2,-3.4,...]，
        [-3.4,-3.1,...]，]
      [[-3.1,-3.2,...]，
        [-3.1,-3.4,...]，]
      [[-3.4,-3.4,...]，
        [-3.7,-3.1,...]，]
    ]，
    "idle_list": [
      [[-0.7,1.5,...]，
        [-1.5,-2.9,...]，]
      [[-1.2,-1.4,...]，
        [-2.4,-0.1,...]，]
      [[-1.1,-3.2,...]，
        [-2.1,-2.4,...]，]
      [[-0.4,-1.4,...]，
        [-2.7,-1.1,...]，]
    ]，
    "params_list": [
      [[0.5,5.5,...]，
        [2.5,1.9,...]，]
      [[1.2,2.4,...]，
        [2.4,2.1,...]，]
      [[1.1,3.2,...]，
        [2.1,2.4,...]，]
      [[0.4,1.4,...]，
        [2.7,1.1,...]，]
    ]，
      "std_list": [
      [1.5,1.5,1.2,1.3,1.4,[[1.9,-0.06],[1.1,-0.03]]]，
      [1.1,1.3,1.5,1.1,1.2,[[1.3,-0.06],[1.5,-0.03]]]，
    ]，
      "cdf_list": [
      [[-3.72,-3.73,...]，
        [-3.72,-3.73,...]，]
      [[-3.71,-3.74,...]，
        [-3.78,-3.71,...]，]
      [[-3.73,-3.732,...]，
        [-3.72,-3.76,...]，]
      [[-3.75,-3.73,...]，
        [-3.71,-3.73,...]，]
    ]，
    
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