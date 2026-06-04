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
from backend import s, info, generate_qubit, generate_coupler

import numpy as np


from lqms.measure.tuners import sq_nodes as sq

_all_qubits = generate_qubit(globals(), info=info, sample=s)
_all_couplers = generate_coupler(globals(), info=info, sample=s)


def t1(qubits:list[str]=['Q0','Q1'],
       zpa_start:float=-1.0,
       zpa_end:float=0.4,
       zpa_sample_num:int=71,
       delay_start:float=0,
       delay_end:float=80000,
       delay_sample_num:int=17):




    zpa_sample_rate = (zpa_end - zpa_start) / zpa_sample_num
    zpa_array=np.arange(zpa_start, zpa_end, zpa_sample_rate)


    delay_sample_rate = (delay_end - delay_start) / delay_sample_num
    delay_array=np.arange(delay_start, delay_end, delay_sample_rate)
    qubit = eval(qubits[0])

    result = sq.t1(qubit, 
                   zpa=zpa_array,
                   delay=delay_array,
                   update=False)
    
    return result