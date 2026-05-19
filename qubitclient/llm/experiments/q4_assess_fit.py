# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
Q4: 评估拟合任务

评估数据拟合是否可用于参数提取
"""

# ========== 独立 Prompt 字符串定义 ==========

# Standard assess fit prompt
PROMPT_STANDARD = """Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable
- Unreliable
- No fit

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

# Special case for qubit_spectroscopy_power_frequency (has background)
PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """This is a 2D qubit spectroscopy experiment on a standard transmon (negative anharmonicity, so f02/2 appears at a lower frequency than f01): we sweep both drive power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, and optionally f02/2) with visible power dependence.

Assess whether the fit to the data in these plots <image>, <image> and <image> is reliable for parameter extraction.

Options:
- Reliable
- Unreliable
- No fit

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

# Aliases for all experiments
PROMPT_COUPLER_FLUX = PROMPT_STANDARD
PROMPT_CZ_BENCHMARKING = PROMPT_STANDARD
# ORIGIN DRAG PROMPT
# PROMPT_DRAG = PROMPT_STANDARD
PROMPT_DRAG = """Evaluate the image <image> and determine the experiment status.
Red curve: fitted to green curve
Orange curve: fitted to blue curve

CRITICAL: The fit does NOT need to perfectly match every noise peak or oscillation.
If the fitted curves(Red and Orange curves) captures the correct crossing trend near x=0, it is Reliable.
If the fitted curves(Red and Orange curves) captures the crossing trend not near  x=0, it is Unreliable.
If the fitted curves(Red and Orange curves)  do not captures any crossing, it is Unreliable.

Options:
- Reliable
- Unreliable
- No fit

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_GMM = PROMPT_STANDARD
PROMPT_MICROWAVE_RAMSEY = PROMPT_STANDARD
PROMPT_MOT_LOADING = PROMPT_STANDARD
PROMPT_PINCHOFF = PROMPT_STANDARD
PROMPT_PINGPONG = PROMPT_STANDARD
PROMPT_QUBIT_FLUX_SPECTROSCOPY = PROMPT_STANDARD
PROMPT_QUBIT_SPECTROSCOPY = PROMPT_STANDARD
# Note: PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY already defined above
PROMPT_RABI = PROMPT_STANDARD
PROMPT_RABI_HW = PROMPT_STANDARD
PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = PROMPT_STANDARD
PROMPT_RAMSEY_FREQ_CAL = PROMPT_STANDARD
PROMPT_RAMSEY_T2STAR = PROMPT_STANDARD
PROMPT_RES_SPEC = PROMPT_STANDARD
PROMPT_RYDBERG_RAMSEY = PROMPT_STANDARD
PROMPT_RYDBERG_SPECTROSCOPY = PROMPT_STANDARD
PROMPT_T1 = PROMPT_STANDARD
PROMPT_T1_FLUCTUATIONS = PROMPT_STANDARD
PROMPT_TWEEZER_ARRAY = PROMPT_STANDARD

# ========== Not in QCalEval ==========
PROMPT_S21 =  """Assess whether the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable
- Unreliable

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_SPECTRUM_2D = """Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

CRITICAL FIRST STEP - VISUAL INSPECTION:
Look at the image carefully. Determine if there is a RED colored curve/lines overlaid on the heatmap.
- If NO red curve exists in the image → answer "No fit"
- Only if a red curve EXISTS, then evaluate whether it tracks the data features

BACKGROUND:
- The data contains a cos_dark feature (low-intensity cosine-shaped curve representing qubit frequency vs Z voltage).
- The fitted curve, when it exists, is plotted in RED color.

CRITERIA:
- Reliable: A RED fitted curve EXISTS in the image AND it accurately follows the visible cos_dark feature (the continuous dark band/curve that shifts with Z amplitude) in the data.
- Unreliable: A RED fitted curve EXISTS but it does NOT follow any coherent feature in the data (e.g., it tracks noise, is misaligned with the dark band, or jumps randomly).
- No fit: NO RED fitted curve is present in the image. (Do not invent or assume a fit exists)

