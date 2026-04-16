# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
Q2: 分类实验结果任务

将实验结果分类为: Expected/Suboptimal/Anomalous/Apparatus issue
"""

# ========== 独立 Prompt 字符串定义 ==========

PROMPT_COUPLER_FLUX = """This is tunable coupler spectroscopy: we map the coupler's frequency response vs applied flux bias. A successful result shows a clear coupler dispersion curve with a good fit.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear avoided crossing with good fit, crossing within range
- Suboptimal parameters: Crossings visible but fit quality poor or crossing near edge
- Anomalous behavior: Multiple crossings, asymmetric pattern, unexpected behavior
- Apparatus issue: No clear crossing pattern, flat/noisy data

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_CZ_BENCHMARKING = """This is CZ (controlled-Z) gate benchmarking on pairs of neutral atoms. It measures atom retention probability and cycle polarization as a function of circuit depth. A successful result shows both retention and polarization close to 1 with gradual decay.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: High retention (>0.9) and polarization, clear decay with depth
- Suboptimal parameters: Moderate values, faster than expected decay
- Anomalous behavior: Unexpected oscillations, polarization loss, irregular decay
- Apparatus issue: No decay pattern, random data, measurement error

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_DRAG = """This is a DRAG calibration: we sweep 1/alpha to find the optimal value that minimizes leakage. A successful result has the zero-crossing of fitted curves clearly observable in the sweep window.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear zero-crossing within sweep window, good linear fits
- Suboptimal parameters: Crossing visible but near edge of range, or limited data
- Anomalous behavior: Wrong crossing direction, asymmetric slopes, unexpected pattern
- Apparatus issue: No clear crossing, flat/noisy data, no signal response

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_GMM = """This is a single-shot readout discrimination experiment: the I-Q scatter plot shows measurement results for |0⟩ and |1⟩ states fitted with a Gaussian Mixture Model. A successful result has two well-separated clusters.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Two well-separated clusters, clear discrimination
- Suboptimal parameters: Clusters touching or partially overlapping, moderate separation
- Anomalous behavior: Single blob, clusters in wrong positions, unexpected distribution
- Apparatus issue: No clusters visible, random scatter, measurement error

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_MICROWAVE_RAMSEY = """This is a Ramsey experiment on the ground-state clock qubit using microwave pulses. A successful result shows sinusoidal oscillations with contrast close to 1 and data well-fit by the curve.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations with high contrast, good fit
- Suboptimal parameters: Low contrast, fast decay, limited oscillations visible
- Anomalous behavior: Unexpected frequency, irregular pattern, drift
- Apparatus issue: No oscillations, flat/noisy data, random scatter

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_MOT_LOADING = """This is a MOT (magneto-optical trap) loading image: a camera captures the fluorescence of trapped atoms. A successful result shows a well-defined, compact atomic cloud in the view.

Based on what you observe in the image <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear, compact cloud with good brightness
- Suboptimal parameters: Cloud present but diffuse or offset
- Anomalous behavior: Multiple clouds, elongated shape, unexpected features
- Apparatus issue: No cloud visible, only background noise

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_PINCHOFF = """This is an electron-on-helium pinch-off measurement: a 1D current trace is measured as a function of gate voltage. The measurement determines whether the device has pinched off — transitioning from conducting to non-conducting state.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear pinch-off transition with identifiable regions
- Suboptimal parameters: Transition visible but noisy or incomplete
- Anomalous behavior: No clear transition, irregular behavior
- Apparatus issue: No measurable current, no transition, noise dominated

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_PINGPONG = """This is a PingPong amplitude calibration: repeated pi-pulse pairs are applied and qubit population is measured vs gate count. A successful result shows error accumulation that can be fitted linearly.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear linear error accumulation, good fit
- Suboptimal parameters: Some oscillation visible, moderate error rate
- Anomalous behavior: Oscillatory pattern, irregular accumulation
- Apparatus issue: No clear pattern, random scatter, no response

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """This is flux-dependent qubit spectroscopy: a 2D map of qubit transition frequency vs applied flux bias. A successful result shows a clear dispersion curve (arc or parabola) with a good fit overlaid.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear dispersion curve with good fit, in range
- Suboptimal parameters: Curve visible but noisy or fit poor
- Anomalous behavior: Multiple curves, unexpected features, asymmetric
- Apparatus issue: No clear curve, flat/noisy, no response

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_QUBIT_SPECTROSCOPY = """This is a qubit spectroscopy experiment: we sweep drive frequency to find the qubit transition. A successful result has a single clear spectral peak with a good Lorentzian fit.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Single clear peak with good Lorentzian fit
- Suboptimal parameters: Peak visible but multiple peaks or poor fit
- Anomalous behavior: Multiple peaks, unexpected positions, asymmetric
- Apparatus issue: No peaks, flat/noisy, no signal

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """This is a 2D qubit spectroscopy experiment: we sweep both drive power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, and optionally f02/2) with visible power dependence.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear f01 line visible, optionally f02/2
- Suboptimal parameters: Weak f01, limited power range
- Anomalous behavior: Multiple lines, unexpected features
- Apparatus issue: No clear lines, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RABI = """This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude where the qubit population inverts. A successful result shows clear sinusoidal oscillations with a fit that tracks the data closely.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations, good fit, visible inversion
- Suboptimal parameters: Oscillations visible but distorted or limited range
- Anomalous behavior: Wrong frequency, unexpected pattern, damping issues
- Apparatus issue: No oscillations, flat/noisy, no signal response

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RABI_HW = """This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude where the qubit population inverts. A successful result shows clear sinusoidal oscillations with a fit that tracks the data closely.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations with good fit
- Suboptimal parameters: Limited amplitude range, moderate noise
- Anomalous behavior: Unexpected oscillations, distortion
- Apparatus issue: No oscillations, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """This is a Ramsey charge tomography scan: repeated Ramsey measurements over time form a 2D map revealing charge jump events. A clean result shows continuous, undisturbed fringes.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clean fringes, no jumps visible
- Suboptimal parameters: Some noise, occasional small jumps
- Anomalous behavior: Multiple charge jumps, disrupted fringes
- Apparatus issue: No fringes, random noise, no pattern

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RAMSEY_FREQ_CAL = """This is a Ramsey frequency calibration experiment: two π/2 pulses separated by a variable delay measure frequency detuning. A successful result shows clear oscillations at the detuning frequency with a fit that accurately extracts the frequency offset.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations, clear detuning, good fit
- Suboptimal parameters: Limited oscillations, noisy data
- Anomalous behavior: Wrong frequency, unexpected pattern
- Apparatus issue: No oscillations, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RAMSEY_T2STAR = """This is a Ramsey T2* dephasing experiment: two π/2 pulses separated by a variable delay measure the dephasing time T2*. A successful result shows decaying oscillations with a fit that accurately extracts T2*.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear decaying oscillations, good T2* fit
- Suboptimal parameters: Limited decay visible, noisy
- Anomalous behavior: Beating, unexpected features
- Apparatus issue: No oscillations, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RES_SPEC = """This is a resonator spectroscopy experiment: we sweep probe frequency to find the resonator resonance. A successful result has a clear resonance feature (dip or peak).

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear resonance dip/peak with good contrast
- Suboptimal parameters: Weak resonance, limited depth
- Anomalous behavior: Multiple features, unexpected positions
- Apparatus issue: No resonance, flat/noisy baseline

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RYDBERG_RAMSEY = """This is a Ramsey experiment on the ground-to-Rydberg transition: two π/2 pulses separated by variable delay measure the coherence time (T2) and detuning frequency. A successful result shows clear oscillations.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations, good coherence
- Suboptimal parameters: Limited oscillations, fast decay
- Anomalous behavior: Unexpected frequency, irregular pattern
- Apparatus issue: No oscillations, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RYDBERG_SPECTROSCOPY = """This is Rydberg transition spectroscopy: optical detuning is swept across multiple atomic sites to locate the transition frequency. A successful result shows clear spectral features with good fits and high contrast across sites.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear spectral lines, good fits, high contrast
- Suboptimal parameters: Weak features, limited sites
- Anomalous behavior: Unexpected features, site variation
- Apparatus issue: No features, noise dominated

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_T1 = """This is a T1 relaxation experiment: after exciting the qubit to |1⟩, we measure population vs delay time. A successful result shows a clear exponential decay from high to low population with a good fit.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear exponential decay, good fit, T1 in range
- Suboptimal parameters: Decay visible but noisy or limited range
- Anomalous behavior: Unexpected rise, non-exponential behavior
- Apparatus issue: No decay, flat/noisy, no signal

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_T1_FLUCTUATIONS = """This is a T1 stability measurement: T1 relaxation time is tracked over repeated measurements. A successful result shows stable T1 values with minimal drift or jumps.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Stable T1 values, minimal variation
- Suboptimal parameters: Moderate drift, occasional jumps
- Anomalous behavior: Random walk, telegraphic noise, large jumps
- Apparatus issue: No measurable T1, random scatter

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_TWEEZER_ARRAY = """This is a camera image of an optical tweezer array used to trap neutral atoms in a regular grid. A successful image shows sharp, uniform, well-separated spots indicating proper aberration correction.

Based on what you observe in the image <image>, classify the experimental outcome.

Options:
- Expected behavior: Sharp, uniform spots in regular grid
- Suboptimal parameters: Some spots visible but irregular
- Anomalous behavior: Aberrated spots, irregular grid
- Apparatus issue: No spots visible, only background

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""


# ========== Prompt 字典映射 ==========

CLASSIFY_OUTCOME_PROMPTS = {
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


def get_classify_outcome_prompt(experiment_family: str) -> str:
    """获取分类实验结果的专属 prompt"""
    return CLASSIFY_OUTCOME_PROMPTS.get(experiment_family, CLASSIFY_OUTCOME_PROMPTS["rabi"])


# Q2: 分类实验结果 Response Schema
CLASSIFY_OUTCOME_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "Classification": {
            "type": "string",
            "enum": [
                "Expected behavior",
                "Suboptimal parameters",
                "Anomalous behavior",
                "Apparatus issue",
            ],
        },
        "Reason": {"type": "string"},
    },
    "required": ["Classification", "Reason"],
}


__all__ = [
    "CLASSIFY_OUTCOME_PROMPTS",
    "CLASSIFY_OUTCOME_RESPONSE_SCHEMA",
    "get_classify_outcome_prompt",
]