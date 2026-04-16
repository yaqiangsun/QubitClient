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
- SUCCESS: Clear coupler dispersion curve, fit tracks data
- FIT_POOR: Dispersion visible but fit deviates

When the status is not SUCCESS, provide a SPECIFIC suggested (<min flux>, <max flux>) [flux quanta].

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min flux>, <max flux>) [flux quanta] (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_CZ_BENCHMARKING = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Both retention and polarization close to 1, gradual decay, good fits
- NO_GATE: Retention unrealistically high (flat ~1) with fast depolarization — gate may not actually be occurring
- MISCALIBRATED: Fast depolarization and/or poor retention — gate miscalibrated or circuits too deep for accurate characterization

When the status is not SUCCESS, provide a SPECIFIC Suggested action: <specific recommendation for gate calibration or circuit depth adjustment>.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: Suggested action: <specific recommendation for gate calibration or circuit depth adjustment> (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_DRAG = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Zero-crossing clearly observable in sweep window
- NO_SIGNAL: Flat or random, no crossing pattern
- OPTIMAL_NOT_CENTERED: Crossing exists but in first/last quarter or outside range

When the status is not SUCCESS, provide a SPECIFIC suggested (<min 1/alpha>, <max 1/alpha>).

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min 1/alpha>, <max 1/alpha>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_GMM = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Two clearly separated clusters
- NO_SIGNAL: No distinguishable clusters
- NO_EXCITATION: No significant difference between the two distributions — qubit state not changed by the drive
- HIGH_POWER: Clusters distorted, elongated, or fragmented
- NO_RES_RESPONSE: All points collapsed to single region

When the status is not SUCCESS, provide a SPECIFIC suggested Suggested action: <specific recommendation for readout power, frequency, or qubit drive>.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: Suggested action: <specific recommendation for readout power, frequency, or qubit drive> (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_MICROWAVE_RAMSEY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: High contrast (~1), good fit, data well-described by curve
- LOW_CONTRAST: Low contrast oscillations and/or low overall retention — possible system problem
- DETUNED: Retention can be high but minima significantly above 0 — microwaves detuned on order of Rabi frequency

When the status is not SUCCESS, provide a SPECIFIC Suggested action: <specific recommendation for microwave frequency, power, or system check>.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: Suggested action: <specific recommendation for microwave frequency, power, or system check> (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_MOT_LOADING = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Well-defined, symmetric Gaussian-shaped cloud with high SNR
- NO_SIGNAL: Uniform noise across entire field, no fluorescence from trapped atoms — fundamental trap setup issue
- ASYMMETRIC: Cloud visible but with asymmetric tail/comet structure — radiation pressure imbalance or magnetic field gradient misalignment

When the status is not SUCCESS, provide a SPECIFIC suggested Suggested action: <specific recommendation for trap alignment or laser parameter adjustment>.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: Suggested action: <specific recommendation for trap alignment or laser parameter adjustment> (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_PINCHOFF = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear transition from conducting to pinched-off (current drops to near-zero residual)
- INVERTED: Current increases with gate voltage instead of decreasing — polarity or configuration error
- INCOMPLETE: Current begins to drop but sweep range too narrow to capture full transition to zero
- NO_TRANSITION: No identifiable transition — current remains flat or noisy without clear pinch-off
- NEGATIVE_OFFSET: Current crosses zero and saturates at negative value — instrumental offset or background subtraction error
- POSITIVE_OFFSET: Current decreases but saturates at a finite positive value instead of reaching zero — incomplete depletion or parasitic leakage

When the status is not SUCCESS, provide a SPECIFIC suggested Suggested action: <specific recommendation for gate voltage range or device configuration>.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: Suggested action: <specific recommendation for gate voltage range or device configuration> (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_PINGPONG = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Signal stable with increasing gate count
- NO_EXCITATION: Signal flat near ground state
- MODERATE_ERROR: Visible drift or oscillation, pi-pulse approximately correct
- LARGE_ERROR: Strong oscillation or rapid divergence

When the status is not SUCCESS, provide a SPECIFIC suggested Suggested action: <specific recommendation for pi-pulse amplitude adjustment>.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: Suggested action: <specific recommendation for pi-pulse amplitude adjustment> (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear dispersion curve, fit tracks data
- FIT_POOR: Dispersion visible but fit deviates
- FIT_FAILED: Fit completely failed to converge
- RANGE_TOO_NARROW: Dispersion only partially visible
- NO_SIGNAL: No spectral features in 2D map
- NOT_TUNABLE: Qubit frequency flat or nearly flat across flux range; no significant dispersion

When the status is not SUCCESS, provide a SPECIFIC suggested (<min flux>, <max flux>) [flux quanta] or (<min freq>, <max freq>) [GHz].

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min flux>, <max flux>) [flux quanta] or (<min freq>, <max freq>) [GHz] (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_QUBIT_SPECTROSCOPY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Single clear spectral peak with good fit
- NO_SIGNAL: No peaks visible
- MULTIPLE_PEAKS: Multiple spectral lines, ambiguous ID

When the status is not SUCCESS, provide a SPECIFIC suggested (<min frequency>, <max frequency>) [GHz].

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min frequency>, <max frequency>) [GHz] (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

# Special case: prompt includes background (different version from experiment_background field)
PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """This is a 2D qubit spectroscopy experiment on a standard transmon (negative anharmonicity, so f02/2 appears at a lower frequency than f01): we sweep both drive power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, and optionally f02/2) with visible power dependence.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear transition line(s) with full power dependence visible, usable for extraction
- AMP_TOO_HIGH: Transition power-broadened/saturated, features washed out and frequency shifted
- NO_SIGNAL: No features — wrong frequency window entirely

When the status is not SUCCESS, provide a SPECIFIC suggested (<min power>, <max power>) [a.u.] or (<min freq>, <max freq>) [GHz].

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min power>, <max power>) [a.u.] or (<min freq>, <max freq>) [GHz] (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RABI = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations, fit tracks data
- FIT_POOR: Oscillations visible but fit deviates
- RANGE_TOO_NARROW: Fewer than one full period visible
- NO_SIGNAL: Flat or random, no oscillatory structure
- DAMPED: Amplitude decays >50% within window
- UNDERSAMPLED: Too many oscillation periods; signal aliased or under-resolved

When the status is not SUCCESS, provide a SPECIFIC suggested (<min amplitude>, <max amplitude>).

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min amplitude>, <max amplitude>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RABI_HW = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations, fit tracks data
- FIT_POOR: Oscillations visible but fit deviates
- OFF_RESONANCE: Oscillations visible but drive frequency is off-resonance — distorted response with poor fit
- RANGE_TOO_NARROW: Fewer than one full period visible

When the status is not SUCCESS, provide a SPECIFIC suggested (<min amplitude>, <max amplitude>).

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min amplitude>, <max amplitude>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """Classify the charge jump activity observed in this scan <image>.

CLASSIFICATION CRITERIA
- NO_EVENT: Continuous undisturbed fringes, no charge jump detected
- EVENT: One or more discrete charge jump events visible as horizontal discontinuities in the fringe pattern
- NO_COHERENCE: No discernible fringes — coherence lost entirely, cannot assess charge jump activity

Provide your classification and briefly describe the observed charge jump activity.

The response MUST follow this exact format:

Classification: <one of the listed categories>
Notes: <1-3 sentences describing the charge jump activity>"""

PROMPT_RAMSEY_FREQ_CAL = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations with decay envelope, fit tracks data
- NO_DETUNING: Signal is flat — no oscillations
- BEATING: Amplitude modulation from multiple frequencies
- TOO_MANY_OSC: Detuning too large for time window
- TOO_FEW_OSC: Detuning too small for time window
- WINDOW_TOO_SHORT: Decay not fully captured
- SAMPLING_TOO_COARSE: Oscillations undersampled/aliased

When the status is not SUCCESS, provide a SPECIFIC suggested (<min delay>, <max delay>) [unit].

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min delay>, <max delay>) [unit] (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RAMSEY_T2STAR = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations with decay envelope, fit tracks data
- NO_DETUNING: Signal is flat — no oscillations
- BEATING: Amplitude modulation from multiple frequencies
- TOO_MANY_OSC: Detuning too large for time window
- TOO_FEW_OSC: Detuning too small for time window
- WINDOW_TOO_SHORT: Decay not fully captured
- SAMPLING_TOO_COARSE: Oscillations undersampled/aliased

When the status is not SUCCESS, provide a SPECIFIC suggested (<min delay>, <max delay>) [unit].

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min delay>, <max delay>) [unit] (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RES_SPEC = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear resonance feature visible
- NO_SIGNAL: Flat response, no resonance in frequency range

When the status is not SUCCESS, provide a SPECIFIC suggested (<min frequency>, <max frequency>) [GHz].

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min frequency>, <max frequency>) [GHz] (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RYDBERG_RAMSEY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: A single decaying sinusoidal fit is consistent across all time windows, with low RChi2
- UNDERSAMPLED: Data clusters do not span enough of the oscillation period; the fit cannot reconcile all time windows simultaneously

When the status is not SUCCESS, provide a SPECIFIC Suggested action: <specific recommendation for sampling density or measurement window>.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: Suggested action: <specific recommendation for sampling density or measurement window> (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_RYDBERG_SPECTROSCOPY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Good fits (low chi-squared), clear spectral features, high contrast across sites
- LOW_CONTRAST: Reduced contrast, noisy resonance, many sites failed to fit

When the status is not SUCCESS, provide a SPECIFIC Suggested action: <specific recommendation for laser power, frequency, or alignment>.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: Suggested action: <specific recommendation for laser power, frequency, or alignment> (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_T1 = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear exponential decay, fit tracks data
- NO_SIGNAL: Population is flat — qubit never excited or decayed instantly
- WINDOW_TOO_SHORT: Signal hasn't reached baseline
- SAMPLING_TOO_COARSE: Time steps too large to resolve decay

When the status is not SUCCESS, provide a SPECIFIC suggested (<min delay>, <max delay>) [us].

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min delay>, <max delay>) [us] (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_T1_FLUCTUATIONS = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- STABLE: T1 values tightly clustered around a single baseline, variation dominated by measurement scatter
- TELEGRAPHIC: T1 switches abruptly between two or more discrete metastable levels — indicates coupling to a two-level system defect
- RANDOM_WALK: T1 shows continuous correlated drift over a wide range — indicates slow environmental changes (temperature, magnetic field, charge noise)

Provide a brief explanation of your classification.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: Suggested action: <specific recommendation for T1 stabilization or further characterization> (or "N/A" if STABLE)
Notes: <1-3 sentences explaining your reasoning>"""

PROMPT_TWEEZER_ARRAY = """Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- CORRECTED: Regular grid of sharp, uniform spots — aberration corrected
- ABERRATED: Spots are blurred, non-uniform, or missing — aberration not corrected

When the status is not SUCCESS, provide a SPECIFIC Suggested action: <specific recommendation>.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: Suggested action: <specific recommendation> (or "N/A" if SUCCESS)
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
                "INVERTED",
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