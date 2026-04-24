# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/21
########################################################################

"""
Q3: 科学推理任务 (中文版)

分析实验结果的物理含义并给出下一步建议
"""

# ========== 独立 Prompt 字符串定义 ==========

PROMPT_COUPLER_FLUX = """这个结果说明了什么？

请解释：
- 离散曲线形状揭示了耦合器可调范围和耦合强度方面的信息
- 磁通范围是否捕获了足够的离散以进行可靠的参数提取
- 下一步是什么（例如，设置耦合器偏置点，校准双量子比特门交互）

请提供您的评估。"""

PROMPT_CZ_BENCHMARKING = """这个结果<image>说明了什么？

请解释：
- 保持衰减率和极化衰减率显示了门保真度、每次门的原子损失和整体门质量方面的信息
- 电路深度范围是否跨越了足够的衰减以从保持和极化中提取有意义的保真度指标
- 接下来是什么调整（例如，重新校准CZ门，调整电路深度范围，或调查原子损失机制）

请提供您的评估。"""

PROMPT_DRAG = """这个结果<image>说明了什么？

请解释：
- 零交叉位置和斜率表明了DRAG系数最优性和泄漏抑制方面的信息
- 扫描范围是否捕获了足够清晰的交叉以进行可靠的提取
- 下一步校准步骤是什么（例如，在交叉点附近缩小扫描范围，或进行门基准测试）

请提供您的评估。"""

PROMPT_GMM = """这个结果<image>说明了什么？

请解释：
- 聚类分离度、形状和重叠表明了读出保真度和信噪比方面的信息
- 区分度是否足以进行可靠的单次状态分配
- 下一步调整是什么（例如，优化读出功率、频率或积分时间）

请提供您的评估。"""

PROMPT_MICROWAVE_RAMSEY = """这个结果<image>说明了什么？

请解释：
- 对比度、保持水平和拟合质量表明了量子比特相干性和微波驱动校准方面的信息
- 对比度和保持度是否足以进行可靠的状态区分和参数提取
- 下一步调整是什么（例如，将微波频率调得更接近共振，调查系统保持问题，或进行电流校准）

请提供您的评估。"""

PROMPT_MOT_LOADING = """这个MOT加载结果<image>表明了关于阱性能的什么信息？

请解释：
- 云形态（大小、对称性、亮度）表明了阱对准和原子数方面的信息
- 图像质量和信噪比是否足以进行可靠的云表征
- 下一步阱参数调整是什么（例如，光束对准、磁场梯度调谐或激光失谐）

请提供您的评估。"""

PROMPT_PINCHOFF = """这个结果<image>说明了什么？

请解释：
- 转变形状（陡峭度、完整性、剩余电流）表明了沟道耗尽和器件质量方面的信息
- 门电压范围是否捕获了完整的夹断转变以进行可靠的阈值提取
- 下一步调整是什么（例如，扩展电压范围，检查器件极性，调查泄漏路径）

请提供您的评估。"""

PROMPT_PINGPONG = """这个结果<image>说明了什么？

请解释：
- 斜率和振荡模式表明了pi脉冲幅度误差的大小和方向方面的信息
- 门计数范围是否足以区分校准质量和噪声
- 基于观察到的误差累积趋势，接下来脉冲幅度调整是什么

请提供您的评估。"""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """这个结果说明了什么？

请解释：
- 离散曲线形状揭示了量子比特sweet spot位置、Ej/Ec比和磁通可调性方面的信息
- 磁通和频率范围是否捕获了足够的离散以进行可靠的参数提取
- 下一步是什么（例如，偏置到sweet spot，扩展磁通范围，优化拟合模型）

请提供您的评估。"""

PROMPT_QUBIT_SPECTROSCOPY = """这个结果说明了什么？

请解释：
- 峰位、线宽和形状表明了量子比特频率和相干性方面的信息
- 频率跨度和分辨率是否足以进行明确的跃迁识别
- 下一步是什么（例如，在峰附近缩小扫描范围，进行Rabi或Ramsey校准）

请提供您的评估。"""

PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """这是一个二维量子比特谱实验，测试标准的transmon量子比特（负非谐性，所以f02/2出现在比f01更低的频率）：我们同时扫描驱动功率和频率来绘制量子比特跃迁图。成功的结果会显示清晰的跃迁线（f01，可选地还有f02/2）以及明显的功率依赖性。

这些结果<image>、<image>和<image>说明了什么？

请解释：
- 跃迁线结构揭示了量子比特非谐性和驱动功率耦合方面的信息
- 频率和功率范围是否足以识别所有相关跃迁
- 接下来是什么参数调整（功率范围、频率窗口）或下一步（单音谱、Rabi）

请提供您的评估。"""

PROMPT_RABI = """这个结果<image>说明了什么？

请解释：
- 振荡模式表明了驱动耦合强度和pi脉冲幅度方面的信息
- 幅度范围和采样是否足以进行可靠的Rabi速率提取
- 下一步校准步骤是什么（例如，调整驱动幅度，扩展扫描范围，或进行DRAG校准）

请提供您的评估。"""

