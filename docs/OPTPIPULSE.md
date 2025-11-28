# OPTPIPULSE 任务接口文档

## 概述

OPTPIPULSE 是 Scope 中的一个任务，用于对量子比特的 π 脉冲优化波形进行峰值检测，返回每个量子比特的共峰位置及置信度，适用于多波形共峰点提取

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
| `task_type` | `TaskName`                  | 是   | 任务类型，固定为 `TaskName.OPTPIPULSE`                               |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": [waveforms_array, x_array],   
            "Q1": [waveforms_array, x_array],
            ...
        }
    }
    ```

waveforms_array: 二维 np.ndarray，形状为 (n_waveforms, n_points)，表示多个波形
x_array: 一维 np.ndarray，表示时间点
每个量子比特对应一个键（如 "Q0"），值为 [waveforms, x] 的列表

#### 调用示例

```python
# 使用文件路径
response = client.request(file_list=["data/opt_pipulse/file1.npy", "data/opt_pipulse/file2.npy"], task_type=TaskName.OPTPIPULSE)

dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

# 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=TaskName.OPTPIPULSE)

```

### 获取结果

```python
response_data = client.get_result(response)
threshold = 0.5
response_data_filtered = client.get_filtered_result(response, threshold, TaskName.OPTPIPULSE.value)

results = response_data_filtered.get("results")
# 或使用未过滤的原始结果
# results = response_data.get("results")
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
{
  "type": "optpipulse",
  "results": [
    {
      "params": [[float], ...],
      "confs": [[float], ...],
      "status": "success" | "failed"
    },
    ...
  ]
}
```

params[i] 和 confs[i] 对应第 i 个量子比特的共峰位置列表；若某比特无共峰，则为空列表 []。

### 字段说明

| 字段名   | 类型                   | 描述 |
|----------|------------------------|------|
| `params` | `List[List[float]]`    | 每个量子比特检测到的共峰时间位置 |
| `confs`  | `List[List[float]]`    | 每个共峰的置信度（范围 [0, 1]） |
| `status` | `str`                  | 处理状态：`"success"` 或 `"failed"` |

### 示例结果

```python
{
  "type": "optpipulse",
  "results": [
    {
      "params": [
        [0.08235],
        [0.34865, 0.40090],
        [0.24323],
        [0.21787, 0.24465],
        [0.26750],
        [0.11500],
        [0.18900, 0.20745],
        [0.22342, 0.28283]
      ],
      "confs": [
        [0.37008],
        [0.31266, 0.24710],
        [0.78828],
        [0.34015, 0.26108],
        [0.69258],
        [0.72413],
        [0.35279, 0.19651],
        [0.25220, 0.35880]
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
  save_path_prefix = f"./tmp/client/result_{TaskName.OPTPIPULSE.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.OPTPIPULSE.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.OPTPIPULSE.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )

```