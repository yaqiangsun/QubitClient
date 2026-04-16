# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/16 13:23:10
########################################################################

"""
决策模块 - 测量策略决策

包含决策相关的 prompt 和 response schema
"""

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

DECISION_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "recommended_task": {"type": "string"},
        "task_params": {"type": "object"},
        "reason": {"type": "string"}
    },
    "required": ["recommended_task", "task_params", "reason"]
}


def get_decision_prompt(
    evaluation_result: str,
    available_actions: list | None = None,
    context: str | None = None,
) -> str:
    """获取决策提示词"""
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


__all__ = [
    "DEFAULT_DECISION_PROMPT",
    "DECISION_RESPONSE_SCHEMA",
    "get_decision_prompt",
]