# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:34
########################################################################

# -*- coding: utf-8 -*-
"""QCalEval Coupler_Flux 实验测试"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "..", "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM, ExperimentFamily
from qubitclient.llm.task import LLMTaskName


# Coupler_Flux 测试数据
TEST_SAMPLE = {
    "id": "coupler_flux_failure_bad_fit_a",
    "experiment_type": "coupler_flux_failure_bad_fit",
    "experiment_family": "coupler_flux",
    "image_filename": "567471411059a0e3.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Suboptimal parameters",
    "q4_answer": "Unreliable",
    "q5_answer": {
  "crossing_voltages_V": [-0.85, 1.15],
  "left_fig_branch_freqs_GHz": [4.525, 4.515, 4.525],
  "right_fig_branch_freqs_GHz": [4.62, 4.615, 4.625]
},
    "q6_expected_status": "FIT_POOR",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images", filename)


def test_coupler_flux_q1_describe():
    print("\n=== Coupler_Flux: Q1 Describe Plot ===")
    llm = QubitLLM()
    # prompt_data = llm.get_prompt(
    #     LLMTaskName.DESCRIBE_PLOT,
    #     image_data=get_image_path(TEST_SAMPLE["image_filename"]),
    #     experiment_family=ExperimentFamily.COUPLER_FLUX
    # )
    # result = llm.chat(**prompt_data)
    result = llm.run(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.COUPLER_FLUX
    )
    print(f"  结果: {str(result)[:800]}...")
    assert "plot_type" in result
    print("  ✓")


def test_coupler_flux_q2_classify():
    print("\n=== Coupler_Flux: Q2 Classify Outcome ===")
    llm = QubitLLM()
    # prompt_data = llm.get_prompt(
    #     LLMTaskName.CLASSIFY_OUTCOME,
    #     image_data=get_image_path(TEST_SAMPLE["image_filename"]),
    #     experiment_family=ExperimentFamily.COUPLER_FLUX
    # )
    # result = llm.chat(**prompt_data)
    result = llm.run(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.COUPLER_FLUX
    )
    print(f"  结果: {str(result)[:800]}...")
    assert "Classification" in result
    print("  ✓")


def test_coupler_flux_q3_reasoning():
    print("\n=== Coupler_Flux: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    # prompt_data = llm.get_prompt(
    #     LLMTaskName.SCIENTIFIC_REASONING,
    #     image_data=get_image_path(TEST_SAMPLE["image_filename"]),
    #     experiment_family=ExperimentFamily.COUPLER_FLUX
    # )
    # result = llm.chat(**prompt_data)
    result = llm.run(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.COUPLER_FLUX
    )
    print(f"  结果: {result[:200]}...")
    assert len(result) > 0
    print("  ✓")


def test_coupler_flux_q4_assess():
    print("\n=== Coupler_Flux: Q4 Assess Fit ===")
    llm = QubitLLM()
    # prompt_data = llm.get_prompt(
    #     LLMTaskName.ASSESS_FIT,
    #     image_data=get_image_path(TEST_SAMPLE["image_filename"]),
    #     experiment_family=ExperimentFamily.COUPLER_FLUX
    # )
    # result = llm.chat(**prompt_data)
    result = llm.run(
        LLMTaskName.ASSESS_FIT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.COUPLER_FLUX
    )
    print(f"  结果: {str(result)[:800]}...")
    assert "Assessment" in result
    print("  ✓")


def test_coupler_flux_q5_extract():
    print("\n=== Coupler_Flux: Q5 Extract Params ===")
    llm = QubitLLM()
    # prompt_data = llm.get_prompt(
    #     LLMTaskName.EXTRACT_PARAMS,
    #     image_data=get_image_path(TEST_SAMPLE["image_filename"]),
    #     experiment_family=ExperimentFamily.COUPLER_FLUX
    # )
    # result = llm.chat(**prompt_data)
    result = llm.run(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.COUPLER_FLUX
    )
    print(f"  结果: {str(result)[:800]}...")
    assert result is not None
    print("  ✓")


def test_coupler_flux_q6_status():
    print("\n=== Coupler_Flux: Q6 Evaluate Status ===")
    llm = QubitLLM()
    # prompt_data = llm.get_prompt(
    #     LLMTaskName.EVALUATE_STATUS,
    #     image_data=get_image_path(TEST_SAMPLE["image_filename"]),
    #     experiment_family=ExperimentFamily.COUPLER_FLUX
    # )
    # result = llm.chat(**prompt_data)
    result = llm.run(
        LLMTaskName.EVALUATE_STATUS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.COUPLER_FLUX
    )
    print(f"  结果: {str(result)[:800]}...")
    assert "Status" in result
    print("  ✓")


if __name__ == "__main__":
    test_coupler_flux_q1_describe()
    test_coupler_flux_q2_classify()
    test_coupler_flux_q3_reasoning()
    test_coupler_flux_q4_assess()
    test_coupler_flux_q5_extract()
    test_coupler_flux_q6_status()
    print("\n✓ Coupler_Flux tests passed!")
