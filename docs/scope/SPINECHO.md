# SPINECHO 任务接口文档

## 概述

SPINECHO 是 Scope 中的一个任务，用于对量子比特的 **Spin Echo（自旋回波）** 衰减信号进行拟合，提取每个量子比特的 $T_2$ 弛豫时间、拟合包络曲线、$R^2$ 拟合优度及处理状态。

---

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitScopeClient, TaskName

client = QubitScopeClient()
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
# 不过滤的结果
results = client.get_result(response)

# 或过滤后的结果
threshold = 0.5
results = client.get_result(response, threshold=threshold, task_type=TaskName.SPINECHO.value)
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
[
  {
    "params_list": [[float, ...], ...],
    "fit_envelope_list": [[float, ...], ...],
    "r2_list": [float, ...],
    "x_out_list": [[float, ...], ...],
    "amp_out_list": [[float, ...], ...],
    "envelope_list": [[float, ...], ...],
    "success_list": [true | false, ...],
    "t2_list": [float, ...],
    "status": "success" | "failed"
  },
  ...
]
```

`params_list[i]`：第 i 个量子比特的拟合参数  
`fit_envelope_list[i]`：第 i 个量子比特的包络拟合曲线  
`envelope_list[i]`：第 i 个量子比特从原始信号提取的包络  
`x_out_list[i]` / `amp_out_list[i]`：第 i 个量子比特的时间轴与幅度  
`t2_list[i]`：第 i 个量子比特的自旋回波 $T_2$ 弛豫时间（µs）  
`r2_list[i]`：第 i 个量子比特的 $R^2$ 拟合优度  
`success_list[i]`：第 i 个量子比特拟合是否成功  

量子比特顺序与输入 `image` 字典的键顺序一致。

### 字段说明

| 字段名               | 类型                   | 描述 |
|----------------------|------------------------|------|
| `params_list`        | `List[List[float]]`    | 每个量子比特的包络拟合参数 |
| `fit_envelope_list`  | `List[List[float]]`    | 每个量子比特的包络拟合曲线 |
| `envelope_list`      | `List[List[float]]`    | 每个量子比特从原始信号提取的包络 |
| `x_out_list`         | `List[List[float]]`    | 每个量子比特的延迟时间序列 |
| `amp_out_list`       | `List[List[float]]`    | 每个量子比特的原始信号强度 |
| `t2_list`            | `List[float]`          | 每个量子比特的 $T_2$ 弛豫时间（µs） |
| `r2_list`            | `List[float]`          | 每个量子比特的 $R^2$ 拟合优度 |
| `success_list`       | `List[bool]`           | 每个量子比特拟合是否成功 |
| `status`             | `str`                  | 处理状态：`"success"` 或 `"failed"` |

> 说明：内置 plotter 绘图时使用 `fit_envelope_list` 作为拟合曲线，原始数据来自输入 `dict_param["image"]`。

### 示例结果

```python
{
  "type": "spinecho",
  "results": [
    {
      "params_list": [[0.95, 0.02, 125360.0, 0.0]],
      "fit_envelope_list": [[0.96, 0.84, 0.73, 0.64, ...]],
      "r2_list": [0.9821],
      "x_out_list": [[0.0, 50.0, 100.0, 150.0, ...]],
      "amp_out_list": [[0.95, 0.82, 0.71, 0.63, ...]],
      "envelope_list": [[0.94, 0.83, 0.72, 0.64, ...]],
      "success_list": [True],
      "t2_list": [125.36],
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
