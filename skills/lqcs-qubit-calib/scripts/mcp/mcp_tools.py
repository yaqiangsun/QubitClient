# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/03/26 15:50:15
########################################################################
"""
全局参数单位说明：频率: GHz
                时间: 纳秒(ns)
"""
import numpy as np
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from typing import Annotated
import os
from lqcs_mcp.tools import s21 as lqcs_s21
from lqcs_mcp.tools import s21multi as lqcs_s21multi
from lqcs_mcp.tools import rabi as lqcs_rabi
from lqcs_mcp.tools import ramsey as lqcs_ramsey
from lqcs_mcp.tools import t1 as lqcs_t1
from lqcs_mcp.tools import t1_2d as lqcs_t1_2d
from lqcs_mcp.tools import spectrum as lqcs_spectrum
from lqcs_mcp.tools import spectrum_2d as lqcs_spectrum_2d
from lqcs_mcp.tools import s21vsflux as lqcs_s21vsflux
from lqcs_mcp.tools import singleshot as lqcs_singleshot
# from  lqcs_mcp.tools import drag as lqcs_drag
from lqcs_mcp.tools import setpialpha as lqcs_setpialpha
from lqcs_mcp.tools import powershift as lqcs_powershift
# from  lqcs_mcp.tools import delta as lqcs_delta
from lqcs_mcp.tools import spinecho_t2 as lqcs_spinecho_t2
from lqcs_mcp.tools import ramsey_t2 as lqcs_ramsey_t2
from lqcs_mcp.tools import xeb as lqcs_xeb
from lqcs_mcp.tools import pipulsef10 as lqcs_pipulsef10
from lqcs_mcp.tools import optqubitreadfreq as lqcs_optqubitreadfreq
from lqcs_mcp.tools import pulseshape as lqcs_pulseshape
from lqcs_mcp.tools import timingxyz as lqcs_timingxyz
# from  lqcs_mcp.tools import rb as lqcs_rb
from lqcs_mcp.tools import baseslope as lqcs_baseslope

import os
import numpy as np
import h5py
from swiftmcp import mcp

from backend import s
from lqms.measure import (
    generate_coupler,
    generate_qubit,
)
_all_qubits = generate_qubit(globals(), info=None, sample=s)
_all_couplers = generate_coupler(globals(), info=None, sample=s)


def find_latest_filename(task_type):
    ROOT_FOLDER = 'D:/DataVault/LQHL.dir/test.dir/20260324.dir/'
    max_num = -1
    latest_file_name = None
    for filename in os.listdir(ROOT_FOLDER):
        # print("filename: ", filename)
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


def find_top3_latest_filename(task_type):
    ROOT_FOLDER = 'D:/DataVault/LQHL.dir/test.dir/20260324.dir/'
    file_info_list = []
    for filename in os.listdir(ROOT_FOLDER):
        if not filename.endswith('.hdf5'):
            continue
        if task_type not in filename.lower():
            continue
        # 提取序号数字
        number_id = int(filename.split(' - ')[0])
        file_info_list.append((number_id, filename))

    if not file_info_list:
        return []

    # 取前3
    file_info_list.sort(key=lambda x: x[0], reverse=True)
    top3 = file_info_list[:3]

    # 拼接完整路径
    result_path_list = []
    for num, fname in top3:
        full_path = os.path.join(ROOT_FOLDER, fname)
        result_path_list.append(full_path)
        print(f"Found file ID:{num} -> {fname}")

    return result_path_list


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
def get_data(rid: Annotated[int | str, "HDF5文件路径或文件ID"]):
    '''
    Args:
        rid: HDF5文件路径或文件ID
    '''
    hdf5_file_path = rid
    # 根据返回的路径，读取文件内容
    abs_path = os.path.abspath(hdf5_file_path)
    result = {}
    if not os.path.exists(abs_path):
        print(f" hdf5文件不存在:{abs_path}")
        return None
    with h5py.File(hdf5_file_path, 'r') as f:
        dv = f['DataVault']
        title = dv.attrs.get('Title', '').split(':')[0]
        if isinstance(dv, h5py.Dataset):
            data = dv[()]
            result[title] = data
            return convert_ndarray(result)


