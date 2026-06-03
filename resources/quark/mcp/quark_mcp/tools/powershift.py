# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/09 16:45:38
#########################################################################



from qubitctrl.task.quark import call_interface
# from ..templates import powershift as powershift_template
from quark_templates import powershift as powershift_template


def powershift(qubits: list[str],
               power,
               freq,
               plot: bool = True,
               *args, **kwargs
               ):

    tid = call_interface(workflow=powershift_template,
                        qubits=qubits,
                        power=power,
                        freq=freq,
                        *args, **kwargs
                        )
    return tid