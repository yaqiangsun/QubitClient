# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
Q2: 分类实验结果任务

将实验结果分类为: Expected/Suboptimal/Anomalous/Apparatus issue
"""

# ========== 独立 Prompt 字符串定义 ==========

# Standard classify outcome prompt
PROMPT_STANDARD = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Experiment produced usable calibration data
- Suboptimal parameters: Working but needs parameter adjustment within this experiment
- Anomalous behavior: Requires upstream recalibration or shows uncontrollable quantum effects
- Apparatus issue: No meaningful signal — measurement system misconfigured

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

# Special case for qubit_spectroscopy_power_frequency (has background)
PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """This is a 2D qubit spectroscopy experiment on a standard transmon (negative anharmonicity, so f02/2 appears at a lower frequency than f01): we sweep both drive power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, and optionally f02/2) with visible power dependence.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Experiment produced usable calibration data
- Suboptimal parameters: Working but needs parameter adjustment within this experiment
- Anomalous behavior: Requires upstream recalibration or shows uncontrollable quantum effects
- Apparatus issue: No meaningful signal — measurement system misconfigured

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

# Aliases for all experiments (most use the same prompt)
PROMPT_COUPLER_FLUX = PROMPT_STANDARD
PROMPT_CZ_BENCHMARKING = PROMPT_STANDARD
PROMPT_DRAG = PROMPT_STANDARD
PROMPT_GMM = PROMPT_STANDARD
PROMPT_MICROWAVE_RAMSEY = PROMPT_STANDARD
PROMPT_MOT_LOADING = PROMPT_STANDARD
PROMPT_PINCHOFF = PROMPT_STANDARD

# Aliases for remaining experiments
PROMPT_PINGPONG = PROMPT_STANDARD
PROMPT_QUBIT_FLUX_SPECTROSCOPY = PROMPT_STANDARD
PROMPT_QUBIT_SPECTROSCOPY = PROMPT_STANDARD
# Note: PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY already defined above with special case
PROMPT_RABI = PROMPT_STANDARD
PROMPT_RABI_HW = PROMPT_STANDARD
PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = PROMPT_STANDARD
PROMPT_RAMSEY_FREQ_CAL = PROMPT_STANDARD
PROMPT_RAMSEY_T2STAR = PROMPT_STANDARD
PROMPT_RES_SPEC = PROMPT_STANDARD
PROMPT_RYDBERG_RAMSEY = PROMPT_STANDARD

# Aliases for remaining experiments
PROMPT_RYDBERG_SPECTROSCOPY = PROMPT_STANDARD
PROMPT_T1 = PROMPT_STANDARD
PROMPT_T1_FLUCTUATIONS = PROMPT_STANDARD
PROMPT_TWEEZER_ARRAY = PROMPT_STANDARD


# ========== Prompt 字典映射 ==========

CLASSIFY_OUTCOME_PROMPTS = {
    "coupler_flux": PROMPT_COUPLER_FLUX,
    "cz_benchmarking": PROMPT_CZ_BENCHMARKING,
    "drag": PROMPT_DRAG,
    "gmm": PROMPT_GMM,
    "microwave_ramsey": PROMPT_MICROWAVE_RAMSEY,
    "mot_loading": PROMPT_MOT_LOADING,
    "pinchoff": PROMPT_PINCHOFF,
    "pingpong": PROMPT_PINGPONG,
    "qubit_flux_spectroscopy": PROMPT_QUBIT_FLUX_SPECTROSCOPY,
    "qubit_spectroscopy": PROMPT_QUBIT_SPECTROSCOPY,
    "qubit_spectroscopy_power_frequency": PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY,
    "rabi": PROMPT_RABI,
    "rabi_hw": PROMPT_RABI_HW,
    "ramsey_charge_tomography": PROMPT_RAMSEY_CHARGE_TOMOGRAPHY,
    "ramsey_freq_cal": PROMPT_RAMSEY_FREQ_CAL,
    "ramsey_t2star": PROMPT_RAMSEY_T2STAR,
    "res_spec": PROMPT_RES_SPEC,
    "rydberg_ramsey": PROMPT_RYDBERG_RAMSEY,
    "rydberg_spectroscopy": PROMPT_RYDBERG_SPECTROSCOPY,
    "t1": PROMPT_T1,
    "t1_fluctuations": PROMPT_T1_FLUCTUATIONS,
    "tweezer_array": PROMPT_TWEEZER_ARRAY,
}


def get_classify_outcome_prompt(experiment_family: str) -> str:
    """获取分类实验结果的专属 prompt"""
    return CLASSIFY_OUTCOME_PROMPTS.get(experiment_family, CLASSIFY_OUTCOME_PROMPTS["rabi"])


# Q2: 分类实验结果 Response Schema
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


__all__ = [
    "CLASSIFY_OUTCOME_PROMPTS",
    "CLASSIFY_OUTCOME_RESPONSE_SCHEMA",
    "get_classify_outcome_prompt",
]