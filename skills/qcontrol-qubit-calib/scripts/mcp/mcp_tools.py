# -*- coding: utf-8 -*-
import sys
import os
import csv
import json
import numpy as np

from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from typing import Dict, Any, Optional, List
from typing import Annotated
from swiftmcp import mcp
from labrad.units import Unit, Value, WithUnit

# 定义物理单位
V, mV, us, ns, GHz, MHz, dBm, rad, uA = [
    Unit(s) for s in ("V", "mV", "us", "ns", "GHz", "MHz", "dBm", "rad", "uA")
]

from qcontrol_mcp.tools import s21 as qcontrol_s21
from qcontrol_mcp.tools import spectrum as qcontrol_spectrum
from qcontrol_mcp.tools import spectrum_2d as qcontrol_spectrum_2d
from qcontrol_mcp.tools import pi_pulse as qcontrol_pi_pulse
from qcontrol_mcp.tools import pi_pulse_half as qcontrol_pi_pulse_half
from qcontrol_mcp.tools import drag as qcontrol_drag
from qcontrol_mcp.tools import singleshot as qcontrol_singleshot
from qcontrol_mcp.tools import t1 as qcontrol_t1
from qcontrol_mcp.tools import ramsey as qcontrol_ramsey
from qcontrol_mcp.tools import rb as qcontrol_rb

data_vault_path = ["", "test", "single"]

# 配置文件路径
CONFIG_PATH = Path(__file__).parent / "qubit_config.json"


def load_qubit_config() -> dict:
    """加载量子比特参数 JSON"""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"load config json fail: {str(e)}")


def save_qubit_config(data: dict):
    """写入量子比特参数 JSON"""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise RuntimeError(f"write config json fail: {str(e)}")
    

# ------模拟r数列-----------
class RangeObj:
    def __init__(self, start, stop, step, unit=None):
        self.start = start
        self.stop = stop
        self.step = step
        self.unit = unit

class RangeMaker:
    def __getitem__(self, item):
        if isinstance(item, tuple):
            slice_part, unit = item
        else:
            slice_part = item
            unit = None
        start = slice_part.start
        stop = slice_part.stop
        step = slice_part.step
        return RangeObj(start, stop, step, unit)

r = RangeMaker()


class TaskUpdateConfig:
    """任务参数配置类"""
    def __init__(self):
        self._config = {
            's21': {'params': ['readout_freq(GHz)']},
            'spectrum': {'params': ['f10(GHz)', 'f21(GHz)']},  # f21可能不更新，如果出现双峰，左侧为f21,non计算为(左峰-右峰)*2
            'spectrum_2d': {'params': []},
            'singleshot': {'params': ['center |0>', 'center |1>']},  # FIXME:没有 'discriminator.threshold'
            'rabi': {'params': ['PiGate.amp', 'pi_amp_half']},  # PiHalf.amp数值是除以2
            'pipulsef10': {'params': ['f10(GHz)', 'f21(GHz)']},
            'ramsey': {'params': ['f10(GHz)', 'f21(GHz)']},
            'optqubitreadfreq': {'params': ['fread']},
            'opt_pipulse': {'params': ['PiGate.amp', 'PiGate.alpha']},
            'setpialpha': {'params': ['pi_amp', 'pi_alpha', 'pi_amp_half', 'pi_alpha_half']},
            'pulseshape': {'params': []},
            't1': {'params': []},
        }
        self._param_mapping = {
            'readout_freq_star': 'readout_freq(GHz)',
            'readout_power_star': 'readout_power(dBm)',
            'readout_len_star': 'readout_len(us)',
            'z_offset_star': 'z_offset',
            'f10_star': 'f10(GHz)',
            'f21_star': 'f21(GHz)',
            'pi_amp_star': 'pi_amp',
            'pi_alpha_star': 'pi_alpha',
            'timing_xy_star': 'timing_lag_xy(ns)',
            'center0_star': 'center |0>',
            'center1_star': 'center |1>',
            'pi_amp_half_star': 'pi_amp_half',
            'pi_alpha_half_star': 'pi_alpha_half',
            'adc_start_delay_star': 'adc_start_delay(ns)',
            'spec_len_star': 'spec_len(us)'
        }

    def get_task_params(self, task_type):
        if task_type not in self._config:
            raise ValueError(f"unknown task: {task_type}")
        return self._config[task_type]['params']

    def get_original_param_name(self, mapped_name):
        if mapped_name not in self._param_mapping:
            raise KeyError(f"Parameter '{mapped_name}' not found in mapping")
        return self._param_mapping[mapped_name]


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
def get_data(rid: Annotated[int | str, "csv文件路径"]):
    '''
    Args:
        rid: csv文件路径
    '''
    csv_file_path = rid
    abs_path = os.path.abspath(csv_file_path)
    result = {}

    if not os.path.exists(abs_path):
        print(f" csv文件不存在:{abs_path}")
        return None

    # 读取CSV并转为numpy数组
    data_list = []
    with open(abs_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, "data")
        title = header.split(':')[0] if isinstance(header, str) else "data"
        
        for row in reader:
            row_data = [float(val) for val in row]
            data_list.append(row_data)
    
    # 转为ndarray，保持和原HDF5输出结构一致
    data = np.array(data_list)
    result[title] = data
    return convert_ndarray(result)

