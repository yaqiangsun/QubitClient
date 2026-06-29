# SPECTRUM 任务接口文档

## 概述

SPECTRUM 是 NNScope 中的一个任务,用于寻找峰值区域的起点、终点、peak所在x值、峰宽度、置信度。
选取服务端接口返回值“confidences_list”第idx个量子的[float]中数值最大的索引，
找到“peaks_list”中对应索引的peak，所为寻找到的f10参数。
如果是双峰，左侧峰对应的peak数值为f21参数，
non参数的计算方式是：（左峰freq-右峰freq）* 2


## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitNNScopeClient
from qubitclient import NNTaskName

client = QubitNNScopeClient()
```

### 请求参数

| 参数名     | 类型                                         | 必需 | 描述                           |
| ---------- | -------------------------------------------- | ---- | ------------------------------ |
| file_list  | list[str\|dict[str,np.ndarray]\| np.ndarray] | 是   | 数据文件列表，支持.npy或numpy数组 |
| task_type  | NNTaskName                                   | 是   | 任务类型，固定为 `NNTaskName.SPECTRUM` |

### 数据格式

#### 输入格式

NPY文件需要包含一个字典：

```python
{
    "image": {
        "Q0": (freq, amp),   # tuple, length=2
        "Q1": (freq, amp),
        ...
    }
}
```

每个量子比特对应一个键（如 "Q0"），值为 tuple，长度为7：

| 元素 | 类型 | 描述 |
|------|------|------|
| x | np.ndarray, shape=(N,) | 频率数据，dtype=float64 |
| y | np.ndarray, shape=(N,) | 读取强度amp，dtype=float32 |
| freq | float | 频率值 |
| flag | bool | 标志位 |
| width | float | 宽度值 |
| list1 | list | 附加列表数据 |
| list2 | list | 附加列表数据 |

#### 调用示例

```python
# 使用文件路径
response = client.request(file_list=["data/singlepath/file1.npy", "data/singlepath/file2.npy"], task_type=NNTaskName.SPECTRUM)
```

或使用加载后的数据：

```python
from qubitclient.scope.utils.data_parser import load_npy_file

dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

client = QubitNNScopeClient()
# 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=NNTaskName.SPECTRUM)
results = client.get_result(response=response)
```

### 获取结果

```python
# 不过滤的结果
results = client.get_result(response)

# 或过滤后的结果
threshold = 0.5
results = client.get_result(response, threshold=threshold, task_type=NNTaskName.SPECTRUM.value)
```

## 返回值格式

返回的结果是一个列表：

```json
[
	{
		"peaks_list": [[float, float, ...], ...],   // 每个npy文件所有波的所有峰的x值
		"peak_start": [[float, float, ...], ...],   // 每个npy文件所有波的所有峰的起点x值
		"peak_end": [[float, float, ...], ...],     // 每个npy文件所有波的所有峰的终点x值
		"confidences_list": [[float, float, ...], ...],  // 每个npy文件所有波的所有峰的置信度
		"status": "success" | "failed"
	},
	...
]
```

### 字段说明

| 字段名           | 类型          | 描述                               |
| ---------------- | ------------- | ---------------------------------- |
| peaks_list       | List[List[float]] | 每个npy文件所有波的所有峰的x值     |
| peak_start       | List[List[float]] | 每个npy文件所有波的所有峰的起点x值 |
| peak_end         | List[List[float]] | 每个npy文件所有波的所有峰的终点x值 |
| confidences_list | List[List[float]] | 每个npy文件所有波的所有峰的置信度  |
| status           | str           | 处理状态，"success" 或 "failed"    |

### 示例结果

```python
[
	{
		'peaks_list': [[4431999999.99993, 4431999999.99993], [4293999999.9999456]],  // 一个波有多个峰
		'confidences_list': [[0.44802555441856384, 0.15026916563510895], [0.685797929763794]],
		'peak_start': [[4402666666.67, 4410666666.67], [4262666666.67]],
		'peak_end': [[4437333333.33, 4438666666.67], [4317333333.33]],
		'status': 'success'
	},
	// 一个npy文件中其他波
]
```

## 可视化

处理结果可以通过内置的绘图工具进行可视化：

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

ply_plot_manager = QuantumPlotPlyManager()
plt_plot_manager = QuantumPlotPltManager()

for idx, (result, item) in enumerate(zip(results, dict_list)):
    save_path_prefix = f"./tmp/client/result_{NNTaskName.SPECTRUM.value}_{savenamelist[idx]}"
    save_path_png = save_path_prefix + ".png"
    save_path_html = save_path_prefix + ".html"

    # 绘图
    plt_plot_manager.plot_quantum_data(
        task_type=NNTaskName.SPECTRUM.value,
        save_path=save_path_png,
        data_type='npy',
        result=result,
        dict_param=item
    )
    ply_plot_manager.plot_quantum_data(
        task_type=NNTaskName.SPECTRUM.value,
        save_path=save_path_html,
        data_type='npy',
        result=result,
        dict_param=item
    )

```