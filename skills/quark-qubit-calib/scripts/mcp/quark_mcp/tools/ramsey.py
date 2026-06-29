# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/09 17:05:23
#########################################################################



from qubitctrl.task.quark import call_interface
# from ..templates import ramsey_template
from quark_templates import ramsey_template


def ramsey(qubits: list[str],
                    delta: float = 20e6,
                    delay: float = 10e-6,
                    stage: int = 1,
                    scale: int = 15,
                    signal: str = "population",
                    plot: bool = True,
                    *args, **kwargs
                    ):
    tid = call_interface(workflow=ramsey_template,
                        qubits=qubits,
                        stage=stage,
                        delta=delta,
                        delay=delay,
                        scale=scale,
                        signal=signal,
                        plot=plot,
                        *args, **kwargs
                        )
    return tid