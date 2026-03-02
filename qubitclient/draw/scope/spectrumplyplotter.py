import numpy as np
from ..plyplotter import QuantumDataPlyPlotter

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
            x = image_q[0]  # x轴数据（如频率）
            amp = image_q[1]  # 幅度数据
            
            x_list.append(x)
            amp_list.append(amp)
            q_name_list.append(q_name)

        # 结果数据
        peaks_list = result['peaks_list']
        confidences_list = result['confidences_list']

        # 生成子图标题
        titles = [f'Spectrum for {q_name}' for q_name in q_name_list]
        # 使用父类方法创建子图布局
        fig, rows, cols = self.create_subplots(num_qubits, titles)

        # 为每个 qubit 绘制子图
        for idx, (x, amp, q_name) in enumerate(zip(x_list, amp_list, q_name_list)):
            row = (idx // cols) + 1  # Plotly的行列索引从1开始
            col = (idx % cols) + 1

            # 绘制信号曲线（调用父类add_line方法）
            self.add_line(
                fig,
                x=x,
                y=amp,
                row=row,
                col=col,
                color_index=0,  # 蓝色（对应原代码的blue）
                line_style_index=0,
                name='Signal',
                showlegend=(idx == 0)  # 只在第一个子图显示图例
            )
            
            # 获取当前 qubit 的峰值和置信度
            peaks = peaks_list[idx] if idx < len(peaks_list) else []
            confidences = confidences_list[idx] if idx < len(confidences_list) else None

            # 绘制峰值（调用父类add_scatter方法）
            if peaks:
                if confidences is None:
                    confidences = [None] * len(peaks)
                elif len(confidences) != len(peaks):
                    raise ValueError(f"q_name {q_name} 的peaks和confidences长度不一致")
                
                # 计算峰值对应的幅度（找到最接近的x值）
                peak_amps = [amp[np.argmin(np.abs(x - p))] for p in peaks]
                
                # 添加峰值散点
                self.add_scatter(
                    fig,
                    x=peaks,
                    y=peak_amps,
                    row=row,
                    col=col,
                    color_index=1,  # 红色（对应原代码的red）
                    marker_index=0,
                    name='Peak',
                    showlegend=(idx == 0)  # 只在第一个子图显示图例
                )
                
                # 添加置信度标注（调用父类add_annotation方法）
                for peak, conf, amp_val in zip(peaks, confidences, peak_amps):
                    annotation_text = f'conf: {conf:.4f}' if conf is not None else f'{peak:.4f}'
                    self.add_annotation(
                        fig,
                        text=annotation_text,
                        x=peak,
                        y=amp_val,
                        xref="x",
                        yref="y",
                        row=row,
                        col=col,
                        xanchor='left',
                        yanchor='bottom',
                        showarrow=True,
                        arrowhead=1,
                        font=dict(size=8),
                        bgcolor='yellow',
                        opacity=0.5
                    )

        # 调用父类方法更新布局
        self.update_layout(fig, rows, cols, showlegend=True)
        # 配置坐标轴标签
        self.configure_axis(fig, rows, cols, xlable="Frequency", ylable="Amplitude")

        return fig