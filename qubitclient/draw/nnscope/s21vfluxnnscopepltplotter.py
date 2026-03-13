import numpy as np
from ..pltplotter import QuantumDataPltPlotter



class S21VfluxNNScopeDataPltPlotter(QuantumDataPltPlotter):


    def __init__(self):
        super().__init__("s21vfluxnnscope")
    def plot_result_npy(self, **kwargs):
        s21vflux_labels = {0:"cos_light",1:"cos_dark",2:"line_light",3:"line_dark"}

        results = kwargs.get('result')
        data_ndarray = kwargs.get('dict_param')






        data_dict = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
        data_dict = data_dict['image']
        dict_list = []
        q_list = data_dict.keys()

        for idx, q_name in enumerate(q_list):
            npz_dict = {}
            image_q = data_dict[q_name]
            data = image_q[2]
            if data.ndim != 2:
                raise ValueError("数据格式无效，data不是二维数组")
            data = np.array(data)
            data = np.abs(data)

            npz_dict['bias'] = image_q[1]
            npz_dict['frequency'] = image_q[0]
            npz_dict['iq_avg'] = data
            npz_dict['name'] = q_name
            dict_list.append(npz_dict)
        n_plots = len(q_list) * 2
        fig, axes, rows, cols = self.create_subplots(n_plots)
        axs = axes.flatten()

        linepoints_list = results['linepoints_list']
        class_ids = results['class_ids']
        confidence_list = results['confidence_list']

        for index in range(n_plots):
            ax = axs[index]
            points_list = linepoints_list[index // 2]





            c = self.add_2dmap(ax,dict_list[index // 2]["bias"], dict_list[index // 2]["frequency"],
                           np.flipud(dict_list[index // 2]["iq_avg"].T),shading_index=0,cmap_index=0)
            fig.colorbar(c, ax=ax)





            if (index % 2 != 0):
                for i in range(len(points_list)):
                    reflection_points = points_list[i]
                    reflection_points = np.array(reflection_points)
                    xy_x = reflection_points[:, 0]
                    xy_y = reflection_points[:, 1]
                    class_id  = s21vflux_labels[int(class_ids[index//2][i])]
                    self.add_line(ax, xy_x, xy_y, color_index=i, line_style_index=0)
                    centcol = len(xy_x) // 2
                    self.add_annotation(ax, f'{class_id} conf:{round(confidence_list[index//2][i], 2)}',
                                        (xy_x[centcol], xy_y[centcol]))


            file_name = dict_list[index // 2]["name"]

            handles, labels = ax.get_legend_handles_labels()
            self.add_legend(ax, handles, labels)
            self.configure_axis(ax, title=f"{file_name}", xlabel="Bias", ylabel="Frequency (GHz)")
        fig.tight_layout()
        return fig

