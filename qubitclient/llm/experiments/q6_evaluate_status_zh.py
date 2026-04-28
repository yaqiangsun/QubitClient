# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/21
########################################################################

"""
Q6: 评估状态任务 (中文版)

判断实验成功/失败状态并给出建议
"""

# ========== 独立 Prompt 字符串定义 ==========

PROMPT_COUPLER_FLUX = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 清晰的耦合器离散曲线，拟合追踪数据
- FIT_POOR: 离散可见但拟合偏离

当状态不是 SUCCESS 时，提供一个具体的建议（<min flux>, <max flux>）[磁通量子]。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: (<min flux>, <max flux>) [flux quanta]（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_CZ_BENCHMARKING = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 保持度和极化度都接近1，逐渐衰减，拟合良好
- NO_GATE: 保持度不切实际地高（平坦~1）且快速去极化——门可能实际上没有发生
- MISCALIBRATED: 快速去极化和/或保持度差——门未校准或电路太深无法准确表征

当状态不是 SUCCESS 时，提供一个具体的建议操作：<关于门校准或电路深度调整的具体建议>。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: Suggested action: <关于门校准或电路深度调整的具体建议>（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_DRAG = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 在扫描窗口中清晰可见零交叉
- NO_SIGNAL: 平坦或随机，无交叉模式
- OPTIMAL_NOT_CENTERED: 交叉存在但位于第一个/最后一个四分位或范围之外

当状态不是 SUCCESS 时，提供一个具体的建议（<min 1/alpha>, <max 1/alpha>）。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: (<min 1/alpha>, <max 1/alpha>)（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_GMM = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 两个明显分离的聚类
- NO_SIGNAL: 无法区分的聚类
- NO_EXCITATION: 两个分布之间没有显著差异——量子比特状态没有被驱动改变
- HIGH_POWER: 聚类变形、伸长或碎片化
- NO_RES_RESPONSE: 所有点塌缩到单个区域

当状态不是 SUCCESS 时，提供一个具体的建议操作：<关于读出功率、频率或量子比特驱动的具体建议>。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: Suggested action: <关于读出功率、频率或量子比特驱动的具体建议>（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_MICROWAVE_RAMSEY = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 高对比度（~1），良好的拟合，数据被曲线很好地描述
- LOW_CONTRAST: 低对比度振荡和/或整体保持度低——可能是系统问题
- DETUNED: 保持度可以很高但最小值显著高于0——微波失谐在Rabi频率量级

当状态不是 SUCCESS 时，提供一个具体的建议操作：<关于微波频率、功率或系统检查的具体建议>。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: Suggested action: <关于微波频率、功率或系统检查的具体建议>（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_MOT_LOADING = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 定义明确、对称的Gaussian形状的云，高信噪比
- NO_SIGNAL: 整个视场均匀噪声，没有来自捕获原子的荧光——基本阱设置问题
- ASYMMETRIC: 云可见但有不对称尾部/彗星结构——辐射压力不平衡或磁场梯度未对准

当状态不是 SUCCESS 时，提供一个具体的建议操作：<关于阱对准或激光参数调整的具体建议>。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: Suggested action: <关于阱对准或激光参数调整的具体建议>（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_PINCHOFF = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 从导通到夹断的清晰转变（电流降至近零）
- INVERTED: 电流随门电压增加而不是减少——极性或配置错误
- INCOMPLETE: 电流开始下降但扫描范围太窄，无法捕获到零的完整转变
- NO_TRANSITION: 无法识别的转变——电流保持平坦或噪声，无明确的夹断
- NEGATIVE_OFFSET: 电流过零并在负值饱和——仪器偏移或背景减法错误
- POSITIVE_OFFSET: 电流减少但在有限正值饱和而不是达到零——耗尽不完全或寄生泄漏

当状态不是 SUCCESS 时，提供一个具体的建议操作：<关于门电压范围或器件配置的具体建议>。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: Suggested action: <关于门电压范围或器件配置的具体建议>（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_PINGPONG = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 信号随门计数增加而稳定
- NO_EXCITATION: 信号在基态附近平坦
- MODERATE_ERROR: 可见漂移或振荡，pi脉冲近似正确
- LARGE_ERROR: 强振荡或快速发散

