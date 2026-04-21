# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:03
########################################################################

from ..pltplotter import QuantumDataPltPlotter
import numpy as np


class T2FitDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("t2fit")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        n_qubits = len(qubit_names)
        fig, axes, rows, cols = self.create_subplots(n_qubits)
        axs = axes.flatten()

        #如果数据点较少可以使用'x_dense'和'fit_data_dense'
        params_list   = result.get("params_list",   [])
        r2_list       = result.get("r2_list",       [])
        fit_data_dense_list = result.get("fit_data_dense_list", [])
        x_dense_list = result.get("x_dense_list", [])

        for q_idx, q_name in enumerate(qubit_names):
            ax = axs[q_idx]
            item = image_dict.get(q_name)

            if not isinstance(item, (list, tuple)) or len(item) < 2:
                ax.axis('off')
                continue

            x_raw = np.asarray(item[0])
            y_raw = np.asarray(item[1])


            # 原始数据 - 散点
            scatter = self.add_scatter(
                ax,
                x_raw,
                y_raw,
                label="Data",           # 每个子图都给 label
                marker_index=1,         # 'o'
                color_index=6,          # 橙色
                alpha=0.7
            )

            # 拟合曲线
            if (q_idx < len(fit_data_dense_list) and 
                q_idx < len(x_dense_list) and
                fit_data_dense_list[q_idx] is not None and 
                x_dense_list[q_idx] is not None and
                len(fit_data_dense_list[q_idx]) > 0 and
                len(x_dense_list[q_idx]) > 0):
                
                fit_data_dense = np.asarray(fit_data_dense_list[q_idx])
                x_dense = np.asarray(x_dense_list[q_idx]) 
    
                self.add_line(
                    ax,
                    x_dense,
                    fit_data_dense,
                    label="Fit",            # 每个子图都给 label
                    color_index=0,          # 蓝色
                    line_style_index=0
                )

            # 图例：每个子图都尝试添加
            handles, labels = ax.get_legend_handles_labels()
            if handles:  
                self.add_legend(
                    ax=ax,
                    handles=handles,
                    labels=labels,
                )

            # 参数文本
            if q_idx < len(params_list) and params_list[q_idx]:
                A, B, T1, T2, w, phi = params_list[q_idx]
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0

                text_str = (
                    f"A   = {A:.3f}\n"
                    f"B   = {B:.3f}\n"
                    f"T₁  = {T1:.1f} s\n"
                    f"T₂  = {T2*1e6:.3f} µs\n"
                    f"ω   = {w/1e6:.3f} MHz\n"
                    f"φ   = {phi:.3f}\n"
                    f"R²  = {r2:.3f}"
                )

                self.add_annotation(
                    ax,
                    text_str,
                    xy=(0, 1),                 
                    annotation_xycoords="axes fraction",
                    annotation_textcoords="axes fraction",
                    annotation_xytext=(0, 1),
                    color_index=0,
                    showarrow=False,
                    ha='left',                      # 文字左对齐
                    va='top'                      # 文字顶部对齐
                )

            # 坐标轴标题
            self.configure_axis(
                ax,
                title=q_name,
                xlabel="Time",
                ylabel="Amp"
            )

        fig.tight_layout()
        return fig