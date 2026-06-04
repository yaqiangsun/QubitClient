# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/01/26 13:39:45
########################################################################


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from backend import s, info, generate_qubit, generate_coupler

import numpy as np


from lqms.measure.tuners import sq_nodes as sq

_all_qubits = generate_qubit(globals(), info=info, sample=s)
_all_couplers = generate_coupler(globals(), info=info, sample=s)


def optqubitreadfreq(qubits:list[str]=['Q0','Q1'],
                     freq_span_center:float=6.390,
                     freq_span_half_bandwidth:float=0.0055,
                     freq_span_sample_num:int=40,
                     ):
    
    freq_start = freq_span_center - freq_span_half_bandwidth
    freq_end = freq_span_center + freq_span_half_bandwidth
    freq_array = np.linspace(freq_start, freq_end, freq_span_sample_num).tolist()
    qubit = eval(qubits[0])

    result = sq.opt_read_freq(qubit, freq=freq_array, update=False)
    
    return result