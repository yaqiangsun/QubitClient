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

PROMPT_COUPLER_FLUX = """This is tunable coupler spectroscopy: we map the coupler's frequency response vs applied flux bias. A successful result shows a clear coupler dispersion curve with a good fit.

Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable: Clear avoided crossing with good fit quality
- Unreliable: No clear pattern or poor fit quality
- No fit: No fit attempted or visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_CZ_BENCHMARKING = """This is CZ gate benchmarking: measures retention probability and cycle polarization vs circuit depth. A successful result shows retention and polarization close to 1 with gradual decay.

Assess whether the data in this plot <image> is reliable for gate fidelity assessment.

Options:
- Reliable: Clear decay pattern with high retention/polarization
- Unreliable: No clear pattern or unexpected behavior
- No fit: No clear trend visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_DRAG = """This is a DRAG calibration: we sweep 1/alpha to find the optimal value. A successful result has the zero-crossing clearly observable in the sweep window.

Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable: Clear crossing with good linear fits
- Unreliable: No clear crossing or poor fit quality
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_GMM = """This is GMM discrimination: I-Q scatter plot for |0⟩ and |1⟩ states with GMM fit. A successful result has two well-separated clusters.

Assess whether the GMM fit in this plot <image> is reliable for state discrimination.

Options:
- Reliable: Clear separation with good fit
- Unreliable: Overlapping clusters or poor fit
- No fit: No fit visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_MICROWAVE_RAMSEY = """This is a microwave Ramsey: sinusoidal oscillations with contrast close to 1 and good fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting frequency and contrast.

Options:
- Reliable: Clear oscillations with good fit
- Unreliable: No clear oscillations or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_MOT_LOADING = """This is a MOT loading image: shows trapped atoms in a magneto-optical trap.

Assess whether the image <image> shows a reliable atomic cloud for experiments.

Options:
- Reliable: Clear, compact cloud visible
- Unreliable: Diffuse or unclear cloud
- No cloud: No cloud visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_PINCHOFF = """This is pinch-off measurement: current trace vs gate voltage to determine device pinch-off.

Assess whether the data in this plot <image> shows a reliable pinch-off transition.

Options:
- Reliable: Clear transition with identifiable regions
- Unreliable: No clear transition or noisy
- No transition: No pinch-off visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_PINGPONG = """This is PingPong calibration: error accumulation vs gate count. A successful result shows linear error accumulation.

Assess whether the fit to the data in this plot <image> is reliable for extracting error rate.

Options:
- Reliable: Clear linear accumulation with good fit
- Unreliable: No clear pattern or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """This is flux-dependent qubit spectroscopy: 2D map of qubit frequency vs flux. A successful result shows clear dispersion curve with good fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting dispersion.

Options:
- Reliable: Clear curve with good fit
- Unreliable: No clear curve or poor fit
- No fit: No fit visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_QUBIT_SPECTROSCOPY = """This is qubit spectroscopy: sweep drive frequency to find qubit transition. A successful result has a single clear peak with good Lorentzian fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting frequency.

Options:
- Reliable: Clear peak with good Lorentzian fit
- Unreliable: No clear peak or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """This is 2D qubit spectroscopy: sweep power and frequency to map transitions. A successful result shows clear transition lines.

Assess whether the data in this plot <image> shows reliable transition lines.

Options:
- Reliable: Clear f01 line (and f02/2 if present)
- Unreliable: No clear lines or very weak
- No features: No transition features visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RABI = """This is Rabi experiment: sweep pulse amplitude to find pi-pulse. A successful result shows clear oscillations with fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting pi-pulse amplitude.

Options:
- Reliable: Clear oscillations with good fit
- Unreliable: No clear oscillations or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RABI_HW = """This is Rabi experiment with hardware characterization: clear oscillations with fit.

Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable: Clear oscillations with good fit
- Unreliable: No clear oscillations or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """This is Ramsey charge tomography: 2D map over time revealing charge jumps. Clean result shows continuous fringes.

Assess whether the data in this plot <image> shows reliable fringe pattern for charge analysis.

Options:
- Reliable: Clear fringes, no jumps
- Unreliable: Jumps present or very noisy
- No pattern: No clear fringe pattern

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RAMSEY_FREQ_CAL = """This is Ramsey frequency calibration: oscillations at detuning frequency with accurate fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting detuning.

Options:
- Reliable: Clear oscillations with good fit
- Unreliable: No clear oscillations or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RAMSEY_T2STAR = """This is Ramsey T2* dephasing: decaying oscillations with fit that extracts T2*.

Assess whether the fit to the data in this plot <image> is reliable for extracting T2*.

Options:
- Reliable: Clear decaying oscillations with good fit
- Unreliable: No clear decay or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RES_SPEC = """This is resonator spectroscopy: sweep probe frequency to find resonance. A successful result has clear resonance feature.

Assess whether the data in this plot <image> shows a reliable resonance for extracting frequency.

Options:
- Reliable: Clear resonance with good contrast
- Unreliable: No clear resonance or very weak
- No resonance: No resonance feature visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RYDBERG_RAMSEY = """This is Rydberg Ramsey: oscillations on ground-to-Rydberg transition. Clear oscillations indicate good coherence.

Assess whether the data in this plot <image> is reliable for extracting T2 and detuning.

Options:
- Reliable: Clear oscillations with good contrast
- Unreliable: No clear oscillations or poor quality
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_RYDBERG_SPECTROSCOPY = """This is Rydberg spectroscopy: sweep detuning across sites. Clear spectral features with good fits indicate success.

Assess whether the fits to the data in this plot <image> are reliable for extracting transition frequencies.

Options:
- Reliable: Clear features with good fits
- Unreliable: No clear features or poor fits
- No fit: No fit visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_T1 = """This is T1 relaxation: measure population vs delay after excitation. A successful result shows clear exponential decay with good fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting T1.

Options:
- Reliable: Clear decay with good fit
- Unreliable: No clear decay or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_T1_FLUCTUATIONS = """This is T1 stability: T1 tracked over measurements. Stable values indicate good qubit stability.

Assess whether the data in this plot <image> is reliable for classifying T1 stability.

Options:
- Reliable: Clear trend (stable/fluctuating)
- Unreliable: No clear pattern or very noisy
- No data: No measurable T1

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>"""

PROMPT_TWEEZER_ARRAY = """This is optical tweezer array image: trapped atoms in regular grid. Sharp, uniform spots indicate proper aberration correction.

Assess whether the image <image> shows a reliable tweezer array for experiments.

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