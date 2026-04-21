# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/21
########################################################################

"""
实验背景配置模块 (中文版)

定义每种实验家族的背景描述，用于 LLM 理解实验上下文
与 QCalEval 数据集保持一致
"""

# ========== Prompt 字符串 ==========

COUPLER_FLUX = """这是可调耦合器谱：我们绘制耦合器频率响应与施加的磁通偏置的关系。成功的结果显示清晰的耦合器离散曲线和良好的拟合。"""

CZ_BENCHMARKING = """这是 CZ（控制-Z）门基准测试，针对中性原子对。它测量原子保持概率和循环极化作为电路深度（ CZ 门数量）的函数。成功的结果显示保持度和极化度都接近1并逐渐衰减，拟合与数据很好地匹配。"""

DRAG = """这是 DRAG 校准：我们扫描 1/alpha 以找到最小化泄漏的最优值。成功的结果是拟合曲线的零交叉在扫描窗口中清晰可见。"""

GMM = """这是单次读出辨别实验：I-Q 散点图显示用高斯混合模型拟合的 |0⟩ 和 |1⟩ 态的测量结果。成功的结果是两个分离良好的聚类。"""

MICROWAVE_RAMSEY = """这是使用微波脉冲的基态时钟量子比特的 Ramsey 实验。成功的结果显示正弦振荡，对比度接近1，数据被曲线很好地拟合。"""

MOT_LOADING = """这是 MOT（磁光阱）装载图像：相机捕获被困原子的荧光。成功的结果显示视场中定义明确、紧凑的原子云。"""

PINCHOFF = """这是电子-氦夹断测量：作为门电压函数的 一维电流轨迹。测量确定器件是否夹断——从导通（高电流）转变为非导通（零电流）状态。关键特征是饱和区（稳定高电流）、转变区（电流下降）和截止区（电流为零）。成功的结果显示清晰、完整的转变，具有可识别的饱和、转变中点和截止索引。"""

PINGPONG = """这是 PingPong 幅度校准：重复的 pi 脉冲对被施加，量子比特 population 相对于门计数进行测量。成功的结果显示可以线性拟合的误差累积。"""

QUBIT_FLUX_SPECTROSCOPY = """这是磁通依赖的量子比特谱：量子比特跃迁频率与施加的磁通偏置的二维图。成功的结果显示清晰的离散曲线（弧或抛物线）并叠加有良好的拟合。"""

QUBIT_SPECTROSCOPY = """这是量子比特谱实验：我们扫描驱动频率以找到量子比特跃迁。成功的结果是具有良好洛伦兹拟合的单个清晰谱峰。"""

QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """这是二维量子比特谱实验：我们同时扫描驱动功率和频率来绘制量子比特跃迁图。成功的结果显示清晰的跃迁线（f01，可选地还有 f02/2）以及明显的功率依赖性。"""

RABI = """这是 Rabi 实验：我们扫描脉冲幅度以找到量子比特 population 反转的 pi-pulse 幅度。成功的结果显示清晰的正弦振荡，拟合紧密追踪数据。"""

RABI_HW = """这是 Rabi 实验：我们扫描脉冲幅度以找到量子比特 population 反转的 pi-pulse 幅度。成功的结果显示清晰的正弦振荡，拟合紧密追踪数据。"""

RAMSEY_CHARGE_TOMOGRAPHY = """这是 Ramsey 电荷层析扫描：随时间重复的 Ramsey 测量形成二维图，揭示电荷跳跃事件为条纹模式中的水平不连续。干净的结果显示连续、未受干扰的条纹。"""

RAMSEY_FREQ_CAL = """这是 Ramsey 频率校准实验：两个 π/2 脉冲被可变延迟分隔，测量频率失谐。成功的结果显示失谐频率处的清晰振荡，拟合准确提取频率偏移。"""

RAMSEY_T2STAR = """这是 Ramsey T2* 去相干实验：两个 π/2 脉冲被可变延迟分隔，测量去相干时间 T2*。成功的结果显示衰减振荡，拟合准确提取 T2*。"""

RES_SPEC = """这是谐振器谱实验：我们扫描探针频率以找到谐振器共振。成功的结果是具有清晰共振特征（凹陷或峰）。"""

RYDBERG_RAMSEY = """这是基态到 Rydberg 跃迁的 Ramsey 实验：两个 π/2 脉冲被可变延迟分隔，测量相干时间（T2）和失谐频率。数据点在选定的时间窗口中聚簇收集，而不是在完整的延迟范围内均匀分布。成功的结果显示单一衰减正弦模型在所有时间窗口中一致拟合，数据点沿着曲线，低归约卡方（RChi2）。"""

RYDBERG_SPECTROSCOPY = """这是 Rydberg 跃迁谱：光学失谐跨多个原子位点扫描以定位跃迁频率并测量 Rabi 频率。成功的结果显示清晰的谱特征，良好的拟合（低卡方）和跨位点的高对比度。"""

T1 = """这是 T1 弛豫实验：将量子比特激发到 |1⟩ 后，我们测量 population 相对于延迟时间。成功的结果显示从高 population 到低 population 的清晰指数衰减和良好的拟合。"""

T1_FLUCTUATIONS = """这是 T1 稳定性测量：T1 弛豫时间在重复测量中追踪。成功的结果显示稳定的 T1 值，最小漂移或跳跃。"""

TWEEZER_ARRAY = """这是用于在规则网格中捕获中性原子的光镊阵列的相机图像。成功的图像显示清晰、均匀、良好分离的光点，表明像差校正正确。"""


# ========== 配置字典 ==========

EXPERIMENT_BACKGROUNDS_ZH = {
    "coupler_flux": COUPLER_FLUX,
    "cz_benchmarking": CZ_BENCHMARKING,
    "drag": DRAG,
    "gmm": GMM,
    "microwave_ramsey": MICROWAVE_RAMSEY,
    "mot_loading": MOT_LOADING,
    "pinchoff": PINCHOFF,
    "pingpong": PINGPONG,
    "qubit_flux_spectroscopy": QUBIT_FLUX_SPECTROSCOPY,
    "qubit_spectroscopy": QUBIT_SPECTROSCOPY,
    "qubit_spectroscopy_power_frequency": QUBIT_SPECTROSCOPY_POWER_FREQUENCY,
    "rabi": RABI,
    "rabi_hw": RABI_HW,
    "ramsey_charge_tomography": RAMSEY_CHARGE_TOMOGRAPHY,
    "ramsey_freq_cal": RAMSEY_FREQ_CAL,
    "ramsey_t2star": RAMSEY_T2STAR,
    "res_spec": RES_SPEC,
    "rydberg_ramsey": RYDBERG_RAMSEY,
    "rydberg_spectroscopy": RYDBERG_SPECTROSCOPY,
    "t1": T1,
    "t1_fluctuations": T1_FLUCTUATIONS,
    "tweezer_array": TWEEZER_ARRAY,
}

# 默认背景（用于未知实验类型）
DEFAULT_BACKGROUND_ZH = """这是一个量子物理实验。请分析图表并提供您的评估。"""


def get_experiment_background_zh(experiment_family: str) -> str:
    """获取指定实验家族的中文背景描述

    Args:
        experiment_family: 实验家族名称（如 'rabi', 't1', 'drag' 等）

    Returns:
        实验背景描述字符串
    """
    return EXPERIMENT_BACKGROUNDS_ZH.get(experiment_family, DEFAULT_BACKGROUND_ZH)


__all__ = [
    "EXPERIMENT_BACKGROUNDS_ZH",
    "get_experiment_background_zh",
    "DEFAULT_BACKGROUND_ZH",
]