class TaskUpdateConfig:
    """任务参数配置类"""
    def __init__(self):
        self._config = {
            's21': {'params': ['fread']},
            's21multi': {'params': ['fread']},
            'powershift': {'params': ['ReadIn.power']},
            's21vflux': {'params': []},
            'spectrum': {'params': ['f10', 'f21']},  # f21可能不更新，如果出现双峰，左侧为f21,non计算为(左峰-右峰)*2
            'spectrum_2d': {'params': []},
            'singleshot': {'params': ['discriminator.center0', 'discriminator.center1', 'discriminator.threshold']},  # 要更新
            'rabi': {'params': ['PiGate.amp', 'PiHalf.amp']},  # PiHalf.amp数值是除以2
            'pipulsef10': {'params': ['f10', 'f21']},
            'ramsey': {'params': ['f10', 'f21']},
            'optqubitreadfreq': {'params': ['fread']},
            'opt_pipulse': {'params': ['PiGate.amp', 'PiGate.alpha']},
            'setpialpha': {'params': ['PiGate.amp', 'PiGate.alpha', 'PiHalf.amp', 'PiHalf.alpha']},  # 如果gate=X则更新'PiGate.amp', 'PiGate.alpha'这一组，如果X/2则'PiHalf.amp', 'PiHalf.alpha'这一组
            'timingxyz': {'params': ['timing.xy', 'timing.z']},  # 二选一，一般是'timing.z'，很少'timing.xy'
            'pulseshape': {'params': []},
            't1': {'params': []},
            't1_2d': {'params': []},
            'spinecho_t2': {'params': []},
            'ramsey_t2': {'params': []},
            'xeb': {'params': []}
        }
        self._param_mapping = {
            'fread_star': 'fread',
            'ReadIn_power_star': 'ReadIn.power',
            'bias_z_star': 'bias_z',
            'f10_star': 'f10',
            'f21_star': 'f21',
            'PiGate_amp_star': 'PiGate.amp',
            'PiGate_alpha_star': 'PiGate.alpha',
            'timing_xy_star': 'timing.xy',
            'discriminator_center0_star': 'discriminator.center0',
            'discriminator_center1_star': 'discriminator.center1',
            'discriminator_threshold_star': 'discriminator.threshold',
            'PiHalf_amp_star': 'PiHalf.amp',
            'PiHalf_alpha_star': 'PiHalf.alpha',
            'timing_xy_star': 'timing.xy',
            'timing_z_star': 'timing.z',
        }

    def get_task_params(self, task_type):
        if task_type not in self._config:
            raise ValueError(f"unknown task: {task_type}")
        return self._config[task_type]['params']

    def get_original_param_name(self, mapped_name):
        if mapped_name not in self._param_mapping:
            raise KeyError(f"Parameter '{mapped_name}' not found in mapping")
        return self._param_mapping[mapped_name]


def set_nested_attr(obj: object, attr_path: str, value):
    """
    支持多级带点属性赋值，例如 obj.regs.ReadIn.power = val
    """
    attrs = attr_path.split(".")
    # 遍历到倒数第二层
    parent = obj
    for attr_name in attrs[:-1]:
        parent = getattr(parent, attr_name)
    # 最后一级赋值
    target_attr = attrs[-1]
    print("parent, target_attr, value: ", parent, target_attr, value)
    setattr(parent, target_attr, value)


@mcp.tool
def update_param(
    qname: Annotated[str, "量子比特名称"],
    task_type: Annotated[str, "任务类型"],
    values: Annotated[str, "待更新参数值，多值以逗号分隔"]
):
    '''
    Args:
        qname: 量子比特名称
        task_type: 任务类型
        values: 待更新参数值，多值以逗号分隔
    '''
    TASK_UPDATE_CONFIG = TaskUpdateConfig()
    params = TASK_UPDATE_CONFIG.get_task_params(task_type)
    values = [float(v.strip()) for v in values.split(',')]
    if len(values) != len(params):
        raise ValueError(f"{task_type} update {len(params)} params, but got {len(values)} : {values}")

    qubit = globals()[qname]
    for param, val in zip(params, values):
        if val != "Null":
            set_nested_attr(qubit.regs, param, val)


