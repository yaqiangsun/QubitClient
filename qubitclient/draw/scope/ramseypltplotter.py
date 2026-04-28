# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:03
########################################################################

from ..pltplotter import QuantumDataPltPlotter
import matplotlib.pyplot as plt
import numpy as np


class RamseyDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("ramsey")

    def plot_result_npy(self, **kwargs):
        result     = kwargs.get('result')
        dict_param = kwargs.get('dict_param')


        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get('image', {})
        qubit_names = list(image_dict.keys())

        fig, axes, rows, cols = self.create_subplots(len(qubit_names))
        axs = axes.flatten()

        params_list   = result.get("params_list", [])
        r2_list       = result.get("r2_list", [])
        fit_data_list = result.get("fit_data_list", [])

        for q_idx, q_name in enumerate(qubit_names):
            ax = axs[q_idx]
            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                ax.axis('off')
                continue

            x_raw = np.asarray(item[0])
            y_raw = np.asarray(item[1])

            # 原始数据（散点）
            scatter = self.add_scatter(
                ax,
                x_raw,
                y_raw,
                label="Data",
                marker_index=1,  # 'o'
                color_index=6,  # 橙色
                alpha=0.7
            )
            if q_idx < len(fit_data_list):
                y_fit = np.asarray(fit_data_list[q_idx])
                x_fit = x_raw if len(y_fit) == len(x_raw) else np.linspace(x_raw.min(), x_raw.max(), len(y_fit))
                self.add_line(
                    ax,
                    x_fit,
                    y_fit,
                    label="Fit",
                    color_index=0,
                    line_style_index=0
                )
            handles, labels = ax.get_legend_handles_labels()
            if handles:
                self.add_legend(
                    ax=ax,
                    handles=handles,
                    labels=labels,
                )
            if q_idx < len(params_list):
                A, B, freq, phi, T2 = params_list[q_idx]
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0
                text = (f"A={A:.3f}\nB={B:.3f}\nf={freq/1e6:.3f}MHz\n"
                        f"φ={phi:.3f}\nT2={T2:.1f}µs\nR²={r2:.4f}")
                self.add_annotation(
                    ax,
                    text,
                    xy=(0, 1),  # 子图左上角
                    annotation_xycoords="axes fraction",
                    annotation_textcoords="offset points",  # 改为 offset points
                    annotation_xytext=(10, -10),  # 向右10像素，向下10像素
                    color_index=0,
                    showarrow=False,
                    ha='left',
                    va='top'
                )

            self.configure_axis(
                ax,
                title=q_name,
                xlabel="Time (ns)",
                ylabel="P(|1>)"
            )
        fig.tight_layout()
        return fig