# SPECTRUM2D 任务接口文档

## 概述

SPECTRUM2D 是 Scope 中的一个任务，用于对二维频谱数据进行曲线分割。该任务支持多种曲线拟合类型，包括多项式拟合和余弦拟合。

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitScopeClient
from qubitclient import TaskName


client = QubitScopeClient()
```

### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| file_list | list[np.ndarray] | 是 | 数据列表，支持.npy的numpy数组 |
| task_type | TaskName | 是 | 任务类型，固定为`TaskName.SPECTRUM2D` |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典：

   ```python
   {
       "image": {
           "Q0": (iq_avg, bias, frequency),   # tuple, length=3
           "Q1": (iq_avg, bias, frequency),
           ...
       }
   }
   
   
   ```
每个量子比特对应一个键（如 "Q0"），值为 (iq_avg, bias, frequency)，至少包含前3个元素：
| 元素 | 类型 | 描述 |
|------|------|------|
| iq_avg | np.ndarray,  shape=(B, A) | IQ平均值，dtype=complex64 |
| bias | np.ndarray, shape=(A,) | 偏置数组，dtype=float64 |
| frequency | np.ndarray,  shape=(B,) | 频率数组，dtype=float64 |


#### 调用示例

```python
# 使用文件路径

response = client.request(file_list=["data/singlepath/file1.npy", "data/singlepath/file2.npy"], task_type=TaskName.SPECTRUM2D)


dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

    # 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=TaskName.SPECTRUM2D)

```

### 获取结果

```python
# 不过滤的结果
results = client.get_result(response)

# 或过滤后的结果
threshold = 0.5
results = client.get_result(response, threshold=threshold, task_type=TaskName.SPECTRUM2D.value)
```



### 返回值格式

返回的结果是一个列表，每个字典元素对应一个输入文件的处理结果：

```json
[
  {
    "params": List[List[List[List[float]]]],          // 余弦曲线点集合
    "confs": List[List[float]],               // 余弦曲线置信度
    "coscompress_list": List[List[float]],    // 余弦曲线压缩程度
    "lines_list": List[List[List[List[float]]]],      // 直线点集合
    "lineconfs_list": List[List[float]],      // 直线置信度
    "status": str               // 处理状态
  },
  ...
]
```


### 字段说明

| 字段名 | 类型 | 描述                                                |
|--------|------|---------------------------------------------------|
| params | List[List[List[List[float]]]] | 余弦曲线点集合 |
| confs | List[List[float]] | 余弦曲线置信度  |
| coscompress_list | List[List[float]] | 余弦曲线压缩程度 |
| lines_list | List[List[List[List[float]]]] | 直线点集合  |
| lineconfs_list | List[List[float]] | 直线置信度 |
| status | str | 处理状态，'success' 表示成功   |


### 示例结果

```python
[
  {
    "params": [[[[-1,3.8e9],[-0.9,3.7e9],...]],[[[-1,3.8e9],[-0.9,3.7e9],...]]],
    "confs": [[0.7],[0.9]],
    "coscompress_list": [[0.7],[0.9]],
    "lines_list": [[[[-1,3.8e9],[-0.9,3.7e9],...]],[[[-1,3.8e9],[-0.9,3.7e9],...]]],
    "lineconfs_list": [[0.7],[0.9]],
    "status":'success'
  },  
  ...
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
  save_path_prefix = f"./tmp/client/result_{TaskName.SPECTRUM2D.value}_{savenamelist[idx]}"
  save_path_png = save_path_prefix + ".png"
  save_path_html = save_path_prefix + ".html"
  plt_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.SPECTRUM2D.value,
      save_path=save_path_png,
      result=result,
      dict_param=dict_param
  )
  ply_plot_manager.plot_quantum_data(
      data_type='npy',
      task_type=TaskName.SPECTRUM2D.value,
      save_path=save_path_html,
      result=result,
      dict_param=dict_param
  )


```