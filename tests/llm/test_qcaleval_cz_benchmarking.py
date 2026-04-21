# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:34
########################################################################

# -*- coding: utf-8 -*-
"""QCalEval Cz_Benchmarking 实验测试"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM, ExperimentFamily
from qubitclient.llm.task import LLMTaskName


# Cz_Benchmarking 测试数据
TEST_SAMPLE = {
    "id": "cz_benchmarking_success_a",
    "experiment_type": "cz_benchmarking_success",
    "experiment_family": "cz_benchmarking",
    "image_filename": "acdbca020a5f6f7d.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Expected behavior",
    "q4_answer": "Reliable",
    "q5_answer": {
  "site_indices": [9, 11],
  "retention_per_cz": 0.9955,
  "retention_per_cz_unc": 0.0004,
  "cycle_polarization": 0.9968,
  "cycle_polarization_unc": 0.0006,
  "chi_squared_retention": 0.519,
  "chi_squared_polarization": 0.646,
  "max_circuit_depth": 24
},
    "q6_expected_status": "SUCCESS",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images", filename)


def test_cz_benchmarking_q1_describe():
    print("\n=== Cz_Benchmarking: Q1 Describe Plot ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.CZ_BENCHMARKING
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "plot_type" in result
    print("  ✓")


def test_cz_benchmarking_q2_classify():
    print("\n=== Cz_Benchmarking: Q2 Classify Outcome ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.CZ_BENCHMARKING
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Classification" in result
    print("  ✓")


def test_cz_benchmarking_q3_reasoning():
    print("\n=== Cz_Benchmarking: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.CZ_BENCHMARKING
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {result[:200]}...")
    assert len(result) > 0
    print("  ✓")


def test_cz_benchmarking_q4_assess():
    print("\n=== Cz_Benchmarking: Q4 Assess Fit ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.ASSESS_FIT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.CZ_BENCHMARKING
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Assessment" in result
    print("  ✓")


def test_cz_benchmarking_q5_extract():
    print("\n=== Cz_Benchmarking: Q5 Extract Params ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.CZ_BENCHMARKING
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert result is not None
    print("  ✓")


def test_cz_benchmarking_q6_status():
    print("\n=== Cz_Benchmarking: Q6 Evaluate Status ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EVALUATE_STATUS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.CZ_BENCHMARKING
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Status" in result
    print("  ✓")


if __name__ == "__main__":
    test_cz_benchmarking_q1_describe()
    test_cz_benchmarking_q2_classify()
    test_cz_benchmarking_q3_reasoning()
    test_cz_benchmarking_q4_assess()
    test_cz_benchmarking_q5_extract()
    test_cz_benchmarking_q6_status()
    print("\n✓ Cz_Benchmarking tests passed!")
