# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
Q6: 评估状态任务

判断实验成功/失败状态并给出建议
"""

# ========== 独立 Prompt 字符串定义 ==========

PROMPT_COUPLER_FLUX = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear avoided crossing with good fit within sweep range
- NO_SIGNAL: Flat or noisy data, no clear crossing pattern
- OPTIMAL_NOT_CENTERED: Crossing exists but near edge of range or fit poor

When the status is not SUCCESS, provide a SPECIFIC suggested flux range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_CZ_BENCHMARKING = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: High retention (>0.9) and polarization, clear decay pattern
- NO_SIGNAL: Random data, no clear decay
- OPTIMAL_NOT_CENTERED: Moderate values but acceptable

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_DRAG = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Zero-crossing clearly observable in sweep window
- NO_SIGNAL: Flat or random, no crossing pattern
- OPTIMAL_NOT_CENTERED: Crossing exists but in first/last quarter or outside range

When the status is not SUCCESS, provide a SPECIFIC suggested 1/alpha range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min 1/alpha>, <max 1/alpha>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_GMM = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Two well-separated clusters clearly visible
- NO_SIGNAL: Single blob or random scatter, no discrimination possible
- OPTIMAL_NOT_CENTERED: Clusters touching or partially overlapping

When the status is not SUCCESS, provide a SPECIFIC suggested adjustment.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_MICROWAVE_RAMSEY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations with high contrast (>0.8), good fit
- NO_SIGNAL: Flat or random, no oscillations
- OPTIMAL_NOT_CENTERED: Oscillations visible but low contrast or noisy

When the status is not SUCCESS, provide a SPECIFIC suggested delay range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_MOT_LOADING = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear, compact cloud with good brightness
- NO_SIGNAL: No cloud visible, only background
- OPTIMAL_NOT_CENTERED: Cloud present but diffuse or offset

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_PINCHOFF = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear pinch-off transition with identifiable regions
- NO_SIGNAL: No measurable current or no transition
- OPTIMAL_NOT_CENTERED: Transition visible but noisy or incomplete

When the status is not SUCCESS, provide a SPECIFIC suggested voltage range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_PINGPONG = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear linear error accumulation, good fit
- NO_SIGNAL: No clear pattern, random scatter
- OPTIMAL_NOT_CENTERED: Some pattern but irregular

When the status is not SUCCESS, provide a SPECIFIC suggested gate count range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear dispersion curve with good fit, in range
- NO_SIGNAL: Flat or noisy, no clear curve
- OPTIMAL_NOT_CENTERED: Curve visible but noisy or fit poor

When the status is not SUCCESS, provide a SPECIFIC suggested flux range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_QUBIT_SPECTROSCOPY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Single clear peak with good Lorentzian fit
- NO_SIGNAL: Flat or noisy, no peaks
- OPTIMAL_NOT_CENTERED: Multiple peaks or poor fit

When the status is not SUCCESS, provide a SPECIFIC suggested frequency range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear f01 line visible (and f02/2 if present)
- NO_SIGNAL: No clear lines, flat/noisy
- OPTIMAL_NOT_CENTERED: Weak features or limited range

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RABI = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations, good fit, visible inversion
- NO_SIGNAL: Flat or random, no oscillations
- OPTIMAL_NOT_CENTERED: Oscillations visible but distorted or limited

When the status is not SUCCESS, provide a SPECIFIC suggested amplitude range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RABI_HW = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations with good fit
- NO_SIGNAL: Flat or noisy, no oscillations
- OPTIMAL_NOT_CENTERED: Limited amplitude range

When the status is not SUCCESS, provide a SPECIFIC suggested amplitude range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clean fringes, no jumps visible
- NO_SIGNAL: No clear pattern, random noise
- OPTIMAL_NOT_CENTERED: Occasional small jumps or noise

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RAMSEY_FREQ_CAL = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations, clear detuning, good fit
- NO_SIGNAL: Flat or noisy, no oscillations
- OPTIMAL_NOT_CENTERED: Limited oscillations, noisy

When the status is not SUCCESS, provide a SPECIFIC suggested delay range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RAMSEY_T2STAR = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear decaying oscillations, good T2* fit
- NO_SIGNAL: Flat or noisy, no oscillations
- OPTIMAL_NOT_CENTERED: Limited decay visible, noisy

When the status is not SUCCESS, provide a SPECIFIC suggested delay range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RES_SPEC = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear resonance dip/peak with good contrast
- NO_SIGNAL: Flat baseline, no resonance
- OPTIMAL_NOT_CENTERED: Weak resonance, limited depth

When the status is not SUCCESS, provide a SPECIFIC suggested frequency range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RYDBERG_RAMSEY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations, good coherence
- NO_SIGNAL: Flat or noisy, no oscillations
- OPTIMAL_NOT_CENTERED: Limited oscillations, fast decay

When the status is not SUCCESS, provide a SPECIFIC suggested delay range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RYDBERG_SPECTROSCOPY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear spectral lines, good fits, high contrast
- NO_SIGNAL: No features, noise dominated
- OPTIMAL_NOT_CENTERED: Weak features, limited sites

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_T1 = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear exponential decay, good fit, T1 in reasonable range
- NO_SIGNAL: Flat or random, no decay pattern
- OPTIMAL_NOT_CENTERED: Decay visible but noisy or limited range

When the status is not SUCCESS, provide a SPECIFIC suggested delay range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_T1_FLUCTUATIONS = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Stable T1 values, minimal variation
- NO_SIGNAL: No measurable T1, random scatter
- OPTIMAL_NOT_CENTERED: Moderate drift or occasional jumps

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_TWEEZER_ARRAY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Sharp, uniform spots in regular grid
- NO_SIGNAL: No spots visible, only background
- OPTIMAL_NOT_CENTERED: Some spots but irregular or non-uniform

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""


# ========== Prompt 字典映射 ==========

EVALUATE_STATUS_PROMPTS = {
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


def get_evaluate_status_prompt(experiment_family: str) -> str:
    """获取评估状态的专属 prompt"""
    return EVALUATE_STATUS_PROMPTS.get(experiment_family, EVALUATE_STATUS_PROMPTS["rabi"])


# Q6: 评估状态 Response Schema
EVALUATE_STATUS_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "Status": {
            "type": "string",
            "enum": [
                "SUCCESS",
                "NO_SIGNAL",
                "OPTIMAL_NOT_CENTERED",
                "ABERRATED",
                "AMP_TOO_HIGH",
                "ASYMMETRIC",
                "BEATING",
                "CORRECTED",
                "DAMPED",
                "DETUNED",
                "EVENT",
                "FIT_FAILED",
                "FIT_POOR",
                "HIGH_POWER",
                "INCOMPLETE",
                "LARGE_ERROR",
                "LOW_CONTRAST",
                "MISCALIBRATED",
                "MODERATE_ERROR",
                "MULTIPLE_PEAKS",
                "NEGATIVE_OFFSET",
                "NOT_TUNABLE",
                "NO_COHERENCE",
                "NO_DETUNING",
                "NO_EVENT",
                "NO_EXCITATION",
                "NO_GATE",
                "NO_RES_RESPONSE",
                "NO_TRANSITION",
                "OFF_RESONANCE",
                "POSITIVE_OFFSET",
                "RANDOM_WALK",
                "RANGE_TOO_NARROW",
                "SAMPLING_TOO_COARSE",
                "STABLE",
                "TELEGRAPHIC",
                "TOO_FEW_OSC",
                "TOO_MANY_OSC",
                "UNDERSAMPLED",
                "WINDOW_TOO_SHORT",
            ],
        },
        "Suggested range": {"type": "string"},
        "Notes": {"type": "string"},
    },
    "required": ["Status", "Suggested range", "Notes"],
}


__all__ = [
    "EVALUATE_STATUS_PROMPTS",
    "EVALUATE_STATUS_RESPONSE_SCHEMA",
    "get_evaluate_status_prompt",
]