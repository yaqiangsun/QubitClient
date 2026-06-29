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


#####################################################################################