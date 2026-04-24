# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/21
########################################################################

"""
Q2: 分类实验结果任务 (中文版)

将实验结果分类为: Expected/Suboptimal/Anomalous/Apparatus issue
"""

# ========== 独立 Prompt 字符串定义 ==========

# Standard classify outcome prompt
PROMPT_STANDARD = """根据您在数据<image>中观察到的内容，对实验结果进行分类。

选项：
- Expected behavior: 实验产生了可用的校准数据
- Suboptimal parameters: 正常工作但需要在此实验内调整参数
- Anomalous behavior: 需要上游重新校准或显示不可控的量子效应
- Apparatus issue: 无有效信号——测量系统配置错误

请按以下格式提供答案：
Classification: <your choice>
Reason: <brief explanation>"""

# Special case for qubit_spectroscopy_power_frequency (has background)
PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """这是一个二维量子比特谱实验，测试标准的transmon量子比特（负非谐性，所以f02/2出现在比f01更低的频率）：我们同时扫描驱动功率和频率来绘制量子比特跃迁图。成功的结果会显示清晰的跃迁线（f01，可选地还有f02/2）以及明显的功率依赖性。

根据您在数据<image>中观察到的内容，对实验结果进行分类。

选项：
- Expected behavior: 实验产生了可用的校准数据
- Suboptimal parameters: 正常工作但需要在此实验内调整参数
- Anomalous behavior: 需要上游重新校准或显示不可控的量子效应
- Apparatus issue: 无有效信号——测量系统配置错误

请按以下格式提供答案：
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

# ========== Not in QCalEval ==========
PROMPT_S21 = PROMPT_STANDARD



# ========== Prompt 字典映射 ==========

CLASSIFY_OUTCOME_PROMPTS_ZH = {
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


def get_classify_outcome_prompt_zh(experiment_family: str) -> str:
    """获取分类实验结果的中文专属 prompt"""
    return CLASSIFY_OUTCOME_PROMPTS_ZH.get(experiment_family, CLASSIFY_OUTCOME_PROMPTS_ZH["rabi"])


__all__ = [
    "CLASSIFY_OUTCOME_PROMPTS_ZH",
    "get_classify_outcome_prompt_zh",
]