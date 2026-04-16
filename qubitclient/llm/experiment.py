# -*- coding: utf-8 -*-
"""
QCalEval 实验配置模块
定义每种实验类型的背景、提示词和响应Schema
"""

from enum import Enum, unique
from typing import Any


@unique
class ExperimentFamily(Enum):
    """实验家族枚举 - 用于指定不同实验类型的 prompt"""
    COUPLER_FLUX = "coupler_flux"
    CZ_BENCHMARKING = "cz_benchmarking"
    DRAG = "drag"
    GMM = "gmm"
    MICROWAVE_RAMSEY = "microwave_ramsey"
    MOT_LOADING = "mot_loading"
    PINCHOFF = "pinchoff"
    PINGPONG = "pingpong"
    QUBIT_FLUX_SPECTROSCOPY = "qubit_flux_spectroscopy"
    QUBIT_SPECTROSCOPY = "qubit_spectroscopy"
    QUBIT_SPECTROSCOPY_POWER_FREQUENCY = "qubit_spectroscopy_power_frequency"
    RABI = "rabi"
    RABI_HW = "rabi_hw"
    RAMSEY_CHARGE_TOMOGRAPHY = "ramsey_charge_tomography"
    RAMSEY_FREQ_CAL = "ramsey_freq_cal"
    RAMSEY_T2STAR = "ramsey_t2star"
    RES_SPEC = "res_spec"
    RYDBERG_RAMSEY = "rydberg_ramsey"
    RYDBERG_SPECTROSCOPY = "rydberg_spectroscopy"
    T1 = "t1"
    T1_FLUCTUATIONS = "t1_fluctuations"
    TWEEZER_ARRAY = "tweezer_array"


