# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
Q5: 提取参数任务

从图表中提取指定参数
"""

# ========== 独立 Prompt 字符串定义 ==========

# Special case: prompt includes background (different from experiment_background field)
PROMPT_COUPLER_FLUX = """This is tunable coupler spectroscopy: we map the coupler's frequency response vs applied flux bias. Each image has two panels (left and right), each showing a different qubit. There are three frequency branches separated by two avoided crossings.

Extract the following parameters from this coupler flux plot <image>.

Report in JSON format:
{"crossing_voltages_V": [float, float], "left_fig_branch_freqs_GHz": [float, float, float], "right_fig_branch_freqs_GHz": [float, float, float]}

crossing_voltages_V: the two bias voltages where avoided crossings occur, ordered left to right.
left/right_fig_branch_freqs_GHz: the three branch plateau frequencies in each panel, ordered left to right along the voltage axis. Use "Unreliable" if the fit is too poor to read."""

PROMPT_CZ_BENCHMARKING = """Extract the following parameters from this CZ benchmarking data <image>.

Read the site/qubit pair indices from the title (e.g. 'Sites (9, 11)').
Read uncertainties from the title (parenthetical notation, e.g. '0.9955 (4)' means 0.9955 +/- 0.0004).

Report in JSON format:
{"site_indices": [int, int], "retention_per_cz": float, "retention_per_cz_unc": float, "cycle_polarization": float, "cycle_polarization_unc": float, "chi_squared_retention": float | null, "chi_squared_polarization": float | null, "max_circuit_depth": int}"""

PROMPT_DRAG = """Extract the following parameters from this DRAG calibration plot <image>.

Report in JSON format:
{"optimal_alpha_inv": float, "intersection_clear": true | false}"""

PROMPT_GMM = """Extract the following parameters from this GMM plot <image>.

Report in JSON format:
{"separation": "well-separated" | "touching" | "overlapping", "cluster0_center": [I, Q], "cluster1_center": [I, Q]}"""

PROMPT_MICROWAVE_RAMSEY = """Extract the following parameters from this microwave Ramsey plot <image>.

Read the detuning and its uncertainty from the title (+/- notation).

Report in JSON format:
{"detuning_Hz": float | null, "detuning_Hz_unc": float | null, "contrast": float, "retention_min": float}"""

PROMPT_MOT_LOADING = """Extract the cloud parameters from this MOT image <image>.

Report in JSON format:
{"has_cloud": true | false, "center_x": int, "center_y": int, "cloud_present": true | false}

- has_cloud: whether a distinct atom cloud is visible
- center_x: approximate x-coordinate of cloud center (pixels)
- center_y: approximate y-coordinate of cloud center (pixels)
- cloud_present: same as has_cloud (for verification)

If no cloud is visible, report center coordinates as 0."""

PROMPT_PINCHOFF = """Extract the key transition indices from this pinchoff measurement <image>.

The x-axis shows gate voltage index (0-40, total 41 points).
Identify three key positions as index values:

Report in JSON format:
{"cut_off_index": int | null, "transition_index": int | null, "saturation_index": int | null}

- saturation_index: Index where the current first reaches its high plateau (saturation region)
- transition_index: Index of the midpoint of the transition region
- cut_off_index: Index where the current reaches its low plateau (device pinched off)

If the transition is not clear enough to identify these indices, use null."""

PROMPT_PINGPONG = """Extract the following parameters from this PingPong measurement <image>.

Report in JSON format:
{"error_per_gate": float | null, "accumulation_type": "linear" | "oscillatory" | "none"}"""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """Extract the following parameters from this qubit spectroscopy plot <image>.

Report in JSON format:
{"num_resonances": int, "resonance_freq_GHz": float}"""

PROMPT_QUBIT_SPECTROSCOPY = """Extract the following parameters from this spectroscopy plot <image>.

Report in JSON format:
{"num_resonances": int, "resonance_freq_GHz": float, "resonance_type": "peak" | "dip"}"""

# Special case: prompt includes background (different version from experiment_background field)
PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """This is a 2D qubit spectroscopy experiment on a standard transmon (negative anharmonicity, so f02/2 appears at a lower frequency than f01): we sweep both drive power and frequency to map qubit transitions. A successful result shows clear transition lines (f01, and optionally f02/2) with visible power dependence.

Extract the following parameters from this 2D qubit spectroscopy plot <image>.

