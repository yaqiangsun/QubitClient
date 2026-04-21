# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:34
########################################################################

# -*- coding: utf-8 -*-
"""QCalEval Rabi_Hw 实验测试"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "..", "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM, ExperimentFamily
from qubitclient.llm.task import LLMTaskName


# Rabi_Hw 测试数据
TEST_SAMPLE = {
    "id": "rabi_hw_failure_incorrect_fit_c",
    "experiment_type": "rabi_hw_failure_incorrect_fit",
    "experiment_family": "rabi_hw",
    "image_filename": "d209871206308bed.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Suboptimal parameters",
    "q4_answer": "Unreliable",
    "q5_answer": {
  "periods_visible": 6.0,
  "amplitude_decay": "stable",
  "signal_quality": "noisy"
},
    "q6_expected_status": "FIT_POOR",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images", filename)


def test_rabi_hw_q1_describe():
    print("\n=== Rabi_Hw: Q1 Describe Plot ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.RABI_HW
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "plot_type" in result
    print("  ✓")


def test_rabi_hw_q2_classify():
    print("\n=== Rabi_Hw: Q2 Classify Outcome ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.RABI_HW
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Classification" in result
    print("  ✓")


def test_rabi_hw_q3_reasoning():
    print("\n=== Rabi_Hw: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.RABI_HW
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {result[:200]}...")
    assert len(result) > 0
    print("  ✓")


def test_rabi_hw_q4_assess():
    print("\n=== Rabi_Hw: Q4 Assess Fit ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.ASSESS_FIT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.RABI_HW
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Assessment" in result
    print("  ✓")


def test_rabi_hw_q5_extract():
    print("\n=== Rabi_Hw: Q5 Extract Params ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.RABI_HW
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert result is not None
    print("  ✓")


def test_rabi_hw_q6_status():
    print("\n=== Rabi_Hw: Q6 Evaluate Status ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EVALUATE_STATUS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.RABI_HW
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Status" in result
    print("  ✓")


if __name__ == "__main__":
    test_rabi_hw_q1_describe()
    test_rabi_hw_q2_classify()
    test_rabi_hw_q3_reasoning()
    test_rabi_hw_q4_assess()
    test_rabi_hw_q5_extract()
    test_rabi_hw_q6_status()
    print("\n✓ Rabi_Hw tests passed!")
