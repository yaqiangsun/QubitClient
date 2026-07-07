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
        image_qubits = list(image_dict.keys())
        qubit_names = [
            q for q in image_qubits
            if isinstance(result, dict)
            and isinstance(result.get(q), dict)
            and len(result[q].get("x", [])) > 0
            and len(result[q].get("amp", [])) > 0
        ]
        if not qubit_names and isinstance(result, dict):
            qubit_names = [
                k for k, v in result.items()
                if k != "status" and isinstance(v, dict)
                and len(v.get("x", [])) > 0 and len(v.get("amp", [])) > 0
            ]

        n_qubits = len(qubit_names)
        titles = [f"Timing_xyz {q_name}" for q_name in qubit_names]

        fig, rows, cols = self.create_subplots(
            n_plots=n_qubits,
            titles=titles,
            second_y=False,
        )

        show_data_legend = True
        show_fit_legend = True

        for q_idx, q_name in enumerate(qubit_names):
            row = q_idx // cols + 1
            col = q_idx % cols + 1

            item = result.get(q_name)
            x = np.asarray(item.get("x", []), dtype=float)
            amp = np.asarray(item.get("amp", []), dtype=float)
            fit_data = item.get("fit_data")
            zd_xy = item.get("zd_xy")
            r2 = item.get("r2", 0.0)

            self.add_line(
                fig,
                x=x,
                y=amp,
                row=row,
                col=col,
                color_index=6,
                line_style_index=0,
                name="Data" if show_data_legend else None,
                showlegend=show_data_legend,
            )
            if show_data_legend:
                show_data_legend = False

            if fit_data is not None and len(fit_data) > 0:
                self.add_line(
                    fig,
                    x=x,
                    y=np.asarray(fit_data, dtype=float),
                    row=row,
                    col=col,
                    color_index=0,
                    line_style_index=0,
                    name="Fit" if show_fit_legend else None,
                    showlegend=show_fit_legend,
                )
                if show_fit_legend:
                    show_fit_legend = False

            if zd_xy is not None:
                self.add_vline(
                    fig,
                    zd_xy * 1e-9,
                    row=row,
                    col=col,
                    color_index=1,
                    line_style_index=1,
                )
                text = f"zd_xy={zd_xy:.3f} ns<br>R²={r2:.4f}"
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

            fig.update_xaxes(title_text="Time(s)", row=row, col=col)
            fig.update_yaxes(title_text="amp", row=row, col=col)

        self.update_layout(fig, rows=rows, cols=cols, showlegend=True)
        return fig