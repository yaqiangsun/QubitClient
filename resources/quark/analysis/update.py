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

from .utils import query_param, update_param

from .utils import (
    validate_result,
    select_best_by_conf,
    validate_list_bounds,
    validate_numeric_range,
)

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

def s21_update(data_converted, result: dict, file_idx: int = 0, conf_threshold: float = 0.7):
    """
    根据S21PEAK波谷检测结果更新量子比特读取腔的频率参数
    Args:
        data_converted: s21_convert转换后的实验数据
        result: 服务器返回的S21PEAK分析结果（波谷检测）
        file_idx: 如果服务器同时处理了多个批次的实验数据，选择处理第几个的结果（默认0）
        conf_threshold: 置信度阈值
    """
    update_dict = {}

    file_result = validate_result(result, file_idx, "S21PEAK")
    if file_result is None:
        return update_dict

    valleys_idx = file_result.get("peaks", [])
    valleys_confs = file_result.get("confs", [])
    valleys_freqs = file_result.get("freqs_list", [])

    image = data_converted.get("image", [])
    qubits = list(image.keys()) if isinstance(image, dict) else image
    for idx, qubit in enumerate(qubits):
        if not validate_list_bounds(idx, {"valleys_idx": valleys_idx, "valleys_confs": valleys_confs, "valleys_freqs": valleys_freqs}, qubit, "S21"):
            continue

        best_valley_freq, best_valley_conf, best_idx = select_best_by_conf(
            valleys_freqs[idx], valleys_confs[idx]
        )
        if best_valley_freq is None:
            logging.warning(f"{qubit} 无有效S21波谷数据")
            continue

        if best_valley_conf < conf_threshold:
            logging.warning(f"{qubit} 置信度{best_valley_conf:.4f} < {conf_threshold}，跳过更新")
            continue

        original_read_freq = 4.432e9  # 测试用
        # 实际original_read_freq需要读取
        if original_read_freq is not None:
            update_dict[f'gate.Measure.{qubit}.params.frequency'] = original_read_freq+best_valley_freq
            logging.info(
                f"S21更新 | 比特：{qubit} | 原始读取腔频率：{original_read_freq*1e-9:.4f} GHz | "
                f"新读取腔频率：{(original_read_freq+best_valley_freq)*1e-9:.4f} GHz | 置信度：{best_valley_conf:.2f}"
            )
        else:
            logging.warning(f"{qubit} 原始读取腔频率参数未设置")
    return update_dict



def spectrum_update(data_converted, result: dict, file_idx: int = 0, conf_threshold: float = 0.7, top_n: int = 3):
    """
    根据SPECTRUM峰值检测结果，更新量子比特的频率参数
    Args:
        data_converted: spectrum_convert转换后的实验数据
        result: 服务器返回的SPECTRUM分析结果
        file_idx: 如果服务器同时处理了多个批次的实验数据，选择处理第几个的结果（默认0）
        conf_threshold: 置信度阈值
        top_n: 备选的最有可能的几个峰值
    """
    update_dict = {}

    file_result = validate_result(result, file_idx, "SPECTRUM")
    if file_result is None:
        return update_dict

    peaks_list = file_result.get("peaks_list", [])
    confidences_list = file_result.get("confidences_list", [])

    if not peaks_list or not confidences_list:
        logging.warning("SPECTRUM结果中无峰值或置信度数据")
        return update_dict

    image = data_converted.get("image", [])
    qubits = list(image.keys()) if isinstance(image, dict) else image
    for idx, qubit in enumerate(qubits):
        if not validate_list_bounds(idx, {"peaks_list": peaks_list, "confidences_list": confidences_list}, qubit, "SPECTRUM"):
            continue

        best_peak_freq, best_conf, _ = select_best_by_conf(peaks_list[idx], confidences_list[idx])
        if best_peak_freq is None:
            logging.warning(f"{qubit} 无有效峰值")
            continue

        if best_conf < conf_threshold:
            logging.warning(f"{qubit} 置信度{best_conf:.4f} < {conf_threshold}，跳过更新")
            continue

        original_freq = 4.1e9  # 测试用
        if original_freq is not None:
            update_dict[f'gate.R.{qubit}.params.frequency'] = best_peak_freq
            logging.info(
                f"SPECTRUM更新 | 比特：{qubit} | "
                f"原始频率：{original_freq*1e-9:.4f} GHz | "
                f"新频率：{best_peak_freq*1e-9:.4f} GHz | "
                f"置信度：{best_conf:.2f}"
            )
        else:
            logging.warning(f"{qubit} 原始频率参数未设置")
    return update_dict


