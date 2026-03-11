import os
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Union
from .pltplotstyle import PltPlotStyleConfig

class QuantumDataPltPlotter(ABC):
    """统一绘图基类"""

    def __init__(self, task_type: str, style_config: Optional[PltPlotStyleConfig] = None):
        self.task_type = task_type
        self.style = style_config or PltPlotStyleConfig()

    @abstractmethod
    def plot_result_npy(self, **kwargs) -> plt.Figure:
        """绘制npy格式结果"""
        pass

    def plot_result_npz(self, **kwargs) -> plt.Figure:
        """绘制npz格式结果"""
        return self.plot_result_npy(**kwargs)

    def create_subplots(self, n_plots: int, **kwargs) -> Tuple[plt.Figure, np.ndarray, int, int]:
        """创建统一风格的子图布局，返回标准化后的二维 axes 数组"""
        if n_plots < 1:
            raise ValueError("n_plots must be at least 1")

        cols = min(n_plots, self.style.max_cols)
        rows = (n_plots + cols - 1) // cols   # 向上取整

        figsize = self.style.get_figure_size(rows, cols)
        fig, axes = plt.subplots(rows, cols, figsize=figsize, squeeze=False)

        # squeeze=False 强制返回 (rows, cols) 形状的二维数组，即使 rows=1 或 cols=1
        # 把多余的 axes 关掉（如果有）
        for i in range(n_plots, rows * cols):
            axes[i // cols, i % cols].axis('off')

        # 统一处理 axes 为二维数组（已经保证了）
        axes = np.asarray(axes).reshape(rows, cols)

        for ax in axes.flat:
            ax.set_aspect('auto')
            ax.autoscale(enable=True, axis='y', tight=True)

        plt.subplots_adjust(
            hspace=self.style.subplot_hspace,
            wspace=self.style.subplot_wspace,
            left=self.style.subplot_left,
            right=self.style.subplot_right,
            top=self.style.subplot_top,
            bottom=self.style.subplot_bottom
        )

        return fig, axes, rows, cols

    def configure_axis(self, ax: plt.Axes, title: Optional[str] = None,
                       xlabel: Optional[str] = None, ylabel: Optional[str] = None, show_legend: bool = True,**kwargs):
        """配置坐标轴样式"""
        # 设置刻度样式
        ax.tick_params(labelsize=self.style.tick_labelsize,
                       direction=self.style.tick_direction)

        # 设置标签
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=self.style.label_fontsize,
                          color=self.style.label_color)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=self.style.label_fontsize,
                          color=self.style.label_color)

        # 设置标题
        if title:
            ax.set_title(title, fontsize=self.style.title_fontsize,
                         fontweight=self.style.title_fontweight,
                         color=self.style.title_color, pad=self.style.title_pad)

        # 网格
        if self.style.show_grid:
            ax.grid(True, alpha=self.style.grid_alpha,
                    linestyle=self.style.grid_linestyle)

        return None

    def add_line(self, ax: plt.Axes, x, y,
                 label: str = '', line_style_index: int = 0, color_index: int = 0,
                  **kwargs):
        """添加统一风格的线条"""
        color = self.style.line_colors[color_index % len(self.style.line_colors)]
        linestyle = self.style.line_styles[line_style_index % len(self.style.line_styles)]

        line = ax.plot(x, y, color=color, linestyle=linestyle,
                              linewidth=self.style.line_width, label=label, **kwargs)
        return line, ax


    def add_2dmap(self, ax: plt.Axes, x, y,s,
                 label: str = '', shading_index: int = 0, cmap_index: int = 0,
                  **kwargs):
        """添加统一风格的线条"""
        cmap = self.style.cmap[cmap_index % len(self.style.cmap)]
        shading = self.style.shading[shading_index % len(self.style.shading)]
        mesh = ax.pcolormesh(x, y, s, shading=shading, cmap=cmap)
        return mesh

    def add_histogram(self, ax: plt.Axes, x, bins,xrange,
                  **kwargs):

        ax.hist(x, bins=100, density=self.style.histogram_density, range=xrange, alpha=self.style.histogram_alpha)


    def add_scatter(self, ax: plt.Axes, x,y, label: str = '',
                    marker_index: int = 0, color_index: int = 0, **kwargs):
        """添加统一风格的散点"""
        marker = self.style.marker_styles[marker_index % len(self.style.marker_styles)]
        color = self.style.marker_colors[color_index % len(self.style.marker_colors)]

        scatter = ax.scatter(x, y, color=color, marker=marker,
                             s=self.style.marker_size, label=label,
                             edgecolors='black', linewidth=self.style.marker_edge_width,
                             **kwargs)
        return scatter

    def add_annotation(self, ax: plt.Axes, text: str, xy: Tuple[float, float],annotation_xycoords: str="data",annotation_textcoords: str = "offset points",
    annotation_xytext = (0, 10),color_index: int = 0,showarrow=True, **kwargs):
        """添加统一风格的注释"""
        color = self.style.marker_colors[color_index % len(self.style.marker_colors)]
        if showarrow:
            arrow = self.style.annotation_arrowprops
        else:
            arrow = None

        annotation = ax.annotate(text, xy,
                                 xycoords=annotation_xycoords,
                                 textcoords=annotation_textcoords,
                                 fontsize=self.style.annotation_fontsize,
                                 color=color, xytext=annotation_xytext,
                                 bbox=self.style.annotation_bbox,arrowprops = arrow, **kwargs)
        return annotation


    def add_vline(self, ax: plt.Axes, x: float, label=None,**kwargs):
        """添加统一风格的竖线"""
        color = self.style.vline_color
        vline = ax.axvline(x, label=label, color=color, linestyle=self.style.vline_style,
                           alpha=self.style.vline_alpha,
                           linewidth=self.style.vline_width,**kwargs)
        return vline



    def add_legend(self, ax: plt.Axes, handles=None, labels=None, twinx: bool = False):
        """添加统一风格的图例"""
        target_ax = ax.twinx() if twinx else ax

        if handles is None or labels is None:
            legend = target_ax.legend(loc=self.style.legend_loc,
                                      fontsize=self.style.legend_fontsize,
                                      bbox_to_anchor=self.style.legend_bbox_to_anchor)
        else:
            legend = target_ax.legend(handles, labels,
                                      loc=self.style.legend_loc,
                                      fontsize=self.style.legend_fontsize,
                                      bbox_to_anchor=self.style.legend_bbox_to_anchor)
        return legend
   
    def save_plot(self, fig: plt.Figure, save_path: str):
        """保存图片"""
        directory = os.path.dirname(save_path)
        if os.path.exists(directory):
            fig.savefig(save_path, dpi=300, bbox_inches='tight',pad_inches=0)

        return fig