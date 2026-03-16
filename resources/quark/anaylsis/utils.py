# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/11 11:54:18
########################################################################

import os
import numpy as np
import pickle
import logging

def get_pkl_content(pkl_file_path):
    """
    读取你的PKL文件（包含上述复杂结构）
    """
    abs_path = os.path.abspath(pkl_file_path)
    if not os.path.exists(abs_path):
        print(f"❌ PKL文件不存在：{abs_path}")
        return None
    
    print(f"📌 读取PKL文件：{os.path.basename(abs_path)}")
    try:
        with open(abs_path, 'rb') as f:
            result = pickle.load(f)
        print("✅ PKL文件读取成功，数据结构包含：", list(result.keys()))
        return result
    except Exception as e:
        print(f"❌ 读取失败：{str(e)}")
        return None

#####################################################################################
# updata
def update_param(key:str, value):
    """更新指定key的参数值"""
    from quark.app import s
    s.update(key, value)
def query_param(key:str):
    """查询指定key的参数"""
    from quark.app import s
    return s.query(key)

#####################################################################################
# format
def extract_waveform_data(result, index=None, priority=("population", "iq_avg", "iq")):
    """
    从result["data"]中按优先级提取波形数据

    Args:
        result (dict): 原始实验数据字典
        index: 数据索引（None表示不切片，用于单比特场景）
        priority (tuple): 关键词检测优先级，默认 population → iq_avg → iq
    Returns:
        tuple: (matched_key, np.ndarray) 匹配到的关键词名称和提取的数据
    Raises:
        ValueError: 所有关键词均不存在时抛出
    """
    data_dict = result["data"]

    for key in priority:
        if key in data_dict:
            raw_data = data_dict[key]
            # 根据index切片（支持多维索引）
            if index is not None:
                if raw_data.ndim == 3:
                    return key, np.array(raw_data[:, :, index])
                elif raw_data.ndim == 2:
                    return key, np.array(raw_data[:, index])
                else:
                    return key, np.array(raw_data)
            else: 
                return key, np.array(raw_data)

    # 所有关键词均不存在
    raise ValueError(
        f"未检测到有效数据关键词（{'/'.join(priority)}），"
        f"请确认数据中的实际关键词名称。当前可用关键词: {list(data_dict.keys())}"
    )


# 校验规则表: {func_name: [(数组名, 期望维度, [(自身维度索引, 目标数组名, 目标维度索引)]), ...]}
_VALIDATION_RULES = {
    "optpipulse": [
        ("waveforms", 2, [(1, "x_array", 0)]),
        ("x_array", 1, []),
    ],
    "delta": [
        ("waveforms", 2, [(1, "x_array", 0)]),
        ("x_array", 1, []),
    ],
    "drag": [
        ("x", 1, []),
        ("y0y1", 2, [(1, "x", 0)]),
    ],
    "s21": [
        ("x_array", 1, []),
        ("iq_avg", 1, []),
         # 第一层校验：amp必须是 1 维数组； 第二层校验：amp的第 0 维长度（如21），必须等于x_array的第 0 维长度（如21）；
        ("amp", 1, [(0, "x_array", 0)]),  
        ("phi", 1, [(0, "x_array", 0)]),
    ],
    "s21multi": "s21",
    "s21vsflux": [
        ("volt", 1, []),
        ("freq", 1, []),
        # 第一层：s必须是 2 维数组；
        # 第二层：
        # s的第 0 维长度 = freq的第 0 维长度；
        # s的第 1 维长度 = volt的第 0 维长度；
        ("s", 2, [(0, "freq", 0), (1, "volt", 0)]),
    ],
    "nns21vsflux": "s21vsflux",
    "singleshot": [
        ("s0", 1, []),
        ("s1", 1, []),
    ],
    "nnspectrum2d": [
        ("freq", 1, []),
        ("bias", 1, []),
        ("s", 2, [(0, "bias", 0), (1, "freq", 0)]),
    ],
    "spectrum2d": "nnspectrum2d",
    "rabicos": [
        ("x_array", 1, []),
        ("amp_array", 1, [(0, "x_array", 0)]),
    ],
    "t1fit": [
        ("delay_array", 1, []),
        ("population", 1, [(0, "delay_array", 0)]),
    ],
    "t2fit": "t1fit",
    "ramsey": "t1fit",
    "nnspectrum": [
        ("freq", 1, []),
        ("s", 1, [(0, "freq", 0)]),
    ],
    "spectrum": "nnspectrum",
}


