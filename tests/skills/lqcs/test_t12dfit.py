# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/02/11 11:48:16
########################################################################

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../skills/lqcs-qubit-calib/scripts"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils import get_hdf5_content
from analysis.inception import t12dfit
from analysis.visualization import plot_t12dfit


def test_t12dfit(task_key, base_dir):
    for filename in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, filename)
        
        # 提取文件名前缀
        pure_name = os.path.splitext(os.path.basename(pkl_path))[0]
        
        data = get_hdf5_content(pkl_path)
        if data is None:
            continue

        if task_key in ["t12dfit", "t12d"]:
            print(f"正在测试 t1fit 文件：{pkl_path}")
            analysis_result = t12dfit(data)
            fig_list = plot_t12dfit(data, analysis_result, save_path=f'./tmp/vis/t12dfit_{pure_name}.png')
            # if fig_list and len(fig_list) > 0:
            #     fig_list[0].show()


def main():
    task_key = "t12dfit"
    base_dir = "./tmp/data/t12d"
    test_t12dfit(task_key, base_dir)


if __name__ == "__main__":
    main()