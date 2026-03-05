# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/27 10:13:17
########################################################################

import logging
import numpy as np

from .utils import query_param, update_param

def optpipulse_update(data_converted, result: dict, file_idx: int = 0):
    """
    根据OptPi脉冲分析结果更新量子比特AMP参数
    Args:
        data_converted: optpipulse_convert转换后的实验数据
        result: 服务器返回的OptPi分析结果
        file_idx: 处理第几个文件的结果（默认0，单文件场景）
    """
    update_dict = {}

    if "results" not in result or not isinstance(result["results"], list):
        logging.error("OptPi结果格式错误，无有效results字段")
        return update_dict
    if file_idx < 0 or file_idx >= len(result["results"]):
        logging.error(f"OptPi file_idx={file_idx} 越界，有效范围0~{len(result['results'])-1}")
        return update_dict
    
    # 提取共峰位置和置信度
    all_params = result["results"][file_idx].get("params", [])
    all_confs = result["results"][file_idx].get("confs", [])
    
    # 遍历比特更新AMP参数
    for idx, qubit in enumerate(data_converted["image"]):
        if idx >= len(all_params) or idx >= len(all_confs):
            logging.warning(f"{qubit} 无匹配分析结果")
            continue
        
        qubit_params = all_params[idx]
        qubit_confs = all_confs[idx]
        
        # 无有效共峰点
        if not qubit_params or not qubit_confs:
            logging.warning(f"{qubit} 无有效共峰点")
            continue
        
        # 选置信度最高的共峰点
        best_conf_idx = qubit_confs.index(max(qubit_confs))
        best_peak_pos = qubit_params[best_conf_idx]
        best_conf = qubit_confs[best_conf_idx]
        
        # 计算最终AMP值
        # original_amp = 0.2 # 测试用，实际替换为query_param(f"gate.R.{qubit}.params.amp")
        original_amp = query_param(f"gate.R.{qubit}.params.amp")
        if original_amp is not None:
            final_amp = original_amp * best_peak_pos
            # 实际使用 update_param(f"gate.R.{qubit}.params.amp", final_amp)
            update_dict[f"gate.R.{qubit}.params.amp"] = final_amp
            logging.info(
                f"OptPi更新 | 比特：{qubit} | 共峰位置：{best_peak_pos:.5f} | "
                f"置信度：{best_conf:.4f} | 最终AMP：{final_amp:.5f}"
            )
        else:
            logging.warning(f"{qubit} 原始AMP参数未设置")
    return update_dict

def drag_update(data_converted, result: dict, file_idx: int = 0):
    """
    根据Drag脉冲分析结果更新量子比特beta参数
    Args:
        data_converted: drag_convert转换后的实验数据
        result: 服务器返回的Drag分析结果
        file_idx: 处理第几个文件的结果（默认0，单文件场景）
    """

    update_dict = {}

    if "results" not in result or not isinstance(result["results"], list):
        logging.error("Drag结果格式错误，无有效results字段")
        return update_dict
    if file_idx < 0 or file_idx >= len(result["results"]):
        logging.error(f"Drag file_idx={file_idx} 越界，有效范围0~{len(result['results'])-1}")
        return update_dict
    
    # 提取交点坐标和置信度
    intersections = result["results"][file_idx].get("intersections_list", [])
    confs = result["results"][file_idx].get("intersections_confs_list", [])
    
    # 遍历比特更新beta参数
    for idx, qubit in enumerate(data_converted["image"]):
 
        if idx >= len(intersections) or idx >= len(confs):
            logging.warning(f"{qubit} 无匹配分析结果，跳过beta更新")
            continue
        
        qubit_intersections = intersections[idx]
        qubit_confs = confs[idx]
        
        # 无有效交点
        if not qubit_intersections or not qubit_confs:
            logging.warning(f"{qubit} 无有效交点，跳过beta更新")
            continue
        
        # 选置信度最高的交点
        best_conf_idx = qubit_confs.index(max(qubit_confs))
        beta_offset = qubit_intersections[best_conf_idx][0]
        best_conf = qubit_confs[best_conf_idx]
        
        # 计算最终beta值
        # original_beta = 0.0 # 测试用，实际替换为query_param(f'gate.R.{qubit}.params.beta')
        original_beta = query_param(f'gate.R.{qubit}.params.beta')
        if original_beta is not None:
            final_beta = original_beta + beta_offset
            # update_param(f'gate.R.{qubit}.params.beta', final_beta)
            update_dict[f'gate.R.{qubit}.params.beta'] = final_beta
            logging.info(
                f"Drag更新 | 比特：{qubit} | 原始beta：{original_beta:.6e} | "
                f"偏差：{beta_offset:.6e} | 最终beta：{final_beta:.6e} | 置信度：{best_conf:.2f}"
            )
        else:
            logging.warning(f"{qubit} 原始beta参数未设置")
    return update_dict

