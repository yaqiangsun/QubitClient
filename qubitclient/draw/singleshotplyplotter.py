from .plyplotter import QuantumDataPlyPlotter
import numpy as np
from scipy.stats import norm

class SingleShotDataPlyPlotter(QuantumDataPlyPlotter):


    def __init__(self):
        super().__init__("singleshot")
    def plotEllipse(self, c0, a, b, phi):
        """生成椭圆坐标点"""
        t = np.linspace(0, 1, 1001) * 2 * np.pi
        c = np.exp(1j * t)
        s = c0 + (c.real * a + 1j * c.imag * b) * np.exp(1j * phi)
        return s.real, s.imag

    def plot_result_npy(self, **kwargs):

        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        dict_param = dict_param.item()
        image = dict_param["image"]
        q_list = image.keys()
        s0_list = []
        s1_list = []
        q_name_list = []

        # 提取数据
        for idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            s0 = image_q[0]
            s1 = image_q[1]
            s0_list.append(s0)
            s1_list.append(s1)
            q_name_list.append(q_name)

        sep_score_list = result['sep_score_list']
        threshold_list = result['threshold_list']
        phi_list = result['phi_list']
        signal_list = result['signal_list']
        idle_list = result['idle_list']
        params_list = result['params_list']
        cdf_list = result['cdf_list']
        num_qubits = len(s0_list)


        n_plots = len(s0_list) * 2
        titles = [f"{q_name_list[i//2]}" for i in range(n_plots)]
        # 创建子图布局
        second_y = True
        fig, rows, cols = self.create_subplots(n_plots, titles, second_y=second_y)
        hotThresh = 10000

        for i in range(len(s0_list)):
            s0 = s0_list[i]
            s1 = s1_list[i]

            sep_score = sep_score_list[i]
            thr = threshold_list[i]
            phi  = phi_list[i]

            # 计算行和列位置
            row_pos = (i) + 1
            col_pos_left =  1
            col_pos_right = col_pos_left + 1

            # 子图1：复平面图
            if (len(s0) + len(s1)) < hotThresh:

                self.add_scatter(fig,x=np.real(s0), y=np.imag(s0),\
                                        name=f'{q_name_list[i]}|0⟩',row=row_pos, col=col_pos_left,color_index=0)
                self.add_scatter(fig, x=np.real(s1), y=np.imag(s1), \
                                        name=f'{q_name_list[i]}|1⟩', row=row_pos, col=col_pos_left, color_index=1)
            else:
                # 热力图模式
                _, *bins = np.histogram2d(
                    np.real(np.hstack([s0, s1])),
                    np.imag(np.hstack([s0, s1])),
                    bins=50
                )
                H0, *_ = np.histogram2d(
                    np.real(s0), np.imag(s0),
                    bins=bins, density=True
                )
                H1, *_ = np.histogram2d(
                    np.real(s1), np.imag(s1),
                    bins=bins, density=True
                )

                heatmap_data = H1.T - H0.T


                self.add_2dmap(fig,z=heatmap_data,
                        x=bins[0],
                        y=bins[1],showscale=False,row=row_pos, col=col_pos_left,colorscale_index=1)

            self.add_annotation(fig, x=0, y=1,xref="x domain",yref="y domain",showarrow=False,
                                text=f'Separation: {sep_score:.3f}', row=row_pos,
                                col=col_pos_left)

            # 椭圆绘制
            params = params_list[i]
            r0, i0, r1, i1 = params[0][0], params[1][0], params[0][1], params[1][1]
            a0, b0, a1, b1 = params[0][2], params[1][2], params[0][3], params[1][3]
            c0 = (r0 + 1j * i0) * np.exp(1j * phi)
            c1 = (r1 + 1j * i1) * np.exp(1j * phi)
            phi0 = phi + params[0][6]
            phi1 = phi + params[1][6]

            # 绘制两个椭圆
            ellipse0_x, ellipse0_y = self.plotEllipse(c0, 2 * a0, 2 * b0, phi0)
            ellipse1_x, ellipse1_y = self.plotEllipse(c1, 2 * a1, 2 * b1, phi1)


            self.add_line(fig,x=ellipse0_x, y=ellipse0_y,row=row_pos, col=col_pos_left,color_index=0,\
                          line_style_index=0)
            self.add_line(fig, x=ellipse1_x, y=ellipse1_y, row=row_pos, col=col_pos_left, color_index=1, \
                          line_style_index=0)

            im0, im1 = idle_list[i]
            im0 = np.array(im0)
            im1 = np.array(im1)
            lim = min(im0.min(), im1.min()), max(im0.max(), im1.max())
            t = (np.linspace(lim[0], lim[1], 3) + 1j * thr) * np.exp(-1j * phi)

            self.add_line(fig,  x=t.imag,y=t.real, row=row_pos, col=col_pos_left, color_index=2, \
                          line_style_index=0)

            self.add_scatter(fig, x=[np.real(c0)], y=[np.imag(c0)], row=row_pos,
                                    col=col_pos_left, color_index=2,marker_index=0)
            self.add_scatter(fig,  x=[np.real(c1)], y=[np.imag(c1)],  row=row_pos,
                                    col=col_pos_left, color_index=3,marker_index=0)

            # 子图2：投影信号分布图
            re0, re1 = signal_list[i]
            x, a, b, c = cdf_list[i]
            re0 = np.array(re0)
            re1 = np.array(re1)
            xrange = (min(re0.min(), re1.min()), max(re0.max(), re1.max()))


            self.add_histogram(fig,x=re0,nbinsx=100,xbins=dict(start=xrange[0], end=xrange[1]), name='|0⟩',\
                               marker_color_index=0,row=row_pos, col=col_pos_right)
            self.add_histogram(fig, x=re1, nbinsx=100, xbins=dict(start=xrange[0], end=xrange[1]), name='|1⟩', \
                               marker_color_index=1, row=row_pos, col=col_pos_right)


            # 高斯拟合曲线
            mu1_y, std1_y = norm.fit(re0)
            mu2_y, std2_y = norm.fit(re1)
            y_range = np.linspace(
                min(min(re0), min(re1)),
                max(max(re0), max(re1)),
                100
            )
            pdf1_y = norm.pdf(y_range, mu1_y, std1_y)
            pdf2_y = norm.pdf(y_range, mu2_y, std2_y)


            self.add_line(fig, x=y_range, y=pdf1_y, row=row_pos, col=col_pos_right, color_index=0, \
                          line_style_index=0)

            self.add_line(fig, x=y_range, y=pdf2_y, row=row_pos, col=col_pos_right, color_index=1, \
                          line_style_index=0)

            self.add_line(fig,x=x, y=a, row=row_pos, col=col_pos_right, color_index=0, \
                          line_style_index=0,secondary_y=True)
            self.add_line(fig, x=x, y=b, row=row_pos, col=col_pos_right, color_index=1, \
                          line_style_index=0,secondary_y=True)
            self.add_line(fig, x=x, y=c, row=row_pos, col=col_pos_right, color_index=2, \
                          line_style_index=0,secondary_y=True)
            self.add_vline(fig, x=thr, row=row_pos, col=col_pos_right, color_index=3, \
                          line_style_index=0)



        self.update_layout(fig, rows, cols)

        self.configure_axis(fig, rows, cols, ylable="Probability", secondary_y=True)

        return fig
