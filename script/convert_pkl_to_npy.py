# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:50
########################################################################

import sys
sys.path.append("./")
from resources.quark.analysis.format import powershift_convert
from resources.quark.analysis.utils import get_pkl_content
import numpy as np

def convert(path):
    content = get_pkl_content(path)
    data = powershift_convert(content)
    npy_path = path.replace(".pkl", ".npy")
    np.save(npy_path,data)
if __name__ == "__main__":
    convert("tmp/data/powershift/955.pkl")
