# RABICOS 任务接口文档

## 概述

RABICOS 是 Scope 中的一个任务，用于对 Rabi 余弦振荡信号进行峰值检测，返回每个量子比特的第一个峰值位置及置信度

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitScopeClient, TaskName

client = QubitScopeClient(url="http://your-server-address:port", api_key="your-api-key")
```

### 请求参数

| 参数名      | 类型                        | 必需 | 描述                                                                 |
|-------------|-----------------------------|------|----------------------------------------------------------------------|
| `file_list` | `list[str\|dict[str,np.ndarray]]`     | 是   | 数据文件列表，支持 `.npy` 文件路径或 `numpy` 数组                     |
| `task_type` | `TaskName`                  | 是   | 任务类型，固定为 `TaskName.RABICOS`                                  |

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
response = client.request(file_list=["data/rabicos/file1.npy", "data/rabicos/file2.npy"], task_type=TaskName.RABICOS)

dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

# 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=TaskName.RABICOS)
```

### 获取结果

```python
response_data = client.get_result(response)
threshold = 0.5
response_data_filtered = client.get_filtered_result(response, threshold, TaskName.RABICOS.value)

results = response_data_filtered.get("results")
# 或使用未过滤的结果
# results = response_data.get("results")
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
{
  "type": "rabicos",
  "results": [
    {
      "peaks": [[float], ...],
      "confs": [[float], ...],
      "status": "success" | "failed"
    },
    ...
  ]
}
```

peaks[i] 和 confs[i] 对应第 i 个量子比特；若某比特无峰，则为空列表 []。

### 字段说明


| 字段名   | 类型                   | 描述 |
|----------|------------------------|------|
| `peaks`  | `List[List[float]]`    | 每个量子比特检测到的峰值时间位置 |
| `confs`  | `List[List[float]]`    | 每个峰值的置信度（范围 [0, 1]） |
| `status` | `str`                  | 处理状态：`"success"` 或 `"failed"` |

### 示例结果

```python
{
  "type": "rabicos",
  "results": [
    {
      "peaks": [[0.02]],
      "confs": [[0.0911383107304573]],
      "status": "success"
    },
    {
      "peaks": [[0.29], [0.33], [0.71], [0.3], [0.14], [0.36], [0.28], [0.22], [0.15], [0.27]],
      "confs": [[0.989116370677948], [0.9622823596000671], [0.34767669439315796], [0.9559057354927063], [0.03568170592188835], [0.8894426226615906], [0.05686560645699501], [0.29671725630760193], [0.10239258408546448], [0.08909483999013901]],
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
  save_path_prefix = f"./tmp/client/result_{TaskName.RABICOS.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.RABICOS.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.RABICOS.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )

```