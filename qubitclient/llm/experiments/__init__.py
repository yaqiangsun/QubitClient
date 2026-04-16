# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/16 14:43:09
########################################################################

"""
QCalEval 实验配置模块

本模块包含 QCalEval VLM 任务的 Prompt 和 Response Schema:
- Q1: describe_plot - 描述图表
- Q2: classify_outcome - 分类实验结果
- Q3: scientific_reasoning - 科学推理
- Q4: assess_fit - 评估拟合
- Q5: extract_params - 提取参数
- Q6: evaluate_status - 评估状态
"""

from qubitclient.llm.experiments.q1_describe_plot import (
    DESCRIBE_PLOT_PROMPTS,
    DESCRIBE_PLOT_RESPONSE_SCHEMA,
    get_describe_plot_prompt,
)

from qubitclient.llm.experiments.q2_classify_outcome import (
    CLASSIFY_OUTCOME_PROMPTS,
    CLASSIFY_OUTCOME_RESPONSE_SCHEMA,
    get_classify_outcome_prompt,
)

from qubitclient.llm.experiments.q3_scientific_reasoning import (
    SCIENTIFIC_REASONING_PROMPTS,
    get_scientific_reasoning_prompt,
)

from qubitclient.llm.experiments.q4_assess_fit import (
    ASSESS_FIT_PROMPTS,
    ASSESS_FIT_RESPONSE_SCHEMA,
    get_assess_fit_prompt,
)

from qubitclient.llm.experiments.q5_extract_params import (
    EXTRACT_PARAMS_PROMPTS,
    EXTRACT_PARAMS_SCHEMAS,
    get_extract_params_prompt,
    get_extract_params_schema,
)

from qubitclient.llm.experiments.q6_evaluate_status import (
    EVALUATE_STATUS_PROMPTS,
    EVALUATE_STATUS_RESPONSE_SCHEMA,
    get_evaluate_status_prompt,
)

from qubitclient.llm.experiments.experiment_background import (
    EXPERIMENT_BACKGROUNDS,
    get_experiment_background,
    DEFAULT_BACKGROUND,
)

__all__ = [
    # Q1: describe_plot
    "DESCRIBE_PLOT_PROMPTS",
    "DESCRIBE_PLOT_RESPONSE_SCHEMA",
    "get_describe_plot_prompt",
    # Q2: classify_outcome
    "CLASSIFY_OUTCOME_PROMPTS",
    "CLASSIFY_OUTCOME_RESPONSE_SCHEMA",
    "get_classify_outcome_prompt",
    # Q3: scientific_reasoning
    "SCIENTIFIC_REASONING_PROMPTS",
    "get_scientific_reasoning_prompt",
    # Q4: assess_fit
    "ASSESS_FIT_PROMPTS",
    "ASSESS_FIT_RESPONSE_SCHEMA",
    "get_assess_fit_prompt",
    # Q5: extract_params
    "EXTRACT_PARAMS_PROMPTS",
    "EXTRACT_PARAMS_SCHEMAS",
    "get_extract_params_prompt",
    "get_extract_params_schema",
    # Q6: evaluate_status
    "EVALUATE_STATUS_PROMPTS",
    "EVALUATE_STATUS_RESPONSE_SCHEMA",
    "get_evaluate_status_prompt",
    # experiment_background
    "EXPERIMENT_BACKGROUNDS",
    "get_experiment_background",
    "DEFAULT_BACKGROUND",
]