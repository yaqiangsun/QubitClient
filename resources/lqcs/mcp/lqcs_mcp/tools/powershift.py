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


def powershift(qubits:list[str]=['Q0','Q1'],
               frequency_center=6.539,
               frequency_half_bandwidth=0.0015,
               frequency_sample_num=16,
               power_start=-40,
               power_end=-16,
               power_sample_num=13,
               ):
    qubit = eval(qubits[0])

    frequency_start = frequency_center - frequency_half_bandwidth
    frequency_end = frequency_center + frequency_half_bandwidth
    

   

    freq = np.linspace(frequency_start, frequency_end, frequency_sample_num)
    power = np.linspace(power_start, power_end, power_sample_num)



    result = sq.s21_power2d(qubit, freq=freq, power=power,update=False)
    
    return result