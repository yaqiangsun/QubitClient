# DELTA 任务接口文档

## 概述

DELTA 是 Scope 中的一个任务，用于对量子比特的频率偏移量进行测量和分析。

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
| `task_type` | `TaskName`                                | 是   | 任务类型，固定为 `TaskName.DELTA`                                    |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": (waveforms_array, x_array),
            "Q1": (waveforms_array, x_array),
            ...
        }
    }
    ```

    waveforms_array: 二维 np.ndarray，shape `(N_waveforms, M)`，表示各条扫描波形
    x_array: 一维 np.ndarray，shape `(M,)`，表示横轴（偏置/频率等）
    每个量子比特对应一个键（如 "Q0"），值为 `(waveforms_array, x_array)` 的元组（list 亦可）

#### 调用示例

```python
# 使用文件路径
response = client.request(
    file_list=["data/delta/file1.npy", "data/delta/file2.npy"],
    task_type=TaskName.DELTA
)

# 使用numpy数组
import numpy as np
data_ndarray = np.load("file1.npy", allow_pickle=True)
response = client.request(
    file_list=[data_ndarray],
    task_type=TaskName.DELTA
)
```

### 获取结果

```python
response_data = client.get_result(response)

results = response_data.get("results")
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
{
  "type": "delta",
  "results": [
    {
      "params": [[float, ...], [float, ...], ...],
      "confs": [[float, ...], [float, ...], ...],
      "status": "success" | "failed"
    },
    ...
  ]
}
```

params[i]: 第 i 个量子比特检测到的 Delta 峰位置列表
confs[i]: 第 i 个量子比特各峰对应的置信度，与 `params[i]` 一一对应

### 字段说明

| 字段名   | 类型                  | 描述 |
|----------|-----------------------|------|
| `params` | `List[List[float]]`   | 每个量子比特的 Delta 峰位置列表 |
| `confs`  | `List[List[float]]`   | 每个量子比特各峰的置信度，范围 `[0, 1]` |
| `status` | `str`                 | 处理状态：`"success"` 或 `"failed"` |

### 示例结果

```python
{
  "type": "delta",
  "results": [
    {
      "params": [[1.23e-6, 2.45e-6]],
      "confs": [[0.92, 0.85]],
      "status": "success"
    }
  ]
}
```

无有效峰时，`params` 对应元素为空列表 `[]`，`confs` 可能为 `[[0.0]]` 等占位值。

## 可视化

处理结果可以通过内置的绘图工具进行可视化：

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

ply_plot_manager = QuantumPlotPlyManager()
plt_plot_manager = QuantumPlotPltManager()

for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
  save_path_prefix = f"./tmp/client/result_{TaskName.DELTA.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.DELTA.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.DELTA.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )
```