IMPORTANT: 
- The cos_dark feature is typically a low-intensity curve. Do NOT mark as Unreliable just because the tracked feature is not the brightest in the image.
- The presence of a RED curve means a fitting attempt was made. Assess whether it correctly tracks the cos_dark feature.

Options:
- Reliable
- Unreliable
- No fit

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""
PROMPT_OPTPIPULSE = """Assess whether the peak detection in this plot <image> is reliable for extracting common peak position.

CRITICAL FIRST STEP - VISUAL INSPECTION:
Look at the image carefully. This is a PEAK DETECTION task on RAW WAVEFORMS. There are NO fitted curves — only original data traces and possibly a red dashed line.

Check for:
1. How many waveforms (curves) are present?
2. Does EACH waveform have a clear, identifiable peak?
3. Is there a RED VERTICAL DASHED LINE on the plot?
4. If a red dashed line exists, does it pass through the peaks of ALL waveforms?

CRITERIA:
- Reliable: 
  - A red vertical dashed line EXISTS in the plot
  - EACH waveform has a clear peak
  - The red dashed line ALIGNS with the peaks of ALL waveforms (common peak)
- Unreliable: 
  - A red dashed line exists but does NOT align with peaks of all waveforms, OR
  - No red dashed line exists but waveforms DO have common peak (algorithm missed it), OR
  - Any waveform lacks a clear peak (flat, monotonic, too noisy)
- No signal: No waveforms present, or all waveforms are flat/noisy with no detectable peaks

IMPORTANT:
- The presence of a red vertical dashed line indicates the detection algorithm identified a common peak
- Reliability depends on whether that red line actually passes through the visible peaks
- Do NOT evaluate fit quality — there is no fit

Options:
- Reliable
- Unreliable
- No signal

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RABICOS = """Assess whether the peak detection in this plot <image> is reliable for extracting the first peak position (π/2 pulse amplitude).

CRITICAL FIRST STEP - VISUAL INSPECTION:
Look at the image carefully. This is a PEAK DETECTION task on RAW WAVEFORM. There are NO fitted curves — only the original data trace and possibly a red dashed line.

Check for:
1. Does the waveform show a clear Rabi oscillation pattern (oscillating up and down)?
2. Is there a clear FIRST PEAK (first maximum after start)?
3. Is there a RED VERTICAL DASHED LINE on the plot?
4. If a red dashed line exists, does it align with the first peak of the waveform?

CRITERIA:
- Reliable: 
  - A red vertical dashed line EXISTS in the plot
  - The waveform has a clear first peak
  - The red dashed line ALIGNS with the first peak
- Unreliable: 
  - A red dashed line exists but does NOT align with the first peak, OR
  - No red dashed line exists but the waveform DOES have a clear first peak (algorithm missed it), OR
  - The waveform lacks a clear first peak (flat, monotonic, too noisy, or first peak not discernible)
- No signal: No waveform present, or waveform is flat/noisy with no detectable oscillation

IMPORTANT:
- The presence of a red vertical dashed line indicates the detection algorithm identified a first peak
- Reliability depends on whether that red line actually passes through the visible first peak
- Do NOT evaluate fit quality — there is no fit

Options:
- Reliable
- Unreliable
- No signal

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""


PROMPT_RAMSEY = """Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

CRITICAL FIRST STEP - VISUAL INSPECTION:
Look at the image carefully. Identify the raw data points and the fitted curve (blue line or similar).

Check for:
1. Does the fitted curve accurately follow the raw data points across the ENTIRE range?
2. Are there systematic deviations (e.g., early-time misfit, phase shift, amplitude mismatch)?
3. Does the fit capture key features (oscillation frequency, decay envelope)?

CRITERIA:
- Reliable: The fitted curve accurately tracks the raw data points throughout the entire time range. No systematic deviations.
- Unreliable: The fitted curve shows significant deviation from raw data in any region (especially early time), OR misses key features like oscillation frequency or decay rate.
- No fit: No fitted curve present.

Options:
- Reliable
- Unreliable
- No fit

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_S21VFLUX = """Assess whether the fit to the data in this plot  <image> is reliable for parameter extraction.

