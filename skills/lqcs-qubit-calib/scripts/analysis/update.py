# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:50
########################################################################

import logging
import numpy as np
import math


def optpipulse_update(data_converted, result: dict, file_idx: int = 0, conf_threshold: float = 0.7):
    """
    根据OptPi脉冲分析结果更新量子比特AMP参数
    Args:
        data_converted: optpipulse_convert转换后的实验数据
        result: 服务器返回的OptPi分析结果
        file_idx: 如果服务器同时处理了多个批次的实验数据，选择处理第几个的结果（默认0）
        conf_threshold: 置信度阈值
    """
    update_dict = {}

    file_result = validate_result(result, file_idx, "OptPi")
    if file_result is None:
        return update_dict

    all_params = file_result.get("params", [])
    all_confs = file_result.get("confs", [])

    image = data_converted.get("image", [])
    qubits = list(image.keys()) if isinstance(image, dict) else image
    for idx, qubit in enumerate(qubits):
        if not validate_list_bounds(idx, {"params": all_params, "confs": all_confs}, qubit, "OptPi"):
            continue

        best_peak_pos, best_conf, _ = select_best_by_conf(all_params[idx], all_confs[idx])
        if best_peak_pos is None:
            logging.warning(f"{qubit} 无有效共峰点")
            continue

        if best_conf < conf_threshold:
            logging.warning(f"{qubit} 置信度{best_conf:.4f} < {conf_threshold}，跳过更新")
            continue

        original_amp = 0.2  # 测试用，实际替换为query_param(f"gate.R.{qubit}.params.amp")
        if original_amp is not None:
            final_amp = original_amp * best_peak_pos
            update_dict[f"gate.R.{qubit}.params.amp"] = final_amp
            logging.info(
                f"OptPi更新 | 比特：{qubit} | 共峰位置：{best_peak_pos:.5f} | "
                f"置信度：{best_conf:.4f} | 最终AMP：{final_amp:.5f}"
            )
        else:
            logging.warning(f"{qubit} 原始AMP参数未设置")
    return update_dict

def drag_update(data_converted, result: dict, file_idx: int = 0, conf_threshold: float = 0.7):
    """
    根据Drag脉冲分析结果更新量子比特beta参数
    Args:
        data_converted: drag_convert转换后的实验数据
        result: 服务器返回的Drag分析结果
        file_idx: 如果服务器同时处理了多个批次的实验数据，选择处理第几个的结果（默认0）
        conf_threshold: 置信度阈值
    """
    update_dict = {}

    file_result = validate_result(result, file_idx, "Drag")
    if file_result is None:
        return update_dict

    intersections = file_result.get("intersections_list", [])
    confs = file_result.get("intersections_confs_list", [])

    image = data_converted.get("image", [])
    qubits = list(image.keys()) if isinstance(image, dict) else image
    for idx, qubit in enumerate(qubits):
        if not validate_list_bounds(idx, {"intersections": intersections, "confs": confs}, qubit, "Drag"):
            continue

        qubit_intersections = intersections[idx]
        qubit_confs = confs[idx]

        if not qubit_intersections or not qubit_confs:
            logging.warning(f"{qubit} 无有效交点")
            continue

        best_conf_idx = qubit_confs.index(max(qubit_confs))
        beta_offset = qubit_intersections[best_conf_idx][0]
        best_conf = qubit_confs[best_conf_idx]

        if best_conf < conf_threshold:
            logging.warning(f"{qubit} 置信度{best_conf:.4f} < {conf_threshold}，跳过更新")
            continue

        original_beta = 0.0  # 测试用，实际替换为query_param(f'gate.R.{qubit}.params.beta')
        if original_beta is not None:
            final_beta = original_beta + beta_offset
            update_dict[f'gate.R.{qubit}.params.beta'] = final_beta
            logging.info(
                f"Drag更新 | 比特：{qubit} | 原始beta：{original_beta:.6e} | "
                f"偏差：{beta_offset:.6e} | 最终beta：{final_beta:.6e} | 置信度：{best_conf:.2f}"
            )
        else:
            logging.warning(f"{qubit} 原始beta参数未设置")
    return update_dict


