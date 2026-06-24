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


def pulseshape(qubits:list[str]=['Q0','Q1'],
               zpa_height:float=0.2,
               delay_start:float=0, 
               delay_end:float=1000, 
               delay_sample_num:float=100,
               z_offset_half_bandwidth:float=0.01, 
               z_offset_num:float=1.0
               ):
    
    qubit = eval(qubits[0])

    result = sq.pulse_shape(qubit, step_height=zpa_height, update=False) # 查下是否接受这些参数
    
    return result