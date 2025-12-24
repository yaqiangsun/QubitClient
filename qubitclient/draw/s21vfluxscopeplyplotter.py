from .plyplotter import QuantumDataPlyPlotter
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from scipy.stats import norm

class S21VfluxScopeDataPlyPlotter(QuantumDataPlyPlotter):

    def __init__(self):
        super().__init__("s21vfluxscope")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item()
        image = data["image"]
        q_list = image.keys()

        # 数据提取
        volt_list = []
        freq_list = []
        s_list = []
        q_name_list = []

        for idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            volt = image_q[0]
            freq = image_q[1]
            s = image_q[2]

            volt_list.append(volt)
            freq_list.append(freq)
            s_list.append(s)
            q_name_list.append(q_name)

        # 结果数据
        coscurves_list = result['coscurves_list']
        cosconfs_list = result['cosconfs_list']
        lines_list = result['lines_list']
        lineconfs_list = result['lineconfs_list']

        # 计算子图布局
        nums = len(volt_list) * 2
        rows = (nums // 2) + 1 if nums % 2 != 0 else nums // 2
        cols = 2

        # 创建子图布局
        fig = make_subplots(
            rows=rows,
            cols=cols,
            shared_xaxes=True,  # 共享X轴以增强交互一致性
            shared_yaxes=True,
            subplot_titles=[f"{q_name_list[i // 2]}_Heatmap" if i % 2 == 0
                            else f"{q_name_list[i // 2]}_WithCurves" for i in range(nums)],
            horizontal_spacing=0.1,
            vertical_spacing=0.01
        )

        # 遍历所有子图位置
        for ii in range(nums):
            row_pos = (ii // cols) + 1
            col_pos = (ii % cols) + 1

            volt = volt_list[ii // 2]
            freq = freq_list[ii // 2]
            s = s_list[ii // 2]
            q_name = q_name_list[ii // 2]

            # 热力图数据
            heatmap_trace = go.Heatmap(
                x=freq,
                y=volt,
                z=s.T,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='Intensity')
            )

            fig.add_trace(heatmap_trace, row=row_pos, col=col_pos)

            # 在奇数编号的子图中添加曲线和线条
            if (ii % 2 != 0):
                centcol = len(freq) // 2

                # 添加余弦曲线
                for j, curve in enumerate(coscurves_list[ii // 2]):
                    if curve:  # 确保曲线数据不为空
                        final_x_cos = [item[0] for item in curve]
                        final_y_cos = [item[1] for item in curve]

                        # 余弦曲线轨迹
                        cos_trace = go.Scatter(
                            x=final_x_cos,
                            y=final_y_cos,
                            mode='lines',
                            line=dict(color='red', width=2),
                            name=f'Cosine Curve {j + 1}'
                        )
                        fig.add_trace(cos_trace, row=row_pos, col=col_pos)

                        # 添加置信度文本
                        if centcol < len(final_x_cos):
                            fig.add_annotation(
                                x=final_x_cos[centcol],
                                y=final_y_cos[centcol],
                                text=f"conf:{cosconfs_list[ii // 2][j]:.2f}",
                                showarrow=False,
                                font=dict(color='red', size=12),
                                row=row_pos,
                                col=col_pos
                            )

                # 添加直线
                if lines_list[ii // 2]:
                    for j, line in enumerate(lines_list[ii // 2]):
                        if line:  # 确保直线数据不为空
                            final_x_line = [item[0] for item in line]
                            final_y_line = [item[1] for item in line]

                            line_trace = go.Scatter(
                                x=final_x_line,
                                y=final_y_line,
                                mode='lines',
                                line=dict(color='blue', width=2),
                                name=f'Line {j + 1}'
                            )
                            fig.add_trace(line_trace, row=row_pos, col=col_pos)
                            if centcol < len(final_x_line):
                                fig.add_annotation(
                                    x=final_x_line[centcol],
                                    y=final_y_line[centcol],
                                    text=f"conf:{lineconfs_list[ii // 2][j]:.2f}",
                                    showarrow=False,
                                    font=dict(color='red', size=12),
                                    row=row_pos,
                                    col=col_pos
                                )
        # 更新布局设置
        fig.update_layout(
            height=500 * rows,
            width=900 * cols,
            margin=dict(r=60, t=60, b=60, l=60),
            legend=dict(
                font=dict(family="Courier", size=12, color="black"),
                borderwidth=1
            )
        )

        # 更新坐标轴标签
        fig.update_xaxes(title_text="频率", row=rows, col=1)
        fig.update_yaxes(title_text="电压", col=1)

        # 隐藏未使用的子图
        for ii in range(nums, rows * cols):
            row_pos = (ii // cols) + 1
            col_pos = (ii % cols) + 1
            fig.update_xaxes(visible=False, row=row_pos, col=col_pos)
            fig.update_yaxes(visible=False, row=row_pos, col=col_pos)

        return fig