def setpialpha_update(results, conf_threshold, qubit_name_list):
    update_map = {}
    for result in results:
        params_list = result.get("params", [])
        confs_list = result.get("confs", [])
        for i in range(len(qubit_name_list)):
            if i >= len(params_list) or i >= len(confs_list):
                continue
            peaks = params_list[i]
            confs = confs_list[i]
            if not confs:
                continue
            max_conf = max(confs)
            if max_conf < conf_threshold:
                continue
            best_idx = confs.index(max_conf)
            best_peak = peaks[best_idx]
            target_amp = best_peak
            target_alpha = "Null"
            values = f"{target_amp},{target_alpha}"
            qname = qubit_name_list[i]
            update_map[qname] = values
    return update_map


def s21_update(results, conf_threshold, qubit_name_list):
    """
    根据S21PEAK波谷检测结果更新量子比特读取腔的频率参数
    Args:
        results: 分析结果
        conf_threshold: 置信度阈值
        qubit_name_list:量子名称
    """
    update_dict = {}

    for result in results:
        valleys_confs = result.get("confs", [])
        valleys_freqs = result.get("freqs_list", [])

        for idx in range(len(qubit_name_list)):
            valley_freq, valley_conf = valleys_freqs[idx], valleys_confs[idx]

            if len(valley_freq) and len(valley_conf):

                if valley_conf[0] < conf_threshold:
                    continue

                update_dict[qubit_name_list[idx]] = {"fread_star": valley_freq[0]}
                logging.info(
                    f"S21更新 | 比特：{qubit_name_list[idx]} | "
                    f"新读取腔频率：{(valley_freq[0]):.4f} GHz | 置信度：{valley_conf[0]:.2f}"
                )
        
    return update_dict


def s21peakmulti_update(results, conf_threshold, qubit_name_list, base_freq_list):
    """
    根据S21PEAKMULTI频谱分析结果更新量子比特读取腔频率参数
    Args:
        results: 分析结果列表
        conf_threshold: 置信度阈值
        qubit_name_list: 量子比特名称列表
        base_freq_dict: 各比特基准频率字典
    Returns:
        dict: 待更新的比特-频率映射字典
    """
    update_map = {}
    for res in results:
        peaks_list = res.get("peaks", [])
        confs_list = res.get("confs", [])
        freqs_list = res.get("freqs_list", [])

        for idx, qname in enumerate(qubit_name_list):
            # 索引越界防护
            if idx >= len(confs_list) or idx >= len(freqs_list):
                continue

            confs = confs_list[idx]
            freqs = freqs_list[idx]
            
            for each_dict in base_freq_list:
                if qname in each_dict:
                    base_freq = each_dict[qname]

            # 找到距离基准频率最近的频点
            target_idx = freqs.index(min(freqs, key=lambda f: abs(f - base_freq)))
            closest_freq = freqs[target_idx]
            cur_conf = float(confs[target_idx])

            if cur_conf > conf_threshold:
                update_map[qname] = {"fread_star": closest_freq}
                logging.info(
                    f"S21MULTI更新 | 比特：{qname} | "
                    f"新读取腔频率：{closest_freq:.4f} GHz | 置信度：{cur_conf:.2f}"
                )
    return update_map

import logging

def optreadfreq_update(results, raw_data, conf_threshold, qubit_name_list):
    """
    根据Opt Qubit Read Freq分析结果更新读取频率
    Args:
        results: 解析后分析结果列表
        raw_data: 原始实验数据
        conf_threshold: 置信度阈值（当前逻辑未使用，保留传参）
        qubit_name_list: 比特列表
    Returns:
        dict: {比特名: {"fread": 新频率值}}
    """
    update_map = {}
    

    for result in results:
        freqs_list = result.get('peak_list', [])
        for idx, curr_q in enumerate(qubit_name_list):
            if idx >= len(freqs_list):
                continue
            freqs = freqs_list[idx]
            if not freqs:
                continue
            data_content = raw_data.get(curr_q, {})

            updated_freq = str(data_content[freqs][0])
            update_map[curr_q] = {"fread_star": float(updated_freq)}
            logging.info(
                f"OPTQUBITREADFREQ更新 | 比特：{curr_q} | 新读取频率：{updated_freq}"
            )
    return update_map