def ramsey_update(data_converted, result: dict, file_idx: int = 0, conf_threshold: float = 0.8, rotate_freq: float = 2e6):
    """
    根据Ramsey实验的分析结果更新量子比特R门共振频率参数
    Args:
        data_converted: ramsey_convert转换后的实验数据
        result: 服务器返回的ramsey分析结果
        file_idx: 如果服务器同时处理了多个批次的实验数据，选择处理第几个的结果（默认0）
        conf_threshold: 置信度阈值（默认0.8）
        rotate_freq: Ramsey实验预设的rotate频率（Hz，默认2e6）
    """
    update_dict = {}

    if not validate_numeric_range(rotate_freq, 0, float('inf'), "rotate_freq"):
        return update_dict

    file_result = validate_result(result, file_idx, "Ramsey")
    if file_result is None:
        return update_dict

    if file_result.get("status") != "success":
        logging.error(f"第{file_idx}个文件拟合失败，status={file_result.get('status')}")
        return update_dict

    params_list = file_result.get("params_list", [])
    r2_list = file_result.get("r2_list", [])

    image = data_converted.get("image", [])
    qubits = list(image.keys()) if isinstance(image, dict) else image
    for idx, qubit in enumerate(qubits):
        if not validate_list_bounds(idx, {"params_list": params_list, "r2_list": r2_list}, qubit, "Ramsey"):
            continue

        params = params_list[idx]
        r2 = r2_list[idx]

        if r2 < conf_threshold:
            logging.warning(f"{qubit} 拟合优度R²{r2:.4f} < {conf_threshold}，跳过更新")
            continue

        try:
            w = params[3]  # 这里要根据服务器返回情况修改
            logging.info(f"{qubit} 拟合参数 | w={w:.2e}rad/s")
        except (IndexError, ValueError):
            logging.error(f"{qubit} 拟合参数格式错误，无法提取w | params={params}")
            continue

        if w <= 0:
            logging.warning(f"{qubit} 参数物理异常 | w={w:.2e}rad/s | 跳过更新")
            continue

        f_actual = w / (2 * np.pi)
        f_diff = np.abs(f_actual) - rotate_freq

        param_key = f"gate.R.{qubit}.params.frequency"
        try:
            original_freq = 4.00e9  # 测试用
        except Exception as e:
            logging.error(f"{qubit} 查询原始频率失败：{str(e)}，跳过更新")
            continue

        if original_freq is not None:
            final_freq = original_freq + f_diff
            update_dict[param_key] = final_freq
            logging.info(
                f"Ramsey更新 | 比特：{qubit} | "
                f"实际进动频率：{f_actual/1e6:.6f}MHz | 频率偏差：{f_diff/1e3:.3f}kHz | "
                f"原始频率：{original_freq/1e9:.8f}GHz | 最终频率：{final_freq/1e9:.8f}GHz | "
                f"拟合优度：R²={r2:.4f}"
            )
        else:
            logging.warning(f"{qubit} 原始频率参数未设置")
    return update_dict


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




