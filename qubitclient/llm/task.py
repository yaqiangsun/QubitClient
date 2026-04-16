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

from qubitclient.llm.experiment_tools import ExperimentFamily

from qubitclient.llm.decision import (
    DECISION_RESPONSE_SCHEMA,
    get_decision_prompt,
)

from qubitclient.llm.experiments import (
    # Response Schema
    DESCRIBE_PLOT_RESPONSE_SCHEMA,
    CLASSIFY_OUTCOME_RESPONSE_SCHEMA,
    ASSESS_FIT_RESPONSE_SCHEMA,
    EVALUATE_STATUS_RESPONSE_SCHEMA,
    # 获取函数
    get_describe_plot_prompt,
    get_classify_outcome_prompt,
    get_scientific_reasoning_prompt,
    get_assess_fit_prompt,
    get_extract_params_prompt,
    get_evaluate_status_prompt,
    get_extract_params_schema,
    get_experiment_background,
)


# 实验类型+问题：这些组合的prompt中已包含背景信息，不需要再添加experiment_background
# 格式: (experiment_family, question_number)
PROMPTS_WITH_EMBEDDED_BACKGROUND = {
    ("coupler_flux", 5),           # Q5包含背景
    ("qubit_spectroscopy_power_frequency", 2),  # Q2包含背景
    ("qubit_spectroscopy_power_frequency", 3),  # Q3包含背景
    ("qubit_spectroscopy_power_frequency", 4),  # Q4包含背景
    ("qubit_spectroscopy_power_frequency", 5),  # Q5包含背景
    ("qubit_spectroscopy_power_frequency", 6),  # Q6包含背景
}

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
    # 决策任务：给出下一步目标与对应参数
    DECIDE_NEXT_ACTION = "decide_next_action"
    # QCalEval tasks
    DESCRIBE_PLOT = "describe_plot"
    CLASSIFY_OUTCOME = "classify_outcome"
    SCIENTIFIC_REASONING = "scientific_reasoning"
    ASSESS_FIT = "assess_fit"
    EXTRACT_PARAMS = "extract_params"
    EVALUATE_STATUS = "evaluate_status"


@task_register
def decide_next_action(
    evaluation_result: dict | str,
    available_actions: list | None = None,
    context: dict | None = None,
    prompt: str | None = None,
) -> dict:
    """
    决策任务：基于评估结果给出下一步测量目标及参数建议

    Args:
        evaluation_result: VLM 评估结果（dict 或 JSON 字符串）
        available_actions: 可用的 ctrl 行动列表
        context: 上下文信息（历史数据、当前状态等），用于生成参数建议
        prompt: 自定义提示词

    Returns:
        包含 messages 和 response_schema 的字典
    """
    # 转换评估结果为字符串
    if isinstance(evaluation_result, dict):
        eval_str = json.dumps(evaluation_result, ensure_ascii=False, indent=2)
    else:
        eval_str = str(evaluation_result)

    # 转换上下文为字符串
    context_str = json.dumps(context, ensure_ascii=False, indent=2) if context else None

    # 转换可用行动为字符串
    actions_str = ", ".join(available_actions) if available_actions else None

    # 构建提示词
    if prompt is None:
        prompt = get_decision_prompt(eval_str, actions_str, context_str)
    else:
        prompt = prompt.format(evaluation_result=eval_str)

    messages = [{"role": "user", "content": prompt}]

    return {
        "messages": messages,
        "response_schema": DECISION_RESPONSE_SCHEMA,
    }


# ========== QCalEval Tasks ==========


@task_register
def describe_plot(
    image_data: str | bytes | list,
    experiment_family: str | ExperimentFamily | None = None,
) -> dict:
    """
    描述图表任务 (QCalEval Q1)
    描述图像中的图表类型、坐标轴、范围和主要特征

    Args:
        image_data: 图像数据
        experiment_family: 实验家族（字符串或 ExperimentFamily 枚举），使用专属 prompt

    Returns:
        包含 messages, images 和 response_schema 的字典
    """
    # 获取专属 prompt
    family = experiment_family
    if isinstance(family, ExperimentFamily):
        family = family.value

    # 合并 experiment_background 和任务 prompt
    # 如果prompt中已包含背景信息，则跳过添加
    if family and (family, 1) in PROMPTS_WITH_EMBEDDED_BACKGROUND:
        background = ""
    else:
        background = get_experiment_background(family) if family else ""
    task_prompt = get_describe_plot_prompt(family) if family else "Describe the figure <image> in JSON format."
    prompt = f"{background}\n\n{task_prompt}" if background else task_prompt

    return {
        "messages": [{"role": "user", "content": prompt}],
        "images": image_data,
        "response_schema": DESCRIBE_PLOT_RESPONSE_SCHEMA,
    }


@task_register
def classify_outcome(
    image_data: str | bytes | list,
    experiment_family: str | ExperimentFamily | None = None,
) -> dict:
    """
    分类实验结果任务 (QCalEval Q2)
    将实验结果分类为: Expected/Suboptimal/Anomalous/Apparatus issue

    Args:
        image_data: 图像数据
        experiment_family: 实验家族（字符串或 ExperimentFamily 枚举），使用专属 prompt

    Returns:
        包含 messages, images 和 response_schema 的字典
    """
    # 获取专属 prompt
    family = experiment_family
    if isinstance(family, ExperimentFamily):
        family = family.value

    # 合并 experiment_background 和任务 prompt
    # 如果prompt中已包含背景信息，则跳过添加
    if family and (family, 2) in PROMPTS_WITH_EMBEDDED_BACKGROUND:
        background = ""
    else:
        background = get_experiment_background(family) if family else ""
    task_prompt = get_classify_outcome_prompt(family) if family else get_classify_outcome_prompt("rabi")
    prompt = f"{background}\n\n{task_prompt}" if background else task_prompt

    return {
        "messages": [{"role": "user", "content": prompt}],
        "images": image_data,
        "response_schema": CLASSIFY_OUTCOME_RESPONSE_SCHEMA,
    }


