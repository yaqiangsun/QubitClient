# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/11 11:08:00
########################################################################

import os
import pickle
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
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
def main(task_key="Opt"):
    for pkl_path in os.listdir("tmp/rid"):
        pkl_path = os.path.join("tmp/rid", pkl_path)
        result = get_pkl_content(pkl_path)
        if result is None:
            continue
        if "meta" not in result.keys():
            continue
        if "name" not in result["meta"].keys():
            continue
        if task_key.lower() in result["meta"]["name"].lower():
            if len(result["meta"]["other"]["qubits"])>1:
                from resources.quark.anaylsis.format import optpipulse_convert
                formated_result = optpipulse_convert(result)
    pass
if __name__ == "__main__":
    main(task_key="opt")