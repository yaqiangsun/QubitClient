# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/01/26 13:39:45
########################################################################



from qubitctrl.task.quark import call_interface
# from ..templates import S21_template
from quark_templates import S21_template


def s21(qubits:list[str],
        frequency_start:float=-40e6,
        frequency_end:float=40e6,
        frequency_sample_num:int=101,
        state: int | list[int] | None = [0],
        plot=True,
        *args, **kwargs
        ):
    tid = call_interface(workflow=S21_template,
                        qubits_use=qubits,
                        frequency_start=frequency_start,
                        frequency_end=frequency_end,
                        frequency_sample_num=frequency_sample_num,
                        state=state,
                        *args, **kwargs
                        )
    return tid