def s21multi_update(result: dict, file_idx: int = 0, conf_threshold: float = 0.8, top_n: int = 13,
                    MIN_FREQ: float = 5 * 10**9, MAX_FREQ: float = 7 * 10**9,
                    qubits_lists: list = ['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','Q10','Q11','Q12','Q13']):
    """
    处理S21全扫描的多峰数据，更新读取腔频率参数
    Args:
        result (dict): 服务器返回的S21全扫描结果，需包含results/result字段
        file_idx (int): 处理第几个文件的结果（默认0，单文件场景）
        conf_threshold (float): 置信度阈值，范围[0,1]（默认0.8）
        top_n (int): 最大更新数量（默认13）
        MIN_FREQ (float): 频率最小值（Hz）
        MAX_FREQ (float): 频率最大值（Hz）
        qubits_lists (list): 比特名称列表，如['Q1','Q2',...,'Q13']
    Returns:
        dict: 更新字典 {参数路径: 频率值(Hz)}
    """
    update_dict = {}

    # 参数校验
    if not isinstance(qubits_lists, list) or not qubits_lists:
        logging.error("qubits_lists无效或为空，无法执行更新")
        return update_dict
    if not validate_numeric_range(conf_threshold, 0, 1, "conf_threshold"):
        return update_dict
    if not isinstance(top_n, int) or top_n <= 0:
        logging.error(f"top_n无效：{top_n}，必须为正整数")
        return update_dict

    logging.info("开始执行S21多峰更新")

    # 校验result结构并获取指定索引的结果
    s21_res = validate_result(result, file_idx ,"S21multi_scan")
    if s21_res is None:
        return update_dict

    if s21_res.get("status") != "success":
        logging.error(f"文件索引{file_idx}分析失败（status={s21_res.get('status')}），跳过更新")
        return update_dict

    # 提取核心数据
    peaks_list = s21_res.get("peaks", [])
    confs_list = s21_res.get("confs", [])
    freqs_list = s21_res.get("freqs_list", [])

    # 校验列表类型和数据有效性
    if not all(isinstance(lst, list) and lst and isinstance(lst[0], list)
               for lst in [peaks_list, confs_list, freqs_list]):
        logging.warning("peaks/confs/freqs_list格式错误或为空，跳过更新")
        return update_dict

    bit_peaks, bit_confs, bit_freqs = peaks_list[0], confs_list[0], freqs_list[0]

    peak_conf_freq = list(zip(bit_peaks, bit_confs, bit_freqs))
    logging.info(f"有效数据数量：{len(peak_conf_freq)}")

    valid_data = []
    for idx, (p, c, f) in enumerate(peak_conf_freq):
        # 检查置信度
        conf_valid = isinstance(c, (int, float)) and c >= conf_threshold
        # 检查频率
        freq_is_number = isinstance(f, (int, float))
        # 频率范围判断
        freq_in_range = (MIN_FREQ <= f <= MAX_FREQ) if freq_is_number else False

        # 打印异常日志
        if freq_is_number and not freq_in_range:
            if f < MIN_FREQ:
                logging.error(f"第{idx}个峰值数据异常：频率＜5GHz → 峰值位置{p}，频率{f/10**9:.2f} GHz（合理范围5~7GHz）")
            else:
                logging.error(f"第{idx}个峰值数据异常：频率＞7GHz → 峰值位置{p}，频率{f/10**9:.2f} GHz（合理范围5~7GHz）")

        # 筛选有效数据
        if conf_valid and freq_is_number and freq_in_range:
            valid_data.append((p, c, f))

    if not valid_data:
        logging.warning(f"无置信度≥{conf_threshold}且频率在5~7GHz范围内的有效峰值，跳过更新")
        return update_dict

    # 确保不超出 valid_data 实际长度
    max_n = min(top_n, len(qubits_lists), len(valid_data))
    valid_data = valid_data[:max_n]
    for idx, (peak, conf, freq) in enumerate(valid_data):
        qubit = qubits_lists[idx]
        param_key = f"gate.R.{qubit}.params.freq_{idx}"
        update_dict[param_key] = freq
        logging.info(
            f"更新{qubit}频率 | 序号{idx} | 峰值位置{peak:.0f} | "
            f"置信度{conf:.6f} | 频率{freq/10**9:.2f} GHz（按频率升序赋值）"
        )

    logging.info(f"S21mulit更新完成，共更新{len(update_dict)}个频率参数")
    return update_dict


