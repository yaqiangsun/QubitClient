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

PROMPT_COUPLER_FLUX = """What does this result imply?

Explain:
- What the dispersion curve shape reveals about coupler tunability range and coupling strength
- Whether the flux range captures enough of the dispersion for reliable parameter extraction
- What next step follows (e.g., setting coupler bias point, calibrating two-qubit gate interaction)

Provide your assessment."""

PROMPT_CZ_BENCHMARKING = """What does this result <image> imply?

Explain:
- What the retention decay rate and polarization decay rate indicate about gate fidelity, atom loss per gate, and overall gate quality
- Whether the circuit depth range spans enough decay to extract meaningful fidelity metrics from both retention and polarization
- What adjustment follows (e.g., recalibrating the CZ gate, adjusting circuit depth range, or investigating atom loss mechanisms)

Provide your assessment."""

PROMPT_DRAG = """What does this result <image> imply?

Explain:
- What the zero-crossing position and slope indicate about DRAG coefficient optimality and leakage suppression
- Whether the sweep range captures the crossing with sufficient resolution for reliable extraction
- What calibration step follows (e.g., narrowing the sweep around the crossing, or proceeding to gate benchmarking)

Provide your assessment."""

PROMPT_GMM = """What does this result <image> imply?

Explain:
- What the cluster separation, shape, and overlap indicate about readout fidelity and SNR
- Whether the discrimination is sufficient for reliable single-shot state assignment
- What adjustment follows (e.g., optimizing readout power, frequency, or integration time)

Provide your assessment."""

PROMPT_MICROWAVE_RAMSEY = """What does this result <image> imply?

Explain:
- What the oscillation contrast, retention level, and fit quality indicate about qubit coherence and microwave drive calibration
- Whether the contrast and retention are sufficient for reliable state discrimination and parameter extraction
- What adjustment follows (e.g., tuning microwave frequency closer to resonance, investigating system retention issues, or proceeding with current calibration)

Provide your assessment."""

PROMPT_MOT_LOADING = """What does this MOT loading result <image> indicate about the trap performance?

Explain:
- What the cloud morphology (size, symmetry, brightness) indicates about trap alignment and atom number
- Whether the image quality and SNR are sufficient for reliable cloud characterization
- What trap parameter adjustment follows (e.g., beam alignment, magnetic gradient tuning, or laser detuning)

Provide your assessment."""

PROMPT_PINCHOFF = """What does this result <image> imply?

Explain:
- What the transition shape (steepness, completeness, residual current) indicates about channel depletion and device quality
- Whether the gate voltage range captures the full pinch-off transition for reliable threshold extraction
- What adjustment follows (e.g., extending voltage range, checking device polarity, investigating leakage paths)

Provide your assessment."""

PROMPT_PINGPONG = """What does this result <image> imply?

Explain:
- What the slope and oscillation pattern indicate about pi-pulse amplitude error magnitude and direction
- Whether the gate count range is sufficient to distinguish calibration quality from noise
- What pulse amplitude adjustment follows based on the observed error accumulation trend

Provide your assessment."""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """What does this result imply?

Explain:
- What the dispersion curve shape reveals about qubit sweet spot location, Ej/Ec ratio, and flux tunability
- Whether the flux and frequency ranges capture enough of the dispersion for reliable parameter extraction
- What next step follows (e.g., biasing to sweet spot, extending flux range, refining fit model)

Provide your assessment."""

PROMPT_QUBIT_SPECTROSCOPY = """What does this result imply?

Explain:
- What the peak position, linewidth, and shape indicate about qubit frequency and coherence
- Whether the frequency span and resolution are sufficient for unambiguous transition identification
- What next step follows (e.g., narrowing scan around peak, proceeding to Rabi or Ramsey calibration)

Provide your assessment."""

PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """This is a 2D qubit spectroscopy experiment on a standard transmon (negative anharmonicity, so f02/2 appears at a lower frequency than f01): we sweep both drive power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, and optionally f02/2) with visible power dependence.

What do these results <image>, <image> and <image> imply?

Explain:
- What the transition line structure reveals about qubit anharmonicity and drive power coupling
- Whether the frequency and power ranges are sufficient to identify all relevant transitions
- What parameter adjustment (power range, frequency window) or next step (single-tone spectroscopy, Rabi) follows

Provide your assessment."""

PROMPT_RABI = """What does this result <image> imply?

Explain:
- What the oscillation pattern indicates about drive coupling strength and pi-pulse amplitude
- Whether the amplitude range and sampling are sufficient for reliable Rabi rate extraction
- What calibration step follows (e.g., adjusting drive amplitude, extending sweep range, or proceeding to DRAG calibration)

Provide your assessment."""