@mcp.tool
def update_param(
    qname: Annotated[str, "量子比特名称，如 qr1、qr2"],
    task_type: Annotated[str, "任务类型"],
    values: Annotated[list, "待更新参数值列表，与TaskUpdateConfig中定义的任务参数列表一致"]
) -> str:
    """
    读写并修改 qubit_config.json 中的量子比特参数
    """

    # load json
    cfg = load_qubit_config()

    if qname not in cfg:
        return f"错误：量子比特 {qname} 不存在"
    
    TASK_UPDATE_CONFIG = TaskUpdateConfig()
    params = TASK_UPDATE_CONFIG.get_task_params(task_type)

    if len(values) != len(params):
        raise ValueError(f"{task_type} update {len(params)} params, but got {len(values)} : {values}")
    
    for param_name, param_val in zip(params, values):
        # 更新参数（支持float、数组）
        old_val = cfg[qname].get(param_name, None)
        cfg[qname][param_name] = param_val

    # write json
    save_qubit_config(cfg)


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
    # load json
    cfg = load_qubit_config()

    if qname not in cfg:
        return f"错误：量子比特 {qname} 不存在"
    
    TASK_UPDATE_CONFIG = TaskUpdateConfig()
    machine_key = TASK_UPDATE_CONFIG.get_original_param_name(key)

    value = cfg[qname].get(machine_key, None)

    return value


# FIXME:根据csv保存地址重新修改此接口
def find_latest_filename(task_type):
    ROOT_FOLDER = 'D:/DataVault/LQHL.dir/test.dir/20260324.dir/'
    max_num = -1
    latest_file_name = None
    for filename in os.listdir(ROOT_FOLDER):
        # print("filename: ", filename)
        if not filename.endswith('.csv'):
            continue
        number_id = int(filename.split(' - ')[0])
        if number_id > max_num and task_type in filename.lower():
            max_num = number_id
            latest_file_name = filename
    if latest_file_name is not None:
        print("find latest file: ", latest_file_name)
    else:
        return
    csv_path = os.path.join(ROOT_FOLDER, latest_file_name)
    return csv_path


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
    res = qcontrol_s21(qubits=qubits,
                      frequency_center=frequency_center,
                      frequency_half_bandwidth=frequency_half_bandwidth,
                      frequency_sample_num=frequency_sample_num
                      )
    csv_path = find_latest_filename(task_type='s21')
    return csv_path
    
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
    res = qcontrol_spectrum(qubits=qubits,
                           freq_start=freq_start,
                           freq_end=freq_end,
                           freq_sample_num=freq_sample_num,
                           zpa=zpa,
                           spec_amp=spec_amp,
                           sb_freq=sb_freq
                           )
    csv_path = find_latest_filename(task_type='spectrum')
    return csv_path


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
) -> str:
    res = qcontrol_spectrum_2d(qubits=qubits,
                                freq_start=freq_start,
                                freq_end=freq_end,
                                freq_sample_num=freq_sample_num,
                                zpa_start=zpa_start,
                                zpa_end=zpa_end,
                                zpa_sample_num=zpa_sample_num,
                                spec_amp=spec_amp,
                                sb_freq=sb_freq)
    csv_path = find_latest_filename(task_type='spectrum_2d')
    return csv_path