@mcp.tool
def query_param(
    qname: Annotated[str, "量子比特名称"],
    key: Annotated[str, "参数标识名"]
):
    '''
    Args:
        qname: 量子比特名称
        key: 参数标识名
    '''
    TASK_UPDATE_CONFIG = TaskUpdateConfig()
    original_key = TASK_UPDATE_CONFIG.get_original_param_name(key)
    value = eval(f"{qname}.regs.{original_key}")
    return value


@mcp.tool
def s21(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q1'],
    frequency_center: Annotated[float, "中心频率，单位GHz"] = 6.5,
    frequency_half_bandwidth: Annotated[float, "频率半带宽，单位GHz"] = 0.0005,
    frequency_sample_num: Annotated[int, "频率采样点数"] = 101,
):
    '''
    Args:
        qubits: 量子比特名称
        frequency_center: 中心频率，单位GHz
        frequency_half_bandwidth: 频率半带宽，单位GHz
        frequency_sample_num: 频率采样点数
    '''
    result = lqcs_s21(qubits=qubits,
                      frequency_center=frequency_center,
                      frequency_half_bandwidth=frequency_half_bandwidth,
                      frequency_sample_num=frequency_sample_num
                      )
    hdf5_path = find_latest_filename(task_type='s21')
    return hdf5_path


@mcp.tool
def s21multi(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q1'],
    frequency_start: Annotated[float, "扫描起始频率，单位GHz"] = 6.3,
    frequency_end: Annotated[float, "扫描终止频率，单位GHz"] = 6.9,
    frequency_sample_rate: Annotated[float, "频率步长，单位GHz"] = 0.0001,
):
    '''
    Args:
        qubits: 量子比特名称
        frequency_start: 扫描起始频率，单位GHz
        frequency_end: 扫描终止频率，单位GHz
        frequency_sample_rate: 频率步长，单位GHz
    '''
    result = lqcs_s21multi(qubits=qubits,
                      frequency_start=frequency_start,
                      frequency_end=frequency_end,
                      frequency_sample_rate=frequency_sample_rate
                      )
    hdf5_path = find_latest_filename(task_type='s21')
    return hdf5_path

# @mcp.tool
# def drag(qubits:list[str]=['Q0','Q1'],
#          lamb:list[float]=[-0.5, 0.5],
#          stage:int=1,
#          N_repeat:int=1,
#          pulsePair:list[int]=[0, 1],
#          signal:str='population',
#          ):
#     result = lqcs_drag(qubits=qubits)
#     hdf5_path = find_latest_filename(task_type='drag')
#     return hdf5_path

@mcp.tool
def rabi(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q1'],
    piamp_start: Annotated[float, "脉冲幅值起始值"] = 0,
    piamp_end: Annotated[float, "脉冲幅值终止值"] = 2,
    piamp_sample_num: Annotated[int, "幅值采样点数"] = 16,
    pi_len: Annotated[int, "脉冲时长，单位纳秒"] = 50
):
    '''
    Args:
        qubits: 量子比特名称
        piamp_start: 脉冲幅值起始值
        piamp_end: 脉冲幅值终止值
        piamp_sample_num: 幅值采样点数
        pi_len: 脉冲时长，单位纳秒
    '''
    result = lqcs_rabi(qubits=qubits,
                      piamp_start=piamp_start,
                      piamp_end=piamp_end,
                      piamp_sample_num=piamp_sample_num,
                      pi_len=pi_len)
    hdf5_path = find_latest_filename(task_type='piamp')
    return hdf5_path


@mcp.tool
def ramsey(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q2'],
    delay_start: Annotated[int, "延时起始值，单位纳秒"] = 0,
    delay_end: Annotated[int, "延时终止值，单位纳秒"] = 600,
    delay_sample_num: Annotated[int, "延时采样点数"] = 100,
    fringeFreq: Annotated[float, "振荡频率，单位GHz"] = 0.005
):
    '''
    Args:
        qubits: 量子比特名称
        delay_start: 延时起始值，单位纳秒
        delay_end: 延时终止值，单位纳秒
        delay_sample_num: 延时采样点数
        fringeFreq: 振荡频率，单位GHz
    '''
    result = lqcs_ramsey(qubits=qubits,
                      delay_start=delay_start,
                      delay_end=delay_end,
                      delay_sample_num=delay_sample_num,
                      fringeFreq=fringeFreq
                      )
    hdf5_path = find_latest_filename(task_type='ramsey df')
    return hdf5_path


