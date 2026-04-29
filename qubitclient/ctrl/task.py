# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/06 18:09:15
########################################################################

import numpy as np
from qubitclient.ctrl import MCPClient
import json

def call_mcp(task_type:str,*args,**kwargs):
    mcp = MCPClient(mcpServers=None)
    result = mcp.call(task_type,*args,**kwargs)
    try:
        result = json.loads(result)
    except Exception as e:
        pass
    return result

DEFINED_TASKS = {}
def task_register(func):
    DEFINED_TASKS[func.__name__.lower()] = func
    return func


from enum import Enum, unique
@unique
class CtrlTaskName(Enum):
    S21 = "s21"
    S21MULTI = "s21multi"
    DRAG = "drag"
    DELTA = "delta"
    OPTPIPULSE = "opt_pipulse"
    POWERSHIFT = "powershift"
    RABI = "rabi"
    RAMSEY = "ramsey"
    S21VSFLUX = "s21vsflux"
    SINGLESHOT = "singleshot"
    SPECTRUM = "spectrum"
    SPECTRUM_2D = "spectrum_2d"
    T1 = "t1"
    T2 = "t2"
    RB = "rb"
    DATA = "get_data"
    QUERY_PARAM = "query_param"
    UPDATE_PARAM = "update_param"
    XEB = 'xeb'


def run_task(task_type,*args,**kwargs):
    if not isinstance(task_type, str):
        task_type = task_type.value
    response = DEFINED_TASKS[task_type](*args,**kwargs)
    return response



@task_register
def s21(qubits:list[str],
        frequency_start=-40e6,
        frequency_end=40e6,
        frequency_sample_num=101,
        state: int | list[int] | None = [0],
        *args,**kwargs):
    if isinstance(state, int):
        state = [state]
    result = call_mcp("s21",
                      qubits=qubits,
                      frequency_start=frequency_start,
                      frequency_end=frequency_end,
                      frequency_sample_num=frequency_sample_num,
                      state=state
                      )
    return result
@task_register
def s21multi(qubits:list[str],
        frequency_start=-40e6,
        frequency_end=40e6,
        frequency_sample_num=101,
        state: int | list[int] | None = [0],
        *args,**kwargs):
    if isinstance(state, int):
        state = [state]
    result = call_mcp("s21",
                      qubits=qubits,
                      frequency_start=frequency_start,
                      frequency_end=frequency_end,
                      frequency_sample_num=frequency_sample_num,
                      state=state
                      )
    return result
@task_register
def drag(qubits:list[str],
         lamb:list[float],
         stage:int=1,
         N_repeat:int=1,
         pulsePair:list[int]=[0, 1],
         signal: str = "population",
         *args, **kwargs):
    result = call_mcp("drag",
                      qubits=qubits,
                      lamb=lamb,
                      stage=stage,
                      N_repeat=N_repeat,
                      pulsePair=pulsePair,
                      signal=signal
                      )
    return result
@task_register
def delta(qubits:list[str],
          N_list: list[int] | None = [1, 5, 13],
          delta_list: list[float] | None = None,
          stage:int=1,
          delay: float = 20e-9,
          *args, **kwargs):
    if delta_list is None:
        delta_list = (np.linspace(-20, 20, 101) * 1e6).tolist()

    result = call_mcp("delta",
                      qubits=qubits,
                      stage=stage,
                      delay=delay,
                      N_list=N_list,
                      delta_list=delta_list
                      )
    return result
@task_register
def opt_pipulse(qubits:list[str],
                stage:int=1,
                N_list: list[int] | None = [1, 3, 5],
                amp_list: list[float] | None = None,
                signal: str = "population",
                delay: float = 20e-9,
                *args, **kwargs):
    if amp_list is None:
        amp_list = np.linspace(0.5, 1.5, 51).tolist()
    result = call_mcp("opt_pipulse",
                      qubits=qubits,
                      stage=stage,
                      N_list=N_list,
                      amp_list=amp_list,
                      delay=delay,
                      signal=signal
                      )
    return result

