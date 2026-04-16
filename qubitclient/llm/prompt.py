# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
LLM/VLM Prompt 模板
"""

# 默认评估提示词
DEFAULT_EVALUATION_PROMPT = """你是一个量子测量数据分析专家。请评估以下分析结果的质量。

分析结果:
{analysis_result}

评估标准:
- 数据质量评分 (0-100)
- 主要问题分析
- 改进建议

请以 JSON 格式返回评估结果，包含以下字段:
- score: 质量评分 (0-100)
- issues: 主要问题列表
- suggestions: 改进建议列表
"""

# 默认决策提示词
DEFAULT_DECISION_PROMPT = """基于以下评估结果，建议下一步应该执行的测量任务。

评估结果:
{evaluation_result}

可选任务类型:
- s21: S21 频率扫描
- s21multi: 多 qubit S21 扫描
- rabi: Rabi 实验
- ramsey: Ramsey 实验
- t1: T1 弛豫时间测量
- drag: DRAG 优化
- delta: Delta 测量
- powershift: 功率偏移测量
- spectrum: 频谱测量
- spectrum_2d: 二维频谱测量
- singleshot: 单次测量
- rb: 随机基准测试

请以 JSON 格式返回决策，包含以下字段:
- recommended_task: 推荐的下一个任务名称
- task_params: 推荐的任务参数字典
- reason: 决策原因
"""

# 默认图像分析提示词
DEFAULT_VLM_ANALYZE_PROMPT = "你是一个量子物理实验专家。请分析这张测量图像，描述你观察到的特征、物理意义以及可能的优化方向。"

# 参数建议提示词
DEFAULT_SUGGEST_PARAMS_PROMPT = """根据以下上下文信息，为 {task_type} 任务建议最优参数。

上下文信息:
{context}

请以 JSON 格式返回建议的参数。"""

# 评估响应 JSON Schema
EVALUATION_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "number"},
        "issues": {"type": "array", "items": {"type": "string"}},
        "suggestions": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["score", "issues", "suggestions"]
}

# 决策响应 JSON Schema
DECISION_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "recommended_task": {"type": "string"},
        "task_params": {"type": "object"},
        "reason": {"type": "string"}
    },
    "required": ["recommended_task", "task_params", "reason"]
}

# 参数建议响应 JSON Schema
SUGGEST_PARAMS_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "suggested_params": {"type": "object"},
        "reason": {"type": "string"}
    },
    "required": ["suggested_params", "reason"]
}


def get_evaluation_prompt(analysis_result: str, criteria: str | None = None) -> str:
    """
    获取评估提示词

    Args:
        analysis_result: 分析结果字符串
        criteria: 自定义评估标准（可选）

    Returns:
        格式化后的提示词
    """
    prompt = DEFAULT_EVALUATION_PROMPT.format(analysis_result=analysis_result)
    if criteria:
        prompt += f"\n\n自定义评估标准: {criteria}"
    return prompt


def get_decision_prompt(evaluation_result: str, available_actions: list | None = None) -> str:
    """
    获取决策提示词

    Args:
        evaluation_result: 评估结果字符串
        available_actions: 可用行动列表

    Returns:
        格式化后的提示词
    """
    prompt = DEFAULT_DECISION_PROMPT.format(evaluation_result=evaluation_result)
    if available_actions:
        prompt += f"\n\n可用的行动: {available_actions}"
    return prompt


def get_suggest_params_prompt(task_type: str, context: str) -> str:
    """
    获取参数建议提示词

    Args:
        task_type: 任务类型
        context: 上下文信息

    Returns:
        格式化后的提示词
    """
    return DEFAULT_SUGGEST_PARAMS_PROMPT.format(
        task_type=task_type,
        context=context
    )


def get_vlm_analyze_prompt(prompt: str | None = None) -> str:
    """
    获取 VLM 分析提示词

    Args:
        prompt: 自定义提示词

    Returns:
        提示词
    """
    return prompt or DEFAULT_VLM_ANALYZE_PROMPT


__all__ = [
    "DEFAULT_EVALUATION_PROMPT",
    "DEFAULT_DECISION_PROMPT",
    "DEFAULT_VLM_ANALYZE_PROMPT",
    "DEFAULT_SUGGEST_PARAMS_PROMPT",
    "EVALUATION_RESPONSE_SCHEMA",
    "DECISION_RESPONSE_SCHEMA",
    "SUGGEST_PARAMS_RESPONSE_SCHEMA",
    "get_evaluation_prompt",
    "get_decision_prompt",
    "get_suggest_params_prompt",
    "get_vlm_analyze_prompt",
]