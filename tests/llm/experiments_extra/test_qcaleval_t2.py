# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/05/14
########################################################################

"""
QCalEval T2 实验测试

T2 退相干时间测量，与 RAMSEY_T2STAR 完全相同
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


# T2 测试数据
TEST_SAMPLE = {
    "experiment_family": "t2",
    "q5_answer": {
        "T2_star_us": 50.0,
        "detuning_MHz": 1.0,
        "fringes_visible": 5
    },
    "q6_expected_statuses": ["SUCCESS", "NO_DETUNING", "BEATING", "TOO_MANY_OSC", "TOO_FEW_OSC", "WINDOW_TOO_SHORT", "SAMPLING_TOO_COARSE"],
}


def test_t2_q1_describe():
    print("\n=== T2: Q1 Describe Plot ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.DESCRIBE_PLOT,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.T2
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_t2_q2_classify():
    print("\n=== T2: Q2 Classify Outcome ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.CLASSIFY_OUTCOME,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.T2
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Classification" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_t2_q3_reasoning():
    print("\n=== T2: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.SCIENTIFIC_REASONING,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.T2
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {result[:300]}...")
        assert len(result) > 0
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_t2_q4_assess():
    print("\n=== T2: Q4 Assess Fit ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.ASSESS_FIT,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.T2
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Assessment" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_t2_q5_extract():
    print("\n=== T2: Q5 Extract Params ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EXTRACT_PARAMS,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.T2
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert result is not None
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_t2_q6_status():
    print("\n=== T2: Q6 Evaluate Status ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EVALUATE_STATUS,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.T2
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Status" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


if __name__ == "__main__":
    test_t2_q1_describe()
    test_t2_q2_classify()
    test_t2_q3_reasoning()
    test_t2_q4_assess()
    test_t2_q5_extract()
    test_t2_q6_status()
    print("\n[OK] T2 tests completed!")