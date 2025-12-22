# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/04/11 17:58:29
########################################################################

import os
import numpy as np



def load_npy_file(file_path):
    try:
        array = np.load(file_path, allow_pickle=True)
        return array
    except Exception as e:
        raise ValueError(f"加载文件 {file_path} 时出错: {str(e)}")