Report in JSON format:
{"f01_MHz": float | null, "transitions_visible": "f01_only" | "f01_f02half" | "none", "power_regime": "optimal" | "high" | "none", "measurement_usable": bool}"""

PROMPT_RABI = """Extract the following parameters from this Rabi oscillation plot <image>.

Report in JSON format:
{"periods_visible": float, "amplitude_decay": "stable" | "decaying" | "growing", "signal_quality": "clean" | "noisy" | "distorted"}"""

PROMPT_RABI_HW = """Extract the following parameters from this Rabi oscillation plot <image>.

Report in JSON format:
{"periods_visible": float, "amplitude_decay": "stable" | "decaying" | "growing", "signal_quality": "clean" | "noisy" | "distorted"}"""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """Analyze this Ramsey charge tomography scan <image> for charge jump events.

Classify whether any charge jump event is detected, and if so, extract positions and sizes.

Report in JSON format:
{"event_detected": true | false, "jump_count": int, "jump_positions": [int, ...], "jump_sizes_mV": [float, ...]}

- event_detected: whether any charge jump event is visible
- jump_count: total number of charge jump events (horizontal discontinuities)
- jump_positions: list of scan numbers where jumps occur (approximate)
- jump_sizes_mV: list of estimated charge jump sizes in mV for each detected jump"""

PROMPT_RAMSEY_FREQ_CAL = """Extract the following parameters from this Ramsey measurement <image>.

Report in JSON format:
{"T2_star_us": float | null, "detuning_MHz": float | null, "fringes_visible": int}"""

PROMPT_RAMSEY_T2STAR = """Extract the following parameters from this Ramsey measurement <image>.

Report in JSON format:
{"T2_star_us": float | null, "detuning_MHz": float | null, "fringes_visible": int}"""

PROMPT_RES_SPEC = """Extract the following parameters from this resonator spectroscopy plot <image>.

Report in JSON format:
{"resonance_freq_GHz": float | null | null, "contrast": float | null}"""

PROMPT_RYDBERG_RAMSEY = """Extract the following parameters from this Rydberg Ramsey plot <image>.

Read uncertainties from the title/header (+/- notation).

Report in JSON format:
{"frequency_MHz": float, "frequency_MHz_unc": float, "T2_us": float, "T2_us_unc": float, "RChi2": float, "frequency_noise_kHz": float | null}"""

PROMPT_RYDBERG_SPECTROSCOPY = """Extract the following parameters from this Rydberg spectroscopy plot <image>.

If the plot shows multiple sites/panels, report a JSON array with one object per site.
Read the site index label from the plot (e.g. 153, 171). Read uncertainties from the title/header (+/- or parenthetical notation).

Report in JSON format (array of objects, one per site):
[{"site_index": int, "f0_kHz": float, "f0_kHz_unc": float, "t_ns": float, "t_ns_unc": float, "f_Rabi_MHz": float, "f_Rabi_MHz_unc": float, "chi_squared": float}]"""

PROMPT_T1 = """Extract the following parameters from this T1 decay plot <image>.

Report in JSON format:
{"T1_us": float | null, "decay_visible": true | false}"""

PROMPT_T1_FLUCTUATIONS = """Extract the following parameters from this T1 fluctuation measurement <image>.

Report in JSON format:
{"classification": "stable" | "telegraphic" | "random_walk", "mean_t1_us": float}"""

PROMPT_TWEEZER_ARRAY = """Examine this tweezer array camera image <image>.

Extract the following properties.

