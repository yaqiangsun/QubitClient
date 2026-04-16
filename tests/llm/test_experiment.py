# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""Tests for qubitclient.llm.experiment module."""

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm.experiments import (
    EXPERIMENT_BACKGROUNDS,
    get_experiment_background,
)

from qubitclient.llm.experiments.q5_extract_params import (
    EXTRACT_PARAMS_SCHEMAS,
    get_extract_params_schema,
)


def test_experiment_backgrounds():
    """测试实验背景配置"""
    # 检查关键实验类型
    assert "drag" in EXPERIMENT_BACKGROUNDS
    assert "rabi" in EXPERIMENT_BACKGROUNDS
    assert "t1" in EXPERIMENT_BACKGROUNDS
    assert "ramsey_t2star" in EXPERIMENT_BACKGROUNDS
    assert "qubit_spectroscopy" in EXPERIMENT_BACKGROUNDS

    # 检查内容
    assert "DRAG" in EXPERIMENT_BACKGROUNDS["drag"]
    assert "Rabi" in EXPERIMENT_BACKGROUNDS["rabi"]
    assert "T1" in EXPERIMENT_BACKGROUNDS["t1"]

    print(f"✓ 实验背景配置: {len(EXPERIMENT_BACKGROUNDS)} 种实验")


def test_extract_params_schemas():
    """测试参数提取Schema"""
    # 检查关键实验类型
    assert "drag" in EXTRACT_PARAMS_SCHEMAS
    assert "rabi" in EXTRACT_PARAMS_SCHEMAS
    assert "t1" in EXTRACT_PARAMS_SCHEMAS

    # 检查Schema内容
    drag_schema = EXTRACT_PARAMS_SCHEMAS["drag"]
    assert "properties" in drag_schema
    assert "intersection_clear" in drag_schema["properties"]

    rabi_schema = EXTRACT_PARAMS_SCHEMAS["rabi"]
    assert "periods_visible" in rabi_schema["properties"]
    assert "amplitude_decay" in rabi_schema["properties"]

    t1_schema = EXTRACT_PARAMS_SCHEMAS["t1"]
    assert "T1_us" in t1_schema["properties"]
    assert "decay_visible" in t1_schema["properties"]

    print(f"✓ 参数提取Schema: {len(EXTRACT_PARAMS_SCHEMAS)} 种实验")


def test_get_experiment_background():
    """测试获取实验背景函数"""
    # 已知实验类型
    bg = get_experiment_background("drag")
    assert bg is not None
    assert "DRAG" in bg

    bg = get_experiment_background("rabi")
    assert "Rabi" in bg

    # 未知实验类型
    bg = get_experiment_background("unknown_experiment")
    assert bg is not None
    assert len(bg) > 0

    print("✓ get_experiment_background 函数正常")


def test_get_extract_params_schema():
    """测试获取参数提取Schema函数"""
    # 已知实验类型
    schema = get_extract_params_schema("rabi")
    assert schema is not None
    assert "properties" in schema

    schema = get_extract_params_schema("t1")
    assert "T1_us" in schema["properties"]

    # 未知实验类型
    schema = get_extract_params_schema("unknown")
    assert schema is not None
    assert "properties" in schema

    print("✓ get_extract_params_schema 函数正常")


def test_all_families_have_backgrounds():
    """测试所有实验家族都有背景描述"""
    # QCalEval中的22种实验家族
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
        assert family in EXTRACT_PARAMS_SCHEMAS, f"Missing schema for {family}"

    print(f"✓ 所有 {len(expected_families)} 种实验家族配置完整")


if __name__ == "__main__":
    test_experiment_backgrounds()
    test_extract_params_schemas()
    test_get_experiment_background()
    test_get_extract_params_schema()
    test_all_families_have_backgrounds()
    print("\n✓ All experiment module tests passed!")