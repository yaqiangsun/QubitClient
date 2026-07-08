# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.

from ..plyplotter import QuantumDataPlyPlotter
import numpy as np


class XyzTimingDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("xyz_timing")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get("result")
        dict_param = kwargs.get("dict_param")

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())
        titles = [f"Timing_xyz {q_name}" for q_name in qubit_names]

        fig, rows, cols = self.create_subplots(
            n_plots=len(qubit_names),
            titles=titles,
            second_y=False,
        )

        fit_data_list = result.get("fit_data_list", [])
        r2_list = result.get("r2_list", [])
        zd_xy_list = result.get("zd_xy_list", [])
        x_out_list = result.get("x_out_list", [])

        show_data_legend = True
        show_fit_legend = True

        for q_idx, q_name in enumerate(qubit_names):
            row = q_idx // cols + 1
            col = q_idx % cols + 1
            item = image_dict.get(q_name)
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            y_raw = np.asarray(item[0], dtype=float)
            x_raw = np.asarray(item[1], dtype=float)

            self.add_line(
                fig,
                x=x_raw,
                y=y_raw,
                row=row,
                col=col,
                color_index=6,
                line_style_index=0,
                name="Data" if show_data_legend else None,
                showlegend=show_data_legend,
            )
            if show_data_legend:
                show_data_legend = False

            if q_idx < len(fit_data_list):
                y_fit = np.asarray(fit_data_list[q_idx], dtype=float)
                if q_idx < len(x_out_list) and len(x_out_list[q_idx]) == len(y_fit):
                    x_fit = np.asarray(x_out_list[q_idx], dtype=float)
                elif len(y_fit) == len(x_raw):
                    x_fit = x_raw
                else:
                    x_fit = np.linspace(x_raw.min(), x_raw.max(), len(y_fit))
                self.add_line(
                    fig,
                    x=x_fit,
                    y=y_fit,
                    row=row,
                    col=col,
                    color_index=0,
                    line_style_index=0,
                    name="Fit" if show_fit_legend else None,
                    showlegend=show_fit_legend,
                )
                if show_fit_legend:
                    show_fit_legend = False

            if q_idx < len(zd_xy_list):
                self.add_vline(
                    fig,
                    zd_xy_list[q_idx] * 1e-9,
                    row=row,
                    col=col,
                    color_index=1,
                    line_style_index=1,
                )
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0
                text = f"zd_xy={zd_xy_list[q_idx]:.3f} ns<br>R²={r2:.4f}"
                self.add_annotation(
                    fig,
                    text=text,
                    row=row,
                    col=col,
                    x=0,
                    y=1,
                    xref="x domain",
                    yref="y domain",
                    showarrow=False,
                )

            fig.update_xaxes(title_text="t", row=row, col=col)
            fig.update_yaxes(title_text="amp", row=row, col=col)

        self.update_layout(fig, rows=rows, cols=cols, showlegend=True)
        return fig
