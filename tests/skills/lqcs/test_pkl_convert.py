# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/11 11:08:00
########################################################################

import os
import pickle
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../skills/lqcs-qubit-calib/scripts"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils import get_hdf5_content
from analysis.format import optpipulse_convert


def main(task_key="opt"):
    base_dir = "tmp/data"
    for hdf5_path in os.listdir(base_dir):
        hdf5_path = os.path.join(base_dir, hdf5_path)
        result = get_hdf5_content(hdf5_path)
        if result is None:
            continue
        if task_key.lower() in result.get("name", "").lower():
            if task_key in "opt_pipulse":
                formated_result = optpipulse_convert(result)
    pass
if __name__ == "__main__":
    main(task_key="opt")