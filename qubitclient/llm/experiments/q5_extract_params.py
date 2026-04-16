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

PROMPT_COUPLER_FLUX = """Extract the following parameters from this coupler flux spectroscopy plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_CZ_BENCHMARKING = """Extract the following parameters from this CZ benchmarking plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_DRAG = """Extract the following parameters from this DRAG calibration plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_GMM = """Extract the following parameters from this GMM plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_MICROWAVE_RAMSEY = """Extract the following parameters from this Ramsey plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_MOT_LOADING = """Extract the following parameters from this MOT image <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_PINCHOFF = """Extract the following parameters from this pinch-off plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_PINGPONG = """Extract the following parameters from this PingPong plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_QUBIT_FLUX_SPECTROSCOPY = """Extract the following parameters from this flux spectroscopy plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_QUBIT_SPECTROSCOPY = """Extract the following parameters from this spectroscopy plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_QUBIT_SPECTROSCOPY_POWER_FREQUENCY = """Extract the following parameters from this 2D spectroscopy plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_RABI = """Extract the following parameters from this Rabi plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_RABI_HW = """Extract the following parameters from this Rabi HW plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_RAMSEY_CHARGE_TOMOGRAPHY = """Extract the following parameters from this charge tomography plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_RAMSEY_FREQ_CAL = """Extract the following parameters from this Ramsey freq cal plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_RAMSEY_T2STAR = """Extract the following parameters from this T2* plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_RES_SPEC = """Extract the following parameters from this resonator spectroscopy plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_RYDBERG_RAMSEY = """Extract the following parameters from this Rydberg Ramsey plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_RYDBERG_SPECTROSCOPY = """Extract the following parameters from this Rydberg spectroscopy plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_T1 = """Extract the following parameters from this T1 plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_T1_FLUCTUATIONS = """Extract the following parameters from this T1 stability plot <image>.

Report in JSON format:
{{params_schema}}"""

PROMPT_TWEEZER_ARRAY = """Extract the following parameters from this tweezer array image <image>.

Report in JSON format:
{{params_schema}}"""


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


def get_extract_params_prompt(experiment_family: str, params_schema: str | None = None) -> str:
    """获取提取参数的专属 prompt"""
    base_prompt = EXTRACT_PARAMS_PROMPTS.get(experiment_family, EXTRACT_PARAMS_PROMPTS["rabi"])
    schema = params_schema or '{"optimal_value": float, "note": string}'
    return base_prompt.replace("{{params_schema}}", schema)


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
        "max_circuit_depth": {"type": "integer"},
    },
    "required": ["retention_per_cz", "cycle_polarization"],
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