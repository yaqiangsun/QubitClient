# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/03/26 15:50:15
########################################################################

import os
import numpy as np
import json
from qubitctrl import mcp
data_list = [
    # "tmp/data/s21_full_scan/14.pkl",
    # "tmp/data/s21_multi/1344.pkl"
    "tmp/data/s21/107.pkl",
    "tmp/data/s21vsamp/17.pkl",
    "tmp/data/powershift/18.pkl",
    "tmp/data/spectrum/22.pkl",
    "tmp/data/singleshot/SingleShot_7415662691861532672.pkl",
    "tmp/data/opt_pipulse/3921.pkl",
    "tmp/data/rabi/256.pkl",
    "tmp/data/ramsey/Ramsey_7415668616680837120.pkl",
    "tmp/data/t1/633.pkl",
    "tmp/data/delta/2313.pkl",
    "tmp/data/drag/2309.pkl",
    "tmp/data/RB/2314.pkl",
]
params = {}
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
    import pickle
    data_name = data_list[rid]
    print(data_name)
    with open(data_name, 'rb') as f:
        data = pickle.load(f)
    return convert_ndarray(data)
@mcp.tool
def update_param(key:str, value):
    """更新指定key的参数值"""
    # from qubitctrl.task.quark import update_param as update_quark_param
    # update_quark_param(key, value)
    params[key] = value
    return "success"
@mcp.tool
def query_param(key:str):
    """查询指定key的参数"""
    value = params[key] if key in params else None
    return value
@mcp.tool
def s21(qubits:list[str]=['Q0','Q1'],
        frequency_start:float=-40e6,
        frequency_end:float=40e6,
        frequency_sample_num:int=101,
        state: int | list[int] | None = [0],
        plot:bool=True,
        ):
    # 获取当前函数名
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    tid = tid[0]
    return tid  # 确保返回字符串类型

@mcp.tool
def rabi(qubits:list[str]=['Q0','Q1'],
         drive_amp:list[float]=[0.01, 0.1],
         width:float=30e-9,
         signal:str='iq_avg',
         ):

    # 获取当前函数名
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    tid = tid[0]
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def ramsey(qubits:list[str]=['Q0','Q2'],
           delta:float=20e6,
           delay:float=10e-6,
           stage:int=1,
           scale:int=15,
           signal:str='population',
           ):

    # 获取当前函数名
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    tid = tid[0]
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def t1(qubits:list[str]=['Q0','Q1'],
       delay:list[float]=[0, 100e-6],
       signal:str='population',
       ):

    # 获取当前函数名
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    tid = tid[0]
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def spectrum(qubits:list[str]=['Q0','Q1'],
             freq:list[float]=[-100e6, 100e6],
             drive_amp:float=0.5,
             duration:float=100e-9,
             from_idle:bool=True,
             absolute:bool=True,
             signal:str='population',
             build_dependencies:bool=False,
             ):
    # 获取当前函数名
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    tid = tid[0]
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def spectrum_2d(qubits:list[str]=['Q0','Q1'],
                drive_amp:float=0.5,
                duration:float=100e-9,
                freq:list[float]=[-100e6, 100e6],
                bias:list[float]=[-0.1, 0.1],
                from_idle:bool=False,
                absolute:bool=True,
                ):
    
    # 获取当前函数名
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    tid = tid[0]
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def s21vsflux(qubits_scan:list[str]=['Q0','Q1'],
              qubits_read:list[str]=None,
              freq:list[float]=None,
              read_bias:list[float]=None,
              ):
    
    # 获取当前函数名
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    if len(tid) == 0: return None
    tid = tid[0]
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def singleshot(qubits:list[str]=['Q0','Q1'],
               stage:int=1,
               ):
    
    # 获取当前函数名
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    tid = tid[0]
    return str(tid)  # 确保返回字符串类型
@mcp.tool
def drag(qubits:list[str]=['Q0','Q1'],
         lamb:list[float]=[-0.5, 0.5],
         stage:int=1,
         N_repeat:int=1,
         pulsePair:list[int]=[0, 1],
         signal:str='population',
         ):

    # 获取当前函数名
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    tid = tid[0]
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def opt_pipulse(qubits:list[str]=['Q0','Q1'],
                stage:int=1,
                N_list:list[int]=[1, 3, 5],
                amp_list:list[float]=None,
                signal:str='population',
                delay:float=20e-9,
                ):

    # 获取当前函数名
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    tid = tid[0]
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def powershift(qubits:list[str]=['Q0','Q1'],
               power:list[float]=[-20, 0],
               freq:list[float]=[-100e6, 100e6],
               ):
    
    # 获取当前函数名
    print(qubits)
    print(power)
    print(freq)
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    tid = tid[0]
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def delta(qubits:list[str]=['Q0','Q1'],
          N_list:list[int]=[1, 5, 13],
          delta_list:list[float]=None,
          stage:int=1,
          delay:float=20e-9,
          ):

    # 获取当前函数名
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    tid = tid[0]
    return str(tid)  # 确保返回字符串类型

@mcp.tool
def rb(qubits:list[str],
          couplers:tuple=tuple([]),
          stage:int=3,
          gate:list=['ref'],
          cycle:list=None,
          size:int=11,
          plot:bool=True,
          ):

    # 获取当前函数名
    import inspect
    func_name = inspect.currentframe().f_code.co_name   # 得到 's21'
    # 小写化
    func_name = func_name.lower()
    # 如果名字在data_list中的某个元素，获取这个元素的索引
    tid = [i for i, name in enumerate(data_list) if func_name in name.lower()]
    tid = tid[0]
    return str(tid)  # 确保返回字符串类型