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

from qubitclient.llm.experiments.q1_describe_plot_zh import (
    DESCRIBE_PLOT_PROMPTS_ZH,
    get_describe_plot_prompt_zh,
)

from qubitclient.llm.experiments.q2_classify_outcome import (
    CLASSIFY_OUTCOME_PROMPTS,
    CLASSIFY_OUTCOME_RESPONSE_SCHEMA,
    get_classify_outcome_prompt,
)

from qubitclient.llm.experiments.q2_classify_outcome_zh import (
    CLASSIFY_OUTCOME_PROMPTS_ZH,
    get_classify_outcome_prompt_zh,
)

from qubitclient.llm.experiments.q3_scientific_reasoning import (
    SCIENTIFIC_REASONING_PROMPTS,
    get_scientific_reasoning_prompt,
)

from qubitclient.llm.experiments.q3_scientific_reasoning_zh import (
    SCIENTIFIC_REASONING_PROMPTS_ZH,
    get_scientific_reasoning_prompt_zh,
)

from qubitclient.llm.experiments.q4_assess_fit import (
    ASSESS_FIT_PROMPTS,
    ASSESS_FIT_RESPONSE_SCHEMA,
    get_assess_fit_prompt,
)

from qubitclient.llm.experiments.q4_assess_fit_zh import (
    ASSESS_FIT_PROMPTS_ZH,
    get_assess_fit_prompt_zh,
)

from qubitclient.llm.experiments.q5_extract_params import (
    EXTRACT_PARAMS_PROMPTS,
    EXTRACT_PARAMS_SCHEMAS,
    get_extract_params_prompt,
    get_extract_params_schema,
)

from qubitclient.llm.experiments.q5_extract_params_zh import (
    EXTRACT_PARAMS_PROMPTS_ZH,
    get_extract_params_prompt_zh,
)

from qubitclient.llm.experiments.q6_evaluate_status import (
    EVALUATE_STATUS_PROMPTS,
    EVALUATE_STATUS_RESPONSE_SCHEMA,
    get_evaluate_status_prompt,
)

from qubitclient.llm.experiments.q6_evaluate_status_zh import (
    EVALUATE_STATUS_PROMPTS_ZH,
    get_evaluate_status_prompt_zh,
)

from qubitclient.llm.experiments.experiment_background import (
    EXPERIMENT_BACKGROUNDS,
    get_experiment_background,
    DEFAULT_BACKGROUND,
)

from qubitclient.llm.experiments.experiment_background_zh import (
    EXPERIMENT_BACKGROUNDS_ZH,
    get_experiment_background_zh,
)

__all__ = [
    # Q1: describe_plot
    "DESCRIBE_PLOT_PROMPTS",
    "DESCRIBE_PLOT_PROMPTS_ZH",
    "DESCRIBE_PLOT_RESPONSE_SCHEMA",
    "get_describe_plot_prompt",
    "get_describe_plot_prompt_zh",
    # Q2: classify_outcome
    "CLASSIFY_OUTCOME_PROMPTS",
    "CLASSIFY_OUTCOME_PROMPTS_ZH",
    "CLASSIFY_OUTCOME_RESPONSE_SCHEMA",
    "get_classify_outcome_prompt",
    "get_classify_outcome_prompt_zh",
    # Q3: scientific_reasoning
    "SCIENTIFIC_REASONING_PROMPTS",
    "SCIENTIFIC_REASONING_PROMPTS_ZH",
    "get_scientific_reasoning_prompt",
    "get_scientific_reasoning_prompt_zh",
    # Q4: assess_fit
    "ASSESS_FIT_PROMPTS",
    "ASSESS_FIT_PROMPTS_ZH",
    "ASSESS_FIT_RESPONSE_SCHEMA",
    "get_assess_fit_prompt",
    "get_assess_fit_prompt_zh",
    # Q5: extract_params
    "EXTRACT_PARAMS_PROMPTS",
    "EXTRACT_PARAMS_PROMPTS_ZH",
    "EXTRACT_PARAMS_SCHEMAS",
    "get_extract_params_prompt",
    "get_extract_params_prompt_zh",
    "get_extract_params_schema",
    # Q6: evaluate_status
    "EVALUATE_STATUS_PROMPTS",
    "EVALUATE_STATUS_PROMPTS_ZH",
    "EVALUATE_STATUS_RESPONSE_SCHEMA",
    "get_evaluate_status_prompt",
    "get_evaluate_status_prompt_zh",
    # experiment_background
    "EXPERIMENT_BACKGROUNDS",
    "EXPERIMENT_BACKGROUNDS_ZH",
    "get_experiment_background",
    "get_experiment_background_zh",
    "DEFAULT_BACKGROUND",
]