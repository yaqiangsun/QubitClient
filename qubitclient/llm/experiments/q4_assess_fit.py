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

PROMPT_COUPLER_FLUX = """Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable: Clear avoided crossing with good fit quality
- Unreliable: No clear pattern or poor fit quality
- No fit: No fit attempted or visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_CZ_BENCHMARKING = """Assess whether the data in this plot <image> is reliable for gate fidelity assessment.

Options:
- Reliable: Clear decay pattern with high retention/polarization
- Unreliable: No clear pattern or unexpected behavior
- No fit: No clear trend visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_DRAG = """A successful result has the zero-crossing clearly observable in the sweep window.

Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable: Clear crossing with good linear fits
- Unreliable: No clear crossing or poor fit quality
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_GMM = """Assess whether the GMM fit in this plot <image> is reliable for state discrimination.

Options:
- Reliable: Clear separation with good fit
- Unreliable: Overlapping clusters or poor fit
- No fit: No fit visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_MICROWAVE_RAMSEY = """Assess whether the fit to the data in this plot <image> is reliable for extracting frequency and contrast.

Options:
- Reliable: Clear oscillations with good fit
- Unreliable: No clear oscillations or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_MOT_LOADING = """Assess whether the image <image> shows a reliable atomic cloud for experiments.

Options:
- Reliable: Clear, compact cloud visible
- Unreliable: Diffuse or unclear cloud
- No cloud: No cloud visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_PINCHOFF = """Assess whether the data in this plot <image> shows a reliable pinch-off transition.

Options:
- Reliable: Clear transition with identifiable regions
- Unreliable: No clear transition or noisy
- No transition: No pinch-off visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_PINGPONG = """Assess whether the fit to the data in this plot <image> is reliable for extracting error rate.

Options:
- Reliable: Clear linear accumulation with good fit
- Unreliable: No clear pattern or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """A successful result shows clear dispersion curve with good fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting dispersion.

Options:
- Reliable: Clear curve with good fit
- Unreliable: No clear curve or poor fit
- No fit: No fit visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_QUBIT_SPECTROSCOPY = """Assess whether the fit to the data in this plot <image> is reliable for extracting frequency.

Options:
- Reliable: Clear peak with good Lorentzian fit
- Unreliable: No clear peak or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """Assess whether the data in this plot <image> shows reliable transition lines.

Options:
- Reliable: Clear f01 line (and f02/2 if present)
- Unreliable: No clear lines or very weak
- No features: No transition features visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RABI = """Assess whether the fit to the data in this plot <image> is reliable for extracting pi-pulse amplitude.

Options:
- Reliable: Clear oscillations with good fit
- Unreliable: No clear oscillations or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RABI_HW = """Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable: Clear oscillations with good fit
- Unreliable: No clear oscillations or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """Assess whether the data in this plot <image> shows reliable fringe pattern for charge analysis.

Options:
- Reliable: Clear fringes, no jumps
- Unreliable: Jumps present or very noisy
- No pattern: No clear fringe pattern

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RAMSEY_FREQ_CAL = """Assess whether the fit to the data in this plot <image> is reliable for extracting detuning.

Options:
- Reliable: Clear oscillations with good fit
- Unreliable: No clear oscillations or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RAMSEY_T2STAR = """Assess whether the fit to the data in this plot <image> is reliable for extracting T2*.

Options:
- Reliable: Clear decaying oscillations with good fit
- Unreliable: No clear decay or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RES_SPEC = """Assess whether the data in this plot <image> shows a reliable resonance for extracting frequency.

Options:
- Reliable: Clear resonance with good contrast
- Unreliable: No clear resonance or very weak
- No resonance: No resonance feature visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RYDBERG_RAMSEY = """Assess whether the data in this plot <image> is reliable for extracting T2 and detuning.

Options:
- Reliable: Clear oscillations with good contrast
- Unreliable: No clear oscillations or poor quality
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RYDBERG_SPECTROSCOPY = """Assess whether the fits to the data in this plot <image> are reliable for extracting transition frequencies.

Options:
- Reliable: Clear features with good fits
- Unreliable: No clear features or poor fits
- No fit: No fit visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_T1 = """Assess whether the fit to the data in this plot <image> is reliable for extracting T1.

Options:
- Reliable: Clear decay with good fit
- Unreliable: No clear decay or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_T1_FLUCTUATIONS = """Assess whether the data in this plot <image> is reliable for classifying T1 stability.

Options:
- Reliable: Clear trend (stable/fluctuating)
- Unreliable: No clear pattern or very noisy
- No data: No measurable T1

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_TWEEZER_ARRAY = """Assess whether the image <image> shows a reliable tweezer array for experiments.

Options:
- Reliable: Sharp, uniform spots in grid
- Unreliable: Irregular or non-uniform spots
- No spots: No spots visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""


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