# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
Q3: 科学推理任务

分析实验结果的物理含义并给出下一步建议
"""

# ========== 独立 Prompt 字符串定义 ==========

PROMPT_COUPLER_FLUX = """This is tunable coupler spectroscopy: we map the coupler's frequency response vs applied flux bias. A successful result shows a clear coupler dispersion curve with a good fit.

What does this result <image> imply?

Explain:
- What the avoided crossing pattern indicates about coupler tuning
- Whether the crossing frequencies are in the desired range
- What calibration step follows (e.g., adjust coupling strength, proceed to gate calibration)

Provide your assessment."""

PROMPT_CZ_BENCHMARKING = """This is CZ (controlled-Z) gate benchmarking on pairs of neutral atoms. It measures atom retention probability and cycle polarization as a function of circuit depth. A successful result shows both retention and polarization close to 1 with gradual decay.

What does this result <image> imply?

Explain:
- What the decay rate indicates about gate fidelity
- Whether the polarization is sufficient for entangling operations
- What calibration step follows (e.g., optimize pulse timing, adjust atom positions)

Provide your assessment."""

PROMPT_DRAG = """This is a DRAG calibration: we sweep 1/alpha to find the optimal value that minimizes leakage. A successful result has the zero-crossing of fitted curves clearly observable in the sweep window.

What does this result <image> imply?

Explain:
- What the zero-crossing position and slope indicate about DRAG coefficient optimality and leakage suppression
- Whether the sweep range captures the crossing with sufficient resolution for reliable extraction
- What calibration step follows (e.g., narrowing the sweep around the crossing, or proceeding to gate benchmarking)

Provide your assessment."""

PROMPT_GMM = """This is a single-shot readout discrimination experiment: the I-Q scatter plot shows measurement results for |0⟩ and |1⟩ states fitted with a Gaussian Mixture Model. A successful result has two well-separated clusters.

What does this result <image> imply?

Explain:
- What the cluster separation indicates about readout fidelity
- Whether the state discrimination is sufficient for quantum error correction
- What calibration step follows (e.g., adjust readout amplitude, optimize integration time)

Provide your assessment."""

PROMPT_MICROWAVE_RAMSEY = """This is a Ramsey experiment on the ground-state clock qubit using microwave pulses. A successful result shows sinusoidal oscillations with contrast close to 1 and data well-fit by the curve.

What does this result <image> imply?

Explain:
- What the oscillation frequency and contrast indicate about qubit coherence
- Whether the T2* is sufficient for gate operations
- What calibration step follows (e.g., improve coherence, adjust drive frequency)

Provide your assessment."""

PROMPT_MOT_LOADING = """This is a MOT (magneto-optical trap) loading image: a camera captures the fluorescence of trapped atoms. A successful result shows a well-defined, compact atomic cloud in the view.

What does this result <image> imply?

Explain:
- What the cloud characteristics indicate about loading efficiency
- Whether the atom number is sufficient for experiments
- What calibration step follows (e.g., adjust MOT parameters, proceed to trapping)

Provide your assessment."""

PROMPT_PINCHOFF = """This is an electron-on-helium pinch-off measurement: a 1D current trace is measured as a function of gate voltage. The measurement determines whether the device has pinched off.

What does this result <image> imply?

Explain:
- What the current-voltage relationship indicates about device pinch-off
- Whether the device is suitable for electron transport experiments
- What calibration step follows (e.g., adjust gate voltages, optimize device design)

Provide your assessment."""

PROMPT_PINGPONG = """This is a PingPong amplitude calibration: repeated pi-pulse pairs are applied and qubit population is measured vs gate count. A successful result shows error accumulation that can be fitted linearly.

What does this result <image> imply?

Explain:
- What the error accumulation rate indicates about gate fidelity
- Whether the gates are sufficient for deep circuits
- What calibration step follows (e.g., optimize pulse amplitude, adjust spacing)

Provide your assessment."""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """This is flux-dependent qubit spectroscopy: a 2D map of qubit transition frequency vs applied flux bias. A successful result shows a clear dispersion curve with a good fit.

What does this result <image> imply?

Explain:
- What the dispersion curve shape indicates about qubit nonlinearity
- Whether the qubit is properly tunable in the desired frequency range
- What calibration step follows (e.g., set operating point, proceed to spectroscopy)

Provide your assessment."""

PROMPT_QUBIT_SPECTROSCOPY = """This is a qubit spectroscopy experiment: we sweep drive frequency to find the qubit transition. A successful result has a single clear spectral peak with a good Lorentzian fit.

What does this result <image> imply?

Explain:
- What the peak position indicates about qubit frequency
- Whether the linewidth is sufficient for reliable operations
- What calibration step follows (e.g., set drive frequency, proceed to Rabi)

Provide your assessment."""

PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """This is a 2D qubit spectroscopy experiment: we sweep both drive power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, optionally f02/2).

What does this result <image> imply?

Explain:
- What the transition lines indicate about qubit energy levels
- Whether the power dependence is as expected
- What calibration step follows (e.g., set operating power, proceed to further calibration)

