

# QuantumDataPlyPlotter - 量子数据可视化工具

# 概述

QuantumDataPlyPlotter 是一个基于 Plotly 的量子数据可视化工具库，提供了统一的接口来绘图。支持热力图、散点图、线图等多种图表类型，并提供了灵活的样式配置系统。


# 类说明

1. PlyPlotStyleConfig:  样式配置类，管理所有可视化元素的默认样式。

2. QuantumDataPlyPlotter: 主绘图类，继承自 ABC，提供所有绘图方法。
3. S21VfluxScopeDataPlyPlotter: S21Vflux绘图类，继承自 QuantumDataPlyPlotter，提供具体任务的绘图。

## PlyPlotStyleConfig 参数详解

### create_subplots 参数

| 参数名                | 类型   | 默认值 | 说明
|subplots_per_row      | int   |  2    |每行子图数量
|horizontal_spacing    | float | 0.1   |子图之间的水平间距

### add_2dmap 参数
| 参数名                | 类型   | 默认值     | 说明
|colorbar_config      | dict   |  {...}    | 颜色条配置
|color_scale          | str    | 'Viridis' |颜色渐变方案

colorbar_config 详细配置：

```python
{
    'thickness': 15,      # 颜色条厚度
    'len': 0.7,            # 颜色条长度
    'yanchor': 'middle',   # Y轴锚点
    'y': 0.5               # Y轴位置
}
```

### add_scatter 参数
| 参数名                | 类型   | 默认值     | 说明
|marker_size      | int   |  10    | 标记点大小
|marker_styles          | list    | ["circle","square","diamond"] |标记点样式
|marker_opacity      | float   |  0.7   | 标记点透明度
|marker_color_palette          | list    | 25种颜色 |颜色调色板



###  add_line 参数

| 参数名                | 类型   | 默认值     | 说明
|line_width      | int   |  2    | 线宽
|line_styles          | list    | ["solid","dash","dot","dashdot","longdash"] |线条样式
|line_colors      | list   |  14种颜色   | 线条颜色


### add_annotation 参数
| 参数名                | 类型   | 默认值     | 说明
|annotation_font_size      | int   |  12    | 注释字体大小
|annotation_font_color          | str    | 'red' |注释字体颜色
|annotation_bordercolor      | str   |  'black'   | 注释边框颜色
|annotation_bgcolor          | str    | 'yellow' |注释背景颜色
|annotation_borderwidth      | int   |  1   | 注释边框宽度


### update_layout 参数


| 参数名                | 类型   | 默认值     | 说明
|figure_height_per_row      | int   |  400    | 每行图像高度
|figure_width_per_col          | int    | 800 |每列图像宽度
|font_family      | str   |  'Arial'   | 字体族
|font_size          | int    | 12 |字体大小
|legend      | dict   |  {...}| 图例配置


legend 详细配置：

```python
{
    'x': 1.05,              # 图例X位置
    'y': 0.5,               # 图例Y位置
    'xanchor': 'left',      # X轴锚点
    'yanchor': 'middle',    # Y轴锚点
    'groupclick': "toggleitem"  # 点击行为
}
```

### add_histogram 参数
| 参数名                | 类型   | 默认值     | 说明
|opacity      | float   |   0.5    | 透明度
|histnorm      | str   |  "probability density"    | 数据归一化参数




## QuantumDataPlyPlotter 方法详解

### 初始化方法

```python
    def __init__(self, task_type: str, style_config: Optional[PlyPlotStyleConfig] = None):
        self.task_type = task_type
        self.style = style_config or PlyPlotStyleConfig()```
参数：
1. task_type: 任务类型标识

### create_subplots - 创建子图画布

```python
def create_subplots(self, n_plots, titles: List[str], **kwargs)
```

参数：
1.位置参数
· n_plots: 子图数量
· titles: 子图标题列表
2.可变参数
· **kwargs:
  · second_y: 是否启用双Y轴

返回： (fig, rows, cols) 元组


### add_2dmap - 添加热力图

```python
def add_2dmap(self, fig: go.Figure, z: np.ndarray, x: np.ndarray, y: np.ndarray,
                    row: int, col: int,showscale=False,colorscale_index=0,**kwargs)
```

