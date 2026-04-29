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



def singleshot_convert(result):
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(result.keys()):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        data = result[qubit_name]
        if type(data)==list:
            data_arr = np.array(data)
            I_channel = data_arr[:, 1]
            Q_channel = data_arr[:, 2]
            X_channel = data_arr[:, 3]
            Y_channel = data_arr[:, 4]

        elif data.dtype.names:
            time = data['f0']  # 时间/索引
            I_channel = data['f1']  # Is | I
            Q_channel = data['f2']  # Qs | I
            X_channel = data['f3']  # Is | X
            Y_channel = data['f4']  # Qs | X

        s0 = I_channel + 1j * Q_channel  # 复数 s0 (I 通道)
        s1 = X_channel + 1j * Y_channel  # 复数 s1 (X 通道)
        data_formated["image"][qubit_name] = (s0, s1)
    return data_formated


def s21_convert(result):
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(result.keys()):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        data = result[qubit_name]
        if type(data)==list:
            # 双层[[0, 1, 2, 3..7],,,20个]
            data_arr = np.array(data)
            freq = data_arr[:, 0]
            phi = data_arr[:, 2]
            I_channel = data_arr[:, 3]
            Q_channel = data_arr[:, 4]

        elif data.dtype.names:
            # f0 = data['f0']
            # f1 = data['f1']
            # f2 = data['f2']
            # f3 = data['f3']
            # f4 = data['f4']
            # f5 = data['f5']
            # f6 = data['f6']
            # f7 = data['f7']
            freq = data['f0']  # 时间/索引
            amp = data['f1']
            phi = data['f2']
            I_channel = data['f3']  # Is | I
            Q_channel = data['f4']  # Qs | I

        s = I_channel + 1j * Q_channel  # 复数 s0 (I 通道)

        amp2 = np.abs(s)
        phi2 = np.unwrap(np.angle(s))
        phi_processed = scipy.signal.detrend(phi, type='linear')
        phi2_processed = scipy.signal.detrend(phi2, type='linear')

        data_formated["image"][qubit_name] = (freq, amp2,phi2_processed)


    return data_formated


def s21multi_convert(result):
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(result.keys()):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        data = result[qubit_name]
        if type(data)==list:
            # 双层[[0, 1, 2, 3..7],,,20个]
            data_arr = np.array(data)
            freq = data_arr[:, 0]
            phi = data_arr[:, 2]
            I_channel = data_arr[:, 3]
            Q_channel = data_arr[:, 4]

        elif data.dtype.names:
            # f0 = data['f0']
            # f1 = data['f1']
            # f2 = data['f2']
            # f3 = data['f3']
            # f4 = data['f4']
            # f5 = data['f5']
            # f6 = data['f6']
            # f7 = data['f7']
            freq = data['f0']  # 时间/索引
            amp = data['f1']
            phi = data['f2']
            I_channel = data['f3']  # Is | I
            Q_channel = data['f4']  # Qs | I

        s = I_channel + 1j * Q_channel  # 复数 s0 (I 通道)

        amp2 = np.abs(s)
        phi2 = np.unwrap(np.angle(s))
        phi_processed = scipy.signal.detrend(phi, type='linear')
        phi2_processed = scipy.signal.detrend(phi2, type='linear')

        data_formated["image"][qubit_name] = (freq, amp2,phi2_processed)

    return data_formated


def s21vsflux_convert(result):
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(result.keys()):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        data = result[qubit_name]
        if type(data)==list:
            data_arr = np.array(data)

            freq = data_arr[:, 0]
            volt = data_arr[:, 1]
            I_channel = data_arr[:, 4]
            Q_channel = data_arr[:, 5]
        elif data.dtype.names:
            f0 = data['f0']
            f1 = data['f1']
            f2 = data['f2']
            f3 = data['f3']
            f4 = data['f4']
            f5 = data['f5']
            f6 = data['f6']
            f7 = data['f7']
            f8 = data['f8']

            freq = data['f0']  # 时间/索引
            volt = data['f1']
            I_channel = data['f4']  # Is | I
            Q_channel = data['f5']  # Qs | I

        s = I_channel + 1j * Q_channel  # 复数 s0 (I 通道)

        amp = np.abs(s)
        unique_freq = np.unique(freq)  # 得到16个唯一频率值
        unique_volt = np.unique(volt)  # 得到11个唯一电压值

        n_freq = len(unique_freq)
        n_volt = len(unique_volt)

        first_n_volt_volt = volt[:n_volt]
        is_row_major = len(np.unique(first_n_volt_volt)) == n_volt

        if is_row_major:
            # 行优先：每个频率的所有电压连续存储
            amp_2d = amp.reshape(n_freq, n_volt)
        else:
            # 列优先：每个电压的所有频率连续存储
            amp_2d = amp.reshape(n_volt, n_freq).T

        # 重塑 amp 为2D

        # 验证：检查 amp_2d 是否与原始数据一致

        data_formated["image"][qubit_name] = (unique_volt, unique_freq, amp_2d)
        # data_formated["image"][qubit_name] = (unique_freq, unique_volt, amp_2d.T)

        assert len(unique_volt) > 1, "DATA ERROR: volt length must be > 1"
        assert len(unique_freq) > 1, "DATA ERROR: freq length must be > 1"
    return data_formated


