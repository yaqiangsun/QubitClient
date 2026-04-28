# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:03
########################################################################

import os
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from typing import Tuple, Optional
from .pltplotstyle import PltPlotStyleConfig

class QuantumDataPltPlotter(ABC):
    """统一绘图基类"""

    def __init__(self, task_type: str, style_config: Optional[PltPlotStyleConfig] = None):
        self.task_type = task_type
        self.style = style_config or PltPlotStyleConfig()
        self._current_n_subplots = 0  # 记录当前子图数量

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

        self._current_n_subplots = n_plots

        cols = min(n_plots, self.style.max_cols)
        rows = (n_plots + cols - 1) // cols

        figsize = self.style.get_figure_size(rows, cols)
        fig, axes = plt.subplots(rows, cols, figsize=figsize, squeeze=False)

        # 隐藏多余子图
        for i in range(n_plots, rows * cols):
            axes[i // cols, i % cols].axis('off')

        axes = np.asarray(axes).reshape(rows, cols)

        for ax in axes.flat:
            ax.set_aspect('auto')
            ax.autoscale(enable=True, axis='y', tight=True)

        # 使用布局参数
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
                       xlabel: Optional[str] = None, ylabel: Optional[str] = None,
                       show_legend: bool = True, **kwargs):
        """配置坐标轴样式（固定字体大小，保证不同子图数量时一致）"""

        # 设置刻度样式 - 使用固定字体大小
        ax.tick_params(labelsize=self.style.tick_labelsize,
                       direction=self.style.tick_direction,
                       width=1.2,  # 刻度线宽度
                       length=6)  # 刻度线长度

        # 设置标签 - 增大字体
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
                    linestyle=self.style.grid_linestyle, linewidth=0.8)

        # 设置坐标轴线宽
        for spine in ax.spines.values():
            spine.set_linewidth(1.2)

        return None

    def add_line(self, ax: plt.Axes, x, y,
                 label: str = '', line_style_index: int = 0, color_index: int = 0,
                 **kwargs):
        """添加统一风格的线条（加粗）"""
        color = self.style.line_colors[color_index % len(self.style.line_colors)]
        linestyle = self.style.line_styles[line_style_index % len(self.style.line_styles)]

        line = ax.plot(x, y, color=color, linestyle=linestyle,
                       linewidth=self.style.line_width, label=label, **kwargs)
        return line, ax

    def add_2dmap(self, ax: plt.Axes, x, y, s,
                  label: str = '', shading_index: int = 0, cmap_index: int = 0,
                  **kwargs):
        """添加统一风格的热图"""
        cmap = self.style.cmap[cmap_index % len(self.style.cmap)]
        shading = self.style.shading[shading_index % len(self.style.shading)]
        mesh = ax.pcolormesh(x, y, s, shading=shading, cmap=cmap)
        return mesh

    def add_histogram(self, ax: plt.Axes, x, bins=100, xrange=None,
                      **kwargs):
        """添加直方图"""
        ax.hist(x, bins=bins, density=self.style.histogram_density,
                range=xrange, alpha=self.style.histogram_alpha,
                linewidth=1.5, edgecolor='black', **kwargs)

    def add_scatter(self, ax: plt.Axes, x, y, label: str = '',
                    marker_index: int = 0, color_index: int = 0, **kwargs):
        """添加统一风格的散点"""
        marker = self.style.marker_styles[marker_index % len(self.style.marker_styles)]
        color = self.style.marker_colors[color_index % len(self.style.marker_colors)]

        scatter = ax.scatter(x, y, color=color, marker=marker,
                             s=self.style.marker_size, label=label,
                             edgecolors='black', linewidth=self.style.marker_edge_width,
                             **kwargs)
        return scatter

    def add_annotation(self, ax: plt.Axes, text: str, xy: Tuple[float, float],
                       annotation_xycoords: str = "data",
                       annotation_textcoords: str = "offset points",
                       annotation_xytext=(0, 10), color_index: int = 0,
                       showarrow=True, **kwargs):
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
                                 bbox=self.style.annotation_bbox, arrowprops=arrow, **kwargs)
        return annotation

    def add_vline(self, ax: plt.Axes, x: float, label=None, **kwargs):
        """添加统一风格的竖线"""
        color = self.style.vline_color
        vline = ax.axvline(x, label=label, color=color, linestyle=self.style.vline_style,
                           alpha=self.style.vline_alpha,
                           linewidth=self.style.vline_width, **kwargs)
        return vline

    def add_legend(self, ax: plt.Axes, handles=None, labels=None, twinx: bool = False):
        """添加统一风格的图例，自动换行居中"""
        target_ax = ax.twinx() if twinx else ax

        # 获取图例句柄和标签
        if handles is None or labels is None:
            handles, labels = target_ax.get_legend_handles_labels()

        if not handles:  # 没有图例项时直接返回
            return None

        n_items = len(handles)


        ncol = 2


        # 根据列数调整图例位置

        bbox_anchor = (0.5, -0.15)

        # 创建图例 - 使用固定字体大小
        # legend = target_ax.legend(
        #     handles, labels,
        #     loc=self.style.legend_loc,
        #     fontsize=self.style.legend_fontsize,
        #     bbox_to_anchor=bbox_anchor,
        #     ncol=ncol,
        #     frameon=True,
        #     fancybox=True,
        #     shadow=False,
        #     handlelength=2.0,  # 图例线长度
        #     handletextpad=0.8,  # 图标与文字间距
        #     columnspacing=1.2  # 列间距
        # )
        legend = target_ax.legend(
            handles, labels,
            loc='upper right',  # 右上角
            fontsize=self.style.legend_fontsize,
            frameon=True,
            fancybox=True,
            shadow=False,
            handlelength=2.0,
            handletextpad=0.8,
            columnspacing=1.2
        )
        # 设置图例边框线宽
        if legend:
            legend.get_frame().set_linewidth(1.0)

        return legend

    def save_plot(self, fig: plt.Figure, save_path: str, bbox_inches: str = 'tight',
                  pad_inches: float = 0.2, dpi: int = 200):
        """保存图片，确保边框完整"""
        directory = os.path.dirname(save_path)
        if directory:  # 避免空字符串
            os.makedirs(directory, exist_ok=True)

        # 保存前确保布局完整
        fig.tight_layout(pad=0.5, h_pad=0.5, w_pad=0.5)

        # 使用 bbox_inches='tight' 自动包含所有元素
        fig.savefig(save_path, dpi=dpi, bbox_inches=bbox_inches,
                    pad_inches=pad_inches, facecolor='white', edgecolor='none')

        return fig