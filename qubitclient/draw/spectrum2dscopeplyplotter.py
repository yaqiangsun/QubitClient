from .plyplotter import QuantumDataPlyPlotter
import numpy as np

class Spectrum2DScopeDataPlyPlotter(QuantumDataPlyPlotter):


    def __init__(self):
        super().__init__("spectrum2dscope")

    def plot_result_npy(self, **kwargs):

        results = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        data = dict_param.item()
        image = data["image"]
        q_list = image.keys()

        # 数据提取
        volt_list = []
        freq_list = []
        s_list = []
        q_name_list = []

        for idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            volt = image_q[1]
            freq = image_q[2]
            s = np.abs(image_q[0])

            volt_list.append(volt)
            freq_list.append(freq)
            s_list.append(s)
            q_name_list.append(q_name)

        # 结果数据
        coslines_list = results['params']
        cosconfs_list = results['confs']
        coscompress_list = results['coscompress_list']
        lines_list = results['lines_list']
        lineconfs_list = results['lineconfs_list']


        n_plots = len(volt_list) * 2

        titles = [f"{q_name_list[i // 2]}" for i in range(n_plots)]
        # 创建子图布局
        fig, rows, cols = self.create_subplots(n_plots, titles)

        # 遍历所有子图位置
        for ii in range(n_plots):
            row_pos = (ii // cols) + 1
            col_pos = (ii % cols) + 1

            volt = volt_list[ii // 2]
            freq = freq_list[ii // 2]
            s = s_list[ii // 2]
            coslines = coslines_list[ii // 2]
            cosconfs = cosconfs_list[ii // 2]
            coscompress = coscompress_list[ii // 2]
            lines = lines_list[ii // 2]
            lineconfs = lineconfs_list[ii // 2]


            self.add_2dmap(fig, x=volt,
                y=freq,
                z=s,row=row_pos, col=col_pos,showscale=(ii == 0))

            # 在奇数编号的子图中添加曲线和线条
            if (ii % 2 != 0):
                # 添加直线
                if lines:
                    for j, line in enumerate(lines):
                        if line:
                            final_x_line = [item[0] for item in line]
                            final_line_pred = [item[1] for item in line]
                            self.add_line(fig, x=final_x_line,
                                y=final_line_pred,row=row_pos, col=col_pos, name=f'Line {j + 1}',
                                          color_index=0, line_style_index=0)
                            centcol = len(final_x_line)//2
                            self.add_annotation(fig, x=final_x_line[centcol],
                                                y=final_line_pred[centcol],
                                                text=f"conf: {lineconfs[j]:.2f}", row=row_pos,
                                                col=col_pos)


                # 添加余弦曲线
                if coslines:
                    for j, cosline in enumerate(coslines):
                        if cosline:
                            final_x_cos = [item[0] for item in cosline]
                            final_cos_pred = [item[1] for item in cosline]
                            self.add_line(fig, x=final_x_cos,
                                          y=final_cos_pred, row=row_pos, col=col_pos, name=f'Cosine {j + 1}',
                                          color_index=0, line_style_index=0)
                            centcol = len(final_x_cos) // 2
                            self.add_annotation(fig, x=final_x_cos[centcol],
                                                y=final_cos_pred[centcol],
                                                text=f"conf: {cosconfs[j]:.2f}<br>compress: {coscompress[j]:.2f}", row=row_pos,
                                                col=col_pos)

        self.update_layout(fig, rows, cols)
        self.configure_axis(fig, rows, cols, xlable="Bias", ylable="Frequency (GHz)")


        return fig
