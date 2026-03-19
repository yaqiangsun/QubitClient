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
        if "amp" in result["meta"]["axis"]:     
            x_array = np.array(result["meta"]["axis"]["amp"]["def"], dtype=np.float64)
            amp_points = len(x_array)
        else:
            raise ValueError("optpipulse数据缺少AMP轴定义")

        # 处理Population波形
        if "population" in result["data"]:
            waveforms = np.array(result["data"]["population"][:,:,index], dtype=np.float64)
        else:
            raise ValueError("optpipulse数据缺少Population轴定义")

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
        if "freq" in result["meta"]["axis"]:
            x_array = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)
            x_points = len(x_array)
        else:
            raise ValueError("数据缺少freq定义")

        # 处理iq_avg波形
        if "iq_avg" in result["data"]:
            iq_avg = np.array(result["data"]["iq_avg"][:, index], dtype=np.complex64)
            amp = np.abs(iq_avg)
        else:
            raise ValueError("数据缺少iq_avg定义")
        # 去基线
        # indices = np.arange(len(amp))
        # coeffs = np.polyfit(indices, amp, deg=5)
        # trend = np.polyval(coeffs, indices)
        # amp = amp - trend

        phi = np.angle(iq_avg)
        phi = np.unwrap(np.angle(iq_avg))
        import scipy
        phi = scipy.signal.detrend(phi, type='linear')
        # 最终格式校验
        assert x_array.ndim == 1, "x轴需为一维数组"
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

        if "lamb" in result["meta"]["axis"]:
            x = np.array(result["meta"]["axis"]["lamb"]["def"], dtype=np.float64)
        else:
            raise ValueError("drag数据缺少LAMB轴定义")

        # 处理Population波形
        if "population" in result["data"]:
            y0y1 = np.array(result["data"]["population"][:,:, index], dtype=np.float64)
        else:
            raise ValueError("drag数据缺少Population轴定义")

        assert x.ndim == 1, "x为一维"
        assert y0y1.ndim == 2, "y0y1为二维"
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

        # 提取轴数据
        if "freq" not in result["meta"]["axis"]:
            raise ValueError("s21vsflux数据缺少freq轴定义")
        volt = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)
        assert volt.ndim == 1, "volt轴需为一维数组"

        if "read_bias" not in result["meta"]["axis"]:
            raise ValueError("s21vsflux数据缺少read_bias轴定义")
        freq = np.array(result["meta"]["axis"]["read_bias"]["def"], dtype=np.float64)
        assert freq.ndim == 1, "freq轴需为一维数组"

        # 处理iq_avg波形
        if "iq_avg" not in result["data"]:
            raise ValueError("s21vsflux数据缺少iq_avg字段")
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

        # 提取轴数据
        if "freq" not in result["meta"]["axis"]:
            raise ValueError("nns21vsflux数据缺少freq轴定义")
        volt = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)
        assert volt.ndim == 1, "volt轴需为一维数组"

        if "read_bias" not in result["meta"]["axis"]:
            raise ValueError("nns21vsflux数据缺少read_bias轴定义")
        freq = np.array(result["meta"]["axis"]["read_bias"]["def"], dtype=np.float64)
        assert freq.ndim == 1, "freq轴需为一维数组"

        # 处理iq_avg波形
        if "iq_avg" not in result["data"]:
            raise ValueError("nns21vsflux数据缺少iq_avg字段")
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

        # 处理IQ数据
        if "iq" not in result["data"]:
            raise ValueError("singleshot数据缺少iq字段")
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

        # 提取轴数据
        if "freq" not in result["meta"]["axis"]:
            raise ValueError("nnspectrum2d数据缺少freq轴定义")
        freq = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)
        assert freq.ndim == 1, "freq轴需为一维数组"

        if "bias" not in result["meta"]["axis"]:
            raise ValueError("nnspectrum2d数据缺少bias轴定义")
        bias = np.array(result["meta"]["axis"]["bias"]["def"], dtype=np.float64)
        assert bias.ndim == 1, "bias轴需为一维数组"

        # 处理iq_avg波形
        if "iq_avg" in result["data"]:
            s = np.array(result["data"]["iq_avg"][:, :, index], dtype=np.complex64)
        elif "population" in result["data"]:
            s = np.array(result["data"]["population"][:, :, index], dtype=np.complex64)
        else:
            raise ValueError("nnspectrum2d数据缺少iq_avg或population字段")

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

        # 提取轴数据
        if "freq" not in result["meta"]["axis"]:
            raise ValueError("spectrum2d数据缺少freq轴定义")
        freq = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)
        assert freq.ndim == 1, "freq轴需为一维数组"

        if "bias" not in result["meta"]["axis"]:
            raise ValueError("spectrum2d数据缺少bias轴定义")
        bias = np.array(result["meta"]["axis"]["bias"]["def"], dtype=np.float64)
        assert bias.ndim == 1, "bias轴需为一维数组"

        # 处理iq_avg波形
        if "iq_avg" in result["data"]:
            s = np.array(result["data"]["iq_avg"][:, :, index], dtype=np.complex64)
        elif "population" in result["data"]:
            s = np.array(result["data"]["population"][:, :, index], dtype=np.complex64)
        else:
            raise ValueError("spectrum2d数据缺少iq_avg或population字段")

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
        if "amp" in result["meta"]["axis"]:
            x_array = np.array(result["meta"]["axis"]["amp"]["def"], dtype=np.float64)
        elif "drive_amp" in result["meta"]["axis"]:
            x_array = np.array(result["meta"]["axis"]["drive_amp"]["def"], dtype=np.float64)
        else:
            raise ValueError("rabicos数据缺少amp轴定义")
        assert x_array.ndim == 1, "amp/drive_amp 轴需为一维数组"

        # 获取 IQ 数据并计算幅度
        if "iq_avg" not in result["data"]:
            raise ValueError("rabicos数据缺少iq_avg字段")
        iq_data = result["data"]["iq_avg"]
        assert iq_data.shape[1] == len(qubit_name_list), \
            f"iq_avg 的 qubit 维度 {iq_data.shape[1]} 与 qubits 数量不匹配"

        # 计算幅度（Rabi 通常使用幅度）
        amp_array = np.abs(iq_data[:, index])   # shape: (n_amp,)

        # 最终格式校验
        assert amp_array.ndim == 1, "amp_array 应为一维数组"
        assert amp_array.shape[0] == x_array.shape[0], \
            f"{qubit_name} 的 amp_array 长度与 amp/drive_amp 不匹配"

        # 转换成所需的标准格式
        data_formated["image"][qubit_name] = (x_array, amp_array)
    
    return data_formated


