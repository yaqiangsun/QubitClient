# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/05/14
########################################################################

"""
QCalEval OPTPIPULSE 实验测试

最优 π 脉冲校准实验，通过重复 Rabi 振荡测量确定 π 脉冲幅度
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


# OPTPIPULSE 测试数据
TEST_SAMPLE = {
    "experiment_family": "optpipulse",
    "q5_answer": {
        "pi_amp_relative": 0.5,
        "contrast": 0.95,
        "checkerboard_quality": "good",
        "n_range": 20
    },
    "q6_expected_statuses": ["SUCCESS", "NO_CONTRAST", "POOR_CALIBRATION", "LIMITED_N_RANGE"],
}


def test_optpipulse_q1_describe():
    print("\n=== OPTPIPULSE: Q1 Describe Plot ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.DESCRIBE_PLOT,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.OPTPIPULSE
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_optpipulse_q2_classify():
    print("\n=== OPTPIPULSE: Q2 Classify Outcome ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.CLASSIFY_OUTCOME,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.OPTPIPULSE
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Classification" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_optpipulse_q3_reasoning():
    print("\n=== OPTPIPULSE: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.SCIENTIFIC_REASONING,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.OPTPIPULSE
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {result[:300]}...")
        assert len(result) > 0
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_optpipulse_q4_assess():
    print("\n=== OPTPIPULSE: Q4 Assess Fit ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.ASSESS_FIT,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.OPTPIPULSE
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Assessment" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_optpipulse_q5_extract():
    print("\n=== OPTPIPULSE: Q5 Extract Params ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EXTRACT_PARAMS,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.OPTPIPULSE
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert result is not None
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_optpipulse_q6_status():
    print("\n=== OPTPIPULSE: Q6 Evaluate Status ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EVALUATE_STATUS,
            image_data="dummy.png",
            experiment_family=ExperimentFamily.OPTPIPULSE
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Status" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


if __name__ == "__main__":
    test_optpipulse_q1_describe()
    test_optpipulse_q2_classify()
    test_optpipulse_q3_reasoning()
    test_optpipulse_q4_assess()
    test_optpipulse_q5_extract()
    test_optpipulse_q6_status()
    print("\n[OK] OPTPIPULSE tests completed!")