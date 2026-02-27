import numpy as np
from ..pltplotter import QuantumDataPltPlotter
from scipy.stats import norm

class SingleShotDataPltPlotter(QuantumDataPltPlotter):

    def __init__(self):
        super().__init__("singleshot")
    def plotEllipse(self, c0, a, b, phi, ax, color):
        t = np.linspace(0, 1, 1001) * 2 * np.pi  # 生成1001个角度点
        c = np.exp(1j * t)  # 计算椭圆坐标点(包含旋转)
        s = c0 + (c.real * a + 1j * c.imag * b) * np.exp(1j * phi)
        self.add_line(ax,s.real, s.imag, color_index=color)
    def plot_result_npy(self, **kwargs):
        result = kwargs.get('result')
        dict_param = kwargs.get('dict_param')

        dict_param = dict_param.item()

        image = dict_param["image"]
        q_list = image.keys()
        s0_list = []
        s1_list = []
        q_name_list =[]

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
        std_list = result['std_list']
        cdf_list = result['cdf_list']
        hotThresh = 10000  # 切换为热力图模式的样本数阈值




        n_plots = len(s0_list) * 2
        fig, axes, rows, cols = self.create_subplots(n_plots)
        axs = axes.flatten()

        # 隐藏多余的子图
        for i in range(n_plots, len(axs)):
            axs[i].axis('off')






        for i in range(len(s0_list)):
            s0 = s0_list[i]
            s1 = s1_list[i]
            filename = q_name_list[i]
            _, *bins = np.histogram2d(np.real(np.hstack([s0, s1])),
                                      np.imag(np.hstack([s0, s1])),
                                      bins=50)  # 构建二维直方图
            H0, *_ = np.histogram2d(np.real(s0),
                                    np.imag(s0),
                                    bins=bins,
                                    density=True)  # 计算各组密度分
            H1, *_ = np.histogram2d(np.real(s1),
                                    np.imag(s1),
                                    bins=bins,
                                    density=True)
            vlim = max(np.max(np.abs(H0)), np.max(np.abs(H1)))  # 确定可视化范围

            sep_score = sep_score_list[i]

            thr = threshold_list[i]
            phi = phi_list[i]

            # 子图1：复平面图


            ax1 = axs[i*2]
            ax2 = axs[i * 2+1]
            if (len(s0) + len(s1)) < hotThresh:

                self.add_scatter(ax1, np.real(s0), np.imag(s0),marker_index = 0,
                                 color_index=0,alpha=0.8)
                self.add_scatter(ax1, np.real(s1), np.imag(s1), marker_index=0,
                                 color_index=1, alpha=0.8)
            else:
                self.add_2dmap(ax1, s=H1.T - H0.T,
                               x=bins[0],
                               y=bins[1], showscale=False, cmap_index=4)
            self.add_annotation(ax1,f'Separation Degree: {sep_score:.3f}',xy=(0,1),annotation_xytext=(0,1),annotation_textcoords="axes fraction",\
                                color_index=0,showarrow=False)



            ax1.axis('equal')
            for s in ax1.spines.values():
                s.set_visible(False)

            # 椭圆参数提取和绘制
            params = params_list[i]
            r0, i0, r1, i1 = params[0][0], params[1][0], params[0][1], params[1][1]
            a0, b0, a1, b1 = params[0][2], params[1][2], params[0][3], params[1][3]
            c0 = (r0 + 1j * i0) * np.exp(1j * phi)
            c1 = (r1 + 1j * i1) * np.exp(1j * phi)
            phi0 = phi + params[0][6]
            phi1 = phi + params[1][6]
            self.plotEllipse(c0, 2 * a0, 2 * b0, phi0, ax1,0)
            self.plotEllipse(c1, 2 * a1, 2 * b1, phi1, ax1,1)
            im0, im1 = idle_list[i]
            im0 = np.array(im0)
            im1 = np.array(im1)
            lim = min(im0.min(), im1.min()), max(im0.max(), im1.max())
            t = (np.linspace(lim[0], lim[1], 3) + 1j * thr) * np.exp(-1j * phi)

            self.add_line(ax1,t.imag, t.real,line_style_index=1,color_index=2)
            self.add_scatter(ax1, np.real(c0), np.imag(c0), marker_index=1,color_index=0)
            self.add_scatter(ax1, np.real(c1), np.imag(c1), marker_index=1,color_index=1)





            ax1.axis('off')

            # 子图2：投影信号分布图 + CDF
            re0, re1 = signal_list[i]
            x, a, b, c = cdf_list[i]
            re0 = np.array(re0)
            re1 = np.array(re1)
            xrange = (min(re0.min(), re1.min()), max(re0.max(), re1.max()))
            self.add_histogram(ax2,x=re0,bins=100, xrange=xrange)
            self.add_histogram(ax2,x=re1,bins=100, xrange=xrange)


            mu1_y, std1_y = norm.fit(re0)
            mu2_y, std2_y = norm.fit(re1)
            y_range = np.linspace(min(min(re0), min(re1)), max(max(re0), max(re1)), 100)
            pdf1_y = norm.pdf(y_range, mu1_y, std1_y)
            pdf2_y = norm.pdf(y_range, mu2_y, std2_y)


            self.add_line(ax2, y_range, pdf1_y, line_style_index=0, color_index=0)
            self.add_line(ax2, y_range, pdf2_y, line_style_index=0, color_index=1)


            x = np.array(x)
            x_range = np.linspace(x.min(), x.max(), 1001)
            *_, cov0, cov1 = std_list[i]

            ax3 = ax2.twinx()

            self.add_line(ax3, x, a, line_style_index=0, color_index=0)
            self.add_line(ax3, x, b, line_style_index=0, color_index=1)
            self.add_line(ax3, x, c, line_style_index=1, alpha=0.5)

            ax3.set_ylim(0, 1.1)
            self.add_vline(ax3,thr)
            ax2.axis('off')

            self.configure_axis(ax3, title=f"{filename}", ylabel='Probability')


        fig.tight_layout()
        return fig  # ✅ 返回 Figure 对象


