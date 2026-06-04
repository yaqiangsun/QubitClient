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




def s21multi(qubits:list[str]=['Q0','Q1'],
        frequency_start:float=6.3,
        frequency_end:float=6.9,
        frequency_sample_rate:float=0.0001):
    qubit = eval(qubits[0])

    result = sq.s21(qubit, 
                    freq=np.arange(frequency_start, frequency_end, frequency_sample_rate),
                    update=False,
                    do_plot=False,
                    des='')
    
    return result
