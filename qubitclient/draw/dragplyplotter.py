import numpy as np
import matplotlib.pyplot as plt
from .plyplotter import QuantumDataPlyPlotter
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class DragDataPlyPlotter(QuantumDataPlyPlotter):
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
        col = 2
        row = (nums // col) + (1 if nums % col != 0 else 0)

        fig = make_subplots(
            rows=row, cols=col,
            subplot_titles=[f"Dataset {i + 1}" for i in range(nums)],
            vertical_spacing=0.01,
            horizontal_spacing=0.01
        )

        for ii in range(nums):
            r = (ii // col) + 1
            c = (ii % col) + 1

            x = x_list[ii]
            y0 = y0_list[ii]
            y1 = y1_list[ii]
            x_pred = x_pred_list[ii]
            y0_pred = y0_pred_list[ii]
            y1_pred = y1_pred_list[ii]
            intersections = intersections_list[ii]
            intersections_confs = intersections_confs_list[ii]

            fig.add_trace(
                go.Scatter(
                    x=x, y=y0,
                    mode='markers',
                    marker=dict(color='green', size=6, opacity=0.7),
                    name=f'Data Y0 #{ii + 1}',
                    showlegend=False
                ),
                row=r, col=c
            )

            fig.add_trace(
                go.Scatter(
                    x=x, y=y1,
                    mode='markers',
                    marker=dict(color='blue', size=6, opacity=0.7),
                    name=f'Data Y1 #{ii + 1}',
                    showlegend=False
                ),
                row=r, col=c
            )

            fig.add_trace(
                go.Scatter(
                    x=x_pred, y=y0_pred,
                    mode='lines',
                    line=dict(color='red', width=2),
                    name=f'Fit Y0 #{ii + 1}',
                    showlegend=False
                ),
                row=r, col=c
            )

            fig.add_trace(
                go.Scatter(
                    x=x_pred, y=y1_pred,
                    mode='lines',
                    line=dict(color='orange', width=2),
                    name=f'Fit Y1 #{ii + 1}',
                    showlegend=False
                ),
                row=r, col=c
            )

            if intersections:
                intersection_x = [point[0] for point in intersections]
                intersection_y = [point[1] for point in intersections]

                fig.add_trace(
                    go.Scatter(
                        x=intersection_x, y=intersection_y,
                        mode='markers+text',
                        marker=dict(
                            color='purple',
                            size=12,
                            symbol='circle',
                            line=dict(color='black', width=2)
                        ),
                        name=f'Intersections #{ii + 1}',
                        showlegend=False,
                        text=[f'Conf: {conf:.2f}'
                              for (x_int, y_int), conf in zip(intersections, intersections_confs)],
                        textposition="top center",
                        textfont=dict(size=12, color='black'),
                        hovertemplate='%{text}<extra></extra>'
                    ),
                    row=r, col=c
                )

        fig.update_layout(
            height=300 * row,
            showlegend=False,
            hovermode='closest',
            font=dict(size=12)
        )

        for i in range(1, row + 1):
            for j in range(1, col + 1):
                fig.update_xaxes(title_text="X Values", row=i, col=j)
                fig.update_yaxes(title_text="Y Values", row=i, col=j)
        return fig