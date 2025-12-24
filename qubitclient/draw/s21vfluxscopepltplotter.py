import numpy as np
import matplotlib.pyplot as plt
from .pltplotter import QuantumDataPltPlotter


class S21VfluxScopeDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("s21vfluxscope")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')
        data = dict_param.item()
        image = data["image"]
        q_list = image.keys()
        volt_list = []
        freq_list = []
        s_list = []
        q_name_list=[]
        for idx, q_name in enumerate(q_list):
            image_q = image[q_name]

            volt = image_q[0]
            freq = image_q[1]
            s = image_q[2]
            volt_list.append(volt)
            freq_list.append(freq)
            s_list.append(s)
            q_name_list.append(q_name)
        coscurves_list = result['coscurves_list']
        cosconfs_list = result['cosconfs_list']
        lines_list = result['lines_list']
        lineconfs_list = result['lineconfs_list']


        nums = len(volt_list) * 2
        row = (nums // 2) + 1 if nums % 2 != 0 else nums // 2
        col = 2

        fig, axes = plt.subplots(row, col, figsize=(10 * col, 4 * row))

        axes = axes.flatten()  # Flatten in case of multiple rows

        for ii in range(nums):
            ax = axes[ii]

            volt = volt_list[ii//2]
            freq = freq_list[ii//2]
            s = s_list[ii//2]

            c = ax.pcolormesh(freq, volt, s.T, shading='auto', cmap='viridis')
            fig.colorbar(c, ax=ax, label='Intensity')
            if (ii % 2 != 0):
                centcol = len(freq) // 2

                if coscurves_list[ii// 2]:
                    for j, curve in enumerate(coscurves_list[ii// 2]):
                        final_x_cos = [item[0] for item in curve]
                        final_y_cos = [item[1] for item in curve]
                        ax.plot(final_x_cos, final_y_cos, 'r')
                        if centcol < len(final_x_cos):
                            ax.text(final_x_cos[centcol], final_y_cos[centcol],
                                    f"conf:{cosconfs_list[ii// 2][j]:.2f}", color='r', fontsize=12)

                if lines_list[ii// 2]:
                    for j, line in enumerate(lines_list[ii// 2]):
                        final_x_line = [item[0] for item in line]
                        final_y_line = [item[1] for item in line]
                        ax.plot(final_x_line, final_y_line, 'r')
                        if centcol < len(final_x_line):
                            ax.text(final_x_line[centcol], final_y_line[centcol],
                                    f"conf:{lineconfs_list[ii// 2][j]:.2f}", color='r', fontsize=12)

            # ax.set_title('Smoothed Heatmap')
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_title(f"{q_name_list[ii//2]}")
        # Hide unused subplots if any
        for jj in range(nums, len(axes)):
            fig.delaxes(axes[jj])

        fig.tight_layout()
        return fig  # ✅ 返回 Figure 对象
