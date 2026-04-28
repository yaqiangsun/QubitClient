# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:03
########################################################################


from typing import List, Tuple

class PltPlotStyleConfig:
    """绘图风格配置类"""

    # 每个子图的固定尺寸（英寸）- 保证字体大小一致
    subplot_width: float = 6.0  # 每个子图的宽度（英寸）- 增大以容纳更大字体
    subplot_height: float = 5.0  # 每个子图的高度（英寸）- 增大以容纳更大字体

    def get_figure_size(self, rows: int, cols: int) -> Tuple[float, float]:
        """根据子图数量和大小计算图形尺寸，保持每个子图物理尺寸固定"""
        width = self.subplot_width * cols
        height = self.subplot_height * rows
        # 为图例和边距增加额外空间
        width += 1.2  # 左右边距
        height += 1.5  # 上下边距（给图例留空间）
        return width, height

    max_cols: int = 2
    subplot_hspace: float = 0.2  # 增大子图间距
    subplot_wspace: float = 0.2
    subplot_left: float = 0.10  # 左边距
    subplot_right: float = 0.94  # 右边距
    subplot_bottom: float = 0.15  # 底部空间，给图例
    subplot_top: float = 0.90  # 顶部空间

    show_grid: bool = True
    grid_alpha: float = 0.3
    grid_linestyle: str = '--'

    # 字体大小 - 增大所有字体
    title_fontsize: int = 18  # 标题字体（原来是12）
    label_fontsize: int = 15  # 坐标轴标签字体（原来是10）
    tick_labelsize: int = 13  # 刻度字体（原来是9）
    legend_fontsize: int = 13  # 图例字体（原来是9）

    # add_line 参数 - 线条加粗
    line_width: float = 2.5  # 线条宽度（原来是2）
    line_styles: List[str] = ['-', '--', '-.', ':', 'o']
    line_colors: List[str] = [
        '#1f77b4', '#2ca02c', '#ff7f0e', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        'C3', 'C4', 'C0', 'C1'
    ]

    # add_scatter 参数
    marker_styles: List[str] = ['.', 'o', 's', '^', 'D', 'v', '*', 'p', 'h', 'x', '+']
    marker_colors: List[str] = [
        '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF',
        '#00FFFF', '#FFA500', '#800080', '#008000', '#FFC0CB',
        '#4B0082', '#FF4500', '#2E8B57', '#DA70D6', '#1E90FF',
        '#32CD32', '#8A2BE2', '#DC143C', '#00CED1', '#FFD700',
        '#006400', '#8B4513'
    ]
    marker_size: int = 120  # 散点大小（原来是100）
    marker_edge_width: float = 0.8  # 散点边框宽度（原来是0.5）

    # add_2dmap 参数
    shading: List[str] = ['auto', 'flat', 'nearest', 'gouraud']
    cmap: List[str] = ['viridis', 'jet', 'hot', 'coolwarm', 'RdBu', 'gray']

    # add_vline 参数
    vline_style: str = '--'
    vline_alpha: float = 0.7
    vline_width: float = 1.5  # 竖线宽度（原来是1.0）
    vline_color: str = 'red'

    # configure_axis 参数
    title_fontweight: str = 'bold'
    title_color: str = 'black'
    title_pad: int = 20  # 标题间距（原来是15）

    label_color: str = 'black'
    tick_direction: str = 'in'

    # add_legend 参数 - 图例放在图下方
    legend_loc: str = 'upper center'
    legend_bbox_to_anchor: Tuple[float, float] = (0.5, -0.18)  # 调整位置适应更大字体
    legend_max_scatters: int = 5
    legend_max_lines: int = 5

    # add_annotation 参数
    annotation_fontsize: int = 12  # 注释字体（原来是10）
    annotation_bbox = dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7)
    annotation_arrowprops = dict(arrowstyle='->', connectionstyle='arc3,rad=0')

    # add_histogram 参数
    histogram_density: bool = True
    histogram_alpha: float = 0.5