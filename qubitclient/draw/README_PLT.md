

# QuantumDataPltPlotter - 量子数据可视化工具

# 概述

QuantumDataPltPlotter 是一个基于 matplotlib 的量子数据可视化工具库，提供了统一的接口来绘图。支持热力图、散点图、线图等多种图表类型，并提供了灵活的样式配置系统。


# 类说明

1. PltPlotStyleConfig:  样式配置类，管理所有可视化元素的默认样式。

2. QuantumDataPltPlotter: 主绘图类，继承自 ABC，提供所有绘图方法。
3. S21VfluxScopeDataPltPlotter: S21Vflux绘图类，继承自 QuantumDataPltPlotter，提供具体任务的绘图。

## PltPlotStyleConfig 参数详解

### create_subplots参数

| 参数名                | 类型   | 默认值 | 说明
|figure_width      | float   |  15    |图形宽度
|max_cols    | int | 2   |列数
|subplot_hspace      | float   |  0.05    |子图垂直距离
|subplot_wspace    | float | 0.05   |子图水平距离
|subplot_left      | float   |  0.05    |左侧距离
|subplot_right    | float |0.95   |右侧距离
|subplot_bottom      | float   |  0.01    |底部距离
|subplot_top    | float | 0.99   |顶部距离
|show_grid    | bool | True   |是否显示网格
|grid_alpha      | float   |  0.3    |网格透明度
|grid_linestyle    | str | '--'  |网格线条



### add_2dmap参数
| 参数名                | 类型   | 默认值     | 说明
|shading      | List   |  ['auto', 'flat', 'nearest', 'gouraud']    | 着色索引方案
|cmap          | List    | ['viridis', 'jet', 'hot', 'coolwarm', 'RdBu', 'gray'] |颜色渐变方案


### add_scatter参数
| 参数名                | 类型   | 默认值     | 说明
|marker_size      | int   |  100    | 标记点大小
|marker_styles          | list    | ['.','o', 's', '^', 'D', 'v', '*', 'p', 'h', 'x', '+'] |标记点样式
|marker_edge_width      | float   |  0.5   | 边界宽度
|marker_colors          | list    | 25种颜色 |颜色调色板



### add_line参数

| 参数名                | 类型   | 默认值     | 说明
|line_width      | int   |  2    | 线宽
|line_styles          | list    |  ['-', '--', '-.', ':','o'] |线条样式
|line_colors      | list   |  14种颜色   | 线条颜色


 # add_histogram 参数
 | 参数名                | 类型   | 默认值     | 说明
|histogram_density      | bool   |  True    | 归一化方式
|histogram_alpha          | float    | 0.5 |透明度
 

### add_annotation参数
| 参数名                | 类型   | 默认值     | 说明
|annotation_fontsize      | int   |  10    | 注释字体大小
|annotation_bbox          | dict    | {}|注释边框
|annotation_arrowprops      | dict   |  {}  | 注释箭头

annotation_bbox 详细配置：
```python
dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7)
```

annotation_arrowprops 详细配置：
```python
dict(arrowstyle='->', connectionstyle='arc3,rad=0')

```


### add_legend参数

| 参数名                | 类型   | 默认值     | 说明
|legend_fontsize      | int   |  12    | 图例字体
|legend_loc          | str    | 'upper left' |图例位置
|legend_bbox_to_anchor      | Tuple   |   (1.05, 1)   | 图例坐标
|legend_max_scatters          | int    | 5 |图例显示的最大离散点数(一般先按照conf排序,图例只显示最大的5个)
|legend_max_lines      | int   | 5| 图例显示的最大线条数(一般先按照conf排序,图例只显示最大的5个)







 # add_vline 参数

| 参数名                | 类型   | 默认值     | 说明
|vline_style      | str   |   '--'    | 类型
|vline_alpha          | float    | 0.7|透明度
|vline_width      | float   |  1.0  | 宽度
|vline_color          | str    | 'red' |颜色
  
 # configure_axis 参数
| 参数名                | 类型   | 默认值     | 说明
|title_fontsize      | int   |   14    | 标题字体大小
|title_fontweight          | str    | 'bold'|标题字体粗细
|title_color      | str   |  'black'  | 标题颜色
|title_pad          | int    | 15 |标题与图形之间的间距
|label_fontsize          | int    | 12 |坐标轴标题字体大小
|label_color          | str    | 'black' |坐标轴标题字体颜色
|tick_labelsize          | int    | 10 |坐标轴刻度尺寸
|tick_direction          | str    | 'in'|坐标轴刻度方向











