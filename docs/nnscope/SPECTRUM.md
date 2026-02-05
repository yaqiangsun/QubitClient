# SPECTRUM 任务接口文档

## 概述

SPECTRUM 是 NNScope 中的一个任务,用于寻找峰值区域的起点、终点、peak所在x值、峰宽度、置信度。

## 接口使用方式

### 客户端初始化

```python
from qubitclient import QubitNNScopeClient
from qubitclient import NNTaskName

client = QubitNNScopeClient(url=url,api_key=api_key)
```

### 请求参数

| 参数名     | 类型                                         | 必需 | 描述                                                          |
| ---------- | -------------------------------------------- | ---- | ------------------------------------------------------------- |
| file_list  | list[str\|dict[str,np.ndarray]\| np.ndarray] | 是   | 数据文件列表，支持.npy或numpy数组                             |
| task_type  | NNTaskName                                   | 是   | 任务类型，固定为 `NNTaskName.POWERSHIFT`                    |
| curve_type | CurveType                                    | 是   | 任务类型，固定为 `CurveType.AUTO(返回poly和cosine的最优解)` |

### 数据格式

#### 输入格式

1. **NPY 文件格式**：
   NPY文件需要包含一个字典

   ```python
    {
        "image": {
            "Q0": [x, y,...],
            "Q1": [x, y,...],
            ...
        }
    }
   ```

x: 一维 np.ndarray,shape(A,),表示频率数据
y: 一维 np.ndarray,shape(B,),表示读取强度amp

每个量子比特对应一个键（如 "Q0"），值为 [x, y,...] 的列表

#### 调用示例

```python
dict_list = []
for file_path in file_path_list:
    content = load_npy_file(file_path)
    dict_list.append(content)

client = QubitNNScopeClient(url=url, api_key=api_key)
# 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
response = client.request(file_list=dict_list, task_type=NNTaskName.SPECTRUM,curve_type=CurveType.AUTO)
results = client.get_result(response=response)

```

### 获取结果

```python

results = client.get_result(response=response)

threshold = 0.3
print("before filter results: ", results)
results_filtered = client.get_filtered_result(response, threshold, NNTaskName.SPECTRUM.value) 

# response_data 和 response_data_filtered 分别是阈值筛选前和筛选后的结果
```

## 返回值格式

返回的结果是一个字典：

```json
[
	{
		"peaks_list":[[float,float,...], ...],\
		"peak_start":[[float,float,...], ...],\
		"peak_end":[[float,float,...], ...],\
		"confidences_list":[[float,float,...], ...],\
		"mean_cut_widths_list":[[float,float,...], ...],\
		"status":"success" | "failed"
	}
]

```

### 字段说明

| 字段名               | 类型        | 描述                               |
| -------------------- | ----------- | ---------------------------------- |
| peaks_list           | List[float] | 每个npy文件所有波的所有峰的x值     |
| peak_start           | List[float] | 每个npy文件所有波的所有峰的起点x值 |
| peak_end             | List[float] | 每个npy文件所有波的所有峰的终点x值 |
| confidences_list     | List[float] | 每个npy文件所有波的所有峰的置信度  |
| mean_cut_widths_list | List[float] | 每个npy文件所有波的所有峰的宽度    |

### 示例结果

```python
[ 
	{
		'peaks_list': [[4431999999.99993, 4431999999.99993], [4293999999.9999456]],  //一个波有多个峰
		'confidences_list': [[0.44802555441856384, 0.15026916563510895], [0.685797929763794]], 
		'mean_cut_widths_list': [[34666666.67, 28000000.0], [54666666.67]], 
		'peak_start': [[4402666666.67, 4410666666.67], [4262666666.67]], 
		'peak_end': [[4437333333.33, 4438666666.67], [4317333333.33]], 
		'status': 'success'
	}，
	//一个npy文件中其他波
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
        data_type='npy',
        task_type=NNTaskName.SPECTRUM.value,
        save_path=save_path_png,
        result=result,
        dict_param=item
    )
    ply_plot_manager.plot_quantum_data(
        data_type='npy',
        task_type=NNTaskName.SPECTRUM.value,
        save_path=save_path_html,
        result=result,
        dict_param=item
    )

```
