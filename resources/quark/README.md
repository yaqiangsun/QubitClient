# 在quark中使用


## 配置
1. 将analysis目录复制到QuLab根目录下；
2. 将`config.py.example`拷贝为`config.py`,并配置相关参数

## 使用
1. 对于测量后的结果，使用quark接口获取测量后的数据：
- 在线获取数据：
```python
data = t.result()
```
- 离线获取数据：
```python
data = get_data_by_tid(tid)
```
获取得到的数据即为后续功能的输入.

2. 使用接口分析
```
from anaylsis.inception import optpipulse
results = optpipulse(data)
```

3. 绘图
```python
from analysis.visualization import plot_optpipulse
plot_optpipulse(data,analysis_result,save_path='./tmp/vis/opt_pipulse.png')
```