def nns21vsflux_convert(result):
    data_formated = s21vsflux_convert(result)
    return data_formated

def powershift_convert(result):
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(result.keys()):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        data = result[qubit_name]
        if data.dtype.names:
            f0 = data['f0']
            f1 = data['f1']
            f2 = data['f2']
            f3 = data['f3']
            f4 = data['f4']
            f5 = data['f5']
            f6 = data['f6']
            f7 = data['f7']
            f8 = data['f8']

            freq = data['f0']  # 时间/索引
            volt = data['f1']
            I_channel = data['f4']  # Is | I
            Q_channel = data['f5']  # Qs | I

            s = I_channel + 1j * Q_channel  # 复数 s0 (I 通道)

            amp = np.abs(s)
            unique_freq = np.unique(freq)  # 得到16个唯一频率值
            unique_volt = np.unique(volt)  # 得到11个唯一电压值

            n_freq = len(unique_freq)
            n_volt = len(unique_volt)

            first_n_volt_volt = volt[:n_volt]
            is_row_major = len(np.unique(first_n_volt_volt)) == n_volt

            if is_row_major:
                # 行优先：每个频率的所有电压连续存储
                amp_2d = s.reshape(n_freq, n_volt)
            else:
                # 列优先：每个电压的所有频率连续存储
                amp_2d = s.reshape(n_volt, n_freq).T

            # 重塑 amp 为2D

            # 验证：检查 amp_2d 是否与原始数据一致

        data_formated["image"][qubit_name] = (unique_freq, unique_volt, amp_2d.T)
        assert len(unique_volt) > 1, "DATA ERROR: volt length must be > 1"
        assert len(unique_freq) > 1, "DATA ERROR: freq length must be > 1"
    return data_formated

def t1fit_convert(result):
    data_formated = {"image": {}}

    for qubit_name, data in result.items():
        qubit_name = qubit_name.strip()
        
        if type(data)==list:
            data_arr = np.array(data)
            delay = data_arr[:, 0]
            p_x = data_arr[:, 2]
            data_formated["image"][qubit_name] = (delay, p_x)

        elif data.dtype.names:  # 结构化数组
            delay = data['f0']          # 自变量：延迟时间
            #p_i   = data['f1']          # Dependent0: P1 | I 
            p_x = data['f2']          # Dependent1: P1 | X 

            data_formated["image"][qubit_name] = (delay, p_x)

        else:
            data_formated["image"][qubit_name] = data

    return data_formated



def t2fit_convert(result):
    data_formated = {"image": {}}

    for qubit_name, data in result.items():
        qubit_name = qubit_name.strip()
        
        if type(data)==list:
            data_arr = np.array(data)
            delay = data_arr[:, 0]
            amplitude = data_arr[:, 1]
            data_formated["image"][qubit_name] = (delay, amplitude)

        elif data.dtype.names:   
            delay = data['f0']      
            # p1    = data['f6']      
            amplitude = data['f1']

            data_formated["image"][qubit_name] = (delay, amplitude)
            
        else:
            data_formated["image"][qubit_name] = data

    return data_formated


def nnspectrum_convert(result):
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(result.keys()):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        data = result[qubit_name]
        if data.dtype.names:
            field_names = data.dtype.names
            
            # 时间轴 f0
            time = data[field_names[0]]

            for channel_idx in range(1, len(field_names)):
                channel_field = field_names[channel_idx]
                channel_data = data[channel_field]

                # 生成名字：qubit_1, qubit_2
                new_qubit_name = f"{qubit_name}_{channel_idx}"

                data_formated["image"][new_qubit_name] = (time, channel_data)

    return data_formated


