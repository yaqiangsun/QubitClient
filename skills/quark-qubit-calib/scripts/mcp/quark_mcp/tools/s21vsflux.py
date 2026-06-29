# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/09 17:04:25
#########################################################################



from qubitctrl.task.quark import call_interface
# from ..templates import S21vsflux_scan
from quark_templates import S21vsflux_scan


def s21vsflux(
              qubits_scan: list[str],
              qubits_read: list[str] = None,
                freq: list = None,
                read_bias: list = None,
                plot: bool = True,
                *args, **kwargs
                   ):
    if qubits_read is None:
        qubits_read = qubits_scan
    if qubits_scan is None:
        qubits_scan = qubits

    tid = call_interface(workflow=S21vsflux_scan,
                        qubits=qubits_scan,
                        qubits_read=qubits_read,
                        qubits_scan=qubits_scan,
                        freq=freq,
                        read_bias=read_bias,
                        plot=plot,
                        *args, **kwargs)
    return tid