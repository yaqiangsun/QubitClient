# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.

from ..pltplotter import QuantumDataPltPlotter
import numpy as np


class XyzTimingDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("xyz_timing")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get("result")
        dict_param = kwargs.get("dict_param")

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        fig, axes, rows, cols = self.create_subplots(len(qubit_names))
        axs = axes.flatten()

        fit_data_list = result.get("fit_data_list", [])
        r2_list = result.get("r2_list", [])
        zd_xy_list = result.get("zd_xy_list", [])
        x_out_list = result.get("x_out_list", [])

        for q_idx, q_name in enumerate(qubit_names):
            ax = axs[q_idx]
            item = image_dict.get(q_name)
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                ax.axis("off")
                continue

            y_raw = np.asarray(item[0], dtype=float)
            x_raw = np.asarray(item[1], dtype=float)

            self.add_line(
                ax,
                x_raw,
                y_raw,
                label="Data",
                color_index=6,
                line_style_index=0,
                marker="o",
                markersize=4,
                alpha=0.7,
            )

            if q_idx < len(fit_data_list):
                y_fit = np.asarray(fit_data_list[q_idx], dtype=float)
                if q_idx < len(x_out_list) and len(x_out_list[q_idx]) == len(y_fit):
                    x_fit = np.asarray(x_out_list[q_idx], dtype=float)
                elif len(y_fit) == len(x_raw):
                    x_fit = x_raw
                else:
                    x_fit = np.linspace(x_raw.min(), x_raw.max(), len(y_fit))
                self.add_line(
                    ax,
                    x_fit,
                    y_fit,
                    label="Fit",
                    color_index=0,
                    line_style_index=0,
                )

            if q_idx < len(zd_xy_list):
                self.add_vline(ax, zd_xy_list[q_idx] * 1e-9, label="zd_xy")
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0
                text = f"zd_xy={zd_xy_list[q_idx]:.3f} ns\nR²={r2:.4f}"
                self.add_annotation(
                    ax,
                    text,
                    xy=(0, 1),
                    annotation_xycoords="axes fraction",
                    annotation_textcoords="offset points",
                    annotation_xytext=(10, -10),
                    color_index=0,
                    showarrow=False,
                    ha="left",
                    va="top",
                )

            handles, labels = ax.get_legend_handles_labels()
            if handles:
                self.add_legend(ax=ax, handles=handles, labels=labels)

            self.configure_axis(
                ax,
                title=f"Timing_xyz {q_name}",
                xlabel="t",
                ylabel="amp",
            )

        fig.tight_layout()
        return fig
