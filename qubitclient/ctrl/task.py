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
    DRAG = "drag"
    DELTA = "delta"
    OPT_PIPULSE = "opt_pipulse"
    POWERSHIFT = "powershift"
    RABI = "rabi"
    RAMSEY = "ramsey"
    S21VSFLUX = "s21vsflux"
    SINGLESHOT = "singleshot"
    SPECTRUM = "spectrum"
    SPECTRUM_2D = "spectrum_2d"
    T1 = "t1"


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

@task_register
def drag(qubits:list[str], lamb:list[float], stage:int=1, N_repeat:int=1, pulsePair:list[int]=[0, 1], *args, **kwargs):
    result = call_mcp("drag",
                      qubits=qubits,
                      lamb=lamb,
                      stage=stage,
                      N_repeat=N_repeat,
                      pulsePair=pulsePair
                      )
    return result
@task_register
def delta(qubits:list[str], stage:int=1, *args, **kwargs):
    result = call_mcp("delta",
                      qubits=qubits,
                      stage=stage
                      )
    return result
@task_register
def opt_pipulse(qubits:list[str], stage:int=1, *args, **kwargs):
    result = call_mcp("opt_pipulse",
                      qubits=qubits,
                      stage=stage
                      )
    return result

@task_register
def powershift(qubits:list[str], power:list[float], freq:list[float], *args, **kwargs):
    result = call_mcp("powershift",
                      qubits=qubits,
                      power=power,
                      freq=freq
                      )
    return result

@task_register
def rabi(qubits:list[str], drive_amp:list[float], width:float=30e-9, *args, **kwargs):
    result = call_mcp("rabi",
                      qubits=qubits,
                      drive_amp=drive_amp,
                      width=width
                      )
    return result

@task_register
def ramsey(qubits:list[str], delta:float=20e6, delay:float=10e-6, stage:int=1, scale:int=15, *args, **kwargs):
    result = call_mcp("ramsey",
                      qubits=qubits,
                      delta=delta,
                      delay=delay,
                      stage=stage,
                      scale=scale
                      )
    return result

@task_register
def s21vsflux(qubits_scan:list[str], read_bias:list[float], freq:list[float], qubits_read:list[str], *args, **kwargs):
    result = call_mcp("s21vsflux",
                      qubits_scan=qubits_scan,
                      read_bias=read_bias,
                      freq=freq,
                      qubits_read=qubits_read
                      )
    return result

@task_register
def singleshot(qubits:list[str], stage:int=1, *args, **kwargs):
    result = call_mcp("singleshot",
                      qubits=qubits,
                      stage=stage
                      )
    return result

@task_register
def spectrum(qubits:list[str], freq:list[float], drive_amp:float=0.04, duration:float=40e-6, 
             from_idle:bool=True, absolute:bool=True, signal:str="iq_avg", build_dependencies:bool=False, *args, **kwargs):
    result = call_mcp("spectrum",
                      qubits=qubits,
                      freq=freq,
                      drive_amp=drive_amp,
                      duration=duration,
                      from_idle=from_idle,
                      absolute=absolute,
                      signal=signal,
                      build_dependencies=build_dependencies
                      )
    return result

@task_register
def spectrum_2d(qubits:list[str], drive_amp:float=0.05, duration:float=40e-6, freq:list[float]=None, 
                bias:list[float]=None, from_idle:bool=False, absolute:bool=True, *args, **kwargs):
    result = call_mcp("spectrum_2d",
                      qubits=qubits,
                      drive_amp=drive_amp,
                      duration=duration,
                      freq=freq,
                      bias=bias,
                      from_idle=from_idle,
                      absolute=absolute
                      )
    return result

@task_register
def t1(qubits:list[str], delay:list[float], *args, **kwargs):
    result = call_mcp("t1",
                      qubits=qubits,
                      delay=delay
                      )
    return result