## QuantumDataPltPlotter 方法详解

### 初始化方法

```python
    def __init__(self, task_type: str, style_config: Optional[PltPlotStyleConfig] = None):
        self.task_type = task_type
        self.style = style_config or PltPlotStyleConfig()
```
参数：
1. task_type: 任务类型标识

### create_subplots - 创建子图画布

```python
def create_subplots(self, n_plots: int,**kwargs) -> Tuple[plt.Figure, np.ndarray, int, int]
```

参数：
1.位置参数
· n_plots: 子图数量
2. 可变参数
· **kwargs

返回： (fig, axes, rows, cols) 元组


### add_2dmap - 添加热力图

```python
 def add_2dmap(self, ax: plt.Axes, x, y,s,
                 label: str = '', shading_index: int = 0, cmap_index: int = 0,
                  **kwargs)
```

参数：
1. 位置参数
· ax: matplotlib的Axes对象
· s: 2D数据数组
· x: X轴坐标数组
· y: Y轴坐标数组
2. 默认值参数
· shading_index: 着色索引
· label: 数据标签
· cmap_index: 颜色索引
3. 可变参数
· **kwargs


### add_hist - 添加直方图

```python
def add_histogram(self, ax: plt.Axes, x, bins,xrange,
                  **kwargs)

```

参数：
1. 位置参数
· ax: matplotlib的Axes对象
· x: 数据
· bins: 分箱数
· xrange: 数据范围

2. 可变参数
· **kwargs


###  add_scatter - 添加散点图

```python
 def add_scatter(self, ax: plt.Axes, x,y, label: str = '',
                    marker_index: int = 0, color_index: int = 0, **kwargs)
```

参数：
1. 位置参数
· ax: matplotlib的Axes对象
· x: X轴坐标数组
· y: Y轴坐标数组
2. 默认值参数
· color_index: 颜色索引（循环使用调色板）
· marker_index: 标记样式索引
· label: 数据标签
3. 可变参数
· **kwargs


### add_line - 添加线条

```python
def add_line(self, ax: plt.Axes, x, y,
                 label: str = '', line_style_index: int = 0, color_index: int = 0,
                  **kwargs)
```

参数：
1. 位置参数
· ax: matplotlib的Axes对象
· x: X轴坐标数组
· y: Y轴坐标数组
2. 默认值参数
· label: 数据标签
· line_style_index: 线条样式索引
· color_index: 线条颜色索引
3. 可变参数
· **kwargs


### add_annotation - 添加注释

```python
def add_annotation(self, ax: plt.Axes, text: str, xy: Tuple[float, float],annotation_xycoords: str="data",annotation_textcoords: str = "offset points",
    annotation_xytext = (0, 10),color_index: int = 0,showarrow=True, **kwargs)
```

参数：
1. 位置参数
· ax: matplotlib的Axes对象
· xy: 注释位置
· text: 注释文本

2. 默认值参数
. annotation_xycoords: xy参数的坐标系
· annotation_textcoords: 文本参照坐标系
· annotation_xytext: 文本偏移位置
· color_index: 颜色索引
· showarrow: 是否显示箭头

3. 可变参数
· **kwargs

### add_vline - 添加垂直线

```python
def add_vline(self, ax: plt.Axes, x: float, label=None,**kwargs)
```
参数：
1. 位置参数
· ax: matplotlib的Axes对象
· x: 垂直线位置
2. 默认值参数
· label: 数据标签

3. 可变参数
· **kwargs


### add_legend - 更新布局
　　他们在冰岛玩了两天，打卡了气势磅礴的黄金瀑布，探索了冰岛冬日限定蓝冰世界，还去参观了电影《白日梦想家》的取景地斯蒂基斯霍尔米。江望依旧表现得风度翩翩，与当地人谈笑风生，偶尔流露出的风流仿佛是他的本能，许归忆则保持着她一贯的自由随性，对新鲜事物充满好奇，神色阳光爽朗。


```python
def add_legend(self, ax: plt.Axes, handles=None, labels=None, twinx: bool = False)
```
参数：
1. 位置参数
· ax: matplotlib的Axes对象

2. 默认值参数
· handles: 是否添加图例标签
· labels: 是否添加图例标签
· twinx: 是否双坐标轴上添加图例

