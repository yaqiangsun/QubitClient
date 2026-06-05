# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/03/26 15:50:15
########################################################################

import os
from  lqcs_mcp.tools import s21 as lqcs_s21
from  lqcs_mcp.tools import s21mul as lqcs_s21mul
from  lqcs_mcp.tools import rabi as lqcs_rabi
from  lqcs_mcp.tools import ramsey as lqcs_ramsey
from  lqcs_mcp.tools import t1 as lqcs_t1
from  lqcs_mcp.tools import spectrum as lqcs_spectrum
from  lqcs_mcp.tools import spectrum_2d as lqcs_spectrum_2d
from  lqcs_mcp.tools import s21vsflux as lqcs_s21vsflux
from  lqcs_mcp.tools import singleshot as lqcs_singleshot
from  lqcs_mcp.tools import drag as lqcs_drag
from  lqcs_mcp.tools import opt_pipulse as lqcs_opt_pipulse
from  lqcs_mcp.tools import powershift as lqcs_powershift
from  lqcs_mcp.tools import delta as lqcs_delta
from  lqcs_mcp.tools import rb as lqcs_rb
from  lqcs_mcp.tools import spinecho_t2 as lqcs_spinecho_t2
from  lqcs_mcp.tools import ramsey_t2 as lqcs_ramsey_t2
from  lqcs_mcp.tools import xeb as lqcs_xeb
from  lqcs_mcp.tools import pipulsef10 as lqcs_pipulsef10
from  lqcs_mcp.tools import optqubitreadfreq as lqcs_optqubitreadfreq
from  lqcs_mcp.tools import pulseshape as lqcs_pulseshape
from  lqcs_mcp.tools import timingxyz as lqcs_timingxyz



import numpy as np
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from backend import s, info, generate_qubit, generate_coupler
import os
import numpy as np
import json
import h5py
from swiftmcp import mcp

params = {}

ROOT_FOLDER = 'D:/DataVault/LQHL.dir/test.dir/20260324.dir/'


def find_latest_filename(task_type):
    max_num = -1
    latest_file_name = None

    for filename in os.listdir(ROOT_FOLDER):
        print("filename: ", filename)
        if not filename.endswith('.hdf5'):
            continue

        number_id = int(filename.split(' - ')[0])

        if number_id > max_num and task_type in filename.lower():
            max_num = number_id
            latest_file_name = filename

    if latest_file_name is not None:
        print("find latest file: ", latest_file_name)
    else:
        return

    hdf5_path = os.path.join(ROOT_FOLDER, latest_file_name)
    return hdf5_path


