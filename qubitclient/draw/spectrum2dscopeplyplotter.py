from .plyplotter import QuantumDataPlyPlotter
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Spectrum2DScopeDataPlyPlotter(QuantumDataPlyPlotter):

    def __init__(self):
        super().__init__("spectrum2dscope")


    def plot_result_npy(self, **kwargs):

        results = kwargs.get('result')
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
            volt = image_q[1]
            freq = image_q[2]
            s = np.abs(image_q[0])

            volt_list.append(volt)
            freq_list.append(freq)
            s_list.append(s)
            q_name_list.append(q_name)

        # 结果数据
        coslines_list = results['params']
        cosconfs_list = results['confs']
        coscompress_list = results['coscompress_list']
        lines_list = results['lines_list']
        lineconfs_list = results['lineconfs_list']

        # 计算子图布局
        nums = len(volt_list) * 2
        rows = (nums // 2) + 1 if nums % 2 != 0 else nums // 2
        cols = min(nums, 2)

        # 计算安全的垂直间距
        max_vertical_spacing = 1 / (rows - 1) if rows > 1 else 0.1
        safe_vertical_spacing = min(0.05, max_vertical_spacing - 0.01)

        # 创建子图布局
        fig = make_subplots(
            rows=rows,
            cols=cols,
            vertical_spacing=0.01,
            horizontal_spacing=0.1,
            subplot_titles=[f"{q_name_list[ii // 2]}_Heatmap" if ii % 2 == 0
                            else f"{q_name_list[ii // 2]}_WithCurves" for ii in range(nums)]
        )

        # 遍历所有子图位置
        for ii in range(nums):
            row_pos = (ii // cols) + 1
            col_pos = (ii % cols) + 1

            volt = volt_list[ii // 2]
            freq = freq_list[ii // 2]
            s = s_list[ii // 2]
            coslines = coslines_list[ii // 2]
            cosconfs = cosconfs_list[ii // 2]
            coscompress = coscompress_list[ii // 2]
            lines = lines_list[ii // 2]
            lineconfs = lineconfs_list[ii // 2]

            # 热力图数据
            heatmap_trace = go.Heatmap(
                x=volt,
                y=freq,
                z=s,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='Intensity'),
                hovertemplate=(
                        'Volt: %{x}<br>' +
                        'Freq: %{y}<br>' +
                        'Intensity: %{z}<extra></extra>'
                )
            )

            fig.add_trace(heatmap_trace, row=row_pos, col=col_pos)

            # 在奇数编号的子图中添加曲线和线条
            if (ii % 2 != 0):
                # 添加直线
                if lines:
                    for j, line in enumerate(lines):
                        if line:
                            final_x_line = [item[0] for item in line]
                            final_line_pred = [item[1] for item in line]

                            line_trace = go.Scatter(
                                x=final_x_line,
                                y=final_line_pred,
                                mode='lines',
                                line=dict(color='red', width=3),
                                name=f'Line {j + 1}',
                                showlegend=False,
                                hovertemplate=(
                                        'Volt: %{x}<br>' +
                                        'Freq: %{y}<br>' +
                                        f'Confidence: {lineconfs[j]:.2f}<extra></extra>'
                                )
                            )
                            fig.add_trace(line_trace, row=row_pos, col=col_pos)

                            # 添加置信度文本
                            mid_idx = len(volt) // 2
                            if mid_idx < len(volt):
                                fig.add_annotation(
                                    x=volt[mid_idx],
                                    y=freq[mid_idx],
                                    text=f"conf: {lineconfs[j]:.2f}",
                                    showarrow=False,
                                    font=dict(color='red', size=12),
                                    bgcolor='rgba(255,255,255,0.8)',
                                    row=row_pos,
                                    col=col_pos
                                )

                # 添加余弦曲线
                if coslines:
                    for j, cosline in enumerate(coslines):
                        if cosline:
                            final_x_cos = [item[0] for item in cosline]
                            final_cos_pred = [item[1] for item in cosline]

                            cos_trace = go.Scatter(
                                x=final_x_cos,
                                y=final_cos_pred,
                                mode='lines',
                                line=dict(color='red', width=3),
                                name=f'Cosine {j + 1}',
                                showlegend=False,
                                hovertemplate=(
                                        'Volt: %{x}<br>' +
                                        'Freq: %{y}<br>' +
                                        f'Confidence: {cosconfs[j]:.2f}<br>' +
                                        f'Compress: {coscompress[j]:.2f}<extra></extra>'
                                )
                            )
                            fig.add_trace(cos_trace, row=row_pos, col=col_pos)

                            # 添加置信度和压缩比文本
                            mid_idx = len(volt) // 2
                            if mid_idx < len(volt):
                                fig.add_annotation(
                                    x=volt[mid_idx],
                                    y=freq[mid_idx],
                                    text=f"conf: {cosconfs[j]:.2f}<br>compress: {coscompress[j]:.2f}",
                                    showarrow=False,
                                    font=dict(color='red', size=12),
                                    bgcolor='rgba(255,255,255,0.8)',
                                    row=row_pos,
                                    col=col_pos
                                )


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