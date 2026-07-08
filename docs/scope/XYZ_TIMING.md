# XYZ_TIMING 任务接口文档

## 概述

XYZ_TIMING 是 Scope 中的一个任务，用于对量子比特的 **XYZ 时序校准（Timing XYZ）** 实验数据进行分析，返回每个量子比特的拟合曲线、时序偏移量 `zd_xy`、$R^2$ 拟合优度及处理状态。

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
| `task_type` | `TaskName`                                | 是   | 任务类型，固定为 `TaskName.TIMINGXYZ`（API 值为 `"xyz_timing"`）      |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": [amp_array, delay_array],   
            "Q1": [amp_array, delay_array],
            ...
        }
    }
    ```

    amp_array: 一维 np.ndarray，表示信号强度
    delay_array: 一维 np.ndarray，表示延迟时间（单位：秒）
    每个量子比特对应一个键（如 "Q0"），值为 [amp, delay] 的列表

#### 调用示例

```python
# 使用文件路径
response = client.request(
    file_list=["data/XYZ_Timing/file1.npy", "data/XYZ_Timing/file2.npy"],
    task_type=TaskName.TIMINGXYZ
)

dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

# 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=TaskName.TIMINGXYZ)
```

### 获取结果

```python
# 不过滤的结果
results = client.get_result(response)

# 或过滤后的结果
threshold = 0.5
results = client.get_result(response, threshold=threshold, task_type=TaskName.TIMINGXYZ.value)
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
[
  {
    "params_list": [[float, ...], ...],
    "fit_data_list": [[float, ...], ...],
    "r2_list": [float, ...],
    "x_out_list": [[float, ...], ...],
    "amp_out_list": [[float, ...], ...],
    "success_list": [true | false, ...],
    "zd_xy_list": [float, ...],
    "status": "success" | "failed"
  },
  ...
]
```

`params_list[i]`：第 i 个量子比特的 Erf 拟合参数  
`fit_data_list[i]`：第 i 个量子比特的拟合曲线值  
`x_out_list[i]` / `amp_out_list[i]`：第 i 个量子比特的延迟时间与幅度  
`zd_xy_list[i]`：第 i 个量子比特的 XYZ 时序偏移量（ns）  
`r2_list[i]`：第 i 个量子比特的 $R^2$ 拟合优度  
`success_list[i]`：第 i 个量子比特拟合是否成功  

量子比特顺序与输入 `image` 字典的键顺序一致。

### 字段说明

| 字段名           | 类型                   | 描述 |
|------------------|------------------------|------|
| `params_list`    | `List[List[float]]`    | 每个量子比特的 Erf 拟合参数 |
| `fit_data_list`  | `List[List[float]]`    | 每个量子比特的拟合曲线值 |
| `x_out_list`     | `List[List[float]]`    | 每个量子比特的延迟时间序列（秒） |
| `amp_out_list`   | `List[List[float]]`    | 每个量子比特的原始信号强度 |
| `zd_xy_list`     | `List[float]`          | 每个量子比特的 XYZ 时序偏移量（ns） |
| `r2_list`        | `List[float]`          | 每个量子比特的 $R^2$ 拟合优度 |
| `success_list`   | `List[bool]`           | 每个量子比特拟合是否成功 |
| `status`         | `str`                  | 处理状态：`"success"` 或 `"failed"` |

> 说明：内置 plotter 绘图时使用 `fit_data_list` 作为拟合曲线，原始数据来自输入 `dict_param["image"]`。

### 示例结果

```python
{
  "type": "xyz_timing",
  "results": [
    {
      "params_list": [[0.95, 0.05, -2.0, 8.0]],
      "fit_data_list": [[0.40, 0.53, 0.76, 0.94, 0.83, ...]],
      "r2_list": [0.9654],
      "x_out_list": [[-6e-8, -4e-8, -2e-8, 0.0, 2e-8, ...]],
      "amp_out_list": [[0.42, 0.55, 0.78, 0.95, 0.81, ...]],
      "success_list": [True],
      "zd_xy_list": [3.193],
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
  save_path_prefix = f"./tmp/client/result_{TaskName.TIMINGXYZ.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.TIMINGXYZ.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.TIMINGXYZ.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )
```