def powershift_update(data_converted, result: dict, file_idx: int = 0, conf_threshold: float = 0.5, base_amp: float = 0.05):
    """
    基于S21功率扫描（s21vsamp）结果更新腔/比特的AMP振幅参数
    Args:
        data_converted: s21_convert转换后的数据
        result: 服务器返回的分析结果
        file_idx: 处理第几个文件结果（默认0）
        conf_threshold: 置信度阈值（默认0.5）
        base_amp: 检测到的结果不符合要求时候的经验值（0.05）
    Returns:
        dict: 更新字典 {gate.R.比特名.params.amp: 目标振幅值}
    """
    update_dict = {}

    file_result = validate_result(result, file_idx, "PowerShift")
    if file_result is None:
        return update_dict

    q_list = file_result.get("q_list", [])
    confs = file_result.get("confs", [])
    keypoints_list = file_result.get("keypoints_list", [])

    if not q_list:
        logging.warning("无有效比特列表，跳过AMP更新")
        return update_dict
    if len(keypoints_list) != len(q_list) or len(confs) != len(q_list):
        logging.error("比特列表/置信度/关键点数量不匹配，跳过更新")
        return update_dict

    image_dict = data_converted.get("image", {})
    original_qubit_names = list(image_dict.keys()) if isinstance(image_dict, dict) else []

    for idx, qubit in enumerate(q_list):
        conf = confs[idx] if idx < len(confs) else 0.0
        if conf < conf_threshold:
            logging.warning(f"{qubit} 置信度{conf:.4f} < {conf_threshold}，跳过更新")
            continue

        keypoints = keypoints_list[idx] if idx < len(keypoints_list) else []
        valid_keypoints = [
            point[1] for point in keypoints
            if isinstance(point, list) and len(point) >= 2
            and isinstance(point[1], (int, float)) and point[1] >= 0
        ]

        valid_point_count = len(valid_keypoints)
        if valid_point_count <= 1:
            logging.warning(f"{qubit} 检测到{valid_point_count}个有效点，跳过更新")
            continue

        # 确保 valid_keypoints 中所有元素为数值
        if not all(isinstance(x, (int, float)) for x in valid_keypoints):
            logging.warning(f"{qubit} valid_keypoints包含非数值元素，跳过更新")
            continue

        if valid_point_count == 3:
            inflection_amp = np.mean(valid_keypoints[:2])
            logging.debug(f"{qubit} 检测到3个有效点，取前2个点平均值")
        else:
            inflection_amp = np.mean(valid_keypoints)
            logging.warning(f"{qubit} 检测到{valid_point_count}个有效点，取所有点平均值")

        # base_amp = 0.05
        target_amp = inflection_amp

        if target_amp > 0.9 or target_amp < 0.01:
            logging.warning(f"{qubit} 目标AMP{target_amp:.4f} 超出合理范围，使用经验值{base_amp}")
            target_amp = base_amp

        final_qubit_name = original_qubit_names[idx] if idx < len(original_qubit_names) else qubit
        update_key = f"gate.R.{final_qubit_name}.params.amp"
        update_dict[update_key] = target_amp

        logging.info(
            f"PowerShift更新 | 比特：{final_qubit_name} | 置信度：{conf:.4f} | "
            f"inflection_amp：{inflection_amp:.4f} | 目标AMP：{target_amp:.4f}"
        )

    logging.info(f"PowerShift AMP更新完成，共更新{len(update_dict)}个比特")
    return update_dict


def rabi_update(data_converted, result: dict, file_idx: int = 0, conf_threshold: float = 0.7):
    """
    根据Rabi实验结果更新量子比特R.amp参数
    Args:
        data_converted: 转换后数据
        result: 服务器返回的Rabi分析结果
        file_idx: 文件索引（默认0）
        conf_threshold: 置信度阈值
    """
    update_dict = {}

    rabi_res = validate_result(result, file_idx, "Rabi")
    if rabi_res is None:
        return update_dict

    if rabi_res.get("status") != "success":
        logging.error("Rabi更新失败：分析状态非success")
        return update_dict

    peaks_list = rabi_res.get("peaks", [])
    confs_list = rabi_res.get("confs", [])

    image = data_converted.get("image", [])
    qubits = list(image.keys()) if isinstance(image, dict) else image
    for bit_idx, qubit in enumerate(qubits):
        if not validate_list_bounds(bit_idx, {"peaks_list": peaks_list, "confs_list": confs_list}, qubit, "Rabi"):
            continue

        best_peak, best_conf, _ = select_best_by_conf(peaks_list[bit_idx], confs_list[bit_idx])
        if best_peak is None:
            continue

        if best_conf < conf_threshold:
            logging.warning(f"{qubit} 置信度{best_conf:.4f} < {conf_threshold}，跳过更新")
            continue

        param_key = f"gate.R.{qubit}.params.amp"
        update_dict[param_key] = best_peak
        logging.info(f"Rabi更新 | 比特{qubit} | 最佳峰值：{best_peak:.5f} | 置信度：{best_conf:.4f} | 最终AMP：{best_peak:.5f}")

    return update_dict

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