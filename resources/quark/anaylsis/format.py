# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/11 10:39:49
########################################################################

import logging
import numpy as np

def optpipulse_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """

    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {
        "image": {
        }
    }
    for index,qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取AMP幅值轴x_array
        x_array = np.array(result["meta"]["axis"]["amp"]["def"], dtype=np.float64)
        assert x_array.ndim == 1, "AMP轴需为一维数组"
        amp_points = len(x_array)

        # 处理Population波形
        waveforms = np.array(result["data"]["population"][:,:,index], dtype=np.float64)
                
        # 最终格式校验
        assert waveforms.ndim == 2, "waveforms需为(m, n)二维数组, m为波形数量"
        assert waveforms.shape[1] == amp_points, "waveforms点数需与AMP轴一致"
        assert x_array.ndim == 1 and len(x_array) == amp_points, "AMP轴格式错误"
    
        # 转换成所需的标准格式
        data_formated["image"][qubit_name] =  (waveforms, x_array)
    return data_formated


def s21_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """

    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {
        "image": {
        }
    }
    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取AMP幅值轴x_array
        x_array = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)
        assert x_array.ndim == 1, "x轴需为一维数组"
        x_points = len(x_array)

        # 处理Population波形
        iq_avg = np.array(result["data"]["iq_avg"][:, index], dtype=np.complex64)
        amp = np.abs(iq_avg)
        phi = np.angle(iq_avg)
        phi = np.unwrap(np.angle(iq_avg))
        # import scipy
        # phi = scipy.signal.detrend(phi, type='linear')
        # 最终格式校验
        assert iq_avg.ndim == 1, "iq_avg为一维"

        assert amp.shape[0] == x_points, "amp点数需与x轴一致"
        assert phi.shape[0] == x_points, "phi点数需与x轴一致"

        # 转换成所需的标准格式
        data_formated["image"][qubit_name] = (x_array, amp,phi)
    return data_formated


def nns21_convert(result):
    data_formated = s21_convert(result)
    return data_formated

def drag_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """

    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {
        "image": {
        }
    }
    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        x = np.array(result["meta"]["axis"]["lamb"]["def"], dtype=np.float64)

        # 处理Population波形
        y0y1 = np.array(result["data"]["population"][:,:, index], dtype=np.float64)


        assert x.ndim == 1, "x为一维"
        assert y0y1.ndim == 2, "y0为一维"

        assert x.shape[0] == y0y1.shape[1], "x点数需与 y0y1.shape[1]轴一致"

        # 转换成所需的标准格式
        data_formated["image"][qubit_name] = (x, y0y1)
    return data_formated

def s21vsflux_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """

    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {
        "image": {
        }
    }
    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取AMP幅值轴x_array
        volt = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)
        assert volt.ndim == 1, "volt轴需为一维数组"
        freq = np.array(result["meta"]["axis"]["read_bias"]["def"], dtype=np.float64)
        assert freq.ndim == 1, "freq轴需为一维数组"
        # 处理Population波形
        s = np.array(result["data"]["iq_avg"][:,:, index], dtype=np.complex64)
        s = np.abs(s)
        # 最终格式校验
        assert s.ndim == 2, "s为二维"

        assert s.shape[0] == freq.shape[0], "s的第一维度点数需与freq轴一致"
        assert s.shape[1] == volt.shape[0], "s的第二维度点数需与volt轴一致"

        # 转换成所需的标准格式
        data_formated["image"][qubit_name] = (volt, freq,s)
    return data_formated


def nns21vsflux_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """

    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {
        "image": {
        }
    }
    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取AMP幅值轴x_array
        volt = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)
        assert volt.ndim == 1, "volt轴需为一维数组"
        freq = np.array(result["meta"]["axis"]["read_bias"]["def"], dtype=np.float64)
        assert freq.ndim == 1, "freq轴需为一维数组"
        # 处理Population波形
        s = np.array(result["data"]["iq_avg"][:,:, index], dtype=np.complex64)
        s = np.abs(s)
        # 最终格式校验
        assert s.ndim == 2, "s为二维"

        assert s.shape[0] == freq.shape[0], "s的第一维度点数需与freq轴一致"
        assert s.shape[1] == volt.shape[0], "s的第二维度点数需与volt轴一致"

        # 转换成所需的标准格式
        data_formated["image"][qubit_name] = (volt, freq,s)
    return data_formated




def singleshot_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """

    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {
        "image": {
        }
    }
    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"



        # 处理Population波形
        s0 = np.array(result["data"]["iq"][0,:, index], dtype=np.complex64)
        s1 = np.array(result["data"]["iq"][1,:, index], dtype=np.complex64)


        assert s0.ndim == 1, "s0为一维"
        assert s1.ndim == 1, "s1为一维"

        data_formated["image"][qubit_name] = (s0, s1)
    return data_formated

