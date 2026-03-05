# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/11 11:48:16
########################################################################

import os
import sys
import logging

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from resources.quark.anaylsis.utils import get_pkl_content
from resources.quark.anaylsis.inception import t1fit
from resources.quark.anaylsis.visualization import plot_t1fit
import matplotlib.pyplot as plt


def test_t1fit(task_key, base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if "t1" in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"]) >= 1:
                if task_key in ["t1fit", "t1"]:
                    print(f"正在测试 t1fit 文件：{pkl_path}")
                    analysis_result = t1fit(data)
                    #print("第一个 qubit 的 results 示例：", analysis_result.get("results", [{}])[0])                                        
                    fig_list = plot_t1fit(data, analysis_result, save_path='./tmp/vis/t1fit.png')
                    # if fig_list and len(fig_list) > 0:
                    #     fig_list[0].show()
                    # plt.show(block=True)


def main():
    task_key = "t1"
    base_dir = "./tmp/data/t1"
    test_t1fit(task_key, base_dir)


if __name__ == "__main__":
    main()
