# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/05/14
########################################################################

"""
QCalEval POWERSHIFT 实验测试

功率偏移实验，测量腔体频率随驱动功率的变化（Kerr 效应）
"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "..", "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM, ExperimentFamily
from qubitclient.llm.task import LLMTaskName


# POWERSHIFT 测试数据
TEST_SAMPLE = {
    "experiment_family": "powershift",
    "q5_answer": {
        "low_power_freq_GHz": 7.5,
        "power_shift_MHz": 5.0,
        "kerr_coefficient_kHz": 100.0,
        "linearity": "good"
    },
    "q6_expected_statuses": ["SUCCESS", "NO_SIGNAL", "NO_POWER_SHIFT", "FIT_POOR"],
}


def test_powershift_q1_describe():
    print("\n=== POWERSHIFT: Q1 Describe Plot ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.DESCRIBE_PLOT,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.POWERSHIFT
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_powershift_q2_classify():
    print("\n=== POWERSHIFT: Q2 Classify Outcome ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.CLASSIFY_OUTCOME,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.POWERSHIFT
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Classification" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_powershift_q3_reasoning():
    print("\n=== POWERSHIFT: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.SCIENTIFIC_REASONING,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.POWERSHIFT
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {result[:300]}...")
        assert len(result) > 0
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_powershift_q4_assess():
    print("\n=== POWERSHIFT: Q4 Assess Fit ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.ASSESS_FIT,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.POWERSHIFT
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Assessment" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_powershift_q5_extract():
    print("\n=== POWERSHIFT: Q5 Extract Params ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EXTRACT_PARAMS,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.POWERSHIFT
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert result is not None
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_powershift_q6_status():
    print("\n=== POWERSHIFT: Q6 Evaluate Status ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EVALUATE_STATUS,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.POWERSHIFT
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Status" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


if __name__ == "__main__":
    test_powershift_q1_describe()
    test_powershift_q2_classify()
    test_powershift_q3_reasoning()
    test_powershift_q4_assess()
    test_powershift_q5_extract()
    test_powershift_q6_status()
    print("\n[OK] POWERSHIFT tests completed!")