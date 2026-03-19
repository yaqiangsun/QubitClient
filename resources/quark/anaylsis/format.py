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
        data_dict = result["data"]
        for key in ("population", "iq_avg", "iq"):
            if key in data_dict:
                matched_key = key
                raw_data = np.array(data_dict[key])
                break
        else:
            raise ValueError(
                f"未检测到有效数据关键词（population/iq_avg/iq），"
                f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
            )

        if raw_data.ndim == 3:
            raw = np.array(raw_data[:, :, index])
        else:
            raw = np.array(raw_data)
        logging.info(f"optpipulse | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            waveforms = raw.astype(np.float64)
        else:
            # iq_avg为复数，取模得到实数波形  但是iq的维度要做特殊处理
            waveforms = np.abs(raw.astype(np.complex64)).astype(np.float64)

        # 统一格式校验
        if waveforms.ndim != 2:
            raise ValueError(
                f"optpipulse数据格式不符合要求：waveforms应为2维数组，"
                f"实际为{waveforms.ndim}维，形状{waveforms.shape}"
            )
        if x_array.ndim != 1:
            raise ValueError(
                f"optpipulse数据格式不符合要求：x_array应为1维数组，"
                f"实际为{x_array.ndim}维，形状{x_array.shape}"
            )
        if waveforms.shape[1] != x_array.shape[0]:
            raise ValueError(
                f"optpipulse数据格式不符合要求：waveforms的第1维长度({waveforms.shape[1]})"
                f"需与x_array的第0维长度({x_array.shape[0]})一致"
            )

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

        data_dict = result["data"]
        for key in ("population", "iq_avg", "iq"):
            if key in data_dict:
                matched_key = key
                raw_data = np.array(data_dict[key])
                break
        else:
            raise ValueError(
                f"未检测到有效数据关键词（population/iq_avg/iq），"
                f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
            )

        if raw_data.ndim == 3:
            raw = np.array(raw_data[:, :, index])
        else:
            raw = np.array(raw_data)
        logging.info(f"delta | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            waveforms = -raw.astype(np.float64)
        else:
            # iq_avg 为复数，取模后取负 这个时候调用的还是opt_pi的分析 所以要去负
            waveforms = -np.abs(raw.astype(np.complex64))  # 但是iq这个维度有问题 这儿还未处理

        if waveforms.ndim != 2:
            raise ValueError(
                f"delta数据格式不符合服务器要求：waveforms应为2维数组，"
                f"实际为{waveforms.ndim}维，形状{waveforms.shape}"
            )
        if x_array.ndim != 1:
            raise ValueError(
                f"delta数据格式不符合服务器要求：x_array应为1维数组，"
                f"实际为{x_array.ndim}维，形状{x_array.shape}"
            )
        if waveforms.shape[1] != x_array.shape[0]:
            raise ValueError(
                f"delta数据格式不符合服务器要求：waveforms的第1维长度({waveforms.shape[1]})"
                f"需与x_array的第0维长度({x_array.shape[0]})一致"
            )

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
        data_dict = result["data"]
        for key in ("iq_avg", "iq"):
            if key in data_dict:
                matched_key = key
                raw_data = np.array(data_dict[key])
                break
        else:
            raise ValueError(
                f"未检测到有效数据关键词（iq_avg/iq），"
                f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
            )

        if raw_data.ndim == 2:
            raw = np.array(raw_data[:, index])
        elif raw_data.ndim == 3:
            raw = np.array(raw_data[:, :, index])
            if matched_key == "iq":
                raw = np.array(raw[:, 0])
                logging.info(f"s21 | qubit={qubit_name} | iq 2维数据剔除最后维后形状：{raw.shape}")
        else:
            raw = np.array(raw_data)
        logging.info(f"s21 | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        iq_avg = raw.astype(np.complex64)

        # 计算幅度和相位
        amp = np.abs(iq_avg)
        phi = np.unwrap(np.angle(iq_avg))
        phi = scipy.signal.detrend(phi, type='linear')

        if x_array.ndim != 1:
            raise ValueError(
                f"s21数据格式不符合服务器要求：x_array应为1维数组，"
                f"实际为{x_array.ndim}维，形状{x_array.shape}"
            )
        if iq_avg.ndim != 1:
            raise ValueError(
                f"s21数据格式不符合服务器要求：iq_avg应为1维数组，"
                f"实际为{iq_avg.ndim}维，形状{iq_avg.shape}"
            )
        if amp.ndim != 1:
            raise ValueError(
                f"s21数据格式不符合服务器要求：amp应为1维数组，"
                f"实际为{amp.ndim}维，形状{amp.shape}"
            )
        if amp.shape[0] != x_array.shape[0]:
            raise ValueError(
                f"s21数据格式不符合服务器要求：amp的第0维长度({amp.shape[0]})"
                f"需与x_array的第0维长度({x_array.shape[0]})一致"
            )
        if phi.ndim != 1:
            raise ValueError(
                f"s21数据格式不符合服务器要求：phi应为1维数组，"
                f"实际为{phi.ndim}维，形状{phi.shape}"
            )
        if phi.shape[0] != x_array.shape[0]:
            raise ValueError(
                f"s21数据格式不符合服务器要求：phi的第0维长度({phi.shape[0]})"
                f"需与x_array的第0维长度({x_array.shape[0]})一致"
            )

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
    data_dict = result["data"]
    for key in ("iq_avg", "iq"):
        if key in data_dict:
            matched_key = key
            raw_data = np.array(data_dict[key])
            break
    else:
        raise ValueError(
            f"未检测到有效数据关键词（iq_avg/iq），"
            f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
        )

    if raw_data.ndim == 2:
        raw = np.array(raw_data[:, 0])
    elif raw_data.ndim == 3:
        raw = np.array(raw_data[:, :, 0])
        if matched_key == "iq":
            raw = np.array(raw[:, 0])
            logging.info(f"s21multi | qubit={qubit_name} | iq 2维数据剔除最后维后形状：{raw.shape}")
    else:
        raw = np.array(raw_data)
    logging.info(f"s21multi | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
    iq_avg = raw.astype(np.complex64)

    amp = np.abs(iq_avg)
    phi = np.unwrap(np.angle(iq_avg))
    phi = scipy.signal.detrend(phi, type='linear')

    if x_array.ndim != 1:
        raise ValueError(
            f"s21multi数据格式不符合服务器要求：x_array应为1维数组，"
            f"实际为{x_array.ndim}维，形状{x_array.shape}"
        )
    if iq_avg.ndim != 1:
        raise ValueError(
            f"s21multi数据格式不符合服务器要求：iq_avg应为1维数组，"
            f"实际为{iq_avg.ndim}维，形状{iq_avg.shape}"
        )
    if amp.ndim != 1:
        raise ValueError(
            f"s21multi数据格式不符合服务器要求：amp应为1维数组，"
            f"实际为{amp.ndim}维，形状{amp.shape}"
        )
    if amp.shape[0] != x_array.shape[0]:
        raise ValueError(
            f"s21multi数据格式不符合服务器要求：amp的第0维长度({amp.shape[0]})"
            f"需与x_array的第0维长度({x_array.shape[0]})一致"
        )
    if phi.ndim != 1:
        raise ValueError(
            f"s21multi数据格式不符合服务器要求：phi应为1维数组，"
            f"实际为{phi.ndim}维，形状{phi.shape}"
        )
    if phi.shape[0] != x_array.shape[0]:
        raise ValueError(
            f"s21multi数据格式不符合服务器要求：phi的第0维长度({phi.shape[0]})"
            f"需与x_array的第0维长度({x_array.shape[0]})一致"
        )

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
        data_dict = result["data"]
        for key in ("population", "iq_avg", "iq"):
            if key in data_dict:
                matched_key = key
                raw_data = np.array(data_dict[key])
                break
        else:
            raise ValueError(
                f"未检测到有效数据关键词（population/iq_avg/iq），"
                f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
            )

        if raw_data.ndim == 3:
            raw = np.array(raw_data[:, :, index])
        else:
            raw = np.array(raw_data)
        logging.info(f"drag | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            y0y1 = raw.astype(np.float64)
        else:
            # iq_avg为复数，取模得到实数波形  iq的时候需要考虑维度问题 
            y0y1 = np.abs(raw.astype(np.complex64)).astype(np.float64)

        if x.ndim != 1:
            raise ValueError(
                f"drag数据格式不符合服务器要求：x应为1维数组，"
                f"实际为{x.ndim}维，形状{x.shape}"
            )
        if y0y1.ndim != 2:
            raise ValueError(
                f"drag数据格式不符合服务器要求：y0y1应为2维数组，"
                f"实际为{y0y1.ndim}维，形状{y0y1.shape}"
            )
        if y0y1.shape[1] != x.shape[0]:
            raise ValueError(
                f"drag数据格式不符合服务器要求：y0y1的第1维长度({y0y1.shape[1]})"
                f"需与x的第0维长度({x.shape[0]})一致"
            )

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
        data_dict = result["data"]
        for key in ("iq_avg", "iq"):
            if key in data_dict:
                matched_key = key
                raw_data = np.array(data_dict[key])
                break
        else:
            raise ValueError(
                f"未检测到有效数据关键词（iq_avg/iq），"
                f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
            )

        if raw_data.ndim == 3:
            raw = np.array(raw_data[:, :, index])
        else:
            raw = np.array(raw_data)
        logging.info(f"s21vsflux | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        s = np.abs(raw.astype(np.complex64))

        if volt.ndim != 1:
            raise ValueError(
                f"s21vsflux数据格式不符合服务器要求：volt应为1维数组，"
                f"实际为{volt.ndim}维，形状{volt.shape}"
            )
        if freq.ndim != 1:
            raise ValueError(
                f"s21vsflux数据格式不符合服务器要求：freq应为1维数组，"
                f"实际为{freq.ndim}维，形状{freq.shape}"
            )
        if s.ndim != 2:
            raise ValueError(
                f"s21vsflux数据格式不符合服务器要求：s应为2维数组，"
                f"实际为{s.ndim}维，形状{s.shape}"
            )
        if s.shape[0] != freq.shape[0]:
            raise ValueError(
                f"s21vsflux数据格式不符合服务器要求：s的第0维长度({s.shape[0]})"
                f"需与freq的第0维长度({freq.shape[0]})一致"
            )
        if s.shape[1] != volt.shape[0]:
            raise ValueError(
                f"s21vsflux数据格式不符合服务器要求：s的第1维长度({s.shape[1]})"
                f"需与volt的第0维长度({volt.shape[0]})一致"
            )

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

        data_dict = result["data"]
        for key in ("iq_avg", "iq", "population"):
            if key in data_dict:
                matched_key = key
                raw = np.array(data_dict[key])
                break
        else:
            raise ValueError(
                f"未检测到有效数据关键词（iq_avg/iq/population），"
                f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
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

        if s0.ndim != 1:
            raise ValueError(
                f"singleshot数据格式不符合服务器要求：s0应为1维数组，"
                f"实际为{s0.ndim}维，形状{s0.shape}"
            )
        if s1.ndim != 1:
            raise ValueError(
                f"singleshot数据格式不符合服务器要求：s1应为1维数组，"
                f"实际为{s1.ndim}维，形状{s1.shape}"
            )

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
        data_dict = result["data"]
        for key in ("iq_avg", "population", "iq"):
            if key in data_dict:
                matched_key = key
                raw_data = np.array(data_dict[key])
                break
        else:
            raise ValueError(
                f"未检测到有效数据关键词（iq_avg/population/iq），"
                f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
            )

        if raw_data.ndim == 3:
            raw = np.array(raw_data[:, :, index])
        else:
            raw = np.array(raw_data)
        logging.info(f"nnspectrum2d | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            s = raw.astype(np.float64)
        else:
            s = raw.astype(np.complex64)

        if freq.ndim != 1:
            raise ValueError(
                f"nnspectrum2d数据格式不符合服务器要求：freq应为1维数组，"
                f"实际为{freq.ndim}维，形状{freq.shape}"
            )
        if bias.ndim != 1:
            raise ValueError(
                f"nnspectrum2d数据格式不符合服务器要求：bias应为1维数组，"
                f"实际为{bias.ndim}维，形状{bias.shape}"
            )
        if s.ndim != 2:
            raise ValueError(
                f"nnspectrum2d数据格式不符合服务器要求：s应为2维数组，"
                f"实际为{s.ndim}维，形状{s.shape}"
            )
        if s.shape[0] != bias.shape[0]:
            raise ValueError(
                f"nnspectrum2d数据格式不符合服务器要求：s的第0维长度({s.shape[0]})"
                f"需与bias的第0维长度({bias.shape[0]})一致"
            )
        if s.shape[1] != freq.shape[0]:
            raise ValueError(
                f"nnspectrum2d数据格式不符合服务器要求：s的第1维长度({s.shape[1]})"
                f"需与freq的第0维长度({freq.shape[0]})一致"
            )

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
        data_dict = result["data"]
        for key in ("iq_avg", "population", "iq"):
            if key in data_dict:
                matched_key = key
                raw_data = np.array(data_dict[key])
                break
        else:
            raise ValueError(
                f"未检测到有效数据关键词（iq_avg/population/iq），"
                f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
            )

        if raw_data.ndim == 3:
            raw = np.array(raw_data[:, :, index])
        else:
            raw = np.array(raw_data)
        logging.info(f"spectrum2d | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            s = raw.astype(np.float64)
        else:
            s = raw.astype(np.complex64)

        if freq.ndim != 1:
            raise ValueError(
                f"spectrum2d数据格式不符合服务器要求：freq应为1维数组，"
                f"实际为{freq.ndim}维，形状{freq.shape}"
            )
        if bias.ndim != 1:
            raise ValueError(
                f"spectrum2d数据格式不符合服务器要求：bias应为1维数组，"
                f"实际为{bias.ndim}维，形状{bias.shape}"
            )
        if s.ndim != 2:
            raise ValueError(
                f"spectrum2d数据格式不符合服务器要求：s应为2维数组，"
                f"实际为{s.ndim}维，形状{s.shape}"
            )
        if s.shape[0] != bias.shape[0]:
            raise ValueError(
                f"spectrum2d数据格式不符合服务器要求：s的第0维长度({s.shape[0]})"
                f"需与bias的第0维长度({bias.shape[0]})一致"
            )
        if s.shape[1] != freq.shape[0]:
            raise ValueError(
                f"spectrum2d数据格式不符合服务器要求：s的第1维长度({s.shape[1]})"
                f"需与freq的第0维长度({freq.shape[0]})一致"
            )

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
        data_dict = result["data"]
        for key in ("iq_avg", "population", "iq"):
            if key in data_dict:
                matched_key = key
                raw = np.array(data_dict[key])
                break
        else:
            raise ValueError(
                f"未检测到有效数据关键词（iq_avg/population/iq），"
                f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
            )
        logging.info(f"rabicos | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        iq_data = raw
        if matched_key == "iq":
            if iq_data.ndim == 3:
                iq_data = iq_data[:, 0, :]
                logging.info(f"rabicos | qubit={qubit_name} | iq 3维数据剔除中间维后形状：{iq_data.shape}")

        assert iq_data.shape[1] == len(qubit_name_list), \
            f"数据的 qubit 维度 {iq_data.shape[1]} 与 qubits 数量不匹配"

        # 计算幅度
        amp_array = np.abs(iq_data[:, index])

        if x_array.ndim != 1:
            raise ValueError(
                f"rabicos数据格式不符合服务器要求：x_array应为1维数组，"
                f"实际为{x_array.ndim}维，形状{x_array.shape}"
            )
        if amp_array.ndim != 1:
            raise ValueError(
                f"rabicos数据格式不符合服务器要求：amp_array应为1维数组，"
                f"实际为{amp_array.ndim}维，形状{amp_array.shape}"
            )
        if amp_array.shape[0] != x_array.shape[0]:
            raise ValueError(
                f"rabicos数据格式不符合服务器要求：amp_array的第0维长度({amp_array.shape[0]})"
                f"需与x_array的第0维长度({x_array.shape[0]})一致"
            )

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
        data_dict = result["data"]
        for key in ("population", "iq_avg", "iq"):
            if key in data_dict:
                matched_key = key
                raw_data = np.array(data_dict[key])
                break
        else:
            raise ValueError(
                f"未检测到有效数据关键词（population/iq_avg/iq），"
                f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
            )

        if raw_data.ndim == 2:
            raw = np.array(raw_data[:, index])
        elif raw_data.ndim == 3:
            raw = np.array(raw_data[:, :, index])
        else:
            raw = np.array(raw_data)
        logging.info(f"t1fit | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            population = raw.astype(np.float64)
        else:
            if matched_key == "iq" and raw.ndim == 2:
                raw = raw[:, 0]
                logging.info(f"t1fit | qubit={qubit_name} | iq 2维数据剔除最后维后形状：{raw.shape}")
            population = np.abs(raw.astype(np.complex64))

        if delay_array.ndim != 1:
            raise ValueError(
                f"t1fit数据格式不符合服务器要求：delay_array应为1维数组，"
                f"实际为{delay_array.ndim}维，形状{delay_array.shape}"
            )
        if population.ndim != 1:
            raise ValueError(
                f"t1fit数据格式不符合服务器要求：population应为1维数组，"
                f"实际为{population.ndim}维，形状{population.shape}"
            )
        if population.shape[0] != delay_array.shape[0]:
            raise ValueError(
                f"t1fit数据格式不符合服务器要求：population的第0维长度({population.shape[0]})"
                f"需与delay_array的第0维长度({delay_array.shape[0]})一致"
            )

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
        data_dict = result["data"]
        for key in ("population", "iq_avg", "iq"):
            if key in data_dict:
                matched_key = key
                raw_data = np.array(data_dict[key])
                break
        else:
            raise ValueError(
                f"未检测到有效数据关键词（population/iq_avg/iq），"
                f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
            )

        if raw_data.ndim == 2:
            raw = np.array(raw_data[:, index])
        elif raw_data.ndim == 3:
            raw = np.array(raw_data[:, :, index])
        else:
            raw = np.array(raw_data)
        logging.info(f"t2fit | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            population = raw.astype(np.float64)
        else:
            if matched_key == "iq" and raw.ndim == 2:
                raw = raw[:, 0]
                logging.info(f"t2fit | qubit={qubit_name} | iq 2维数据剔除最后维后形状：{raw.shape}")
            population = np.abs(raw.astype(np.complex64))

        if delay_array.ndim != 1:
            raise ValueError(
                f"t2fit数据格式不符合服务器要求：delay_array应为1维数组，"
                f"实际为{delay_array.ndim}维，形状{delay_array.shape}"
            )
        if population.ndim != 1:
            raise ValueError(
                f"t2fit数据格式不符合服务器要求：population应为1维数组，"
                f"实际为{population.ndim}维，形状{population.shape}"
            )
        if population.shape[0] != delay_array.shape[0]:
            raise ValueError(
                f"t2fit数据格式不符合服务器要求：population的第0维长度({population.shape[0]})"
                f"需与delay_array的第0维长度({delay_array.shape[0]})一致"
            )

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
    data_dict = result["data"]
    for key in ("iq_avg", "iq", "population"):
        if key in data_dict:
            iq_data = np.array(data_dict[key])
            break
    else:
        raise ValueError(
            f"未检测到有效数据关键词（iq_avg/iq/population），"
            f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
        )

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

        data_dict = result["data"]
        for key in ("iq_avg", "population", "iq"):
            if key in data_dict:
                matched_key = key
                raw_data = np.array(data_dict[key])
                break
        else:
            raise ValueError(
                f"未检测到有效数据关键词（iq_avg/population/iq），"
                f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
            )

        if raw_data.ndim == 2:
            raw = np.array(raw_data[:, index])
        elif raw_data.ndim == 3:
            raw = np.array(raw_data[:, :, index])
        else:
            raw = np.array(raw_data)
        logging.info(f"nnspectrum | qubit={qubit_name} | key={matched_key} | shape={raw.shape}")
        if matched_key == "population":
            s = raw.astype(np.float64)
        else:
            if matched_key == "iq" and raw.ndim == 2:
                raw = raw[:, 0]
                logging.info(f"nnspectrum | qubit={qubit_name} | iq 2维数据剔除最后维后形状：{raw.shape}")
            # iq/iq_avg为复数，一维频谱取幅值
            s = np.abs(raw.astype(np.complex64))

        if freq.ndim != 1:
            raise ValueError(
                f"nnspectrum数据格式不符合服务器要求：freq应为1维数组，"
                f"实际为{freq.ndim}维，形状{freq.shape}"
            )
        if s.ndim != 1:
            raise ValueError(
                f"nnspectrum数据格式不符合服务器要求：s应为1维数组，"
                f"实际为{s.ndim}维，形状{s.shape}"
            )
        if s.shape[0] != freq.shape[0]:
            raise ValueError(
                f"nnspectrum数据格式不符合服务器要求：s的第0维长度({s.shape[0]})"
                f"需与freq的第0维长度({freq.shape[0]})一致"
            )

        data_formated["image"][qubit_name] = [freq, s]
    return data_formated

def spectrum_convert(result):
    return nnspectrum_convert(result)

def rb_convert(result):
    """
    将 quark 格式的 Randomized Benchmarking 数据转换为 qubitclient 所需格式。
    仅支持 signal 为 "population" 的数据，iq_avg 类型将被明确拒绝。
    
    输出格式：
        {"image": {"qubit_name": [x_array, [y_main, y_ref]]} }
    其中：
      - y_main 用于拟合（ref 的 1 - population）
      - y_ref 为参考曲线（X gate 的 1 - population，或与 y_main 等长的全零数组）

    Args:
        result (dict): 原始实验数据字典（需包含 meta/data）

    Returns:
        dict: 转换后的格式数据
    """
    if not isinstance(result, dict) or "meta" not in result or "data" not in result:
        raise ValueError("输入数据缺少 'meta' 或 'data' 字段")

    # 提取量子比特名称
    qubits = result["meta"].get("other", {}).get("qubits", [])
    if not qubits:
        raise ValueError("meta.other 中缺少 qubits 字段或为空")

    # 提取 cycle 轴（Clifford 数 / 序列长度）
    if "cycle" not in result["meta"].get("axis", {}):
        raise ValueError("缺少 cycle 轴定义")
    x_array = np.asarray(result["meta"]["axis"]["cycle"]["def"], dtype=np.float64)
    if x_array.ndim != 1:
        raise ValueError("cycle 轴应为一维数组")

    signal_type = result["meta"]["other"].get("signal", "").lower()
    data_formatted = {"image": {}}

    if signal_type != "population":
        raise ValueError(
            f"当前版本仅支持 signal='population'，实际得到 signal='{signal_type}'"
        )

    # ────────────────────────────────────────────────
    # 仅处理 population 情况
    # ────────────────────────────────────────────────
    if "population" not in result["data"]:
        raise ValueError("signal 为 population，但数据中缺少 'population' 字段")

    pop_data = np.asarray(result["data"]["population"], dtype=np.float64)

    if pop_data.ndim < 3:
        raise ValueError(f"population 数据维度过低（至少需要 3 维）：{pop_data.shape}")

    # 压缩多余维度
    while pop_data.ndim > 3:
        pop_data = pop_data.mean(axis=-1)

    n_gates, n_qubits_in_data, n_points = pop_data.shape[:3]

    if n_points != len(x_array):
        raise ValueError(f"cycle 长度 {len(x_array)} 与 population 点数 {n_points} 不匹配")

    # 检查 qubit 维度是否匹配
    if n_qubits_in_data != len(qubits):
        # 尝试转置：可能是 (n_gates, n_points, n_qubits)
        if pop_data.shape[1] == len(qubits):
            pop_data = np.transpose(pop_data, (0, 2, 1))
            n_gates, n_qubits_in_data, n_points = pop_data.shape
        else:
            raise ValueError(
                f"qubit 数量不匹配：数据维度 {pop_data.shape} vs meta qubits {len(qubits)}"
            )

    # 转换为激发态概率：1 - population
    exc_data = 1.0 - pop_data

    for i, qname in enumerate(qubits):
        qname = qname.strip()
        if not qname:
            continue

        if n_gates == 1:
            # 只有 ref
            y_main = exc_data[0, i, :]
            # y_ref 使用全零数组，与 y_main 形状相同
            y_ref = np.zeros_like(y_main)
        elif n_gates == 2:
            # ref + X，拟合使用 ref 的激发态概率
            y_main = exc_data[0, i, :]   # ref 的 1 - P0 用于拟合
            y_ref  = exc_data[1, i, :]   # X gate 的 1 - P0 作为参考曲线
        else:
            # 非标准情况，抛出错误（严格控制）
            raise ValueError(
                f"{qname} 的 gate 类型数 {n_gates} 不为 1 或 2，无法处理"
            )

        data_formatted["image"][qname] = [x_array, [y_main, y_ref]]

    return data_formated