def t1fit_convert(result):
    """
    将 quark 格式的 T1 弛豫数据转换为 qubitclient 所需格式
    支持 signal 为 'population' 或 'iq_avg'，且存在 delay 轴的数据
    Args:
        result (dict): 原始实验数据字典（需包含 meta/data 核心字段）
    Returns:
        dict: 符合服务器要求的格式数据 {"image": {qubit_name: (delay_array, decay_curve)}}
        其中 decay_curve 为一维实数数组（衰减曲线，已强制非负）
    """
    data_formated = {"image": {}}
    if "meta" not in result or "data" not in result:
        raise ValueError("数据缺少 'meta' 或 'data' 字段")

    meta = result["meta"]
    data = result["data"]
    
    # 1. 检查信号类型
    signal = meta.get("other", {}).get("signal", "")
    if signal not in ["population", "iq_avg"]:
        raise ValueError(f"T1 拟合只支持 signal='population' 或 'iq_avg'，当前为：{signal!r}")

    # 2. 检查 delay 轴
    axis = meta.get("axis", {})
    if "delay" not in axis or "def" not in axis["delay"]:
        raise ValueError("缺少 delay 轴，无法进行 T1 拟合")
    
    # 排除明显的多参数扫描（N_list）
    if "N_list" in axis or "N_list" in meta.get("other", {}):
        raise ValueError("检测到 N_list 轴，此数据为多轮重复实验或变参扫描，不适合直接 T1 拟合")
    
    delay_array = np.array(axis["delay"]["def"], dtype=np.float64)
    if delay_array.ndim != 1:
        raise ValueError("delay 轴必须是一维数组")

    # 3. 获取量子比特列表
    qubits = [q.strip() for q in meta.get("other", {}).get("qubits", [])]
    if not qubits:
        raise ValueError("meta.other 中缺少 qubits 字段")


    # 4. 处理 population（支持二维和三维情况）
    if signal == "population":
        if "population" not in data and "P0" not in data:
            raise ValueError("signal=population 但 data 中缺少 'population' 或 'P0' 字段")
        
        # 兼容两种可能的 key 名
        pop_key = "population" if "population" in data else "P0"
        pop_data = np.array(data[pop_key], dtype=np.float64)
        
        # 维度规范化：接受 2D 或 3D
        if pop_data.ndim == 2:
            # 标准 2D: (n_delay, n_qubit)
            if pop_data.shape[0] != len(delay_array):
                raise ValueError(f"population 第一维 {pop_data.shape[0]} 与 delay 长度 {len(delay_array)} 不匹配")
            if pop_data.shape[1] != len(qubits):
                raise ValueError(f"population 第二维 {pop_data.shape[1]} 与 qubits 数量 {len(qubits)} 不匹配")
            
            for i, qubit in enumerate(qubits):
                decay_curve = np.maximum(pop_data[:, i], 0.0)  # 强制非负
                data_formated["image"][qubit] = (delay_array, decay_curve)
        
        elif pop_data.ndim == 3:
            # 常见三维情况：(n_delay, n_extra, n_qubit)，n_extra 通常=1
            if pop_data.shape[0] != len(delay_array):
                raise ValueError(f"population 第0维 {pop_data.shape[0]} 与 delay 不匹配")
            
            n_extra = pop_data.shape[1]
            n_qubit_in_data = pop_data.shape[2]
            
            if n_qubit_in_data != len(qubits):
                raise ValueError(f"population 第2维 {n_qubit_in_data} 与 qubits 数量 {len(qubits)} 不匹配")
            
            # 取中间维度（通常为1），并 squeeze
            if n_extra != 1:
                print(f"警告：population 中间维度为 {n_extra}（非1），将取第一层数据")
            
            pop_squeezed = pop_data[:, 0, :]  # 取 [:, 0, :]
            
            for i, qubit in enumerate(qubits):
                decay_curve = np.maximum(pop_squeezed[:, i], 0.0)
                data_formated["image"][qubit] = (delay_array, decay_curve)
        
        else:
            raise ValueError(f"不支持的 population 维度：{pop_data.shape}（仅支持 2D 或 3D）")

    # 5. 处理 iq_avg（保持原有逻辑，暂不考虑三维）
    elif signal == "iq_avg":
        if "iq_avg" not in data:
            raise ValueError("signal=iq_avg 但 data 中缺少 'iq_avg' 字段")
            
        iq_data = np.array(data["iq_avg"], dtype=np.complex128)
        
        if iq_data.ndim != 2:
            raise ValueError(f"iq_avg 预期为二维数组，实际维度：{iq_data.shape}")
        
        if iq_data.shape[0] != len(delay_array):
            raise ValueError(f"iq_avg 第一维与 delay 不匹配")
        if iq_data.shape[1] != len(qubits):
            raise ValueError(f"iq_avg 第二维与 qubits 数量不匹配")
        
        amp_data = np.abs(iq_data)
        
        for i, qubit in enumerate(qubits):
            decay_curve = np.maximum(amp_data[:, i], 0.0)
            data_formated["image"][qubit] = (delay_array, decay_curve)
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
        if "delay" not in result["meta"]["axis"]:
            raise ValueError("t2fit数据缺少delay轴定义")
        delay_array = np.array(result["meta"]["axis"]["delay"]["def"], dtype=np.float64)
        assert delay_array.ndim == 1, "delay 轴需为一维数组"

        # 处理 population 波形（Ramsey 实验中最常用的字段）
        if "population" not in result["data"]:
            raise ValueError("t2fit数据缺少population字段")
        population = np.array(result["data"]["population"][:, index], dtype=np.float64)
        
        # 最终格式校验
        assert population.ndim == 1, "population 应为一维数组"
        assert population.shape[0] == delay_array.shape[0], \
            f"{qubit_name} 的 population 长度与 delay 轴不匹配"

        # 转换成所需的标准格式
        data_formated["image"][qubit_name] = (delay_array, population)
    
    return data_formated

