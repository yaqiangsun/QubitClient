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


def baseslope(qubits:list[str]=['Q0','Q1'],
         delay_start: float=1.0,
         delay_end:float = 100.0,
         delay_sample_num: float=50,
         step_height:float=0):
    
    qobj = eval(qubits[0])
    delay_array = np.linspace(delay_start, delay_end, delay_sample_num)
    qobj.set_piLen(1000, 1000)
    runner = bassex.PulseShapeFreq()

    runner(qobj, delay=delay_array, step_height=step_height)
    qobj.set_piLen(30,30)
    
    return None