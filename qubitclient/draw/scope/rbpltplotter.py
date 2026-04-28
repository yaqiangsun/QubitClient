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

class RBDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("rb")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        fig, axes, rows, cols = self.create_subplots(len(qubit_names))
        axs = axes.flatten()

        params_list   = result.get("params_list",   [])
        r2_list       = result.get("r2_list",       [])
        fit_data_dense_list = result.get("fit_data_dense_list", [])
        x_dense_list  = result.get("x_dense_list",  [])

        for q_idx, q_name in enumerate(qubit_names):
            ax = axs[q_idx]
            item = image_dict.get(q_name)

            if not isinstance(item, (list, tuple)) or len(item) < 2:
                ax.axis('off')
                continue

            x_raw = np.asarray(item[0])
            y_raw = np.asarray(item[1][0])

            # 原始数据（散点）
            self.add_scatter(
                ax,
                x_raw,
                y_raw,
                label="Data",
                marker_index=1,           # 'o'
                color_index=6,            # 橙色
                alpha=0.7
            )

            # 拟合曲线 — 使用高密度数据
            if (q_idx < len(fit_data_dense_list) and 
                q_idx < len(x_dense_list) and
                fit_data_dense_list[q_idx] is not None and
                x_dense_list[q_idx] is not None and
                len(fit_data_dense_list[q_idx]) > 0 and
                len(x_dense_list[q_idx]) > 0):

                x_dense = np.asarray(x_dense_list[q_idx])
                fit_y_dense = np.asarray(fit_data_dense_list[q_idx])

                self.add_line(
                    ax,
                    x_dense,
                    fit_y_dense,
                    label="Fit",
                    color_index=0,
                    line_style_index=0
                )

            # 图例（每个子图独立）
            handles, labels = ax.get_legend_handles_labels()
            if handles:
                self.add_legend(
                    ax=ax,
                    handles=handles,
                    labels=labels,
                )

            # 参数文本（左上角） — 与 T1 格式保持一致风格
            if q_idx < len(params_list) and params_list[q_idx]:
                A, p, B = params_list[q_idx]          # 假设参数顺序为 A, p (decay), B
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0

                text_str = (
                    f"A  = {A:.3f}\n"
                    f"p  = {p:.4f}\n"
                    f"B  = {B:.3f}\n"
                    f"R² = {r2:.3f}"
                )


                self.add_annotation(
                    ax,
                    text_str,
                    xy=(0, 1),  # 子图左上角
                    annotation_xycoords="axes fraction",
                    annotation_textcoords="offset points",  # 改为 offset points
                    annotation_xytext=(10, -10),  # 向右10像素，向下10像素
                    color_index=0,
                    showarrow=False,
                    ha='left',
                    va='top'
                )
            # 坐标轴设置
            self.configure_axis(
                ax,
                title=q_name,
                xlabel="X",
                ylabel="Amp"
            )

        fig.tight_layout()
        return fig