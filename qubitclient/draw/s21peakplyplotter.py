from .plyplotter import QuantumDataPlyPlotter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
# import pandas as pd
class S21PeakDataPlyPlotter(QuantumDataPlyPlotter):

    def __init__(self):
        super().__init__("s21peak")

    # def plot_result_npy(self, **kwargs):
    #     result = kwargs.get('result')
    #     dict_param = kwargs.get('dict_param')
    #
    #     dict_param = dict_param.item()
    #
    #     image = dict_param["image"]
    #     q_list = list(image.keys())
    #     x_list = []
    #     amp_list = []
    #     phi_list = []
    #     q_name_list = []
    #
    #     for idx, q_name in enumerate(q_list):
    #         image_q = image[q_name]
    #         x = image_q[0]
    #         amp = image_q[1]
    #         phi = image_q[2]
    #         x_list.append(x)
    #         amp_list.append(amp)
    #         phi_list.append(phi)
    #         q_name_list.append(q_name)
    #
    #     peaks_list = result['peaks']
    #     confs_list = result['confs']
    #     freqs_list = result['freqs_list']
    #
    #     nums = len(x_list)
    #     rows = nums
    #     cols = 1
    #
    #     # 创建子图
    #     fig = make_subplots(
    #         rows=rows, cols=cols,
    #         subplot_titles=q_name_list,
    #         vertical_spacing=0.08,
    #         shared_xaxes=True
    #     )
    #
    #     for i in range(nums):
    #         x = x_list[i]
    #         y1 = amp_list[i]
    #         y2 = phi_list[i]
    #         peaks = peaks_list[i]
    #         confs = confs_list[i]
    #         freqs = freqs_list[i]
    #
    #         # 添加幅度曲线
    #         fig.add_trace(
    #             go.Scatter(
    #                 x=x, y=y1,
    #                 mode='lines',
    #                 name=f'{q_name_list[i]} - Amp',
    #                 line=dict(color='blue', width=3),
    #                 legendgroup=f'group_{i}',
    #                 showlegend=True
    #             ),
    #             row=i + 1, col=1
    #         )
    #
    #         # 添加相位曲线（使用次坐标轴）
    #         fig.add_trace(
    #             go.Scatter(
    #                 x=x, y=y2,
    #                 mode='lines',
    #                 name=f'{q_name_list[i]} - Phi',
    #                 line=dict(color='green', width=2),
    #                 legendgroup=f'group_{i}',
    #                 showlegend=True,
    #                 yaxis=f'y{i * 2 + 2}'
    #             ),
    #             row=i + 1, col=1
    #         )
    #
    #         # 使用plotly express为峰值点创建彩色散点图
    #         if len(peaks) > 0:
    #             # 准备峰值点数据
    #             peak_x = [x[p] for p in peaks]
    #             peak_y = [y1[p] for p in peaks]
    #             peak_confs = [confs[j] for j in range(len(peaks))]
    #             peak_freqs = [freqs[j] for j in range(len(peaks))]
    #             peak_ids = [f'Peak_{j + 1}' for j in range(len(peaks))]
    #
    #             # 创建数据框
    #             import pandas as pd
    #             peak_df = pd.DataFrame({
    #                 'Frequency': peak_x,
    #                 'Amplitude': peak_y,
    #                 'Confidence': peak_confs,
    #                 'Peak_Frequency': peak_freqs,
    #                 'Peak_ID': peak_ids
    #             })
    #
    #             # 使用plotly express创建彩色散点图
    #             peak_scatter = px.scatter(
    #                 peak_df,
    #                 x='Frequency',
    #                 y='Amplitude',
    #                 color='Peak_ID',
    #                 size='Confidence',
    #                 hover_data=['Confidence', 'Peak_Frequency'],
    #                 color_discrete_sequence=px.colors.qualitative.Set3
    #             )
    #
    #             # 将px图形转换为go图形并添加到子图中
    #             index=0
    #             for trace in peak_scatter.data:
    #                 trace.update(
    #                     marker=dict(
    #                         symbol='star',
    #                         size=15,
    #                         line=dict(width=2, color='darkred')
    #                     ),
    #                     text=[f'Conf: {conf:.3f}' for conf in peak_confs],
    #                     showlegend=True,
    #                     legendgroup=f'group_{i}',
    #                     name=f'freq: {freqs[index] / 1e9:.2f}GHz'
    #                 )
    #                 index+=1
    #                 fig.add_trace(trace, row=i + 1, col=1)
    #
    #         fig.update_layout(
    #             height=500 * rows,
    #             width=1800 * cols,
    #             margin=dict(r=60, t=60, b=60, l=60),
    #             showlegend=True
    #         )
    #
    #
    #     return fig
    def plot_result_npy(self, **kwargs):

        result_param = kwargs.get('result')
        dict_param = kwargs.get('dict_param')
        dict_param = dict_param.item()

        image = dict_param["image"]
        q_list = image.keys()
        x_list = []
        amp_list = []
        phi_list = []
        qname_list=[]
        for idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            x = image_q[0]
            amp = image_q[1]
            phi = image_q[2]
            x_list.append((x))
            amp_list.append((amp))
            phi_list.append((phi))
            qname_list.append(q_name)




        peaks_list = result_param['peaks']
        confs_list = result_param['confs']
        freqs_list = result_param['freqs_list']

        nums = len(x_list)
        row = (nums // 1) + 1 if nums % 1 != 0 else nums // 1
        col = 1

        fig = make_subplots(
            rows=row, cols=col,
            subplot_titles=qname_list,
            vertical_spacing=0.015,
            horizontal_spacing=0.1
            # x_title="Bias",
            # y_title="Frequency (GHz)"
        )

        for i in range(len(x_list)):
            x = x_list[i]
            y1 = amp_list[i]
            y2 = phi_list[i]
            peaks = peaks_list[i]
            confs = confs_list[i]
            freqs = freqs_list[i]

            current_row = i // col + 1
            current_col = i % col + 1

            # 添加幅度曲线
            fig.add_trace(
                go.Scatter(x=x, y=y1, mode='lines',
                           name=f'{qname_list[i]}:  Amp Curve',legendgroup=f"group_{i}",showlegend=True, line=dict(color='blue', width=2)),
                row=current_row, col=current_col
            )

            # 添加相位曲线
            fig.add_trace(
                go.Scatter(x=x, y=y2, mode='lines',
                           name=f'{qname_list[i]}: Phi Curve',legendgroup=f"group_{i}",showlegend=True, line=dict(color='green')),
                row=current_row, col=current_col
            )
            color_palette = [
                '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF',  # 红、绿、蓝、黄、紫
                '#00FFFF', '#FFA500', '#800080', '#008000', '#FFC0CB',  # 青、橙、紫红、深绿、粉红
                '#4B0082', '#FF4500', '#2E8B57', '#DA70D6', '#1E90FF',  # 靛蓝、橙红、海绿、兰紫、道奇蓝
                '#32CD32', '#8A2BE2', '#DC143C', '#00CED1', '#FFD700',  # 酸橙、紫罗兰、深红、深青、金色
                '#006400', '#8B4513'  # 深绿、鞍褐
            ]
            # 添加峰值点
            for j in range(len(peaks)):
                peak_x = x[peaks[j]]
                peak_y = y1[peaks[j]]
                conf = confs[j]
                freq = freqs[j]
                fig.add_trace(
                    go.Scatter(x=[peak_x], y=[peak_y], mode='markers',
                               marker=dict(symbol='star', size=12, color=color_palette[j%len(color_palette)]),
                               name=f'freq: {freq / 1e9:.2f}GHz',legendgroup=f"group_{i}",showlegend=True),
                               row=current_row, col=current_col
                               )

                # 添加峰值标注
                fig.add_annotation(
                    x=peak_x, y=peak_y,
                    text=f'{conf:.2f}',
                    showarrow=False,
                    ax=0, ay=-30,
                    font=dict(size=30, color='darkred'),
                    row=current_row, col=current_col
                )

                # 添加垂直线
                fig.add_vline(
                    x=peak_x, line_dash="dash",
                    line_color=color_palette[j%len(color_palette)], opacity=0.8,
                    row=current_row, col=current_col
                )

                # 更新布局配置
                fig.update_layout(
                    height=500 * row,
                    width=1800 * col,
                    margin=dict(r=60, t=60, b=60, l=60),
                    showlegend=True,
                    legend = dict(
                        x=1.05,  # 将图例放在图表右侧外部
                        y=0.5,
                        xanchor='left',
                        yanchor='middle',groupclick="toggleitem")
                )
                fig.update_xaxes(tickformat='.2e')
                # fig.update_xaxes(
                #     title_text="Bias",
                #     title_font=dict(size=10),  # 缩小字体
                #     title_standoff=8  # 增加标题与坐标轴的距离（单位：像素）
                # )
                # fig.update_yaxes(
                #     title_text="Frequency (GHz)",
                #     title_font=dict(size=10),
                #     title_standoff=8
                # )
        return fig