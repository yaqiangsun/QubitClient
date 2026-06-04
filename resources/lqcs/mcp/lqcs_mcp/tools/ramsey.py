# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/09 17:05:23
#########################################################################



import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from backend import s, info, generate_qubit, generate_coupler

import numpy as np


from lqms.measure.tuners import sq_nodes as sq

_all_qubits = generate_qubit(globals(), info=info, sample=s)
_all_couplers = generate_coupler(globals(), info=info, sample=s)


def ramsey(qubits:list[str]=['Q0','Q2'],
           delay_start:float=0,
           delay_end:float=100,
           delay_sample_num:int=100,
           fringeFreq:float=0.05
           ):
    qubit = eval(qubits[0])
    sample_rate = (delay_end - delay_start) / delay_sample_num
    delay_array=np.arange(delay_start, delay_end, sample_rate)
    result = sq.ramsey_df(qubit, 
                          delay=delay_array,
                          fringeFreq=fringeFreq,
                          update=False)
    
    return result