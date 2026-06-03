# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/09 16:36:27
#########################################################################



from qubitctrl.task.quark import call_interface
# from ..templates import opt_delta as opt_delta_template
from quark_templates import opt_delta as opt_delta_template


def delta(qubits: list[str],
                N_list: list[int] | None = [1, 5, 13],
                delta_list: list[float] | None = None,
                stage: int = 1,
                delay: float = 20e-9,
                plot: bool = True,
                *args, **kwargs
                ):
    
    tid = call_interface(workflow=opt_delta_template,
                        qubits=qubits,
                        N_list=N_list,
                        delta_list=delta_list,
                        stage=stage,
                        delay=delay,
                        *args, **kwargs
                        )
    return tid