def pipulsef10_update(results, conf_threshold, qubit_name_list):
    """
    根据 PiPulseF10 分析结果更新 f10 / f21 参数
    Args:
        results: 解析后分析结果列表
        conf_threshold: 置信度阈值
        qubit_name_list: 比特列表
    Returns:
        dict: {qname: {"f10": val, "f21": val}}
    """
    update_map = {}
    non = -0.2

    for result in results:
        peaks_list = result.get("peaks_list", [])
        confidences_list = result.get("confidences_list", [])

        for idx, qname in enumerate(qubit_name_list):
            if idx >= len(peaks_list) or idx >= len(confidences_list):
                continue

            peaks = peaks_list[idx]
            confidences = confidences_list[idx]
            if not confidences:
                continue

            max_conf = max(confidences)
            if max_conf < conf_threshold:
                continue

            best_idx = confidences.index(max_conf)
            best_peak = peaks[best_idx]
            f10_val = best_peak
            f21_val = best_peak + non

            update_map[qname] = {
                "f10": f10_val,
                "f21": f21_val
            }
            logging.info(
                f"PiPulseF10更新 | 比特：{qname} | f10: {f10_val:.4f} | f21: {f21_val:.4f} | 最大置信度: {max_conf:.2f}"
            )
    return update_map


def spectrum_update(results, conf_threshold, qubit_name_list):
    freq_update_map = {}
    non = -0.2
    for result in results:
        peaks_list = result.get("peaks_list", [])
        confidences_list = result.get("confidences_list", [])
        for i in range(len(qubit_name_list)):
            if i >= len(peaks_list) or i >= len(confidences_list):
                continue
            peaks = peaks_list[i]
            confidences = confidences_list[i]
            if not confidences:
                continue

            max_conf = max(confidences)
            if max_conf <= conf_threshold:
                continue

            best_idx = confidences.index(max_conf)
            best_peak = peaks[best_idx]
            
            target_freq = best_peak
            freq_update_map[qubit_name_list[i]] = {
                "f10": target_freq,
                "f21": target_freq + non
            }
    return freq_update_map


def timingxyz_update(results, conf_threshold, qubit_list):
    """
    TimingXYZ 数据解析与待更新参数计算
    :param results: 经 QubitScopeClient 解析后的结果列表
    :param conf_threshold: 置信度阈值
    :param qubit_list: 比特列表
    :return: 待更新参数字典 {qubit_name: value}
    """
    update_map = {}
    # 保留原有固定值逻辑，可根据实际业务替换为结果解析
    fixed_val = "3.193120459017055, 3.22222"

    for idx, qname in enumerate(qubit_list):
        # 此处可根据 results 内部置信度、时序值扩展解析逻辑
        # 示例：conf = results[idx].get("confs", 0)
        # if conf <= conf_threshold:
        #     continue
        update_map[qname] = fixed_val

    return update_map


def ramsey_update(results, fringe_freq, qubit_name_list, ctrl_client):
    freq_update_map = {}
    non = -0.2
    for result in results:
        params_list = result['params_list']
        for i in range(len(qubit_name_list)):
            if i >= len(params_list):
                continue
            params = params_list[i]
            w = params[4]
            qname = qubit_name_list[i]
            
            f10_raw = ctrl_client.query_param(qname=qname, key="f10_star")
            f10 = float(f10_raw)
            deltaf = w / (2 * math.pi)

            logging.info(f"fringeFreq, f10: {fringe_freq}, {f10}")
            if fringe_freq > f10:
                target_freq = fringe_freq - deltaf
            else:
                target_freq = fringe_freq + deltaf

            freq_update_map[qname] = {
                "f10": target_freq,
                "f21": target_freq + non
            }
    return freq_update_map


