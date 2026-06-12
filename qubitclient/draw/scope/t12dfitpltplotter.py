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

class T12DFitDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("t1fit")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item() if isinstance(dict_param, np.ndarray) else dict_param
        image_dict = data.get("image", {})
        qubit_names = list(image_dict.keys())
        n_plots = len(qubit_names)

        fig, axes, rows, cols = self.create_subplots(n_plots)
        axs = axes.flatten()

        t1_list   = result.get("t1_list",   [])
        zpa_list       = result.get("zpa_list", [])
        pdata_list=[]
        delaydata_list=[]
        zpadata_list=[]

        for idx, q_name in enumerate(qubit_names):
            image_q = image_dict[q_name]
            delay = image_q[1]
            p = image_q[0]
            zpa = image_q[2]

            pdata_list.append(p)
            delaydata_list.append(delay)
            zpadata_list.append(zpa)

        for i in range(n_plots):
            ax = axs[i]
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



            c = self.add_2dmap(ax, zpadata, delaydata, pdata.T, shading_index=0, cmap_index=0)
            fig.colorbar(c, ax=ax)

            self.add_line(ax, zpa, t1_norm,color_index=3, alpha=0.5)
            self.add_scatter(ax, zpa, t1_norm, alpha=0.5)
            self.configure_axis(ax, title=f"{file_name}", xlabel="ZPA", ylabel="Delay")

        fig.tight_layout()
        return fig