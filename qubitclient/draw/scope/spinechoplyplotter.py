# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.

from ..plyplotter import QuantumDataPlyPlotter
import numpy as np


class SpinEchoDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("spinecho")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get("result")
        dict_param = kwargs.get("dict_param")

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        fig, rows, cols = self.create_subplots(
            n_plots=len(qubit_names),
            titles=qubit_names,
            second_y=False,
        )

        fit_envelope_list = result.get("fit_envelope_list", [])
        r2_list = result.get("r2_list", [])
        t2_list = result.get("t2_list", [])
        x_out_list = result.get("x_out_list", [])

        show_raw_legend = True
        show_fit_legend = True

        for q_idx, q_name in enumerate(qubit_names):
            row = q_idx // cols + 1
            col = q_idx % cols + 1
            item = image_dict.get(q_name)
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            x_raw = np.asarray(item[0], dtype=float)
            y_raw = np.asarray(item[1], dtype=float)

            self.add_line(
                fig,
                x=x_raw,
                y=y_raw,
                row=row,
                col=col,
                color_index=0,
                line_style_index=0,
                name="raw" if show_raw_legend else None,
                showlegend=show_raw_legend,
            )
            if show_raw_legend:
                show_raw_legend = False

            if q_idx < len(fit_envelope_list):
                y_fit = np.asarray(fit_envelope_list[q_idx], dtype=float)
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
                    color_index=1,
                    line_style_index=1,
                    name="fit" if show_fit_legend else None,
                    showlegend=show_fit_legend,
                )
                if show_fit_legend:
                    show_fit_legend = False

            if q_idx < len(t2_list):
                r2 = r2_list[q_idx] if q_idx < len(r2_list) else 0.0
                text = f"T₂ = {t2_list[q_idx]:.2f} µs<br>R² = {r2:.2f}"
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
