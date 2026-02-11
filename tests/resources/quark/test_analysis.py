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

def main(task_key="pi"):
    base_dir = "tmp/data"
    for pkl_path in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, pkl_path)
        result = get_pkl_content(pkl_path)
        if result is None:
            continue
        if "meta" not in result.keys():
            continue
        if "name" not in result["meta"].keys():
            continue
        if task_key.lower() in result["meta"]["name"].lower():
            if len(result["meta"]["other"]["qubits"])>1:
                if task_key in "opt_pipulse":
                    optpipulse(result)

if __name__ == "__main__":
    main()