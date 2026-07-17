# -*- coding: utf-8 -*-
import sys
import os
import csv
import json
import numpy as np

from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from typing import Dict, Any, Optional, List, Tuple, Union
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
from qcontrol_mcp.tools import rabi as qcontrol_rabi
from qcontrol_mcp.tools import rabihalf as qcontrol_rabihalf
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
            'rabi': {'params': ['pi_amp', 'pi_len']},
            'rabihalf': {'params': ['pi_amp_half', 'pi_len_half']},
            't1': {'params': []},
            'ramsey': {'params': ['f10(GHz)', 'f21(GHz)']},
            'drag': {'params': []},
            'rb': {'params': []},
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
            'pi_len_star': 'pi_len(ns)',
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
def get_data(rid: Annotated[int | str, "csv文件路径/文件标识"]):
    '''
    Args:
        rid: csv文件路径或文件唯一标识
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
    task_type: Annotated[str, "任务类型标识"],
    values: Annotated[list, "待更新参数值列表，顺序与任务定义参数列表一一对应"]
) -> str:
    """
    读写并修改 qubit_config.json 中的量子比特参数
    Args:
        qname: 目标量子比特名称
        task_type: 标定任务类型
        values: 参数更新值列表，与当前任务所需参数数量、顺序保持一致
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
    return f"比特 {qname} 参数更新成功"


@mcp.tool
def query_param(
    qname: Annotated[str, "量子比特名称"],
    key: Annotated[str, "业务层参数映射标识名"]
):
    '''
    Args:
        qname: 目标量子比特名称
        key: 业务参数映射名，用于匹配配置文件原始字段
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
    # ROOT_FOLDER = 'D:/DataVault/LQHL.dir/test.dir/20260324.dir/'
    ROOT_FOLDER = 'D:/test/single/'

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
def rabi(
    qubits: Annotated[list[str], "量子比特名称列表"] = ['Q0', 'Q1'],
    piamp_start: Annotated[float, "π脉冲幅值扫描起始值"] = 0,
    piamp_end: Annotated[float, "π脉冲幅值扫描终止值"] = 2,
    piamp_sample_num: Annotated[int, "幅值扫描采样点数"] = 16,
    pi_len: Annotated[int, "π脉冲时长，单位纳秒(ns)"] = 50
):
    '''
    Args:
        qubits: 待标定量子比特名称列表
        piamp_start: π脉冲幅度扫描区间起始值
        piamp_end: π脉冲幅度扫描区间终止值
        piamp_sample_num: 幅度扫描采样点数
        pi_len: π脉冲固定时长，单位纳秒
    '''
    res = qcontrol_rabi(qubits=qubits,
                  piamp_start=piamp_start,
                  piamp_end=piamp_end,
                  piamp_sample_num=piamp_sample_num,
                  pi_len=pi_len)

    csv_path = find_latest_filename(task_type='pipulse')
    return csv_path


# 新增
@mcp.tool
def rabihalf(qubits: Annotated[list[str], "量子比特名称列表"] = ['Q0', 'Q1'],
         piamp_half_start: Annotated[float, "π/2脉冲幅值扫描起始值"] = 0,
         piamp_half_end: Annotated[float, "π/2脉冲幅值扫描终止值"] = 2,
         piamp_half_sample_num: Annotated[int, "幅值扫描采样点数"] = 16,
         pi_len_half: Annotated[int, "π/2脉冲时长，单位纳秒(ns)"] = 50):
    '''
    Args:
        qubits: 待标定量子比特名称列表
        piamp_half_start: π/2脉冲幅度扫描起始值
        piamp_half_end: π/2脉冲幅度扫描终止值
        piamp_half_sample_num: π/2脉冲幅度采样点数
        pi_len_half: π/2脉冲固定时长，单位纳秒
    '''
    res = qcontrol_rabihalf(qubits=qubits,
                  piamp_half_start=piamp_half_start,
                  piamp_half_end=piamp_half_end,
                  piamp_half_sample_num=piamp_half_sample_num,
                  pi_len_half=pi_len_half)

    csv_path = find_latest_filename(task_type='pipulse_half')
    return csv_path


