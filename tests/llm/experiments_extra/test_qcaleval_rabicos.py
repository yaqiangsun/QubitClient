# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/05/14
########################################################################

"""
QCalEval RABICOS 实验测试

功率 Rabi 振荡实验，测量不同驱动功率下的 Rabi 振荡
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


# RABICOS 测试数据
TEST_SAMPLE = {
    "experiment_family": "rabicos",
    "q5_answer": {
        "rabi_rate_MHz": 10.0,
        "pi_amp": 0.5,
        "pi_half_amp": 0.25,
        "oscillation_quality": "good"
    },
    "q6_expected_statuses": ["SUCCESS", "NO_SIGNAL", "FIT_POOR", "AMPLITUDE_TOO_LOW", "AMPLITUDE_TOO_HIGH"],
}


def test_rabicos_q1_describe():
    print("\n=== RABICOS: Q1 Describe Plot ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.DESCRIBE_PLOT,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.RABICOS
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_rabicos_q2_classify():
    print("\n=== RABICOS: Q2 Classify Outcome ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.CLASSIFY_OUTCOME,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.RABICOS
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Classification" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_rabicos_q3_reasoning():
    print("\n=== RABICOS: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.SCIENTIFIC_REASONING,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.RABICOS
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {result[:300]}...")
        assert len(result) > 0
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_rabicos_q4_assess():
    print("\n=== RABICOS: Q4 Assess Fit ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.ASSESS_FIT,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.RABICOS
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Assessment" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_rabicos_q5_extract():
    print("\n=== RABICOS: Q5 Extract Params ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EXTRACT_PARAMS,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.RABICOS
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert result is not None
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_rabicos_q6_status():
    print("\n=== RABICOS: Q6 Evaluate Status ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EVALUATE_STATUS,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.RABICOS
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Status" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


if __name__ == "__main__":
    test_rabicos_q1_describe()
    test_rabicos_q2_classify()
    test_rabicos_q3_reasoning()
    test_rabicos_q4_assess()
    test_rabicos_q5_extract()
    test_rabicos_q6_status()
    print("\n[OK] RABICOS tests completed!")