def singleshot_update(data_converted, result: dict, file_idx: int = 0, visibility_threshold: float = 0.10):
    """
    根据Scatter实验结果更新量子比特测量参数（threshold/phi）
    Args:
        data_converted: scatter_convert转换后的实验数据
        result: 服务器返回的Scatter结果
        file_idx: 如果服务器同时处理了多个批次的实验数据，选择处理第几个的结果（默认0）
        visibility_threshold: 分离度阈值（测试效果用的0.10，实际这太小了）
    Returns:
        dict: 更新字典 {参数路径: 目标值}
    """
    update_dict = {}

    file_result = validate_result(result, file_idx, "Scatter")
    if file_result is None:
        return update_dict

    # 提取核心参数
    threshold_list = file_result.get("threshold_list", [])
    sep_score_list = file_result.get("sep_score_list", [])
    phi_list = file_result.get("phi_list", [])

    # 提取比特列表
    image = data_converted.get("image", [])
    qubits = list(image.keys()) if isinstance(image, dict) else image
    if not qubits:
        logging.error("data_converted无有效比特列表")
        return update_dict

    # 参数长度校验
    if not sep_score_list or not phi_list:
        logging.warning(
            f"参数列表为空 | sep_score:{len(sep_score_list)}, phi:{len(phi_list)}, "
            f"threshold:{len(threshold_list)}, 比特数:{len(qubits)}"
        )
        return update_dict

    # 遍历比特更新参数
    for idx, q in enumerate(qubits):
        if idx >= len(sep_score_list) or idx >= len(phi_list):
            logging.warning(f"比特{q}无匹配的Scatter参数（索引{idx}越界），跳过更新")
            continue

        sep_score = sep_score_list[idx]
        phi = phi_list[idx]
        threshold = threshold_list[idx] if idx < len(threshold_list) else None

        # 有效性校验
        if not isinstance(sep_score, (int, float)) or not np.isfinite(sep_score):
            logging.warning(f"比特{q}分离度无效：{sep_score}，跳过更新")
            continue
        if sep_score < visibility_threshold:
            logging.warning(f"比特{q}分离度{sep_score:.4f} < {visibility_threshold}，跳过更新")
            continue
        if not isinstance(phi, (int, float)) or not np.isfinite(phi):
            logging.warning(f"比特{q}phi参数无效：{phi}，跳过更新")
            continue

        # 构建更新参数
        param_prefix = f'gate.Measure.{q}.params'
        if threshold is not None and isinstance(threshold, (int, float)) and np.isfinite(threshold):
            update_dict[f'{param_prefix}.threshold'] = float(threshold)
        update_dict[f'{param_prefix}.phi'] = float(phi)
        update_dict[f'{param_prefix}.signal'] = 'state'
        update_dict[f'{param_prefix}.PgPe'] = [1 - sep_score, 1 - sep_score]

        # 日志输出
        log_msg = f"Scatter更新 | 比特：{q} | 分离度：{sep_score:.4f} | Phi：{phi:.5f}"
        if threshold is not None:
            log_msg += f" | 阈值：{threshold:.5f}"
        logging.info(log_msg)

    # 统计日志
    updated_qubits = len(set(k.split('.')[2] for k in update_dict)) if update_dict else 0
    logging.info(
        f"Scatter参数更新完成 | 总计更新{len(update_dict)}个参数 | "
        f"涉及{updated_qubits}个比特（总比特数：{len(qubits)}）"
    )

    return update_dict


