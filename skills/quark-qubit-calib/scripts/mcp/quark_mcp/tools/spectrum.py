# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/10 10:32:47
#########################################################################



from qubitctrl.task.quark import call_interface
# from ..templates import spectrum as spectrum_template
from quark_templates import spectrum as spectrum_template


def spectrum(qubits: list[str],
             freq,
             drive_amp: float = 0.5,
             duration: float = 100e-9,
             from_idle: bool = True,
             absolute: bool = True,
             signal: str = 'population',
             build_dependencies: bool = False,
             plot: bool = True,
             *args, **kwargs
             ):
    tid = call_interface(workflow=spectrum_template,
                        qubits=qubits,
                        freq=freq,
                        drive_amp=drive_amp,
                        duration=duration,
                        from_idle=from_idle,
                        absolute=absolute,
                        signal=signal,
                        build_dependencies=build_dependencies,
                        *args, **kwargs
                        )
    return tid