Report in JSON format:
{"grid_regularity": "regular" | "irregular", "spot_uniformity": "uniform" | "non-uniform", "aberration_corrected": true | false}"""


# ========== Prompt 字典映射 ==========

EXTRACT_PARAMS_PROMPTS = {
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


def get_extract_params_prompt(experiment_family: str) -> str:
    """获取提取参数的专属 prompt"""
    return EXTRACT_PARAMS_PROMPTS.get(experiment_family, EXTRACT_PARAMS_PROMPTS["rabi"])


# ========== 参数提取 Schema ==========

SCHEMA_COUPLER_FLUX = {
    "type": "object",
    "properties": {
        "crossing_voltages_V": {"type": "array", "items": {"type": "number"}, "description": "the two bias voltages where avoided crossings occur"},
        "left_fig_branch_freqs_GHz": {"type": "array", "items": {"type": "number"}},
        "right_fig_branch_freqs_GHz": {"type": "array", "items": {"type": "number"}},
    },
    "required": ["crossing_voltages_V"],
}

SCHEMA_CZ_BENCHMARKING = {
    "type": "object",
    "properties": {
        "site_indices": {"type": "array", "items": {"type": "integer"}},
        "retention_per_cz": {"type": "number"},
        "retention_per_cz_unc": {"type": "number"},
        "cycle_polarization": {"type": "number"},
        "cycle_polarization_unc": {"type": "number"},
        "chi_squared_retention": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        "chi_squared_polarization": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        "max_circuit_depth": {"type": "integer"},
    },
    "required": ["site_indices", "retention_per_cz", "cycle_polarization"],
}

SCHEMA_DRAG = {
    "type": "object",
    "properties": {
        "optimal_alpha_inv": {"oneOf": [{"type": "number"}, {"type": "string"}]},
        "intersection_clear": {"type": "boolean"},
    },
    "required": ["intersection_clear"],
}

SCHEMA_GMM = {
    "type": "object",
    "properties": {
        "separation": {"type": "string", "enum": ["well-separated", "touching", "overlapping"]},
        "cluster0_center": {"type": "array", "items": {"type": "number"}},
        "cluster1_center": {"type": "array", "items": {"type": "number"}},
    },
    "required": ["separation"],
}

SCHEMA_MICROWAVE_RAMSEY = {
    "type": "object",
    "properties": {
        "detuning_Hz": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        "detuning_Hz_unc": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        "contrast": {"type": "number"},
        "retention_min": {"type": "number"},
    },
    "required": ["contrast"],
}

SCHEMA_MOT_LOADING = {
    "type": "object",
    "properties": {
        "has_cloud": {"type": "boolean"},
        "center_x": {"type": "integer"},
        "center_y": {"type": "integer"},
        "cloud_present": {"type": "boolean"},
    },
    "required": ["has_cloud"],
}

SCHEMA_PINCHOFF = {
    "type": "object",
    "properties": {
        "cut_off_index": {"oneOf": [{"type": "integer"}, {"type": "null"}]},
        "transition_index": {"oneOf": [{"type": "integer"}, {"type": "null"}]},
        "saturation_index": {"oneOf": [{"type": "integer"}, {"type": "null"}]},
    },
    "required": [],
}

SCHEMA_PINGPONG = {
    "type": "object",
    "properties": {
        "error_per_gate": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        "accumulation_type": {"type": "string", "enum": ["linear", "oscillatory", "none"]},
    },
    "required": ["accumulation_type"],
}

SCHEMA_QUBIT_FLUX_SPECTROSCOPY = {
    "type": "object",
    "properties": {
        "num_resonances": {"type": "integer"},
        "resonance_freq_GHz": {"type": "number"},
    },
    "required": ["num_resonances"],
}

SCHEMA_QUBIT_SPECTROSCOPY = {
    "type": "object",
    "properties": {
        "num_resonances": {"type": "integer"},
        "resonance_freq_GHz": {"type": "number"},
        "resonance_type": {"type": "string", "enum": ["peak", "dip"]},
    },
    "required": ["num_resonances"],
}

SCHEMA_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = {
    "type": "object",
    "properties": {
        "f01_MHz": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        "transitions_visible": {"type": "string", "enum": ["f01_only", "f01_f02half", "none"]},
        "power_regime": {"type": "string", "enum": ["optimal", "high", "none"]},
        "measurement_usable": {"type": "boolean"},
    },
    "required": ["measurement_usable"],
}

SCHEMA_RABI = {
    "type": "object",
    "properties": {
        "periods_visible": {"type": "number"},
        "amplitude_decay": {"type": "string", "enum": ["stable", "decaying", "growing"]},
        "signal_quality": {"type": "string", "enum": ["clean", "noisy", "distorted"]},
    },
    "required": ["periods_visible"],
}

SCHEMA_RABI_HW = {
    "type": "object",
    "properties": {
        "periods_visible": {"type": "number"},
        "amplitude_decay": {"type": "string", "enum": ["stable", "decaying", "growing"]},
        "signal_quality": {"type": "string", "enum": ["clean", "noisy", "distorted"]},
    },
    "required": ["periods_visible"],
}

SCHEMA_RAMSEY_CHARGE_TOMOGRAPHY = {
    "type": "object",
    "properties": {
        "event_detected": {"type": "boolean"},
        "jump_count": {"type": "integer"},
        "jump_positions": {"type": "array", "items": {"type": "integer"}},
        "jump_sizes_mV": {"type": "array", "items": {"type": "number"}},
    },
    "required": ["event_detected"],
}

SCHEMA_RAMSEY_FREQ_CAL = {
    "type": "object",
    "properties": {
        "T2_star_us": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        "detuning_MHz": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        "fringes_visible": {"type": "integer"},
    },
    "required": [],
}

SCHEMA_RAMSEY_T2STAR = {
    "type": "object",
    "properties": {
        "T2_star_us": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        "detuning_MHz": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        "fringes_visible": {"type": "integer"},
    },
    "required": [],
}

SCHEMA_RES_SPEC = {
    "type": "object",
    "properties": {
        "resonance_freq_GHz": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        "contrast": {"oneOf": [{"type": "number"}, {"type": "null"}]},
    },
    "required": [],
}

SCHEMA_RYDBERG_RAMSEY = {
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
}

SCHEMA_RYDBERG_SPECTROSCOPY = {
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
}

SCHEMA_T1 = {
    "type": "object",
    "properties": {
        "T1_us": {"oneOf": [{"type": "number"}, {"type": "null"}]},
        "decay_visible": {"type": "boolean"},
    },
    "required": ["decay_visible"],
}

SCHEMA_T1_FLUCTUATIONS = {
    "type": "object",
    "properties": {
        "classification": {"type": "string", "enum": ["stable", "telegraphic", "random_walk"]},
        "mean_t1_us": {"type": "number"},
    },
    "required": ["classification"],
}

SCHEMA_TWEEZER_ARRAY = {
    "type": "object",
    "properties": {
        "grid_regularity": {"type": "string", "enum": ["regular", "irregular"]},
        "spot_uniformity": {"type": "string", "enum": ["uniform", "non-uniform"]},
        "aberration_corrected": {"type": "boolean"},
    },
    "required": ["aberration_corrected"],
}


# ========== Schema 字典映射 ==========

EXTRACT_PARAMS_SCHEMAS = {
    "coupler_flux": SCHEMA_COUPLER_FLUX,
    "cz_benchmarking": SCHEMA_CZ_BENCHMARKING,
    "drag": SCHEMA_DRAG,
    "gmm": SCHEMA_GMM,
    "microwave_ramsey": SCHEMA_MICROWAVE_RAMSEY,
    "mot_loading": SCHEMA_MOT_LOADING,
    "pinchoff": SCHEMA_PINCHOFF,
    "pingpong": SCHEMA_PINGPONG,
    "qubit_flux_spectroscopy": SCHEMA_QUBIT_FLUX_SPECTROSCOPY,
    "qubit_spectroscopy": SCHEMA_QUBIT_SPECTROSCOPY,
    "qubit_spectroscopy_power_frequency": SCHEMA_QUBIT_SPECTROSCOPY_POWER_FREQUENCY,
    "rabi": SCHEMA_RABI,
    "rabi_hw": SCHEMA_RABI_HW,
    "ramsey_charge_tomography": SCHEMA_RAMSEY_CHARGE_TOMOGRAPHY,
    "ramsey_freq_cal": SCHEMA_RAMSEY_FREQ_CAL,
    "ramsey_t2star": SCHEMA_RAMSEY_T2STAR,
    "res_spec": SCHEMA_RES_SPEC,
    "rydberg_ramsey": SCHEMA_RYDBERG_RAMSEY,
    "rydberg_spectroscopy": SCHEMA_RYDBERG_SPECTROSCOPY,
    "t1": SCHEMA_T1,
    "t1_fluctuations": SCHEMA_T1_FLUCTUATIONS,
    "tweezer_array": SCHEMA_TWEEZER_ARRAY,
}


def get_extract_params_schema(experiment_family: str) -> dict:
    """获取参数提取的JSON Schema"""
    return EXTRACT_PARAMS_SCHEMAS.get(
        experiment_family,
        {"type": "object", "properties": {}}
    )


__all__ = [
    "EXTRACT_PARAMS_PROMPTS",
    "EXTRACT_PARAMS_SCHEMAS",
    "get_extract_params_prompt",
    "get_extract_params_schema",
]