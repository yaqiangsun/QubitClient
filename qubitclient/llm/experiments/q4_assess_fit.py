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
PROMPT_DRAG = PROMPT_STANDARD
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
PROMPT_S21 = PROMPT_STANDARD
PROMPT_SPECTRUM_2D = PROMPT_STANDARD
PROMPT_OPTPIPULSE = PROMPT_STANDARD
PROMPT_RABICOS = PROMPT_STANDARD
PROMPT_RAMSEY = PROMPT_STANDARD
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

BACKGROUND:
The trajectory is obtained by:
1. For each row (power level), finding the darkest column (frequency) — the resonance dip
2. Clustering these dip points across rows to form continuous segments
3. Connecting segments that are physically meaningful

Possible trajectory shapes (ALL are valid as long as clustering is correct):
- No dip points found in any row
- Single straight line
- Single bent line (continuous slope change)
- Two segments: straight → bent, OR bent → straight, OR straight → straight (with possible vertical jump at boundary)
- Three segments: straight → bent → straight

CRITICAL RULES:
- A vertical jump (same power, different frequency between consecutive rows) is a VALID trajectory feature — it indicates a mode jump or bistability. Do NOT mark as unreliable solely because of a vertical jump.
- "Fragmented" means gaps where no dip point exists between segments. This is different from a vertical jump (where dip exists in every row, just at different frequencies).
- Only mark as UNRELIABLE if:
  1. No dip points found in any row (completely empty trajectory), OR
  2. Clustering is clearly wrong (e.g., points randomly scattered with no coherent path, or obvious outliers connected incorrectly)

Reliability criteria:
- Reliable: Dip points form a coherent path (straight, bent, or with vertical jumps). Segments are correctly connected. Clustering captures the physical resonance movement.
- Unreliable: No dip points at all, OR clustering is erroneous (random noise, obviously wrong connections, points do not follow a clear trend).

Options:
- Reliable
- Unreliable

Provide your answer as:
Assessment: <your choice>
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