def validate_server_format(func_name, **arrays):
    """
    统一格式校验函数，根据func_name执行对应校验规则
    Args:
        func_name (str): 调用方函数名称标识
        **arrays: 需要校验的数据数组，键名为数据名称
    用法示例:
        validate_server_format("optpipulse", waveforms=waveforms, x_array=x_array)
        validate_server_format("s21", x_array=x_array, iq_avg=iq_avg, amp=amp, phi=phi)
    Raises:
        ValueError: 数据格式不符合服务器要求时抛出详细错误信息
    """
    rules = _VALIDATION_RULES.get(func_name)
    if rules is None:  # 未定义规则的函数
        return 

    # 解析别名
    while isinstance(rules, str):
        rules = _VALIDATION_RULES[rules]

    for name, expected_ndim, shape_checks in rules:
        arr = arrays.get(name)
        if arr is None:
            continue

        # 维度校验
        if arr.ndim != expected_ndim:
            raise ValueError(
                f"{func_name}数据格式不符合服务器要求：{name}应为{expected_ndim}维数组，"
                f"实际为{arr.ndim}维，形状{arr.shape}"
            )

        # 形状匹配校验
        for dim_idx, target_name, target_dim_idx in shape_checks:
            target = arrays.get(target_name)
            if target is not None and arr.shape[dim_idx] != target.shape[target_dim_idx]:
                raise ValueError(
                    f"{func_name}数据格式不符合服务器要求：{name}的第{dim_idx}维长度({arr.shape[dim_idx]})"
                    f"需与{target_name}的第{target_dim_idx}维长度({target.shape[target_dim_idx]})一致"
                )

def normalize_iq_data(raw_data, context, reduce_2d=False, expected_qubit_dim=None):
    """
    规范化 iq 数据维度：
    - 3维：剔除中间维度 -> (n, k)
    - 2维：如需要剔除最后一维 -> (n,)
    """
    if raw_data.ndim == 3:
        raw_data = raw_data[:, 0, :]
        logging.info(f"{context} | iq 3维数据剔除中间维后形状：{raw_data.shape}")
    elif raw_data.ndim == 2 and reduce_2d:
        if expected_qubit_dim is None or raw_data.shape[1] != expected_qubit_dim:
            raw_data = raw_data[:, 0]
            logging.info(f"{context} | iq 2维数据剔除最后维后形状：{raw_data.shape}")
    return raw_data

def _get_results_list(result: dict, exp_name: str, keys: tuple[str, ...]) -> list:
    if not isinstance(result, dict):
        logging.error(f"{exp_name}结果格式错误，result类型：{type(result)}，期望dict")
        return None

    results_list = None
    for key in keys:
        if key in result:
            results_list = result.get(key)
            break

    if results_list is None:
        logging.error(f"{exp_name}结果格式错误，无有效{ '/'.join(keys) }字段")
        return None

    if not isinstance(results_list, list):
        logging.error(f"{exp_name}结果格式错误，{key}字段类型：{type(results_list)}，期望list")
        return None

    return results_list


def validate_result(result: dict, file_idx: int, exp_name: str) -> dict:
    """验证result格式并返回指定索引的结果"""
    results_list = _get_results_list(result, exp_name, ("results", "result"))
    if results_list is None:
        return None
    if file_idx < 0 or file_idx >= len(results_list):
        logging.error(f"{exp_name} file_idx={file_idx} 越界，有效范围0~{len(results_list)-1}")
        return None
    return results_list[file_idx]



def select_best_by_conf(params: list, confs: list) -> tuple:
    """选择置信度最高的参数，返回(best_param, best_conf, best_idx)"""
    "参数选择策略"
    if not params or not confs:
        return None, None, None
    best_idx = confs.index(max(confs))
    return params[best_idx], confs[best_idx], best_idx


def validate_list_bounds(idx: int, lists: dict, qubit: str, context: str) -> bool:
    """
    检查索引是否在所有列表范围内
    Args:
        idx: 索引值
        lists: 字典 {列表名: 列表对象}
        qubit: 比特名称
        context: 上下文描述（用于日志）
    Returns:
        bool: True=有效, False=越界
    """
    for name, lst in lists.items():
        if idx >= len(lst):
            logging.warning(f"{qubit} 无匹配的{context}结果（{name}索引越界）")
            return False
    return True

def validate_numeric_range(value, min_val, max_val, param_name: str, allow_none: bool = False) -> bool:
    """
    校验数值是否在指定范围内
    Args:
        value: 待校验值
        min_val: 最小值
        max_val: 最大值
        param_name: 参数名称
        allow_none: 是否允许None
    Returns:
        bool: True=有效, False=无效
    """
    if value is None and allow_none:
        return True
    if not isinstance(value, (int, float)):
        logging.error(f"{param_name}类型错误：{type(value)}，期望数值")
        return False
    if not (min_val <= value <= max_val):
        logging.error(f"{param_name}超出范围[{min_val}, {max_val}]：{value}")
        return False
    return True


