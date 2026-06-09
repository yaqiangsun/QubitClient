# -*- coding: utf-8 -*-

'''
将npy文件中的量子数据 可视化 的脚本
'''

import os
import numpy as np
import matplotlib.pyplot as plt

# -----------配置常量---------------
data_type = 'zz_coupling'
root_folder = f'./tmp/dataset/run/{data_type}'
plot_save_folder = f'./plot_{data_type}_matplotlib'
cnt = 0

# -----------创建目录---------------
os.makedirs(plot_save_folder, exist_ok=True)


def inspect_info_structure(each_qubit_info):
    '''打印 数据的类型和结构，便于解析数据'''
    for i in range(len(each_qubit_info)):
        tmp = each_qubit_info[i]
        if type(tmp) == np.ndarray:
            print("1-------tmp is ndarray, len(tmp):  ", i, len(tmp), tmp.shape, "\n", tmp)
        elif type(tmp) == list:
            print("2-------tmp is list, len(tmp): ", i, len(tmp), "\n", tmp)
        elif type(tmp) == tuple:
            print("3-------tmp is tuple, len(tmp): ", i, len(tmp), "\n", tmp)
        else:
            print("4-------tmp: ", i, type(tmp), tmp)


def plot_pic(file_path):
    '''处理单个npy文件，将多个量子比特的 图形 解析并绘制'''
    with open(file_path, 'rb') as f:
        data = np.load(f, allow_pickle=True)
        print("npy data: ", data.keys())
    image = data['image']

    print("image: ", image.keys())

    # ---------遍历每个qubit---------
    for each_qubit_name, each_qubit_info  in image.items():
        print("each_qubit_name: ", each_qubit_name)
        print("each_qubit_info: ", len(each_qubit_info))

        # ------打印数据类型和结构------------
        # inspect_info_structure(each_qubit_info)

        # ---------解析数据---------
        data = each_qubit_info[0]
        
        x_axis = each_qubit_info[1]
        y_axis = each_qubit_info[2]

        img_height = len(y_axis)
        img_width = len(x_axis)

        # ---------初始化图像，并逐行逐列填充数据---------
        img = np.zeros((len(y_axis), len(x_axis)), dtype=np.float32)
        for row_idx in range(img_height):
            # print("\n", row_idx)

            cur_row_value = []
            for col_idx in range(img_width):
                x = x_axis[col_idx]
                # print("data.shape: ",type(data), data.shape)
                value = data[row_idx, col_idx]
                cur_row_value.append(value)

                img[row_idx, col_idx] = float(value)

        # ---------绘制热力图---------
        plt.figure(figsize=(10, 6))
        plt.imshow(img, cmap='viridis', aspect='auto', origin='lower' )

        plt.xlabel('X Qubit-A Flux Bias (V)')
        plt.ylabel('Y Frequency of Qubit-B (GHz)')
        plt.xticks(
            ticks=np.arange(0, len(x_axis), 6),
            labels=np.round(x_axis[::6], 6),
            rotation=45
        )
        plt.yticks(ticks=np.arange(0, len(y_axis), 10), labels=np.round(y_axis[::10] * 1e6, 2) )
        plt.title(f'{data_type} \n {file_name} \n {each_qubit_name}')

        # ---------保存图像---------
        plt.tight_layout()
        save_path = os.path.join(plot_save_folder, f"pic_{file_name}_{each_qubit_name}.png")
        plt.savefig(save_path, bbox_inches='tight', dpi=150, pad_inches=0.2)
        
        plt.close()
        print("plot pic saved to ", os.path.join(plot_save_folder, f"pic_{file_name}_{each_qubit_name}.png"))


if __name__ == "__main__":
    # 遍历文件夹中的所有.npy文件
    for file_name in os.listdir(root_folder):
        if not file_name.endswith('.npy'):
            continue

        file_path = os.path.join(root_folder, file_name)
        print("Processing:  ", file_path)

        plot_pic(file_path)
