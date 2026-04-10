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

from resources.quark.analysis.utils import get_pkl_content
from resources.quark.analysis.inception import s21
from resources.quark.analysis.visualization import plot_s21
import matplotlib.pyplot as plt


def test_s21peak(task_key, base_dir):
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
        if task_key.lower() in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"]) >= 1:
                if task_key in "s21peak":
                    analysis_result = s21(data)
                    fig_list = plot_s21(data, analysis_result, save_path=f'./tmp/vis/s21_{pure_name}.png')
                    # fig_list[0].show()
                    # plt.show(block=True)


def main():
    task_key = "s21"
    base_dir = "tmp/data/s21"
    test_s21peak(task_key, base_dir)


if __name__ == "__main__":
    main()
