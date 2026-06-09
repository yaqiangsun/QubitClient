# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/03/26 15:50:15
########################################################################

import os
from  quark_mcp.tools import s21 as quark_s21
from  quark_mcp.tools import rabi as quark_rabi
from  quark_mcp.tools import ramsey as quark_ramsey
from  quark_mcp.tools import t1 as quark_t1
from  quark_mcp.tools import spectrum as quark_spectrum
from  quark_mcp.tools import spectrum_2d as quark_spectrum_2d
from  quark_mcp.tools import s21vsflux as quark_s21vsflux
from  quark_mcp.tools import singleshot as quark_singleshot
from  quark_mcp.tools import drag as quark_drag
from  quark_mcp.tools import opt_pipulse as quark_opt_pipulse
from  quark_mcp.tools import powershift as quark_powershift
from  quark_mcp.tools import delta as quark_delta
from  quark_mcp.tools import rb as quark_rb


from qubitctrl import mcp,suppress_stdout
from qubitctrl.task.quark import get_data as get_data_by_rid
import numpy as np
def convert_ndarray(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_ndarray(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_ndarray(i) for i in obj]
    else:
        return obj
@mcp.tool
def get_data(rid:int|str):
    from qubitctrl.task.quark import get_data as get_data_by_rid
    data = get_data_by_rid(rid)
    return convert_ndarray(data)
@mcp.tool
def update_param(key:str, value):
    """更新指定key的参数值"""
    from qubitctrl.task.quark import update_param as update_quark_param
    update_quark_param(key, value)
    return "success"
@mcp.tool
def query_param(key:str):
    """查询指定key的参数"""
    from qubitctrl.task.quark import query_param as query_quark_param
    value = query_quark_param(key)
    return value
@mcp.tool
def s21(
        qubits:list[str]=['Q0','Q1'],
        frequency_center=6.5,
        frequency_half_bandwidth=0.0005,
        frequency_sample_num=101,
        *args,**kwargs
        ):
    frequency_start = frequency_center - frequency_half_bandwidth
    frequency_end = frequency_center + frequency_half_bandwidth
    frequency_start=frequency_start*1e6
    frequency_end=frequency_end*1e6
    state: int | list[int] | None = [0]
    plot:bool=False
    if isinstance(state, int):
        state = [state]
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_s21(
                qubits=qubits,
                frequency_start=frequency_start,
                frequency_end=frequency_end,
                frequency_sample_num=frequency_sample_num,
                state=state,
                plot=plot
            )
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def rabi(qubits:list[str]=['Q0','Q1'],
         amp_start=0,
         amp_end=2,
         amp_sample_num=16,   
         *args, **kwargs
         ):
    drive_amp = np.linspace(amp_start, amp_end, amp_sample_num).tolist()
    width:float=30e-9
    signal:str='iq_avg'
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_rabi(
                qubits=qubits,
                drive_amp=drive_amp,
                width=width,
                signal=signal,
                plot=True
            )
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def ramsey(qubits:list[str]=['Q0','Q2'],
           delay_start=0,
           delay_end=100,
           delay_sample_num=100,
           *args, **kwargs):
    delta:float=20e6
    # delay:float=10e-6
    delay = np.linspace(delay_start, delay_end, delay_sample_num).tolist()
    delay = (np.array(delay) * 1e-9).tolist()
    stage:int=1
    scale:int=15
    signal:str='population'
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_ramsey(
                qubits=qubits,
                delta=delta,
                delay=delay,
                stage=stage,
                scale=scale,
                signal=signal,
                plot=True
            )
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def t1(qubits:list[str]=['Q0','Q1'],
       delay_start=0,
       delay_end=80000,
       delay_sample_num=17,
       *args, **kwargs):
    delay = np.linspace(delay_start, delay_end, delay_sample_num).tolist()
    delay = (np.array(delay) * 1e-9).tolist()
    signal:str='population'
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_t1(
                qubits=qubits,
                delay=delay,
                signal=signal,
                plot=True
            )
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def spectrum(qubits:list[str]=['Q0','Q1'],
             freq_start=-3,
             freq_end=3,
             freq_sample_num=200,
             bias=0,
             drive_amp=0.0,
             *args, **kwargs):    
    freq = np.linspace(freq_start, freq_end, freq_sample_num).tolist()
    freq = (np.array(freq) * 1e6).tolist()
    duration:float=100e-9
    from_idle:bool=True
    absolute:bool=True
    signal:str='population'
    build_dependencies:bool=False
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_spectrum(
                qubits=qubits,
                freq=freq,
                drive_amp=drive_amp,
                duration=duration,
                from_idle=from_idle,
                absolute=absolute,
                signal=signal,
                build_dependencies=build_dependencies,
                plot=True
            )
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def spectrum_2d(qubits:list[str]=['Q0','Q1'],
                freq_start=-3,
                freq_end=3,
                freq_sample_num=200,
                bias_start=-1,
                bias_end=1,
                bias_sample_num=100,
                drive_amp=0.0,
                *args, **kwargs):
    freq = np.linspace(freq_start, freq_end, freq_sample_num).tolist()
    freq = (np.array(freq) * 1e6).tolist()
    bias = np.linspace(bias_start, bias_end, bias_sample_num).tolist()
    duration:float=100e-9
    from_idle:bool=False
    absolute:bool=True
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_spectrum_2d(
                qubits=qubits,
                drive_amp=drive_amp,
                duration=duration,
                freq=freq,
                bias=bias,
                from_idle=from_idle,
                absolute=absolute,
                plot=True
            )
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def s21vsflux(qubits:list[str]=['Q0','Q1'],
              freq_center:float=6.5,
              freq_half_bandwidth:float=0.03,
              freq_sample_num:int=11,
              read_bias_start:float=-3,
              read_bias_end:float=3,
              read_bias_sample_num:int=16,
              *args, **kwargs):
    freq_start = freq_center-freq_half_bandwidth
    freq_end = freq_center+freq_half_bandwidth
    freq = np.linspace(freq_start, freq_end, freq_sample_num).tolist()
    freq = (np.array(freq) * 1e6).tolist()
    read_bias = np.linspace(read_bias_start, read_bias_end, read_bias_sample_num).tolist()
    qubits_scan=qubits
    qubits_read=qubits
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_s21vsflux(
                qubits_scan=qubits_scan,
                qubits_read=qubits_read,
                freq=freq,
                read_bias=read_bias,
                plot=True
            )
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def singleshot(qubits:list[str]=['Q0','Q1'],
               *args, **kwargs):
    stage:int=1
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_singleshot(
                qubits=qubits,
                stage=stage,
                plot=True
            )
    return str(tid)  # 确保返回字符串类型

@mcp.tool

def drag(qubits:list[str]=['Q0','Q1'],
         lamb:list[float]=[-0.5, 0.5],
         stage:int=1,
         N_repeat:int=1,
         pulsePair:list[int]=[0, 1],
         signal:str='population',
         *args, **kwargs):
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_drag(
                qubits=qubits,
                lamb=lamb,
                stage=stage,
                N_repeat=N_repeat,
                pulsePair=pulsePair,
                signal=signal,
                plot=True
            )
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def opt_pipulse(qubits:list[str]=['Q0','Q1'],
                N_list:list[int]=[1, 3, 5],
                amp_list:list[float]=None,
                *args, **kwargs):
    stage:int=1
    signal:str='population'
    delay:float=20e-9
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_opt_pipulse(
                qubits=qubits,
                stage=stage,
                N_list=N_list,
                amp_list=amp_list,
                signal=signal,
                delay=delay,
                plot=True
            )
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def powershift(qubits:list[str]=['Q0','Q1'],
               freq_center=6.539,
               freq_half_bandwidth=0.0015,
               freq_sample_num=16,
               power_start=-40,
               power_end=-16,
               power_sample_num=13,
               *args, **kwargs):
    freq_start = freq_center-freq_half_bandwidth
    freq_end = freq_center+freq_half_bandwidth
    freq = np.linspace(freq_start, freq_end, freq_sample_num).tolist()
    freq = (np.array(freq) * 1e6).tolist()
    power = np.linspace(power_start, power_end, power_sample_num).tolist()
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_powershift(
                qubits=qubits,
                power=power,
                freq=freq,
                plot=True
            )
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def delta(qubits:list[str]=['Q0','Q1'],
          N_list:list[int]=[1, 5, 13],
          delta_list:list[float]=None,
          stage:int=1,
          delay:float=20e-9,
          *args, **kwargs):
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_delta(
                qubits=qubits,
                N_list=N_list,
                delta_list=delta_list,
                stage=stage,
                delay=delay,
                plot=True
            )
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def rb(qubits:list[str],
          couplers:tuple=tuple([]),
          stage:int=3,
          gate:list=['ref'],
          cycle:list=None,
          size:int=11,
          plot:bool=True,
       *args, **kwargs):
    if gate is None:
        gate = [
            'ref',
            [('Y/2', 0)],
            [('I', 0)],
            [('X', 0)],
            [('X/2', 0)],
            [('Y', 0)],
        ][:1]
    if cycle is None:
        import numpy as np
        cycle = np.unique(np.logspace(0, np.log10(1000), 21, dtype=int)).tolist()
    # 使用上下文管理器抑制stdout输出，避免污染MCP协议通信
    with suppress_stdout():
        tid = quark_rb(
                qubits=qubits,
                couplers=couplers,
                stage=stage,
                gate=gate,
                cycle=cycle,
                size=size,
                plot=plot
            )
    return str(tid)  # 确保返回字符串类型