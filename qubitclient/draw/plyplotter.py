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
from abc import ABC, abstractmethod
from typing import List, Optional
from .plyplotstyle import PlyPlotStyleConfig
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class QuantumDataPlyPlotter(ABC):
    def __init__(self, task_type: str, style_config: Optional[PlyPlotStyleConfig] = None):
        self.task_type = task_type
        self.style = style_config or PlyPlotStyleConfig()

    @abstractmethod
    def plot_result_npy(self, **kwargs):
        pass

    def plot_result_npz(self, **kwargs):
        pass

    def create_subplots(self, n_plots, titles: List[str], **kwargs):
        """创建基础画布"""
        cols = min(self.style.subplots_per_row, n_plots)

        rows = (n_plots // cols) + 1 if n_plots % cols != 0 else n_plots // cols
        secondy = kwargs.get("second_y")

        # vertical_spacing = min(0.2,(1 / (rows - 1)))
        if rows <= 2:
            vertical_spacing = 0.15
        elif rows <= 4:
            vertical_spacing = 0.10
        elif rows <= 6:
            vertical_spacing = 0.06
        elif rows <= 10:
            vertical_spacing = 0.04
        elif rows <= 15:
            vertical_spacing = 0.02
        elif rows <= 20:
            vertical_spacing = 0.015
        else:  # rows > 20
            vertical_spacing = 0.008
            vertical_spacing = min(1 / (rows - 1), vertical_spacing)

        if secondy:
            fig = make_subplots(
                rows=rows,
                cols=cols,
                subplot_titles=titles,
                horizontal_spacing=self.style.horizontal_spacing,
                vertical_spacing=vertical_spacing,
                shared_xaxes=False,
                shared_yaxes=False,
                specs=[[{"secondary_y": True} for _ in range(cols)] for _ in range(rows)]
            )
            fig.update_annotations(
                font=dict(
                    size=self.style.subtitle_fontsize,  # 子图标题字体大小，如 18
                    family=self.style.font_family,  # 字体族，如 'Arial'
                    color='black'  # 字体颜色
                )
            )
        else:
            fig = make_subplots(
                rows=rows,
                cols=cols,
                subplot_titles=titles,
                horizontal_spacing=self.style.horizontal_spacing,
                vertical_spacing=vertical_spacing,
                shared_xaxes=False,
                shared_yaxes=False
            )
            fig.update_annotations(
                font=dict(
                    size=self.style.subtitle_fontsize,  # 子图标题字体大小，如 18
                    family=self.style.font_family,  # 字体族，如 'Arial'
                    color='black'  # 字体颜色
                )
            )
        # for i in range(n_plots):
        #     row_pos = (i // cols) + 1
        #     col_pos = (i % cols) + 1
        #     fig.update_xaxes(
        #         tickformat='.1e',
        #         tickfont=dict(
        #             size=self.style.tick_fontsize,
        #             family=self.style.font_family,
        #             color='black',
        #             style='normal'  # 关键：设置为正常样式
        #         ),
        #         row=row_pos, col=col_pos
        #     )

        for i in range(n_plots, rows * cols):
            row_pos = (i // cols) + 1
            col_pos = (i % cols) + 1
            fig.update_xaxes(visible=False, row=row_pos, col=col_pos)
            fig.update_yaxes(visible=False, row=row_pos, col=col_pos)

        return fig, rows, cols

    def add_2dmap(self, fig: go.Figure, z: np.ndarray, x: np.ndarray, y: np.ndarray,
                  row: int, col: int, showscale=False, colorscale_index=0, **kwargs) -> None:
        color_scale = self.style.color_scale[colorscale_index % len(self.style.color_scale)]

        fig.add_trace(
            go.Heatmap(
                z=z,
                x=x,
                y=y,
                colorscale=color_scale,
                showscale=showscale,
                colorbar=self.style.colorbar_config
            ),
            row=row, col=col, **kwargs
        )

    def add_histogram(self, fig: go.Figure, x, xbins, nbinsx,
                      row: int, col: int, name="", marker_color_index=0, **kwargs) -> None:

        marker_color = self.style.marker_color_palette[marker_color_index % len(self.style.marker_color_palette)]
        fig.add_trace(
            go.Histogram(
                x=x,
                nbinsx=nbinsx,
                opacity=self.style.opacity,
                xbins=xbins,
                name=name,
                marker_color=marker_color,
                histnorm=self.style.histnorm
            ),
            row=row, col=col, **kwargs
        )

    def add_scatter(self, fig: go.Figure, x, y,
                    row: int, col: int, color_index=0, marker_index=0, name="None",
                    showlegend: bool = False, **kwargs) -> None:
        color = self.style.marker_color_palette[color_index % len(self.style.marker_color_palette)]
        marker = self.style.marker_styles[marker_index % len(self.style.marker_styles)]
        fig.add_scatter(
            x=x, y=y,
            mode='markers',
            marker=dict(
                color=color,
                size=self.style.marker_size,
                opacity=self.style.marker_opacity, symbol=marker
            ),
            name=name,
            showlegend=showlegend,
            row=row, col=col, **kwargs
        )

    def add_scatter_points_with_anno(self, fig: go.Figure, x, y,
                                     row: int, col: int, color_index=0, name="None", text="None",
                                     showlegend: bool = False, **kwargs) -> None:
        """统一的散点图添加方法"""
        color = self.style.marker_color_palette[color_index % len(self.style.marker_color_palette)]

        fig.add_scatter(

            x=x, y=y,
            mode='markers+text',
            marker=dict(
                color=color,
                size=self.style.marker_size,
                opacity=self.style.marker_opacity
            ),
            name=name,
            text=text,
            textposition='bottom center',
            textfont=dict(size=10, color='darkred'),
            showlegend=showlegend,
            row=row, col=col, **kwargs
        )

    def add_line(self, fig: go.Figure, x, y,
                 row: int, col: int, color_index: int = 0, line_style_index: int = 0, name: str = "None",
                 showlegend: bool = False, **kwargs) -> None:
        """统一的线条添加方法"""
        color = self.style.line_colors[color_index % len(self.style.line_colors)]

        linestyle = self.style.line_styles[line_style_index % len(self.style.line_styles)]
        fig.add_scatter(
            x=x, y=y,
            mode='lines',
            line=dict(
                color=color,
                width=self.style.line_width,
                dash=linestyle
            ),
            name=name,
            showlegend=showlegend,
            row=row, col=col, **kwargs
        )

    def add_annotation(self, fig: go.Figure, text: str,
                       row: int, col: int, x: float = 0.95, y: float = 0.95, xref="x", yref="y", showarrow=True,
                       **kwargs) -> None:
        if showarrow:
            annotation_kwargs = {

                'x': x,
                'y': y,
                'xref': xref,
                'yref': yref,
                'text': text,
                'row': row,
                'col': col,
                'font': {
                    'size': self.style.annotation_font_size,
                    'color': self.style.annotation_font_color
                },
                'bgcolor': 'rgba(255,255,0,0.7)',  # 直接设置黄色背景，alpha=0.7
                'bordercolor': 'rgba(0,0,0,0.7)',   # 边框也是 alpha=0.7
                'borderwidth': self.style.annotation_borderwidth,
                'showarrow': showarrow,
                'arrowhead': 2,  # 箭头类型：0=无箭头，1=曲线，2=三角箭头，3=尖三角，4=开放箭头
                'arrowsize': 1.2,  # 箭头大小
                'arrowwidth': 1.5,  # 箭头线宽
                'arrowcolor': 'black',  # 箭头颜色
                **kwargs
            }
        else:
            annotation_kwargs = {

                'x': x,
                'y': y,
                'xref': xref,
                'yref': yref,
                'text': text,
                'row': row,
                'col': col,
                'font': {
                    'size': self.style.annotation_font_size,
                    'color': self.style.annotation_font_color
                },
                'bgcolor': 'rgba(255,255,0,0.7)',  # 直接设置黄色背景，alpha=0.7
                'bordercolor': 'rgba(0,0,0,0.7)',  # 边框也是 alpha=0.7
                'borderwidth': self.style.annotation_borderwidth,
                'showarrow': showarrow,
                **kwargs
            }
        fig.add_annotation(**annotation_kwargs)

    def add_vline(self, fig: go.Figure, x: float,
                  row: int, col: int, color_index: int = 0, line_style_index: int = 0,
                  **kwargs) -> None:
        """统一的阈值线添加方法"""
        color = self.style.line_colors[color_index % len(self.style.line_colors)]
        linestyle = self.style.line_styles[line_style_index % len(self.style.line_styles)]

        fig.add_vline(
            x=x,
            line_dash=linestyle,
            line_color=color,
            opacity=0.7,
            row=row, col=col, **kwargs
        )

    def update_layout(self, fig: go.Figure, rows: int, cols: int, showlegend: Optional[bool] = False, **kwargs) -> None:
        """统一的布局更新方法"""
        fig.update_layout(
            height=self.style.figure_height_per_row * rows,
            width=(self.style.figure_width_per_col * cols),
            margin=dict(r=60, t=60, b=60, l=60),
            showlegend=showlegend,
            legend=self.style.legend,
            font=dict(
                family=self.style.font_family,
                size=self.style.font_size
            ),
            **kwargs
        )

    def configure_axis(self, fig: go.Figure, rows: int, cols: int, xlable=None, ylable=None, **kwargs) -> None:
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                if xlable:
                    fig.update_xaxes(title_text=xlable, row=i, col=j)
                if ylable:
                    fig.update_yaxes(title_text=ylable, row=i, col=j, **kwargs)

    def save_plot(self, fig, save_path: str):
        directory = os.path.dirname(save_path)
        if os.path.exists(directory):
            fig.write_html(save_path)  # save_path  最中存储路径 “./tmp/client/result_s21peak_tmp***.html”
        return fig