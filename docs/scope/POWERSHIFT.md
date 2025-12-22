# POWERSHIFT 任务接口文档

## 概述

POWERSHIFT 是 Scope 中的一个任务，用于对量子比特的进行分类以及关键点提取，返回每个量子比特的类别、关键点及可信度


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
| `task_type` | `TaskName`                                | 是   | 任务类型，固定为 `TaskName.POWERSHIFT`                                    |                             |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": [x_array, y_array, value_array],   
            "Q1": [x_array, y_array, value_array],
            ...
        }
    }
    ```

    x_array: 一维 np.ndarray，表示x轴坐标
    y_array: 一维 np.ndarray，表示y轴坐标
    value_array: 一维 np.ndarray，表示信号强度
    每个量子比特对应一个键（如 "Q0"），值为 [x, y, value] 的列表

#### 调用示例

```python
# 使用文件路径
response = client.request(
    file_list=["data/powershift/file1.npy", "data/powershift/file2.npy"],
    task_type=TaskName.POWERSHIFT
)

# 使用numpy数组
import numpy as np
data_ndarray = np.load("file1.npy", allow_pickle=True)
response = client.request(
    file_list=[data_ndarray],
    task_type=TaskName.POWERSHIFT
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
    "type":"powershift",
    "results":
    [
        {
            "q_list":["Q0","Q1",...],
            "confs":[float,...],
            "class_num_list":[int,...],
            "keypoints_list":
            [
                [
                    [float,float],...
                ],
                ...
            ],
            "status":"success" | "failed"
        },
        ...
    ]
}
```

q_list[i]: 第 i 个量子比特
confs[i]: 第 i 个量子比特关键点的可信度
class_num_list[i]: 第 i 个量子比特的类别
keypoints_list[i]: 第 i 个量子比特的关键点序列

### 字段说明

| 字段名           | 类型                   | 描述 |
|------------------|------------------------|------|
| `q_list`          | `List[char]`    | 当前npy文件包含的量子比特 |
| `confs`        | `List[float]`    | 每个量子比特每个关键点构成的线的可信度，范围 `[0, 1]`，越接近 1 越可信 |
| `class_num_list`  | `List[int]`    | 每个量子比特的类别，取值范围为`[1，2，3，4，5]`，其中class1：垂直于x轴，class2：两端都有垂直部分中部倾斜，class3：仅有底部垂直随后倾斜，class4：整体倾斜向上，class5：无信息 |
|'keypoints_list'|`List[List[List[float,float]]]`|每个量子比特的关键点，存储内容为坐标点，其中class1：[[顶部端点], [底部端点]]; class2：[[顶部端点], [上部拐点], [下部拐点], [底部端点]；class3：[[顶部端点], [拐点], [底部端点]]；class4：[[顶部端点], [底部端点]]；class5：[]|
| `status`         | `str`                  | 处理状态：`"success"` 或 `"failed"` |

### 示例结果

```python
{
    "type":"powershift",
    "results":
    [
        {"q_list":["Q0","Q1","Q2"],
        "confs":[0.1429,0.2198,0.6857],
        "class_num_list":[2,2,1],
        "keypoints_list":[
            [
                [6907600000.0,0.25],[6907600000.0,0.137545],[6908800000.0,0.0],[6908800000.0,0.12505]
            ],
            [
                [6963750000.0,0.25],[6963750000.0,0.187525],[6965750000.0,0.0],[6965750000.0,0.12505]
            ],
            [
                [7026200000.0,0.0],[7026200000.0,0.25]
            ]
        ],
        "status":"success"
        },
        ...
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
    task_type=TaskName.POWERSHIFT.value,
    save_path=save_path_html,
    result=result,
    dict_param=item
)

# 使用Matplotlib绘制（PNG）
plot_manager = QuantumPlotPltManager()
plt_plot_manager.plot_quantum_data(
    data_type='npy',
    task_type=TaskName.POWERSHIFT.value,
    save_path=save_path_png,
    result=result,
    dict_param=item
)
```