@unique
class ExperimentType(Enum):
    """实验类型枚举 - QCalEval 数据集中的 87 个具体测试用例"""
    # coupler_flux
    COUPLER_FLUX_FAILURE_BAD_FIT = "coupler_flux_failure_bad_fit"
    COUPLER_FLUX_SUCCESS = "coupler_flux_success"
    # cz_benchmarking
    CZ_BENCHMARKING_FAILURE_MISCALIBRATED = "cz_benchmarking_failure_miscalibrated"
    CZ_BENCHMARKING_FAILURE_NO_GATE = "cz_benchmarking_failure_no_gate"
    CZ_BENCHMARKING_SUCCESS = "cz_benchmarking_success"
    # drag
    DRAG_FAILURE_NO_SIGNAL = "drag_failure_no_signal"
    DRAG_FAILURE_POSITION_FAR_OFFSET = "drag_failure_position_far_offset"
    DRAG_FAILURE_POSITION_FIRST_QUARTER = "drag_failure_position_first_quarter"
    DRAG_FAILURE_POSITION_LAST_QUARTER = "drag_failure_position_last_quarter"
    DRAG_SUCCESS = "drag_success"
    # gmm
    GMM_FAILURE_HIGH_POWER = "gmm_failure_high_power"
    GMM_FAILURE_NO_EXCITATION = "gmm_failure_no_excitation"
    GMM_FAILURE_NO_RES_RESPONSE = "gmm_failure_no_res_response"
    GMM_FAILURE_NO_SIGNAL = "gmm_failure_no_signal"
    GMM_SUCCESS = "gmm_success"
    # microwave_ramsey
    MICROWAVE_RAMSEY_FAILURE_DETUNED = "microwave_ramsey_failure_detuned"
    MICROWAVE_RAMSEY_FAILURE_LOW_CONTRAST = "microwave_ramsey_failure_low_contrast"
    MICROWAVE_RAMSEY_SUCCESS = "microwave_ramsey_success"
    # mot_loading
    MOT_LOADING_GOOD = "mot_loading_good"
    MOT_LOADING_NO_SIGNAL = "mot_loading_no_signal"
    MOT_LOADING_TAILED = "mot_loading_tailed"
    # pinchoff
    PINCHOFF_FAILURE_INCOMPLETE_TRANSITION = "pinchoff_failure_incomplete_transition"
    PINCHOFF_FAILURE_NOISY_NO_TRANSITION = "pinchoff_failure_noisy_no_transition"
    PINCHOFF_FAILURE_STABILIZE_NEGATIVE = "pinchoff_failure_stabilize_negative"
    PINCHOFF_FAILURE_STABILIZE_POSITIVE = "pinchoff_failure_stabilize_positive"
    PINCHOFF_SUCCESS = "pinchoff_success"
    # pingpong
    PINGPONG_FAILURE_LARGE_ERROR = "pingpong_failure_large_error"
    PINGPONG_FAILURE_MODERATE_ERROR = "pingpong_failure_moderate_error"
    PINGPONG_FAILURE_NO_EXCITATION = "pingpong_failure_no_excitation"
    PINGPONG_SUCCESS_WELL_CALIBRATED = "pingpong_success_well_calibrated"
    # qubit_flux_spectroscopy
    QUBIT_FLUX_SPECTROSCOPY_FAILURE_BAD_FIT = "qubit_flux_spectroscopy_failure_bad_fit"
    QUBIT_FLUX_SPECTROSCOPY_FAILURE_FIT_FAILED = "qubit_flux_spectroscopy_failure_fit_failed"
    QUBIT_FLUX_SPECTROSCOPY_FAILURE_NO_DATA = "qubit_flux_spectroscopy_failure_no_data"
    QUBIT_FLUX_SPECTROSCOPY_FAILURE_NO_RESPONSE = "qubit_flux_spectroscopy_failure_no_response"
    QUBIT_FLUX_SPECTROSCOPY_FAILURE_NOT_TUNABLE = "qubit_flux_spectroscopy_failure_not_tunable"
    QUBIT_FLUX_SPECTROSCOPY_SUCCESS = "qubit_flux_spectroscopy_success"
    # qubit_spectroscopy
    QUBIT_SPECTROSCOPY_FAILURE_MULTIPLE_PEAKS = "qubit_spectroscopy_failure_multiple_peaks"
    QUBIT_SPECTROSCOPY_FAILURE_NO_PEAKS = "qubit_spectroscopy_failure_no_peaks"
    QUBIT_SPECTROSCOPY_SUCCESS = "qubit_spectroscopy_success"
    # qubit_spectroscopy_power_frequency
    QUBIT_SPECTROSCOPY_POWER_FREQUENCY_FAILURE_F01_F02HALF_AMP_TOO_HIGH = "qubit_spectroscopy_power_frequency_failure_f01_f02half_amp_too_high"
    QUBIT_SPECTROSCOPY_POWER_FREQUENCY_FAILURE_F01_ONLY_AMP_TOO_HIGH = "qubit_spectroscopy_power_frequency_failure_f01_only_amp_too_high"
    QUBIT_SPECTROSCOPY_POWER_FREQUENCY_FAILURE_NO_SIGNAL = "qubit_spectroscopy_power_frequency_failure_no_signal"
    QUBIT_SPECTROSCOPY_POWER_FREQUENCY_SUCCESS_F01_F02HALF_FULL_RANGE = "qubit_spectroscopy_power_frequency_success_f01_f02half_full_range"
    QUBIT_SPECTROSCOPY_POWER_FREQUENCY_SUCCESS_F01_LOW_AMP_SHARP = "qubit_spectroscopy_power_frequency_success_f01_low_amp_sharp"
    QUBIT_SPECTROSCOPY_POWER_FREQUENCY_SUCCESS_F01_ONLY_FULL_RANGE = "qubit_spectroscopy_power_frequency_success_f01_only_full_range"
    # rabi
    RABI_FAILURE_DAMPED_OSCILLATIONS = "rabi_failure_damped_oscillations"
    RABI_FAILURE_RANDOM_SIGNAL = "rabi_failure_random_signal"
    RABI_FAILURE_TOO_FAST = "rabi_failure_too_fast"
    RABI_FAILURE_TOO_SLOW = "rabi_failure_too_slow"
    RABI_SUCCESS = "rabi_success"
    RABI_SUCCESS_OFF_RESONANCE = "rabi_success_off_resonance"
    RABI_SUCCESSFUL_LIMITED_RANGE = "rabi_successful_limited_range"
    # rabi_hw
    RABI_HW_FAILURE_INCORRECT_FIT = "rabi_hw_failure_incorrect_fit"
    RABI_HW_FAILURE_INSUFFICIENT_AMPLITUDE_RANGE = "rabi_hw_failure_insufficient_amplitude_range"
    RABI_HW_FAILURE_OFF_RESONANT_DRIVE = "rabi_hw_failure_off_resonant_drive"
    RABI_HW_SUCCESS = "rabi_hw_success"
    # ramsey_charge_tomography
    RAMSEY_CHARGE_TOMOGRAPHY_CLEAN = "ramsey_charge_tomography_clean"
    RAMSEY_CHARGE_TOMOGRAPHY_FEW_BURSTS = "ramsey_charge_tomography_few_bursts"
    RAMSEY_CHARGE_TOMOGRAPHY_MANY_BURSTS = "ramsey_charge_tomography_many_bursts"
    RAMSEY_CHARGE_TOMOGRAPHY_NOISY = "ramsey_charge_tomography_noisy"
    # ramsey_freq_cal
    RAMSEY_FAILURE_FREQ_CAL_BEATING = "ramsey_failure_freq_cal_beating"
    RAMSEY_FAILURE_FREQ_CAL_TOO_FEW_OSC = "ramsey_failure_freq_cal_too_few_osc"
    RAMSEY_FAILURE_FREQ_CAL_TOO_MANY_OSC = "ramsey_failure_freq_cal_too_many_osc"
    RAMSEY_SUCCESS_FREQ_CAL = "ramsey_success_freq_cal"
    # ramsey_t2star
    RAMSEY_FAILURE_T2STAR_BEATING = "ramsey_failure_t2star_beating"
    RAMSEY_FAILURE_T2STAR_SAMPLING_TOO_COARSE = "ramsey_failure_t2star_sampling_too_coarse"
    RAMSEY_FAILURE_T2STAR_WINDOW_TOO_SHORT = "ramsey_failure_t2star_window_too_short"
    RAMSEY_FAILURE_T2STAR_ZERO_DETUNING = "ramsey_failure_t2star_zero_detuning"
    RAMSEY_SUCCESS_T2STAR = "ramsey_success_t2star"
    # res_spec
    RES_SPEC_FAILURE_WIDE_SCAN_NO_SIGNAL = "res_spec_failure_wide_scan_no_signal"
    RES_SPEC_FAILURE_ZOOMED_NO_SIGNAL = "res_spec_failure_zoomed_no_signal"
    RES_SPEC_SUCCESS_2QUBIT_WIDE_SCAN_RESONATOR = "res_spec_success_2qubit_wide_scan_resonator"
    RES_SPEC_SUCCESS_WIDE_SCAN_RESONATOR = "res_spec_success_wide_scan_resonator"
    RES_SPEC_SUCCESS_ZOOMED_RESONATOR = "res_spec_success_zoomed_resonator"
    # rydberg_ramsey
    RYDBERG_RAMSEY_FAILURE_UNDERSAMPLED = "rydberg_ramsey_failure_undersampled"
    RYDBERG_RAMSEY_SUCCESS = "rydberg_ramsey_success"
    # rydberg_spectroscopy
    RYDBERG_SPECTROSCOPY_FAILURE_LOW_CONTRAST = "rydberg_spectroscopy_failure_low_contrast"
    RYDBERG_SPECTROSCOPY_SUCCESS = "rydberg_spectroscopy_success"
    # t1
    T1_FAILURE_NO_SIGNAL = "t1_failure_no_signal"
    T1_FAILURE_SAMPLING_TOO_COARSE = "t1_failure_sampling_too_coarse"
    T1_FAILURE_WINDOW_TOO_SHORT = "t1_failure_window_too_short"
    T1_SUCCESS = "t1_success"
    # t1_fluctuations
    T1_FLUCTUATIONS_RANDOM_WALK = "t1_fluctuations_random_walk"
    T1_FLUCTUATIONS_STABLE = "t1_fluctuations_stable"
    T1_FLUCTUATIONS_TELEGRAPHIC_FLUCTUATIONS = "t1_fluctuations_telegraphic_fluctuations"
    # tweezer_array
    TWEEZER_ARRAY_FAILURE_ABERRATED = "tweezer_array_failure_aberrated"
    TWEEZER_ARRAY_SUCCESS = "tweezer_array_success"


