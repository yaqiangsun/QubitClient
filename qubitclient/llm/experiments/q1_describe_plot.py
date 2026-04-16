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

# ========== 独立 Prompt 字符串定义 ==========

# Standard prompt for single-image plots
PROMPT_STANDARD = """Describe the figure <image> in JSON format.

Required fields:
{
  "plot_type": "scatter" | "line" | "heatmap" | "histogram",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "main_features": string
}"""

# Two-image prompt
PROMPT_TWO_IMAGES = """Describe each figure <image> in JSON format.

This entry has 2 images. Provide a JSON array with one object per image, in order.

Required fields per image:
{
  "plot_type": "scatter" | "line" | "heatmap" | "histogram",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "main_features": string
}"""

# MOT loading / tweezer array prompt
PROMPT_CAMERA_IMAGE = """Describe the figure <image> in JSON format.

Required fields:
{
  "plot_type": "image" | "heatmap" | "scatter",
  "x_axis": {"label": string, "unit": string},
  "y_axis": {"label": string, "unit": string},
  "colorbar": {"label": string},
  "main_features": string
}"""

# Tweezer array prompt (no colorbar)
PROMPT_TWEEZER = """Describe the figure <image> in JSON format.

Required fields:
{
  "plot_type": "image" | "heatmap" | "scatter",
  "x_axis": {"label": string, "unit": string},
  "y_axis": {"label": string, "unit": string},
  "main_features": string
}"""

# Charge tomography prompt
PROMPT_CHARGE_TOMOGRAPHY = """Describe the figure <image> in JSON format.

Required fields:
{
  "plot_type": "heatmap" | "line" | "scatter",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "colorbar": {"label": string},
  "main_features": string
}"""

# Aliases for compatibility
PROMPT_COUPLER_FLUX = PROMPT_STANDARD
# Special case for cz_benchmarking (different field name)
PROMPT_CZ_BENCHMARKING = """Describe each figure <image> in JSON format.

This entry has 2 images. Provide a JSON array with one object per image, in order.

Required fields per object:
{
  "plot_type": "scatter" | "line" | "heatmap" | "histogram",
  "x_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "y_axis": {"label": string, "scale": "linear" | "log", "range": [min, max]},
  "main_features": string
}"""
PROMPT_DRAG = PROMPT_STANDARD
PROMPT_GMM = PROMPT_STANDARD
PROMPT_MICROWAVE_RAMSEY = PROMPT_STANDARD
PROMPT_MOT_LOADING = PROMPT_CAMERA_IMAGE

# Aliases for remaining experiments
PROMPT_PINCHOFF = PROMPT_STANDARD
PROMPT_PINGPONG = PROMPT_STANDARD
PROMPT_QUBIT_FLUX_SPECTROSCOPY = PROMPT_STANDARD
PROMPT_QUBIT_SPECTROSCOPY = PROMPT_STANDARD
PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = PROMPT_TWO_IMAGES
PROMPT_RABI = PROMPT_STANDARD
PROMPT_RABI_HW = PROMPT_STANDARD
PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = PROMPT_CHARGE_TOMOGRAPHY
PROMPT_RAMSEY_FREQ_CAL = PROMPT_TWO_IMAGES
PROMPT_RAMSEY_T2STAR = PROMPT_TWO_IMAGES
PROMPT_RES_SPEC = PROMPT_TWO_IMAGES
PROMPT_RYDBERG_RAMSEY = PROMPT_STANDARD
PROMPT_RYDBERG_SPECTROSCOPY = PROMPT_STANDARD
PROMPT_T1 = PROMPT_STANDARD
PROMPT_T1_FLUCTUATIONS = PROMPT_STANDARD
PROMPT_TWEEZER_ARRAY = PROMPT_TWEEZER


# ========== Prompt 字典映射 ==========

DESCRIBE_PLOT_PROMPTS = {
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