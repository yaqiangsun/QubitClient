# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:03
########################################################################

from ..plyplotter import QuantumDataPlyPlotter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


class RamseyDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("ramsey")

    def plot_result_npy(self, **kwargs):
        result     = kwargs.get('result')
        dict_param = kwargs.get('dict_param')


        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        fig, rows, cols = self.create_subplots(
            n_plots=len(qubit_names),
            titles=qubit_names,
            second_y=False
        )



        params_list   = result.get("params_list", [])
        r2_list       = result.get("r2_list", [])
        fit_data_list = result.get("fit_data_list", [])

        show_data_legend = True
        show_fit_legend = True

        for q_idx, q_name in enumerate(qubit_names):
            row = q_idx // cols + 1
            col = q_idx % cols + 1

            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            x_raw = np.asarray(item[0])
            y_raw = np.asarray(item[1])


            self.add_scatter(
                fig, x=x_raw, y=y_raw,
                row=row, col=col,
                color_index=6,  # 橙色
                marker_index=0,  # circle
                name="Data" if show_data_legend else None,
                showlegend=show_data_legend,
                opacity=0.7
            )

            if show_data_legend:
                show_data_legend = False

            if q_idx < len(fit_data_list):
                y_fit = np.asarray(fit_data_list[q_idx])
                x_fit = x_raw if len(y_fit) == len(x_raw) else np.linspace(x_raw.min(), x_raw.max(), len(y_fit))

                self.add_line(
                    fig, x=x_fit, y=y_fit,
                    row=row, col=col,
                    color_index=0,
                    line_style_index=0,
                    name="Fit" if show_fit_legend else None,
                    showlegend=show_fit_legend
                )
                if show_fit_legend:
                    show_fit_legend = False
            if q_idx < len(params_list):
                A, B, freq, phi, T2 = params_list[q_idx]
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0
                txt = f"A={A:.3f}<br>B={B:.3f}<br>freq={freq/1e6:.3f}MHz<br>φ={phi:.3f}<br>T2={T2:.1f}µs<br>R²={r2:.4f}"

                self.add_annotation(fig, x=0, y=1, xref="x domain", yref="y domain", showarrow=False,
                                    text=txt, row=row,
                                    col=col)

            fig.update_xaxes(title_text="Time (ns)", row=row, col=col)
            fig.update_yaxes(title_text="P(|1>)", row=row, col=col)
        self.update_layout(
            fig,
            rows=rows,
            cols=cols,
            showlegend=True
        )
        return fig