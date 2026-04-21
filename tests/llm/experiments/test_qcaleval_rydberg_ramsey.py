# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:34
########################################################################

# -*- coding: utf-8 -*-
"""QCalEval Rydberg_Ramsey 实验测试"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "..", "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM, ExperimentFamily
from qubitclient.llm.task import LLMTaskName


# Rydberg_Ramsey 测试数据
TEST_SAMPLE = {
    "id": "rydberg_ramsey_success_a",
    "experiment_type": "rydberg_ramsey_success",
    "experiment_family": "rydberg_ramsey",
    "image_filename": "6d156053fe63ae83.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Expected behavior",
    "q4_answer": "Reliable",
    "q5_answer": {
  "frequency_MHz": 9.937,
  "frequency_MHz_unc": 0.002,
  "T2_us": 9.7,
  "T2_us_unc": 0.9,
  "RChi2": 1.3,
  "frequency_noise_kHz": 23.1
},
    "q6_expected_status": "SUCCESS",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images", filename)


def test_rydberg_ramsey_q1_describe():
    print("\n=== Rydberg_Ramsey: Q1 Describe Plot ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.RYDBERG_RAMSEY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "plot_type" in result
    print("  ✓")


def test_rydberg_ramsey_q2_classify():
    print("\n=== Rydberg_Ramsey: Q2 Classify Outcome ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.RYDBERG_RAMSEY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Classification" in result
    print("  ✓")


def test_rydberg_ramsey_q3_reasoning():
    print("\n=== Rydberg_Ramsey: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.RYDBERG_RAMSEY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {result[:200]}...")
    assert len(result) > 0
    print("  ✓")


def test_rydberg_ramsey_q4_assess():
    print("\n=== Rydberg_Ramsey: Q4 Assess Fit ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.ASSESS_FIT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.RYDBERG_RAMSEY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Assessment" in result
    print("  ✓")


def test_rydberg_ramsey_q5_extract():
    print("\n=== Rydberg_Ramsey: Q5 Extract Params ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.RYDBERG_RAMSEY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert result is not None
    print("  ✓")


def test_rydberg_ramsey_q6_status():
    print("\n=== Rydberg_Ramsey: Q6 Evaluate Status ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EVALUATE_STATUS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.RYDBERG_RAMSEY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Status" in result
    print("  ✓")


if __name__ == "__main__":
    test_rydberg_ramsey_q1_describe()
    test_rydberg_ramsey_q2_classify()
    test_rydberg_ramsey_q3_reasoning()
    test_rydberg_ramsey_q4_assess()
    test_rydberg_ramsey_q5_extract()
    test_rydberg_ramsey_q6_status()
    print("\n✓ Rydberg_Ramsey tests passed!")