# 实验家族背景描述
EXPERIMENT_BACKGROUNDS = {
    "coupler_flux": (
        "This is tunable coupler spectroscopy: we map the coupler's frequency response vs applied flux bias. "
        "A successful result shows a clear coupler dispersion curve with a good fit."
    ),
    "cz_benchmarking": (
        "This is CZ (controlled-Z) gate benchmarking on pairs of neutral atoms. "
        "It measures atom retention probability and cycle polarization as a function of circuit depth. "
        "A successful result shows both retention and polarization close to 1 with gradual decay."
    ),
    "drag": (
        "This is a DRAG calibration: we sweep 1/alpha to find the optimal value that minimizes leakage. "
        "A successful result has the zero-crossing of fitted curves clearly observable in the sweep window."
    ),
    "gmm": (
        "This is a single-shot readout discrimination experiment: the I-Q scatter plot shows measurement results "
        "for |0⟩ and |1⟩ states fitted with a Gaussian Mixture Model. "
        "A successful result has two well-separated clusters."
    ),
    "microwave_ramsey": (
        "This is a Ramsey experiment on the ground-state clock qubit using microwave pulses. "
        "A successful result shows sinusoidal oscillations with contrast close to 1 and data well-fit by the curve."
    ),
    "mot_loading": (
        "This is a MOT (magneto-optical trap) loading image: a camera captures the fluorescence of trapped atoms. "
        "A successful result shows a well-defined, compact atomic cloud in the view."
    ),
    "pinchoff": (
        "This is an electron-on-helium pinch-off measurement: a 1D current trace is measured as a function of gate voltage. "
        "The measurement determines whether the device has pinched off — transitioning from conducting to non-conducting state. "
        "Key features are the saturation region, transition region, and pinch-off region."
    ),
    "pingpong": (
        "This is a PingPong amplitude calibration: repeated pi-pulse pairs are applied and qubit population is measured vs gate count. "
        "A successful result shows error accumulation that can be fitted linearly."
    ),
    "qubit_flux_spectroscopy": (
        "This is flux-dependent qubit spectroscopy: a 2D map of qubit transition frequency vs applied flux bias. "
        "A successful result shows a clear dispersion curve (arc or parabola) with a good fit overlaid."
    ),
    "qubit_spectroscopy": (
        "This is a qubit spectroscopy experiment: we sweep drive frequency to find the qubit transition. "
        "A successful result has a single clear spectral peak with a good Lorentzian fit."
    ),
    "qubit_spectroscopy_power_frequency": (
        "This is a 2D qubit spectroscopy experiment: we sweep both drive power and frequency to map qubit transitions. "
        "A successful result shows clear transition lines (f01, and optionally f02/2) with visible power dependence."
    ),
    "rabi": (
        "This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude where the qubit population inverts. "
        "A successful result shows clear sinusoidal oscillations with a fit that tracks the data closely."
    ),
    "rabi_hw": (
        "This is a Rabi experiment: we sweep pulse amplitude to find the pi-pulse amplitude where the qubit population inverts. "
        "A successful result shows clear sinusoidal oscillations with a fit that tracks the data closely."
    ),
    "ramsey_charge_tomography": (
        "This is a Ramsey charge tomography scan: repeated Ramsey measurements over time form a 2D map revealing charge jump events. "
        "A clean result shows continuous, undisturbed fringes."
    ),
    "ramsey_freq_cal": (
        "This is a Ramsey frequency calibration experiment: two π/2 pulses separated by a variable delay measure frequency detuning. "
        "A successful result shows clear oscillations at the detuning frequency with a fit that accurately extracts the frequency offset."
    ),
    "ramsey_t2star": (
        "This is a Ramsey T2* dephasing experiment: two π/2 pulses separated by a variable delay measure the dephasing time T2*. "
        "A successful result shows decaying oscillations with a fit that accurately extracts T2*."
    ),
    "res_spec": (
        "This is a resonator spectroscopy experiment: we sweep probe frequency to find the resonator resonance. "
        "A successful result has a clear resonance feature (dip or peak)."
    ),
    "rydberg_ramsey": (
        "This is a Ramsey experiment on the ground-to-Rydberg transition: two π/2 pulses separated by variable delay measure "
        "the coherence time (T2) and detuning frequency. A successful result shows clear oscillations."
    ),
    "rydberg_spectroscopy": (
        "This is Rydberg transition spectroscopy: optical detuning is swept across multiple atomic sites to locate the transition frequency. "
        "A successful result shows clear spectral features with good fits and high contrast across sites."
    ),
    "t1": (
        "This is a T1 relaxation experiment: after exciting the qubit to |1⟩, we measure population vs delay time. "
        "A successful result shows a clear exponential decay from high to low population with a good fit."
    ),
    "t1_fluctuations": (
        "This is a T1 stability measurement: T1 relaxation time is tracked over repeated measurements. "
        "A successful result shows stable T1 values with minimal drift or jumps."
    ),
    "tweezer_array": (
        "This is a camera image of an optical tweezer array used to trap neutral atoms in a regular grid. "
        "A successful image shows sharp, uniform, well-separated spots indicating proper aberration correction."
    ),
}