def nnspectrum2d_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """

    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {
        "image": {
        }
    }
    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取AMP幅值轴x_array
        freq = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)
        assert freq.ndim == 1, "volt轴需为一维数组"
        bias = np.array(result["meta"]["axis"]["bias"]["def"], dtype=np.float64)
        assert bias.ndim == 1, "freq轴需为一维数组"
        # 处理Population波形
        s = np.array(result["data"]["iq_avg"][:, :, index], dtype=np.complex64)
        # s = np.abs(s)
        # 最终格式校验
        assert s.ndim == 2, "s为二维"

        assert s.shape[0] == bias.shape[0], "s的第一维度点数需与bias轴一致"
        assert s.shape[1] == freq.shape[0], "s的第二维度点数需与freq轴一致"

        # 转换成所需的标准格式
        data_formated["image"][qubit_name] = (s.T, bias, freq)
    return data_formated



def spectrum2d_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """

    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {
        "image": {
        }
    }
    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取AMP幅值轴x_array
        freq = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)
        assert freq.ndim == 1, "volt轴需为一维数组"
        bias = np.array(result["meta"]["axis"]["bias"]["def"], dtype=np.float64)
        assert bias.ndim == 1, "freq轴需为一维数组"
        # 处理Population波形
        s = np.array(result["data"]["iq_avg"][:, :, index], dtype=np.complex64)
        # s = np.abs(s)
        # 最终格式校验
        assert s.ndim == 2, "s为二维"

        assert s.shape[0] == bias.shape[0], "s的第一维度点数需与bias轴一致"
        assert s.shape[1] == freq.shape[0], "s的第二维度点数需与freq轴一致"

        # 转换成所需的标准格式
        data_formated["image"][qubit_name] = (s.T, bias, freq)
    return data_formated


def rabicos_convert(result):
    """
    将 quark 格式的 Rabi 幅度扫描数据转换为 qubitclient 所需格式
    Args:
        result (dict): 原始实验数据字典（需包含 meta/data 核心字段）
    Returns:
        dict: 符合服务器要求的格式数据 {"image": {qubit_name: (x_array, amp_array)}}
    """
    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}
    
    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取驱动幅度轴 x_array
        x_array = np.array(result["meta"]["axis"]["drive_amp"]["def"], dtype=np.float64)
        assert x_array.ndim == 1, "drive_amp 轴需为一维数组"

        # 获取 IQ 数据并计算幅度
        iq_data = result["data"]["iq_avg"]
        assert iq_data.shape[1] == len(qubit_name_list), \
            f"iq_avg 的 qubit 维度 {iq_data.shape[1]} 与 qubits 数量不匹配"

        # 计算幅度（Rabi 通常使用幅度）
        amp_array = np.abs(iq_data[:, index])   # shape: (n_amp,)

        # 最终格式校验
        assert amp_array.ndim == 1, "amp_array 应为一维数组"
        assert amp_array.shape[0] == x_array.shape[0], \
            f"{qubit_name} 的 amp_array 长度与 drive_amp 不匹配"

        # 转换成所需的标准格式
        data_formated["image"][qubit_name] = (x_array, amp_array)
    
    return data_formated


def t1fit_convert(result):
    """
    将 quark 格式的 T1 弛豫数据转换为 qubitclient 所需格式
    Args:
        result (dict): 原始实验数据字典（需包含 meta/data 核心字段）
    Returns:
        dict: 符合服务器要求的格式数据 {"image": {qubit_name: (delay_array, population_array)}}
    """
    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}
    
    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取延迟时间轴 x_array
        delay_array = np.array(result["meta"]["axis"]["delay"]["def"], dtype=np.float64)
        assert delay_array.ndim == 1, "delay 轴需为一维数组"

        # 处理 population 波形（最常用字段）
        population = np.array(result["data"]["population"][:, index], dtype=np.float64)
        
        # 最终格式校验
        assert population.ndim == 1, "population 应为一维数组"
        assert population.shape[0] == delay_array.shape[0], \
            f"{qubit_name} 的 population 长度与 delay 轴不匹配"

        # 转换成所需的标准格式
        data_formated["image"][qubit_name] = (delay_array, population)
    
    return data_formated


def t2fit_convert(result):
    """
    将 quark 格式的 T2/Ramsey 数据转换为 qubitclient 所需格式
    Args:
        result (dict): 原始实验数据字典（需包含 meta/data 核心字段）
    Returns:
        dict: 符合服务器要求的格式数据 {"image": {qubit_name: (delay_array, population_array)}}
    """
    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}
    
    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取延迟时间轴 x_array
        delay_array = np.array(result["meta"]["axis"]["delay"]["def"], dtype=np.float64)
        assert delay_array.ndim == 1, "delay 轴需为一维数组"

        # 处理 population 波形（Ramsey 实验中最常用的字段）
        population = np.array(result["data"]["population"][:, index], dtype=np.float64)
        
        # 最终格式校验
        assert population.ndim == 1, "population 应为一维数组"
        assert population.shape[0] == delay_array.shape[0], \
            f"{qubit_name} 的 population 长度与 delay 轴不匹配"

        # 转换成所需的标准格式
        data_formated["image"][qubit_name] = (delay_array, population)
    
    return data_formated

def nnspectrum_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式（一维频谱专用）
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 服务器要求的格式数据
    """

    # 提取量子比特名称
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {
        "image": {
        }
    }
    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取频率轴数据
        freq_key = f"$gate.R.{qubit_name}.params.frequency"
        freq = np.array(result["meta"]["axis"]["freq"].get(freq_key, result["meta"]["axis"]["freq"]["def"]), dtype=np.float64)
        assert freq.ndim == 1, "freq轴需为一维数组"
        
        # 处理IQ均值波形
        s = np.array(result["data"]["iq_avg"][:, index], dtype=np.complex64)
        # 一维频谱分析取复数幅值
        s = np.abs(s)  

        assert s.ndim == 1, "s为一维"
        assert s.shape[0] == freq.shape[0], "s的点数需与freq轴一致"

        data_formated["image"][qubit_name] = [freq, s]  
    return data_formated

def spectrum_convert(result):
    return nnspectrum_convert(result)