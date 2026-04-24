# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/21
########################################################################

"""
Q4: 评估拟合任务 (中文版)

评估数据拟合是否可用于参数提取
"""

# ========== 独立 Prompt 字符串定义 ==========

# Standard assess fit prompt
PROMPT_STANDARD = """评估此图中<image>数据的拟合是否可靠，可用于参数提取。

选项：
- Reliable (可靠)
- Unreliable (不可靠)
- No fit (无拟合)

请按以下格式提供答案：
Assessment: <your choice>
Reason: <brief explanation>"""

# Special case for qubit_spectroscopy_power_frequency (has background)
PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """这是一个二维量子比特谱实验，测试标准的transmon量子比特（负非谐性，所以f02/2出现在比f01更低的频率）：我们同时扫描驱动功率和频率来绘制量子比特跃迁图。成功的结果会显示清晰的跃迁线（f01，可选地还有f02/2）以及明显的功率依赖性。

评估这些图中<image>、<image>和<image>数据的拟合是否可靠，可用于参数提取。

选项：
- Reliable (可靠)
- Unreliable (不可靠)
- No fit (无拟合)

请按以下格式提供答案：
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

ASSESS_FIT_PROMPTS_ZH = {
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


def get_assess_fit_prompt_zh(experiment_family: str) -> str:
    """获取评估拟合的中文专属 prompt"""
    return ASSESS_FIT_PROMPTS_ZH.get(experiment_family, ASSESS_FIT_PROMPTS_ZH["rabi"])


__all__ = [
    "ASSESS_FIT_PROMPTS_ZH",
    "get_assess_fit_prompt_zh",
]