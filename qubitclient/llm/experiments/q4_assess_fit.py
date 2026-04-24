# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
Q4: 评估拟合任务

评估数据拟合是否可用于参数提取
"""

# ========== 独立 Prompt 字符串定义 ==========

# Standard assess fit prompt
PROMPT_STANDARD = """Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable
- Unreliable
- No fit

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

# Special case for qubit_spectroscopy_power_frequency (has background)
PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """This is a 2D qubit spectroscopy experiment on a standard transmon (negative anharmonicity, so f02/2 appears at a lower frequency than f01): we sweep both drive power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, and optionally f02/2) with visible power dependence.

Assess whether the fit to the data in these plots <image>, <image> and <image> is reliable for parameter extraction.

Options:
- Reliable
- Unreliable
- No fit

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

# Aliases for all experiments
PROMPT_COUPLER_FLUX = PROMPT_STANDARD
PROMPT_CZ_BENCHMARKING = PROMPT_STANDARD
PROMPT_DRAG = PROMPT_STANDARD
PROMPT_GMM = PROMPT_STANDARD
PROMPT_MICROWAVE_RAMSEY = PROMPT_STANDARD
PROMPT_MOT_LOADING = PROMPT_STANDARD
PROMPT_PINCHOFF = PROMPT_STANDARD
PROMPT_PINGPONG = PROMPT_STANDARD
PROMPT_QUBIT_FLUX_SPECTROSCOPY = PROMPT_STANDARD
PROMPT_QUBIT_SPECTROSCOPY = PROMPT_STANDARD
# Note: PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY already defined above
PROMPT_RABI = PROMPT_STANDARD
PROMPT_RABI_HW = PROMPT_STANDARD
PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = PROMPT_STANDARD
PROMPT_RAMSEY_FREQ_CAL = PROMPT_STANDARD
PROMPT_RAMSEY_T2STAR = PROMPT_STANDARD
PROMPT_RES_SPEC = PROMPT_STANDARD
PROMPT_RYDBERG_RAMSEY = PROMPT_STANDARD
PROMPT_RYDBERG_SPECTROSCOPY = PROMPT_STANDARD
PROMPT_T1 = PROMPT_STANDARD
PROMPT_T1_FLUCTUATIONS = PROMPT_STANDARD
PROMPT_TWEEZER_ARRAY = PROMPT_STANDARD

# ========== Not in QCalEval ==========
PROMPT_S21 = PROMPT_STANDARD



# ========== Prompt 字典映射 ==========

ASSESS_FIT_PROMPTS = {
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
    # ========== Not in QCalEval ==========
    "s21": PROMPT_S21,
}


def get_assess_fit_prompt(experiment_family: str) -> str:
    """获取评估拟合的专属 prompt"""
    return ASSESS_FIT_PROMPTS.get(experiment_family, ASSESS_FIT_PROMPTS["rabi"])


# Q4: 评估拟合 Response Schema
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


__all__ = [
    "ASSESS_FIT_PROMPTS",
    "ASSESS_FIT_RESPONSE_SCHEMA",
    "get_assess_fit_prompt",
]