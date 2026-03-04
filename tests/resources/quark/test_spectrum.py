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
from resources.quark.anaylsis.inception import spectrum
from resources.quark.anaylsis.visualization import plot_spectrum
import matplotlib.pyplot as plt


def test_spectrum(task_key, base_dir):
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        print(f" print task_key: {task_key}, data name: {data['meta']['name']}")

        # 因为是拿 spectrum 数据来测 nnscope，所以 False
        # if task_key.lower() in data["meta"]["name"].lower():
        if "spectrum" in data["meta"]["name"].lower():
            if len(data["meta"]["other"].get("qubits", [])) >= 1:
                logging.info("task_key: %s, qubits: %s", task_key, data["meta"]["other"]["qubits"])
                if task_key in "spectrum":
                    analysis_result = spectrum(data)
                    logging.info(f"-----spectrum analysis result: {analysis_result}")
                    fig_list = plot_spectrum(data, analysis_result, save_path='./tmp/vis/spectrum.png')
                    fig_list[0].show()
                    plt.show(block=True)


def main():
    task_key = "spectrum"
    base_dir = "tmp/data/spectrum"
    test_spectrum(task_key, base_dir)


if __name__ == "__main__":
    main()
