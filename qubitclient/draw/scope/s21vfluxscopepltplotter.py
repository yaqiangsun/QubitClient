from qubitclient.draw.pltplotter import QuantumDataPltPlotter


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


        n_plots = len(volt_list) * 2

        fig, axes, rows, cols = self.create_subplots(n_plots)
        axs = axes.flatten()

        # 隐藏多余的子图






        for ii in range(n_plots):
            ax = axs[ii]
            file_name = q_name_list[ii//2]
            volt = volt_list[ii//2]
            freq = freq_list[ii//2]
            s = s_list[ii//2]

            c = self.add_2dmap(ax,freq, volt, s.T,shading_index=0,cmap_index=0)
            #
            fig.colorbar(c, ax=ax)

            if (ii % 2 != 0):
                centcol = len(freq) // 2

                if coscurves_list[ii// 2]:
                    for j, curve in enumerate(coscurves_list[ii// 2]):
                        final_x_cos = [item[0] for item in curve]
                        final_y_cos = [item[1] for item in curve]


                        self.add_line(ax,final_x_cos,final_y_cos, color_index=0, line_style_index=0)
                        if centcol < len(final_x_cos):

                            self.add_annotation(ax,f"conf:{cosconfs_list[ii// 2][j]:.2f}",(final_x_cos[centcol], final_y_cos[centcol]))
            #
                if lines_list[ii// 2]:
                    for j, line in enumerate(lines_list[ii// 2]):
                        final_x_line = [item[0] for item in line]
                        final_y_line = [item[1] for item in line]
                        self.add_line(ax,final_x_line,final_y_line, color_index=1, line_style_index=0)

                        if centcol < len(final_x_line):
                            self.add_annotation(ax,f"conf:{lineconfs_list[ii// 2][j]:.2f}",(final_x_line[centcol], final_y_line[centcol]))

            handles, labels = ax.get_legend_handles_labels()
            self.add_legend(ax, handles, labels)
            self.configure_axis(ax,title=f"{file_name}",xlabel="Bias",ylabel="Frequency (GHz)")

        fig.tight_layout()
        return fig  # ✅ 返回 Figure 对象
