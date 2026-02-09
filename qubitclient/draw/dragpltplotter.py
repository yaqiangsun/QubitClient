import numpy as np
import matplotlib.pyplot as plt
from .pltplotter import QuantumDataPltPlotter


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
            x = image_q[2]
            y0 = image_q[3][0]
            y1 = image_q[3][1]
            x_list.append((x))
            y0_list.append(y0)
            y1_list.append(y1)
            qname_list.append(q_name)


        x_pred_list = result_param['x_pred_list']
        y0_pred_list = result_param['y0_pred_list']
        y1_pred_list = result_param['y1_pred_list']
        intersections_list = result_param['intersections_list']

        intersections_confs_list = result_param['intersections_confs_list']

        nums = len(x_list)
        col = 3
        row = (nums // col) + (1 if nums % col != 0 else 0)

        fig, axes = plt.subplots(row, col, figsize=(20, 10 * row))

        axes = axes.flatten()  # Flatten in case of multiple rows

        for ii in range(nums):
            ax = axes[ii]

            x = x_list[ii]
            y0 = y0_list[ii]
            y1 = y1_list[ii]
            x_pred = x_pred_list[ii]
            y0_pred = y0_pred_list[ii]
            y1_pred = y1_pred_list[ii]
            intersections = intersections_list[ii]
            intersections_confs = intersections_confs_list[ii]

            ax.plot(x, y0, color='green', label='Data', linestyle='-', marker='o', markersize=4,
                    alpha=0.7)
            ax.plot(x, y1, color='blue', label='Data', linestyle='-', marker='o', markersize=4,
                    alpha=0.7)

            ax.plot(x_pred, y0_pred, color='red', label='Data', linestyle='-', marker='o', markersize=4, alpha=0.7)
            ax.plot(x_pred, y1_pred, color='red', label='Data', linestyle='-', marker='o', markersize=4, alpha=0.7)
            if intersections:
                intersection_x = [point[0] for point in intersections]
                intersection_y = [point[1] for point in intersections]
                ax.scatter(intersection_x, intersection_y, color='green', s=100, zorder=5,
                           marker='o', edgecolors='black', linewidth=1,
                           label=f'Intersections ({len(intersections)} points)')

                for i, (x_int, y_int) in enumerate(intersections):
                    ax.annotate(f'({x_int:.2f}, {y_int:.2f}),conf:{intersections_confs[i]:.2f}',
                                (x_int, y_int),
                                xytext=(10, 10),
                                textcoords='offset points',
                                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for jj in range(nums, len(axes)):
            fig.delaxes(axes[jj])

        fig.tight_layout()
        return fig


