# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/10 10:28:21
#########################################################################



from qubitctrl.task.quark import call_interface
# from ..templates import spectrum_2d as spectrum_2d_template
from quark_templates import spectrum_2d as spectrum_2d_template


def spectrum_2d(qubits: list[str],
                drive_amp: float,
                duration: float,
                freq,
                bias,
                from_idle: bool = False,
                absolute: bool = True,
                plot: bool = True,
                *args, **kwargs
                ):

    tid = call_interface(workflow=spectrum_2d_template,
                        qubits=qubits,
                        drive_amp=drive_amp,
                        duration=duration,
                        freq=freq,
                        bias=bias,
                        from_idle=from_idle,
                        absolute=absolute,
                        *args, **kwargs
                        )
    return tid