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
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from resources.quark.anaylsis.utils import get_pkl_content
from resources.quark.anaylsis.inception import optpipulse
from resources.quark.anaylsis.visualization import plot_optpipulse

def main(task_key="pi"):
    base_dir = "tmp/data"
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
        if "meta" not in data.keys():
            continue
        if "name" not in data["meta"].keys():
            continue
        if task_key.lower() in data["meta"]["name"].lower():
            if len(data["meta"]["other"]["qubits"])>1:
                if task_key in "opt_pipulse":
                    analysis_result = optpipulse(data)
                    plot_optpipulse(data,analysis_result,save_path='./tmp/vis/opt_pipulse.png')

if __name__ == "__main__":
    main()