参数：
1. 位置参数
· fig: Plotly图形对象
· z: 2D数据数组
· x: X轴坐标数组
· y: Y轴坐标数组
· row: 子图行号
· col: 子图列号
2. 默认值参数
· showscale: 是否显示颜色条,在第一个map设置显示.其余不显示
· colorscale_index : 颜色渐变索引
3. 可变参数
· **kwargs

###  add_scatter - 添加散点图

```python
def add_scatter(self, fig: go.Figure, x, y, row: int, col: int, 
                color_index=0, marker_index=0, name="None",
                showlegend: bool = False, **kwargs)
```

参数：
1. 位置参数
· fig: Plotly图形对象
· x: X轴坐标数组
· y: Y轴坐标数组
· row: 子图行号
· col: 子图列号
2. 默认值参数
· color_index: 颜色索引（循环使用调色板）
· marker_index: 标记样式索引
· name: 数据系列名称
· showlegend: 是否显示图例
3. 可变参数
· **kwargs

### add_scatter_points_with_anno - 添加带注释的散点图

```python
def add_scatter_points_with_anno(self, fig: go.Figure, x, y,
                                  row: int, col: int, color_index=0, 
                                  name="None", text="None",
                                  showlegend: bool = False, **kwargs)
```

参数：
1. 位置参数
· fig: Plotly图形对象
· x: X轴坐标数组
· y: Y轴坐标数组
· row: 子图行号
· col: 子图列号
2. 默认值参数
· color_index: 颜色索引（循环使用调色板）
· name: 数据系列名称
· showlegend: 是否显示图例
· text: 注释
3. 可变参数
· **kwargs

### add_line - 添加线条

```python
def add_line(self, fig: go.Figure, x, y, row: int, col: int, 
             color_index: int=0, line_style_index: int=0, 
             name: str="None", showlegend: bool = False, **kwargs)
```

参数：
1. 位置参数
· fig: Plotly图形对象
· x: X轴坐标数组
· y: Y轴坐标数组
· row: 子图行号
· col: 子图列号
2. 默认值参数
· color_index: 颜色索引（循环使用调色板）
· line_style_index: 线条样式索引
· name: 数据系列名称
· showlegend: 是否显示图例
3. 可变参数
· **kwargs


### add_annotation - 添加注释

```python
def add_annotation(self, fig: go.Figure, text: str, row: int, col: int,
                   x: float = 0.95, y: float = 0.95, 
                   xref="x", yref="y", showarrow=True, **kwargs)
```

参数：
1. 位置参数
· fig: Plotly图形对象
· x: X轴坐标注释位置
· y: Y轴坐标注释位置
· row: 子图行号
· col: 子图列号
· text: 注释文本

2. 默认值参数
· xref: 参照坐标系
· yref: 参照坐标系
· showarrow: 是否显示箭头
3. 可变参数
· **kwargs

### add_vline - 添加垂直线

```python
def add_vline(self, fig: go.Figure, x: float, row: int, col: int,
              color_index: int = 0, line_style_index: int = 0, **kwargs)
```
参数：
1. 位置参数
· fig: Plotly图形对象
· x: 垂直线位置
· row: 子图行号
· col: 子图列号

2. 默认值参数
· color_index: 颜色索引（循环使用调色板）
· line_style_index: 线条索引（循环使用调色板）
3. 可变参数
· **kwargs


### update_layout - 更新布局

```python
def update_layout(self, fig: go.Figure, rows: int, cols: int,
                  showlegend: Optional[bool] = False, **kwargs)
```
参数：
1. 位置参数
· fig: Plotly图形对象
· row: 子图行号
· col: 子图列号

2. 默认值参数
· showlegend: 是否显示图例
3. 可变参数
· **kwargs


### add_histogram - 添加直方图
```python

def add_histogram(self, fig: go.Figure, x, xbins,nbinsx,
                           row: int, col: int, name="",marker_color_index=0,**kwargs)
```
参数：
1. 位置参数
· fig: Plotly图形对象
· xbins: 边界位置
· nbinsx: 分箱数
· row: 子图行号
· col: 子图列号

2. 默认值参数
· name: 数据标签
· marker_color_index: 只方图颜色
3. 可变参数
· **kwargs




### configure_axis - 配置坐标轴

