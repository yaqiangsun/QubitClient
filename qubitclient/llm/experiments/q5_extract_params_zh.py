# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/21
########################################################################

"""
Q5: 提取参数任务 (中文版)

从图表中提取指定参数
"""

# ========== 独立 Prompt 字符串定义 ==========

# Special case: prompt includes background (different from experiment_background field)
PROMPT_COUPLER_FLUX = """这是可调耦合器谱：我们绘制耦合器频率响应与施加的磁通偏置的关系。每张图有两个面板（左和右），每个面板显示不同的量子比特。有三个频率分支被两个避免交叉分隔。

从该耦合器磁通图<image>中提取以下参数。

以JSON格式报告：
{"crossing_voltages_V": [float, float], "left_fig_branch_freqs_GHz": [float, float, float], "right_fig_branch_freqs_GHz": [float, float, float]}

crossing_voltages_V: 两个发生避免交叉的偏置电压，从左到右排序。
left/right_fig_branch_freqs_GHz: 每个面板中三个分支的 plateau 频率，沿电压轴从左到右排序。如果拟合太差无法读取，使用 "Unreliable"。"""

PROMPT_CZ_BENCHMARKING = """从该CZ基准测试数据<image>中提取以下参数。

从标题中读取位点/量子比特对索引（例如，'Sites (9, 11)'）。
从标题中读取不确定性（括号表示法，例如，'0.9955 (4)' 表示 0.9955 +/- 0.0004）。

以JSON格式报告：
{"site_indices": [int, int], "retention_per_cz": float, "retention_per_cz_unc": float, "cycle_polarization": float, "cycle_polarization_unc": float, "chi_squared_retention": float | null, "chi_squared_polarization": float | null, "max_circuit_depth": int}"""

PROMPT_DRAG = """从该DRAG校准图<image>中提取以下参数。

以JSON格式报告：
{"optimal_alpha_inv": float, "intersection_clear": true | false}"""

PROMPT_GMM = """从该GMM图<image>中提取以下参数。

以JSON格式报告：
{"separation": "well-separated" | "touching" | "overlapping", "cluster0_center": [I, Q], "cluster1_center": [I, Q]}"""

PROMPT_MICROWAVE_RAMSEY = """从该微波Ramsey图<image>中提取以下参数。

从标题中读取失谐及其不确定性（+/- 表示法）。

以JSON格式报告：
{"detuning_Hz": float | null, "detuning_Hz_unc": float | null, "contrast": float, "retention_min": float}"""

PROMPT_MOT_LOADING = """从该MOT图像<image>中提取云参数。

以JSON格式报告：
{"has_cloud": true | false, "center_x": int, "center_y": int, "cloud_present": true | false}

- has_cloud: 是否可以看到明显的原子云
- center_x: 云中心的近似 x 坐标（像素）
- center_y: 云中心的近似 y 坐标（像素）
- cloud_present: 与 has_cloud 相同（用于验证）

如果看不到云，报告中心坐标为 0。"""

PROMPT_PINCHOFF = """从该夹断测量<image>中提取关键转变索引。

x轴显示门电压索引（0-40，共41个点）。
识别三个关键位置作为索引值：

以JSON格式报告：
{"cut_off_index": int | null, "transition_index": int | null, "saturation_index": int | null}

- saturation_index: 电流首次达到其高 plateau（饱和区）的索引
- transition_index: 转变区域中点的索引
- cut_off_index: 电流达到其低 plateau（器件夹断）的索引

如果转变不够清晰无法识别这些索引，使用 null。"""

PROMPT_PINGPONG = """从该PingPong测量<image>中提取以下参数。

以JSON格式报告：
{"error_per_gate": float | null, "accumulation_type": "linear" | "oscillatory" | "none"}"""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """从该量子比特谱图<image>中提取以下参数。

以JSON格式报告：
{"num_resonances": int, "resonance_freq_GHz": float}"""

PROMPT_QUBIT_SPECTROSCOPY = """从该谱图<image>中提取以下参数。

以JSON格式报告：
{"num_resonances": int, "resonance_freq_GHz": float, "resonance_type": "peak" | "dip"}"""

