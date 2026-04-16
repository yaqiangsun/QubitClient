# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
Tests for qubitclient.llm.experiments module.
"""

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# ========== Q1: Describe Plot Tests ==========

from qubitclient.llm.experiments.q1_describe_plot import (
    DESCRIBE_PLOT_PROMPTS,
    DESCRIBE_PLOT_RESPONSE_SCHEMA,
    get_describe_plot_prompt,
)


def test_q1_all_families_have_prompts():
    """测试所有实验家族都有 describe_plot prompt"""
    expected_families = [
        "coupler_flux", "cz_benchmarking", "drag", "gmm",
        "microwave_ramsey", "mot_loading", "pinchoff", "pingpong",
        "qubit_flux_spectroscopy", "qubit_spectroscopy",
        "qubit_spectroscopy_power_frequency", "rabi", "rabi_hw",
        "ramsey_charge_tomography", "ramsey_freq_cal", "ramsey_t2star",
        "res_spec", "rydberg_ramsey", "rydberg_spectroscopy",
        "t1", "t1_fluctuations", "tweezer_array",
    ]

    for family in expected_families:
        assert family in DESCRIBE_PLOT_PROMPTS, f"Missing prompt for {family}"
        prompt = DESCRIBE_PLOT_PROMPTS[family]
        assert len(prompt) > 0
        assert "Required fields" in prompt

    print(f"✓ Q1: 所有 {len(expected_families)} 种实验都有 describe_plot prompt")


def test_q1_response_schema():
    """测试 Q1 response schema 结构"""
    assert "properties" in DESCRIBE_PLOT_RESPONSE_SCHEMA
    props = DESCRIBE_PLOT_RESPONSE_SCHEMA["properties"]
    assert "plot_type" in props
    assert "x_axis" in props
    assert "y_axis" in props
    assert "main_features" in props

    # 检查 required
    required = DESCRIBE_PLOT_RESPONSE_SCHEMA.get("required", [])
    assert "plot_type" in required
    assert "x_axis" in required

    print("✓ Q1: Response Schema 结构正确")


def test_q1_get_prompt_function():
    """测试 get_describe_plot_prompt 函数"""
    # 已知实验类型
    prompt = get_describe_plot_prompt("drag")
    assert "DRAG" in prompt

    prompt = get_describe_plot_prompt("rabi")
    assert "Rabi" in prompt

    # 未知实验类型应返回默认
    prompt = get_describe_plot_prompt("unknown_family")
    assert prompt is not None
    assert len(prompt) > 0

    print("✓ Q1: get_describe_plot_prompt 函数正常")


# ========== Q2: Classify Outcome Tests ==========

from qubitclient.llm.experiments.q2_classify_outcome import (
    CLASSIFY_OUTCOME_PROMPTS,
    CLASSIFY_OUTCOME_RESPONSE_SCHEMA,
    get_classify_outcome_prompt,
)


def test_q2_all_families_have_prompts():
    """测试所有实验家族都有 classify_outcome prompt"""
    for family in ["drag", "rabi", "t1", "ramsey_t2star", "gmm"]:
        assert family in CLASSIFY_OUTCOME_PROMPTS, f"Missing prompt for {family}"
        prompt = CLASSIFY_OUTCOME_PROMPTS[family]
        assert "Expected behavior" in prompt or "Options:" in prompt

    print(f"✓ Q2: {len(CLASSIFY_OUTCOME_PROMPTS)} 种实验有 classify_outcome prompt")


def test_q2_response_schema():
    """测试 Q2 response schema"""
    assert "properties" in CLASSIFY_OUTCOME_RESPONSE_SCHEMA
    props = CLASSIFY_OUTCOME_RESPONSE_SCHEMA["properties"]
    assert "Classification" in props
    assert "Reason" in props
    print("✓ Q2: Response Schema 正确")


def test_q2_get_prompt_function():
    """测试 get_classify_outcome_prompt 函数"""
    prompt = get_classify_outcome_prompt("drag")
    assert "Expected behavior" in prompt
    assert "Apparatus issue" in prompt

    prompt = get_classify_outcome_prompt("rabi")
    assert "Expected behavior" in prompt
    assert "Oscillations" in prompt or "oscillations" in prompt

    print("✓ Q2: get_classify_outcome_prompt 函数正常")


# ========== Q3: Scientific Reasoning Tests ==========

from qubitclient.llm.experiments.q3_scientific_reasoning import (
    SCIENTIFIC_REASONING_PROMPTS,
    get_scientific_reasoning_prompt,
)


def test_q3_all_families_have_prompts():
    """测试所有实验家族都有 scientific_reasoning prompt"""
    for family in ["drag", "rabi", "t1", "ramsey_t2star"]:
        assert family in SCIENTIFIC_REASONING_PROMPTS
        prompt = SCIENTIFIC_REASONING_PROMPTS[family]
        assert len(prompt) > 0

    print(f"✓ Q3: {len(SCIENTIFIC_REASONING_PROMPTS)} 种实验有 scientific_reasoning prompt")


def test_q3_get_prompt_function():
    """测试 get_scientific_reasoning_prompt 函数"""
    prompt = get_scientific_reasoning_prompt("drag")
    assert "DRAG" in prompt

    prompt = get_scientific_reasoning_prompt("t1")
    assert "T1" in prompt

    print("✓ Q3: get_scientific_reasoning_prompt 函数正常")


# ========== Q4: Assess Fit Tests ==========

from qubitclient.llm.experiments.q4_assess_fit import (
    ASSESS_FIT_PROMPTS,
    ASSESS_FIT_RESPONSE_SCHEMA,
    get_assess_fit_prompt,
)


def test_q4_all_families_have_prompts():
    """测试所有实验家族都有 assess_fit prompt"""
    for family in ["drag", "rabi", "t1", "ramsey_t2star"]:
        assert family in ASSESS_FIT_PROMPTS
        assert "Reliable" in ASSESS_FIT_PROMPTS[family]

    print(f"✓ Q4: {len(ASSESS_FIT_PROMPTS)} 种实验有 assess_fit prompt")


def test_q4_response_schema():
    """测试 Q4 response schema"""
    props = ASSESS_FIT_RESPONSE_SCHEMA["properties"]
    assert "Assessment" in props
    assert "Reason" in props

    # 检查 Assessment 枚举值
    assessment_enum = props["Assessment"].get("enum", [])
    assert "Reliable" in assessment_enum
    assert "Unreliable" in assessment_enum

    print("✓ Q4: Response Schema 正确")


def test_q4_get_prompt_function():
    """测试 get_assess_fit_prompt 函数"""
    prompt = get_assess_fit_prompt("drag")
    assert "Reliable" in prompt

    print("✓ Q4: get_assess_fit_prompt 函数正常")


# ========== Q5: Extract Params Tests ==========

from qubitclient.llm.experiments.q5_extract_params import (
    EXTRACT_PARAMS_SCHEMAS,
    get_extract_params_schema,
    get_extract_params_prompt,
)


def test_q5_all_families_have_schemas():
    """测试所有实验家族都有 extract_params schema"""
    expected_families = [
        "coupler_flux", "cz_benchmarking", "drag", "gmm",
        "microwave_ramsey", "mot_loading", "pinchoff", "pingpong",
        "qubit_flux_spectroscopy", "qubit_spectroscopy",
        "qubit_spectroscopy_power_frequency", "rabi", "rabi_hw",
        "ramsey_charge_tomography", "ramsey_freq_cal", "ramsey_t2star",
        "res_spec", "rydberg_ramsey", "rydberg_spectroscopy",
        "t1", "t1_fluctuations", "tweezer_array",
    ]

    for family in expected_families:
        assert family in EXTRACT_PARAMS_SCHEMAS, f"Missing schema for {family}"
        schema = EXTRACT_PARAMS_SCHEMAS[family]
        # schema 可以是 object（有 properties）或 array（items 有 properties）
        if schema.get("type") == "object":
            assert "properties" in schema
        elif schema.get("type") == "array":
            assert "items" in schema and "properties" in schema.get("items", {})

    print(f"✓ Q5: 所有 {len(expected_families)} 种实验都有 extract_params schema")


def test_q5_specific_schemas():
    """测试特定实验的 schema 内容"""
    # DRAG schema
    drag_schema = EXTRACT_PARAMS_SCHEMAS["drag"]
    assert "optimal_alpha_inv" in drag_schema["properties"]
    assert "intersection_clear" in drag_schema["properties"]

    # Rabi schema
    rabi_schema = EXTRACT_PARAMS_SCHEMAS["rabi"]
    assert "periods_visible" in rabi_schema["properties"]
    assert "amplitude_decay" in rabi_schema["properties"]

    # T1 schema
    t1_schema = EXTRACT_PARAMS_SCHEMAS["t1"]
    assert "T1_us" in t1_schema["properties"]
    assert "decay_visible" in t1_schema["properties"]

    # GMM schema
    gmm_schema = EXTRACT_PARAMS_SCHEMAS["gmm"]
    assert "separation" in gmm_schema["properties"]

    print("✓ Q5: 特定实验 schema 内容正确")


def test_q5_get_schema_function():
    """测试 get_extract_params_schema 函数"""
    schema = get_extract_params_schema("rabi")
    assert "properties" in schema
    assert "periods_visible" in schema["properties"]

    # 未知类型应返回默认 schema
    schema = get_extract_params_schema("unknown")
    assert "properties" in schema

    print("✓ Q5: get_extract_params_schema 函数正常")


def test_q5_get_prompt_function():
    """测试 get_extract_params_prompt 函数"""
    schema_str = '{"optimal_alpha_inv": "float"}'
    prompt = get_extract_params_prompt("drag", schema_str)
    assert "DRAG" in prompt or "optimal" in prompt

    prompt = get_extract_params_prompt("rabi", '{"periods_visible": "int"}')
    assert "Rabi" in prompt

    print("✓ Q5: get_extract_params_prompt 函数正常")


# ========== Q6: Evaluate Status Tests ==========

from qubitclient.llm.experiments.q6_evaluate_status import (
    EVALUATE_STATUS_PROMPTS,
    EVALUATE_STATUS_RESPONSE_SCHEMA,
    get_evaluate_status_prompt,
)


def test_q6_all_families_have_prompts():
    """测试所有实验家族都有 evaluate_status prompt"""
    for family in ["drag", "rabi", "t1", "gmm"]:
        assert family in EVALUATE_STATUS_PROMPTS
        prompt = EVALUATE_STATUS_PROMPTS[family]
        assert "SUCCESS" in prompt

    print(f"✓ Q6: {len(EVALUATE_STATUS_PROMPTS)} 种实验有 evaluate_status prompt")


def test_q6_response_schema():
    """测试 Q6 response schema"""
    props = EVALUATE_STATUS_RESPONSE_SCHEMA["properties"]
    assert "Status" in props
    assert "Suggested range" in props
    assert "Notes" in props

    # 检查 Status 枚举值
    status_enum = props["Status"].get("enum", [])
    assert "SUCCESS" in status_enum
    assert "NO_SIGNAL" in status_enum
    assert "OPTIMAL_NOT_CENTERED" in status_enum

    print("✓ Q6: Response Schema 正确")


def test_q6_get_prompt_function():
    """测试 get_evaluate_status_prompt 函数"""
    prompt = get_evaluate_status_prompt("drag")
    assert "SUCCESS" in prompt
    assert "NO_SIGNAL" in prompt

    prompt = get_evaluate_status_prompt("rabi")
    assert "SUCCESS" in prompt
    assert "Oscillations" in prompt or "oscillations" in prompt

    print("✓ Q6: get_evaluate_status_prompt 函数正常")


# ========== Experiment Background Tests ==========

from qubitclient.llm.experiments import (
    EXPERIMENT_BACKGROUNDS,
    get_experiment_background,
)


def test_experiment_backgrounds():
    """测试实验背景配置"""
    expected_families = [
        "coupler_flux", "cz_benchmarking", "drag", "gmm",
        "microwave_ramsey", "mot_loading", "pinchoff", "pingpong",
        "qubit_flux_spectroscopy", "qubit_spectroscopy",
        "qubit_spectroscopy_power_frequency", "rabi", "rabi_hw",
        "ramsey_charge_tomography", "ramsey_freq_cal", "ramsey_t2star",
        "res_spec", "rydberg_ramsey", "rydberg_spectroscopy",
        "t1", "t1_fluctuations", "tweezer_array",
    ]

    for family in expected_families:
        assert family in EXPERIMENT_BACKGROUNDS, f"Missing background for {family}"
        bg = EXPERIMENT_BACKGROUNDS[family]
        assert len(bg) > 0

    print(f"✓ 实验背景: {len(EXPERIMENT_BACKGROUNDS)} 种实验")


def test_get_experiment_background_function():
    """测试 get_experiment_background 函数"""
    bg = get_experiment_background("drag")
    assert bg is not None
    assert "DRAG" in bg

    bg = get_experiment_background("rabi")
    assert "Rabi" in bg

    # 未知实验类型应返回通用背景
    bg = get_experiment_background("unknown")
    assert bg is not None

    print("✓ get_experiment_background 函数正常")


# ========== Run All Tests ==========

if __name__ == "__main__":
    # Q1 Tests
    test_q1_all_families_have_prompts()
    test_q1_response_schema()
    test_q1_get_prompt_function()

    # Q2 Tests
    test_q2_all_families_have_prompts()
    test_q2_response_schema()
    test_q2_get_prompt_function()

    # Q3 Tests
    test_q3_all_families_have_prompts()
    test_q3_get_prompt_function()

    # Q4 Tests
    test_q4_all_families_have_prompts()
    test_q4_response_schema()
    test_q4_get_prompt_function()

    # Q5 Tests
    test_q5_all_families_have_schemas()
    test_q5_specific_schemas()
    test_q5_get_schema_function()
    test_q5_get_prompt_function()

    # Q6 Tests
    test_q6_all_families_have_prompts()
    test_q6_response_schema()
    test_q6_get_prompt_function()

    # Experiment Background Tests
    test_experiment_backgrounds()
    test_get_experiment_background_function()

    print("\n✓ All experiment module tests passed!")