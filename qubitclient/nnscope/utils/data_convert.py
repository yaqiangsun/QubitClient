# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/10/24 15:54:07
########################################################################


import numpy as np
import io
import os
import numpy as np



def load_npz_file(file_path):
    with np.load(file_path, allow_pickle=True) as data:  # 修改：添加 allow_pickle=True 参数
        # file_contents[file_name] = dict(data)  # 将 .npz 文件内容转换为字典
        content = dict(data)  # 将 .npz 文件内容转换为字典
    return content
def convert_data_to_image(npz_content):
    content = npz_content
    iq_avg = content["iq_avg"]  # 二维数据
    iq_avg_normalized = convert_complex_map__to_image(iq_avg=iq_avg)
    return iq_avg_normalized
def convert_complex_map__to_image(iq_avg):
    import cv2
    
    # 检查并转置
    rows, cols = iq_avg.shape
    if rows < cols:
        iq_avg = iq_avg.T  # 转置矩阵


    # 取相位
    phase = np.angle(iq_avg)
    phase_normalized = ((phase + np.pi) / (2 * np.pi)) * 255
    # 纵向归一化
    phase_mean = phase_normalized.mean(axis=0, keepdims=True)   # 形状(1,30)
    ppase_std = phase_normalized.std(axis=0, keepdims=True)     # 形状(1,30)
    phase_normalized = (phase_normalized - phase_mean) / (ppase_std+1e-8)
    # phase_normalized = phase_normalized.astype(np.uint8)
    # 全局归一化
    phase_normalized = cv2.normalize(phase_normalized, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # 取幅度
    iq_avg = np.abs(iq_avg)
    
    # iq_avg = phase_normalized
    # 纵向归一化
    # mean = iq_avg.mean(axis=0, keepdims=True)   # 形状(1,30)
    # std = iq_avg.std(axis=0, keepdims=True)     # 形状(1,30)
    # iq_avg = (iq_avg - mean) / (std+1e-8)
    # 幅度全局归一化
    iq_avg_normalized = cv2.normalize(iq_avg, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    # return iq_avg_normalized

    #取幅度的梯度
    gradient_y, gradient_x = np.gradient(iq_avg)
    gradient_y = np.abs(gradient_y)
    gradient_y_normalized = cv2.normalize(gradient_y, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    # iq_avg_normalized = cv2.merge([iq_avg_normalized, phase_normalized, gradient_y_normalized])
    iq_avg_normalized = cv2.merge([iq_avg_normalized, iq_avg_normalized, iq_avg_normalized])
    return iq_avg_normalized

    
def load_npz_to_image(file_path):
    npz_content = load_npz_file(file_path)
    image = convert_data_to_image(npz_content)
    return image

def convert_spectrum_npy2npz(npy_file_path:str):
    data = np.load(npy_file_path, allow_pickle=True)
    data = data.item() if isinstance(data, np.ndarray) else data
    dict_list, name_list = convert_spectrum_dict2npz(data,npy_file_path)
    return dict_list, name_list
def convert_spectrum_dict2npz(data:dict,npy_file_path:str="None.npy"):
    if not isinstance(data, dict) or 'image' not in data:
            raise ValueError("数据格式无效，缺少 'image' 键")
    image = data["image"]
    q_list = image.keys()

    dict_list = []
    name_list = []

    for idx, q_name in enumerate(q_list):
        image_q = image[q_name]

        data = image_q[0]
        if data.ndim != 2:
            raise ValueError("数据格式无效，data不是二维数组")
        data = np.array(data)
        data = np.abs(data)
        height_axis = image_q[1]
        width_axis = image_q[2]
        new_dict = {}
        new_dict["iq_avg"] = data
        new_dict["frequency"] = image_q[2]
        new_dict["bias"] = image_q[1]

        npz_file_path = npy_file_path.replace(".npy", f"{q_name}.npz")
        dict_list.append(new_dict)
        name_list.append(npz_file_path)
        # npz_file_path = npz_file_path.replace("npyfile","npyconverted")
        # np.savez(npz_file_path,**new_dict)
        # np.savez(npz_file_path,iq_avg=image_q[0],frequency=image_q[2],bias=image_q[1])
    return dict_list, name_list

if __name__ == '__main__':
    npy_file_path = "tmp/npyfile/tmp0ffc025b.py_4905.npy"
    convert_spectrum_npy2npz(npy_file_path)

    image = load_npz_to_image("tmp/npyconverted/tmp0ffc025b.py_4905Q6.npz")