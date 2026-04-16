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
DEFAULT_DECISION_PROMPT = """基于以下评估结果和上下文信息，给出下一步测量目标及参数建议。

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

{context_info}

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


def get_decision_prompt(
    evaluation_result: str,
    available_actions: list | None = None,
    context: str | None = None,
) -> str:
    """
    获取决策提示词

    Args:
        evaluation_result: 评估结果字符串
        available_actions: 可用行动列表
        context: 上下文信息字符串

    Returns:
        格式化后的提示词
    """
    # 构建上下文信息
    if context:
        context_info = f"上下文信息:\n{context}"
    else:
        context_info = "上下文信息: (无)"

    prompt = DEFAULT_DECISION_PROMPT.format(
        evaluation_result=evaluation_result,
        context_info=context_info,
    )
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


# ========== QCalEval Prompt Templates ==========

# Q1: 描述图表
DEFAULT_DESCRIBE_PLOT_PROMPT = """Describe the figure <image> in JSON format.

Required fields:
{{background}}
{{schema}}
"""

DESCRIBE_PLOT_SCHEMA = """{
  "plot_type": "scatter" | "line" | "heatmap" | "histogram",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "main_features": string
}"""


# Q2: 分类实验结果
DEFAULT_CLASSIFY_OUTCOME_PROMPT = """{{background}}

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Experiment produced usable calibration data
- Suboptimal parameters: Working but needs parameter adjustment within this experiment
- Anomalous behavior: Requires upstream recalibration or shows uncontrollable quantum effects
- Apparatus issue: No meaningful signal — measurement system misconfigured

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>
"""

CLASSIFY_OUTCOME_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "Classification": {
            "type": "string",
            "enum": [
                "Expected behavior",
                "Suboptimal parameters",
                "Anomalous behavior",
                "Apparatus issue",
            ],
        },
        "Reason": {"type": "string"},
    },
    "required": ["Classification", "Reason"],
}


# Q3: 科学推理
DEFAULT_SCIENTIFIC_REASONING_PROMPT = """{{background}}

What does this result <image> imply?

Explain:
- What the key features indicate about the physical system
- Whether the measurement quality is sufficient for reliable analysis
- What calibration step follows (if applicable)

Provide your assessment.
"""


# Q4: 评估拟合
DEFAULT_ASSESS_FIT_PROMPT = """{{background}}

Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable
- Unreliable
- No fit

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>
"""

ASSESS_FIT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "Assessment": {
            "type": "string",
            "enum": ["Reliable", "Unreliable", "No fit"],
        },
        "Reason": {"type": "string"},
    },
    "required": ["Assessment", "Reason"],
}


# Q5: 提取参数
DEFAULT_EXTRACT_PARAMS_PROMPT = """{{background}}

Extract the following parameters from this calibration plot <image>.

Report in JSON format:
{{params_schema}}
"""

DEFAULT_EXTRACT_PARAMS_SCHEMA = '{"optimal_value": float, "intersection_clear": true | false}'

EXTRACT_PARAMS_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "optimal_value": {"type": "number", "description": "Extracted optimal parameter value"},
        "intersection_clear": {"type": "boolean", "description": "Whether the intersection/crossing is clear"},
    },
    "required": ["optimal_value", "intersection_clear"],
}


# Q6: 评估状态
DEFAULT_EVALUATE_STATUS_PROMPT = """{{background}}

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear signal observed in measurement window
- NO_SIGNAL: Flat or random, no meaningful pattern
- OPTIMAL_NOT_CENTERED: Signal exists but not in optimal range

When the status is not SUCCESS, provide a SPECIFIC suggested range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>
"""

EVALUATE_STATUS_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "Status": {
            "type": "string",
            "enum": ["SUCCESS", "NO_SIGNAL", "OPTIMAL_NOT_CENTERED"],
        },
        "Suggested range": {"type": "string"},
        "Notes": {"type": "string"},
    },
    "required": ["Status", "Suggested range", "Notes"],
}


# ========== QCalEval Prompt Functions ==========


def get_describe_plot_prompt(experiment_background: str | None = None) -> str:
    """获取描述图表的提示词"""
    background = f"{experiment_background}\n\n" if experiment_background else ""
    return DEFAULT_DESCRIBE_PLOT_PROMPT.replace("{{background}}", background).replace("{{schema}}", DESCRIBE_PLOT_SCHEMA)


def get_classify_outcome_prompt(experiment_background: str) -> str:
    """获取分类实验结果的提示词"""
    return DEFAULT_CLASSIFY_OUTCOME_PROMPT.replace("{{background}}", experiment_background or "")


def get_scientific_reasoning_prompt(experiment_background: str) -> str:
    """获取科学推理的提示词"""
    return DEFAULT_SCIENTIFIC_REASONING_PROMPT.replace("{{background}}", experiment_background or "")


def get_assess_fit_prompt(experiment_background: str) -> str:
    """获取评估拟合的提示词"""
    return DEFAULT_ASSESS_FIT_PROMPT.replace("{{background}}", experiment_background or "")


def get_extract_params_prompt(
    experiment_background: str,
    params_schema: str | None = None,
) -> str:
    """获取提取参数的提示词"""
    schema = params_schema or DEFAULT_EXTRACT_PARAMS_SCHEMA
    return DEFAULT_EXTRACT_PARAMS_PROMPT.replace("{{background}}", experiment_background or "").replace("{{params_schema}}", schema)


def get_evaluate_status_prompt(experiment_background: str) -> str:
    """获取评估实验状态的提示词"""
    return DEFAULT_EVALUATE_STATUS_PROMPT.replace("{{background}}", experiment_background or "")


# Q1 Response Schema
DESCRIBE_PLOT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "plot_type": {
            "type": "string",
            "enum": ["scatter", "line", "heatmap", "histogram"],
        },
        "x_axis": {
            "type": "object",
            "properties": {
                "label": {"type": "string"},
                "scale": {"type": "string", "enum": ["linear", "log"]},
                "range": {"type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2},
            },
            "required": ["label", "scale", "range"],
        },
        "y_axis": {
            "type": "object",
            "properties": {
                "label": {"type": "string"},
                "scale": {"type": "string", "enum": ["linear", "log"]},
                "range": {"type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2},
            },
            "required": ["label", "scale", "range"],
        },
        "main_features": {"type": "string"},
    },
    "required": ["plot_type", "x_axis", "y_axis", "main_features"],
}


__all__ = [
    # Base prompts
    "DEFAULT_DECISION_PROMPT",
    # Base schemas
    "DECISION_RESPONSE_SCHEMA",
    # Base functions
    "get_decision_prompt",
    # QCalEval prompts
    "get_describe_plot_prompt",
    "get_classify_outcome_prompt",
    "get_scientific_reasoning_prompt",
    "get_assess_fit_prompt",
    "get_extract_params_prompt",
    "get_evaluate_status_prompt",
    # QCalEval schemas
    "DESCRIBE_PLOT_RESPONSE_SCHEMA",
    "CLASSIFY_OUTCOME_RESPONSE_SCHEMA",
    "ASSESS_FIT_RESPONSE_SCHEMA",
    "EXTRACT_PARAMS_RESPONSE_SCHEMA",
    "EVALUATE_STATUS_RESPONSE_SCHEMA",
]