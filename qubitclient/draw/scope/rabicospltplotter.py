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


class RabiCosDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("rabicos")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        fig, axes, n_rows, n_cols = self.create_subplots(len(qubit_names))
        axs = axes.flatten()

        peaks_list = result.get("peaks", [])
        confs_list = result.get("confs", [])

        for q_idx, q_name in enumerate(qubit_names):
            ax = axs[q_idx]
            item = image_dict[q_name]
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                ax.axis('off')
                continue

            x = np.asarray(item[0])     
            y = np.asarray(item[1])

            signal_line, _ = self.add_line(
                ax, x, y,
                label='Signal',
                color_index=0,
                line_style_index=0
            )

            legend_handles = [signal_line[0]]
            legend_labels = ['Signal']

            has_peak = False
            if q_idx < len(peaks_list) and peaks_list[q_idx]:
                has_peak = True
                peaks = peaks_list[q_idx]
                confs = confs_list[q_idx] if q_idx < len(confs_list) else [0.0] * len(peaks)

                for p, c in zip(peaks, confs):
                    idx = np.argmin(np.abs(x - p))
                    px = x[idx]
                    py = y[idx]

                    self.add_vline(ax, px)

                    if not has_peak:  
                        continue
                    scatter = self.add_scatter(
                        ax, [px], [py],
                        color_index=0,
                        marker_index=1
                    )

                    if len(legend_handles) == 1: 
                        legend_handles.append(scatter)
                        legend_labels.append('Peak')

                    annot_text = f"x = {px:.3f}\nconf = {c:.3f}"
                    self.add_annotation(
                        ax,
                        annot_text,
                        xy=(px, py),
                        annotation_xytext=(10, 10),
                        color_index=0
                    )

            if legend_handles:
                self.add_legend(
                    ax=ax,
                    handles=legend_handles,
                    labels=legend_labels,
                )

            xlabel = "Time"
            ylabel = "Amp"
            self.configure_axis(ax, title=q_name, xlabel=xlabel, ylabel=ylabel)

        fig.tight_layout()
        return fig