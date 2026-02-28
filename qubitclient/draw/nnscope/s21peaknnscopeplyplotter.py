from ..plyplotter import QuantumDataPlyPlotter
import numpy as np

class S21PeakNNScopeDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("s21peaknnscope")

    def plot_result_npy(self, **kwargs):

        result_param = kwargs.get('result')
        dict_param = kwargs.get('dict_param')
        dict_param = dict_param.item()

        image = dict_param["image"]
        q_list = image.keys()
        x_list = []
        amp_list = []
        phi_list = []
        qname_list=[]
        for idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            x = image_q[0]
            amp = image_q[1]
            phi = image_q[2]
            x_list.append((x))
            amp_list.append((amp))
            phi_list.append((phi))
            qname_list.append(q_name)

        peaks_list = result_param['peaks']
        confs_list = result_param['confs']
        freqs_list = result_param['freqs_list']

        # 计算子图布局
        n_plots = len(x_list)

        titles = [f"{qname_list[i]}" for i in range(n_plots)]
        # 创建子图布局
        second_y=True
        fig, row, col = self.create_subplots(n_plots, titles,second_y=second_y)

        for i in range(len(x_list)):
            x = x_list[i]
            y1 = amp_list[i]
            y2 = phi_list[i]
            peaks = peaks_list[i]
            confs = confs_list[i]
            freqs = freqs_list[i]

            current_row = i // col + 1
            current_col = i % col + 1

            # 添加幅度曲线到主Y轴

            self.add_line(fig,x=x, y=y1,row=current_row, col=current_col,color_index=0,line_style_index=0,name=f'{qname_list[i]}: Amp Curve',showlegend=True)

            self.add_line(fig,x=x, y=y2,row=current_row, col=current_col,color_index=1,line_style_index=0,name=f'{qname_list[i]}: Phi Curve', secondary_y=True,showlegend=True)

            peak_xs = x[peaks]
            peak_ys = y1[peaks]

            # 使用batch_update批量更新
            # with fig.batch_update():
            for j in range(len(peaks)):
                # 简化图例文本，避免过长
                freq = freqs[j]
                legend_name = f'freq: {freq / 1e9:.2f}GHz'  # 简化为 "2.4G" 格式
                self.add_scatter(fig,x=[peak_xs[j]],y=[peak_ys[j]],name=legend_name,row=current_row, col=current_col,color_index=j,showlegend=True)
                self.add_annotation(fig, x=peak_xs[j],
                                    y=peak_ys[j],
                                    text=f"conf:{confs[j]:.2f}", row=current_row,
                                    col=current_col)

            x_coords = []
            y_coords = []
            ymin, ymax = np.min(y1), np.max(y1)
            for peak_x in peak_xs:
                x_coords.extend([peak_x, peak_x, None])
                y_coords.extend([ymin, ymax, None])

            self.add_line(fig,x=x_coords,
                y=y_coords,row=current_row, col=current_col,color_index=2,line_style_index=1,name="peak",showlegend=True)


            annot_text = [f'{conf:.2f}' for conf in confs]

            # self.add_scatter_points_with_anno(fig,x=peak_xs,
            #     y=peak_ys,
            #     text=annot_text,row=current_row, col=current_col,name="peak",color_index=0)   #add_scatter("text+marker")可以批量处理

        self.update_layout(fig,row,col,showlegend=True)

        self.configure_axis(fig,row,col,xlable="Bias",ylable="Amplitude", secondary_y=False)
        self.configure_axis(fig,row,col,ylable="Phase", secondary_y=True)

        return fig