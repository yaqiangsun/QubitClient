# RAMSEY 任务接口文档

## 概述

RAMSEY 是 Scope 中的一个任务，用于对量子比特的进行 **指数衰减 + 余弦振荡** 拟合，返回每个量子比特的拟合参数、拟合曲线、R² 拟合优度及处理状态

$$
y = A \cdot e^{-x / T1} \cdot \cos(2\pi w x + \phi) + B
$$

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
| `task_type` | `TaskName`                                | 是   | 任务类型，固定为 `TaskName.RAMSEY`                                    |                             |

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
response = client.request(file_list=["data/ramsey/file1.npy", "data/ramsey/file2.npy"], task_type=TaskName.RAMSEY)

dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

# 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=TaskName.RAMSEY)
```

### 获取结果

```python
response_data = client.get_result(response)
threshold = 0.8
response_data_filtered = client.get_filtered_result(response, threshold, TaskName.RAMSEY.value)

results = response_data_filtered.get("results")
# 或使用未过滤的原始结果
# results = response_data.get("results")
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
{
  "type": "t2fit",
  "results": [
    {
      "params_list": [[A, B, T1, T2, w, phi], ...],
      "r2_list": [float, ...],
      "fit_data_list": [[float, ...], ...],
      "status": "success" | "failed"
    },
    ...
  ]
}
```

params_list[i]: 第 i 个量子比特的拟合参数 [A, B, T1, T2, w, phi]
fit_data_list[i]: 第 i 个量子比特在 密集时间点 上的拟合值（用于绘制平滑曲线）
r2_list[i]: 第 i 个量子比特的 R² 拟合优度

### 字段说明

| 字段名           | 类型                   | 描述 |
|------------------|------------------------|------|
| `params_list`    | `List[List[float]]`    | 每个量子比特的拟合参数 `[A, B, T1, w, phi]`：<br>• `A`: 初始振幅<br>• `B`: 基线偏移<br>• `T1`: 指数衰减时间（µs）<br>• `w`: 振荡角频率（rad/s）<br>• `phi`: 初始相位（rad） |
| `r2_list`        | `List[float]`          | 每个量子比特的 R² 拟合优度，范围 `[0, 1]`，越接近 1 拟合越好 |
| `fit_data_list`  | `List[List[float]]`    | 每个量子比特的拟合曲线值 |
| `status`         | `str`                  | 处理状态：`"success"` 或 `"failed"` |

### 示例结果

```python
{
  "type": "ramsey",
  "results": [
    {
      "params_list": [
        [0.4220602571148976, 0.6782053429458166, 1021.6257020164796,
         46142276.9097151, 1.075826496551695]
      ],
      "r2_list": [0.9279673627766446],
      "fit_data_list": [
        [0.8786861186854626, 0.7349471964772133, 0.5839287562931449, ...]
      ],
      "status": "success"
    }
  ]
}
```

注意：fit_data_list 中的拟合点对应更密集的时间序列（非原始 x），绘图时需使用 np.linspace(x_min, x_max, len(fit_data)) 生成对应 x_fit。

## 可视化

处理结果可以通过内置的绘图工具进行可视化：

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

ply_plot_manager = QuantumPlotPlyManager()
plt_plot_manager = QuantumPlotPltManager()

for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
  save_path_prefix = f"./tmp/client/result_{TaskName.RAMSEY.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.RAMSEY.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.RAMSEY.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )
```