def s21_update(data_converted, result: dict, file_idx: int = 0):
    """
    根据S21PEAK波谷检测结果更新量子比特读取腔的频率参数
    Args:
        data_converted: s21_convert转换后的实验数据
        result: 服务器返回的S21PEAK分析结果（波谷检测）
        file_idx: 处理第几个文件的结果（默认0，单文件场景）
    """

    update_dict = {}

    if "results" not in result or not isinstance(result["results"], list):
        logging.error("S21PEAK结果格式错误，无有效results字段")
        return update_dict
    if file_idx < 0 or file_idx >= len(result["results"]):
        logging.error(f"S21PEAK file_idx={file_idx} 越界，有效范围0~{len(result['results'])-1}")
        return update_dict
    
    # 提取波谷核心数据
    s21_result = result["results"][file_idx] if len(result["results"]) > 0 else {}
    valleys_idx = s21_result.get("peaks", [])       # 波谷在频率轴的索引（接口字段名peaks，实际是波谷）
    valleys_confs = s21_result.get("confs", [])     # 波谷置信度
    valleys_freqs = s21_result.get("freqs_list", [])# 波谷对应的读取腔频率值
    
    # 遍历每个量子比特，按索引匹配波谷结果
    for idx, qubit in enumerate(data_converted["image"]):
        if idx >= len(valleys_idx) or idx >= len(valleys_confs) or idx >= len(valleys_freqs):
            logging.warning(f"{qubit} 无匹配的S21波谷分析结果，跳读取腔频率更新")
            continue
        
        qubit_valleys_idx = valleys_idx[idx]       # 当前比特的所有波谷索引
        qubit_valleys_conf = valleys_confs[idx]    # 当前比特的波谷置信度
        qubit_valleys_freq = valleys_freqs[idx]    # 当前比特的波谷对应频率
        
        if not qubit_valleys_idx or not qubit_valleys_conf or not qubit_valleys_freq:
            logging.warning(f"{qubit} 无有效S21波谷数据")
            continue
        
        # 选择置信度最高的波谷
        best_conf_idx = qubit_valleys_conf.index(max(qubit_valleys_conf))
        best_valley_freq = qubit_valleys_freq[best_conf_idx]  # 最优波谷对应的读取腔频率
        best_valley_conf = qubit_valleys_conf[best_conf_idx]  # 最优波谷置信度
        
        # 查询原始读取腔频率并更新
        # 实际项目中替换为：original_read_freq = s.query(f'gate.Measure.{qubit}.params.frequency')
        # original_read_freq = 4.432e9  # 测试用（读取腔典型频率）
        original_read_freq = query_param(f'gate.Measure.{qubit}.params.frequency')
        if original_read_freq is not None:
            # 实际更新操作：update_param(f'gate.Measure.{qubit}.params.frequency', best_valley_freq)
            update_dict[f'gate.Measure.{qubit}.params.frequency'] = best_valley_freq
            logging.info(
                f"S21更新 | 比特：{qubit} | 原始读取腔频率：{original_read_freq*1e-9:.4f} GHz | "
                f"新读取腔频率：{best_valley_freq*1e-9:.4f} GHz | 置信度：{best_valley_conf:.2f}"
            )
        else:
            logging.warning(f"{qubit} 原始读取腔频率参数未设置，无法更新")
    return update_dict