@mcp.tool
def t1_2d(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q1'],
    zpa_start: Annotated[float, "偏置起始值"] = -1.0,
    zpa_end: Annotated[float, "偏置终止值"] = 1.0,
    zpa_sample_num: Annotated[int, "偏置采样点数"] = 71,
    delay_start: Annotated[int, "延时起始值，单位纳秒"] = 0,
    delay_end: Annotated[int, "延时终止值，单位纳秒"] = 45000,
    delay_sample_num: Annotated[int, "延时采样点数"] = 40
):
    '''
    Args:
        qubits: 量子比特名称
        zpa_start: 偏置起始值
        zpa_end: 偏置终止值
        zpa_sample_num: 偏置采样点数
        delay_start: 延时起始值，单位纳秒
        delay_end: 延时终止值，单位纳秒
        delay_sample_num: 延时采样点数
    '''
    result = lqcs_t1_2d(qubits=qubits,
                         zpa_start=zpa_start,
                         zpa_end=zpa_end,
                         zpa_sample_num=zpa_sample_num,
                         delay_start=delay_start,
                         delay_end=delay_end,
                         delay_sample_num=delay_sample_num)
    hdf5_path = find_latest_filename(task_type='t1')
    return hdf5_path


@mcp.tool
def t1(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q1'],
    delay_start: Annotated[int, "延时起始值，单位纳秒"] = 0,
    delay_end: Annotated[int, "延时终止值，单位纳秒"] = 80000,
    delay_sample_num: Annotated[int, "延时采样点数"] = 17,
    zpa: Annotated[float, "直流偏置值"] = 0.0
):
    '''
    Args:
        qubits: 量子比特名称
        delay_start: 延时起始值，单位纳秒
        delay_end: 延时终止值，单位纳秒
        delay_sample_num: 延时采样点数
        zpa: 直流偏置值
    '''
    result = lqcs_t1(qubits=qubits,
                        delay_start=delay_start,
                        delay_end=delay_end,
                        delay_sample_num=delay_sample_num,
                        zpa=zpa)
    hdf5_path = find_latest_filename(task_type='t1')
    return hdf5_path


@mcp.tool
def spectrum(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q1'],
    freq_start: Annotated[float, "频率起始值，单位GHz"] = 3.0,
    freq_end: Annotated[float, "频率终止值，单位GHz"] = 5.0,
    freq_sample_num: Annotated[int, "频率采样点数"] = 1000,
    zpa: Annotated[float, "直流偏置值"] = 0,
    spec_amp: Annotated[float, "驱动脉冲幅值"] = 0.5,
    sb_freq: Annotated[float, "边带频率，单位GHz"] = -0.15
):
    '''
    Args:
        qubits: 量子比特名称
        freq_start: 频率起始值，单位GHz
        freq_end: 频率终止值，单位GHz
        freq_sample_num: 频率采样点数
        zpa: 直流偏置值
        spec_amp: 驱动脉冲幅值
        sb_freq: 边带频率，单位GHz
    '''
    result = lqcs_spectrum(qubits=qubits,
                           freq_start=freq_start,
                           freq_end=freq_end,
                           freq_sample_num=freq_sample_num,
                           zpa=zpa,
                           spec_amp=spec_amp,
                           sb_freq=sb_freq
                           )
    hdf5_path = find_latest_filename(task_type='spectroscopy')
    return hdf5_path


