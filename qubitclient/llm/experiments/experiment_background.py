# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
实验背景配置模块

定义每种实验家族的背景描述，用于 LLM 理解实验上下文
"""

# ========== Prompt 字符串 ==========

COUPLER_FLUX = """This is tunable coupler spectroscopy: we map the coupler's frequency response vs applied flux bias. A successful result shows a clear coupler dispersion curve with a good fit."""

CZ_BENCHMARKING = """This is CZ gate benchmarking: measures atom retention probability and cycle polarization vs circuit depth. A successful result shows retention and polarization close to 1 with gradual decay."""

DRAG = """This is a DRAG calibration: we sweep 1/alpha to find the optimal value that minimizes leakage. A successful result has the zero-crossing of fitted curves clearly observable in the sweep window."""

GMM = """This is a single-shot readout discrimination experiment: the I-Q scatter plot shows measurement results for |0⟩ and |1⟩ states fitted with a Gaussian Mixture Model. A successful result has two well-separated clusters."""

MICROWAVE_RAMSEY = """This is a microwave Ramsey experiment: sinusoidal oscillations with contrast close to 1 and good fit."""

MOT_LOADING = """This is a MOT loading image: shows trapped atoms in a magneto-optical trap. A successful result shows a well-defined, compact atomic cloud."""

PINCHOFF = """This is a pinch-off measurement: current trace vs gate voltage to determine device pinch-off."""

PINGPONG = """This is a PingPong amplitude calibration: repeated pi-pulse pairs are applied and qubit population is measured vs gate count. A successful result shows error accumulation that can be fitted linearly."""

QUBIT_FLUX_SPECTROSCOPY = """This is flux-dependent qubit spectroscopy: 2D map of qubit frequency vs flux. A successful result shows clear dispersion curve with good fit."""

QUBIT_SPECTROSCOPY = """This is qubit spectroscopy: sweep drive frequency to find qubit transition. A successful result has a single clear peak with good Lorentzian fit."""

QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """This is 2D qubit spectroscopy: sweep power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, optionally f02/2)."""

RABI = """This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude where the qubit population inverts. A successful result shows clear sinusoidal oscillations with a fit that tracks the data closely."""

RABI_HW = """This is a Rabi experiment with hardware characterization: clear oscillations with fit."""

RAMSEY_CHARGE_TOMOGRAPHY = """This is Ramsey charge tomography: 2D map over time revealing charge jumps. Clean result shows continuous fringes."""

RAMSEY_FREQ_CAL = """This is Ramsey frequency calibration: oscillations at detuning frequency with accurate fit."""

RAMSEY_T2STAR = """This is Ramsey T2* dephasing: decaying oscillations with fit that extracts T2*."""

RES_SPEC = """This is resonator spectroscopy: sweep probe frequency to find resonance. A successful result has clear resonance feature."""

RYDBERG_RAMSEY = """This is Rydberg Ramsey: oscillations on ground-to-Rydberg transition with T2 and detuning."""

RYDBERG_SPECTROSCOPY = """This is Rydberg spectroscopy: sweep detuning across multiple sites. Clear spectral features with good fits."""

T1 = """This is T1 relaxation: measure population vs delay after excitation to |1⟩. A successful result shows clear exponential decay with good fit."""

T1_FLUCTUATIONS = """This is T1 stability measurement: T1 tracked over repeated measurements. Stable values indicate good qubit stability."""

TWEEZER_ARRAY = """This is optical tweezer array image: trapped atoms in regular grid. Sharp, uniform spots indicate proper aberration correction."""


# ========== 配置字典 ==========

EXPERIMENT_BACKGROUNDS = {
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
DEFAULT_BACKGROUND = """This is a quantum physics experiment. Analyze the plot and provide your assessment."""


def get_experiment_background(experiment_family: str) -> str:
    """获取指定实验家族的背景描述

    Args:
        experiment_family: 实验家族名称（如 'rabi', 't1', 'drag' 等）

    Returns:
        实验背景描述字符串
    """
    return EXPERIMENT_BACKGROUNDS.get(experiment_family, DEFAULT_BACKGROUND)


__all__ = [
    "EXPERIMENT_BACKGROUNDS",
    "get_experiment_background",
    "DEFAULT_BACKGROUND",
]