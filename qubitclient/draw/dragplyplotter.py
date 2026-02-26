
from .plyplotter import QuantumDataPlyPlotter

class DragDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("drag")
    def plot_result_npy(self,**kwargs):
        result_param = kwargs.get('result')
        dict_param = kwargs.get('dict_param')
        dict_param = dict_param.item()

        image = dict_param["image"]
        q_list = image.keys()
        x_list = []
        y0_list = []
        y1_list = []
        qname_list = []
        for idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            x = image_q[2]
            y0 = image_q[3][0]
            y1 = image_q[3][1]
            x_list.append((x))
            y0_list.append(y0)
            y1_list.append(y1)
            qname_list.append(q_name)

        x_pred_list = result_param['x_pred_list']
        y0_pred_list = result_param['y0_pred_list']
        y1_pred_list = result_param['y1_pred_list']
        intersections_list = result_param['intersections_list']

        intersections_confs_list = result_param['intersections_confs_list']



        n_plots = len(x_list)

        titles = [f"{qname_list[i]}" for i in range(n_plots)]
        # 创建子图布局
        second_y = True
        fig, row, col = self.create_subplots(n_plots, titles, second_y=second_y)

        for ii in range(n_plots):
            r = (ii // col) + 1
            c = (ii % col) + 1

            x = x_list[ii]
            y0 = y0_list[ii]
            y1 = y1_list[ii]
            x_pred = x_pred_list[ii]
            y0_pred = y0_pred_list[ii]
            y1_pred = y1_pred_list[ii]
            intersections = intersections_list[ii]
            intersections_confs = intersections_confs_list[ii]

            self.add_scatter(fig, x=x, y=y0, name=f'Data Y0 #{ii + 1}', row=r,
                                    col=c, color_index=0)
            self.add_scatter(fig, x=x, y=y1, name=f'Data Y1 #{ii + 1}', row=r,
                                    col=c, color_index=1)
            self.add_line(fig,x=x, y=y0,row=r, col=c,color_index=0,line_style_index=0,\
                          name=f'Data Y0 #{ii + 1}')
            self.add_line(fig, x=x, y=y1, row=r, col=c, color_index=1, line_style_index=0, \
                          name=f'Data Y1 #{ii + 1}')
            self.add_line(fig, x=x_pred, y=y0_pred, row=r, col=c, color_index=2, line_style_index=0, \
                          name=f'Fit Y0 #{ii + 1}')
            self.add_line(fig,x=x_pred, y=y1_pred, row=r, col=c, color_index=2, line_style_index=0, \
                          name=f'Fit Y1 #{ii + 1}')


            if intersections:
                for j in range(len(intersections)):
                    self.add_annotation(fig, x=intersections[j][0],
                                        y=intersections[j][1],
                                        text=f"conf:{intersections_confs[j]:.2f}", row=r,
                                        col=c)

        self.update_layout(fig, row, col)
        self.configure_axis(fig, row, col, xlable="x", ylable="y")

        return fig