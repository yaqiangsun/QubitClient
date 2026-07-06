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

import numpy as np
from lqms.measure.tuners import sq_nodes as sq

from backend import s
from lqms.measure import (
    generate_coupler,
    generate_qubit,
)
_all_qubits = generate_qubit(globals(), info=None, sample=s)
_all_couplers = generate_coupler(globals(), info=None, sample=s)


def ramsey(qubits:list[str]=['Q0','Q2'],
           delay_start:float=0,
           delay_end:float=100,
           delay_sample_num:int=100,
           fringeFreq:float=0.05
           ):
    qubit = eval(qubits[0])
    delay_array = np.linspace(delay_start, delay_end, delay_sample_num)
    # result = sq.ramsey_df(qubit, 
    #                       delay=delay_array,
    #                       fringeFreq=fringeFreq,
    #                       update=False)
    result = sq.ramsey_df(qubit, 
                          update=False)
    
    return result