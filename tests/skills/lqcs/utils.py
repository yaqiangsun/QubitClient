# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/11 11:54:18
########################################################################

import os
import numpy as np
import pickle
import logging
import h5py
import numpy as np

def get_hdf5_content(hdf5_file_path):
    """
    读取你的hdf5文件（包含上述复杂结构）
    """
    print(hdf5_file_path)
    abs_path = os.path.abspath(hdf5_file_path)
    result = {}
    if not os.path.exists(abs_path):
        print(f"❌ hdf5文件不存在：{abs_path}")
        return None
    with h5py.File(hdf5_file_path, 'r') as f:
       

        # 主数据
        dv = f['DataVault']
        title = dv.attrs.get('Title', '').split(':')[0]
        

        if isinstance(dv, h5py.Dataset):
            data = dv[()]  # 获取所有数据

            result[title]=data
            return result


def get_pkl_content(pkl_file_path):
    """
    读取你的PKL文件（包含上述复杂结构）
    """
    abs_path = os.path.abspath(pkl_file_path)
    if not os.path.exists(abs_path):
        print(f"❌ PKL文件不存在：{abs_path}")
        return None
    
    print(f"📌 读取PKL文件：{os.path.basename(abs_path)}")
    try:
        with open(abs_path, 'rb') as f:
            result = pickle.load(f)
        print("✅ PKL文件读取成功，数据结构包含：", list(result.keys()))
        return result
    except Exception as e:
        print(f"❌ 读取失败：{str(e)}")
        return None

