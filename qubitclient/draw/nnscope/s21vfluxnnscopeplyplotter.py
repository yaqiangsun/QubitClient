from ..plyplotter import QuantumDataPlyPlotter
import numpy as np

class S21VfluxNNScopeDataPlyPlotter(QuantumDataPlyPlotter):

    def __init__(self):
        super().__init__("s21vfluxnnscope")
    def plot_result_npy(self, **kwargs):
        s21vflux_labels = {0:"cos_light",1:"cos_dark",2:"line_light",3:"line_dark"}
        results = kwargs.get('result')
        data_ndarray = kwargs.get('dict_param')


        n_plots = len(results) * 2

        titles= [f"{list(data_ndarray.item()['image'].keys())[i // 2]}" for i in range(n_plots)]
        # 创建子图布局
        fig,rows,cols = self.create_subplots(n_plots,titles)

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

        for index in range(n_plots):
            result = results[index // 2]
            points_list = []
            for i in range(len(result["linepoints_list"])):
                points_list.append(result["linepoints_list"][i])

            bias = dict_list[index // 2]["bias"]
            frequency = dict_list[index // 2]["frequency"]
            iq_avg = dict_list[index // 2]["iq_avg"]

            self.add_2dmap(fig,x=bias,
                y=frequency,
                z=np.flipud(iq_avg.T),row=(index // cols) + 1, col=(index % cols) + 1,showscale=(index == 0))

            if (index % 2 != 0):
                colors = [f'hsl({i * 360 / len(points_list)}, 100%, 50%)' for i in range(len(points_list))]
                for i in range(len(points_list)):
                    reflection_points = np.array(points_list[i])
                    xy_x = reflection_points[:, 0]
                    xy_y = reflection_points[:, 1]
                    class_id = s21vflux_labels[int(result["class_ids"][i])]

                    self.add_line(fig, x=xy_x,
                                  y=xy_y, row=(index // cols) + 1, col=(index % cols) + 1, name=f'{class_id}:{round(result["confidence_list"][i], 2)}', color_index=i,
                                  line_style_index=0)
                    centcol = len(xy_y)//2
                    self.add_annotation(fig, x=xy_x[centcol],
                                        y=xy_y[centcol],
                                        text=f'{class_id}:{round(result["confidence_list"][i], 2)}', row=(index // cols) + 1, col=(index % cols) + 1)

        self.update_layout(fig, rows, cols)
        self.configure_axis(fig, rows, cols, xlable="Bias", ylable="Frequency (GHz)")
        return fig