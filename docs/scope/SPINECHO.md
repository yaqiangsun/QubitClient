# SPINECHO 任务接口文档

## 概述

SPINECHO 是 Scope 中的一个任务，用于对量子比特的 **Spin Echo（自旋回波）** 衰减信号进行拟合，提取每个量子比特的 $T_2$ 弛豫时间、拟合包络曲线、$R^2$ 拟合优度及处理状态。

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
| `task_type` | `TaskName`                                | 是   | 任务类型，固定为 `TaskName.SPINECHO`                                 |

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

    x_array: 一维 np.ndarray，表示延迟时间
    amp_array: 一维 np.ndarray，表示信号强度
    每个量子比特对应一个键（如 "Q0"），值为 [x, amp] 的列表

#### 调用示例

```python
# 使用文件路径
response = client.request(
    file_list=["data/spin_echo/file1.npy", "data/spin_echo/file2.npy"],
    task_type=TaskName.SPINECHO
)

dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

# 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=TaskName.SPINECHO)
```

### 获取结果

```python
response_data = client.get_result(response)
threshold = 0.5
response_data_filtered = client.get_filtered_result(response, threshold, TaskName.SPINECHO.value)

results = response_data_filtered.get("results")
# 或使用未过滤的原始结果
# results = response_data.get("results")
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果。每个量子比特（如 `Q0`）以字典键的形式返回拟合结果。

```json
{
  "type": "spinecho",
  "results": [
    {
      "status": "success" | "failed",
      "Q0": {
        "q_name": "Q0",
        "x": [float, ...],
        "amp": [float, ...],
        "envelope": [float, ...],
        "fit_envelope": [float, ...],
        "params": [float, ...],
        "T2": float,
        "r2": float,
        "success": true | false
      },
      "Q1": { ... }
    },
    ...
  ]
}
```

### 字段说明

**文件级字段**（`results[i]`）：

| 字段名   | 类型  | 描述 |
|----------|-------|------|
| `status` | `str` | 该文件整体处理状态：`"success"` 或 `"failed"` |

**量子比特级字段**（`results[i]["Q0"]` 等）：

| 字段名           | 类型                   | 描述 |
|------------------|------------------------|------|
| `q_name`         | `str`                  | 量子比特名称 |
| `x`              | `List[float]`          | 延迟时间序列 |
| `amp`            | `List[float]`          | 原始信号强度 |
| `envelope`       | `List[float]`          | 从原始信号提取的包络曲线 |
| `fit_envelope`   | `List[float]`          | 对 `envelope` 拟合后的包络曲线 |
| `params`         | `List[float]`          | 拟合参数数组 |
| `T2`             | `float`                | 自旋回波 $T_2$ 弛豫时间（µs） |
| `r2`             | `float`                | $R^2$ 拟合优度 |
| `success`        | `bool`                 | 该量子比特拟合是否成功 |

> 说明：`status` 为文件级字符串状态；`success` 为量子比特级布尔值，表示单个 qubit 拟合是否成功。内置 plotter 绘图时使用 `fit_envelope` 作为拟合曲线。

### 示例结果

```python
{
  "type": "spinecho",
  "results": [
    {
      "status": "success",
      "Q0": {
        "q_name": "Q0",
        "x": [0.0, 50.0, 100.0, 150.0, ...],
        "amp": [0.95, 0.82, 0.71, 0.63, ...],
        "envelope": [0.94, 0.83, 0.72, 0.64, ...],
        "fit_envelope": [0.96, 0.84, 0.73, 0.64, ...],
        "params": [0.95, 0.02, 125360.0, 0.0],
        "T2": 125.36,
        "r2": 0.9821,
        "success": True
      }
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
  save_path_prefix = f"./tmp/client/result_{TaskName.SPINECHO.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.SPINECHO.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.SPINECHO.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )
```
