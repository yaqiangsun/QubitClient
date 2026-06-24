# OPTREADFREQ 任务接口文档

## 概述

OPTREADFREQ 是 Scope 中的一个任务，返回每个量子比特的两条s21曲线距离最大处对应索引

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitScopeClient, TaskName

client = QubitScopeClient(url="http://your-server-address:port", api_key="your-api-key")
```

### 请求参数

| 参数名      | 类型                                      | 必需 | 描述                          |
|-------------|-------------------------------------------|------|-----------------------------|
| `file_list` | `list[str \| dict[str, np.ndarray]]`      | 是                           | 数据文件列表，支持 `.npy` 文件路径或 `numpy` 数组                     |
| `task_type` | `TaskName`                                | 是   | 任务类型，固定为 `TaskName.OPTREADFREQ` |                             |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": [freq_array,s0_array, s1_array],   
            "Q1": [freq_array,s0_array, s1_array],
            ...
        }
    }
    ```

    freq_array: 二维 np.ndarray，表示频率
    s0_array: 一维 np.ndarray，表示第一条s21
    s1_array: 一维 np.ndarray，表示第二条s21

    每个量子比特对应一个键（如 "Q0"），值为 [freq,s0, s1] 的列表

#### 调用示例

```python
# 使用文件路径
response = client.request(
    file_list=["data/optreadfreq/file1.npy", "data/optreadfreq/file2.npy"],
    task_type=TaskName.OPTREADFREQ
)

# 使用numpy数组
import numpy as np
data_ndarray = np.load("file1.npy", allow_pickle=True)
response = client.request(
    file_list=[data_ndarray],
    task_type=TaskName.OPTREADFREQ
)
```

### 获取结果

```python
response_data = client.get_result(response)
threshold = 0.5
response_data_filtered = client.get_filtered_result(response, threshold, TaskName.OPTREADFREQ.value)

results = response_data_filtered.get("results")
# 或使用未过滤的原始结果
# results = response_data.get("results")
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
{
  "type": "optreadfreq",
  "results": [
    {
      "peak_list": [float, ...]
      "status": "success" | "failed"
    },
    ...
  ]
}
```

peak_list[i]: 第 i 个量子比特的峰值对应索引 peak


### 字段说明

| 字段名           | 类型                  | 描述                            |
|------------------|-----------------------|-------------------------------|
| `peak_list`    | `List[float]`    | 每个量子比特,峰值对应索引               |
| `status`         | `str`                 | 处理状态：`"success"` 或 `"failed"` |

### 示例结果

```python
{
  "type": "optreadfreq",
  "results": [
    {
      "peak_list": [19, 20, 11],
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
  save_path_prefix = f"./tmp/client/result_{TaskName.OPTREADFREQ.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.OPTREADFREQ.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.OPTREADFREQ.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )

```