import numpy as np
import matplotlib.pyplot as plt
from .pltplotter import QuantumDataPltPlotter

class Spectrum2DScopeDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("spectrum2dscope")

    def plot_result_npy(self, **kwargs):
        results = kwargs.get('result')
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

            volt = image_q[1]
            freq = image_q[2]
            s = np.abs(image_q[0])
            volt_list.append(volt)
            freq_list.append(freq)
            s_list.append(s)
            q_name_list.append(q_name)
        coslines_list= results['params']
        cosconfs_list= results['confs']
        coscompress_list= results['coscompress_list']
        lines_list= results['lines_list']
        lineconfs_list= results['lineconfs_list']

        nums = len(volt_list)*2
        row = (nums // 2) + 1 if nums % 2 != 0 else nums // 2
        col = min(nums, 2)

        fig = plt.figure(figsize=(5 * col, 4 * row))

        for ii in range(nums):
            ax = fig.add_subplot(row, col, ii + 1)

            volt = volt_list[ii//2]
            freq = freq_list[ii//2]
            s = s_list[ii//2]
            coslines = coslines_list[ii//2]
            cosconfs = cosconfs_list[ii//2]
            coscompress = coscompress_list[ii//2]
            lines = lines_list[ii//2]
            lineconfs = lineconfs_list[ii//2]
            plt.pcolormesh(volt, freq, s, cmap='viridis')
            if (ii % 2 != 0):
                if (lines):
                    for j, line in enumerate(lines):
                        final_x_line = [item[0] for item in line]
                        final_line_pred = [item[1] for item in line]
                        plt.plot(final_x_line, final_line_pred, c='r')
                        plt.text(volt[len(volt) // 2], freq[len(freq) // 2], f'confidence: {lineconfs[j]:.2f}', c='red',
                                 size=15)

                if (coslines):
                    for j, cosline in enumerate(coslines):
                        final_x_cos = [item[0] for item in cosline]
                        final_cos_pred = [item[1] for item in cosline]
                        plt.plot(final_x_cos, final_cos_pred, c='r')
                        plt.text(volt[len(volt) // 2], freq[len(freq) // 2],
                                 f'confidence: {cosconfs[j]:.2f}\ncompress: {coscompress[j]:.2f}', c='red', size=15)
            ax.set_title(f"{q_name_list[ii//2]}")
        fig.tight_layout()
        return fig  # ✅ 返回 Figure 对象