def powershift_update(results, conf_threshold, qubit_name_list):
    """
    PowerShift 最优功率更新逻辑
    """
    update_map = {}
    for result in results:
        keypoints_list = result['keypoints_list']
        class_num_list = result['class_num_list']
        confs = result['confs']

        for i in range(len(qubit_name_list)):
            if i > len(keypoints_list):
                continue
            keypoints = keypoints_list[i]
            class_num = class_num_list[i]
            conf = float(confs[i])
            qname = qubit_name_list[i]

            logging.info(f"conf: {conf}")
            if conf <= conf_threshold:
                continue

            keypoints_segments = []
            if class_num == 1:
                keypoints_segments.append([keypoints[1], keypoints[0]])
            if class_num == 2:
                keypoints_segments.append([keypoints[3], keypoints[2]])
            if class_num == 3:
                keypoints_segments.append([keypoints[2], keypoints[1]])

            if keypoints_segments:
                keypoints_segments = keypoints_segments[0]
                logging.info(f"[INFO] keypoints_segments: {keypoints_segments}")
                target_power = keypoints_segments[0][1] + (keypoints_segments[1][1] - keypoints_segments[0][1]) * 0.8
                update_map[qname] = target_power
    return update_map

def rabi_update(results, conf_threshold, qubit_name_list):
    update_amp_map = {}
    for result in results:
        peaks_list = result['peaks']
        confs_list = result['confs']
        for i in range(len(qubit_name_list)):
            if i >= len(peaks_list):
                continue
            peaks = peaks_list[i]
            confs = confs_list[i]
            if not confs:
                continue
            max_conf = max(confs)
            if max_conf < conf_threshold:
                continue
            best_idx = confs.index(max_conf)
            best_peak = peaks[best_idx]
            target_amp = best_peak
            qname = qubit_name_list[i]
            update_amp_map[qname] = target_amp
    return update_amp_map


def delta_update(data_converted, result: dict, file_idx: int = 0, conf_threshold: float = 0.7):
    """
    根据Delta实验分析结果更新量子比特delta参数  （待测试）
    Args:
        data_converted: delta_convert转换后的实验数据
        result: 服务器返回的Delta分析结果
        file_idx: 处理第几个文件的结果（默认0）
        conf_threshold: 置信度阈值
    Returns:
        dict: 更新字典 {gate.R.比特名.params.delta: 目标delta值}
    """
    update_dict = {}

    file_result = validate_result(result, file_idx, "Delta")
    if file_result is None:
        return update_dict

    all_params = file_result.get("params", [])
    all_confs = file_result.get("confs", [])

    image = data_converted.get("image", [])
    qubits = list(image.keys()) if isinstance(image, dict) else image
    for idx, qubit in enumerate(qubits):
        if not validate_list_bounds(idx, {"params": all_params, "confs": all_confs}, qubit, "Delta"):
            continue

        qubit_valley_params = all_params[idx]
        qubit_valley_confs = all_confs[idx]

        if not isinstance(qubit_valley_params, list) or not isinstance(qubit_valley_confs, list):
            logging.warning(f"{qubit} 谷值参数/置信度格式错误")
            continue

        if len(qubit_valley_params) != len(qubit_valley_confs):
            logging.warning(f"{qubit} 谷值位置与置信度数量不匹配")
            continue

        best_valley_pos, best_conf, _ = select_best_by_conf(qubit_valley_params, qubit_valley_confs)
        if best_valley_pos is None:
            logging.warning(f"{qubit} 无有效谷值点")
            continue

        if best_conf < conf_threshold:
            logging.warning(f"{qubit} 置信度{best_conf:.4f} < {conf_threshold}，跳过更新")
            continue

        original_delta = 0.1  # 测试用
        update_key = f"gate.R.{qubit}.params.delta"
        update_dict[update_key] = best_valley_pos

        logging.info(
            f"Delta更新 | 比特：{qubit} | 谷值位置：{best_valley_pos:.5f} | "
            f"置信度：{best_conf:.4f} | 原始delta：{original_delta:.5f} | 最终delta：{best_valley_pos:.5f}"
        )

    logging.info(f"Delta参数更新完成，共更新{len(update_dict)}个比特")
    return update_dict