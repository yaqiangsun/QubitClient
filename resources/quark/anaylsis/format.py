# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/11 10:39:49
########################################################################

import logging
import numpy as np

def optpipulse_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """

    # 初始化返回数据结构
    data_formated = {"image": {}}

    # 量子比特列表、AMP轴和Population原始数据提取
    qubit_name_list = [q.strip() for q in result["meta"]["other"]["qubits"] if q.strip()]
    x_array = np.array(result["meta"]["axis"]["amp"]["def"], dtype=np.float64)
    population_arr = np.array(result["data"]["population"], dtype=np.float64)
    
    # 遍历每个有效比特处理波形
    for index, qubit_name in enumerate(qubit_name_list):
        # 提取当前比特的所有波形：(n_waveforms, amp_points)
        waveforms = population_arr[:, :, index]      
        # 存入对应比特的波形数据
        data_formated["image"][qubit_name] = (waveforms, x_array)
    
    return data_formated