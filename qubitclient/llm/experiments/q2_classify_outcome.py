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

PROMPT_COUPLER_FLUX = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear avoided crossing with good fit, crossing within range
- Suboptimal parameters: Crossings visible but fit quality poor or crossing near edge
- Anomalous behavior: Multiple crossings, asymmetric pattern, unexpected behavior
- Apparatus issue: No clear crossing pattern, flat/noisy data

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_CZ_BENCHMARKING = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: High retention (>0.9) and polarization, clear decay with depth
- Suboptimal parameters: Moderate values, faster than expected decay
- Anomalous behavior: Unexpected oscillations, polarization loss, irregular decay
- Apparatus issue: No decay pattern, random data, measurement error

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_DRAG = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear zero-crossing within sweep window, good linear fits
- Suboptimal parameters: Crossing visible but near edge of range, or limited data
- Anomalous behavior: Wrong crossing direction, asymmetric slopes, unexpected pattern
- Apparatus issue: No clear crossing, flat/noisy data, no signal response

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_GMM = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Two well-separated clusters, clear discrimination
- Suboptimal parameters: Clusters touching or partially overlapping, moderate separation
- Anomalous behavior: Single blob, clusters in wrong positions, unexpected distribution
- Apparatus issue: No clusters visible, random scatter, measurement error

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_MICROWAVE_RAMSEY = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations with high contrast, good fit
- Suboptimal parameters: Low contrast, fast decay, limited oscillations visible
- Anomalous behavior: Unexpected frequency, irregular pattern, drift
- Apparatus issue: No oscillations, flat/noisy data, random scatter

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_MOT_LOADING = """Based on what you observe in the image <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear, compact cloud with good brightness
- Suboptimal parameters: Cloud present but diffuse or offset
- Anomalous behavior: Multiple clouds, elongated shape, unexpected features
- Apparatus issue: No cloud visible, only background noise

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_PINCHOFF = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear pinch-off transition with identifiable regions
- Suboptimal parameters: Transition visible but noisy or incomplete
- Anomalous behavior: No clear transition, irregular behavior
- Apparatus issue: No measurable current, no transition, noise dominated

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_PINGPONG = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear linear error accumulation, good fit
- Suboptimal parameters: Some oscillation visible, moderate error rate
- Anomalous behavior: Oscillatory pattern, irregular accumulation
- Apparatus issue: No clear pattern, random scatter, no response

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear dispersion curve with good fit, in range
- Suboptimal parameters: Curve visible but noisy or fit poor
- Anomalous behavior: Multiple curves, unexpected features, asymmetric
- Apparatus issue: No clear curve, flat/noisy, no response

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_QUBIT_SPECTROSCOPY = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Single clear peak with good Lorentzian fit
- Suboptimal parameters: Peak visible but multiple peaks or poor fit
- Anomalous behavior: Multiple peaks, unexpected positions, asymmetric
- Apparatus issue: No peaks, flat/noisy, no signal

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear f01 line visible, optionally f02/2
- Suboptimal parameters: Weak f01, limited power range
- Anomalous behavior: Multiple lines, unexpected features
- Apparatus issue: No clear lines, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RABI = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations, good fit, visible inversion
- Suboptimal parameters: Oscillations visible but distorted or limited range
- Anomalous behavior: Wrong frequency, unexpected pattern, damping issues
- Apparatus issue: No oscillations, flat/noisy, no signal response

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RABI_HW = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations with good fit
- Suboptimal parameters: Limited amplitude range, moderate noise
- Anomalous behavior: Unexpected oscillations, distortion
- Apparatus issue: No oscillations, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clean fringes, no jumps visible
- Suboptimal parameters: Some noise, occasional small jumps
- Anomalous behavior: Multiple charge jumps, disrupted fringes
- Apparatus issue: No fringes, random noise, no pattern

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RAMSEY_FREQ_CAL = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations, clear detuning, good fit
- Suboptimal parameters: Limited oscillations, noisy data
- Anomalous behavior: Wrong frequency, unexpected pattern
- Apparatus issue: No oscillations, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RAMSEY_T2STAR = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear decaying oscillations, good T2* fit
- Suboptimal parameters: Limited decay visible, noisy
- Anomalous behavior: Beating, unexpected features
- Apparatus issue: No oscillations, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RES_SPEC = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear resonance dip/peak with good contrast
- Suboptimal parameters: Weak resonance, limited depth
- Anomalous behavior: Multiple features, unexpected positions
- Apparatus issue: No resonance, flat/noisy baseline

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RYDBERG_RAMSEY = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations, good coherence
- Suboptimal parameters: Limited oscillations, fast decay
- Anomalous behavior: Unexpected frequency, irregular pattern
- Apparatus issue: No oscillations, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_RYDBERG_SPECTROSCOPY = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear spectral lines, good fits, high contrast
- Suboptimal parameters: Weak features, limited sites
- Anomalous behavior: Unexpected features, site variation
- Apparatus issue: No features, noise dominated

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_T1 = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear exponential decay, good fit, T1 in range
- Suboptimal parameters: Decay visible but noisy or limited range
- Anomalous behavior: Unexpected rise, non-exponential behavior
- Apparatus issue: No decay, flat/noisy, no signal

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_T1_FLUCTUATIONS = """Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Stable T1 values, minimal variation
- Suboptimal parameters: Moderate drift, occasional jumps
- Anomalous behavior: Random walk, telegraphic noise, large jumps
- Apparatus issue: No measurable T1, random scatter

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>"""

PROMPT_TWEEZER_ARRAY = """Based on what you observe in the image <image>, classify the experimental outcome.

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