# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/10/20 18:24:01
########################################################################

import os
import sys

# 获取当前文件的绝对路径，向上两层就是项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient import QubitScopeClient
from qubitclient import TaskName

from qubitclient.scope.utils.data_parser import load_npy_file
from qubitclient.draw.pltmanager import QuantumPlotPltManager  # using matplotlib draw NPY/NPZ data
from qubitclient.draw.plymanager import QuantumPlotPlyManager  # using plotly draw NPY/NPZ data

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def transform_powershift_npy_and_processed_data(url, api_key, dict_list):
    savenamelist = []
    client = QubitScopeClient(url=url, api_key=api_key)
    # 使用从文件路径加载后的对象，格式为np.ndarray，多个组合成list
    response = client.request(file_list=dict_list, task_type=TaskName.POWERSHIFT)

    # === 解析结果并绘图（每个文件单独生成 HTML）===
    # 1. 解析服务器返回
    if hasattr(response, 'parsed'):
        response_data = response.parsed
    elif isinstance(response, dict):
        response_data = response
    else:
        response_data = {}

    results = response_data.get("results", [])
    trans_all_npy = []
    
    for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
        result = result
        data = dict_param.item()
        image = data["image"]
        q_list = list(image.keys())
        keypoints_list = result.get('keypoints_list', [])
        class_num_list = result.get('class_num_list', [])
        conf = result.get('confs', [])
        
        trans_single_npy = []
        
        for q_idx, q_name in enumerate(q_list):
            image_q = image[q_name]
            x = image_q[0]
            y = image_q[1]
            value = image_q[2]
            
            # 构建数据列表
            data_list = []
            for y_idx, y_val in enumerate(y):
                for x_idx, x_val in enumerate(x):
                    # 获取对应位置的value值
                    val = value[y_idx, x_idx]
                    # 添加[x坐标, y坐标, value值]到数据列表
                    data_list.append([x_val.item(), y_val.item(), val.item()])
            
            # 构建标签列表
            label_list = []
            current_keypoints = keypoints_list[q_idx]
            current_classes = class_num_list[q_idx] if q_idx < len(class_num_list) else []
            current_confs = conf[q_idx] if q_idx < len(conf) else []
            
            label_item = {
                "class": current_classes,
                "conf": current_confs,
                "key_point": current_keypoints
            }
            label_list.append(label_item)

            
            # 添加单个通道数据
            trans_single_npy.append({
                "data": data_list,
                "label": label_list
            })
        
        # 添加单个npy文件的所有通道数据
        trans_all_npy.append(trans_single_npy)
    
    return trans_all_npy


def main():
    from config import API_URL, API_KEY
    base_dir = "./tmp/powershift"
    file_names = os.listdir(base_dir)
    file_path_list = []
    for file_name in file_names:
        if file_name.endswith('.npy'):
            file_path = os.path.join(base_dir, file_name)
            file_path_list.append(file_path)
    if len(file_path_list) == 0:
        return
    
    dict_list = []
    for file_path in file_path_list:
        content = load_npy_file(file_path)
        dict_list.append(content)
    
    trans_all_npy = transform_powershift_npy_and_processed_data(API_URL, API_KEY, dict_list)# trans_all_npy的数据格式参考format_powershift.json
    

if __name__ == "__main__":
    main()