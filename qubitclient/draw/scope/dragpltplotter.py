# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:03
########################################################################

from ..pltplotter import QuantumDataPltPlotter
class DragDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("drag")
    def plot_result_npy(self,**kwargs):
        result_param = kwargs.get('result')
        dict_param = kwargs.get('dict_param')
        dict_param = dict_param.item()

        image = dict_param["image"]
        q_list = image.keys()
        x_list = []
        y0_list = []
        y1_list = []
        qname_list = []
        for idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            x = image_q[0]
            y0 = image_q[1][0]
            y1 = image_q[1][1]
            x_list.append((x))
            y0_list.append(y0)
            y1_list.append(y1)
            qname_list.append(q_name)
            # break


        x_pred_list = result_param['x_pred_list']
        y0_pred_list = result_param['y0_pred_list']
        y1_pred_list = result_param['y1_pred_list']
        intersections_list = result_param['intersections_list']

        intersections_confs_list = result_param['intersections_confs_list']



        n_plots = len(x_list)
        fig, axes, rows, cols = self.create_subplots(n_plots)
        axs = axes.flatten()



        for ii in range(n_plots):
            ax = axs[ii]

            x = x_list[ii]
            y0 = y0_list[ii]
            y1 = y1_list[ii]
            x_pred = x_pred_list[ii]
            y0_pred = y0_pred_list[ii]
            y1_pred = y1_pred_list[ii]
            intersections = intersections_list[ii]
            intersections_confs = intersections_confs_list[ii]


            self.add_line(ax,x, y0,color_index=0,line_style_index=0)
            self.add_line(ax,x, y1,color_index=1,line_style_index=0)
            self.add_line(ax, x_pred, y0_pred, color_index=2, line_style_index=0)
            self.add_line(ax, x_pred, y1_pred, color_index=2, line_style_index=0)

            if intersections:
                intersection_x = [point[0] for point in intersections]
                intersection_y = [point[1] for point in intersections]

                self.add_scatter(ax,intersection_x, intersection_y,color_index=0,marker_index=0)
                for i, (x_int, y_int) in enumerate(intersections):
                    self.add_annotation(ax,f'{intersections_confs[i]:.2f}',
                                (x_int, y_int),color_index=0)

            self.configure_axis(ax, title=qname_list[ii],
                                xlabel='x', ylabel='y')
        fig.tight_layout()
        return fig


