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

class OptReadFreqDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("optreadfreq")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())

        fig, axes, rows, cols = self.create_subplots(len(qubit_names))
        axs = axes.flatten()

        peak_list   = result.get("peak_list",   [])


        for q_idx, q_name in enumerate(qubit_names):
            ax = axs[q_idx]
            item = image_dict.get(q_name)

            freq = np.asarray(item[0])
            s0 = np.asarray(item[1])
            s1 = np.asarray(item[2])
            dis = np.abs(s0-s1)
            peak = peak_list[q_idx]
            self.add_line(
                ax,
                freq,
                dis,
                color_index=0,
                line_style_index=0
            )
            self.add_scatter(
                ax,
                freq,
                dis,
                color_index=0
            )
            if peak:
                self.add_vline(ax, freq[peak])

                self.add_annotation(ax, f'freq:{freq[peak]:.2e}', (freq[peak], dis[peak]))

            # 坐标轴设置
            self.configure_axis(
                ax,
                title=q_name,
                xlabel="freq",
                ylabel="distance | 01"
            )

        fig.tight_layout()
        return fig