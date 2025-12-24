import numpy as np
import matplotlib.pyplot as plt
from .pltplotter import QuantumDataPltPlotter

class Spectrum2DNNScopeDataPltPlotter(QuantumDataPltPlotter):
    def __init__(self):
        super().__init__("spectrum2dnnscope")

    def plot_result_npy(self, **kwargs):
        results = kwargs.get('results')
        data_ndarray = kwargs.get('data_ndarray')

        nums = len(results)*2
        row = (nums // 2) + 1 if nums % 2 != 0 else nums // 2
        col = min(nums, 2)

        fig = plt.figure(figsize=(10 * col, 4 * row))
        data_dict = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
        data_dict = data_dict['image']
        dict_list = []
        q_list = data_dict.keys()

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

        for index in range(nums):
            ax = fig.add_subplot(row, col, index + 1)
            result = results[index//2]

            points_list = []
            for i in range(len(result["linepoints_list"])):
                points_list.append(result["linepoints_list"][i])

            plt.pcolormesh(dict_list[index//2]["bias"], dict_list[index//2]["frequency"], dict_list[index//2]["iq_avg"],
                           shading='auto', cmap='viridis')
            plt.colorbar(label='IQ Average')
            colors = plt.cm.rainbow(np.linspace(0, 1, len(result["linepoints_list"])))

            if (index % 2 != 0):
                for i in range(len(points_list)):
                    reflection_points = points_list[i]
                    reflection_points = np.array(reflection_points)
                    xy_x = reflection_points[:, 0]
                    xy_y = reflection_points[:, 1]

                    plt.scatter(xy_x, xy_y, color=colors[i],
                                label=f'XY Points{i}-conf:{round(result["confidence_list"][i], 2)}', s=5,
                                alpha=0.1)
            file_name = dict_list[index//2]["name"]
            plt.title(f"File: {file_name}")
            plt.xlabel("Bias")
            plt.ylabel("Frequency (GHz)")
            plt.legend()
        fig.tight_layout()
        return fig

    def plot_result_npz(self, **kwargs):
        results = kwargs.get('results')
        dict_list = kwargs.get('dict_list')
        file_names = kwargs.get('file_names')

        nums = len(results)*2
        row = (nums // 2) + 1 if nums % 2 != 0 else nums // 2
        col = min(nums, 2)

        fig = plt.figure(figsize=(10 * col, 4 * row))

        for index in range(nums):
            ax = fig.add_subplot(row, col, index + 1)
            result = results[index//2]
            file_name = file_names[index//2]

            points_list = []
            for i in range(len(result["linepoints_list"])):
                points_list.append(result["linepoints_list"][i])

            plt.pcolormesh(dict_list[index//2]["bias"], dict_list[index//2]["frequency"], dict_list[index//2]["iq_avg"],
                           shading='auto', cmap='viridis')
            plt.colorbar(label='IQ Average')
            colors = plt.cm.rainbow(np.linspace(0, 1, len(result["linepoints_list"])))
            if(index%2!=0):
                for i in range(len(points_list)):
                    reflection_points = points_list[i]
                    reflection_points = np.array(reflection_points)
                    xy_x = reflection_points[:, 0]
                    xy_y = reflection_points[:, 1]
                    plt.scatter(xy_x, xy_y, color=colors[i],
                                label=f'XY Points{i}-conf:{round(result["confidence_list"][i], 2)}', s=5,
                                alpha=0.1)
            plt.title(f"File: {file_name}")
            plt.xlabel("Bias")
            plt.ylabel("Frequency (GHz)")
            plt.legend()
        fig.tight_layout()
        return fig
