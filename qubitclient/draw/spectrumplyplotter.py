import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .plyplotter import QuantumDataPlyPlotter

class SpectrumDataPlyPlotter(QuantumDataPlyPlotter):

    def __init__(self):
        super().__init__("spectrum")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item()
        image = data["image"]
        q_list = list(image.keys())  # 确保q_list是列表形式，便于索引
        num_qubits = len(q_list)

        # 数据提取
        x_list = []
        amp_list = []
        q_name_list = []

        for q_name in q_list:
            image_q = image[q_name]
            x = image_q[0]  # 假设这里是x轴数据（如频率）
            amp = image_q[1]  # 假设这里是幅度数据
            
            x_list.append(x)
            amp_list.append(amp)
            q_name_list.append(q_name)

        # 结果数据
        peaks_list = result['peaks_list']
        confidences_list = result['confidences_list']

        max_cols = 5
        cols = min(num_qubits, max_cols)  # 列数不超过max_cols
        rows = (num_qubits + cols - 1) // cols  # 计算需要的行数（向上取整）

        # 创建子图
        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=[f'Spectrum for {q_name}' for q_name in q_name_list],
            vertical_spacing=0.1,
            horizontal_spacing=0.05
        )

        # 为每个 qubit 绘制子图
        for idx, (x, amp, q_name) in enumerate(zip(x_list, amp_list, q_name_list)):
            row = (idx // cols) + 1  # Plotly的行列索引从1开始
            col = (idx % cols) + 1

            # 绘制信号曲线
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=amp,
                    mode='lines',
                    name='Signal',
                    line=dict(color='blue'),
                    showlegend=(idx == 0)  # 只在第一个子图显示图例
                ),
                row=row,
                col=col
            )
            
            # 获取当前 qubit 的峰值和置信度
            peaks = peaks_list[idx] if idx < len(peaks_list) else []
            confidences = confidences_list[idx] if idx < len(confidences_list) else None

            # 绘制峰值
            if peaks:
                if confidences is None:
                    confidences = [None] * len(peaks)
                elif len(confidences) != len(peaks):
                    raise ValueError(f"q_name {q_name} 的peaks和confidences长度不一致")
                
                # 计算峰值对应的幅度（找到最接近的x值）
                peak_amps = [amp[np.argmin(np.abs(x - p))] for p in peaks]
                
                # 添加峰值散点
                fig.add_trace(
                    go.Scatter(
                        x=peaks,
                        y=peak_amps,
                        mode='markers',
                        name='Peak',
                        marker=dict(color='red', size=8),
                        showlegend=(idx == 0)  # 只在第一个子图显示图例
                    ),
                    row=row,
                    col=col
                )
                
                # 添加置信度标注
                for peak, conf, amp_val in zip(peaks, confidences, peak_amps):
                    annotation_text = f'conf: {conf:.4f}' if conf is not None else f'{peak:.4f}'
                    fig.add_annotation(
                        x=peak,
                        y=amp_val,
                        text=annotation_text,
                        xanchor='left',
                        yanchor='bottom',
                        showarrow=True,
                        arrowhead=1,
                        font=dict(size=8),
                        bgcolor='yellow',
                        opacity=0.5,
                        row=row,
                        col=col
                    )
            
            # 设置坐标轴标签
            fig.update_xaxes(title_text='Frequency', row=row, col=col)
            fig.update_yaxes(title_text='Amplitude', row=row, col=col)

        # 调整布局
        fig.update_layout(
            height=400 * rows,  # 每个子图大致400高度
            width=600 * cols,   # 每个子图大致600宽度
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig