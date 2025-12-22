# SPECTRUM 任务接口文档

## 概述

SPECTRUM 是 Scope 中的一个任务，用于对量子比特的进行基于 **AMPD算法** 的峰值检测，返回每个量子比特的峰值位置、可信度及峰宽


---

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitScopeClient, TaskName

client = QubitScopeClient(url="http://your-server-address:port", api_key="your-api-key")
```

### 请求参数

| 参数名      | 类型                                      | 必需 | 描述                                                                 |
|-------------|-------------------------------------------|------|----------------------------------------------------------------------|
| `file_list` | `list[str \| dict[str, np.ndarray]]`      | 是   | 数据文件列表，支持 `.npy` 文件路径或 `numpy` 数组                     |
| `task_type` | `TaskName`                                | 是   | 任务类型，固定为 `TaskName.SPECTRUM`                                    |                             |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": [x_array, amp_array],   
            "Q1": [x_array, amp_array],
            ...
        }
    }
    ```

    x_array: 一维 np.ndarray，表示时间点
    amp_array: 一维 np.ndarray，表示信号强度
    每个量子比特对应一个键（如 "Q0"），值为 [x, amp] 的列表

#### 调用示例

```python
# 使用文件路径
response = client.request(
    file_list=["data/spectrum/file1.npy", "data/spectrum/file2.npy"],
    task_type=TaskName.SPECTRUM
)

# 使用numpy数组
import numpy as np
data_ndarray = np.load("file1.npy", allow_pickle=True)
response = client.request(
    file_list=[data_ndarray],
    task_type=TaskName.SPECTRUM
)
```

### 获取结果

```python
results = client.get_result(response=response)
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
{
    "type":"spectrum",
    "results":[
        {
            "peaks_list":[[float,float,...], ...],
            "confidences_list":[[float,float,...], ...],
            "mean_cut_widths_list":[[float,float,...], ...],
            "status":"success" | "failed"
            }]}, 
```

peaks_list[i]: 第 i 个量子比特的峰所在位置（x值）（一个量子比特可能存在多个峰）
confidences_list[i]: 第 i 个量子比特每个峰的可信度
mean_cut_widths_list[i]: 第 i 个量子比特的每个峰的宽度

### 字段说明

| 字段名           | 类型                   | 描述 |
|------------------|------------------------|------|
| `params_list`    | `List[List[float]]`    | 每个量子比特峰所在位置（x值），一个量子比特可能存在多个峰 |
| `r2_list`        | `List[List[float]]`    | 每个量子比特每个峰的可信度，范围 `[0, 1]`，越接近 1 越可信 |
| `fit_data_list`  | `List[List[float]]`    | 每个量子比特的每个峰的宽度 |
| `status`         | `str`                  | 处理状态：`"success"` 或 `"failed"` |

### 示例结果

```python
{
    "type":"spectrum",
    "results":
    [
        {"peaks_list":
        [
            [4767999999.999981,4909999999.999966],
            [4669999999.999992,4801999999.999977,4885999999.999969],
            [4639999999.999995,4677999999.999991,4715999999.999987,4743999999.999984,4771999999.999981,4835999999.999973,4875999999.9999695,4911999999.999966,4943999999.999962]
            ],
        "confidences_list":
        [
            [1.0,0.572255061220645],
            [0.09499978349220113,0.39529601333658876,1.0],
            [0.11149322544140107,0.07719006783692754,0.27999999999999997,0.33086725953215457,0.877272727272727,0.10810872394573999,0.6059154143176955,0.6110235006617278,0.28481649185658386]
            ],
        "mean_cut_widths_list":
        [
            [51999999.99999428,49999999.99999428],
            [5999999.999999046,25999999.99999714,57999999.999993324],
            [17999999.999998093,0.0,4000000.0,13999999.999998093,41999999.999996185,3999999.9999990463,49999999.99999428,49999999.99999428,27999999.99999714]
            ],
        "status":"success"
        }
    ]
}
```

## 可视化

处理结果可以通过内置的绘图工具进行可视化：

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

# 使用Plotly绘制（HTML）
plot_manager = QuantumPlotPlyManager()
ply_plot_manager.plot_quantum_data(
    data_type='npy',
    task_type=TaskName.SPECTRUM.value,
    save_path=save_path_html,
    result=result,
    dict_param=item
)

# 使用Matplotlib绘制（PNG）
plot_manager = QuantumPlotPltManager()
plt_plot_manager.plot_quantum_data(
    data_type='npy',
    task_type=TaskName.SPECTRUM.value,
    save_path=save_path_png,
    result=result,
    dict_param=item
)
```