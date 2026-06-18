# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.

from ..pltplotter import QuantumDataPltPlotter
import numpy as np


class SpinEchoDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("spinecho")

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
        fig, axes, rows, cols = self.create_subplots(n_qubits)
        axs = axes.flatten()

        for q_idx, q_name in enumerate(qubit_names):
            ax = axs[q_idx]
            item = result.get(q_name)

            x = np.asarray(item.get("x", []), dtype=float)
            amp = np.asarray(item.get("amp", []), dtype=float)
            fit_envelope = item.get("fit_envelope")
            t2_us = item.get("T2")
            r2 = item.get("r2", 0.0)

            self.add_line(
                ax,
                x,
                amp,
                label="raw",
                color_index=0,
                line_style_index=0,
                marker="o",
                markersize=3,
                alpha=0.8,
            )

            if fit_envelope is not None and len(fit_envelope) > 0:
                self.add_line(
                    ax,
                    x,
                    np.asarray(fit_envelope, dtype=float),
                    label="fit",
                    color_index=1,
                    line_style_index=1,
                )

            handles, labels = ax.get_legend_handles_labels()
            if handles:
                self.add_legend(ax=ax, handles=handles, labels=labels)

            if t2_us is not None:
                text = rf"$T_2 = {t2_us:.2f}\,\mu s$" + "\n" + rf"$R^2 = {r2:.2f}$"
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

            self.configure_axis(
                ax,
                title=q_name,
                xlabel="t",
                ylabel="amp",
            )

        fig.tight_layout()
        return fig
