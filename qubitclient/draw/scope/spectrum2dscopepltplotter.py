
import numpy as np
from ..pltplotter import QuantumDataPltPlotter

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


        n_plots = len(volt_list)*2
        fig, axes, rows, cols = self.create_subplots(n_plots)
        axs = axes.flatten()

        for ii in range(n_plots):
            ax = axs[ii]
            file_name = q_name_list[ii//2]

            volt = volt_list[ii//2]
            freq = freq_list[ii//2]
            s = s_list[ii//2]
            coslines = coslines_list[ii//2]
            cosconfs = cosconfs_list[ii//2]
            coscompress = coscompress_list[ii//2]
            lines = lines_list[ii//2]
            lineconfs = lineconfs_list[ii//2]




            c = self.add_2dmap(ax, volt, freq, s, shading_index=0, cmap_index=0)
            fig.colorbar(c, ax=ax)

            if (ii % 2 != 0):
                if (lines):
                    for j, line in enumerate(lines):
                        final_x_line = [item[0] for item in line]
                        final_line_pred = [item[1] for item in line]


                        centcol = len(final_x_line) // 2
                        self.add_line(ax, final_x_line, final_line_pred, color_index=0, line_style_index=0)
                        self.add_annotation(ax, f'confidence: {lineconfs[j]:.2f}',
                                                (final_x_line[centcol], final_line_pred[centcol]))
                if (coslines):
                    for j, cosline in enumerate(coslines):
                        final_x_cos = [item[0] for item in cosline]
                        final_cos_pred = [item[1] for item in cosline]

                        centcol = len(final_x_cos) // 2
                        self.add_line(ax, final_x_cos, final_cos_pred, color_index=1, line_style_index=0)
                        self.add_annotation(ax, f'confidence: {cosconfs[j]:.2f}\ncompress: {coscompress[j]:.2f}',
                                            (final_x_cos[centcol], final_cos_pred[centcol]))
            self.configure_axis(ax,title=f"{file_name}",xlabel="Bias",ylabel="Frequency (GHz)")
        fig.tight_layout()
        return fig  # ✅ 返回 Figure 对象