```python
def configure_axis(self, fig: go.Figure, rows: int, cols: int, 
                   xlable=None, ylable=None, **kwargs)
```
参数：
1. 位置参数
· fig: Plotly图形对象
· row: 子图行号
· col: 子图列号

2. 默认值参数
· xlable: 是否设置x轴坐标
· ylable: 是否设置y轴坐标

3. 可变参数
· **kwargs
### save_plot - 保存图像

```python
def save_plot(self, fig, save_path: str)
```
参数：
1. 位置参数
· fig: Plotly图形对象
· save_path: 保存路径

###  抽象方法：
    plot_result_npy(): 处理.npy格式数据的抽象方法
    plot_result_npz(): 处理.npz格式数据的抽象方法



使用示例

示例1：基本使用(以s21vfluxscope 为例子)

```python
from .plyplotter import QuantumDataPlyPlotter

class S21VfluxScopeDataPlyPlotter(QuantumDataPlyPlotter):
    ## 初始化
    def __init__(self):
        super().__init__("s21vfluxscope")

    def plot_result_npy(self, **kwargs):

        #======1======= 数据提取

        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')
        data = dict_param.item()
        image = data["image"]
        q_list = image.keys()
        volt_list = []
        freq_list = []
        s_list = []
        q_name_list = []
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



        #======2======= 创建子图布局,在该例子中没有双y轴,因此没有second_y参数

        n_plots = len(volt_list) * 2
        titles= [f"{q_name_list[i // 2]}" for i in range(n_plots)]
        fig,rows,cols = self.create_subplots(n_plots,titles)

        for ii in range(n_plots):
            row_pos = (ii // cols) + 1
            col_pos = (ii % cols) + 1
            volt = volt_list[ii // 2]
            freq = freq_list[ii // 2]
            s = s_list[ii // 2]
            q_name = q_name_list[ii // 2]
        #======3======= 添加2dmap,指定位置参数,其他可选参数如不指定则默认
            self.add_2dmap(fig,x=freq, y=volt,z=s.T,row=row_pos, col=col_pos)


            if (ii % 2 != 0):
                centcol = len(freq) // 2
                for j, curve in enumerate(coscurves_list[ii // 2]):
                    if curve: 
                        final_x_cos = [item[0] for item in curve]
                        final_y_cos = [item[1] for item in curve]
        #======4======= 添加line,指定位置参数,其他可选参数如不指定则默认
                        self.add_line(fig, x=final_x_cos,
                            y=final_y_cos,row=row_pos, col=col_pos,name=f'Cosine Curve {j + 1}',color_index=0,line_style_index=0)


                        if centcol < len(final_x_cos):
        #======5======= 添加annotation,指定位置参数,其他可选参数如不指定则默认
                            self.add_annotation(fig,x=final_x_cos[centcol],
                                y=final_y_cos[centcol],
                                text=f"conf:{cosconfs_list[ii // 2][j]:.2f}",row=row_pos,
                                col=col_pos)

                if lines_list[ii // 2]:
                    for j, line in enumerate(lines_list[ii // 2]):
                        if line:  # 确保直线数据不为空
                            final_x_line = [item[0] for item in line]
                            final_y_line = [item[1] for item in line]
        #======6======= 添加line,指定位置参数,其他可选参数如不指定则默认

                            self.add_line(fig, x=final_x_line,
                                          y=final_y_line, row=row_pos, col=col_pos, name=f'Cosine Curve {j + 1}',
                                          color_index=1,line_style_index=0)

                            if centcol < len(final_x_line):
        #======7======= 添加annotation,指定位置参数,其他可选参数如不指定则默认

                                self.add_annotation(fig, x=final_x_line[centcol],
                                                    y=final_y_line[centcol],
                                                    text=f"conf:{lineconfs_list[ii // 2][j]:.2f}", row=row_pos,
                                                    col=col_pos)


        #======8======= 更新子图的布局,指定位置参数,其他可选参数如不指定则默认

        self.update_layout(fig,rows,cols)

         #======9======= 配置坐标轴,指定位置参数,其他可选参数如不指定则默认,如不设置X/Y轴,不指定即可

        self.configure_axis(fig,rows,cols,xlable="Bias",ylable="Frequency (GHz)")
        return fig


```
