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

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../skills/lqcs-qubit-calib/scripts"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils import get_hdf5_content
from analysis.inception import rb
from analysis.visualization import plot_rb
import matplotlib.pyplot as plt


def test_rb(task_key, base_dir):
    for hdf5_path in os.listdir(base_dir):
        hdf5_path = os.path.join(base_dir, hdf5_path)

        # 提取文件名前缀
        pure_name = os.path.splitext(os.path.basename(hdf5_path))[0]

        data = get_hdf5_content(hdf5_path)
        if data is None:
            continue

        if "rb" in data.get("name", "").lower():
            if task_key in ["rb"]:
                print(f"正在测试 rb 文件：{hdf5_path}")
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