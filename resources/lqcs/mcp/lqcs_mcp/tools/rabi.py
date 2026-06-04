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


def rabi(qubits:list[str]=['Q0','Q1'],
         amp_start:float=0,
         amp_end:float=2,
         amp_sample_num:int=16):
    
    qubit = eval(qubits[0])

    sample_rate = (amp_end - amp_start) / amp_sample_num
    amp_array=np.arange(amp_start, amp_end, sample_rate)
    result = sq.piamp(qubit, fc=None, amp=amp_array, update=False)
    
    return result