# T12DFIT 任务接口文档

## 概述

T12DFIT 是 Scope 中的一个任务，用于对量子比特的2D弛豫信号（2DT1 衰减）的每个zpa下的T1进行指数拟合，返回每个量子比特，每个zpa的拟合参数（T1）
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

| 参数名      | 类型                                      | 必需 | 描述                          |
|-------------|-------------------------------------------|------|-----------------------------|
| `file_list` | `list[str \| dict[str, np.ndarray]]`      | 是                           | 数据文件列表，支持 `.npy` 文件路径或 `numpy` 数组                     |
| `task_type` | `TaskName`                                | 是   | 任务类型，固定为 `TaskName.T12DFIT` |                             |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": [p_array,delay_array, zpa_array],   
            "Q1": [p_array,delay_array, zpa_array],
            ...
        }
    }
    ```

    p_array: 二维 np.ndarray，表示概率
    delay_array: 一维 np.ndarray，表示延时
    zpa_array: 一维 np.ndarray，表示脉冲强度

    每个量子比特对应一个键（如 "Q0"），值为 [p, delay,zpa] 的列表

#### 调用示例

```python
# 使用文件路径
response = client.request(
    file_list=["data/t12dfit/file1.npy", "data/t12dfit/file2.npy"],
    task_type=TaskName.T12DFIT
)

# 使用numpy数组
import numpy as np
data_ndarray = np.load("file1.npy", allow_pickle=True)
response = client.request(
    file_list=[data_ndarray],
    task_type=TaskName.T12DFIT
)
```

### 获取结果

```python
response_data = client.get_result(response)
threshold = 0.5
response_data_filtered = client.get_filtered_result(response, threshold, TaskName.T12DFIT.value)

results = response_data_filtered.get("results")
# 或使用未过滤的原始结果
# results = response_data.get("results")
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
{
  "type": "t12dfit",
  "results": [
    {
      "t1_list": [[float, ...], ...],
      "zpa_list": [[float, ...], ...],
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

| 字段名           | 类型                   | 描述                            |
|------------------|------------------------|-------------------------------|
| `t1_list`    | `List[List[float]]`    | 每个量子比特,每个zpa下的的拟合参数           |
| `zpa_list`        | `List[List[float]]`          | 每个量子比特,zpa列表                  |
| `status`         | `str`                  | 处理状态：`"success"` 或 `"failed"` |

### 示例结果

```python
{
  "type": "t12dfit",
  "results": [
    {
      "t1_list": [
        [0.9606002214647686, 27.10772731801952, 0.16825506437258225],
        [1.0316859089502217, 11.33354956261001, -0.00035147308286919733],
        [0.3708991911338009, 30.100798502307462, -0.019399226855197578]
      ],
      "zpa_list": [
        [0.4,0.6,0.8],
        [0.4,0.6,0.8],
        [0.4,0.6,0.8]
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
  save_path_prefix = f"./tmp/client/result_{TaskName.T12DFIT.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.T12DFIT.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.T12DFIT.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )

```