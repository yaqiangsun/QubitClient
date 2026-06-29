# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/09 16:36:27
#########################################################################



from qubitctrl.task.quark import call_interface
# from ..templates import opt_pipulse as opt_pipulse_template
from quark_templates import opt_pipulse as opt_pipulse_template


def opt_pipulse(qubits: list[str],
                stage: int = 1,
                N_list: list[int] | None = [1, 3, 5],
                amp_list: list[float] | None = None,
                signal: str = "population",
                delay: float = 20e-9,
                plot: bool = True,
                *args, **kwargs
                ):

    tid = call_interface(workflow=opt_pipulse_template,
                        qubits=qubits,
                        stage=stage,
                        N_list=N_list,
                        amp_list=amp_list,
                        signal=signal,
                        delay=delay,
                        *args, **kwargs
                        )
    return tid