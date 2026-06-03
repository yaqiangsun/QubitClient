# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/09 16:54:32
#########################################################################



from qubitctrl.task.quark import call_interface
# from ..templates import rabi_in_group
from quark_templates import rabi_in_group


def rabi(qubits: list[str],
                  drive_amp,
                  width: float = 30e-9,
                  signal: str = "iq_avg",
                  plot: bool = True,
                  *args, **kwargs
                  ):
    tid = call_interface(workflow=rabi_in_group,
                        qubits=qubits,
                        drive_amp=drive_amp,
                        width=width,
                        signal=signal,
                        plot=plot,
                        *args, **kwargs
                        )
    return tid