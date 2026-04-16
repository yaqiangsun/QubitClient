# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
LLM/VLM 任务模块 - 只返回 prompt
"""

import json
from enum import Enum, unique

from qubitclient.llm.prompt import (
    get_evaluation_prompt,
    get_decision_prompt,
    get_suggest_params_prompt,
    get_vlm_analyze_prompt,
    EVALUATION_RESPONSE_SCHEMA,
    DECISION_RESPONSE_SCHEMA,
    SUGGEST_PARAMS_RESPONSE_SCHEMA,
)
from qubitclient.ctrl.task import CtrlTaskName


DEFINED_TASKS = {}


def task_register(func):
    """任务注册装饰器"""
    DEFINED_TASKS[func.__name__.lower()] = func
    return func


def get_task_prompt(task_type, *args, **kwargs):
    """运行指定任务"""
    if not isinstance(task_type, str):
        task_type = task_type.value
    if task_type not in DEFINED_TASKS:
        raise ValueError(f"Unknown task: {task_type}")
    return DEFINED_TASKS[task_type](*args, **kwargs)


@unique
class LLMTaskName(Enum):
    """LLM 任务名称枚举"""
    EVALUATE_ANALYSIS = "evaluate_analysis"
    DECIDE_NEXT_ACTION = "decide_next_action"
    VLM_ANALYZE = "vlm_analyze"
    SUGGEST_PARAMS = "suggest_params"


@task_register
def evaluate_analysis(
    analysis_result: dict | str,
    criteria: dict | None = None,
    prompt: str | None = None,
) -> dict:
    """
    获取评估任务的 prompt

    Args:
        analysis_result: 分析结果（dict 或 JSON 字符串）
        criteria: 评估标准（可选）
        prompt: 自定义提示词

    Returns:
        包含 messages 和 response_schema 的字典
    """
    # 转换分析结果为字符串
    if isinstance(analysis_result, dict):
        analysis_str = json.dumps(analysis_result, ensure_ascii=False, indent=2)
    else:
        analysis_str = str(analysis_result)

    # 转换 criteria 为字符串
    criteria_str = json.dumps(criteria, ensure_ascii=False, indent=2) if criteria else None

    # 构建提示词
    if prompt is None:
        prompt = get_evaluation_prompt(analysis_str, criteria_str)
    else:
        prompt = prompt.format(analysis_result=analysis_str)

    messages = [{"role": "user", "content": prompt}]

    return {
        "messages": messages,
        "response_schema": EVALUATION_RESPONSE_SCHEMA,
    }


@task_register
def decide_next_action(
    evaluation_result: dict | str,
    available_actions: list | None = None,
    prompt: str | None = None,
) -> dict:
    """
    获取决策任务的 prompt

    Args:
        evaluation_result: VLM 评估结果（dict 或 JSON 字符串）
        available_actions: 可用的 ctrl 行动列表
        prompt: 自定义提示词

    Returns:
        包含 messages 和 response_schema 的字典
    """
    # 转换评估结果为字符串
    if isinstance(evaluation_result, dict):
        eval_str = json.dumps(evaluation_result, ensure_ascii=False, indent=2)
    else:
        eval_str = str(evaluation_result)

    # 转换可用行动为字符串
    actions_str = ", ".join(available_actions) if available_actions else None

    # 构建提示词
    if prompt is None:
        prompt = get_decision_prompt(eval_str, actions_str)
    else:
        prompt = prompt.format(evaluation_result=eval_str)

    messages = [{"role": "user", "content": prompt}]

    return {
        "messages": messages,
        "response_schema": DECISION_RESPONSE_SCHEMA,
    }


@task_register
def vlm_analyze(
    image_data: str | bytes | list,
    prompt: str = "分析这张量子测量图像，描述你观察到的特征和可能的物理意义",
) -> dict:
    """
    获取 VLM 分析任务的 prompt

    Args:
        image_data: 图像数据（路径、bytes 或图像列表）
        prompt: 分析提示词

    Returns:
        包含 messages, images 的字典
    """
    formatted_prompt = get_vlm_analyze_prompt(prompt)

    return {
        "messages": [{"role": "user", "content": formatted_prompt}],
        "images": image_data,
    }


@task_register
def suggest_params(
    task_type: str | CtrlTaskName,
    context: dict,
) -> dict:
    """
    获取参数建议任务的 prompt

    Args:
        task_type: 目标任务类型
        context: 上下文信息（历史数据、评估结果等）

    Returns:
        包含 messages 和 response_schema 的字典
    """
    # 转换任务类型
    if isinstance(task_type, CtrlTaskName):
        task_type_str = task_type.value
    else:
        task_type_str = str(task_type)

    # 转换上下文为字符串
    context_str = json.dumps(context, ensure_ascii=False, indent=2)

    # 构建提示词
    prompt = get_suggest_params_prompt(task_type_str, context_str)

    messages = [{"role": "user", "content": prompt}]

    return {
        "messages": messages,
        "response_schema": SUGGEST_PARAMS_RESPONSE_SCHEMA,
    }