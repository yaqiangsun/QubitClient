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

class OptReadFreqDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("optreadfreq")

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

        peak_list = result.get("peak_list", [])

        show_data_legend = True
        show_fit_legend  = True

        for q_idx, q_name in enumerate(qubit_names):
            row = (q_idx // cols) + 1
            col = (q_idx % cols) + 1

            item = image_dict.get(q_name)
            if not isinstance(item, (list, tuple)) or len(item) < 2:
                continue

            freq = np.asarray(item[0])
            s0 = np.asarray(item[1])
            s1 = np.asarray(item[2])
            dis = np.abs(s0 - s1)
            peak = peak_list[q_idx]


            if show_data_legend:
                show_data_legend = False


            self.add_line(
                fig, x=freq, y=dis,
                row=row, col=col,
                color_index=0,
                line_style_index=0,
                name="Fit" if show_fit_legend else None,
                showlegend=show_fit_legend
            )
            self.add_scatter(
                fig, x=freq, y=dis,
                row=row, col=col,
                color_index=0
            )

            self.add_scatter(fig,x=[freq[peak]],y=[dis[peak]],row=row, col=col,color_index=0,showlegend=True)
            self.add_annotation(fig, x=freq[peak],
                                y=dis[peak],
                                text=f'freq:{freq[peak]:.2e}', row=row,
                                col=col)


            x_coords = []
            y_coords = []
            ymin, ymax = np.min(dis), np.max(dis)

            x_coords.extend([freq[peak], freq[peak], None])
            y_coords.extend([ymin, ymax, None])

            self.add_line(fig,x=x_coords,
                y=y_coords,row=row, col=col,color_index=2,line_style_index=1,name="peak",showlegend=True)

            fig.update_xaxes(title_text="freq", row=row, col=col)
            fig.update_yaxes(title_text="distance | 01", row=row, col=col)

        self.update_layout(
            fig,
            rows=rows,
            cols=cols,
            showlegend=False
        )

        return fig