Provide your assessment."""

PROMPT_RABI = """This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude where the qubit population inverts. A successful result shows clear sinusoidal oscillations with a fit.

What does this result <image> imply?

Explain:
- What the oscillation visibility indicates about drive efficiency
- Whether the pi-pulse amplitude is in the correct range
- What calibration step follows (e.g., set pi-pulse amplitude, proceed to Ramsey)

Provide your assessment."""

PROMPT_RABI_HW = """This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude. A successful result shows clear sinusoidal oscillations with a fit.

What does this result <image> imply?

Explain:
- What the Rabi frequency indicates about drive strength
- Whether the hardware is operating correctly
- What calibration step follows (e.g., verify hardware settings, proceed)

Provide your assessment."""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """This is a Ramsey charge tomography scan: repeated Ramsey measurements over time form a 2D map revealing charge jump events. A clean result shows continuous fringes.

What does this result <image> imply?

Explain:
- What the fringe pattern indicates about charge stability
- Whether charge jumps are present and their frequency
- What calibration step follows (e.g., investigate charge noise, wait for stabilization)

Provide your assessment."""

PROMPT_RAMSEY_FREQ_CAL = """This is a Ramsey frequency calibration: two π/2 pulses separated by variable delay measure frequency detuning. A successful result shows clear oscillations with accurate fit.

What does this result <image> imply?

Explain:
- What the detuning frequency indicates about qubit frequency accuracy
- Whether the frequency is properly set for operations
- What calibration step follows (e.g., adjust qubit frequency, proceed to gates)

Provide your assessment."""

PROMPT_RAMSEY_T2STAR = """This is a Ramsey T2* dephasing experiment: two π/2 pulses separated by variable delay measure the dephasing time T2*. A successful result shows decaying oscillations with accurate fit.

What does this result <image> imply?

Explain:
- What the T2* value indicates about qubit coherence
- Whether the coherence is sufficient for desired gate fidelities
- What calibration step follows (e.g., improve coherence, adjust operating point)

Provide your assessment."""

PROMPT_RES_SPEC = """This is a resonator spectroscopy: we sweep probe frequency to find the resonator resonance. A successful result has a clear resonance feature (dip or peak).

What does this result <image> imply?

Explain:
- What the resonance frequency indicates about resonator properties
- Whether the coupling is as designed
- What calibration step follows (e.g., set probe frequency, proceed to qubit spectroscopy)

Provide your assessment."""

PROMPT_RYDBERG_RAMSEY = """This is a Ramsey experiment on ground-to-Rydberg transition: two π/2 pulses separated by variable delay measure T2 and detuning. A successful result shows clear oscillations.

What does this result <image> imply?

Explain:
- What the coherence time indicates about Rydberg excitation quality
- Whether the detuning is properly set
- What calibration step follows (e.g., adjust parameters, proceed to gates)

Provide your assessment."""

PROMPT_RYDBERG_SPECTROSCOPY = """This is Rydberg spectroscopy: optical detuning swept across multiple atomic sites. A successful result shows clear spectral features with good fits.

What does this result <image> imply?

Explain:
- What the spectral features indicate about Rydberg level positions
- Whether all sites show consistent behavior
- What calibration step follows (e.g., set detuning, proceed to experiments)

Provide your assessment."""

PROMPT_T1 = """This is a T1 relaxation experiment: after exciting to |1⟩, we measure population vs delay time. A successful result shows clear exponential decay with good fit.

What does this result <image> imply?

Explain:
- What the T1 value indicates about qubit relaxation
- Whether the T1 is sufficient for desired operations
- What calibration step follows (e.g., improve T1, proceed to further experiments)

Provide your assessment."""

PROMPT_T1_FLUCTUATIONS = """This is a T1 stability measurement: T1 tracked over repeated measurements. A successful result shows stable T1 values with minimal drift.

What does this result <image> imply?

Explain:
- What the T1 stability indicates about qubit frequency noise
- Whether the fluctuations are acceptable for experiments
- What calibration step follows (e.g., investigate noise sources, wait for stabilization)

Provide your assessment."""

PROMPT_TWEEZER_ARRAY = """This is an optical tweezer array image: trapped atoms in a regular grid. A successful image shows sharp, uniform, well-separated spots.

What does this result <image> imply?

Explain:
- What the spot characteristics indicate about trapping quality
- Whether the array is suitable for quantum experiments
- What calibration step follows (e.g., adjust trap powers, proceed to experiments)

Provide your assessment."""


# ========== Prompt 字典映射 ==========

SCIENTIFIC_REASONING_PROMPTS = {
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


def get_scientific_reasoning_prompt(experiment_family: str) -> str:
    """获取科学推理的专属 prompt"""
    return SCIENTIFIC_REASONING_PROMPTS.get(experiment_family, SCIENTIFIC_REASONING_PROMPTS["rabi"])


__all__ = [
    "SCIENTIFIC_REASONING_PROMPTS",
    "get_scientific_reasoning_prompt",
]