@task_register
def powershift(qubits:list[str],
               power:list[float],
               freq:list[float],
               *args, **kwargs):
    result = call_mcp("powershift",
                      qubits=qubits,
                      power=power,
                      freq=freq
                      )
    return result

@task_register
def rabi(qubits:list[str],
         drive_amp:list[float],
         width:float=30e-9,
         signal: str = "iq_avg",
         *args, **kwargs):
    result = call_mcp("rabi",
                      qubits=qubits,
                      drive_amp=drive_amp,
                      width=width,
                      signal=signal
                      )
    return result

@task_register
def ramsey(qubits:list[str],
           delta:float=20e6,
           delay:float=10e-6,
           stage:int=1,
           scale:int=15,
           signal: str = "population",
           *args, **kwargs):
    result = call_mcp("ramsey",
                      qubits=qubits,
                      delta=delta,
                      delay=delay,
                      stage=stage,
                      scale=scale,
                      signal=signal
                      )
    return result

@task_register
def s21vsflux(qubits_scan:list[str],
              read_bias:list[float],
              freq:list[float],
              qubits_read:list[str],
              *args, **kwargs):
    result = call_mcp("s21vsflux",
                      qubits_scan=qubits_scan,
                      read_bias=read_bias,
                      freq=freq,
                      qubits_read=qubits_read
                      )
    return result

@task_register
def singleshot(qubits:list[str],
               stage:int=1,
               *args, **kwargs):
    result = call_mcp("singleshot",
                      qubits=qubits,
                      stage=stage
                      )
    return result

@task_register
def spectrum(qubits:list[str],
             freq:list[float],
             drive_amp:float=0.04,
             duration:float=40e-6, 
             from_idle:bool=True,
             absolute:bool=True,
             signal:str="iq_avg",
             build_dependencies:bool=False,
             *args, **kwargs):
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
def spectrum_2d(qubits:list[str],
                drive_amp:float=0.05,
                duration:float=40e-6,
                freq:list[float]=None, 
                bias:list[float]=None,
                from_idle:bool=False,
                absolute:bool=True,
                *args, **kwargs):
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
def t1(qubits: list[str],
       delay:list[float],
       signal: str = "population",
       *args, **kwargs):
    result = call_mcp("t1",
                      qubits=qubits,
                      delay=delay,
                      signal=signal
                      )
    return result

@task_register
def t2(qubits: list[str],
       delay:list[float]=[0, 100e-6],
       fringe_freq:list[float]=[-100e6, 100e6],
       ms: float=0.1,
       *args, **kwargs):
    result = call_mcp("t2",
                      qubits=qubits,
                      delay=delay,
                      fringe_freq=fringe_freq,
                      ms=ms
                      )
    return result

@task_register
def rb(qubits:list[str],
       couplers:tuple=tuple([]),
       stage:int=3,
       gate:list=['ref'],
       cycle:list=None,
       size:int=11,
       *args, **kwargs):
    if cycle is None:
        cycle = np.unique(np.logspace(0, np.log10(1000), 21, dtype=int)).tolist()
    result = call_mcp("rb",
                      qubits=qubits,
                      couplers=couplers,
                      stage=stage,
                      gate=gate,
                      cycle=cycle,
                      size=size
                      )
    return result

@task_register
def xeb(qubits:list[str],
        m:int=3,
        k:int=3,
        gate:list=['ref'],
        tbuffer:list=None,
        stats:int=11,
        *args, **kwargs):
    if cycle is None:
        cycle = np.unique(np.logspace(0, np.log10(1000), 21, dtype=int)).tolist()
    result = call_mcp("xeb",
                      qubits=qubits,
                      m=m,
                      k=k,
                      gate=gate,
                      tbuffer=tbuffer,
                      stats=stats
                      )
    return result


@task_register
def get_data(rid,
       *args, **kwargs):
    result = call_mcp("get_data",
                      rid=rid
                      )
    return result

@task_register
def query_param(key,
       *args, **kwargs):
    result = call_mcp("query_param",
                      key=key
                      )
    return result
@task_register
def update_param(key,value,
       *args, **kwargs):
    result = call_mcp("update_param",
                      key=key,
                      value=value
                      )
    return result