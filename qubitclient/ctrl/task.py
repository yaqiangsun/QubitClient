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
    RB = "rb"
    DATA = "get_data"
    QUERY_PARAM = "query_param"
    UPDATE_PARAM = "update_param"
    ########################################
    T1_2D = "t1_2d"
    SPINECH_T2 = "spinecho_t2"
    RAMSEY_T2 = "ramsey_t2"
    XEB = 'xeb'
    PIPULSEF10 = 'pipulsef10'
    OPTQUBITREADFREQ = 'optqubitreadfreq'
    TIMINGXYZ = 'timingxyz'
    PULSESHAPE = 'pulseshape'


def run_task(task_type,*args,**kwargs):
    if not isinstance(task_type, str):
        task_type = task_type.value
    response = DEFINED_TASKS[task_type](*args,**kwargs)
    return response

@task_register
def s21(qubits:list[str]=['Q0','Q1'],
        frequency_center=6.5,
        frequency_half_bandwidth=0.0005,
        frequency_sample_num=101,
        *args,**kwargs):
    result = call_mcp("s21",
                      qubits=qubits,
                      frequency_center=frequency_center,
                      frequency_half_bandwidth=frequency_half_bandwidth,
                      frequency_sample_num=frequency_sample_num
                      )
    return result

@task_register
def s21multi(qubits:list[str]=['Q0','Q1'],
        frequency_start:float=6.3,
        frequency_end:float=6.9,
        frequency_sample_rate=0.0001,
        *args,**kwargs):
    result = call_mcp("s21multi",
                      qubits=qubits,
                      frequency_start=frequency_start,
                      frequency_end=frequency_end,
                      frequency_sample_rate=frequency_sample_rate
                      )
    return result

@task_register
def drag(qubits:list[str]=['Q0','Q1'],
         lamb:list[float]=[-0.5, 0.5],
         stage:int=1,
         N_repeat:int=1,
         pulsePair:list[int]=[0, 1],
         signal:str='population',
         *args, **kwargs):
    result = call_mcp("drag",
                      qubits=qubits,
                      )
    return result

@task_register
def delta(qubits:list[str]=['Q0','Q1'],
          N_list:list[int]=[1, 5, 13],
          delta_list:list[float]=None,
          stage:int=1,
          delay:float=20e-9,
          *args, **kwargs):
    result = call_mcp("delta",
                      qubits=qubits,
                      )
    return result

@task_register
def opt_pipulse(qubits:list[str]=['Q0','Q1'],
                N_list:list[int]=[1, 3, 5],
                amp_list:list[float]=None,
                *args, **kwargs):
    
    result = call_mcp("opt_pipulse",
                      qubits=qubits,
                      N_list=N_list,
                      )
    return result


@task_register
def powershift(qubits:list[str]=['Q0','Q1'],
               freq_center=6.539,
               freq_half_bandwidth=0.0015,
               freq_sample_num=16,
               power_start=-40,
               power_end=-16,
               power_sample_num=13,
               *args, **kwargs):
    result = call_mcp("powershift",
                      qubits=qubits,
                      freq_center=freq_center,
                      freq_half_bandwidth=freq_half_bandwidth,
                      freq_sample_num=freq_sample_num,
                      power_start=power_start,
                      power_end=power_end,
                      power_sample_num=power_sample_num
                      )
    return result

@task_register
def rabi(qubits:list[str]=['Q0','Q1'],
         amp_start=0,
         amp_end=2,
         amp_sample_num=16,   
         *args, **kwargs):
    result = call_mcp("rabi",
                      qubits=qubits,
                      amp_start=amp_start,
                      amp_end=amp_end,
                      amp_sample_num=amp_sample_num)
    return result

@task_register
def ramsey(qubits:list[str]=['Q0','Q2'],
           delay_start=0,
           delay_end=100,
           delay_sample_num=100,
           *args, **kwargs):
    result = call_mcp("ramsey",
                      qubits=qubits,
                      delay_start=delay_start,
                      delay_end=delay_end,
                      delay_sample_num=delay_sample_num
                      )
    return result

@task_register
def s21vsflux(qubits:list[str]=['Q0','Q1'],
              freq_center:float=6.5,
              freq_half_bandwidth:float=0.03,
              freq_sample_num:int=11,
              read_bias_start:float=-3,
              read_bias_end:float=3,
              read_bias_sample_num:int=16,
              *args, **kwargs):
    result = call_mcp("s21vsflux",
                      qubits=qubits,
                      freq_center=freq_center,
                      freq_half_bandwidth=freq_half_bandwidth,
                      freq_sample_num=freq_sample_num,
                      read_bias_start=read_bias_start,
                      read_bias_end=read_bias_end,
                      read_bias_sample_num=read_bias_sample_num,
                      )
    return result

@task_register
def singleshot(qubits:list[str]=['Q0','Q1'],
               *args, **kwargs):
    result = call_mcp("singleshot",
                      qubits=qubits
                      )
    return result

@task_register
def spectrum(qubits:list[str]=['Q0','Q1'],
             freq_start=-3,
             freq_end=3,
             freq_sample_num=200,
             bias=0,
             drive_amp=0.0,
             *args, **kwargs):
    result = call_mcp("spectrum",
                      qubits=qubits,
                      freq_start=freq_start,
                      freq_end=freq_end,
                      freq_sample_num=freq_sample_num,
                      bias=bias,
                      drive_amp=drive_amp
                      )
    return result

