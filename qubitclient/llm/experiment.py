# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/16 13:23:17
########################################################################

"""
QCalEval 实验配置模块

本模块包含 QCalEval VLM 任务的 Prompt 和 Response Schema:
- Prompt: 22 家族 × 6 任务 = 132 个专属 prompt
- Schema: 6 个任务的 Response Schema + Q5 参数提取 Schema (22个)
- 获取函数: 便捷的 prompt/schema 获取方法
"""

# ========== 专属 Prompt 模板 (22 家族 × 6 任务) ==========

# Q1: 描述图表 - 每个家族关注不同的图表特征
DESCRIBE_PLOT_PROMPTS = {
    "coupler_flux": """Describe the coupler flux spectroscopy figure <image> in JSON format.

This experiment maps the coupler's frequency response vs applied flux bias.
Focus on: avoided crossing pattern, dispersion curve shape, fit quality.

Required fields:
{
  "plot_type": "scatter" | "line" | "heatmap",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "main_features": string
}""",
    "cz_benchmarking": """Describe the CZ benchmarking figure <image> in JSON format.

This experiment measures atom retention probability and cycle polarization vs circuit depth.
Focus on: decay rate, polarization values, circuit depth range.

Required fields:
{
  "plot_type": "scatter" | "line",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "main_features": string
}""",
    "drag": """Describe the DRAG calibration figure <image> in JSON format.

This experiment sweeps 1/alpha to find the optimal DRAG coefficient.
Focus on: zero-crossing position, two datasets with opposite slopes, fit lines.

Required fields:
{
  "plot_type": "scatter" | "line",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "main_features": string
}""",
    "gmm": """Describe the GMM (Gaussian Mixture Model) discrimination figure <image> in JSON format.

This experiment shows I-Q scatter plot for |0⟩ and |1⟩ states with GMM fit.
Focus on: two clusters, separation, overlap, cluster centers.

Required fields:
{
  "plot_type": "scatter",
  "x_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "microwave_ramsey": """Describe the microwave Ramsey figure <image> in JSON format.

This experiment uses microwave pulses to measure Ramsey oscillations.
Focus on: oscillation frequency, contrast, decay envelope.

Required fields:
{
  "plot_type": "scatter" | "line",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "mot_loading": """Describe the MOT loading image <image> in JSON format.

This is a camera image showing trapped atoms in a magneto-optical trap.
Focus on: cloud shape, position, brightness, uniformity.

Required fields:
{
  "plot_type": "heatmap" | "image",
  "x_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "pinchoff": """Describe the pinch-off measurement figure <image> in JSON format.

This measures 1D current trace vs gate voltage to determine device pinch-off.
Focus on: saturation region, transition region, pinch-off point.

Required fields:
{
  "plot_type": "line" | "scatter",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "main_features": string
}""",
    "pingpong": """Describe the PingPong calibration figure <image> in JSON format.

This applies repeated pi-pulse pairs and measures qubit population vs gate count.
Focus on: error accumulation pattern, linear vs oscillatory behavior.

Required fields:
{
  "plot_type": "scatter" | "line",
  "x_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "qubit_flux_spectroscopy": """Describe the qubit flux spectroscopy 2D map <image> in JSON format.

This maps qubit transition frequency vs applied flux bias.
Focus on: dispersion curve (arc/parabola), resonance peaks, fit overlay.

Required fields:
{
  "plot_type": "heatmap" | "scatter",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "main_features": string
}""",
    "qubit_spectroscopy": """Describe the qubit spectroscopy figure <image> in JSON format.

This sweeps drive frequency to find the qubit transition.
Focus on: spectral peak, Lorentzian fit, peak position.

Required fields:
{
  "plot_type": "scatter" | "line",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "qubit_spectroscopy_power_frequency": """Describe the 2D qubit spectroscopy figure <image> in JSON format.

This sweeps both drive power and frequency to map qubit transitions.
Focus on: f01 line, f02/2 line, power dependence, visibility.

Required fields:
{
  "plot_type": "heatmap",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "main_features": string
}""",
    "rabi": """Describe the Rabi oscillation figure <image> in JSON format.

This sweeps pulse amplitude to find the pi-pulse amplitude.
Focus on: sinusoidal oscillations, oscillation visibility, fit quality.

Required fields:
{
  "plot_type": "scatter" | "line",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "rabi_hw": """Describe the Rabi (hardware) figure <image> in JSON format.

This sweeps pulse amplitude to find the pi-pulse amplitude with hardware characterization.
Focus on: oscillation amplitude, periodicity, fit reliability.

Required fields:
{
  "plot_type": "scatter" | "line",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "ramsey_charge_tomography": """Describe the Ramsey charge tomography 2D map <image> in JSON format.

This shows repeated Ramsey measurements over time revealing charge jumps.
Focus on: fringe continuity, jump events, noise level.

Required fields:
{
  "plot_type": "heatmap",
  "x_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "ramsey_freq_cal": """Describe the Ramsey frequency calibration figure <image> in JSON format.

This measures frequency detuning with two π/2 pulses separated by variable delay.
Focus on: oscillation visibility, detuning frequency, fit quality.

Required fields:
{
  "plot_type": "scatter" | "line",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "ramsey_t2star": """Describe the Ramsey T2* figure <image> in JSON format.

This measures dephasing time with two π/2 pulses at variable delay.
Focus on: decaying oscillations, T2* value, FFT peak.

Required fields:
{
  "plot_type": "scatter" | "line",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "res_spec": """Describe the resonator spectroscopy figure <image> in JSON format.

This sweeps probe frequency to find the resonator resonance.
Focus on: resonance dip/peak, depth, width, baseline.

Required fields:
{
  "plot_type": "line" | "scatter",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "rydberg_ramsey": """Describe the Rydberg Ramsey figure <image> in JSON format.

This measures coherence on ground-to-Rydberg transition.
Focus on: oscillation visibility, T2 coherence, detuning.

Required fields:
{
  "plot_type": "scatter" | "line",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "rydberg_spectroscopy": """Describe the Rydberg spectroscopy figure <image> in JSON format.

This sweeps optical detuning across multiple atomic sites.
Focus on: spectral features, contrast, fit quality per site.

Required fields:
{
  "plot_type": "heatmap" | "line" | "scatter",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "main_features": string
}""",
    "t1": """Describe the T1 relaxation figure <image> in JSON format.

This measures qubit population vs delay time after excitation to |1⟩.
Focus on: exponential decay, decay visibility, fit quality.

Required fields:
{
  "plot_type": "scatter" | "line",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "t1_fluctuations": """Describe the T1 stability measurement figure <image> in JSON format.

This tracks T1 relaxation time over repeated measurements.
Focus on: stability, drift, jump events, classification.

Required fields:
{
  "plot_type": "line" | "scatter",
  "x_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
    "tweezer_array": """Describe the optical tweezer array image <image> in JSON format.

This is a camera image showing trapped atoms in a regular grid.
Focus on: spot uniformity, grid regularity, aberration.

Required fields:
{
  "plot_type": "heatmap" | "image",
  "x_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear", "range": [min, max]},
  "main_features": string
}""",
}


# Q2: 分类实验结果 - 每个家族有不同的关注点
CLASSIFY_OUTCOME_PROMPTS = {
    "coupler_flux": """This is tunable coupler spectroscopy: we map the coupler's frequency response vs applied flux bias. A successful result shows a clear coupler dispersion curve with a good fit.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear avoided crossing with good fit, crossing within range
- Suboptimal parameters: Crossings visible but fit quality poor or crossing near edge
- Anomalous behavior: Multiple crossings, asymmetric pattern, unexpected behavior
- Apparatus issue: No clear crossing pattern, flat/noisy data

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "cz_benchmarking": """This is CZ (controlled-Z) gate benchmarking on pairs of neutral atoms. It measures atom retention probability and cycle polarization as a function of circuit depth. A successful result shows both retention and polarization close to 1 with gradual decay.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: High retention (>0.9) and polarization, clear decay with depth
- Suboptimal parameters: Moderate values, faster than expected decay
- Anomalous behavior: Unexpected oscillations, polarization loss, irregular decay
- Apparatus issue: No decay pattern, random data, measurement error

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "drag": """This is a DRAG calibration: we sweep 1/alpha to find the optimal value that minimizes leakage. A successful result has the zero-crossing of fitted curves clearly observable in the sweep window.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear zero-crossing within sweep window, good linear fits
- Suboptimal parameters: Crossing visible but near edge of range, or limited data
- Anomalous behavior: Wrong crossing direction, asymmetric slopes, unexpected pattern
- Apparatus issue: No clear crossing, flat/noisy data, no signal response

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "gmm": """This is a single-shot readout discrimination experiment: the I-Q scatter plot shows measurement results for |0⟩ and |1⟩ states fitted with a Gaussian Mixture Model. A successful result has two well-separated clusters.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Two well-separated clusters, clear discrimination
- Suboptimal parameters: Clusters touching or partially overlapping, moderate separation
- Anomalous behavior: Single blob, clusters in wrong positions, unexpected distribution
- Apparatus issue: No clusters visible, random scatter, measurement error

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "microwave_ramsey": """This is a Ramsey experiment on the ground-state clock qubit using microwave pulses. A successful result shows sinusoidal oscillations with contrast close to 1 and data well-fit by the curve.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations with high contrast, good fit
- Suboptimal parameters: Low contrast, fast decay, limited oscillations visible
- Anomalous behavior: Unexpected frequency, irregular pattern, drift
- Apparatus issue: No oscillations, flat/noisy data, random scatter

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "mot_loading": """This is a MOT (magneto-optical trap) loading image: a camera captures the fluorescence of trapped atoms. A successful result shows a well-defined, compact atomic cloud in the view.

Based on what you observe in the image <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear, compact cloud with good brightness
- Suboptimal parameters: Cloud present but diffuse or offset
- Anomalous behavior: Multiple clouds, elongated shape, unexpected features
- Apparatus issue: No cloud visible, only background noise

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "pinchoff": """This is an electron-on-helium pinch-off measurement: a 1D current trace is measured as a function of gate voltage. The measurement determines whether the device has pinched off — transitioning from conducting to non-conducting state.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear pinch-off transition with identifiable regions
- Suboptimal parameters: Transition visible but noisy or incomplete
- Anomalous behavior: No clear transition, irregular behavior
- Apparatus issue: No measurable current, no transition, noise dominated

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "pingpong": """This is a PingPong amplitude calibration: repeated pi-pulse pairs are applied and qubit population is measured vs gate count. A successful result shows error accumulation that can be fitted linearly.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear linear error accumulation, good fit
- Suboptimal parameters: Some oscillation visible, moderate error rate
- Anomalous behavior: Oscillatory pattern, irregular accumulation
- Apparatus issue: No clear pattern, random scatter, no response

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "qubit_flux_spectroscopy": """This is flux-dependent qubit spectroscopy: a 2D map of qubit transition frequency vs applied flux bias. A successful result shows a clear dispersion curve (arc or parabola) with a good fit overlaid.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear dispersion curve with good fit, in range
- Suboptimal parameters: Curve visible but noisy or fit poor
- Anomalous behavior: Multiple curves, unexpected features, asymmetric
- Apparatus issue: No clear curve, flat/noisy, no response

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "qubit_spectroscopy": """This is a qubit spectroscopy experiment: we sweep drive frequency to find the qubit transition. A successful result has a single clear spectral peak with a good Lorentzian fit.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Single clear peak with good Lorentzian fit
- Suboptimal parameters: Peak visible but multiple peaks or poor fit
- Anomalous behavior: Multiple peaks, unexpected positions, asymmetric
- Apparatus issue: No peaks, flat/noisy, no signal

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "qubit_spectroscopy_power_frequency": """This is a 2D qubit spectroscopy experiment: we sweep both drive power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, and optionally f02/2) with visible power dependence.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear f01 line visible, optionally f02/2
- Suboptimal parameters: Weak f01, limited power range
- Anomalous behavior: Multiple lines, unexpected features
- Apparatus issue: No clear lines, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "rabi": """This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude where the qubit population inverts. A successful result shows clear sinusoidal oscillations with a fit that tracks the data closely.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations, good fit, visible inversion
- Suboptimal parameters: Oscillations visible but distorted or limited range
- Anomalous behavior: Wrong frequency, unexpected pattern, damping issues
- Apparatus issue: No oscillations, flat/noisy, no signal response

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "rabi_hw": """This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude where the qubit population inverts. A successful result shows clear sinusoidal oscillations with a fit that tracks the data closely.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations with good fit
- Suboptimal parameters: Limited amplitude range, moderate noise
- Anomalous behavior: Unexpected oscillations, distortion
- Apparatus issue: No oscillations, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "ramsey_charge_tomography": """This is a Ramsey charge tomography scan: repeated Ramsey measurements over time form a 2D map revealing charge jump events. A clean result shows continuous, undisturbed fringes.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clean fringes, no jumps visible
- Suboptimal parameters: Some noise, occasional small jumps
- Anomalous behavior: Multiple charge jumps, disrupted fringes
- Apparatus issue: No fringes, random noise, no pattern

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "ramsey_freq_cal": """This is a Ramsey frequency calibration experiment: two π/2 pulses separated by a variable delay measure frequency detuning. A successful result shows clear oscillations at the detuning frequency with a fit that accurately extracts the frequency offset.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations, clear detuning, good fit
- Suboptimal parameters: Limited oscillations, noisy data
- Anomalous behavior: Wrong frequency, unexpected pattern
- Apparatus issue: No oscillations, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "ramsey_t2star": """This is a Ramsey T2* dephasing experiment: two π/2 pulses separated by a variable delay measure the dephasing time T2*. A successful result shows decaying oscillations with a fit that accurately extracts T2*.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear decaying oscillations, good T2* fit
- Suboptimal parameters: Limited decay visible, noisy
- Anomalous behavior: Beating, unexpected features
- Apparatus issue: No oscillations, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "res_spec": """This is a resonator spectroscopy experiment: we sweep probe frequency to find the resonator resonance. A successful result has a clear resonance feature (dip or peak).

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear resonance dip/peak with good contrast
- Suboptimal parameters: Weak resonance, limited depth
- Anomalous behavior: Multiple features, unexpected positions
- Apparatus issue: No resonance, flat/noisy baseline

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "rydberg_ramsey": """This is a Ramsey experiment on the ground-to-Rydberg transition: two π/2 pulses separated by variable delay measure the coherence time (T2) and detuning frequency. A successful result shows clear oscillations.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear oscillations, good coherence
- Suboptimal parameters: Limited oscillations, fast decay
- Anomalous behavior: Unexpected frequency, irregular pattern
- Apparatus issue: No oscillations, flat/noisy

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "rydberg_spectroscopy": """This is Rydberg transition spectroscopy: optical detuning is swept across multiple atomic sites to locate the transition frequency. A successful result shows clear spectral features with good fits and high contrast across sites.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear spectral lines, good fits, high contrast
- Suboptimal parameters: Weak features, limited sites
- Anomalous behavior: Unexpected features, site variation
- Apparatus issue: No features, noise dominated

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "t1": """This is a T1 relaxation experiment: after exciting the qubit to |1⟩, we measure population vs delay time. A successful result shows a clear exponential decay from high to low population with a good fit.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Clear exponential decay, good fit, T1 in range
- Suboptimal parameters: Decay visible but noisy or limited range
- Anomalous behavior: Unexpected rise, non-exponential behavior
- Apparatus issue: No decay, flat/noisy, no signal

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "t1_fluctuations": """This is a T1 stability measurement: T1 relaxation time is tracked over repeated measurements. A successful result shows stable T1 values with minimal drift or jumps.

Based on what you observe in the data <image>, classify the experimental outcome.

Options:
- Expected behavior: Stable T1 values, minimal variation
- Suboptimal parameters: Moderate drift, occasional jumps
- Anomalous behavior: Random walk, telegraphic noise, large jumps
- Apparatus issue: No measurable T1, random scatter

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
    "tweezer_array": """This is a camera image of an optical tweezer array used to trap neutral atoms in a regular grid. A successful image shows sharp, uniform, well-separated spots indicating proper aberration correction.

Based on what you observe in the image <image>, classify the experimental outcome.

Options:
- Expected behavior: Sharp, uniform spots in regular grid
- Suboptimal parameters: Some spots visible but irregular
- Anomalous behavior: Aberrated spots, irregular grid
- Apparatus issue: No spots visible, only background

Provide your answer as:
Classification: <your choice>
Reason: <brief explanation>""",
}


def get_describe_plot_prompt(experiment_family: str) -> str:
    """获取描述图表的专属 prompt"""
    return DESCRIBE_PLOT_PROMPTS.get(experiment_family, DESCRIBE_PLOT_PROMPTS["rabi"])


def get_classify_outcome_prompt(experiment_family: str) -> str:
    """获取分类实验结果的专属 prompt"""
    return CLASSIFY_OUTCOME_PROMPTS.get(experiment_family, CLASSIFY_OUTCOME_PROMPTS["rabi"])


# Q3: 科学推理 - 每个家族问不同的问题
SCIENTIFIC_REASONING_PROMPTS = {
    "coupler_flux": """This is tunable coupler spectroscopy: we map the coupler's frequency response vs applied flux bias. A successful result shows a clear coupler dispersion curve with a good fit.

What does this result <image> imply?

Explain:
- What the avoided crossing pattern indicates about coupler tuning
- Whether the crossing frequencies are in the desired range
- What calibration step follows (e.g., adjust coupling strength, proceed to gate calibration)

Provide your assessment.""",
    "cz_benchmarking": """This is CZ (controlled-Z) gate benchmarking on pairs of neutral atoms. It measures atom retention probability and cycle polarization as a function of circuit depth. A successful result shows both retention and polarization close to 1 with gradual decay.

What does this result <image> imply?

Explain:
- What the decay rate indicates about gate fidelity
- Whether the polarization is sufficient for entangling operations
- What calibration step follows (e.g., optimize pulse timing, adjust atom positions)

Provide your assessment.""",
    "drag": """This is a DRAG calibration: we sweep 1/alpha to find the optimal value that minimizes leakage. A successful result has the zero-crossing of fitted curves clearly observable in the sweep window.

What does this result <image> imply?

Explain:
- What the zero-crossing position and slope indicate about DRAG coefficient optimality and leakage suppression
- Whether the sweep range captures the crossing with sufficient resolution for reliable extraction
- What calibration step follows (e.g., narrowing the sweep around the crossing, or proceeding to gate benchmarking)

Provide your assessment.""",
    "gmm": """This is a single-shot readout discrimination experiment: the I-Q scatter plot shows measurement results for |0⟩ and |1⟩ states fitted with a Gaussian Mixture Model. A successful result has two well-separated clusters.

What does this result <image> imply?

Explain:
- What the cluster separation indicates about readout fidelity
- Whether the state discrimination is sufficient for quantum error correction
- What calibration step follows (e.g., adjust readout amplitude, optimize integration time)

Provide your assessment.""",
    "microwave_ramsey": """This is a Ramsey experiment on the ground-state clock qubit using microwave pulses. A successful result shows sinusoidal oscillations with contrast close to 1 and data well-fit by the curve.

What does this result <image> imply?

Explain:
- What the oscillation frequency and contrast indicate about qubit coherence
- Whether the T2* is sufficient for gate operations
- What calibration step follows (e.g., improve coherence, adjust drive frequency)

Provide your assessment.""",
    "mot_loading": """This is a MOT (magneto-optical trap) loading image: a camera captures the fluorescence of trapped atoms. A successful result shows a well-defined, compact atomic cloud in the view.

What does this result <image> imply?

Explain:
- What the cloud characteristics indicate about loading efficiency
- Whether the atom number is sufficient for experiments
- What calibration step follows (e.g., adjust MOT parameters, proceed to trapping)

Provide your assessment.""",
    "pinchoff": """This is an electron-on-helium pinch-off measurement: a 1D current trace is measured as a function of gate voltage. The measurement determines whether the device has pinched off.

What does this result <image> imply?

Explain:
- What the current-voltage relationship indicates about device pinch-off
- Whether the device is suitable for electron transport experiments
- What calibration step follows (e.g., adjust gate voltages, optimize device design)

Provide your assessment.""",
    "pingpong": """This is a PingPong amplitude calibration: repeated pi-pulse pairs are applied and qubit population is measured vs gate count. A successful result shows error accumulation that can be fitted linearly.

What does this result <image> imply?

Explain:
- What the error accumulation rate indicates about gate fidelity
- Whether the gates are sufficient for deep circuits
- What calibration step follows (e.g., optimize pulse amplitude, adjust spacing)

Provide your assessment.""",
    "qubit_flux_spectroscopy": """This is flux-dependent qubit spectroscopy: a 2D map of qubit transition frequency vs applied flux bias. A successful result shows a clear dispersion curve with a good fit.

What does this result <image> imply?

Explain:
- What the dispersion curve shape indicates about qubit nonlinearity
- Whether the qubit is properly tunable in the desired frequency range
- What calibration step follows (e.g., set operating point, proceed to spectroscopy)

Provide your assessment.""",
    "qubit_spectroscopy": """This is a qubit spectroscopy experiment: we sweep drive frequency to find the qubit transition. A successful result has a single clear spectral peak with a good Lorentzian fit.

What does this result <image> imply?

Explain:
- What the peak position indicates about qubit frequency
- Whether the linewidth is sufficient for reliable operations
- What calibration step follows (e.g., set drive frequency, proceed to Rabi)

Provide your assessment.""",
    "qubit_spectroscopy_power_frequency": """This is a 2D qubit spectroscopy experiment: we sweep both drive power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, optionally f02/2).

What does this result <image> imply?

Explain:
- What the transition lines indicate about qubit energy levels
- Whether the power dependence is as expected
- What calibration step follows (e.g., set operating power, proceed to further calibration)

Provide your assessment.""",
    "rabi": """This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude where the qubit population inverts. A successful result shows clear sinusoidal oscillations with a fit.

What does this result <image> imply?

Explain:
- What the oscillation visibility indicates about drive efficiency
- Whether the pi-pulse amplitude is in the correct range
- What calibration step follows (e.g., set pi-pulse amplitude, proceed to Ramsey)

Provide your assessment.""",
    "rabi_hw": """This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude. A successful result shows clear sinusoidal oscillations with a fit.

What does this result <image> imply?

Explain:
- What the Rabi frequency indicates about drive strength
- Whether the hardware is operating correctly
- What calibration step follows (e.g., verify hardware settings, proceed)

Provide your assessment.""",
    "ramsey_charge_tomography": """This is a Ramsey charge tomography scan: repeated Ramsey measurements over time form a 2D map revealing charge jump events. A clean result shows continuous fringes.

What does this result <image> imply?

Explain:
- What the fringe pattern indicates about charge stability
- Whether charge jumps are present and their frequency
- What calibration step follows (e.g., investigate charge noise, wait for stabilization)

Provide your assessment.""",
    "ramsey_freq_cal": """This is a Ramsey frequency calibration: two π/2 pulses separated by variable delay measure frequency detuning. A successful result shows clear oscillations with accurate fit.

What does this result <image> imply?

Explain:
- What the detuning frequency indicates about qubit frequency accuracy
- Whether the frequency is properly set for operations
- What calibration step follows (e.g., adjust qubit frequency, proceed to gates)

Provide your assessment.""",
    "ramsey_t2star": """This is a Ramsey T2* dephasing experiment: two π/2 pulses separated by variable delay measure the dephasing time T2*. A successful result shows decaying oscillations with accurate fit.

What does this result <image> imply?

Explain:
- What the T2* value indicates about qubit coherence
- Whether the coherence is sufficient for desired gate fidelities
- What calibration step follows (e.g., improve coherence, adjust operating point)

Provide your assessment.""",
    "res_spec": """This is a resonator spectroscopy: we sweep probe frequency to find the resonator resonance. A successful result has a clear resonance feature (dip or peak).

What does this result <image> imply?

Explain:
- What the resonance frequency indicates about resonator properties
- Whether the coupling is as designed
- What calibration step follows (e.g., set probe frequency, proceed to qubit spectroscopy)

Provide your assessment.""",
    "rydberg_ramsey": """This is a Ramsey experiment on ground-to-Rydberg transition: two π/2 pulses separated by variable delay measure T2 and detuning. A successful result shows clear oscillations.

What does this result <image> imply?

Explain:
- What the coherence time indicates about Rydberg excitation quality
- Whether the detuning is properly set
- What calibration step follows (e.g., adjust parameters, proceed to gates)

Provide your assessment.""",
    "rydberg_spectroscopy": """This is Rydberg spectroscopy: optical detuning swept across multiple atomic sites. A successful result shows clear spectral features with good fits.

What does this result <image> imply?

Explain:
- What the spectral features indicate about Rydberg level positions
- Whether all sites show consistent behavior
- What calibration step follows (e.g., set detuning, proceed to experiments)

Provide your assessment.""",
    "t1": """This is a T1 relaxation experiment: after exciting to |1⟩, we measure population vs delay time. A successful result shows clear exponential decay with good fit.

What does this result <image> imply?

Explain:
- What the T1 value indicates about qubit relaxation
- Whether the T1 is sufficient for desired operations
- What calibration step follows (e.g., improve T1, proceed to further experiments)

Provide your assessment.""",
    "t1_fluctuations": """This is a T1 stability measurement: T1 tracked over repeated measurements. A successful result shows stable T1 values with minimal drift.

What does this result <image> imply?

Explain:
- What the T1 stability indicates about qubit frequency noise
- Whether the fluctuations are acceptable for experiments
- What calibration step follows (e.g., investigate noise sources, wait for stabilization)

Provide your assessment.""",
    "tweezer_array": """This is an optical tweezer array image: trapped atoms in a regular grid. A successful image shows sharp, uniform, well-separated spots.

What does this result <image> imply?

Explain:
- What the spot characteristics indicate about trapping quality
- Whether the array is suitable for quantum experiments
- What calibration step follows (e.g., adjust trap powers, proceed to experiments)

Provide your assessment.""",
}


# Q4: 评估拟合 - 每个家族有不同的可靠性标准
ASSESS_FIT_PROMPTS = {
    "coupler_flux": """This is tunable coupler spectroscopy: we map the coupler's frequency response vs applied flux bias. A successful result shows a clear coupler dispersion curve with a good fit.

Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable: Clear avoided crossing with good fit quality
- Unreliable: No clear pattern or poor fit quality
- No fit: No fit attempted or visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "cz_benchmarking": """This is CZ gate benchmarking: measures retention probability and cycle polarization vs circuit depth. A successful result shows retention and polarization close to 1 with gradual decay.

Assess whether the data in this plot <image> is reliable for gate fidelity assessment.

Options:
- Reliable: Clear decay pattern with high retention/polarization
- Unreliable: No clear pattern or unexpected behavior
- No fit: No clear trend visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "drag": """This is a DRAG calibration: we sweep 1/alpha to find the optimal value. A successful result has the zero-crossing clearly observable in the sweep window.

Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable: Clear crossing with good linear fits
- Unreliable: No clear crossing or poor fit quality
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "gmm": """This is GMM discrimination: I-Q scatter plot for |0⟩ and |1⟩ states with GMM fit. A successful result has two well-separated clusters.

Assess whether the GMM fit in this plot <image> is reliable for state discrimination.

Options:
- Reliable: Clear separation with good fit
- Unreliable: Overlapping clusters or poor fit
- No fit: No fit visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "microwave_ramsey": """This is a microwave Ramsey: sinusoidal oscillations with contrast close to 1 and good fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting frequency and contrast.

Options:
- Reliable: Clear oscillations with good fit
- Unreliable: No clear oscillations or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "mot_loading": """This is a MOT loading image: shows trapped atoms in a magneto-optical trap.

Assess whether the image <image> shows a reliable atomic cloud for experiments.

Options:
- Reliable: Clear, compact cloud visible
- Unreliable: Diffuse or unclear cloud
- No cloud: No cloud visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "pinchoff": """This is pinch-off measurement: current trace vs gate voltage to determine device pinch-off.

Assess whether the data in this plot <image> shows a reliable pinch-off transition.

Options:
- Reliable: Clear transition with identifiable regions
- Unreliable: No clear transition or noisy
- No transition: No pinch-off visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "pingpong": """This is PingPong calibration: error accumulation vs gate count. A successful result shows linear error accumulation.

Assess whether the fit to the data in this plot <image> is reliable for extracting error rate.

Options:
- Reliable: Clear linear accumulation with good fit
- Unreliable: No clear pattern or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "qubit_flux_spectroscopy": """This is flux-dependent qubit spectroscopy: 2D map of qubit frequency vs flux. A successful result shows clear dispersion curve with good fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting dispersion.

Options:
- Reliable: Clear curve with good fit
- Unreliable: No clear curve or poor fit
- No fit: No fit visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "qubit_spectroscopy": """This is qubit spectroscopy: sweep drive frequency to find qubit transition. A successful result has a single clear peak with good Lorentzian fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting frequency.

Options:
- Reliable: Clear peak with good Lorentzian fit
- Unreliable: No clear peak or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "qubit_spectroscopy_power_frequency": """This is 2D qubit spectroscopy: sweep power and frequency to map transitions. A successful result shows clear transition lines.

Assess whether the data in this plot <image> shows reliable transition lines.

Options:
- Reliable: Clear f01 line (and f02/2 if present)
- Unreliable: No clear lines or very weak
- No features: No transition features visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "rabi": """This is Rabi experiment: sweep pulse amplitude to find pi-pulse. A successful result shows clear oscillations with fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting pi-pulse amplitude.

Options:
- Reliable: Clear oscillations with good fit
- Unreliable: No clear oscillations or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "rabi_hw": """This is Rabi experiment with hardware characterization: clear oscillations with fit.

Assess whether the fit to the data in this plot <image> is reliable for parameter extraction.

Options:
- Reliable: Clear oscillations with good fit
- Unreliable: No clear oscillations or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "ramsey_charge_tomography": """This is Ramsey charge tomography: 2D map over time revealing charge jumps. Clean result shows continuous fringes.

Assess whether the data in this plot <image> shows reliable fringe pattern for charge analysis.

Options:
- Reliable: Clear fringes, no jumps
- Unreliable: Jumps present or very noisy
- No pattern: No clear fringe pattern

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "ramsey_freq_cal": """This is Ramsey frequency calibration: oscillations at detuning frequency with accurate fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting detuning.

Options:
- Reliable: Clear oscillations with good fit
- Unreliable: No clear oscillations or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "ramsey_t2star": """This is Ramsey T2* dephasing: decaying oscillations with fit that extracts T2*.

Assess whether the fit to the data in this plot <image> is reliable for extracting T2*.

Options:
- Reliable: Clear decaying oscillations with good fit
- Unreliable: No clear decay or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "res_spec": """This is resonator spectroscopy: sweep probe frequency to find resonance. A successful result has clear resonance feature.

Assess whether the data in this plot <image> shows a reliable resonance for extracting frequency.

Options:
- Reliable: Clear resonance with good contrast
- Unreliable: No clear resonance or very weak
- No resonance: No resonance feature visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "rydberg_ramsey": """This is Rydberg Ramsey: oscillations on ground-to-Rydberg transition. Clear oscillations indicate good coherence.

Assess whether the data in this plot <image> is reliable for extracting T2 and detuning.

Options:
- Reliable: Clear oscillations with good contrast
- Unreliable: No clear oscillations or poor quality
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "rydberg_spectroscopy": """This is Rydberg spectroscopy: sweep detuning across sites. Clear spectral features with good fits indicate success.

Assess whether the fits to the data in this plot <image> are reliable for extracting transition frequencies.

Options:
- Reliable: Clear features with good fits
- Unreliable: No clear features or poor fits
- No fit: No fit visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "t1": """This is T1 relaxation: measure population vs delay after excitation. A successful result shows clear exponential decay with good fit.

Assess whether the fit to the data in this plot <image> is reliable for extracting T1.

Options:
- Reliable: Clear decay with good fit
- Unreliable: No clear decay or poor fit
- No fit: No fit attempted

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "t1_fluctuations": """This is T1 stability: T1 tracked over measurements. Stable values indicate good qubit stability.

Assess whether the data in this plot <image> is reliable for classifying T1 stability.

Options:
- Reliable: Clear trend (stable/fluctuating)
- Unreliable: No clear pattern or very noisy
- No data: No measurable T1

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
    "tweezer_array": """This is optical tweezer array image: trapped atoms in regular grid. Sharp, uniform spots indicate proper aberration correction.

Assess whether the image <image> shows a reliable tweezer array for experiments.

Options:
- Reliable: Sharp, uniform spots in grid
- Unreliable: Irregular or non-uniform spots
- No spots: No spots visible

Provide your answer as:
Assessment: <your choice>
Reason: <brief explanation>""",
}


def get_scientific_reasoning_prompt(experiment_family: str) -> str:
    """获取科学推理的专属 prompt"""
    return SCIENTIFIC_REASONING_PROMPTS.get(experiment_family, SCIENTIFIC_REASONING_PROMPTS["rabi"])


def get_assess_fit_prompt(experiment_family: str) -> str:
    """获取评估拟合的专属 prompt"""
    return ASSESS_FIT_PROMPTS.get(experiment_family, ASSESS_FIT_PROMPTS["rabi"])


# Q5: 提取参数 - 每个家族提取不同的参数
EXTRACT_PARAMS_PROMPTS = {
    "coupler_flux": """This is tunable coupler spectroscopy: we map the coupler's frequency response vs applied flux bias. A successful result shows a clear coupler dispersion curve with a good fit.

Extract the following parameters from this coupler flux spectroscopy plot <image>.

Report in JSON format:
{{params_schema}}""",
    "cz_benchmarking": """This is CZ gate benchmarking: measures atom retention probability and cycle polarization vs circuit depth. A successful result shows retention and polarization close to 1 with gradual decay.

Extract the following parameters from this CZ benchmarking plot <image>.

Report in JSON format:
{{params_schema}}""",
    "drag": """This is a DRAG calibration: we sweep 1/alpha to find the optimal value that minimizes leakage. A successful result has the zero-crossing of fitted curves clearly observable in the sweep window.

Extract the following parameters from this DRAG calibration plot <image>.

Report in JSON format:
{{params_schema}}""",
    "gmm": """This is a GMM discrimination experiment: I-Q scatter plot for |0⟩ and |1⟩ states with GMM fit. A successful result has two well-separated clusters.

Extract the following parameters from this GMM plot <image>.

Report in JSON format:
{{params_schema}}""",
    "microwave_ramsey": """This is a microwave Ramsey experiment: sinusoidal oscillations with contrast close to 1 and good fit.

Extract the following parameters from this Ramsey plot <image>.

Report in JSON format:
{{params_schema}}""",
    "mot_loading": """This is a MOT loading image: shows trapped atoms in a magneto-optical trap. A successful result shows a well-defined, compact atomic cloud.

Extract the following parameters from this MOT image <image>.

Report in JSON format:
{{params_schema}}""",
    "pinchoff": """This is a pinch-off measurement: current trace vs gate voltage to determine device pinch-off.

Extract the following parameters from this pinch-off plot <image>.

Report in JSON format:
{{params_schema}}""",
    "pingpong": """This is PingPong calibration: repeated pi-pulse pairs measure qubit population vs gate count. A successful result shows linear error accumulation.

Extract the following parameters from this PingPong plot <image>.

Report in JSON format:
{{params_schema}}""",
    "qubit_flux_spectroscopy": """This is flux-dependent qubit spectroscopy: 2D map of qubit frequency vs flux. A successful result shows clear dispersion curve with good fit.

Extract the following parameters from this flux spectroscopy plot <image>.

Report in JSON format:
{{params_schema}}""",
    "qubit_spectroscopy": """This is qubit spectroscopy: sweep drive frequency to find qubit transition. A successful result has a single clear peak with good Lorentzian fit.

Extract the following parameters from this spectroscopy plot <image>.

Report in JSON format:
{{params_schema}}""",
    "qubit_spectroscopy_power_frequency": """This is 2D qubit spectroscopy: sweep power and frequency to map qubit transitions. A successful result shows clear transition lines.

Extract the following parameters from this 2D spectroscopy plot <image>.

Report in JSON format:
{{params_schema}}""",
    "rabi": """This is a Rabi experiment: sweep pulse amplitude to find pi-pulse amplitude where qubit population inverts. A successful result shows clear sinusoidal oscillations with fit.

Extract the following parameters from this Rabi plot <image>.

Report in JSON format:
{{params_schema}}""",
    "rabi_hw": """This is a Rabi experiment with hardware characterization: clear oscillations with fit.

Extract the following parameters from this Rabi HW plot <image>.

Report in JSON format:
{{params_schema}}""",
    "ramsey_charge_tomography": """This is Ramsey charge tomography: 2D map over time revealing charge jumps. Clean result shows continuous fringes.

Extract the following parameters from this charge tomography plot <image>.

Report in JSON format:
{{params_schema}}""",
    "ramsey_freq_cal": """This is Ramsey frequency calibration: oscillations at detuning frequency with accurate fit.

Extract the following parameters from this Ramsey freq cal plot <image>.

Report in JSON format:
{{params_schema}}""",
    "ramsey_t2star": """This is Ramsey T2* dephasing: decaying oscillations with fit that extracts T2*.

Extract the following parameters from this T2* plot <image>.

Report in JSON format:
{{params_schema}}""",
    "res_spec": """This is resonator spectroscopy: sweep probe frequency to find resonance. A successful result has clear resonance feature.

Extract the following parameters from this resonator spectroscopy plot <image>.

Report in JSON format:
{{params_schema}}""",
    "rydberg_ramsey": """This is Rydberg Ramsey: oscillations on ground-to-Rydberg transition with T2 and detuning.

Extract the following parameters from this Rydberg Ramsey plot <image>.

Report in JSON format:
{{params_schema}}""",
    "rydberg_spectroscopy": """This is Rydberg spectroscopy: sweep detuning across multiple sites. Clear spectral features with good fits.

Extract the following parameters from this Rydberg spectroscopy plot <image>.

Report in JSON format:
{{params_schema}}""",
    "t1": """This is T1 relaxation: measure population vs delay after excitation to |1⟩. A successful result shows clear exponential decay with good fit.

Extract the following parameters from this T1 plot <image>.

Report in JSON format:
{{params_schema}}""",
    "t1_fluctuations": """This is T1 stability measurement: T1 tracked over repeated measurements. Stable values indicate good qubit stability.

Extract the following parameters from this T1 stability plot <image>.

Report in JSON format:
{{params_schema}}""",
    "tweezer_array": """This is optical tweezer array image: trapped atoms in regular grid. Sharp, uniform spots indicate proper aberration correction.

Extract the following parameters from this tweezer array image <image>.

Report in JSON format:
{{params_schema}}""",
}


# Q6: 评估状态 - 每个家族有不同的成功/失败标准
EVALUATE_STATUS_PROMPTS = {
    "coupler_flux": """This is tunable coupler spectroscopy: we map the coupler's frequency response vs applied flux bias. A successful result shows a clear coupler dispersion curve with a good fit.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear avoided crossing with good fit within sweep range
- NO_SIGNAL: Flat or noisy data, no clear crossing pattern
- OPTIMAL_NOT_CENTERED: Crossing exists but near edge of range or fit poor

When the status is not SUCCESS, provide a SPECIFIC suggested flux range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "cz_benchmarking": """This is CZ gate benchmarking: measures atom retention probability and cycle polarization vs circuit depth. A successful result shows retention and polarization close to 1 with gradual decay.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: High retention (>0.9) and polarization, clear decay pattern
- NO_SIGNAL: Random data, no clear decay
- OPTIMAL_NOT_CENTERED: Moderate values but acceptable

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "drag": """This is a DRAG calibration: we sweep 1/alpha to find the optimal value that minimizes leakage. A successful result has the zero-crossing of fitted curves clearly observable in the sweep window.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Zero-crossing clearly observable in sweep window
- NO_SIGNAL: Flat or random, no crossing pattern
- OPTIMAL_NOT_CENTERED: Crossing exists but in first/last quarter or outside range

When the status is not SUCCESS, provide a SPECIFIC suggested 1/alpha range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min 1/alpha>, <max 1/alpha>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "gmm": """This is a GMM discrimination experiment: I-Q scatter plot for |0⟩ and |1⟩ states with GMM fit. A successful result has two well-separated clusters.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Two well-separated clusters clearly visible
- NO_SIGNAL: Single blob or random scatter, no discrimination possible
- OPTIMAL_NOT_CENTERED: Clusters touching or partially overlapping

When the status is not SUCCESS, provide a SPECIFIC suggested adjustment.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "microwave_ramsey": """This is a microwave Ramsey experiment: sinusoidal oscillations with contrast close to 1 and good fit.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations with high contrast (>0.8), good fit
- NO_SIGNAL: Flat or random, no oscillations
- OPTIMAL_NOT_CENTERED: Oscillations visible but low contrast or noisy

When the status is not SUCCESS, provide a SPECIFIC suggested delay range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "mot_loading": """This is a MOT loading image: shows trapped atoms in a magneto-optical trap. A successful result shows a well-defined, compact atomic cloud.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear, compact cloud with good brightness
- NO_SIGNAL: No cloud visible, only background
- OPTIMAL_NOT_CENTERED: Cloud present but diffuse or offset

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "pinchoff": """This is a pinch-off measurement: current trace vs gate voltage to determine device pinch-off.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear pinch-off transition with identifiable regions
- NO_SIGNAL: No measurable current or no transition
- OPTIMAL_NOT_CENTERED: Transition visible but noisy or incomplete

When the status is not SUCCESS, provide a SPECIFIC suggested voltage range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "pingpong": """This is PingPong calibration: repeated pi-pulse pairs measure qubit population vs gate count. A successful result shows linear error accumulation.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear linear error accumulation, good fit
- NO_SIGNAL: No clear pattern, random scatter
- OPTIMAL_NOT_CENTERED: Some pattern but irregular

When the status is not SUCCESS, provide a SPECIFIC suggested gate count range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "qubit_flux_spectroscopy": """This is flux-dependent qubit spectroscopy: 2D map of qubit frequency vs flux. A successful result shows clear dispersion curve with good fit.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear dispersion curve with good fit, in range
- NO_SIGNAL: Flat or noisy, no clear curve
- OPTIMAL_NOT_CENTERED: Curve visible but noisy or fit poor

When the status is not SUCCESS, provide a SPECIFIC suggested flux range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "qubit_spectroscopy": """This is qubit spectroscopy: sweep drive frequency to find qubit transition. A successful result has a single clear peak with good Lorentzian fit.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Single clear peak with good Lorentzian fit
- NO_SIGNAL: Flat or noisy, no peaks
- OPTIMAL_NOT_CENTERED: Multiple peaks or poor fit

When the status is not SUCCESS, provide a SPECIFIC suggested frequency range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "qubit_spectroscopy_power_frequency": """This is 2D qubit spectroscopy: sweep power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, optionally f02/2).

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear f01 line visible (and f02/2 if present)
- NO_SIGNAL: No clear lines, flat/noisy
- OPTIMAL_NOT_CENTERED: Weak features or limited range

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "rabi": """This is a Rabi experiment: sweep pulse amplitude to find pi-pulse. A successful result shows clear sinusoidal oscillations with fit.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations, good fit, visible inversion
- NO_SIGNAL: Flat or random, no oscillations
- OPTIMAL_NOT_CENTERED: Oscillations visible but distorted or limited

When the status is not SUCCESS, provide a SPECIFIC suggested amplitude range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "rabi_hw": """This is a Rabi experiment with hardware characterization: clear oscillations with fit.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations with good fit
- NO_SIGNAL: Flat or noisy, no oscillations
- OPTIMAL_NOT_CENTERED: Limited amplitude range

When the status is not SUCCESS, provide a SPECIFIC suggested amplitude range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "ramsey_charge_tomography": """This is Ramsey charge tomography: 2D map over time revealing charge jumps. Clean result shows continuous fringes.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clean fringes, no jumps visible
- NO_SIGNAL: No clear pattern, random noise
- OPTIMAL_NOT_CENTERED: Occasional small jumps or noise

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "ramsey_freq_cal": """This is Ramsey frequency calibration: oscillations at detuning frequency with accurate fit.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations, clear detuning, good fit
- NO_SIGNAL: Flat or noisy, no oscillations
- OPTIMAL_NOT_CENTERED: Limited oscillations, noisy

When the status is not SUCCESS, provide a SPECIFIC suggested delay range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "ramsey_t2star": """This is Ramsey T2* dephasing: decaying oscillations with fit that extracts T2*.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear decaying oscillations, good T2* fit
- NO_SIGNAL: Flat or noisy, no oscillations
- OPTIMAL_NOT_CENTERED: Limited decay visible, noisy

When the status is not SUCCESS, provide a SPECIFIC suggested delay range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "res_spec": """This is resonator spectroscopy: sweep probe frequency to find resonance. A successful result has clear resonance feature.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear resonance dip/peak with good contrast
- NO_SIGNAL: Flat baseline, no resonance
- OPTIMAL_NOT_CENTERED: Weak resonance, limited depth

When the status is not SUCCESS, provide a SPECIFIC suggested frequency range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "rydberg_ramsey": """This is Rydberg Ramsey: oscillations on ground-to-Rydberg transition with T2 and detuning.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear oscillations, good coherence
- NO_SIGNAL: Flat or noisy, no oscillations
- OPTIMAL_NOT_CENTERED: Limited oscillations, fast decay

When the status is not SUCCESS, provide a SPECIFIC suggested delay range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "rydberg_spectroscopy": """This is Rydberg spectroscopy: sweep detuning across multiple sites. Clear spectral features with good fits.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear spectral lines, good fits, high contrast
- NO_SIGNAL: No features, noise dominated
- OPTIMAL_NOT_CENTERED: Weak features, limited sites

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "t1": """This is T1 relaxation: measure population vs delay after excitation to |1⟩. A successful result shows clear exponential decay with good fit.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Clear exponential decay, good fit, T1 in reasonable range
- NO_SIGNAL: Flat or random, no decay pattern
- OPTIMAL_NOT_CENTERED: Decay visible but noisy or limited range

When the status is not SUCCESS, provide a SPECIFIC suggested delay range.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "t1_fluctuations": """This is T1 stability measurement: T1 tracked over repeated measurements. Stable values indicate good qubit stability.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Stable T1 values, minimal variation
- NO_SIGNAL: No measurable T1, random scatter
- OPTIMAL_NOT_CENTERED: Moderate drift or occasional jumps

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
    "tweezer_array": """This is optical tweezer array image: trapped atoms in regular grid. Sharp, uniform spots indicate proper aberration correction.

Evaluate the image <image> and determine the experiment status.

DECISION CRITERIA
- SUCCESS: Sharp, uniform spots in regular grid
- NO_SIGNAL: No spots visible, only background
- OPTIMAL_NOT_CENTERED: Some spots but irregular or non-uniform

When the status is not SUCCESS, provide a SPECIFIC suggestion.

The response MUST follow this exact format:

Status: <one of the listed statuses>
Suggested range: (<min>, <max>) (or "N/A" if SUCCESS)
Notes: <1-3 sentences explaining your reasoning>""",
}


# ========== 通用 Prompt 函数 ==========


def get_extract_params_prompt(experiment_family: str, params_schema: str | None = None) -> str:
    """获取提取参数的专属 prompt"""
    base_prompt = EXTRACT_PARAMS_PROMPTS.get(experiment_family, EXTRACT_PARAMS_PROMPTS["rabi"])
    schema = params_schema or '{"optimal_value": float, "note": string}'
    return base_prompt.replace("{{params_schema}}", schema)


def get_evaluate_status_prompt(experiment_family: str) -> str:
    """获取评估状态的专属 prompt"""
    return EVALUATE_STATUS_PROMPTS.get(experiment_family, EVALUATE_STATUS_PROMPTS["rabi"])


# ========== Response Schema ==========

# Q1: 描述图表 Response Schema
DESCRIBE_PLOT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "plot_type": {
            "type": "string",
            "enum": ["scatter", "line", "heatmap", "histogram"],
        },
        "x_axis": {
            "type": "object",
            "properties": {
                "label": {"type": "string"},
                "scale": {"type": "string", "enum": ["linear", "log"]},
                "range": {"type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2},
            },
            "required": ["label", "scale", "range"],
        },
        "y_axis": {
            "type": "object",
            "properties": {
                "label": {"type": "string"},
                "scale": {"type": "string", "enum": ["linear", "log"]},
                "range": {"type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2},
            },
            "required": ["label", "scale", "range"],
        },
        "main_features": {"type": "string"},
    },
    "required": ["plot_type", "x_axis", "y_axis", "main_features"],
}

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

# Q5: 提取参数 Response Schema - 每个家族提取不同的参数
EXTRACT_PARAMS_SCHEMAS = {
    "coupler_flux": {
        "type": "object",
        "properties": {
            "crossing_voltages_V": {"type": "array", "items": {"type": "number"}, "description": "the two bias voltages where avoided crossings occur"},
            "left_fig_branch_freqs_GHz": {"type": "array", "items": {"type": "number"}},
            "right_fig_branch_freqs_GHz": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["crossing_voltages_V"],
    },
    "cz_benchmarking": {
        "type": "object",
        "properties": {
            "site_indices": {"type": "array", "items": {"type": "integer"}},
            "retention_per_cz": {"type": "number"},
            "retention_per_cz_unc": {"type": "number"},
            "cycle_polarization": {"type": "number"},
            "cycle_polarization_unc": {"type": "number"},
            "max_circuit_depth": {"type": "integer"},
        },
        "required": ["retention_per_cz", "cycle_polarization"],
    },
    "drag": {
        "type": "object",
        "properties": {
            "optimal_alpha_inv": {"oneOf": [{"type": "number"}, {"type": "string"}]},
            "intersection_clear": {"type": "boolean"},
        },
        "required": ["intersection_clear"],
    },
    "gmm": {
        "type": "object",
        "properties": {
            "separation": {"type": "string", "enum": ["well-separated", "touching", "overlapping"]},
            "cluster0_center": {"type": "array", "items": {"type": "number"}},
            "cluster1_center": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["separation"],
    },
    "microwave_ramsey": {
        "type": "object",
        "properties": {
            "detuning_Hz": {"oneOf": [{"type": "number"}, {"type": "null"}]},
            "detuning_Hz_unc": {"oneOf": [{"type": "number"}, {"type": "null"}]},
            "contrast": {"type": "number"},
            "retention_min": {"type": "number"},
        },
        "required": ["contrast"],
    },
    "mot_loading": {
        "type": "object",
        "properties": {
            "has_cloud": {"type": "boolean"},
            "center_x": {"type": "integer"},
            "center_y": {"type": "integer"},
            "cloud_present": {"type": "boolean"},
        },
        "required": ["has_cloud"],
    },
    "pinchoff": {
        "type": "object",
        "properties": {
            "cut_off_index": {"oneOf": [{"type": "integer"}, {"type": "null"}]},
            "transition_index": {"oneOf": [{"type": "integer"}, {"type": "null"}]},
            "saturation_index": {"oneOf": [{"type": "integer"}, {"type": "null"}]},
        },
        "required": [],
    },
    "pingpong": {
        "type": "object",
        "properties": {
            "error_per_gate": {"oneOf": [{"type": "number"}, {"type": "null"}]},
            "accumulation_type": {"type": "string", "enum": ["linear", "oscillatory", "none"]},
        },
        "required": ["accumulation_type"],
    },
    "qubit_flux_spectroscopy": {
        "type": "object",
        "properties": {
            "num_resonances": {"type": "integer"},
            "resonance_freq_GHz": {"type": "number"},
        },
        "required": ["num_resonances"],
    },
    "qubit_spectroscopy": {
        "type": "object",
        "properties": {
            "num_resonances": {"type": "integer"},
            "resonance_freq_GHz": {"type": "number"},
            "resonance_type": {"type": "string", "enum": ["peak", "dip"]},
        },
        "required": ["num_resonances"],
    },
    "qubit_spectroscopy_power_frequency": {
        "type": "object",
        "properties": {
            "f01_MHz": {"oneOf": [{"type": "number"}, {"type": "null"}]},
            "transitions_visible": {"type": "string", "enum": ["f01_only", "f01_f02half", "none"]},
            "power_regime": {"type": "string", "enum": ["optimal", "high", "none"]},
            "measurement_usable": {"type": "boolean"},
        },
        "required": ["measurement_usable"],
    },
    "rabi": {
        "type": "object",
        "properties": {
            "periods_visible": {"type": "number"},
            "amplitude_decay": {"type": "string", "enum": ["stable", "decaying", "growing"]},
            "signal_quality": {"type": "string", "enum": ["clean", "noisy", "distorted"]},
        },
        "required": ["periods_visible"],
    },
    "rabi_hw": {
        "type": "object",
        "properties": {
            "periods_visible": {"type": "number"},
            "amplitude_decay": {"type": "string", "enum": ["stable", "decaying", "growing"]},
            "signal_quality": {"type": "string", "enum": ["clean", "noisy", "distorted"]},
        },
        "required": ["periods_visible"],
    },
    "ramsey_charge_tomography": {
        "type": "object",
        "properties": {
            "event_detected": {"type": "boolean"},
            "jump_count": {"type": "integer"},
            "jump_positions": {"type": "array", "items": {"type": "integer"}},
            "jump_sizes_mV": {"type": "array", "items": {"type": "number"}},
        },
        "required": ["event_detected"],
    },
    "ramsey_freq_cal": {
        "type": "object",
        "properties": {
            "T2_star_us": {"oneOf": [{"type": "number"}, {"type": "null"}]},
            "detuning_MHz": {"oneOf": [{"type": "number"}, {"type": "null"}]},
            "fringes_visible": {"type": "integer"},
        },
        "required": [],
    },
    "ramsey_t2star": {
        "type": "object",
        "properties": {
            "T2_star_us": {"oneOf": [{"type": "number"}, {"type": "null"}]},
            "detuning_MHz": {"oneOf": [{"type": "number"}, {"type": "null"}]},
            "fringes_visible": {"type": "integer"},
        },
        "required": [],
    },
    "res_spec": {
        "type": "object",
        "properties": {
            "resonance_freq_GHz": {"oneOf": [{"type": "number"}, {"type": "null"}]},
            "contrast": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        },
        "required": [],
    },
    "rydberg_ramsey": {
        "type": "object",
        "properties": {
            "frequency_MHz": {"type": "number"},
            "frequency_MHz_unc": {"type": "number"},
            "T2_us": {"type": "number"},
            "T2_us_unc": {"type": "number"},
            "RChi2": {"type": "number"},
            "frequency_noise_kHz": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        },
        "required": ["frequency_MHz", "T2_us"],
    },
    "rydberg_spectroscopy": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "site_index": {"type": "integer"},
                "f0_kHz": {"type": "number"},
                "f0_kHz_unc": {"type": "number"},
                "t_ns": {"type": "number"},
                "t_ns_unc": {"type": "number"},
                "f_Rabi_MHz": {"type": "number"},
                "f_Rabi_MHz_unc": {"type": "number"},
                "chi_squared": {"type": "number"},
            },
        },
    },
    "t1": {
        "type": "object",
        "properties": {
            "T1_us": {"oneOf": [{"type": "number"}, {"type": "null"}]},
            "decay_visible": {"type": "boolean"},
        },
        "required": ["decay_visible"],
    },
    "t1_fluctuations": {
        "type": "object",
        "properties": {
            "classification": {"type": "string", "enum": ["stable", "telegraphic", "random_walk"]},
            "mean_t1_us": {"type": "number"},
        },
        "required": ["classification"],
    },
    "tweezer_array": {
        "type": "object",
        "properties": {
            "grid_regularity": {"type": "string", "enum": ["regular", "irregular"]},
            "spot_uniformity": {"type": "string", "enum": ["uniform", "non-uniform"]},
            "aberration_corrected": {"type": "boolean"},
        },
        "required": ["aberration_corrected"],
    },
}


def get_extract_params_schema(experiment_family: str) -> dict:
    """获取参数提取的JSON Schema"""
    return EXTRACT_PARAMS_SCHEMAS.get(
        experiment_family,
        {"type": "object", "properties": {}}
    )

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
    "EXTRACT_PARAMS_SCHEMAS",
    # Prompt 字典
    "DESCRIBE_PLOT_PROMPTS",
    "CLASSIFY_OUTCOME_PROMPTS",
    "SCIENTIFIC_REASONING_PROMPTS",
    "ASSESS_FIT_PROMPTS",
    "EXTRACT_PARAMS_PROMPTS",
    "EVALUATE_STATUS_PROMPTS",
    # Response Schema
    "DESCRIBE_PLOT_RESPONSE_SCHEMA",
    "CLASSIFY_OUTCOME_RESPONSE_SCHEMA",
    "ASSESS_FIT_RESPONSE_SCHEMA",
    "EVALUATE_STATUS_RESPONSE_SCHEMA",
    # 获取函数
    "get_extract_params_schema",
    "get_describe_plot_prompt",
    "get_classify_outcome_prompt",
    "get_scientific_reasoning_prompt",
    "get_assess_fit_prompt",
    "get_extract_params_prompt",
    "get_evaluate_status_prompt",
]