# T1FIT 任务接口文档

## 概述

RB 是 Scope 中的一个任务，用于对量子比特的随机基准测试（Randomized Benchmarking）数据进行指数衰减拟合，返回每个量子比特的拟合参数、拟合曲线、拟合优度及处理状态。


$$
P(x) = A \cdot p^x + B
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
| `task_type` | `TaskName`                                | 是   | 任务类型，固定为 `TaskName.RB`                                    |                             |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": [x_array, [amp_array,other_amp_array],   
            "Q1": [x_array, [amp_array,other_amp_array],
            ...
        }
    }
    ```

    x_array: 一维 np.ndarray，表示时间点
    amp_array: 一维 np.ndarray，表示信号强度
    每个量子比特对应一个键（如 "Q0"）

#### 调用示例

```python
# 使用文件路径
response = client.request(
    file_list=["data/rb/file1.npy", "data/rb/file2.npy"],
    task_type=TaskName.RB
)

# 使用 numpy 数组
import numpy as np
data_ndarray = np.load("file1.npy", allow_pickle=True)
response = client.request(
    file_list=[data_ndarray],
    task_type=TaskName.RB
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
  "type": "rb",
  "results": [
    {
      "params_list": [[A, p, B], ...],
      "r2_list": [float, ...],
      "fit_data_list": [[float, ...], ...],
      "status": "success" | "failed"
    },
    ...
  ]
}
```

params_list[i]: 第 i 个量子比特的拟合参数 [A, p, B]
fit_data_list[i]: 第 i 个量子比特在原始时间点上的拟合值
r2_list[i]: 第 i 个量子比特的 拟合优度

### 字段说明

| 字段名           | 类型                   | 描述 |
|------------------|------------------------|------|
| `params_list`    | `List[List[float]]`    | 每个量子比特的拟合参数 [A, p, B]，其中 p 为衰减因子|
| `r2_list`        | `List[float]`          | 每个量子比特的 R² 拟合优度，范围 `[0, 1]`，越接近 1 拟合越好 |
| `fit_data_list`  | `List[List[float]]`    | 每个量子比特在原始点上的拟合曲线值（与输入 `x` 长度一致） |
| `status`         | `str`                  | 处理状态：`"success"` 或 `"failed"` |

### 示例结果

```python
{
  "type": "rb",
  "results": [
    {
      "params_list": [
        [0.2648, 0.9872, 0.5001],
        [0.3125, 0.9921, 0.4998],
        [0.2789, 0.9895, 0.5003]
      ],
      "r2_list": [0.9962, 0.9948, 0.9951],
      "fit_data_list": [
        [0.7642, 0.7551, 0.7463, ...],
        [0.8119, 0.8064, 0.8011, ...],
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
  save_path_prefix = f"./tmp/client/result_{TaskName.RB.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.RB.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.RB.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )

```