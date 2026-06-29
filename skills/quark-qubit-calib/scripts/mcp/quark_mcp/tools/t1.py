# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/02/10 10:36:18
#########################################################################



from qubitctrl.task.quark import call_interface
# from ..templates import t1_1d as t1_1d_template
from quark_templates import t1_1d as t1_1d_template


def t1(qubits: list[str],
          delay,
          signal: str = "population",
          plot: bool = True,
          *args, **kwargs
          ):
    tid = call_interface(workflow=t1_1d_template,
                        qubits=qubits,
                        delay=delay,
                        signal=signal,
                        plot=plot,
                        *args, **kwargs
                        )
    return tid