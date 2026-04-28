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
与 QCalEval 数据集保持一致
"""

# ========== Prompt 字符串 ==========

COUPLER_FLUX = """This is tunable coupler spectroscopy: we map the coupler's frequency response vs applied flux bias. A successful result shows a clear coupler dispersion curve with a good fit."""

CZ_BENCHMARKING = """This is CZ (controlled-Z) gate benchmarking on pairs of neutral atoms. It measures atom retention probability and cycle polarization as a function of circuit depth (number of CZ gates). A successful result shows both retention and polarization close to 1 with gradual decay, and fits that match the data well."""

DRAG = """This is a DRAG calibration: we sweep 1/alpha to find the optimal value that minimizes leakage. A successful result has the zero-crossing of fitted curves clearly observable in the sweep window."""

GMM = """This is a single-shot readout discrimination experiment: the I-Q scatter plot shows measurement results for |0⟩ and |1⟩ states fitted with a Gaussian Mixture Model. A successful result has two well-separated clusters."""

MICROWAVE_RAMSEY = """This is a Ramsey experiment on the ground-state clock qubit using microwave pulses. A successful result shows sinusoidal oscillations with contrast close to 1 and data well-fit by the curve."""

MOT_LOADING = """This is a MOT (magneto-optical trap) loading image: a camera captures the fluorescence of trapped atoms. A successful result shows a well-defined, compact atomic cloud in the view."""

PINCHOFF = """This is an electron-on-helium pinch-off measurement: a 1D current trace is measured as a function of gate voltage. The measurement determines whether the device has pinched off — transitioning from a conducting (high current) to non-conducting (zero current) state. Key features are the saturation region (stable high current), the transition region (current drops), and the cut-off region (current reaches zero). A successful result shows a clear, complete transition with identifiable saturation, transition midpoint, and cut-off indices."""

PINGPONG = """This is a PingPong amplitude calibration: repeated pi-pulse pairs are applied and qubit population is measured vs gate count. A successful result shows error accumulation that can be fitted linearly."""

QUBIT_FLUX_SPECTROSCOPY = """This is flux-dependent qubit spectroscopy: a 2D map of qubit transition frequency vs applied flux bias. A successful result shows a clear dispersion curve (arc or parabola) with a good fit overlaid."""

QUBIT_SPECTROSCOPY = """This is a qubit spectroscopy experiment: we sweep drive frequency to find the qubit transition. A successful result has a single clear spectral peak with a good Lorentzian fit."""

QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """This is a 2D qubit spectroscopy experiment: we sweep both drive power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, and optionally f02/2) with visible power dependence."""

RABI = """This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude where the qubit population inverts. A successful result shows clear sinusoidal oscillations with a fit that tracks the data closely."""

RABI_HW = """This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude where the qubit population inverts. A successful result shows clear sinusoidal oscillations with a fit that tracks the data closely."""

RAMSEY_CHARGE_TOMOGRAPHY = """This is a Ramsey charge tomography scan: repeated Ramsey measurements over time form a 2D map revealing charge jump events as horizontal discontinuities in the fringe pattern. A clean result shows continuous, undisturbed fringes."""

RAMSEY_FREQ_CAL = """This is a Ramsey frequency calibration experiment: two π/2 pulses separated by a variable delay measure frequency detuning. A successful result shows clear oscillations at the detuning frequency with a fit that accurately extracts the frequency offset."""

RAMSEY_T2STAR = """This is a Ramsey T2* dephasing experiment: two π/2 pulses separated by a variable delay measure the dephasing time T2*. A successful result shows decaying oscillations with a fit that accurately extracts T2*."""

RES_SPEC = """This is a resonator spectroscopy experiment: we sweep probe frequency to find the resonator resonance. A successful result has a clear resonance feature (dip or peak)."""

RYDBERG_RAMSEY = """This is a Ramsey experiment on the ground-to-Rydberg transition: two π/2 pulses separated by variable delay measure the coherence time (T2) and detuning frequency. Data points are collected in clusters at selected time windows rather than uniformly across the full delay range. A successful result shows that a single decaying sinusoidal model fits consistently across all time windows, with data points following the curve and a low reduced chi-squared (RChi2)."""

RYDBERG_SPECTROSCOPY = """This is Rydberg transition spectroscopy: optical detuning is swept across multiple atomic sites to locate the transition frequency and measure the Rabi frequency. A successful result shows clear spectral features with good fits (low chi-squared) and high contrast across sites."""

T1 = """This is a T1 relaxation experiment: after exciting the qubit to |1⟩, we measure population vs delay time. A successful result shows a clear exponential decay from high to low population with a good fit."""

T1_FLUCTUATIONS = """This is a T1 stability measurement: T1 relaxation time is tracked over repeated measurements. A successful result shows stable T1 values with minimal drift or jumps."""

TWEEZER_ARRAY = """This is a camera image of an optical tweezer array used to trap neutral atoms in a regular grid. A successful image shows sharp, uniform, well-separated spots indicating proper aberration correction."""

# ========== Not in QCalEval ==========
S21 = """This is an S21 cavity frequency search experiment: we sweep probe frequency and measure the complex transmission coefficient S21 from input port to output port to characterize a superconducting resonator. The primary goal is to precisely determine the resonator's resonance frequency (f_r). A successful result shows a clear dip in S21 amplitude at the cavity frequency, accompanied by a sharp phase jump near resonance. The data should be well-fitted to extract f_r."""

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
    # ========== Not in QCalEval ==========
    "s21": S21,
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