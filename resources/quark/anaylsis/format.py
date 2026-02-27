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
        # 最终格式校验
        assert iq_avg.ndim == 1, "iq_avg为一维"

        assert amp.shape[0] == x_points, "amp点数需与x轴一致"
        assert phi.shape[0] == x_points, "phi点数需与x轴一致"

        # 转换成所需的标准格式
        data_formated["image"][qubit_name] = (x_array, amp,phi)
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