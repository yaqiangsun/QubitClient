# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:34
########################################################################

# -*- coding: utf-8 -*-
"""QCalEval Gmm 实验测试"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "..", "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM, ExperimentFamily
from qubitclient.llm.task import LLMTaskName


# Gmm 测试数据
TEST_SAMPLE = {
    "id": "gmm_failure_high_power_a",
    "experiment_type": "gmm_failure_high_power",
    "experiment_family": "gmm",
    "image_filename": "fbc8b87a58704a1c.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Suboptimal parameters",
    "q4_answer": "Unreliable",
    "q5_answer": {
  "separation": "Unreliable",
  "cluster0_center": "Unreliable",
  "cluster1_center": "Unreliable"
},
    "q6_expected_status": "HIGH_POWER",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images", filename)


def test_gmm_q1_describe():
    print("\n=== Gmm: Q1 Describe Plot ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.GMM
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert "plot_type" in result
    print("  ✓")


def test_gmm_q2_classify():
    print("\n=== Gmm: Q2 Classify Outcome ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.GMM
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert "Classification" in result
    print("  ✓")


def test_gmm_q3_reasoning():
    print("\n=== Gmm: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.GMM
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {result[:200]}...")
    assert len(result) > 0
    print("  ✓")


def test_gmm_q4_assess():
    print("\n=== Gmm: Q4 Assess Fit ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.ASSESS_FIT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.GMM
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert "Assessment" in result
    print("  ✓")


def test_gmm_q5_extract():
    print("\n=== Gmm: Q5 Extract Params ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.GMM
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert result is not None
    print("  ✓")


def test_gmm_q6_status():
    print("\n=== Gmm: Q6 Evaluate Status ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EVALUATE_STATUS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.GMM
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert "Status" in result
    print("  ✓")


if __name__ == "__main__":
    test_gmm_q1_describe()
    test_gmm_q2_classify()
    test_gmm_q3_reasoning()
    test_gmm_q4_assess()
    test_gmm_q5_extract()
    test_gmm_q6_status()
    print("\n✓ Gmm tests passed!")
