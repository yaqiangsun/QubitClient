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


def xeb(qubits:list[str],
        m_start:int=0,
        m_end:int=400,
        m_sample_num:int=10,
        k:int=30,
        gate:str='reference',
        tbuffer:int=0,
        stats:int=300
        ):

    qubit = eval(qubits[0])
    m_array = np.linspace(m_start, m_end, m_sample_num).astype(int).tolist()

    result = sq.xeb(qubit, m=m_array, k=k, gate=gate, tbuffer=tbuffer, stats=stats,update=False)
    
    return result