def singleshot_update(data_converted, result: dict, file_idx: int = 0):
    """
    Singleshot结果更新
    Args:
        data_converted: singleshot_convert转换后的实验数据
        result: 服务器返回的Singleshot分析结果
        file_idx: 处理第几个文件的结果（默认0，单文件场景）
    """
    print("singleshot_update函数") # 这个似乎不用更新
    
    update_dict = {}
    return update_dict

def spectrum_update(data_converted, result: list, file_idx: int = 0):
    """
    根据SPECTRUM峰值检测结果，更新量子比特的频率参数
    Args:
        data_converted: nnspectrum_convert转换后的实验数据
        result: 服务器返回的SPECTRUM分析结果（list类型）
        file_idx: 处理第几个文件的结果（默认0，单文件场景）
    """
    
    update_dict = {}

    if not isinstance(result, list):
        logging.error("SPECTRUM结果格式错误，非list类型")
        return update_dict
    if file_idx < 0 or file_idx >= len(result):
        logging.error(f"SPECTRUM file_idx={file_idx} 越界，有效范围0~{len(result)-1}")
        return update_dict
    
    # 提取峰值和置信度
    result_dict = result[file_idx]  # 单个文件对应一个结果，取指定索引的元素
    peaks_list = result_dict.get("peaks_list", [])
    confidences_list = result_dict.get("confidences_list", [])

    if not peaks_list or not confidences_list:
        logging.warning("SPECTRUM结果中无峰值或置信度数据")
        return update_dict

    # 遍历每个量子比特，按顺序匹配结果
    qubits = list(data_converted["image"].keys())  
    for idx, qubit in enumerate(qubits):
        # 检查索引是否越界
        if idx >= len(peaks_list) or idx >= len(confidences_list):
            logging.warning(f"{qubit} 无匹配的SPECTRUM分析结果")
            continue
        
        qubit_peaks = peaks_list[idx]       # 该qubit的所有峰值频率
        qubit_confs = confidences_list[idx] # 对应峰值的置信度
        
        # 检查是否有有效峰值
        if not qubit_peaks or not qubit_confs:
            logging.warning(f"{qubit} 无有效峰值")
            continue
        
        # 找到置信度最高的峰值( 这个更新策略感觉还需要调整 归一化 然后 top-p？)
        best_conf_idx = qubit_confs.index(max(qubit_confs))
        best_peak_freq = qubit_peaks[best_conf_idx]
        best_conf = qubit_confs[best_conf_idx]
        
        # 查询原始频率并更新 
        # original_freq = s.query(f'gate.R.{qubit}.params.frequency')  # 实际项目中替换为真实函数
        # original_freq = 4.1e9 # 测试用，实际替换为query_param(f'gate.R.{qubit}.params.frequency')
        original_freq = query_param(f'gate.R.{qubit}.params.frequency')
        if original_freq is not None: # 更新没有依赖到原本的比特频率，所以这儿其实可以不用读取原本的比特频率（对实验有影响 但是对更新没影响）
            # update_param(f'gate.R.{qubit}.params.frequency', best_peak_freq)  # 实际更新操作
            update_dict[f'gate.R.{qubit}.params.frequency'] = best_peak_freq
            logging.info(
                f"✅ SPECTRUM频率更新 | 比特：{qubit} | "
                f"原始频率：{original_freq*1e-9:.4f} GHz | "
                f"新频率：{best_peak_freq*1e-9:.4f} GHz | "
                f"置信度：{best_conf:.2f}"
            )
        else:
            logging.warning(f"{qubit} 原始频率参数未设置，无法更新")
    return update_dict