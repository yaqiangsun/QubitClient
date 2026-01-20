import numpy as np
import matplotlib.pyplot as plt
from .pltplotter import QuantumDataPltPlotter

class SpectrumDataPltPlotter(QuantumDataPltPlotter):

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

        fig_width = 6 * cols
        fig_height = 4 * rows
        fig, axes = plt.subplots(rows, cols, figsize=(fig_width, fig_height))
        
        # 处理单元素或一维数组的axes，统一转为二维数组便于索引
        if num_qubits == 1:
            axes = np.array([[axes]])
        elif rows == 1 or cols == 1:
            axes = axes.reshape(rows, cols)

        # 为每个 qubit 绘制子图
        for idx, (x, amp, q_name) in enumerate(zip(x_list, amp_list, q_name_list)):
            row = idx // cols  # 计算当前子图所在行
            col = idx % cols   # 计算当前子图所在列
            ax = axes[row, col]

            # 绘制信号曲线
            ax.plot(x, amp, label='Signal', color='blue')
            
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
                ax.scatter(peaks, peak_amps, color='red', s=50, zorder=3, label='Peak')
                
                # 添加置信度标注
                for peak, conf in zip(peaks, confidences):
                    amp_val = amp[np.argmin(np.abs(x - peak))]
                    if conf is not None:
                        ax.annotate(f'conf: {conf:.4f}',
                                    xy=(peak, amp_val),
                                    xytext=(5, 5), 
                                    textcoords='offset points',
                                    fontsize=8,
                                    bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5))
                    else:
                        ax.annotate(f'{peak:.4f}',
                                    xy=(peak, amp_val),
                                    xytext=(5, 5), 
                                    textcoords='offset points')
            
            # 设置子图标题和坐标轴标签
            ax.set_title(f'Spectrum for {q_name}')
            ax.set_xlabel('Frequency')
            ax.set_ylabel('Amplitude')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend()

        # 移除多余的子图（当 qubit 数量不足行列乘积时）
        for idx in range(num_qubits, rows * cols):
            row = idx // cols
            col = idx % cols
            fig.delaxes(axes[row, col])

        # 调整子图间距
        plt.tight_layout()
        return fig