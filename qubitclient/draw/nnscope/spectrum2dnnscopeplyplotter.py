from ..plyplotter import QuantumDataPlyPlotter
import numpy as np

class Spectrum2DNNScopeDataPlyPlotter(QuantumDataPlyPlotter):
    def __init__(self):
        super().__init__("spectrum2dnnscope")

    def plot_result_npy(self, **kwargs):

        results = kwargs.get('result')
        data_ndarray = kwargs.get('dict_param')

        # 参数验证
        if results is None:
            raise ValueError("缺少必需的 'result' 参数")
        if data_ndarray is None:
            raise ValueError("缺少必需的 'dict_param' 参数")


        # 处理数据字典
        data_dict = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
        data_dict = data_dict['image']
        data_dict = data_dict.item() if isinstance(data_dict, np.ndarray) else data_dict
        dict_list = []
        q_list = data_dict.keys()

        # 准备数据列表
        for idx, q_name in enumerate(q_list):
            npz_dict = {}
            image_q = data_dict[q_name]
            data = image_q[0]
            if data.ndim != 2:
                raise ValueError("数据格式无效，data不是二维数组")
            data = np.array(data)
            data = np.abs(data)

            npz_dict['bias'] = image_q[1]
            npz_dict['frequency'] = image_q[2]
            npz_dict['iq_avg'] = data
            npz_dict['name'] = q_name
            dict_list.append(npz_dict)

        n_plots = len(results)*2

        titles = [f"{dict_list[i//2]['name']}" for i in range(n_plots)]
        # 创建子图布局
        fig, rows, cols = self.create_subplots(n_plots, titles)
        # 遍历每个结果绘制子图
        for index in range(n_plots):
            row = (index // cols) + 1
            col = (index % cols) + 1

            result = results[index//2]
            data = dict_list[index//2]

            # 准备点数据
            points_list = []
            for i in range(len(result["linepoints_list"])):
                points_list.append(np.array(result["linepoints_list"][i]))


            self.add_2dmap(fig, z=data["iq_avg"],
                x=data["bias"],
                y=data["frequency"], row=row, col=col,showscale=(index == 0))
            # 添加散点
            if (index % 2 != 0):
                for i, points in enumerate(points_list):
                    if points.shape[0]:
                        xy_x = points[:, 0]
                        xy_y = points[:, 1]
                        self.add_line(fig, x=xy_x,
                                      y=xy_y, row=row, col=col,
                                      color_index=i, line_style_index=0)
                        centcol = len(xy_x) // 2
                        self.add_annotation(fig, x=xy_x[centcol],
                                            y=xy_y[centcol],
                                            text=f'conf:{round(result["confidence_list"][i], 2)}', row=row,
                                            col=col)


        self.update_layout(fig, rows, cols)
        self.configure_axis(fig, rows, cols, xlable="Bias", ylable="Frequency (GHz)")

        return fig
        # 保存图片
    def plot_result_npz(self, **kwargs):

        results = kwargs.get('results')
        dict_list = kwargs.get('dict_list')
        file_names = kwargs.get('file_names')

        n_plots = len(results)*2

        titles =file_names
        # 创建子图布局
        fig, rows, cols = self.create_subplots(n_plots, titles)

        # 遍历每个结果绘制子图
        for index in range(n_plots):
            row = (index // cols) + 1
            col = (index % cols) + 1

            result = results[index//2]
            data = dict_list[index//2]

            # 准备点数据
            points_list = []
            for i in range(len(result["linepoints_list"])):
                points_list.append(np.array(result["linepoints_list"][i]))

            self.add_2dmap(fig, z=data["iq_avg"],
                           x=data["bias"],
                           y=data["frequency"], row=row, col=col,showscale=(index == 0))
            colors = np.linspace(0, 1, len(points_list))
            # 添加散点
            if (index % 2 != 0):
                for i, points in enumerate(points_list):
                    if points.shape[0]:
                        xy_x = points[:, 0]
                        xy_y = points[:, 1]
                        self.add_line(fig, x=xy_x,
                                      y=xy_y, row=row, col=col,
                                      color_index=i, line_style_index=0)
                        centcol = len(xy_x) // 2
                        self.add_annotation(fig, x=xy_x[centcol],
                                            y=xy_y[centcol],
                                            text=f'conf:{round(result["confidence_list"][i], 2)}', row=row,
                                            col=col)

        self.update_layout(fig, rows, cols)
        self.configure_axis(fig, rows, cols, xlable="Bias", ylable="Frequency (GHz)")

        return fig
