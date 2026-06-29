# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/01/26 13:39:45
########################################################################

from qubitctrl.task.quark import call_interface
# from ..templates import S21_template
from quark_templates import rb_1q


import numpy as np


def rb(qubits: list[str],
       couplers: tuple = tuple([]),
       stage: int = 3,
       base=None,
       gate=[
           'ref',
           [('Y/2', 0)],
           [('I', 0)],
           [('X', 0)],
           [('X/2', 0)],
           [('Y', 0)],
       ][:1],
       cycle=np.unique(np.logspace(0, np.log10(1000), 21, dtype=int)),
       size: int = 11,
       plot=True,
       *args, **kwargs
       ):
    tid = call_interface(workflow=rb_1q,
                         qubits=qubits,
                         couplers=couplers,
                         stage=stage,
                         base=base,
                         gate=gate,
                         cycle=cycle,
                         size=size,
                         *args, **kwargs
                         )
    return tid