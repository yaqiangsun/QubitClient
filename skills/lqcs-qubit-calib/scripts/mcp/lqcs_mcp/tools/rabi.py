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

import numpy as np
from lqms.measure.tuners import sq_nodes as sq

from backend import s
from lqms.measure import (
    generate_coupler,
    generate_qubit,
)
_all_qubits = generate_qubit(globals(), info=None, sample=s)
_all_couplers = generate_coupler(globals(), info=None, sample=s)


def rabi(qubits:list[str]=['Q0','Q1'],
         piamp_start:float=0,
         piamp_end:float=2,
         piamp_sample_num:int=16,
         pi_len: float=50.0):
    
    qubit = eval(qubits[0])

    # sample_rate = (amp_end - amp_start) / amp_sample_num
    piamp_array = np.linspace(piamp_start, piamp_end, piamp_sample_num)

    result = sq.piamp(qubit, fc=None, amp=piamp_array, update=False)

    return result