@mcp.tool
def spectrum_2d(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q1'],
    freq_start: Annotated[float, "频率起始值，单位GHz"] = 3.0,
    freq_end: Annotated[float, "频率终止值，单位GHz"] = 5.0,
    freq_sample_num: Annotated[int, "频率采样点数"] = 100,
    zpa_start: Annotated[float, "偏置起始值"] = -1,
    zpa_end: Annotated[float, "偏置终止值"] = 1,
    zpa_sample_num: Annotated[int, "偏置采样点数"] = 100,
    spec_amp: Annotated[float, "驱动脉冲幅值"] = 0.5,
    sb_freq: Annotated[float, "边带频率，单位GHz"] = -0.15
):
    '''
    Args:
        qubits: 量子比特名称
        freq_start: 频率起始值，单位GHz
        freq_end: 频率终止值，单位GHz
        freq_sample_num: 频率采样点数
        zpa_start: 偏置起始值
        zpa_end: 偏置终止值
        zpa_sample_num: 偏置采样点数
        spec_amp: 驱动脉冲幅值
        sb_freq: 边带频率，单位GHz
    '''
    try:
        result = lqcs_spectrum_2d(qubits=qubits,
                                freq_start=freq_start,
                                freq_end=freq_end,
                                freq_sample_num=freq_sample_num,
                                zpa_start=zpa_start,
                                zpa_end=zpa_end,
                                zpa_sample_num=zpa_sample_num,
                                spec_amp=spec_amp,
                                sb_freq=sb_freq
                                )
    except:
        pass
    hdf5_path = find_latest_filename(task_type='spectroscopy')
    return hdf5_path


@mcp.tool
def s21vsflux(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q1'],
    freq_center: Annotated[float, "中心频率，单位GHz"] = 6.5,
    freq_half_bandwidth: Annotated[float, "频率半带宽，单位GHz"] = 0.03,
    freq_sample_num: Annotated[int, "频率采样点数"] = 11,
    read_bias_start: Annotated[float, "读取偏置起始值"] = -3,
    read_bias_end: Annotated[float, "读取偏置终止值"] = 3,
    read_bias_sample_num: Annotated[int, "偏置采样点数"] = 16,
):
    '''
    Args:
        qubits: 量子比特名称
        freq_center: 中心频率，单位GHz
        freq_half_bandwidth: 频率半带宽，单位GHz
        freq_sample_num: 频率采样点数
        read_bias_start: 读取偏置起始值
        read_bias_end: 读取偏置终止值
        read_bias_sample_num: 偏置采样点数
    '''
    result = lqcs_s21vsflux(qubits=qubits,
                      freq_center=freq_center,
                      freq_half_bandwidth=freq_half_bandwidth,
                      freq_sample_num=freq_sample_num,
                      read_bias_start=read_bias_start,
                      read_bias_end=read_bias_end,
                      read_bias_sample_num=read_bias_sample_num)
    hdf5_path = find_latest_filename(task_type='zpa2d')
    return hdf5_path


@mcp.tool
def singleshot(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q1'],
):
    '''
    Args:
        qubits: 量子比特名称
    '''
    result = lqcs_singleshot(qubits=qubits)
    hdf5_path = find_latest_filename(task_type='iqraw')
    return hdf5_path


@mcp.tool
def setpialpha(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q1'],
    pipulse_num: Annotated[list[int], "π脉冲数量列表"] = [1, 3, 5],
    gate: Annotated[str, "门控类型"] = 'X',
):
    '''
    Args:
        qubits: 量子比特名称
        pipulse_num: π脉冲数量列表
        gate: 门控类型
    '''
    result = lqcs_setpialpha(qubits=qubits,
                      pipulse_num=pipulse_num,
                      gate=gate
                      )
    piamp_path_list = find_top3_latest_filename(task_type='piamp')
    alpha_path_list = find_top3_latest_filename(task_type='alpha')
    return [piamp_path_list, alpha_path_list]


@mcp.tool
def powershift(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q1'],
    freq_center: Annotated[float, "中心频率，单位GHz"] = 6.539,
    freq_half_bandwidth: Annotated[float, "频率半带宽，单位GHz"] = 0.0015,
    freq_sample_num: Annotated[int, "频率采样点数"] = 16,
    power_start: Annotated[float, "功率起始值"] = -40,
    power_end: Annotated[float, "功率终止值"] = -16,
    power_sample_num: Annotated[int, "功率采样点数"] = 13,
):
    '''
    Args:
        qubits: 量子比特名称
        freq_center: 中心频率，单位GHz
        freq_half_bandwidth: 频率半带宽，单位GHz
        freq_sample_num: 频率采样点数
        power_start: 功率起始值
        power_end: 功率终止值
        power_sample_num: 功率采样点数
    '''
    result = lqcs_powershift(qubits=qubits,
                      frequency_center=freq_center,
                      frequency_half_bandwidth=freq_half_bandwidth,
                      frequency_sample_num=freq_sample_num,
                      power_start=power_start,
                      power_end=power_end,
                      power_sample_num=power_sample_num
                      )
    hdf5_path = find_latest_filename(task_type='power')
    return hdf5_path

