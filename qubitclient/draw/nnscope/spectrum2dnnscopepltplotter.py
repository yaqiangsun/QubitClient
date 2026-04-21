# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:03
########################################################################


import numpy as np
from ..pltplotter import QuantumDataPltPlotter

class Spectrum2DNNScopeDataPltPlotter(QuantumDataPltPlotter):

    def __init__(self):
        super().__init__("spectrum2dnnscope")
    def plot_result_npy(self, **kwargs):
        results = kwargs.get('result')
        data_ndarray = kwargs.get('dict_param')







        data_dict = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
        data_dict = data_dict['image']
        dict_list = []
        q_list = data_dict.keys()

        for idx, q_name in enumerate(q_list):
            npz_dict = {}
            image_q = data_dict[q_name]
            data = image_q[0]
            if data.ndim != 2:
                raise ValueError("数据格式无效，data不是二维数组")
            data = np.array(data)
            data = np.abs(data)

            npz_dict['bias'] = image_q[1]
            npz_dict['frequency'] = image_q[2]
            npz_dict['iq_avg'] = data
            npz_dict['name'] = q_name
            dict_list.append(npz_dict)
        n_plots = len(q_list) * 2
        fig, axes, rows, cols = self.create_subplots(n_plots)
        axs = axes.flatten()

        linepoints_list = results['linepoints_list']
        class_ids = results['class_ids_list']
        confidences_list = results['confidences_list']
        for index in range(n_plots):
            ax = axs[index]

            points_list =  linepoints_list[index // 2]




            c = self.add_2dmap(ax, dict_list[index//2]["bias"], dict_list[index//2]["frequency"], dict_list[index//2]["iq_avg"], shading_index=0, cmap_index=0)

            fig.colorbar(c, ax=ax)



            if (index % 2 != 0):
                for i in range(len(points_list)):
                    reflection_points = points_list[i]
                    reflection_points = np.array(reflection_points)
                    xy_x = reflection_points[:, 0]
                    xy_y = reflection_points[:, 1]
                    centcol = len(xy_x) // 2

                    self.add_line(ax,xy_x, xy_y,color_index=i,line_style_index=0)
                    self.add_annotation(ax,f'conf:{round(confidences_list[index // 2][i], 2)}',(xy_x[centcol], xy_y[centcol]))




            file_name = dict_list[index//2]["name"]

            self.configure_axis(ax,title=f"{file_name}",xlabel="Bias",ylabel="Frequency (GHz)")
            handle, labels = ax.get_legend_handles_labels()
            self.add_legend(ax, handle, labels)
        fig.tight_layout()
        return fig

    def plot_result_npz(self, **kwargs):
        results = kwargs.get('results')
        dict_list = kwargs.get('dict_list')
        file_names = kwargs.get('file_names')

        linepoints_list = results['linepoints_list']
        class_ids = results['class_ids_list']
        confidences_list = results['confidences_list']
        n_plots = len(linepoints_list) * 2
        fig, axes, row, col = self.create_subplots(n_plots)
        axs = axes.flatten()


        for index in range(n_plots):
            ax = axs[index]
            file_name = file_names[index//2]

            points_list = linepoints_list[index // 2]

            c = self.add_2dmap(ax, dict_list[index // 2]["bias"], dict_list[index // 2]["frequency"],
                               dict_list[index // 2]["iq_avg"], shading_index=0, cmap_index=0)

            fig.colorbar(c, ax=ax)


            if(index%2!=0):
                for i in range(len(points_list)):
                    reflection_points = points_list[i]
                    reflection_points = np.array(reflection_points)
                    xy_x = reflection_points[:, 0]
                    xy_y = reflection_points[:, 1]
                    centcol = len(xy_x) // 2

                    self.add_line(ax, xy_x, xy_y, color_index=i, line_style_index=0)
                    self.add_annotation(ax, f'conf:{round(confidences_list[index // 2][i], 2)}',
                                        (xy_x[centcol], xy_y[centcol]))


            self.configure_axis(ax, title=f"{file_name}", xlabel="Bias", ylabel="Frequency (GHz)")
            handle, labels = ax.get_legend_handles_labels()
            self.add_legend(ax, handle, labels)
        fig.tight_layout()
        return fig