@task_register
def spectrum_2d(qubits:list[str]=['Q0','Q1'],
                freq_start=-3,
                freq_end=3,
                freq_sample_num=200,
                bias_start=-1,
                bias_end=1,
                bias_sample_num=100,
                drive_amp=0.0,
                *args, **kwargs):
    result = call_mcp("spectrum_2d",
                      qubits=qubits,
                      freq_start=freq_start,
                      freq_end=freq_end,
                      freq_sample_num=freq_sample_num,
                      bias_start=bias_start,
                      bias_end=bias_end,
                      bias_sample_num=bias_sample_num,
                      drive_amp=drive_amp
                      )
    return result

@task_register
def t1_2d(qubits:list[str]=['Q0','Q1'],
       bias_start=-1.0,
       bias_end=0.4,
       bias_sample_num=71,
       delay_start=0,
       delay_end=80000,
       delay_sample_num=17,
       *args, **kwargs):
       result = call_mcp("t1",
                         qubits=qubits,
                         bias_start=bias_start,
                         bias_end=bias_end,
                         bias_sample_num=bias_sample_num,
                         delay_start=delay_start,
                         delay_end=delay_end,
                         delay_sample_num=delay_sample_num
                         )
       return result

def t1(qubits:list[str]=['Q0','Q1'],
       delay_start=0,
       delay_end=80000,
       delay_sample_num=17,
       *args, **kwargs):
       result = call_mcp("t1",
                         qubits=qubits,
                         delay_start=delay_start,
                         delay_end=delay_end,
                         delay_sample_num=delay_sample_num
                         )
       return result

@task_register
def spinecho_t2(qubits: list[str],
       delay_start=0,
       delay_end=10000,
       delay_sample_num=200,
       *args, **kwargs):
    result = call_mcp("spinecho_t2",
                      qubits=qubits,
                      delay_start=delay_start,
                      delay_end=delay_end,
                      delay_sample_num=delay_sample_num
                      )
    return result

@task_register
def ramsey_t2(qubits: list[str],
             delay_start=0,
             delay_end=10000,
             delay_sample_num=100,
             *args, **kwargs):
    result = call_mcp("ramsey_t2",
                      qubits=qubits,
                      delay_start=delay_start,
                      delay_end=delay_end,
                      delay_sample_num=delay_sample_num
                      )
    return result

@task_register
def rb(qubits:list[str],
       couplers:tuple=tuple([]),
       stage:int=3,
       gate:list=['ref'],
       cycle:list=None,
       size:int=11,
       plot:bool=True,
       *args, **kwargs):
    result = call_mcp("rb",
                    qubits=qubits,
                    couplers=couplers,
                    stage=stage,
                    gate=gate,
                    cycle=cycle,
                    size=size,
                    plot=plot
                    )
    return result

@task_register
def xeb(qubits:list[str],
        m_start=0,
        m_end=400,
        m_sample_num=10,
        k=30,
        gate='reference',
        tbuffer=0,
        stats=300,
        *args, **kwargs):
    result = call_mcp("xeb",
                      qubits=qubits,
                      m_start=m_start,
                      m_end=m_end,
                      m_sample_num=m_sample_num,
                      k=k,
                      gate=gate,
                      tbuffer=tbuffer,
                      stats=stats
                      )
    return result

@task_register
def pipulsef10(qubits:list[str],
               df_start=0,
               df_end=0.03,
               df_sample_num=21,
               *args, **kwargs):
    result = call_mcp("pipulsef10",
                      qubits=qubits,
                      df_start=df_start,
                      df_end=df_end,
                      df_sample_num=df_sample_num,
                      )
    return result

@task_register
def optqubitreadfreq(qubits:list[str],
                     freq_span_center,
                     freq_span_half_bandwidth=0.0055,
                     freq_span_sample_num=40,
                     *args, **kwargs):
    result = call_mcp("optqubitreadfreq",
                      qubits=qubits,
                      freq_span_center=freq_span_center,
                      freq_span_half_bandwidth=freq_span_half_bandwidth,
                      freq_span_sample_num=freq_span_sample_num,
                      )
    return result

@task_register
def timingxyz(qubits:list[str],
              delay_start=-60,
              delay_end=60,
              delay_sample_num=31,
              *args, **kwargs):
    result = call_mcp("timingxyz",
                      qubits=qubits,
                      delay_start=delay_start,
                      delay_end=delay_end,
                      delay_sample_num=delay_sample_num
                      )
    return result

@task_register
def pulseshape(qubits:list[str],
               step_height=0.2,
               *args, **kwargs):
    result = call_mcp("pulseshape",
                      qubits=qubits,
                      step_height=step_height
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
def query_param(qname, key,
       *args, **kwargs):
    result = call_mcp("query_param",
                      qname=qname,
                      key=key
                      )
    return result

@task_register
def update_param(qname, task_type, values,
       *args, **kwargs):
    result = call_mcp("update_param",
                      qname=qname,
                      task_type=task_type,
                      values=values
                      )
    return result