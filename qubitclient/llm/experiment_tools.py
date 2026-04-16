# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/16 13:21:01
########################################################################

"""
Prompt 工具模块 - 枚举定义

包含实验家族和实验类型的枚举定义
"""

from enum import Enum, unique


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


__all__ = ["ExperimentFamily", "ExperimentType"]