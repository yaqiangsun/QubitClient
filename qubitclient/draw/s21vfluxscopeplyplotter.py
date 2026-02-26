from .plyplotter import QuantumDataPlyPlotter

class S21VfluxScopeDataPlyPlotter(QuantumDataPlyPlotter):


    def __init__(self):
        super().__init__("s21vfluxscope")

    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
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
            volt = image_q[0]
            freq = image_q[1]
            s = image_q[2]

            volt_list.append(volt)
            freq_list.append(freq)
            s_list.append(s)
            q_name_list.append(q_name)

        # 结果数据
        coscurves_list = result['coscurves_list']
        cosconfs_list = result['cosconfs_list']
        lines_list = result['lines_list']
        lineconfs_list = result['lineconfs_list']

        # 计算子图布局
        n_plots = len(volt_list) * 2

        titles= [f"{q_name_list[i // 2]}" for i in range(n_plots)]
        # 创建子图布局
        fig,rows,cols = self.create_subplots(n_plots,titles)

        # 遍历所有子图位置
        for ii in range(n_plots):
            row_pos = (ii // cols) + 1
            col_pos = (ii % cols) + 1

            volt = volt_list[ii // 2]
            freq = freq_list[ii // 2]
            s = s_list[ii // 2]
            q_name = q_name_list[ii // 2]

            self.add_2dmap(fig,x=freq, y=volt,z=s.T,row=row_pos, col=col_pos,showscale=(ii == 0))


            if (ii % 2 != 0):
                centcol = len(freq) // 2

                # 添加余弦曲线
                for j, curve in enumerate(coscurves_list[ii // 2]):
                    if curve:  # 确保曲线数据不为空
                        final_x_cos = [item[0] for item in curve]
                        final_y_cos = [item[1] for item in curve]

                        self.add_line(fig, x=final_x_cos,
                            y=final_y_cos,row=row_pos, col=col_pos,name=f'Cosine Curve {j + 1}',color_index=0,line_style_index=0)


                        # 添加置信度文本
                        if centcol < len(final_x_cos):
                            self.add_annotation(fig,x=final_x_cos[centcol],
                                y=final_y_cos[centcol],
                                text=f"conf:{cosconfs_list[ii // 2][j]:.2f}",row=row_pos,
                                col=col_pos)

                # 添加直线
                if lines_list[ii // 2]:
                    for j, line in enumerate(lines_list[ii // 2]):
                        if line:  # 确保直线数据不为空
                            final_x_line = [item[0] for item in line]
                            final_y_line = [item[1] for item in line]



                            self.add_line(fig, x=final_x_line,
                                          y=final_y_line, row=row_pos, col=col_pos, name=f'Cosine Curve {j + 1}',
                                          color_index=1,line_style_index=0)

                            if centcol < len(final_x_line):

                                self.add_annotation(fig, x=final_x_line[centcol],
                                                    y=final_y_line[centcol],
                                                    text=f"conf:{lineconfs_list[ii // 2][j]:.2f}", row=row_pos,
                                                    col=col_pos)



        self.update_layout(fig,rows,cols)
        self.configure_axis(fig,rows,cols,xlable="Bias",ylable="Frequency (GHz)")
        return fig

