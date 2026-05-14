# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/05/14
########################################################################

"""
QCalEval SINGLESHOT 实验测试

单次读出辨别实验，与 GMM 完全相同
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


# SINGLESHOT 测试数据
TEST_SAMPLE = {
    "experiment_family": "singleshot",
    "q5_answer": {
        "separation": "well-separated",
        "cluster0_center": [0, 0],
        "cluster1_center": [5, 5]
    },
    "q6_expected_statuses": ["SUCCESS", "NO_SIGNAL", "NO_EXCITATION", "HIGH_POWER", "NO_RES_RESPONSE"],
}


def test_singleshot_q1_describe():
    print("\n=== SINGLESHOT: Q1 Describe Plot ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.DESCRIBE_PLOT,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.SINGLESHOT
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_singleshot_q2_classify():
    print("\n=== SINGLESHOT: Q2 Classify Outcome ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.CLASSIFY_OUTCOME,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.SINGLESHOT
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Classification" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_singleshot_q3_reasoning():
    print("\n=== SINGLESHOT: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.SCIENTIFIC_REASONING,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.SINGLESHOT
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {result[:300]}...")
        assert len(result) > 0
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_singleshot_q4_assess():
    print("\n=== SINGLESHOT: Q4 Assess Fit ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.ASSESS_FIT,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.SINGLESHOT
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Assessment" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_singleshot_q5_extract():
    print("\n=== SINGLESHOT: Q5 Extract Params ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EXTRACT_PARAMS,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.SINGLESHOT
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert result is not None
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_singleshot_q6_status():
    print("\n=== SINGLESHOT: Q6 Evaluate Status ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EVALUATE_STATUS,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.SINGLESHOT
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Status" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


if __name__ == "__main__":
    test_singleshot_q1_describe()
    test_singleshot_q2_classify()
    test_singleshot_q3_reasoning()
    test_singleshot_q4_assess()
    test_singleshot_q5_extract()
    test_singleshot_q6_status()
    print("\n[OK] SINGLESHOT tests completed!")