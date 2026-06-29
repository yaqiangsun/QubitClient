# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/10 10:24:46
#########################################################################



from qubitctrl.task.quark import call_interface
# from ..templates import singleshot_template
from quark_templates import singleshot_template


def singleshot(qubits: list[str],
               stage: int = 1,
               plot: bool = True,
               *args, **kwargs
               ):

    tid = call_interface(workflow=singleshot_template,
                        qubits=qubits,
                        stage=stage,
                        *args, **kwargs
                        )
    return tid