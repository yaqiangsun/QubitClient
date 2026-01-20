# S21PEAK 任务接口文档

## 概述

S21PEAK 是 Scope 中的一个任务，用于检测峰值并给出峰值置信度。

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitScopeClient
from qubitclient import TaskName


client = QubitScopeClient(url=url, api_key=api_key)
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| file_list | list[np.ndarray] | 是 | 数据列表，支持.npy的numpy数组 |
| task_type | TaskName | 是 | 任务类型，固定为`TaskName.S21PEAK` |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

    ```python
    {
        "image": {
            "Q0": [x, amp,phi],   
            "Q1": [x, amp,phi],
            ...
        }
    }
    ```

x: 一维 np.ndarray,表示频率信息
amp: 一维 np.ndarray,表示幅度信息
phi: 一维 np.ndarray,表示相位信息

每个量子比特对应一个键（如 "Q0"），值为 [x, amp，phi] 的列表

#### 调用示例

```python
# 使用文件路径

response = client.request(file_list=["data/singlepath/file1.npy", "data/singlepath/file2.npy"], task_type=TaskName.S21PEAK)


dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

    # 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=TaskName.S21PEAK)

```

### 获取结果

```python

response_data = client.get_result(response)
threshold = 0.5
response_data_filtered = client.get_filtered_result(response,threshold,TaskName.S21PEAK.value)

results = client.get_result(response=response_data)  
#results = client.get_result(response=response_data_filtered)
# response_data 和 response_data_filtered 分别是阈值筛选前和筛选后的结果
```

## 返回值格式

返回的结果是一个列表，每个元素对应一个输入文件的处理结果：

```json
[
  {
    "peaks": [[int]],     // 表示峰值位置
    "confs": [[int]] // 表示峰值置信度
  },
  ...
]
```




### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| peaks | [[int]] | 表示峰值位置 |
| confs | [[int]] | 表示峰值置信度 |

### 示例结果

```python
[
  {
    "peaks": [[10,41,20],[22,34]],
    "confs": [[0.3,0.4,0.1],[0.6,0.5]]
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
  save_path_prefix = f"./tmp/client/result_{TaskName.S21PEAK.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.S21PEAK.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.S21PEAK.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )
```