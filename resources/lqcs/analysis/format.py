# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/11 10:39:49
########################################################################

import logging
import numpy as np
import scipy



def singleshot_convert(result):
  


    data_formated = {"image": {}}

    for index, qubit_name in enumerate(result.keys()):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        data = result[qubit_name]
        if data.dtype.names:
           
            time = data['f0']  # 时间/索引
            I_channel = data['f1']  # Is | I
            Q_channel = data['f2']  # Qs | I
            X_channel = data['f3']  # Is | X
            Y_channel = data['f4']  # Qs | X
            s0 = I_channel + 1j * Q_channel  # 复数 s0 (I 通道)
            s1 = X_channel + 1j * Y_channel  # 复数 s1 (X 通道)
        data_formated["image"][qubit_name] = (s0, s1)
    return data_formated