3. 可变参数
· **kwargs


### configure_axis - 配置坐标轴

```python
 def configure_axis(self, ax: plt.Axes, title: Optional[str] = None,
                       xlabel: Optional[str] = None, ylabel: Optional[str] = None, show_legend: bool = True,**kwargs)
```
参数：
1. 位置参数
· ax: matplotlib的Axes对象


2. 默认值参数
· xlable: 是否设置x轴坐标
· ylable: 是否设置y轴坐标
· title: 是否设置标题
· show_legend: 是否显示图例

3. 可变参数
· **kwargs
### save_plot - 保存图像

```python
def save_plot(self, fig: plt.Figure, save_path: str)
```
参数：
1. 位置参数
· ax: matplotlib的Axes对象
· save_path: 保存路径

###  抽象方法：
    plot_result_npy(): 处理.npy格式数据的抽象方法
    plot_result_npz(): 处理.npz格式数据的抽象方法



使用示例

示例1：基本使用(以s21vfluxscope 为例子)

```python
from .pltplotter import QuantumDataPltPlotter


class S21VfluxScopeDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("s21vfluxscope")
    #======1======= 初始化

    def plot_result_npy(self, **kwargs):
    #======2======= 数据预处理

        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')
        data = dict_param.item()
        image = data["image"]
        q_list = image.keys()
        volt_list = []
        freq_list = []
        s_list = []
        q_name_list=[]
        for idx, q_name in enumerate(q_list):
            image_q = image[q_name]

            volt = image_q[0]
            freq = image_q[1]
            s = image_q[2]
            volt_list.append(volt)
            freq_list.append(freq)
            s_list.append(s)
            q_name_list.append(q_name)
        coscurves_list = result['coscurves_list']
        cosconfs_list = result['cosconfs_list']
        lines_list = result['lines_list']
        lineconfs_list = result['lineconfs_list']

    #======3======= 创建子图画布

        n_plots = len(volt_list) * 2
        fig, axes, rows, cols = self.create_subplots(n_plots)
        axs = axes.flatten()

        for ii in range(n_plots):
            ax = axs[ii]
            file_name = q_name_list[ii//2]
            volt = volt_list[ii//2]
            freq = freq_list[ii//2]
            s = s_list[ii//2]
    #======4======= add_2dmap 添加map

            c = self.add_2dmap(ax,freq, volt, s.T,shading_index=0,cmap_index=0)
            #
            fig.colorbar(c, ax=ax)

            if (ii % 2 != 0):
                centcol = len(freq) // 2

                if coscurves_list[ii// 2]:
                    for j, curve in enumerate(coscurves_list[ii// 2]):
                        final_x_cos = [item[0] for item in curve]
                        final_y_cos = [item[1] for item in curve]

    #======5=======添加line,指定位置参数,其他可选参数如不指定则默认

                        self.add_line(ax,final_x_cos,final_y_cos, color_index=0, line_style_index=0)
                        if centcol < len(final_x_cos):
    #======6=======annotation,指定位置参数,其他可选参数如不指定则默认

                            self.add_annotation(ax,f"conf:{cosconfs_list[ii// 2][j]:.2f}",(final_x_cos[centcol], final_y_cos[centcol]))
            #
                if lines_list[ii// 2]:
                    for j, line in enumerate(lines_list[ii// 2]):
                        final_x_line = [item[0] for item in line]
                        final_y_line = [item[1] for item in line]
    #======7=======添加line,指定位置参数,其他可选参数如不指定则默认

                        self.add_line(ax,final_x_line,final_y_line, color_index=1, line_style_index=0)

                        if centcol < len(final_x_line):
    #======8========添加annotation,指定位置参数,其他可选参数如不指定则默认

                            self.add_annotation(ax,f"conf:{lineconfs_list[ii// 2][j]:.2f}",(final_x_line[centcol], final_y_line[centcol]))
    #======9========add_legend,指定位置参数,其他可选参数如不指定则默认

            handles, labels = ax.get_legend_handles_labels()
            self.add_legend(ax, handles, labels)
    #======10========配置标题和坐标轴,指定位置参数,其他可选参数如不指定则默认,如不设置X/Y轴,不指定即可

            self.configure_axis(ax,title=f"{file_name}",xlabel="Bias",ylabel="Frequency (GHz)")

        fig.tight_layout()
        return fig  # ✅ 返回 Figure 对象

```