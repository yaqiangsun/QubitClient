# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/01/26 13:39:45
#########################################################################



from qubitctrl.task.quark import call_interface
# from ..templates import allxy_drag
from quark_templates import allxy_drag


def drag(qubits: list[str],
         lamb,
         stage: int = 1,
         N_repeat: int = 1,
         pulsePair: list = None,
         signal: str = "population",
         plot: bool = True,
         *args, **kwargs
         ):
    if pulsePair is None:
        pulsePair = [0, 1]

    tid = call_interface(workflow=allxy_drag,
                        qubits=qubits,
                        stage=stage,
                        N_repeat=N_repeat,
                        pulsePair=pulsePair,
                        lamb=lamb,
                        signal=signal,
                        *args, **kwargs
                        )
    return tid