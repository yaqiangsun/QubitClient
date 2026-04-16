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

PROMPT_COUPLER_FLUX = """What does this result <image> imply?

Explain:
- What the avoided crossing pattern indicates about coupler tuning
- Whether the crossing frequencies are in the desired range
- What calibration step follows (e.g., adjust coupling strength, proceed to gate calibration)

Provide your assessment."""

PROMPT_CZ_BENCHMARKING = """What does this result <image> imply?

Explain:
- What the decay rate indicates about gate fidelity
- Whether the polarization is sufficient for entangling operations
- What calibration step follows (e.g., optimize pulse timing, adjust atom positions)

Provide your assessment."""

PROMPT_DRAG = """What does this result <image> imply?

Explain:
- What the zero-crossing position and slope indicate about DRAG coefficient optimality and leakage suppression
- Whether the sweep range captures the crossing with sufficient resolution for reliable extraction
- What calibration step follows (e.g., narrowing the sweep around the crossing, or proceeding to gate benchmarking)

Provide your assessment."""

PROMPT_GMM = """What does this result <image> imply?

Explain:
- What the cluster separation indicates about readout fidelity
- Whether the state discrimination is sufficient for quantum error correction
- What calibration step follows (e.g., adjust readout amplitude, optimize integration time)

Provide your assessment."""

PROMPT_MICROWAVE_RAMSEY = """What does this result <image> imply?

Explain:
- What the oscillation frequency and contrast indicate about qubit coherence
- Whether the T2* is sufficient for gate operations
- What calibration step follows (e.g., improve coherence, adjust drive frequency)

Provide your assessment."""

PROMPT_MOT_LOADING = """What does this result <image> imply?

Explain:
- What the cloud characteristics indicate about loading efficiency
- Whether the atom number is sufficient for experiments
- What calibration step follows (e.g., adjust MOT parameters, proceed to trapping)

Provide your assessment."""

PROMPT_PINCHOFF = """What does this result <image> imply?

Explain:
- What the current-voltage relationship indicates about device pinch-off
- Whether the device is suitable for electron transport experiments
- What calibration step follows (e.g., adjust gate voltages, optimize device design)

Provide your assessment."""

PROMPT_PINGPONG = """What does this result <image> imply?

Explain:
- What the error accumulation rate indicates about gate fidelity
- Whether the gates are sufficient for deep circuits
- What calibration step follows (e.g., optimize pulse amplitude, adjust spacing)

Provide your assessment."""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """What does this result <image> imply?

Explain:
- What the dispersion curve shape indicates about qubit nonlinearity
- Whether the qubit is properly tunable in the desired frequency range
- What calibration step follows (e.g., set operating point, proceed to spectroscopy)

Provide your assessment."""

PROMPT_QUBIT_SPECTROSCOPY = """What does this result <image> imply?

Explain:
- What the peak position indicates about qubit frequency
- Whether the linewidth is sufficient for reliable operations
- What calibration step follows (e.g., set drive frequency, proceed to Rabi)

Provide your assessment."""

PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """What does this result <image> imply?

Explain:
- What the transition lines indicate about qubit energy levels
- Whether the power dependence is as expected
- What calibration step follows (e.g., set operating power, proceed to further calibration)

Provide your assessment."""

PROMPT_RABI = """What does this result <image> imply?

Explain:
- What the oscillation visibility indicates about drive efficiency
- Whether the pi-pulse amplitude is in the correct range
- What calibration step follows (e.g., set pi-pulse amplitude, proceed to Ramsey)

Provide your assessment."""

PROMPT_RABI_HW = """What does this result <image> imply?

Explain:
- What the Rabi frequency indicates about drive strength
- Whether the hardware is operating correctly
- What calibration step follows (e.g., verify hardware settings, proceed)

Provide your assessment."""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """What does this result <image> imply?

Explain:
- What the fringe pattern indicates about charge stability
- Whether charge jumps are present and their frequency
- What calibration step follows (e.g., investigate charge noise, wait for stabilization)

Provide your assessment."""

PROMPT_RAMSEY_FREQ_CAL = """What does this result <image> imply?

Explain:
- What the detuning frequency indicates about qubit frequency accuracy
- Whether the frequency is properly set for operations
- What calibration step follows (e.g., adjust qubit frequency, proceed to gates)

Provide your assessment."""

PROMPT_RAMSEY_T2STAR = """What does this result <image> imply?

Explain:
- What the T2* value indicates about qubit coherence
- Whether the coherence is sufficient for desired gate fidelities
- What calibration step follows (e.g., improve coherence, adjust operating point)

Provide your assessment."""

PROMPT_RES_SPEC = """What does this result <image> imply?

Explain:
- What the resonance frequency indicates about resonator properties
- Whether the coupling is as designed
- What calibration step follows (e.g., set probe frequency, proceed to qubit spectroscopy)

Provide your assessment."""

PROMPT_RYDBERG_RAMSEY = """What does this result <image> imply?

Explain:
- What the coherence time indicates about Rydberg excitation quality
- Whether the detuning is properly set
- What calibration step follows (e.g., adjust parameters, proceed to gates)

Provide your assessment."""

PROMPT_RYDBERG_SPECTROSCOPY = """What does this result <image> imply?

Explain:
- What the spectral features indicate about Rydberg level positions
- Whether all sites show consistent behavior
- What calibration step follows (e.g., set detuning, proceed to experiments)

Provide your assessment."""

PROMPT_T1 = """What does this result <image> imply?

Explain:
- What the T1 value indicates about qubit relaxation
- Whether the T1 is sufficient for desired operations
- What calibration step follows (e.g., improve T1, proceed to further experiments)

Provide your assessment."""

PROMPT_T1_FLUCTUATIONS = """What does this result <image> imply?

Explain:
- What the T1 stability indicates about qubit frequency noise
- Whether the fluctuations are acceptable for experiments
- What calibration step follows (e.g., investigate noise sources, wait for stabilization)

Provide your assessment."""

PROMPT_TWEEZER_ARRAY = """What does this result <image> imply?

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