# @mcp.tool
# def delta(qubits:list[str]=['Q0','Q1'],
#           N_list:list[int]=[1, 5, 13],
#           delta_list:list[float]=None,
#           stage:int=1,
#           delay:float=20e-9,
#           ):
#     result = lqcs_delta(qubits=qubits)
#     hdf5_path = find_latest_filename(task_type='delta')
#     return hdf5_path

# @mcp.tool
# def rb(qubits:list[str],
#        couplers:tuple=tuple([]),
#        stage:int=3,
#        gate:list=['ref'],
#        cycle:list=None,
#        size:int=11,
#        plot:bool=True,
#        ):
#     result = lqcs_rb(qubits=qubits)
#     hdf5_path = find_latest_filename(task_type='rb')
#     return hdf5_path

@mcp.tool
def pulseshape(
    qubits: Annotated[list[str], "量子比特名称"],
    zpa_height: Annotated[float, "偏置高度"] = 0.2,
    delay_start: Annotated[int, "延时起始值，单位纳秒"] = 0,
    delay_end: Annotated[int, "延时终止值，单位纳秒"] = 1000,
    delay_sample_num: Annotated[int, "延时采样点数"] = 100,
    z_offset_half_bandwidth: Annotated[float, "Z偏移半带宽，单位GHz"] = 0.01,
    z_offset_num: Annotated[float, "Z偏移数值"] = 1.0
):
    '''
    Args:
        qubits: 量子比特名称
        zpa_height: 偏置高度
        delay_start: 延时起始值，单位纳秒
        delay_end: 延时终止值，单位纳秒
        delay_sample_num: 延时采样点数
        z_offset_half_bandwidth: Z偏移半带宽，单位GHz
        z_offset_num: Z偏移数值
    '''
    result = lqcs_pulseshape(qubits=qubits,
                      zpa_height=zpa_height,
                      delay_start=delay_start,
                      delay_end=delay_end,
                      delay_sample_num=delay_sample_num,
                      z_offset_half_bandwidth=z_offset_half_bandwidth,
                      z_offset_num=z_offset_num
                      )
    hdf5_path = find_latest_filename(task_type='pulseshape')
    return hdf5_path


@mcp.tool
def xeb(
    qubits: Annotated[list[str], "量子比特名称"],
    m_start: Annotated[int, "门数量起始值"] = 0,
    m_end: Annotated[int, "门数量终止值"] = 400,
    m_sample_num: Annotated[int, "门数量采样点数"] = 10,
    k: Annotated[int, "门序列号"] = 30,
    gate: Annotated[str, "门类型"] = 'reference',
    tbuffer: Annotated[int, "缓冲时长，单位纳秒"] = 0,
    stats: Annotated[int, "统计次数"] = 300
):
    '''
    Args:
        qubits: 量子比特名称
        m_start: 门数量起始值
        m_end: 门数量终止值
        m_sample_num: 门数量采样点数
        k: 门序列号
        gate: 门类型
        tbuffer: 缓冲时长，单位纳秒
        stats: 统计次数
    '''
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
def pipulsef10(
    qubits: Annotated[list[str], "量子比特名称"],
    freq_half_bandwidth: Annotated[float, "频率半带宽，单位GHz"] = 0.015,
    freq_sample_num: Annotated[int, "频率采样点数"] = 30
):
    '''
    Args:
        qubits: 量子比特名称
        freq_half_bandwidth: 频率半带宽，单位GHz
        freq_sample_num: 频率采样点数
    '''
    result = lqcs_pipulsef10(qubits=qubits,
                      freq_half_bandwidth=freq_half_bandwidth,
                      freq_sample_num=freq_sample_num)
    hdf5_path = find_latest_filename(task_type='pipulse df')
    return hdf5_path


@mcp.tool
def optqubitreadfreq(
    qubits: Annotated[list[str], "量子比特名称"],
    freq_half_bandwidth: Annotated[float, "频率半带宽，单位GHz"] = 0.0015
):
    '''
    Args:
        qubits: 量子比特名称
        freq_half_bandwidth: 频率半带宽，单位GHz
    '''
    result = lqcs_optqubitreadfreq(qubits=qubits,
                      freq_span=freq_half_bandwidth  # 映射关系待确定
                      )
    hdf5_path = find_latest_filename(task_type='s21_dis')
    return hdf5_path


