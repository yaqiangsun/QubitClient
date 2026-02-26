

from .pltplotter import QuantumDataPltPlotter




class S21PeakDataPltPlotter(QuantumDataPltPlotter):
    """S21峰值数据绘图器"""

    def __init__(self):
        super().__init__("s21peak")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        dict_param = dict_param.item()
        image = dict_param["image"]
        q_list = list(image.keys())

        # 准备数据
        x_list, amp_list, phi_list, q_name_list = [], [], [], []
        for q_name in q_list:
            image_q = image[q_name]
            x_list.append(image_q[0])
            amp_list.append(image_q[1])
            phi_list.append(image_q[2])
            q_name_list.append(q_name)

        peaks_list = result['peaks']
        confs_list = result['confs']
        freqs_list = result['freqs_list']

        # 创建子图
        n_plots = len(x_list)
        fig, axes, rows, cols = self.create_subplots(n_plots)
        axs = axes.flatten()



        # 绘制每个子图
        for i in range(n_plots):
            x = x_list[i]
            y1 = amp_list[i]
            y2 = phi_list[i]
            peaks = peaks_list[i]
            confs = confs_list[i]
            freqs = freqs_list[i]
            ax = axs[i]
            ax2 = ax.twinx()

            print("ddd",i)
            # 绘制曲线
            line1, _ = self.add_line(ax, x, y1, label='Amp Curve', color_index=0,line_style_index=0)
            line2, _ = self.add_line(ax2, x, y2, label='Phi Curve', color_index=1,line_style_index=0)
            peak_conf_pair = list(zip(peaks, confs))
            peak_conf_pair.sort(key=lambda x:x[1],reverse=True)
            # 绘制峰值
            for j, (peak, conf) in enumerate(peak_conf_pair):
                if j==0:
                    self.add_vline(ax, x[peak], label='Peak')
                else:
                    self.add_vline(ax, x[peak])
                color_idx = j % len(self.style.marker_colors)
                if(j<=self.style.legend_max_scatters):
                    self.add_scatter(ax, x[peak], y1[peak],
                                     label=f'freq: {freqs[j]/1e9:.2f}GHz',
                                     color_index=color_idx)
                else:
                    self.add_scatter(ax, x[peak], y1[peak],
                                     color_index=color_idx)
                # 散点注释
                self.add_annotation(ax, f'{conf:.2f}\nfreq: {freqs[j]/1e9:.2f}GHz', (x[peak], y1[peak]))
                # 竖线


            # 添加图例
            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            self.add_legend(ax, lines1 + lines2, labels1 + labels2)

            self.configure_axis(ax, title=q_name_list[i],
                                xlabel='Frequency', ylabel='Amplitude')
            self.configure_axis(ax2, ylabel='Phase')
        fig.tight_layout()
        return fig