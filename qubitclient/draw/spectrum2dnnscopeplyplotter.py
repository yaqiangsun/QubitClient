from .plyplotter import QuantumDataPlyPlotter
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Spectrum2DNNScopeDataPlyPlotter(QuantumDataPlyPlotter):

    def __init__(self):
        super().__init__("spectrum2dnnscope")


    def plot_result_npy(self, **kwargs):

        results = kwargs.get('results')
        data_ndarray = kwargs.get('data_ndarray')

        # 参数验证
        if results is None:
            raise ValueError("缺少必需的 'results' 参数")
        if data_ndarray is None:
            raise ValueError("缺少必需的 'data_ndarray' 参数")
        nums = len(results)
        rows = (nums*2 // 2) + 1 if nums*2 % 2 != 0 else nums*2 // 2
        cols = min(nums*2, 2)

        # 处理数据字典
        data_dict = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
        data_dict = data_dict['image']
        data_dict = data_dict.item() if isinstance(data_dict, np.ndarray) else data_dict
        dict_list = []
        q_list = data_dict.keys()

        # 准备数据列表
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
        subplot_titles = []
        for i in range(nums):
            subplot_titles.append(f"File: {dict_list[i]['name']}")
            subplot_titles.append(f"File: {dict_list[i]['name']}")

        # 创建子图
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=subplot_titles,
            vertical_spacing=0.01,
            horizontal_spacing=0.1,
            x_title="Bias",
            y_title="Frequency (GHz)"
        )

        # 遍历每个结果绘制子图
        for index in range(nums*2):
            row = (index // cols) + 1
            col = (index % cols) + 1

            result = results[index//2]
            data = dict_list[index//2]

            # 准备点数据
            points_list = []
            for i in range(len(result["linepoints_list"])):
                points_list.append(np.array(result["linepoints_list"][i]))

            # 添加热力图
            heatmap = go.Heatmap(
                z=data["iq_avg"],
                x=data["bias"],
                y=data["frequency"],
                colorscale="Viridis",
                colorbar=dict(
                    title="IQ Average",
                    thickness=10,
                    len=0.7,
                    yanchor="middle",
                    y=0.5
                ),
                showscale=(index == 0)  # 只在第一个子图显示颜色条
            )
            fig.add_trace(heatmap, row=row, col=col)
            # 添加散点
            colors = np.linspace(0, 1, len(points_list))
            for i, points in enumerate(points_list):
                if len(points) == 0:
                    continue
                xy_x = points[:, 0]
                xy_y = points[:, 1]
                scatter = go.Scatter(
                    x=xy_x,
                    y=xy_y,
                    mode="markers",
                    marker=dict(
                        color=colors[i],
                        colorscale="Rainbow",
                        size=5,
                        opacity=0.1,
                        showscale=False
                    ),
                    name=f'XY Points{i}-conf:{round(result["confidence_list"][i], 2)}',
                    legendgroup=f"group{index//2}",
                    showlegend=(row == 1 and col == 1)  # 只在第一个子图显示图例
                )
                if(index%2!=0):
                    fig.add_trace(scatter, row=row, col=col)

        # 更新布局
        fig.update_layout(
            height=500 * rows,
            width=900 * cols,
            margin=dict(r=60, t=60, b=60, l=60),
            legend=dict(
                font=dict(family="Courier", size=12, color="black"),
                borderwidth=1
            )
        )

        # 更新坐标轴设置
        fig.update_xaxes(
            title_text="Bias",
            title_font=dict(size=10),  # 缩小字体
            title_standoff=8  # 增加标题与坐标轴的距离（单位：像素）
        )
        fig.update_yaxes(
            title_text="Frequency (GHz)",
            title_font=dict(size=10),
            title_standoff=8
        )
        return fig
        # 保存图片
    def plot_result_npz(self, **kwargs):

        results = kwargs.get('results')
        dict_list = kwargs.get('dict_list')
        file_names = kwargs.get('file_names')

        nums = len(results)*2
        rows = (nums // 2) + 1 if nums % 2 != 0 else nums // 2
        cols = min(nums, 2)
        subplot_titles = []
        for name in file_names:
            subplot_titles.append(f"File: {name}")
            subplot_titles.append(f"File: {name}")

        # 创建子图
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=subplot_titles,
            vertical_spacing=0.015,
            horizontal_spacing=0.1,
            x_title="Bias",
            y_title="Frequency (GHz)"
        )

        # 遍历每个结果绘制子图
        for index in range(nums):
            row = (index // cols) + 1
            col = (index % cols) + 1

            result = results[index//2]
            data = dict_list[index//2]

            # 准备点数据
            points_list = []
            for i in range(len(result["linepoints_list"])):
                points_list.append(np.array(result["linepoints_list"][i]))

            # 添加热力图
            heatmap = go.Heatmap(
                z=data["iq_avg"],
                x=data["bias"],
                y=data["frequency"],
                colorscale="Viridis",
                colorbar=dict(
                    title="IQ Average",
                    thickness=10,
                    len=0.7,
                    yanchor="middle",
                    y=0.5
                ),
                showscale=(index == 0)  # 只在第一个子图显示颜色条
            )
            fig.add_trace(heatmap, row=row, col=col)

            # 添加散点
            colors = np.linspace(0, 1, len(points_list))
            for i, points in enumerate(points_list):
                if len(points) == 0:
                    continue
                xy_x = points[:, 0]
                xy_y = points[:, 1]
                scatter = go.Scatter(
                    x=xy_x,
                    y=xy_y,
                    mode="markers",
                    marker=dict(
                        color=colors[i],
                        colorscale="Rainbow",
                        size=5,
                        opacity=0.1,
                        showscale=False
                    ),
                    name=f'XY Points{i}-conf:{round(result["confidence_list"][i], 2)}',
                    legendgroup=f"group{index//2}",
                    showlegend=(row == 1 and col == 1)  # 只在第一个子图显示图例
                )
                if (index % 2 != 0):
                    fig.add_trace(scatter, row=row, col=col)

        # 更新布局
        fig.update_layout(
            height=500 * rows,
            width=900 * cols,
            margin=dict(r=60, t=60, b=60, l=60),
            legend=dict(
                font=dict(family="Courier", size=12, color="black"),
                borderwidth=1
            )
        )

        # 更新坐标轴设置
        fig.update_xaxes(
            title_text="Bias",
            title_font=dict(size=10),  # 缩小字体
            title_standoff=8  # 增加标题与坐标轴的距离（单位：像素）
        )
        fig.update_yaxes(
            title_text="Frequency (GHz)",
            title_font=dict(size=10),
            title_standoff=8
        )

        return fig
        # 保存图片