CRITICAL FIRST STEP - VISUAL INSPECTION:
Look at the image carefully. Determine if there is a RED colored curve/lines overlaid on the heatmap. 
- If NO red curve exists in the image → answer "No fit"
- Only if a red curve EXISTS, then evaluate whether it tracks the data features

BACKGROUND:
- The data may contain multiple features (cos_dark, cos_light, line_dark, line_light).
- All fitted curves, when they exist, are plotted in RED color.

CRITERIA:
- Reliable: A RED fitted curve EXISTS in the image AND it accurately follows a visible, continuous feature (dark or bright, cosine or line) in the data.
- Unreliable: A RED fitted curve EXISTS but it does NOT follow any coherent feature in the data.
- No fit: NO RED fitted curve is present in the image. (Do not invent or assume a fit exists)

Options:
- Reliable
- Unreliable
- No fit

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_POWERSHIFT = """Assess whether the dip trajectory clustering in this plot <image> is reliable.

CRITICAL: Base your assessment ONLY on what you can SEE in the image.

DEFINITIONS:
- A "bend" or "turn" is where the trajectory changes direction (e.g., from vertical to diagonal). This is a CONNECTION, not a break.
- A "gap" or "fragmentation" means missing dip points between segments (no data).
- A "vertical jump" is a sudden frequency change at the same power — this is a valid feature, not a break.

CONNECTED vs DISCONNECTED:
- If the end of one segment touches the start of the next segment → CONNECTED (valid trajectory)
- If there is empty space (no dip points) between segments → DISCONNECTED (fragmented)

FIRST, determine reliability based on:
- Reliable: Dip points form a coherent path. Segments are connected (even if they bend). No large gaps.
- Unreliable: No dip points visible, OR points are randomly scattered, OR large gaps exist between segments, OR clustering is clearly wrong.

SECOND, describe what you actually observe:
- How many distinct segments?
- Are the segments connected end-to-end? (look for bends/turns, not breaks)
- Sequence of shapes (e.g., "vertical → diagonal → vertical")

Options:
- Reliable
- Unreliable

Provide your answer in this EXACT format:

Assessment: <Reliable or Unreliable>
Observed segments: <number>
Observed shape: <sequence description>
Reason: <brief explanation>"""

PROMPT_SINGLESHOT = PROMPT_GMM
PROMPT_SPECTRUM = PROMPT_QUBIT_SPECTROSCOPY
PROMPT_T2 = PROMPT_RAMSEY_T2STAR
PROMPT_RB = PROMPT_STANDARD



# ========== Prompt 字典映射 ==========

ASSESS_FIT_PROMPTS = {
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
    "spectrum_2d": PROMPT_SPECTRUM_2D,
    "optpipulse": PROMPT_OPTPIPULSE,
    "rabicos": PROMPT_RABICOS,
    "ramsey": PROMPT_RAMSEY,
    "s21vflux": PROMPT_S21VFLUX,
    "powershift": PROMPT_POWERSHIFT,
    "singleshot": PROMPT_SINGLESHOT,
    "spectrum": PROMPT_SPECTRUM,
    "t2": PROMPT_T2,
    "rb": PROMPT_RB,
}


def get_assess_fit_prompt(experiment_family: str) -> str:
    """获取评估拟合的专属 prompt"""
    return ASSESS_FIT_PROMPTS.get(experiment_family, ASSESS_FIT_PROMPTS["rabi"])


# Q4: 评估拟合 Response Schema
ASSESS_FIT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "Assessment": {
            "type": "string",
            "enum": ["Reliable", "Unreliable", "No fit"],
        },
        "Reason": {"type": "string"},
    },
    "required": ["Assessment", "Reason"],
}


__all__ = [
    "ASSESS_FIT_PROMPTS",
    "ASSESS_FIT_RESPONSE_SCHEMA",
    "get_assess_fit_prompt",
]