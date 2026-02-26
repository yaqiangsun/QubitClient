
from typing import List, Tuple

class PltPlotStyleConfig:
    """绘图风格配置类"""

    # create_subplots参数
    figure_width: float = 15
    def get_figure_size(self, rows: int, cols: int) -> Tuple[float, float]:
        """计算图形尺寸"""
        width = self.figure_width
        height = width *  (rows / cols)
        return width, height

    
    max_cols: int = 2
    subplot_hspace: float = 0.1
    subplot_wspace: float = 0.1
    subplot_left: float = 0.05
    subplot_right: float = 0.95
    subplot_bottom: float = 0.01
    subplot_top: float =0.99

    show_grid: bool = True
    grid_alpha: float = 0.3
    grid_linestyle: str = '--'


    # add_line 参数
    line_width: float = 2
    line_styles: List[str] =  ['-', '--', '-.', ':','o']
    line_colors: List[str] =  [
        '#1f77b4',  # 蓝
        '#2ca02c',  # 绿
        '#ff7f0e',  # 橙
        '#d62728',  # 红
        '#9467bd',  # 紫
        '#8c564b',  # 棕
        '#e377c2',  # 粉
        '#7f7f7f',  # 灰
        '#bcbd22',  # 黄绿
        '#17becf',  # 青
        'C3',
        'C4',
        'C0',
        'C1'
    ]

    # add_scatter 参数
    marker_styles: List[str] =  ['.','o', 's', '^', 'D', 'v', '*', 'p', 'h', 'x', '+']
    marker_colors: List[str] = [
        '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF',
        '#00FFFF', '#FFA500', '#800080', '#008000', '#FFC0CB',
        '#4B0082', '#FF4500', '#2E8B57', '#DA70D6', '#1E90FF',
        '#32CD32', '#8A2BE2', '#DC143C', '#00CED1', '#FFD700',
        '#006400', '#8B4513'
    ]
    marker_size: int = 100
    marker_edge_width: float = 0.5

    # add_2dmap 参数
    shading: List[str] =  ['auto', 'flat', 'nearest', 'gouraud']
    cmap: List[str] =  ['viridis', 'jet', 'hot', 'coolwarm', 'RdBu', 'gray']

    # add_vline 参数
    vline_style: str = '--'
    vline_alpha: float = 0.7
    vline_width: float = 1.0
    vline_color: str = 'red'


    # configure_axis 参数
    title_fontsize: int = 14
    title_fontweight: str = 'bold'
    title_color: str = 'black'
    title_pad: int = 15

    label_fontsize: int = 12
    label_color: str = 'black'

    tick_labelsize: int = 10
    tick_direction: str = 'in'

    # add_legend 参数
    legend_fontsize: int = 12
    legend_loc: str = 'upper left'
    legend_bbox_to_anchor: Tuple[float, float] = (1.05, 1)
    legend_max_scatters = 5
    legend_max_lines = 5

    # add_annotation 参数
    annotation_fontsize: int = 10
    annotation_bbox = dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7)
    annotation_arrowprops = dict(arrowstyle='->', connectionstyle='arc3,rad=0')


    # add_histogram 参数
    histogram_density=True
    histogram_alpha=0.5




    

   