PROMPT_RABI_HW = """这个结果说明了什么？

请解释：
- 振荡模式表明了驱动耦合强度和pi脉冲幅度方面的信息
- 幅度范围和采样是否足以进行可靠的Rabi速率提取
- 下一步校准步骤是什么（例如，调整驱动幅度，扩展扫描范围，或进行DRAG校准）

请提供您的评估。"""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """这个Ramsey电荷层析结果<image>对量子比特操作意味着什么？

请解释：
- 条纹连续性和中断模式表明了电荷噪声环境方面的信息
- 扫描持续时间和分辨率是否足以表征电荷跳跃频率和严重程度
- 下一步器件或环境调整是什么（例如，改进滤波、重新定位量子比特工作点或扩展监测）

请提供您的评估。"""

PROMPT_RAMSEY_FREQ_CAL = """这些结果<image>和<image>说明了什么？

请解释：
- 振荡模式表明了量子比特失谐和相干性方面的信息
- 测量是否足以进行可靠的参数提取
- 接下来是什么参数调整或下一步校准步骤

请提供您的评估。"""

PROMPT_RAMSEY_T2STAR = """这些结果<image>和<image>说明了什么？

请解释：
- 振荡模式表明了量子比特失谐和相干性方面的信息
- 测量是否足以进行可靠的参数提取
- 接下来是什么参数调整或下一步校准步骤

请提供您的评估。"""

PROMPT_RES_SPEC = """这个结果<image>说明了什么？

请解释：
- 共振线形（深度、宽度、对称性）表明了内部和耦合品质因子方面的信息
- 频率跨度和分辨率是否足以进行可靠的共振频率提取
- 下一步是什么（例如，调整频率窗口，进行量子比特谱）

请提供您的评估。"""

PROMPT_RYDBERG_RAMSEY = """这个结果<image>说明了什么？

请解释：
- 振荡频率、振幅衰减率和拟合质量（RChi2）表明了量子比特相干性和频率噪声方面的信息
- 数据簇在所有时间窗口中是否被单一拟合一致地描述，或者拟合是否与后面的簇发散
- 下一步校准步骤是什么（例如，调整Rydberg激光参数，添加更多时间窗口，或进行门序列）

请提供您的评估。"""

PROMPT_RYDBERG_SPECTROSCOPY = """这个结果<image>说明了什么？

请解释：
- 谱线形状、拟合质量（卡方）和对比度表明了Rydberg跃迁耦合和激光稳定性方面的信息
- 谱分辨率和信噪比是否足以在所有位点进行可靠的频率和Rabi频率提取
- 下一步校准步骤是什么（例如，调整激光功率或对准，调查噪声位点，或进行Rydberg门校准）

请提供您的评估。"""

PROMPT_T1 = """这个结果<image>说明了什么？

请解释：
- 衰减率和剩余 population 表明了量子比特弛豫时间和热 population方面的信息
- 时间窗口和采样是否捕获了足够的衰减以进行可靠的T1提取
- 下一步是什么（例如，扩展延迟范围，改进热化，或进行T2测量）

请提供您的评估。"""

PROMPT_T1_FLUCTUATIONS = """这个结果<image>说明了什么？

请解释：
- T1时间序列模式（稳定性、切换、漂移）表明了主要退相干机制方面的信息
- 监测持续时间和采样率是否足以表征波动类型
- 接下来是什么缓解策略（例如，TLS避免、热稳定或频率调谐）

请提供您的评估。"""

PROMPT_TWEEZER_ARRAY = """这个结果<image>说明了什么？

请解释：
- 光点均匀性、锐度和网格规则性表明了光学系统对准和像差校正质量方面的信息
- 阵列填充因子和光点质量是否足以在所有位点进行可靠的原子捕获
- 下一步调整是什么（例如，重新运行像差校正，调整阱功率，或进行原子装载）

请提供您的评估。"""

# ========== Not in QCalEval ==========
PROMPT_S21 = """这个结果<image>说明了什么？

请解释：
- S21透射线形（凹陷深度、宽度、对称性）表明了内部和耦合品质因子方面的信息，以及量子比特-谐振器耦合 regime（欠耦合/过耦合/临界）
- 频率跨度和分辨率是否足以进行可靠的共振频率和色散位移提取
- 下一步是什么（例如，进行量子比特谱，调整耦合强度，或进行色散读出校准）

请提供您的评估。"""

# ========== Prompt 字典映射 ==========

SCIENTIFIC_REASONING_PROMPTS_ZH = {
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


def get_scientific_reasoning_prompt_zh(experiment_family: str) -> str:
    """获取科学推理的中文专属 prompt"""
    return SCIENTIFIC_REASONING_PROMPTS_ZH.get(experiment_family, SCIENTIFIC_REASONING_PROMPTS_ZH["rabi"])


__all__ = [
    "SCIENTIFIC_REASONING_PROMPTS_ZH",
    "get_scientific_reasoning_prompt_zh",
]