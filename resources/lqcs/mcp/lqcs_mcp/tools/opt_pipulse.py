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


def opt_pipulse(qubits:list[str]=['Q0','Q1'],
               ms:list[int]=[1, 3, 5],
               gate:str='X',
               ):
    
    qubit = eval(qubits[0])

    result = sq.set_pi(qubit, ms=ms, gate=gate) # 无update,但会更新4个参数
    
    
    return result