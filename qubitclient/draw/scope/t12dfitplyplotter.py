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

class T12DFitDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("t1fit")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())
        n_plots = len(qubit_names)
        titles = [f"{qubit_names[i // 2]}" for i in range(n_plots)]
        fig, rows, cols = self.create_subplots(
            n_plots=n_plots,
            titles=titles,
            second_y=False
        )
        t1_list = result.get("t1_list", [])
        zpa_list = result.get("zpa_list", [])
        pdata_list = []
        delaydata_list = []
        zpadata_list = []

        for idx, q_name in enumerate(qubit_names):
            image_q = image_dict[q_name]
            delay = image_q[1]
            p = image_q[0]
            zpa = image_q[2]
            pdata_list.append(p)
            delaydata_list.append(delay)
            zpadata_list.append(zpa)

        for i in range(n_plots):
            row_pos = (i // cols) + 1
            col_pos = (i % cols) + 1
            file_name = qubit_names[i]
            t1 = t1_list[i]
            zpa = zpa_list[i]
            pdata = pdata_list[i]
            delaydata = delaydata_list[i]
            zpadata = zpadata_list[i]
            if isinstance(t1, list):
                t1 = np.array(t1)


            if t1.max() > t1.min():  # 避免除零
                t1_norm = delaydata.min() + (t1 - t1.min()) / (t1.max() - t1.min()) * (delaydata.max() - delaydata.min())
            else:
                t1_norm = np.full_like(t1, delaydata.mean())
            self.add_2dmap(fig, x=zpadata,
                           y=delaydata,
                           z=pdata.T, row=row_pos, col=col_pos, showscale=(i == 0))



            self.add_line(fig, x=zpa,
                          y=t1_norm, row=row_pos, col=col_pos,
                          color_index=3, line_style_index=0)
            self.add_scatter(fig, x=zpa,y=t1_norm, row=row_pos, col=col_pos)

        self.update_layout(fig, rows, cols)

        self.configure_axis(fig, rows, cols, xlable="ZPA", ylable="Delay")


        return fig