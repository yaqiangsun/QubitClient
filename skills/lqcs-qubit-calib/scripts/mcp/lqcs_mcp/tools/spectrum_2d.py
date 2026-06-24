# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/10 10:28:21
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


def spectrum_2d(qubits:list[str]=['Q0','Q1'],
             freq_start:float=-3,
             freq_end:float=3,
             freq_sample_num:int=200,
             zpa_start=-1,
             zpa_end=0,
             zpa_sample_num=100,
             spec_amp:float=0.0,
             sb_freq:float=0):

    qubit = eval(qubits[0])
    freq_array = np.linspace(freq_start, freq_end, freq_sample_num)
    zpa_array = np.linspace(zpa_start, zpa_end, zpa_sample_num)

    result = sq.spectroscopy(qubit, freq=freq_array, zpa=zpa_array, spec_amp=spec_amp, sb_freq=sb_freq,update=False)
    
    return  