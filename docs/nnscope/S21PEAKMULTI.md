# S21PEAKMULTI 任务接口文档

## 概述

S21PEAKMULTI 是 NNScope 中的一个任务，用于检测多个峰值并给出峰值置信度。与 S21PEAK 不同的是，该任务支持多组数据的并行处理。

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitNNScopeClient
from qubitclient import NNTaskName


client = QubitNNScopeClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| file_list | list[np.ndarray] | 是 | 数据列表，支持.npy的numpy数组 |
| task_type | NNTaskName | 是 | 任务类型，固定为`NNTaskName.S21PEAKMULTI` |

### 数据格式

#### 输入格式

NPY文件需要包含一个字典：

```python
{
    "image": {
        "Q0101": (x, amp, phi),   # tuple, length=3
        "Q0202": (x, amp, phi),
        ...
    }
}
```

**注意**：此任务的数据格式**不包含** `id` 字段，与其他任务不同。

每个量子比特对应一个键（如 "Q0101"），值为 tuple，长度为3：

| 元素 | 类型 | 描述 |
|------|------|------|
| x | np.ndarray, shape=(N,) | 频率信息，dtype=float64 |
| amp | np.ndarray, shape=(N,) | 幅度信息，dtype=float32 |
| phi | np.ndarray, shape=(N,) | 相位信息，dtype=float32 |

#### 调用示例

```python
# 使用文件路径
response = client.request(file_list=["data/singlepath/file1.npy", "data/singlepath/file2.npy"], task_type=NNTaskName.S21PEAKMULTI)
```

或使用加载后的数据：

```python
import os
from qubitclient import QubitNNScopeClient
from qubitclient import NNTaskName
from qubitclient.scope.utils.data_parser import load_npy_file
from qubitclient.draw.pltmanager import QuantumPlotPltManager
from qubitclient.draw.plymanager import QuantumPlotPlyManager


def send_s21multi_npy_to_server(dir_path):
    # get all file in dir
    savenamelist = []
    file_names = os.listdir(dir_path)

    file_path_list = []
    for file_name in file_names:
        if file_name.endswith('.npy'):
            savenamelist.append(os.path.splitext(file_name)[0])
            file_path = os.path.join(dir_path, file_name)
            file_path_list.append(file_path)
    if len(file_path_list) == 0:
        return

    client = QubitNNScopeClient()

    dict_list = []
    for file_path in file_path_list:
        content = load_npy_file(file_path)
        dict_list.append(content)

    # 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
    response = client.request(file_list=dict_list, task_type=NNTaskName.S21PEAKMULTI)
    response_data = client.get_result(response)

    threshold = 0.5
    response_data_filtered = client.get_filtered_result(response, threshold, NNTaskName.S21PEAKMULTI.value)

    results = response_data_filtered.get("result")

    ply_plot_manager = QuantumPlotPlyManager()
    plt_plot_manager = QuantumPlotPltManager()

    for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
        save_path_prefix = f"./tmp/client/result_{NNTaskName.S21PEAKMULTI.value}_{savenamelist[idx]}"
        save_path_png = save_path_prefix + ".png"
        save_path_html = save_path_prefix + ".html"
        fig_plt = plt_plot_manager.plot_quantum_data(
            data_type='npy',
            task_type=NNTaskName.S21PEAKMULTI.value,
            save_path=save_path_png,
            result=result,
            dict_param=dict_param
        )
        fig_ply = ply_plot_manager.plot_quantum_data(
            data_type='npy',
            task_type=NNTaskName.S21PEAKMULTI.value,
            save_path=save_path_html,
            result=result,
            dict_param=dict_param
        )


base_dir = "tmp/yaqiangsun/qubit_examples/s21multi"
send_s21multi_npy_to_server(base_dir)
```

### 获取结果

```python

response_data = client.get_result(response)

threshold = 0.5
response_data_filtered = client.get_filtered_result(response, threshold, NNTaskName.S21PEAKMULTI.value)

results = response_data_filtered.get("result")

```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
[
  {
    "peaks": [[int]],       // 表示峰值索引
    "confs": [[float]]      // 表示峰值置信度
    "freqs_list": [[float]] // 表示峰值横坐标
    "status": "success" | "failed"
  },
  ...
]
```



### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| peaks | [[int]] | 表示峰值索引 |
| confs | [[float]] | 表示峰值置信度 |
| freqs_list | [[float]] | 表示峰值横坐标 |
| status | str | 表示处理状态 |

### 示例结果

```python
[
  {
    "peaks": [[10, 41, 20], [22, 34]],
    "confs": [[0.3, 0.4, 0.1], [0.6, 0.5]],
    "freqs_list": [[0.3e9, 0.4e9, 0.1e9], [0.6e9, 0.5e9]],
    "status": "success"
  }
]
```

## 可视化

处理结果可以通过内置的绘图工具进行可视化：

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

ply_plot_manager = QuantumPlotPlyManager()
plt_plot_manager = QuantumPlotPltManager()

for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
    save_path_prefix = f"./tmp/client/result_{NNTaskName.S21PEAKMULTI.value}_{savenamelist[idx]}"
    save_path_png = save_path_prefix + ".png"
    save_path_html = save_path_prefix + ".html"
    fig_plt = plt_plot_manager.plot_quantum_data(
        data_type='npy',
        task_type=NNTaskName.S21PEAKMULTI.value,
        save_path=save_path_png,
        result=result,
        dict_param=dict_param
    )
    fig_ply = ply_plot_manager.plot_quantum_data(
        data_type='npy',
        task_type=NNTaskName.S21PEAKMULTI.value,
        save_path=save_path_html,
        result=result,
        dict_param=dict_param
    )
```