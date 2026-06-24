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


def pipulsef10(qubits:list[str]=['Q0','Q1'],
               fc:float=None,
               df_start:float=0,
               df_end:float=0.03,
               df_sample_num:int=21,
               ):
    
    df_array = np.linspace(df_start, df_end, df_sample_num).tolist()
    qubit = eval(qubits[0])

    # result = sq.pidf(qubit, fc=fc, df=df_array, update=False)

    # 无fc
    result = sq.pidf(qubit, df=df_array, update=False)
    
    return result
