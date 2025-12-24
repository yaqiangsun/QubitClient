# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/06/06 16:52:53
########################################################################


from enum import Enum

class CurveType(str, Enum):
    COSINE = "cosin"
    POLY = "poly"
    AUTO = "auto"