@task_register
def scientific_reasoning(
    image_data: str | bytes | list,
    experiment_family: str | ExperimentFamily | None = None,
) -> dict:
    """
    科学推理任务 (QCalEval Q3)
    分析实验结果的物理含义并给出下一步建议

    Args:
        image_data: 图像数据
        experiment_family: 实验家族（字符串或 ExperimentFamily 枚举），使用专属 prompt

    Returns:
        包含 messages 和 images 的字典
    """
    # 获取专属 prompt
    family = experiment_family
    if isinstance(family, ExperimentFamily):
        family = family.value

    # 合并 experiment_background 和任务 prompt
    # 如果prompt中已包含背景信息，则跳过添加
    if family and (family, 3) in PROMPTS_WITH_EMBEDDED_BACKGROUND:
        background = ""
    else:
        background = get_experiment_background(family) if family else ""
    task_prompt = get_scientific_reasoning_prompt(family) if family else get_scientific_reasoning_prompt("rabi")
    prompt = f"{background}\n\n{task_prompt}" if background else task_prompt

    return {
        "messages": [{"role": "user", "content": prompt}],
        "images": image_data,
        # Q3 (scientific_reasoning) 是开放性推理任务，输出自由文本
    }


@task_register
def assess_fit(
    image_data: str | bytes | list,
    experiment_family: str | ExperimentFamily | None = None,
) -> dict:
    """
    评估拟合可靠性任务 (QCalEval Q4)
    评估数据拟合是否可用于参数提取

    Args:
        image_data: 图像数据
        experiment_family: 实验家族（字符串或 ExperimentFamily 枚举），使用专属 prompt

    Returns:
        包含 messages, images 和 response_schema 的字典
    """
    # 获取专属 prompt
    family = experiment_family
    if isinstance(family, ExperimentFamily):
        family = family.value

    # 合并 experiment_background 和任务 prompt
    # 如果prompt中已包含背景信息，则跳过添加
    if family and (family, 4) in PROMPTS_WITH_EMBEDDED_BACKGROUND:
        background = ""
    else:
        background = get_experiment_background(family) if family else ""
    task_prompt = get_assess_fit_prompt(family) if family else get_assess_fit_prompt("rabi")
    prompt = f"{background}\n\n{task_prompt}" if background else task_prompt

    return {
        "messages": [{"role": "user", "content": prompt}],
        "images": image_data,
        "response_schema": ASSESS_FIT_RESPONSE_SCHEMA,
    }


@task_register
def extract_params(
    image_data: str | bytes | list,
    experiment_family: str | ExperimentFamily | None = None,
    params_schema: dict | None = None,
) -> dict:
    """
    提取参数任务 (QCalEval Q5)
    从图表中提取指定参数

    Args:
        image_data: 图像数据
        experiment_family: 实验家族（字符串或 ExperimentFamily 枚举），使用专属 prompt
        params_schema: 参数提取模式（可选，默认从experiment_family获取）

    Returns:
        包含 messages, images 和 response_schema 的字典
    """
    # 获取实验家族和 schema
    family = experiment_family
    if isinstance(family, ExperimentFamily):
        family = family.value

    # 获取 schema
    schema = params_schema
    if schema is None and family:
        schema = get_extract_params_schema(family)

    # 合并 experiment_background 和任务 prompt
    # 如果prompt中已包含背景信息，则跳过添加
    if family and (family, 5) in PROMPTS_WITH_EMBEDDED_BACKGROUND:
        background = ""
    else:
        background = get_experiment_background(family) if family else ""
    task_prompt = get_extract_params_prompt(family) if family else get_extract_params_prompt("rabi")
    prompt = f"{background}\n\n{task_prompt}" if background else task_prompt

    return {
        "messages": [{"role": "user", "content": prompt}],
        "images": image_data,
        "response_schema": schema or get_extract_params_schema(family or "rabi"),
    }


@task_register
def evaluate_status(
    image_data: str | bytes | list,
    experiment_family: str | ExperimentFamily | None = None,
) -> dict:
    """
    评估实验状态任务 (QCalEval Q6)
    判断实验成功/失败状态并给出建议

    Args:
        image_data: 图像数据
        experiment_family: 实验家族（字符串或 ExperimentFamily 枚举），使用专属 prompt

    Returns:
        包含 messages, images 和 response_schema 的字典
    """
    # 获取专属 prompt
    family = experiment_family
    if isinstance(family, ExperimentFamily):
        family = family.value

    # 合并 experiment_background 和任务 prompt
    # 如果prompt中已包含背景信息，则跳过添加
    if family and (family, 6) in PROMPTS_WITH_EMBEDDED_BACKGROUND:
        background = ""
    else:
        background = get_experiment_background(family) if family else ""
    task_prompt = get_evaluate_status_prompt(family) if family else get_evaluate_status_prompt("rabi")
    prompt = f"{background}\n\n{task_prompt}" if background else task_prompt

    return {
        "messages": [{"role": "user", "content": prompt}],
        "images": image_data,
        "response_schema": EVALUATE_STATUS_RESPONSE_SCHEMA,
    }