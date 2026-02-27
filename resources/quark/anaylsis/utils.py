# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/11 11:54:18
########################################################################

import os
import pickle
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

def update_param(key:str, value):
    from quark.app import s
    s.update(key, value)
def query_param(key:str):
    from quark.app import s
    return s.query(key)