当状态不是 SUCCESS 时，提供一个具体的建议操作：<关于pi脉冲幅度调整的具体建议>。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: Suggested action: <关于pi脉冲幅度调整的具体建议>（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 清晰的离散曲线，拟合追踪数据
- FIT_POOR: 离散可见但拟合偏离
- FIT_FAILED: 拟合完全未能收敛
- RANGE_TOO_NARROW: 离散仅部分可见
- NO_SIGNAL: 2D图中无谱特征
- NOT_TUNABLE: 量子比特频率在磁通范围内平坦或几乎平坦；无显著离散

当状态不是 SUCCESS 时，提供一个具体的建议（<min flux>, <max flux>）[磁通量子] 或（<min freq>, <max freq>）[GHz]。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: (<min flux>, <max flux>) [flux quanta] 或 (<min freq>, <max freq>) [GHz]（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_QUBIT_SPECTROSCOPY = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 具有良好拟合的单个清晰谱峰
- NO_SIGNAL: 看不到峰
- MULTIPLE_PEAKS: 多条谱线，ID模糊

当状态不是 SUCCESS 时，提供一个具体的建议（<min frequency>, <max frequency>）[GHz]。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: (<min frequency>, <max frequency>) [GHz]（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

# Special case: prompt includes background (different version from experiment_background field)
PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """这是一个二维量子比特谱实验，测试标准的transmon量子比特（负非谐性，所以f02/2出现在比f01更低的频率）：我们同时扫描驱动功率和频率来绘制量子比特跃迁图。成功的结果会显示清晰的跃迁线（f01，可选地还有f02/2）以及明显的功率依赖性。

评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 清晰的跃迁线，具有完整的功率依赖性，可用于提取
- AMP_TOO_HIGH: 跃迁功率展宽/饱和，特征模糊且频率偏移
- NO_SIGNAL: 无特征——完全错误的频率窗口

当状态不是 SUCCESS 时，提供一个具体的建议（<min power>, <max power>）[a.u.] 或（<min freq>, <max freq>）[GHz]。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: (<min power>, <max power>) [a.u.] 或 (<min freq>, <max freq>) [GHz]（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_RABI = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 清晰振荡，拟合追踪数据
- FIT_POOR: 振荡可见但拟合偏离
- RANGE_TOO_NARROW: 可见的完整周期少于一个
- NO_SIGNAL: 平坦或随机，无振荡结构
- DAMPED: 振幅在窗口内衰减>50%
- UNSAMPLED: 太多振荡周期；信号混叠或分辨率不足

当状态不是 SUCCESS 时，提供一个具体的建议（<min amplitude>, <max amplitude>）。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: (<min amplitude>, <max amplitude>)（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_RABI_HW = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 清晰振荡，拟合追踪数据
- FIT_POOR: 振荡可见但拟合偏离
- OFF_RESONANCE: 振荡可见但驱动频率不在共振——失真响应且拟合差
- RANGE_TOO_NARROW: 可见的完整周期少于一个

当状态不是 SUCCESS 时，提供一个具体的建议（<min amplitude>, <max amplitude>）。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: (<min amplitude>, <max amplitude>)（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """分类此扫描<image>中观察到的电荷跳跃活动。

分类标准
- NO_EVENT: 连续未受干扰的条纹，未检测到电荷跳跃
- EVENT: 一个或多个离散电荷跳跃事件，表现为条纹模式中的水平不连续
- NO_COHERENCE: 无法辨别的条纹——完全失去相干性，无法评估电荷跳跃活动

提供您的分类并简要描述观察到的电荷跳跃活动。

响应必须遵循以下精确格式：