def convert_ndarray(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_ndarray(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_ndarray(i) for i in obj]
    else:
        return obj
    
# @mcp.tool
# def get_data(rid:int|str):
    # import pickle
    # data_name = data_list[rid]
    # print(data_name)
    # with open(data_name, 'rb') as f:
    #     data = pickle.load(f)
    # return convert_ndarray(data)
    
@mcp.tool
def get_data(rid:int|str):
    hdf5_file_path = rid
    # 根据返回的路径，读取文件内容
    abs_path = os.path.abspath(hdf5_file_path)
    result = {}
    if not os.path.exists(abs_path):
        print(f" hdf5文件不存在:{abs_path}")
        return None
    # else:
    #     with open(abs_path,"rb") as f:
    #         content = f.read()
    #     return content
    with h5py.File(hdf5_file_path, 'r') as f:
        dv = f['DataVault']
        title = dv.attrs.get('Title', '').split(':')[0]
    
        if isinstance(dv, h5py.Dataset):
            data = dv[()]
            result[title]=data
            return convert_ndarray(result)



TASK_UPDATE_CONFIG = {
    's21': {'params': ['fread']},
    's21mul': {'params': ['fread']},
    'powershift': {'params': ['ReadIn.power']},
    's21vflux': {'params': ['bias_z']},
    'spectrum': {'params': ['f10', 'f21']},
    'singleshot': {'params': []},
    'rabi': {'params': ['PiGate.amp']},
    'PiPulseF10': {'params': ['f10', 'f21']},
    'ramsey': {'params': ['f10', 'f21']},
    'optQubitReadFreq': {'params': ['fread']},
    'opt_pipulse': {'params': ['PiGate.amp', 'PiGate.alpha','PiHalf.amp', 'PiHalf.alpha']},
    'TimingXYZ': {'params': ['timing.xy']},
    'PulseShape': {'params': []},
    'T1': {'params': []},
    'spinecho_t2': {'params': []},
    'Ramsey_T2': {'params': []},
    'xeb': {'params': []}
}
@mcp.tool
def update_param(qname, task_type, values):
    if task_type not in TASK_UPDATE_CONFIG:
            raise ValueError(f"unknown task: {task_type}")
    
    params = TASK_UPDATE_CONFIG[task_type]['params']
    values = [float(v.strip()) for v in values.split(',')]
    if len(values) != len(params):
        raise ValueError(f"{task_type} update {len(params)} params, but got {len(values)} : {values}")
    for param, val in zip(params, values):
        if val != "Null":
            eval(f"{qname}.regs.{param} = {val}")



@mcp.tool
def query_param(qname, task_type, key):
    if task_type not in TASK_UPDATE_CONFIG:
        raise ValueError(f"unknown task: {task_type}")
    if key not in TASK_UPDATE_CONFIG[task_type]['params']:
        raise ValueError(f"{task_type} not support: {key},support param: {TASK_UPDATE_CONFIG[task_type]['params']}")
    value = eval(f"{qname}.regs.{key}")
    return value


@mcp.tool
def s21(qubits:list[str]=['Q0','Q1'],
        frequency_start:float=-40,
        frequency_end:float=40,
        state: int | list[int] | None = [0],
        plot:bool=True,

        frequency_center=6.5,
        frequency_half_bandwidth=0.0005,
        frequency_sample_num=101,
        
        *args,**kwargs):
 
    result = lqcs_s21(qubits=qubits,
                      frequency_center=frequency_center,
                      frequency_half_bandwidth=frequency_half_bandwidth,
                      frequency_sample_num=frequency_sample_num
                      )
    hdf5_path = find_latest_filename(task_type='s21')
    return hdf5_path



@mcp.tool
def s21multi(qubits:list[str]=['Q0','Q1'],
        frequency_start:float=6.3,
        frequency_end:float=6.9,
        state: int | list[int] | None = [0],
        plot:bool=True,
        
        frequency_sample_rate=0.0001,
        *args,**kwargs):
    result = lqcs_s21mul(qubits=qubits,
                      frequency_start=frequency_start,
                      frequency_end=frequency_end,
                      frequency_sample_rate=frequency_sample_rate
                      )
    hdf5_path = find_latest_filename(task_type='s21multi')
    return hdf5_path


@mcp.tool

def drag(qubits:list[str]=['Q0','Q1'],
         lamb:list[float]=[-0.5, 0.5],
         stage:int=1,
         N_repeat:int=1,
         pulsePair:list[int]=[0, 1],
         signal:str='population',
        
         *args, **kwargs):
    result = lqcs_drag(qubits=qubits)
    hdf5_path = find_latest_filename(task_type='drag')
    return hdf5_path




@mcp.tool
def rabi(qubits:list[str]=['Q0','Q1'],
         drive_amp:list[float]=[0.01, 0.1],
         width:float=30e-9,
         signal:str='iq_avg',

         amp_start=0,
         amp_end=2,
         amp_sample_num=16,
         
         *args, **kwargs):
    result = lqcs_rabi(qubits=qubits,
                      amp_start=amp_start,
                      amp_end=amp_end,
                      amp_sample_num=amp_sample_num)
    hdf5_path = find_latest_filename(task_type='rabi')
    return hdf5_path


@mcp.tool

def ramsey(qubits:list[str]=['Q0','Q2'],
           delta:float=20e6,
           delay:float=10e-6,
           stage:int=1,
           scale:int=15,
           signal:str='population',
           
           
           delay_start=0,
           delay_end=100,
           delay_sample_num=100,
           fringeFreq=0.05,

           *args, **kwargs):
    result = lqcs_ramsey(qubits=qubits,
                      fringeFreq=fringeFreq,
                      delay_start=delay_start,
                      delay_end=delay_end,
                      delay_sample_num=delay_sample_num
                      )
    hdf5_path = find_latest_filename(task_type='ramsey')
    return hdf5_path


@mcp.tool

def t1(qubits:list[str]=['Q0','Q1'],
       delay:list[float]=[0, 100e-6],
       signal:str='population',
       
       zpa_start=-1.0,
       zpa_end=0.4,
       zpa_sample_num=71,
       delay_start=0,
       delay_end=80000,
       delay_sample_num=17,

       *args, **kwargs):
       result = lqcs_t1(qubits=qubits,
                         zpa_start=zpa_start,
                         zpa_end=zpa_end,
                         zpa_sample_num=zpa_sample_num,
                         delay_start=delay_start,
                         delay_end=delay_end,
                         delay_sample_num=delay_sample_num)
       hdf5_path = find_latest_filename(task_type='t1')
       return hdf5_path


@mcp.tool
def spectrum(qubits:list[str]=['Q0','Q1'],
             freq:list[float]=[-100, 100],
             drive_amp:float=0.5,
             duration:float=100e-9,
             from_idle:bool=True,
             absolute:bool=True,
             signal:str='population',
             build_dependencies:bool=False,

             freq_start=-3,
             freq_end=3,
             freq_sample_num=200,
             zpa=0,
             spec_amp=0.0,
             sb_freq=0,

             *args, **kwargs):
    result = lqcs_spectrum(qubits=qubits,
                      freq_start=freq_start,
                      freq_end=freq_end,
                      freq_sample_num=freq_sample_num,
                      zpa=zpa,
                      spec_amp=spec_amp,
                      sb_freq=sb_freq
                      )
    hdf5_path = find_latest_filename(task_type='spectrum')
    return hdf5_path
@mcp.tool

def spectrum_2d(qubits:list[str]=['Q0','Q1'],
                drive_amp:float=0.5,
                duration:float=100e-9,
                freq:list[float]=[-100, 100],
                bias:list[float]=[-0.1, 0.1],
                from_idle:bool=False,
                absolute:bool=True,
                
                *args, **kwargs):
    result = lqcs_spectrum_2d(qubits=qubits)
    hdf5_path = find_latest_filename(task_type='spectrum_2d')
    return hdf5_path




@mcp.tool
def s21vsflux(qubits_scan:list[str]=['Q0','Q1'],
              qubits_read:list[str]=None,
              freq:list[float]=None,
              read_bias:list[float]=None,
              freq_center:float=6.5,
              freq_half_bandwidth:float=0.03,
              freq_sample_num:int=11,
              read_bias_start:float=-3,
              read_bias_end:float=3,
              read_bias_sample_num:int=16,
              *args, **kwargs):
    result = lqcs_s21vsflux(qubits_scan=qubits_scan,
                      freq_center=freq_center,
                      freq_half_bandwidth=freq_half_bandwidth,
                      freq_sample_num=freq_sample_num,
                      read_bias_start=read_bias_start,
                      read_bias_end=read_bias_end,
                      read_bias_sample_num=read_bias_sample_num)
    hdf5_path = find_latest_filename(task_type='s21vsflux')
    return hdf5_path





@mcp.tool
def singleshot(qubits:list[str]=['Q0','Q1'],
               stage:int=1,

               *args, **kwargs):
    result = lqcs_singleshot(qubits=qubits)
    hdf5_path = find_latest_filename(task_type='singleshot')
    return hdf5_path


@mcp.tool
def opt_pipulse(qubits:list[str]=['Q0','Q1'],
                stage:int=1,
                N_list:list[int]=[1, 3, 5],
                amp_list:list[float]=None,
                signal:str='population',
                delay:float=20e-9,
                
                ms=None,
                gate='X',
                
                *args, **kwargs):
    
    
    result = lqcs_opt_pipulse(qubits=qubits,
                      ms=ms,
                      gate=gate
                      )
    hdf5_path = find_latest_filename(task_type='opt_pipulse')
    return hdf5_path





@mcp.tool

def powershift(qubits:list[str]=['Q0','Q1'],
               power:list[float]=[-20, 0],
               freq:list[float]=[-100, 100],

               frequency_center=6.539,
               frequency_half_bandwidth=0.0015,
               frequency_sample_num=16,
               power_start=-40,
               power_end=-16,
               power_sample_num=13,

               *args, **kwargs):
    result = lqcs_powershift(qubits=qubits,
                      frequency_center=frequency_center,
                      frequency_half_bandwidth=frequency_half_bandwidth,
                      frequency_sample_num=frequency_sample_num,
                      power_start=power_start,
                      power_end=power_end,
                      power_sample_num=power_sample_num
                      )
    hdf5_path = find_latest_filename(task_type='powershift')
    return hdf5_path




@mcp.tool

def delta(qubits:list[str]=['Q0','Q1'],
          N_list:list[int]=[1, 5, 13],
          delta_list:list[float]=None,
          stage:int=1,
          delay:float=20e-9,
          

          *args, **kwargs):
  

    result = lqcs_delta(qubits=qubits)
    hdf5_path = find_latest_filename(task_type='delta')
    return hdf5_path



@mcp.tool

def rb(qubits:list[str],
          couplers:tuple=tuple([]),
          stage:int=3,
          gate:list=['ref'],
          cycle:list=None,
          size:int=11,
          plot:bool=True,
          
       *args, **kwargs):
    
    result = lqcs_rb(qubits=qubits)
    hdf5_path = find_latest_filename(task_type='rb')
    return hdf5_path



@mcp.tool
def pulseshape(qubits:list[str],
               step_height=0.2,
               *args, **kwargs):
    result = lqcs_pulseshape(qubits=qubits,
                      step_height=step_height
                      )
    hdf5_path = find_latest_filename(task_type='pulseshape')
    return hdf5_path


@mcp.tool
def xeb(qubits:list[str],
        m_start=0,
        m_end=400,
        m_sample_num=10,
        k=30,
        gate='reference',
        tbuffer=0,
        stats=300,
        *args, **kwargs):
    result = lqcs_xeb(qubits=qubits,
                      m_start=m_start,
                      m_end=m_end,
                      m_sample_num=m_sample_num,
                      k=k,
                      gate=gate,
                      tbuffer=tbuffer,
                      stats=stats
                      )
    hdf5_path = find_latest_filename(task_type='xeb')
    return hdf5_path


@mcp.tool
def pipulsef10(qubits:list[str],
               fc=None,
               df_start=0,
               df_end=0.03,
               df_sample_num=21,
               *args, **kwargs):
    result = lqcs_pipulsef10(qubits=qubits,
                      fc=fc,
                      df_start=df_start,
                      df_end=df_end,
                      df_sample_num=df_sample_num,
                      )
    hdf5_path = find_latest_filename(task_type='pipulsef10')
    return hdf5_path


@mcp.tool
def optqubitreadfreq(qubits:list[str],
                     freq_span_center,
                     freq_span_half_bandwidth=0.0055,
                     freq_span_sample_num=40,
                     *args, **kwargs):
    result = lqcs_optqubitreadfreq(qubits=qubits,
                      freq_span_center=freq_span_center,
                      freq_span_half_bandwidth=freq_span_half_bandwidth,
                      freq_span_sample_num=freq_span_sample_num,
                      )
    hdf5_path = find_latest_filename(task_type='optqubitreadfreq')
    return hdf5_path





@mcp.tool
def timingxyz(qubits:list[str],
              delay_start=-60,
              delay_end=60,
              delay_sample_num=31,
              zpa=None,
              *args, **kwargs):
    result = lqcs_timingxyz(qubits=qubits,
                      delay_start=delay_start,
                      delay_end=delay_end,
                      delay_sample_num=delay_sample_num,
                      zpa=zpa
                      )
    hdf5_path = find_latest_filename(task_type='timingxyz')
    return hdf5_path


@mcp.tool
def spinecho_t2(qubits: list[str],
       
       delay_start=0,
       delay_end=10000,
       delay_sample_num=200,
       fringeFreq=0.05,
       *args, **kwargs):
    result = lqcs_spinecho_t2(qubits=qubits,
                       delay_start=delay_start,
                       delay_end=delay_end,
                       delay_sample_num=delay_sample_num,
                       fringeFreq=fringeFreq
                      )
    hdf5_path = find_latest_filename(task_type='spinecho_t2')
    return hdf5_path


@mcp.tool
def ramsey_t2(qubits: list[str],
             delay_start=0,
             delay_end=10000,
             delay_sample_num=100,
             fringeFreq=0.05,
             *args, **kwargs):
    result = lqcs_ramsey_t2(qubits=qubits,
                      delay_start=delay_start,
                      delay_end=delay_end,
                      delay_sample_num=delay_sample_num,
                      fringeFreq=fringeFreq
                      )
    hdf5_path = find_latest_filename(task_type='ramsey_t2')
    return hdf5_path