# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:03
########################################################################

from typing import List

class PlyPlotStyleConfig:

    # create_subplots 参数
    subplots_per_row: int = 2
    horizontal_spacing: float = 0.1

    # add_2dmap 参数
    colorbar_config = {
        'thickness': 15,
        'len': 0.7,
        'yanchor': 'middle',
        'y': 0.5
    }
    color_scale = ['Viridis',"RdBu"]
   

    # add_scatter 参数
    marker_size: int = 10
    marker_styles = ["circle","square","diamond"]
    marker_opacity: float = 0.7
    marker_color_palette = [
        '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF',  # 红、绿、蓝、黄、紫
        '#00FFFF', '#FFA500', '#800080', '#008000', '#FFC0CB',  # 青、橙、紫红、深绿、粉红
        '#4B0082', '#FF4500', '#2E8B57', '#DA70D6', '#1E90FF',  # 靛蓝、橙红、海绿、兰紫、道奇蓝
        '#32CD32', '#8A2BE2', '#DC143C', '#00CED1', '#FFD700',  # 酸橙、紫罗兰、深红、深青、金色
        '#006400', '#8B4513'  # 深绿、鞍褐
    ]
    
    # add_line 参数
    line_width: int = 2
    line_styles = ["solid","dash","dot","dashdot","longdash"]
    line_colors: List[str] = [
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
    

    

   

    # add_annotation 参数
    annotation_font_size: int = 12
    annotation_font_color: str = 'red'
    annotation_bordercolor =  'black'
    annotation_bgcolor =  'yellow'
    annotation_borderwidth = 1


    # update_layout 参数
    figure_height_per_row: int = 400
    figure_width_per_col: int = 800
    font_family: str = 'Arial'
    font_size: int = 12
    legend=dict(
                x=1.05,
                y=0.5,
                xanchor='left',
                yanchor='middle',
                groupclick="toggleitem"
            )
    # add_histogram 参数
    opacity = 0.5
    histnorm = "probability density"


