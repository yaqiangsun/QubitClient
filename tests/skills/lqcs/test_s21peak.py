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

from resources.lqcs.analysis.utils import get_hdf5_content
from resources.lqcs.analysis.inception import s21
from resources.lqcs.analysis.visualization import plot_s21
import matplotlib.pyplot as plt


def test_s21peak(task_key, base_dir):
    for hdf5_path in os.listdir(base_dir):
        hdf5_path = os.path.join(base_dir, hdf5_path)
        
        # 提取文件名前缀
        pure_name = os.path.splitext(os.path.basename(hdf5_path))[0]
        
        data = get_hdf5_content(hdf5_path)

        if task_key in "s21peak":
            analysis_result = s21(data)
            fig_list = plot_s21(data, analysis_result, save_path=f'./tmp/vis/s21_{pure_name}.png')
            # fig_list[0].show()
            # plt.show(block=True)


def main():
    task_key = "s21peak"
    base_dir = "tmp/data/s21peak"
    test_s21peak(task_key, base_dir)


if __name__ == "__main__":
    main()