@mcp.tool
def s21(
    qubits: Annotated[list[str], "量子比特名称列表"] = ['Q0', 'Q1'],
    frequency_center: Annotated[float, "读取中心频率，单位GHz"] = 6.5,
    frequency_half_bandwidth: Annotated[float, "频率扫描半带宽，单位GHz"] = 0.0005,
    frequency_sample_num: Annotated[int, "频率扫描采样点数"] = 101,
):
    '''
    Args:
        qubits: 待测试量子比特名称列表
        frequency_center: S21读取中心频率，单位GHz
        frequency_half_bandwidth: 频率扫描半带宽，单位GHz
        frequency_sample_num: 频率轴采样点数
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
    qubits: Annotated[list[str], "量子比特名称列表"] = ['Q0', 'Q1'],
    freq_start: Annotated[float, "频率扫描起始值，单位GHz"] = 3.0,
    freq_end: Annotated[float, "频率扫描终止值，单位GHz"] = 5.0,
    freq_sample_num: Annotated[int, "频率采样点数"] = 1000,
    zpa: Annotated[float, "比特直流偏置电压"] = 0,
    spec_amp: Annotated[float, "光谱驱动脉冲幅值"] = 0.5,
    sb_freq: Annotated[float, "边带频率，单位GHz"] = -0.15
):
    '''
    Args:
        qubits: 待测试量子比特名称列表
        freq_start: 频谱扫描频率起始值，单位GHz
        freq_end: 频谱扫描频率终止值，单位GHz
        freq_sample_num: 频率采样点数
        zpa: 量子比特直流偏置值
        spec_amp: 频谱测量驱动脉冲幅值
        sb_freq: 调制边带频率，单位GHz
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
    qubits: Annotated[list[str], "量子比特名称列表"] = ['Q0', 'Q1'],
    freq_start: Annotated[float, "频率起始值，单位GHz"] = 3.0,
    freq_end: Annotated[float, "频率终止值，单位GHz"] = 5.0,
    freq_sample_num: Annotated[int, "频率采样点数"] = 100,
    zpa_start: Annotated[float, "偏置电压起始值"] = -1,
    zpa_end: Annotated[float, "偏置电压终止值"] = 1,
    zpa_sample_num: Annotated[int, "偏置采样点数"] = 100,
    spec_amp: Annotated[float, "驱动脉冲幅值"] = 0.5,
    sb_freq: Annotated[float, "边带频率，单位GHz"] = -0.15
) -> str:
    '''
    Args:
        qubits: 待测试量子比特名称列表
        freq_start: 频率轴扫描起始值，单位GHz
        freq_end: 频率轴扫描终止值，单位GHz
        freq_sample_num: 频率轴采样点数
        zpa_start: 直流偏置扫描起始值
        zpa_end: 直流偏置扫描终止值
        zpa_sample_num: 偏置轴采样点数
        spec_amp: 驱动脉冲幅值
        sb_freq: 调制边带频率，单位GHz
    '''
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
def drag(
    qubits: Annotated[list[str], "目标量子比特名称列表"],
    lamb: Annotated[List[float], "DRAG修正系数扫描区间"] = [-0.5, 0.5],
    stage: Annotated[int, "实验阶数"] = 1,
    N_repeat: Annotated[int, "实验重复轮次"] = 1,
    pulsePair: Annotated[List[int], "脉冲配对索引"] = [0, 1],
    signal: Annotated[str, "观测信号类型"] = 'population'
) -> str:
    '''
    Args:
        qubits: 待测试量子比特名称列表
        lamb: DRAG脉冲修正系数扫描范围
        stage: 实验测试阶数
        N_repeat: 实验循环重复次数
        pulsePair: 脉冲组合配对索引
        signal: 观测信号类型，默认 population 布居数
    '''
    res = qcontrol_drag(qubits=qubits,
                         lamb=lamb,
                         stage=stage,
                         N_repeat=N_repeat,
                         pulsePair=pulsePair,
                         signal=signal)

    # csv_path = find_latest_filename(task_type='drag')
    return res


@mcp.tool
def singleshot(
    qubits: Annotated[list[str], "目标量子比特名称列表"],
) -> str:
    '''
    Args:
        qubits: 待做单量子态读取的比特名称列表
    '''
    res = qcontrol_singleshot(
        qubits=qubits
    )
    csv_path = find_latest_filename(task_type='iqraw')
    return csv_path


@mcp.tool
def t1(
    qubits: Annotated[list[str], "量子比特名称列表"] = ['Q0', 'Q1'],
    delay_start: Annotated[int, "延时起始值，单位纳秒(ns)"] = 0,
    delay_end: Annotated[int, "延时终止值，单位纳秒(ns)"] = 80000,
    delay_sample_num: Annotated[int, "延时轴采样点数"] = 17,
    zpa: Annotated[float, "直流偏置值"] = 0.0
):
    '''
    Args:
        qubits: 待测量T1弛豫时间的比特列表
        delay_start: 演化延时起始值，单位纳秒
        delay_end: 演化延时终止值，单位纳秒
        delay_sample_num: 延时轴采样点数
        zpa: 量子比特直流偏置电压
    '''
    res = qcontrol_t1(qubits=qubits,
                        delay_start=delay_start,
                        delay_end=delay_end,
                        delay_sample_num=delay_sample_num,
                        zpa=zpa)

    csv_path = find_latest_filename(task_type='t1')
    return csv_path



@mcp.tool
def ramsey(
    qubits: Annotated[list[str], "目标量子比特名称列表"],
    delay_start: Annotated[float, "演化延时起始值"] = 0,
    delay_end: Annotated[float, "演化延时终止值"] = 100,
    delay_sample_num: Annotated[int, "延时采样点数"] = 100,
    fringeFreq: Annotated[float, "振荡条纹频率"] = 0.05
) -> str:
    '''
    Args:
        qubits: 待测量Ramsey相干时间的比特列表
        delay_start: 自由演化延时起始值
        delay_end: 自由演化延时终止值
        delay_sample_num: 延时轴采样点数
        fringeFreq: Ramsey振荡条纹参考频率
    '''
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
def rb(qubits: Annotated[list[str], "目标量子比特名称列表"],
        couplers: Annotated[Tuple, "耦合比特组合"] = tuple([]),
        stage: Annotated[int, "随机基准测试阶数"] = 3,
        gate: Annotated[List[str], "基准门序列类型"] = ['ref'],
        cycle: Annotated[Optional[List], "循环配置列表"] = None,
        size: Annotated[int, "随机门序列长度"] = 11,
        plot: Annotated[bool, "是否输出绘图数据"] = True
) -> str:
    '''
    Args:
        qubits: 待测量随机基准保真度的比特列表
        couplers: 多比特耦合组合元组
        stage: 随机基准测试阶数
        gate: 基准门类型列表
        cycle: 实验循环配置参数列表
        size: 随机门序列长度
        plot: 是否生成绘图数据
    '''
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