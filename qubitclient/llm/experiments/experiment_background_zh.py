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

# ========== Not in QCalEval ==========
S21 = """这是 S21 腔频查找实验：我们扫描探针频率并测量从输入端口到输出端口的复数透射系数 S21，以表征超导谐振腔。主要目的是精确测定谐振腔的本征频率 (f_r)。成功的结果显示在腔频位置 S21 幅度有一个清晰的向下尖谷，相位在共振附近有显著的跳变。数据应能被很好地拟合以提取 f_r。"""

SPECTRUM_2D = """这是单比特谱实验与Z控制幅度扫描：我们同时扫描微波驱动频率和Z脉冲幅度（V_Z）以绘制量子比特频率响应。这是二维频谱，X轴显示驱动频率，Y轴显示Z脉冲幅度。主要目标是建立 Z 控制电压与量子比特频率之间的校准曲线 f_q = f(V_Z)。成功的结果显示清晰的光谱特征（共振峰或凹陷），这些特征随 Z 脉冲幅度移动，形成特征性的色散曲线。数据使得可以通过 Z 控制实现量子比特频率的精确调节。"""

OPTPIPULSE = """这是 Opt_pi 脉冲校准实验（重复Rabi）：我们扫描驱动幅度和脉冲重复次数（N）以精确校准π脉冲幅度。序列施加N个"双R门+延迟"循环，每个双R门等效于2θ旋转。当θ等于π/2时（即一次R门为π/2），总旋转为Nπ，激发态population随N奇偶性振荡（奇数N=高，偶数N=低）。成功的结果在二维图（幅度vs N）中显示清晰的棋盘格图案，表明正确的π脉冲校准。最优幅度使这种二进制振荡的对比度最大化。"""

RABICOS = """这是功率Rabi实验（RabiCOS）：我们扫描驱动脉冲幅度以观察Rabi振荡。两个相同的R门（每个旋转角度θ∝幅度）连续施加，总旋转为2θ。随着幅度增加，激发态population遵循 P_e = sin²(θ)。成功的结果显示清晰的正弦振荡，第一个峰对应π/2脉冲，第一个谷对应π脉冲。这用于校准量子门的驱动幅度。"""

RAMSEY = """这是Ramsey实验，用于精确校准量子比特频率：两个π/2脉冲被可变延迟分隔，期间量子比特自由演化。第二个脉冲的相位编码了失谐，产生干涉振荡。成功的结果显示在失谐频率处的余弦振荡，能够以kHz级精度提取精确的频率偏移。这通常在通过光谱法进行粗略频率校准之后进行。"""

S21VFLUX = """这是S21 vs Flux实验（腔频 vs 偏置磁通）：我们同时扫描探针频率和施加的磁通偏置电压，以绘制腔共振频率响应。这个二维图揭示了腔共振频率如何随DC偏置（Z控制）变化。成功的结果显示清晰的共振曲线随偏置移动，从而能够校准偏置依赖的腔频率和色散频移。用于优化读取频率和理解串扰。"""

POWERSHIFT = """这是功率偏移实验：我们同时扫描探针频率和读取功率，以表征腔的功率依赖频率偏移（克尔效应/非线性）。在低功率下，腔表现为线性；在高功率下，非线性效应导致频率漂移。成功的结果显示共振频率随功率增加而降低，从而能够提取克尔系数和高保真度读取的最佳工作功率。"""

SINGLESHOT = GMM
SPECTRUM = QUBIT_SPECTROSCOPY
T2 = RAMSEY_T2STAR
RB = """这是随机基准测试（RB）实验：我们对量子比特施加随机的Clifford门序列，并测量存活概率（返回初始状态的概率）随序列长度的变化。每个序列以恢复门结束，如果没有错误则完美撤销随机门。成功的结果显示存活概率随序列长度指数衰减，从中可以提取平均门错误率。这测量了Clifford门集的本征保真度，排除了SPAM错误。"""

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
    # ========== Not in QCalEval ==========
    "s21": S21,
    "spectrum_2d": SPECTRUM_2D,
    "optpipulse": OPTPIPULSE,
    "rabicos": RABICOS,
    "ramsey": RAMSEY,
    "s21vflux": S21VFLUX,
    "powershift": POWERSHIFT,
    "singleshot": SINGLESHOT,
    "spectrum": SPECTRUM,
    "t2": T2,
    "rb": RB,
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