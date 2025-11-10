# Quantum Data Visualization Tool

# 项目概述‌ 
这是一个基于Plotly和matplotlib的量子数据可视化工具包，用于处理和分析量子计算相关的结果，提供二维图，以及一维数据的可视化功能。以下以Plotly工具为例说明代码架构，使用方法‌，新任务的扩展开发，注意事项‌。Plotly同理。

# 代码架构‌

1. 抽象基类 QuantumDataPlyPlotter‌

    文件位置：plyplotter.py
    核心功能：定义绘图器的抽象接口和基础功能

    类构造方法：
    ```python
    def __init__(self, task_type: str):
        self.task_type = task_type
    ```
    抽象方法：
        plot_result_npy(): 处理.npy格式数据的抽象方法
        plot_result_npz(): 处理.npz格式数据的抽象方法
        save_plot(fig, save_name: str = "result_", save_format: str = "html"): 统一保存绘图结果到HTML文件

2. 具体实现类 Spectrum2DDataPlyPlotter‌

    文件位置：spectrum2dplyplotter.py
    继承关系：继承自QuantumDataPlyPlotter
    类构造方法：
    ```python
    def __init__(self):
        super().__init__("spectrum2d")
    ```
    核心方法：
        plot_result_npy(**kwargs): 处理.npy格式的二维频谱数据
        plot_result_npz(**kwargs): 处理.npz格式的二维频谱数据

3. 管理器类 QuantumPlotPlyManager‌

    文件位置：plymanager.py
    类构造方法：
    ```python
    def __init__(self):
        self.plotters: Dict[str, QuantumDataPlyPlotter] = {}
        self.register_plotters()
    ```
    核心方法：
        register_plotters(): 注册可用绘图器
        get_plotter(task_type: str): 根据任务类型获取对应绘图器
        list_available_tasks(): 获取可用任务类型列表
        plot_quantum_data(data_type: str, task_type: str, save_format: str = "html", save_name: str = "tmp0bf97fdf.py_1536", **kwargs): 统一的数据绘图入口

# 使用方法‌

示例代码基本使用流程‌（基于任务spectrum2d）

## 初始化管理器
```python
 plot_manager = QuantumPlotPlyManager()
```
## 绘制量子数据
```python
    plot_manager.plot_quantum_data(
        data_type='npy',           # 数据格式：npy或npz
        task_type='spectrum2d',    # 任务类型
        save_format="html",        # 输出格式
        save_name="my_plot",       # 保存文件名
        results=results_data,      # 绘图数据
        data_ndarray=quantum_data  # 绘图数据
    )
```


## 新任务的扩展开发‌

添加新任务的绘图器‌
对于新的任务如task:t1fit（所有task命名参考如下，对于nnscope的任务通过task_type=NNTaskName.SPECTRUM2D.value指定,对于scope的任务通过task_type=TaskName.SPECTRUM2D.value指定）
```python
    class NNTaskName(Enum):
    # S21PEAK = "s21peak"
    # OPTPIPULSE = "optpipulse"
    # RABI = "rabi"
    # RABICOS = "rabicos"
    # S21VFLUX = "s21vflux"
    # SINGLESHOT = "singleshot"
    # SPECTRUM = "spectrum"
    # T1FIT = "t1fit"
    # T2FIT = "t2fit"
    SPECTRUM2D = "spectrum2d"
```
步骤如下： 
1. 在t1fitplyplotter.py,创建新的绘图器类，继承QuantumDataPlyPlotter，
2. 实现plot_result_npy和plot_result_npz方法
3. 在QuantumPlotPlyManager的register_plotters方法中注册


## 注意事项‌
```python
    def plot_quantum_data(self, data_type: str, task_type: str, save_format: str = "png", save_name: str = "tmp0bf97fdf.py_1536", **kwargs) -> str:

    plot_manager = QuantumPlotPlyManager()
    plot_manager.plot_quantum_data(
        data_type='npy',
        task_type=NNTaskName.SPECTRUM2D.value,
        save_format="html",
        save_name=savename,
        results=results,
        data_ndarray=data_ndarray
    )

    plot_manager = QuantumPlotPltManager()
    plot_manager.plot_quantum_data(
        data_type='npy',
        task_type=NNTaskName.SPECTRUM2D.value,
        save_format="png",
        save_name = savename,
        results=results,
        data_ndarray=data_ndarray
    )
```
1. 对于plt 和 ply画图，参数只有save_format，分别是png，html，其余无需更改。
2. results=results,data_ndarray=data_ndarray，是通过**kwargs 接收的具体关键字参数，需要适配不同的任务
3. save_name为测试npy/npz的文件名，如tmp6d08e0e9.py_7157.npy，则save_name = "tmp6d08e0e9.py_7157"
