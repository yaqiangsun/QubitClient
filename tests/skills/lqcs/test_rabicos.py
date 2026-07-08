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

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../skills/lqcs-qubit-calib/scripts"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils import get_hdf5_content
from analysis.inception import rabi
from analysis.visualization import plot_rabicos
import matplotlib.pyplot as plt


def test_rabicos(task_key, base_dir):
    found_files = 0
    for filename in os.listdir(base_dir):
        if not filename.endswith('.hdf5'):
            continue
        hdf5_path = os.path.join(base_dir, filename)

        # 提取文件名前缀
        pure_name = os.path.splitext(os.path.basename(hdf5_path))[0]

        data = get_hdf5_content(hdf5_path)
        if data is None:
            continue

        if "rabi" in data.get("name", "").lower():
            found_files += 1
            print(f"正在测试 Rabi 文件 ({found_files}): {hdf5_path}")

            analysis_result = rabi(data)
            fig_list = plot_rabicos(data, analysis_result, save_path=f'./tmp/vis/rabicos_{pure_name}.png')
            # if fig_list and len(fig_list) > 0:
            #     fig_list[0].show()
            # plt.show(block=True)


def main():
    task_key = "rabi"
    base_dir = "tmp/data/rabi"
    test_rabicos(task_key, base_dir)


if __name__ == "__main__":
    main()
