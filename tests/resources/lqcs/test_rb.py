# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/03/18
########################################################################

import os
import sys
import logging

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from resources.quark.analysis.utils import get_pkl_content
from resources.quark.analysis.inception import rb          # 假设已在 inception.py 中实现 rb 接口
from resources.quark.analysis.visualization import plot_rb  # 假设已在 visualization.py 中实现 plot_rb
import matplotlib.pyplot as plt


def test_rb(task_key, base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        
        # 提取文件名前缀
        pure_name = os.path.splitext(os.path.basename(pkl_path))[0]
        
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if "rb" in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"]) >= 1:
                if task_key in ["rb"]:
                    print(f"正在测试 rb 文件：{pkl_path}")
                    analysis_result = rb(data)
                    #print("第一个 qubit 的 results 示例：", analysis_result.get("results", [{}])[0])                                        
                    fig_list = plot_rb(data, analysis_result, save_path=f'./tmp/vis/rb_{pure_name}.png')
                    # if fig_list and len(fig_list) > 0:
                    #     fig_list[0].show()
                    # plt.show(block=True)

def main():
    task_key = "rb"
    base_dir = "./data/RB"
    test_rb(task_key, base_dir)


if __name__ == "__main__":
    main()