# Special case: prompt includes background (different version from experiment_background field)
PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """这是一个二维量子比特谱实验，测试标准的transmon量子比特（负非谐性，所以f02/2出现在比f01更低的频率）：我们同时扫描驱动功率和频率来绘制量子比特跃迁图。成功的结果会显示清晰的跃迁线（f01，可选地还有f02/2）以及明显的功率依赖性。

从该二维量子比特谱图<image>中提取以下参数。

以JSON格式报告：
{"f01_MHz": float | null, "transitions_visible": "f01_only" | "f01_f02half" | "none", "power_regime": "optimal" | "high" | "none", "measurement_usable": bool}"""

PROMPT_RABI = """从该Rabi振荡图<image>中提取以下参数。

以JSON格式报告：
{"periods_visible": float, "amplitude_decay": "stable" | "decaying" | "growing", "signal_quality": "clean" | "noisy" | "distorted"}"""

PROMPT_RABI_HW = """从该Rabi振荡图<image>中提取以下参数。

以JSON格式报告：
{"periods_visible": float, "amplitude_decay": "stable" | "decaying" | "growing", "signal_quality": "clean" | "noisy" | "distorted"}"""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """分析该Ramsey电荷层析扫描<image]中的电荷跳跃事件。

分类是否检测到任何电荷跳跃事件，如果是，提取位置和大小。

以JSON格式报告：
{"event_detected": true | false, "jump_count": int, "jump_positions": [int, ...], "jump_sizes_mV": [float, ...]}

- event_detected: 是否可以看到任何电荷跳跃事件
- jump_count: 电荷跳跃事件的总数（水平不连续）
- jump_positions: 发生跳跃的扫描编号列表（近似值）
- jump_sizes_mV: 每个检测到的跳跃的估计电荷跳跃大小（mV）"""

PROMPT_RAMSEY_FREQ_CAL = """从该Ramsey测量<image>中提取以下参数。

以JSON格式报告：
{"T2_star_us": float | null, "detuning_MHz": float | null, "fringes_visible": int}"""

PROMPT_RAMSEY_T2STAR = """从该Ramsey测量<image>中提取以下参数。

以JSON格式报告：
{"T2_star_us": float | null, "detuning_MHz": float | null, "fringes_visible": int}"""

PROMPT_RES_SPEC = """从该谐振器谱图<image>中提取以下参数。

以JSON格式报告：
{"resonance_freq_GHz": float | null, "contrast": float | null}"""

PROMPT_RYDBERG_RAMSEY = """从该Rydberg Ramsey图<image>中提取以下参数。

从标题/头部读取不确定性（+/- 表示法或括号表示法）。

以JSON格式报告：
{"frequency_MHz": float, "frequency_MHz_unc": float, "T2_us": float, "T2_us_unc": float, "RChi2": float, "frequency_noise_kHz": float | null}"""

PROMPT_RYDBERG_SPECTROSCOPY = """从该Rydberg谱图<image>中提取以下参数。

如果图显示多个位点/面板，报告一个JSON数组，每个位点一个对象。
从图中读取位点索引标签（例如，153、171）。从标题/头部读取不确定性（+/- 或括号表示法）。

以JSON格式报告（对象数组，每个位点一个）：
[{"site_index": int, "f0_kHz": float, "f0_kHz_unc": float, "t_ns": float, "t_ns_unc": float, "f_Rabi_MHz": float, "f_Rabi_MHz_unc": float, "chi_squared": float}]"""

PROMPT_T1 = """从该T1衰减图<image>中提取以下参数。

以JSON格式报告：
{"T1_us": float | null, "decay_visible": true | false}"""

PROMPT_T1_FLUCTUATIONS = """从该T1波动测量<image>中提取以下参数。

以JSON格式报告：
{"classification": "stable" | "telegraphic" | "random_walk", "mean_t1_us": float}"""

PROMPT_TWEEZER_ARRAY = """检查该光镊阵列相机图像<image>。

提取以下属性。

以JSON格式报告：
{"grid_regularity": "regular" | "irregular", "spot_uniformity": "uniform" | "non-uniform", "aberration_corrected": true | false}"""


# ========== Prompt 字典映射 ==========

EXTRACT_PARAMS_PROMPTS_ZH = {
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


def get_extract_params_prompt_zh(experiment_family: str) -> str:
    """获取提取参数的中文专属 prompt"""
    return EXTRACT_PARAMS_PROMPTS_ZH.get(experiment_family, EXTRACT_PARAMS_PROMPTS_ZH["rabi"])


__all__ = [
    "EXTRACT_PARAMS_PROMPTS_ZH",
    "get_extract_params_prompt_zh",
]