PROMPT_RABI_HW = """What does this result imply?

Explain:
- What the oscillation pattern indicates about drive coupling strength and pi-pulse amplitude
- Whether the amplitude range and sampling are sufficient for reliable Rabi rate extraction
- What calibration step follows (e.g., adjusting drive amplitude, extending sweep range, or proceeding to DRAG calibration)

Provide your assessment."""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """What does this Ramsey charge tomography result <image> imply for qubit operation?

Explain:
- What the fringe continuity and disruption pattern indicate about the charge noise environment
- Whether the scan duration and resolution are sufficient to characterize charge jump frequency and severity
- What device or environment adjustment follows (e.g., improving filtering, relocating qubit operating point, extending monitoring)

Provide your assessment."""

PROMPT_RAMSEY_FREQ_CAL = """What do these results <image> and <image> imply?

Explain:
- What the oscillation pattern indicates about the qubit's detuning and coherence
- Whether the measurement is sufficient for reliable parameter extraction
- What parameter adjustment or next calibration step follows

Provide your assessment."""

PROMPT_RAMSEY_T2STAR = """What do these results <image> and <image> imply?

Explain:
- What the oscillation pattern indicates about the qubit's detuning and coherence
- Whether the measurement is sufficient for reliable parameter extraction
- What parameter adjustment or next calibration step follows

Provide your assessment."""

PROMPT_RES_SPEC = """What does this result <image> imply?

Explain:
- What the resonance lineshape (depth, width, symmetry) indicates about internal and coupling quality factors
- Whether the frequency span and resolution are sufficient for reliable resonance frequency extraction
- What next step follows (e.g., adjusting frequency window, proceeding to qubit spectroscopy)

Provide your assessment."""

PROMPT_RYDBERG_RAMSEY = """What does this result <image> imply?

Explain:
- What the oscillation frequency, amplitude decay rate, and fit quality (RChi2) indicate about qubit coherence and frequency noise
- Whether the data clusters across all time windows are consistently described by a single fit, or if the fit diverges from later clusters
- What calibration step follows (e.g., adjusting Rydberg laser parameters, adding more time windows, or proceeding to gate sequences)

Provide your assessment."""

PROMPT_RYDBERG_SPECTROSCOPY = """What does this result <image> imply?

Explain:
- What the spectral line shapes, fit quality (chi-squared), and contrast indicate about the Rydberg transition coupling and laser stability
- Whether the spectroscopy resolution and signal-to-noise ratio are sufficient for reliable frequency and Rabi frequency extraction across sites
- What calibration step follows (e.g., adjusting laser power or alignment, investigating noisy sites, or proceeding to Rydberg gate calibration)

Provide your assessment."""

PROMPT_T1 = """What does this result <image> imply?

Explain:
- What the decay rate and residual population indicate about qubit relaxation time and thermal population
- Whether the time window and sampling capture enough of the decay for reliable T1 extraction
- What next step follows (e.g., extending delay range, improving thermalization, proceeding to T2 measurement)

Provide your assessment."""

PROMPT_T1_FLUCTUATIONS = """What does this result <image> imply?

Explain:
- What the T1 time series pattern (stability, switching, drift) indicates about the dominant decoherence mechanism
- Whether the monitoring duration and sampling rate are sufficient to characterize the fluctuation type
- What mitigation strategy follows (e.g., TLS avoidance, thermal stabilization, or frequency tuning)

Provide your assessment."""

PROMPT_TWEEZER_ARRAY = """What does this result <image> imply?

Explain:
- What the spot uniformity, sharpness, and grid regularity indicate about the optical system alignment and aberration correction quality
- Whether the array fill factor and spot quality are sufficient for reliable atom trapping across all sites
- What adjustment follows (e.g., re-running aberration correction, adjusting trap power, or proceeding to atom loading)

Provide your assessment."""

# ========== Not in QCalEval ==========

PROMPT_S21 = """What does this result <image> imply?

Explain:
- What the S21 transmission lineshape (dip depth, width, symmetry) indicates about cavity resonance quality and signal strength
- Whether the frequency span and resolution are sufficient for reliable resonance frequency extraction
- What next step follows (e.g., proceeding to qubit spectroscopy, adjusting frequency window, or performing further cavity characterization)

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
    # ========== Not in QCalEval ==========
    "s21": PROMPT_S21,
}


def get_scientific_reasoning_prompt(experiment_family: str) -> str:
    """获取科学推理的专属 prompt"""
    return SCIENTIFIC_REASONING_PROMPTS.get(experiment_family, SCIENTIFIC_REASONING_PROMPTS["rabi"])


__all__ = [
    "SCIENTIFIC_REASONING_PROMPTS",
    "get_scientific_reasoning_prompt",
]