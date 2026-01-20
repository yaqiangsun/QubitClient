from .plyplotter import QuantumDataPlyPlotter
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from scipy.stats import norm

class S21VfluxNNScopeDataPlyPlotter(QuantumDataPlyPlotter):

    def __init__(self):
        super().__init__("s21vfluxnnscope")

    def plot_result_npy(self, **kwargs):
        s21vflux_labels = {0:"cos_light",1:"cos_dark",2:"line_light",3:"line_dark"}
        results = kwargs.get('results')
        data_ndarray = kwargs.get('data_ndarray')

        nums = len(results) * 2
        row = (nums // 2) + 1 if nums % 2 != 0 else nums // 2
        col = min(nums, 2)

        fig = make_subplots(
            rows=row,
            cols=col,
            subplot_titles=[f"File: {list(data_ndarray.item()['image'].keys())[i // 2]}" for i in range(nums)],
            horizontal_spacing=0.1,
            vertical_spacing=0.01
        )

        data_dict = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
        data_dict = data_dict['image']
        dict_list = []
        q_list = data_dict.keys()

        for idx, q_name in enumerate(q_list):
            npz_dict = {}
            image_q = data_dict[q_name]
            data = image_q[2]
            if data.ndim != 2:
                raise ValueError("数据格式无效，data不是二维数组")
            data = np.array(data)
            data = np.abs(data)

            npz_dict['bias'] = image_q[1]
            npz_dict['frequency'] = image_q[0]
            npz_dict['iq_avg'] = data
            npz_dict['name'] = q_name
            dict_list.append(npz_dict)

        for index in range(nums):
            result = results[index // 2]
            points_list = []
            for i in range(len(result["linepoints_list"])):
                points_list.append(result["linepoints_list"][i])

            bias = dict_list[index // 2]["bias"]
            frequency = dict_list[index // 2]["frequency"]
            iq_avg = dict_list[index // 2]["iq_avg"]

            heatmap = go.Heatmap(
                x=bias,
                y=frequency,
                z=np.flipud(iq_avg.T),
                colorscale='Viridis',
                colorbar=dict(title="IQ Average"),
                showscale=(index == 0)
            )
            fig.add_trace(heatmap, row=(index // col) + 1, col=(index % col) + 1)

            if (index % 2 != 0):
                colors = [f'hsl({i * 360 / len(points_list)}, 100%, 50%)' for i in range(len(points_list))]
                for i in range(len(points_list)):
                    reflection_points = np.array(points_list[i])
                    xy_x = reflection_points[:, 0]
                    xy_y = reflection_points[:, 1]
                    class_id = s21vflux_labels[int(result["class_ids"][i])]
                    scatter = go.Scatter(
                        x=xy_x,
                        y=xy_y,
                        mode='markers',
                        marker=dict(color=colors[i], size=5, opacity=0.6),
                        text=[f'{class_id}:{round(result["confidence_list"][i], 2)}'],
                        hoverinfo='text+name',  # 修改此处
                        name=f'{class_id}:{round(result["confidence_list"][i], 2)}',  # 添加name属性
                        # name=f'{class_id} Points{i}-conf:{round(result["confidence_list"][i], 2)}',
                        showlegend=(row == 1 and col == 1)
                    )
                    fig.add_trace(scatter, row=(index // col) + 1, col=(index % col) + 1)

            fig.update_xaxes(title_text="Bias", row=(index // col) + 1, col=(index % col) + 1)
            fig.update_yaxes(title_text="Frequency (GHz)", row=(index // col) + 1, col=(index % col) + 1)

        fig.update_layout(
            height=500 * row,
            width=900 * col,
            margin=dict(r=60, t=60, b=60, l=60),
            legend=dict(
                font=dict(family="Courier", size=12, color="black"),
                borderwidth=1
            )
        )
        return fig