def powershift_convert(result):
    """
    将quark格式数据转换为qubitclient所需格式
    适配多比特场景：iq_avg最后一维为比特索引（如(21,21,2)对应2个比特）
    Args:
    result (dict): 原始实验数据字典（需包含meta/data核心字段）
    Returns:
        dict: 符合服务器要求的格式数据
    """
    qubit_name_list = result["meta"]["other"]["qubits"]
    data_formated = {
        "image": {
        }
    }
    if "amp" not in result["meta"]["axis"]:
        raise ValueError(f"数据中缺少 amp 轴，当前轴: {list(result['meta']['axis'].keys())}")
    if "freq" not in result["meta"]["axis"]:
        raise ValueError(f"数据中缺少 freq 轴，当前轴: {list(result['meta']['axis'].keys())}")
    amp_axis = np.array(result["meta"]["axis"]["amp"]["def"], dtype=np.float64)
    freq_axis = np.array(result["meta"]["axis"]["freq"]["def"], dtype=np.float64)
    assert amp_axis.ndim == 1 and freq_axis.ndim == 1, "轴需为一维数组"

    if "iq_avg" not in result["data"]:
        raise ValueError("数据中缺少 iq_avg 字段，无法提取数据")
    iq_data = result["data"]["iq_avg"]

    if iq_data.ndim != 3:
        raise ValueError(
            f"iq_avg维度不符合预期: {iq_data.shape}，仅支持3维多比特数据 (m, n, k)（k=比特数）"
        )
    s = iq_data  

    for index, qubit_name in enumerate(qubit_name_list):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        single_bit_s = s[:, :, index]
        abs_s = np.abs(single_bit_s)

        power, freq = amp_axis, freq_axis

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
        if "freq" not in result["meta"]["axis"]:
            raise ValueError("nnspectrum数据缺少freq轴定义")
        freq_key = f"$gate.R.{qubit_name}.params.frequency"
        freq = np.array(result["meta"]["axis"]["freq"].get(freq_key, result["meta"]["axis"]["freq"]["def"]), dtype=np.float64)
        assert freq.ndim == 1, "freq轴需为一维数组"
        
        # 处理IQ均值波形
        if "iq_avg" in result["data"]:
            s = np.array(result["data"]["iq_avg"][:, index], dtype=np.complex64)
        elif "population" in result["data"]:
            s = np.array(result["data"]["population"][:, index], dtype=np.complex64)
        else:
            raise ValueError("nnspectrum数据缺少iq_avg 或 population 字段")
        s = np.array(result["data"]["iq_avg"][:, index], dtype=np.complex64)
        # 一维频谱分析取复数幅值
        s = np.abs(s)  

        assert s.ndim == 1, "s为一维"
        assert s.shape[0] == freq.shape[0], "s的点数需与freq轴一致"

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

    return data_formatted