def spectrum_convert(result):
    data_formated = {"image": {}}

    for index, qubit_name in enumerate(result.keys()):
        qubit_name = qubit_name.strip()
        assert isinstance(qubit_name, str) and len(qubit_name) > 0, "量子比特名不能为空"

        data = result[qubit_name]
        if data.dtype.names:
            field_names = data.dtype.names
            
            # 时间轴 f0
            time = data[field_names[0]]

            for channel_idx in range(1, len(field_names)):
                channel_field = field_names[channel_idx]
                channel_data = data[channel_field]

                # 生成名字：qubit_1, qubit_2
                new_qubit_name = f"{qubit_name}_{channel_idx}"

                data_formated["image"][new_qubit_name] = (time, channel_data)

    return data_formated

def rabicos_convert(result):
    data_formated = {"image": {}}

    for qubit_name, data in result.items():
        qubit_name = qubit_name.strip()
        
        if type(data)==list:
            data_arr = np.array(data)
            delay = data_arr[:, 0]
            p1 = data_arr[:, 1]
            data_formated["image"][qubit_name] = (delay, p1)

        elif data.dtype.names:   
            delay = data['f0']      
            p1    = data['f6']      
            # amplitude = data['f1']

            data_formated["image"][qubit_name] = (delay, p1)
            
        else:
            data_formated["image"][qubit_name] = data

    return data_formated


def rb_convert(result):
    """
    专门处理 XEB Reference 类型数据（k × m 二维结构）
    按照用户建议：先按 k 分组，再对相同 m 的所有 k 求平均
    """
    data_formated = {"image": {}}

    for qubit_name, data in result.items():
        qubit_name = qubit_name.strip()
        
        if data.dtype.names:
            k  = data['f0']   # 序列组索引
            m  = data['f1']   # 序列深度 (横坐标)
            p0 = data['f2']   # |0> 概率
            p1 = data['f3']   # |1> 概率
            
            # ==================== 关键处理逻辑 ====================
            # 1. 获取唯一的 m 值（作为最终横坐标）
            unique_m = np.sort(np.unique(m))
            
            # 2. 对每个 m，收集所有 k 对应的 P1，并求平均
            avg_p1 = np.zeros(len(unique_m))
            
            for i, um in enumerate(unique_m):
                mask = (m == um)
                avg_p1[i] = p1[mask].mean()          # 对相同 m 的所有 k 取平均
            
            # 可选：使用 1 - P0 作为激发态概率（根据服务器习惯选择）
            # avg_p1 = (1.0 - p0[mask]).mean()
            
            # y_ref 使用零数组（reference 数据通常只有一条主曲线）
            y_ref = np.zeros_like(avg_p1)
            
            # ==================== 输出格式 ====================
            data_formated["image"][qubit_name] = [unique_m, [avg_p1, y_ref]]
            
        else:
            data_formated["image"][qubit_name] = data

    return data_formated



def xeb_convert(result):
    """
    专门处理 XEB Reference 类型数据（k × m 二维结构）
    按照用户建议：先按 k 分组，再对相同 m 的所有 k 求平均
    """
    data_formated = {"image": {}}

    for qubit_name, data in result.items():
        qubit_name = qubit_name.strip()
        
        if data.dtype.names:
            k  = data['f0']   # 序列组索引
            m  = data['f1']   # 序列深度 (横坐标)
            p0 = data['f2']   # |0> 概率
            p1 = data['f3']   # |1> 概率
            
            # ==================== 关键处理逻辑 ====================
            # 1. 获取唯一的 m 值（作为最终横坐标）
            unique_m = np.sort(np.unique(m))
            
            # 2. 对每个 m，收集所有 k 对应的 P1，并求平均
            avg_p1 = np.zeros(len(unique_m))
            
            for i, um in enumerate(unique_m):
                mask = (m == um)
                avg_p1[i] = p1[mask].mean()          # 对相同 m 的所有 k 取平均
            
            # 可选：使用 1 - P0 作为激发态概率（根据服务器习惯选择）
            # avg_p1 = (1.0 - p0[mask]).mean()
            
            # y_ref 使用零数组（reference 数据通常只有一条主曲线）
            y_ref = np.zeros_like(avg_p1)
            
            # ==================== 输出格式 ====================
            data_formated["image"][qubit_name] = [unique_m, [avg_p1, y_ref]]
            
        else:
            data_formated["image"][qubit_name] = data

    return data_formated