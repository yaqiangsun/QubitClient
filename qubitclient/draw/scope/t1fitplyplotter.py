# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:03
########################################################################

from ..plyplotter import QuantumDataPlyPlotter
import numpy as np

class T1FitDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("t1fit")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        fig, rows, cols = self.create_subplots(
            n_plots=len(qubit_names),
            titles=qubit_names,
            second_y=False
        )

        params_list   = result.get("params_list",   [])
        r2_list       = result.get("r2_list",       [])
        fit_data_dense_list = result.get("fit_data_dense_list", [])
        x_dense_list  = result.get("x_dense_list",  [])

        show_data_legend = True
        show_fit_legend  = True

        for q_idx, q_name in enumerate(qubit_names):
            row = (q_idx // cols) + 1
            col = (q_idx % cols) + 1

            item = image_dict.get(q_name)
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            x_raw = np.asarray(item[0])
            y_raw = np.asarray(item[1])

            # 原始数据（散点）
            self.add_scatter(
                fig, x=x_raw, y=y_raw,
                row=row, col=col,
                color_index=6,               # 橙色
                marker_index=0,              # circle
                name="Data" if show_data_legend else None,
                showlegend=show_data_legend,
                opacity=0.7
            )
            if show_data_legend:
                show_data_legend = False

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
                    fig, x=x_dense, y=fit_y_dense,
                    row=row, col=col,
                    color_index=0,
                    line_style_index=0,
                    name="Fit" if show_fit_legend else None,
                    showlegend=show_fit_legend
                )
                if show_fit_legend:
                    show_fit_legend = False

            # 参数文本（左上角）
            if q_idx < len(params_list) and params_list[q_idx]:
                A, T1, B = params_list[q_idx]
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0

                text = (
                    f"A  = {A:.3f}<br>"
                    f"T₁ = {T1*1e6:.1f} µs<br>"
                    f"B  = {B:.3f}<br>"
                    f"R² = {r2:.3f}"
                )

                y_max = max(y_raw) if len(y_raw) > 0 else 1.0
                self.add_annotation(
                    fig,
                    text=text,
                    row=row, col=col,
                    x=min(x_raw) if len(x_raw) > 0 else 0.0,
                    y=y_max * 1.08,
                    xref="x", yref="y",
                    showarrow=False,
                    xanchor="left",
                    yanchor="top"
                )

            fig.update_xaxes(title_text="Time", row=row, col=col)
            fig.update_yaxes(title_text="Amp", row=row, col=col)

        self.update_layout(
            fig,
            rows=rows,
            cols=cols,
            showlegend=True
        )

        return fig