Classification: <列出的类别之一>
Notes: <1-3 句描述电荷跳跃活动>"""

PROMPT_RAMSEY_FREQ_CAL = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 清晰振荡带衰减包络，拟合追踪数据
- NO_DETUNING: 信号平坦——无振荡
- BEATING: 来自多个频率的振幅调制
- TOO_MANY_OSC: 失谐对于时间窗口太大
- TOO_FEW_OSC: 失谐对于时间窗口太小
- WINDOW_TOO_SHORT: 衰减未完全捕获
- SAMPLING_TOO_COARSE: 振荡欠采样/混叠

当状态不是 SUCCESS 时，提供一个具体的建议（<min delay>, <max delay>）[单位]。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: (<min delay>, <max delay>) [unit]（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_RAMSEY_T2STAR = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 清晰振荡带衰减包络，拟合追踪数据
- NO_DETUNING: 信号平坦——无振荡
- BEATING: 来自多个频率的振幅调制
- TOO_MANY_OSC: 失谐对于时间窗口太大
- TOO_FEW_OSC: 失谐对于时间窗口太小
- WINDOW_TOO_SHORT: 衰减未完全捕获
- SAMPLING_TOO_COARSE: 振荡欠采样/混叠

当状态不是 SUCCESS 时，提供一个具体的建议（<min delay>, <max delay>）[单位]。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: (<min delay>, <max delay>) [unit]（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_RES_SPEC = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 可见的清晰共振特征
- NO_SIGNAL: 响应平坦，频率范围内无共振

当状态不是 SUCCESS 时，提供一个具体的建议（<min frequency>, <max frequency>）[GHz]。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: (<min frequency>, <max frequency>) [GHz]（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_RYDBERG_RAMSEY = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 单一衰减正弦拟合在所有时间窗口中一致，低RChi2
- UNDERSAMPLED: 数据簇未跨越足够的振荡周期；拟合无法同时协调所有时间窗口

当状态不是 SUCCESS 时，提供一个具体的建议操作：<关于采样密度或测量窗口的具体建议>。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: Suggested action: <关于采样密度或测量窗口的具体建议>（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_RYDBERG_SPECTROSCOPY = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 良好的拟合（低卡方），清晰的谱特征，高对比度跨位点
- LOW_CONTRAST: 对比度降低，共振噪声，许多位点拟合失败

当状态不是 SUCCESS 时，提供一个具体的建议操作：<关于激光功率、频率或对准的具体建议>。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: Suggested action: <关于激光功率、频率或对准的具体建议>（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_T1 = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 清晰的指数衰减，拟合追踪数据
- NO_SIGNAL: Population 平坦——量子比特从未被激发或瞬时衰减
- WINDOW_TOO_SHORT: 信号未达到基线
- SAMPLING_TOO_COARSE: 时间步长太大，无法解析衰减

当状态不是 SUCCESS 时，提供一个具体的建议（<min delay>, <max delay>）[us]。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: (<min delay>, <max delay>) [us]（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_T1_FLUCTUATIONS = """评估图像<image>并确定实验状态。

决策标准
- STABLE: T1值紧密围绕单个基线聚集，变化由测量散点主导
- TELEGRAPHIC: T1在两个或多个离散亚稳态之间 abrupt 切换——表示耦合到双能级系统缺陷
- RANDOM_WALK: T1在宽范围内显示连续相关漂移——表示缓慢的环境变化（温度、磁场、电荷噪声）

提供您分类的简要解释。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: Suggested action: <关于T1稳定或进一步表征的具体建议>（如果是 STABLE 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""

PROMPT_TWEEZER_ARRAY = """评估图像<image>并确定实验状态。

决策标准
- CORRECTED: 锐利、均匀光点的规则网格——像差已校正
- ABERRATED: 光点模糊、不均匀或缺失——像差未校正

当状态不是 SUCCESS 时，提供一个具体的建议操作：<具体建议>。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: Suggested action: <具体建议>（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""


# ========== Not in QCalEval ==========
PROMPT_S21 = """评估图像<image>并确定实验状态。

决策标准
- SUCCESS: 在腔频位置有清晰的S21幅度向下尖谷，相位在共振附近有显著跳变，信噪比良好
- NO_SIGNAL: 响应平坦，频率范围内无共振特征
- LOW_CONTRAST: 共振可见但非常浅，信噪比差
- PHASE_ANOMALY: 相位行为异常，共振附近无明显相位跳变

当状态不是 SUCCESS 时，提供一个具体的建议（<min frequency>, <max frequency>）[GHz]。

响应必须遵循以下精确格式：

Status: <列出的状态之一>
Suggested range: (<min frequency>, <max frequency>) [GHz]（如果是 SUCCESS 则为 "N/A"）
Notes: <1-3 句解释您的推理>"""


# ========== Prompt 字典映射 ==========

EVALUATE_STATUS_PROMPTS_ZH = {
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


def get_evaluate_status_prompt_zh(experiment_family: str) -> str:
    """获取评估状态的中文专属 prompt"""
    return EVALUATE_STATUS_PROMPTS_ZH.get(experiment_family, EVALUATE_STATUS_PROMPTS_ZH["rabi"])


__all__ = [
    "EVALUATE_STATUS_PROMPTS_ZH",
    "get_evaluate_status_prompt_zh",
]