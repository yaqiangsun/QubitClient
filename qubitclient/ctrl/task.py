# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/06 18:09:15
########################################################################


from qubitclient.ctrl import MCPClient

def call_mcp(task_type:str,*args,**kwargs):
    mcp = MCPClient(mcpServers=None)
    result = mcp.call(task_type,*args,**kwargs)
    return result

DEFINED_TASKS = {}
def task_register(func):
    DEFINED_TASKS[func.__name__.lower()] = func
    return func


from enum import Enum, unique
@unique
class CtrlTaskName(Enum):
    S21 = "s21"


def run_task(task_type,*args,**kwargs):
    response = DEFINED_TASKS[task_type.value](*args,**kwargs)
    return response



@task_register
def s21(qubits_use:list[str],
        frequency_start=-40e6,frequency_end=40e6,frequency_sample_num=101,*args,**kwargs):
    result = call_mcp("s21",
                      qubits_use=qubits_use,
                      frequency_start=frequency_start,
                      frequency_end=frequency_end,
                      frequency_sample_num=frequency_sample_num
                      )
    return result

