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

    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {
        "image": {
        }
    }
    for index,qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取AMP幅值轴x_array
        x_array = np.array(result["meta"]["axis"]["amp"]["def"], dtype=np.float64)
        assert x_array.ndim == 1, "AMP轴需为一维数组"
        amp_points = len(x_array)

        # 处理Population波形
        waveforms = np.array(result["data"]["population"][:,:,-1], dtype=np.float64)
                
        # 最终格式校验
        assert waveforms.ndim == 2, "waveforms需为(m, n)二维数组, m为波形数量"
        assert waveforms.shape[1] == amp_points, "waveforms点数需与AMP轴一致"
        assert x_array.ndim == 1 and len(x_array) == amp_points, "AMP轴格式错误"
    
        # 转换成所需的标准格式
        data_formated["image"][qubit_name] =  (waveforms, x_array)
    return data_formated