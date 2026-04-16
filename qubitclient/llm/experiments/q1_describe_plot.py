# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
Q1: 描述图表任务

描述图像中的图表类型、坐标轴、范围和主要特征
"""

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


def get_describe_plot_prompt(experiment_family: str) -> str:
    """获取描述图表的专属 prompt"""
    return DESCRIBE_PLOT_PROMPTS.get(experiment_family, DESCRIBE_PLOT_PROMPTS["rabi"])


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


__all__ = [
    "DESCRIBE_PLOT_PROMPTS",
    "DESCRIBE_PLOT_RESPONSE_SCHEMA",
    "get_describe_plot_prompt",
]