@mcp.tool
def timingxyz(
    qubits: Annotated[list[str], "量子比特名称"],
    delay_start: Annotated[int, "延时起始值，单位纳秒"] = -60,
    delay_end: Annotated[int, "延时终止值，单位纳秒"] = 60,
    delay_sample_num: Annotated[int, "延时采样点数"] = 31,
    zpa: Annotated[float, "直流偏置值"] = 0.5
):
    '''
    Args:
        qubits: 量子比特名称
        delay_start: 延时起始值，单位纳秒
        delay_end: 延时终止值，单位纳秒
        delay_sample_num: 延时采样点数
        zpa: 直流偏置值
    '''
    result = lqcs_timingxyz(qubits=qubits,
                      delay_start=delay_start,
                      delay_end=delay_end,
                      delay_sample_num=delay_sample_num,
                      zpa=zpa
                      )
    hdf5_path = find_latest_filename(task_type='timingxyz')
    return hdf5_path


@mcp.tool
def spinecho_t2(
    qubits: Annotated[list[str], "量子比特名称"],
    delay_start: Annotated[int, "延时起始值，单位纳秒"] = 0,
    delay_end: Annotated[int, "延时终止值，单位纳秒"] = 10000,
    delay_sample_num: Annotated[int, "延时采样点数"] = 200,
    fringeFreq: Annotated[float, "振荡频率，单位GHz"] = 0.005,
    pipulse_num: Annotated[int, "π脉冲数量"] = 1
):
    '''
    Args:
        qubits: 量子比特名称
        delay_start: 延时起始值，单位纳秒
        delay_end: 延时终止值，单位纳秒
        delay_sample_num: 延时采样点数
        fringeFreq: 振荡频率，单位GHz
        pipulse_num: π脉冲数量
    '''
    result = lqcs_spinecho_t2(qubits=qubits,
                       delay_start=delay_start,
                       delay_end=delay_end,
                       delay_sample_num=delay_sample_num,
                       fringeFreq=fringeFreq,
                       pipulse_num=pipulse_num
                      )
    hdf5_path = find_latest_filename(task_type='spinecho')
    return hdf5_path


@mcp.tool
def ramsey_t2(
    qubits: Annotated[list[str], "量子比特名称"],
    delay_start: Annotated[int, "延时起始值，单位纳秒"] = 0,
    delay_end: Annotated[int, "延时终止值，单位纳秒"] = 10000,
    delay_sample_num: Annotated[int, "延时采样点数"] = 100,
    fringeFreq: Annotated[float, "振荡频率，单位GHz"] = 0.005
):
    '''
    Args:
        qubits: 量子比特名称
        delay_start: 延时起始值，单位纳秒
        delay_end: 延时终止值，单位纳秒
        delay_sample_num: 延时采样点数
        fringeFreq: 振荡频率，单位GHz
    '''
    result = lqcs_ramsey_t2(qubits=qubits,
                      delay_start=delay_start,
                      delay_end=delay_end,
                      delay_sample_num=delay_sample_num,
                      fringeFreq=fringeFreq
                      )
    hdf5_path = find_latest_filename(task_type='ramsey')
    return hdf5_path


@mcp.tool
def baseslope(
    qubits: Annotated[list[str], "量子比特名称"],
    delay_start: Annotated[int, "延时起始值，单位纳秒"] = 0,
    delay_end: Annotated[int, "延时终止值，单位纳秒"] = 10000,
    delay_sample_num: Annotated[int, "延时采样点数"] = 100,
    step_height: Annotated[float, "阶跃高度"] = 0
):
    '''
    Args:
        qubits: 量子比特名称
        delay_start: 延时起始值，单位纳秒
        delay_end: 延时终止值，单位纳秒
        delay_sample_num: 延时采样点数
        step_height: 阶跃高度
    '''
    result = lqcs_baseslope(qubits=qubits,
                      delay_start=delay_start,
                      delay_end=delay_end,
                      delay_sample_num=delay_sample_num,
                      step_height=step_height
                      )
    hdf5_path = find_latest_filename(task_type='slope')
    return hdf5_path