@mcp.tool
def pi_pulse(
    qubits: Annotated[list[str], "目标量子比特名称"],
    pi_num: Annotated[int, "脉冲数量"] = None,
    pi_amp: Annotated[Any, "脉冲幅度"] = None,
    pi_len: Annotated[Any, "脉冲时长"] = None,
    z_offset: Annotated[float, "Z偏移量"] = None,
    readout_freq: Annotated[Any, "读取频率"] = None,
    readout_power: Annotated[Any, "读取功率"] = None,
    f10: Annotated[Any, "本征频率"] = None
) -> str:

    res = qcontrol_pi_pulse(
        qubits=qubits, pi_num=pi_num, pi_amp=pi_amp, pi_len=pi_len,
        z_offset=z_offset, readout_freq=readout_freq,
        readout_power=readout_power, f10=f10
    )

    csv_path = find_latest_filename(task_type='pi_pulse')
    return csv_path


@mcp.tool
def pi_pulse_half(
    qubits: Annotated[list[str], "目标量子比特名称"],
    pi_num: Annotated[int, "脉冲数量 1/3/5"],
    pi_amp_half: Annotated[Any, "半脉冲幅度"] = None
) -> str:

    res = qcontrol_pi_pulse_half(qubits=qubits, pi_num=pi_num, pi_amp_half=pi_amp_half)

    csv_path = find_latest_filename(task_type='pi_pulse_half')
    return csv_path


@mcp.tool
def drag(
    qubits: Annotated[list[str], "目标量子比特名称"],
    lamb:list[float]=[-0.5, 0.5],
    stage:int=1,
    N_repeat:int=1,
    pulsePair:list[int]=[0, 1],
    signal:str='population'
) -> str:
    res = qcontrol_drag(qubits=qubits,
                         lamb=lamb,
                         stage=stage,
                         N_repeat=N_repeat,
                         pulsePair=pulsePair,
                         signal=signal)

    csv_path = find_latest_filename(task_type='drag')
    return csv_path


@mcp.tool
def singleshot(
    qubits: Annotated[list[str], "目标量子比特名称"],
) -> str:

    res = qcontrol_singleshot(
        qubits=qubits
    )
    csv_path = find_latest_filename(task_type='iqraw')
    return csv_path


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
    res = qcontrol_t1(qubits=qubits,
                        delay_start=delay_start,
                        delay_end=delay_end,
                        delay_sample_num=delay_sample_num,
                        zpa=zpa)

    csv_path = find_latest_filename(task_type='t1')
    return csv_path

@mcp.tool
def opt_pipulse(qubits:list[str]=['Q0','Q1'],
                N_list:list[int]=[1, 3, 5],
                amp_list:list[float]=None
                ):
    res = qcontrol_pi_pulse(qubits=qubits,
                             N_list=N_list,
                             amp_list=amp_list)
    csv_path = find_latest_filename(task_type='opt_pipulse')
    return csv_path

@mcp.tool
def ramsey(
    qubits: Annotated[list[str], "目标量子比特名称"],
    delay_start:float=0,
    delay_end:float=100,
    delay_sample_num:int=100,
    fringeFreq:float=0.05
) -> str:

    res = qcontrol_ramsey(
        qubits=qubits, 
        delay_start=delay_start, 
        delay_end=delay_end,
        delay_sample_num=delay_sample_num, 
        fringeFreq=fringeFreq
    )
    csv_path = find_latest_filename(task_type='ramsey')
    return csv_path


@mcp.tool
def rb(qubits:list[str],
        couplers:tuple=tuple([]),
        stage:int=3,
        gate:list=['ref'],
        cycle:list=None,
        size:int=11,
        plot:bool=True
) -> str:
    res = qcontrol_rb(
        qubits=qubits,
        couplers=couplers,
        stage=stage,
        gate=gate,
        cycle=cycle,
        size=size,
        plot=plot
    )
    csv_path = find_latest_filename(task_type='rb')
    return csv_path

