# T1FIT 任务接口文档

## 概述

T1FIT 是 Scope 中的一个任务，用于对量子比特的弛豫信号（T1 衰减）进行指数拟合，返回每个量子比特的拟合参数、拟合曲线、拟合优度及处理状态
$$
y = A \cdot e^{-x / T1} + B
$$

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
| `task_type` | `TaskName`                                | 是   | 任务类型，固定为 `TaskName.T1FIT`                                    |                             |

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
    file_list=["data/t1fit/file1.npy", "data/t1fit/file2.npy"],
    task_type=TaskName.T1FIT
)

# 使用numpy数组
import numpy as np
data_ndarray = np.load("file1.npy", allow_pickle=True)
response = client.request(
    file_list=[data_ndarray],
    task_type=TaskName.T1FIT
)
```

### 获取结果

```python
response_data = client.get_result(response)
threshold = 0.5
response_data_filtered = client.get_filtered_result(response, threshold, TaskName.T1FIT.value)

results = response_data_filtered.get("results")
# 或使用未过滤的原始结果
# results = response_data.get("results")
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
{
  "type": "t1fit",
  "results": [
    {
      "params_list": [[A, T1, B], ...],
      "r2_list": [float, ...],
      "fit_data_list": [[float, ...], ...],
      "status": "success" | "failed"
    },
    ...
  ]
}
```

params_list[i]: 第 i 个量子比特的拟合参数 [A, T1, B]
fit_data_list[i]: 第 i 个量子比特在原始时间点上的拟合值
r2_list[i]: 第 i 个量子比特的 拟合优度

### 字段说明

| 字段名           | 类型                   | 描述 |
|------------------|------------------------|------|
| `params_list`    | `List[List[float]]`    | 每个量子比特的拟合参数 `[A, T1, B]`，其中 `A` 为初始幅度，`T1` 为弛豫时间（µs），`B` 为基线偏移 |
| `r2_list`        | `List[float]`          | 每个量子比特的 R² 拟合优度，范围 `[0, 1]`，越接近 1 拟合越好 |
| `fit_data_list`  | `List[List[float]]`    | 每个量子比特在原始时间点上的拟合曲线值（与输入 `x` 长度一致） |
| `status`         | `str`                  | 处理状态：`"success"` 或 `"failed"` |

### 示例结果

```python
{
  "type": "t1fit",
  "results": [
    {
      "params_list": [
        [0.9606002214647686, 27.10772731801952, 0.16825506437258225],
        [1.0316859089502217, 11.33354956261001, -0.00035147308286919733],
        [0.3708991911338009, 30.100798502307462, -0.019399226855197578]
      ],
      "r2_list": [0.9685890006192518, 0.9694060481154481, 0.0567193074573189],
      "fit_data_list": [
        [0.9605647857201113, 0.9605605506147538, ...],
        [1.0315948835931699, 1.0315840050042837, ...],
        [...]
      ],
      "status": "success"
    }
  ]
}
```

## 可视化

处理结果可以通过内置的绘图工具进行可视化：

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

ply_plot_manager = QuantumPlotPlyManager()
plt_plot_manager = QuantumPlotPltManager()

for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
  save_path_prefix = f"./tmp/client/result_{TaskName.T1FIT.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.T1FIF.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.T1FIF.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )

```