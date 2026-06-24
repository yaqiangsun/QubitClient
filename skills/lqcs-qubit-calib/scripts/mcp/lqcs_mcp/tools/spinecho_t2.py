# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/02/10 10:36:18
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


def spinecho_t2(qubits:list[str]=['Q0','Q1'],
        delay_start:float=0,
        delay_end:float=10000,
        delay_sample_num:int=200,
        fringeFreq:float=0.05,
        pipulse_num:float=None):
    
    delay_array = np.linspace(delay_start, delay_end, delay_sample_num).tolist()
    qubit = eval(qubits[0])

    result = sq.spinecho_t2(qubit, 
                    delay=delay_array,
                    fringeFreq=fringeFreq,
                    ms=pipulse_num,
                    update=False)
    
    return 