# Q5 参数提取 Schema (按实验家族)
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


# Q6 评估状态的成功/失败标准 (按实验家族)
EVALUATE_STATUS_CRITERIA = {
    "drag": {
        "SUCCESS": "Zero-crossing clearly observable in sweep window",
        "NO_SIGNAL": "Flat or random, no crossing pattern",
        "OPTIMAL_NOT_CENTERED": "Crossing exists but in first/last quarter or outside range",
    },
    "rabi": {
        "SUCCESS": "Clear sinusoidal oscillations with good fit",
        "NO_SIGNAL": "Flat or random, no oscillations",
        "OPTIMAL_NOT_CENTERED": "Oscillations visible but heavily distorted",
    },
    "t1": {
        "SUCCESS": "Clear exponential decay with good fit",
        "NO_SIGNAL": "Flat or random, no decay pattern",
        "OPTIMAL_NOT_CENTERED": "Decay visible but fit quality poor",
    },
    "ramsey_t2star": {
        "SUCCESS": "Clear decaying oscillations with good fit",
        "NO_SIGNAL": "Flat or random, no oscillations",
        "OPTIMAL_NOT_CENTERED": "Oscillations visible but heavily damped",
    },
    "qubit_spectroscopy": {
        "SUCCESS": "Clear spectral peak with good Lorentzian fit",
        "NO_SIGNAL": "Flat or random, no peaks",
        "OPTIMAL_NOT_CENTERED": "Peaks visible but multiple/unclear",
    },
    "res_spec": {
        "SUCCESS": "Clear resonance feature (dip or peak)",
        "NO_SIGNAL": "Flat or random, no resonance",
        "OPTIMAL_NOT_CENTERED": "Resonance visible but very weak",
    },
    "gmm": {
        "SUCCESS": "Two well-separated clusters",
        "NO_SIGNAL": "Single blob or random scatter",
        "OPTIMAL_NOT_CENTERED": "Clusters touching or heavily overlapping",
    },
    "default": {
        "SUCCESS": "Clear signal with good fit",
        "NO_SIGNAL": "Flat or random, no meaningful pattern",
        "OPTIMAL_NOT_CENTERED": "Signal visible but quality poor",
    },
}


def get_experiment_background(experiment_family: str) -> str:
    """获取实验背景描述"""
    return EXPERIMENT_BACKGROUNDS.get(
        experiment_family,
        EXPERIMENT_BACKGROUNDS.get("default", "This is a quantum calibration experiment.")
    )


def get_extract_params_schema(experiment_family: str) -> dict:
    """获取参数提取的JSON Schema"""
    return EXTRACT_PARAMS_SCHEMAS.get(
        experiment_family,
        {"type": "object", "properties": {}}
    )


def get_evaluate_status_criteria(experiment_family: str) -> dict[str, str]:
    """获取状态评估标准"""
    return EVALUATE_STATUS_CRITERIA.get(experiment_family, EVALUATE_STATUS_CRITERIA["default"])


__all__ = [
    "ExperimentFamily",
    "ExperimentType",
    "EXPERIMENT_BACKGROUNDS",
    "EXTRACT_PARAMS_SCHEMAS",
    "EVALUATE_STATUS_CRITERIA",
    "get_experiment_background",
    "get_extract_params_schema",
    "get_evaluate_status_criteria",
]