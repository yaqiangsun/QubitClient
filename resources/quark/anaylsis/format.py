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
import scipy
from .utils import (
    extract_waveform_data,
    validate_server_format,
    normalize_iq_data,
)



def optpipulse_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取AMP幅值轴
        if "amp" not in result["meta"]["axis"]:
            raise ValueError("optpipulse数据缺少AMP轴定义")
        x_array = np.array(result["meta"]["axis"]["amp"]["def"], dtype=np.float64)

        # 多关键词兼容提取波形数据
        matched_key, raw = extract_waveform_data(result, index)
        logging.info(f"optpipulse | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            waveforms = raw.astype(np.float64)
        else:
            # iq_avg为复数，取模得到实数波形  但是iq的维度要做特殊处理
            waveforms = np.abs(raw.astype(np.complex64)).astype(np.float64)

        # 统一格式校验
        validate_server_format("optpipulse", waveforms=waveforms, x_array=x_array)

        data_formated["image"][qubit_name] = (waveforms, x_array)
    return data_formated


def delta_convert(result):
    """
    将quark格式数据转换为delta所需格式
    核心适配：将所有数据转为「幅值取负的实数数组」，让波峰算法识别原波谷
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据（值为实数数组，适配波峰算法）
    """
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        if "amp" not in result["meta"]["axis"]:
            raise ValueError("delta数据缺少AMP轴定义")
        x_array = np.array(result["meta"]["axis"]["amp"]["def"], dtype=np.float64)

        matched_key, raw = extract_waveform_data(result, index)
        logging.info(f"delta | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            waveforms = -raw.astype(np.float64)
        else:
            # iq / iq_avg 为复数，取模后取负 这个时候调用的还是opt_pi的分析 所以要去负
            waveforms = -np.abs(raw.astype(np.complex64))

        validate_server_format("delta", waveforms=waveforms, x_array=x_array)

        data_formated["image"][qubit_name] = (waveforms, x_array)

    return data_formated
def s21_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        if "freq" not in result["meta"]["axis"]:
            raise ValueError("数据缺少freq定义")
        x_array = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)

        # S21需要复数数据，优先检测iq_avg和iq，理论上也是只有这两个参数
        matched_key, raw = extract_waveform_data(result, index, priority=("iq_avg", "iq"))
        logging.info(f"s21 | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        iq_avg = raw.astype(np.complex64)

        # 计算幅度和相位
        amp = np.abs(iq_avg)
        phi = np.unwrap(np.angle(iq_avg))
        phi = scipy.signal.detrend(phi, type='linear')

        validate_server_format("s21", x_array=x_array, iq_avg=iq_avg, amp=amp, phi=phi)

        data_formated["image"][qubit_name] = (x_array, amp, phi)
    return data_formated


def nns21_convert(result):
    data_formated = s21_convert(result)
    return data_formated


def s21mulit_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式（S21多峰，仅取第一个qubit）
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    qubit_name = qubit_name_list[0]
    assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

    if "freq" not in result["meta"]["axis"]:
        raise ValueError("数据缺少freq定义")
    x_array = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)

    # S21需要复数数据
    matched_key, raw = extract_waveform_data(result, 0, priority=("iq_avg", "iq"))
    logging.info(f"s21multi | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
    iq_avg = raw.astype(np.complex64)

    amp = np.abs(iq_avg)
    phi = np.unwrap(np.angle(iq_avg))
    phi = scipy.signal.detrend(phi, type='linear')

    validate_server_format("s21multi", x_array=x_array, iq_avg=iq_avg, amp=amp, phi=phi)

    data_formated["image"][qubit_name] = (x_array, amp, phi)
    return data_formated


def drag_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        if "lamb" not in result["meta"]["axis"]:
            raise ValueError("drag数据缺少LAMB轴定义")
        x = np.array(result["meta"]["axis"]["lamb"]["def"], dtype=np.float64)

        # 多关键词兼容提取波形数据
        matched_key, raw = extract_waveform_data(result, index)
        logging.info(f"drag | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            y0y1 = raw.astype(np.float64)
        else:
            # iq_avg为复数，取模得到实数波形  iq的时候需要考虑维度问题 
            y0y1 = np.abs(raw.astype(np.complex64)).astype(np.float64)

        validate_server_format("drag", x=x, y0y1=y0y1)

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
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        if "freq" not in result["meta"]["axis"]:
            raise ValueError("s21vsflux数据缺少freq轴定义")
        volt = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)

        if "read_bias" not in result["meta"]["axis"]:
            raise ValueError("s21vsflux数据缺少read_bias轴定义")
        freq = np.array(result["meta"]["axis"]["read_bias"]["def"], dtype=np.float64)

        # 取复数模值
        matched_key, raw = extract_waveform_data(result, index, priority=("iq_avg", "iq"))
        logging.info(f"s21vsflux | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        s = np.abs(raw.astype(np.complex64))

        validate_server_format("s21vsflux", volt=volt, freq=freq, s=s)

        data_formated["image"][qubit_name] = (volt, freq, s)
    return data_formated


def nns21vsflux_convert(result):
    data_formated = s21vsflux_convert(result)
    return data_formated



def singleshot_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        matched_key, raw = extract_waveform_data(
            result,
            index=None,
            priority=("iq_avg", "iq", "population")
        )
        logging.info(f"singleshot | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")

        # 校验数据维度（确保能执行[0,:,index]和[1,:,index]切片）
        if raw.ndim < 3:
            raise ValueError(
                f"singleshot数据需要至少3维数组（当前{matched_key}数据维度：{raw.ndim}），"
                f"数据形状：{raw.shape}，请确认数据格式是否符合要求"
            )
        s0 = np.array(raw[0, :, index], dtype=np.complex64)
        s1 = np.array(raw[1, :, index], dtype=np.complex64)

        validate_server_format("singleshot", s0=s0, s1=s1)

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
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        if "freq" not in result["meta"]["axis"]:
            raise ValueError("nnspectrum2d数据缺少freq轴定义")
        freq = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)

        if "bias" not in result["meta"]["axis"]:
            raise ValueError("nnspectrum2d数据缺少bias轴定义")
        bias = np.array(result["meta"]["axis"]["bias"]["def"], dtype=np.float64)

        # 多关键词兼容提取（优先iq_avg，其次population，最后iq）
        matched_key, raw = extract_waveform_data(result, index, priority=("iq_avg", "population", "iq"))
        logging.info(f"nnspectrum2d | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            s = raw.astype(np.float64)
        else:
            s = raw.astype(np.complex64)

        validate_server_format("nnspectrum2d", freq=freq, bias=bias, s=s)

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
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        if "freq" not in result["meta"]["axis"]:
            raise ValueError("spectrum2d数据缺少freq轴定义")
        freq = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)

        if "bias" not in result["meta"]["axis"]:
            raise ValueError("spectrum2d数据缺少bias轴定义")
        bias = np.array(result["meta"]["axis"]["bias"]["def"], dtype=np.float64)

        # 多关键词兼容提取
        matched_key, raw = extract_waveform_data(result, index, priority=("iq_avg", "population", "iq"))
        logging.info(f"spectrum2d | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            s = raw.astype(np.float64)
        else:
            s = raw.astype(np.complex64)

        validate_server_format("spectrum2d", freq=freq, bias=bias, s=s)

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
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        # 提取驱动幅度轴 x_array
        if "amp" in result["meta"]["axis"]:
            x_array = np.array(result["meta"]["axis"]["amp"]["def"], dtype=np.float64)
        elif "drive_amp" in result["meta"]["axis"]:
            x_array = np.array(result["meta"]["axis"]["drive_amp"]["def"], dtype=np.float64)
        else:
            raise ValueError("rabicos数据缺少amp轴定义")

        # 多关键词兼容提取
        matched_key, raw = extract_waveform_data(result, priority=("iq_avg", "population", "iq"))
        logging.info(f"rabicos | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        iq_data = raw
        if matched_key == "iq":
            iq_data = normalize_iq_data(
                iq_data,
                f"rabicos | qubit={qubit_name}",
                reduce_2d=False,
                expected_qubit_dim=len(qubit_name_list)
            )

        assert iq_data.shape[1] == len(qubit_name_list), \
            f"数据的 qubit 维度 {iq_data.shape[1]} 与 qubits 数量不匹配"

        # 计算幅度
        amp_array = np.abs(iq_data[:, index])

        validate_server_format("rabicos", x_array=x_array, amp_array=amp_array)

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
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        if "delay" not in result["meta"]["axis"]:
            raise ValueError("t1fit数据缺少delay轴定义")
        delay_array = np.array(result["meta"]["axis"]["delay"]["def"], dtype=np.float64)

        # 多关键词兼容提取
        matched_key, raw = extract_waveform_data(result, index, priority=("population", "iq_avg", "iq"))
        logging.info(f"t1fit | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            population = raw.astype(np.float64)
        else:
            if matched_key == "iq":
                raw = normalize_iq_data(
                    raw,
                    f"t1fit | qubit={qubit_name}",
                    reduce_2d=True,
                    expected_qubit_dim=len(qubit_name_list)
                )
            population = np.abs(raw.astype(np.complex64))

        validate_server_format("t1fit", delay_array=delay_array, population=population)

        data_formated["image"][qubit_name] = (delay_array, population)

    return data_formated

def ramsey_convert(result):
    return t1fit_convert(result)

def t2fit_convert(result):
    """
    将 quark 格式的 T2/Ramsey 数据转换为 qubitclient 所需格式
    Args:
        result (dict): 原始实验数据字典（需包含 meta/data 核心字段）
    Returns:
        dict: 符合服务器要求的格式数据 {"image": {qubit_name: (delay_array, population_array)}}
    """
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        if "delay" not in result["meta"]["axis"]:
            raise ValueError("t2fit数据缺少delay轴定义")
        delay_array = np.array(result["meta"]["axis"]["delay"]["def"], dtype=np.float64)

        # 多关键词兼容提取
        matched_key, raw = extract_waveform_data(result, index, priority=("population", "iq_avg", "iq"))
        logging.info(f"t2fit | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            population = raw.astype(np.float64)
        else:
            if matched_key == "iq":
                raw = normalize_iq_data(
                    raw,
                    f"t2fit | qubit={qubit_name}",
                    reduce_2d=True,
                    expected_qubit_dim=len(qubit_name_list)
                )
            population = np.abs(raw.astype(np.complex64))

        validate_server_format("t2fit", delay_array=delay_array, population=population)

        data_formated["image"][qubit_name] = (delay_array, population)

    return data_formated

def powershift_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    适配多比特场景：iq_avg最后一维为比特索引
    Args:
    result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    if "amp" not in result["meta"]["axis"]:
        raise ValueError(f"数据中缺少 amp 轴，当前轴: {list(result['meta']['axis'].keys())}")
    if "freq" not in result["meta"]["axis"]:
        raise ValueError(f"数据中缺少 freq 轴，当前轴: {list(result['meta']['axis'].keys())}")
    amp_axis = np.array(result["meta"]["axis"]["amp"]["def"], dtype=np.float64)
    freq_axis = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)
    assert amp_axis.ndim == 1 and freq_axis.ndim == 1, "轴需为一维数组"

    # 多关键词兼容提取（不切片，保留3维结构）
    _, iq_data = extract_waveform_data(result, priority=("iq_avg", "iq", "population"))

    if iq_data.ndim != 3:
        raise ValueError(
            f"数据维度不符合预期: {iq_data.shape}，仅支持3维多比特数据 (m, n, k)（k=比特数）"
        )

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        single_bit_s = iq_data[:, :, index]
        abs_s = np.abs(single_bit_s)

        power, freq = amp_axis, freq_axis

        # 裁剪逻辑
        if abs_s.shape[1] == len(power) and abs_s.shape[0] == len(freq):
            abs_s = abs_s[:-1, :-1]
        elif abs_s.shape[1] != len(power) - 1 or abs_s.shape[0] != len(freq) - 1:
            raise ValueError(f"数据维度{abs_s.shape} 与轴长度不匹配: power={len(power)}, freq={len(freq)}")

        abs_s = abs_s.T
        abs_s = abs_s[:, ::-1]
        data_formated["image"][qubit_name] = (freq, power, abs_s)

    return data_formated

def nnspectrum_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式（一维频谱专用）
    Args:
        result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 服务器要求的格式数据
    """
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        if "freq" not in result["meta"]["axis"]:
            raise ValueError("nnspectrum数据缺少freq轴定义")
        freq_key = f"$gate.R.{qubit_name}.params.frequency"
        freq = np.array(result["meta"]["axis"]["freq"].get(freq_key, result["meta"]["axis"]["freq"]["def"]), dtype=np.float64)

        matched_key, raw = extract_waveform_data(result, index, priority=("iq_avg", "population", "iq"))
        logging.info(f"nnspectrum | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            s = raw.astype(np.float64)
        else:
            if matched_key == "iq":
                raw = normalize_iq_data(
                    raw,
                    f"nnspectrum | qubit={qubit_name}",
                    reduce_2d=True,
                    expected_qubit_dim=len(qubit_name_list)
                )
            # iq/iq_avg为复数，一维频谱取幅值
            s = np.abs(raw.astype(np.complex64))

        validate_server_format("nnspectrum", freq=freq, s=s)

        data_formated["image"][qubit_name] = [freq, s]
    return data_formated

def spectrum_convert(result):
    return nnspectrum_convert(result)