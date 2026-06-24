# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/09 17:04:25
#########################################################################



import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import numpy as np
from lqms.measure.tuners import sq_nodes as sq

from backend import s
from lqms.measure import (
    generate_coupler,
    generate_qubit,
)
_all_qubits = generate_qubit(globals(), info=None, sample=s)
_all_couplers = generate_coupler(globals(), info=None, sample=s)


def s21vsflux(qubits:list[str],
              freq_center:float,
              freq_half_bandwidth:float,
              freq_sample_num:int,
              read_bias_start:float=-3,
              read_bias_end:float=3,
              read_bias_sample_num:int=16):
    freq_start = freq_center - freq_half_bandwidth
    freq_end = freq_center + freq_half_bandwidth
    

    freq_array = np.linspace(freq_start, freq_end, freq_sample_num)
    read_bias_array = np.linspace(read_bias_start, read_bias_end, read_bias_sample_num)

    qubit = eval(qubits[0])

    result = sq.s21_zpa2d(qubit, freq=freq_array, zpa=read_bias_array, freq_span=None, update=False)
    
    return result