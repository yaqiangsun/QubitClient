import numpy as np
import matplotlib.pyplot as plt
from ..pltplotter import QuantumDataPltPlotter

class SpectrumNNscopeDataPltPlotter(QuantumDataPltPlotter):

    def __init__(self):
        super().__init__("spectrumnnscope")

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
        
        # 调用父类方法创建子图布局（统一风格）
        n_plots = num_qubits
        fig, axes, rows, cols = self.create_subplots(n_plots)
        axs = axes.flatten()

        # 为每个 qubit 绘制子图
        for idx, (x, amp, q_name) in enumerate(zip(x_list, amp_list, q_name_list)):
            ax = axs[idx]

            # 1. 调用父类方法添加信号曲线（统一风格的线条）
            self.add_line(ax, x, amp, label='Signal', color_index=0, line_style_index=0)
            
            # 获取当前 qubit 的峰值和置信度
            peaks = peaks_list[idx] if idx < len(peaks_list) else []
            confidences = confidences_list[idx] if idx < len(confidences_list) else None

            # 绘制峰值（调用父类散点方法）
            if peaks:
                if confidences is None:
                    confidences = [None] * len(peaks)
                elif len(confidences) != len(peaks):
                    raise ValueError(f"q_name {q_name} 的peaks和confidences长度不一致")
                
                # 计算峰值对应的幅度
                peak_amps = [amp[np.argmin(np.abs(x - p))] for p in peaks]
                
                # 2. 调用父类方法添加峰值散点（统一风格）
                self.add_scatter(ax, peaks, peak_amps, label='Peak', 
                                 marker_index=1, color_index=1)
                
                # 添加置信度标注（调用父类注释方法）
                for peak, conf, peak_amp in zip(peaks, confidences, peak_amps):
                    if conf is not None:
                        self.add_annotation(ax, f'conf: {conf:.4f}', 
                                           xy=(peak, peak_amp),
                                           annotation_xytext=(5, 5),
                                           color_index=1,
                                           showarrow=True)
                    else:
                        self.add_annotation(ax, f'{peak:.4f}', 
                                           xy=(peak, peak_amp),
                                           annotation_xytext=(5, 5),
                                           color_index=1,
                                           showarrow=False)
            
            # 3. 调用父类方法配置坐标轴（统一风格）
            self.configure_axis(ax,
                               title=f'Spectrum for {q_name}',
                               xlabel='Frequency',
                               ylabel='Amplitude',
                               show_legend=True)
            
            # 4. 调用父类方法添加图例（统一风格）
            handles, labels = ax.get_legend_handles_labels()
            self.add_legend(ax, handles, labels)

        # 隐藏多余的子图
        for i in range(num_qubits, len(axs)):
            axs[i].axis('off')

        fig.tight_layout()
        return fig