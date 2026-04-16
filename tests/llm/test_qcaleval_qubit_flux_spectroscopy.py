# -*- coding: utf-8 -*-
"""QCalEval Qubit_Flux_Spectroscopy 实验测试"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM
from qubitclient.llm.task import LLMTaskName


# Qubit_Flux_Spectroscopy 测试数据
TEST_SAMPLE = {
    "id": "qubit_flux_spectroscopy_failure_bad_fit_b",
    "experiment_type": "qubit_flux_spectroscopy_failure_bad_fit",
    "experiment_family": "qubit_flux_spectroscopy",
    "image_filename": "8adb985e09f38830.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Suboptimal parameters",
    "q4_answer": "Unreliable",
    "q5_answer": {
  "num_resonances": 2,
  "resonance_freq_GHz": "Unreliable"
},
    "q6_expected_status": "FIT_POOR",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images", filename)


def test_qubit_flux_spectroscopy_q1_describe():
    print("\n=== Qubit_Flux_Spectroscopy: Q1 Describe Plot ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "plot_type" in result
    print("  ✓")


def test_qubit_flux_spectroscopy_q2_classify():
    print("\n=== Qubit_Flux_Spectroscopy: Q2 Classify Outcome ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Classification" in result
    print("  ✓")


def test_qubit_flux_spectroscopy_q3_reasoning():
    print("\n=== Qubit_Flux_Spectroscopy: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {result[:200]}...")
    assert len(result) > 0
    print("  ✓")


def test_qubit_flux_spectroscopy_q4_assess():
    print("\n=== Qubit_Flux_Spectroscopy: Q4 Assess Fit ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.ASSESS_FIT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Assessment" in result
    print("  ✓")


def test_qubit_flux_spectroscopy_q5_extract():
    print("\n=== Qubit_Flux_Spectroscopy: Q5 Extract Params ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert result is not None
    print("  ✓")


def test_qubit_flux_spectroscopy_q6_status():
    print("\n=== Qubit_Flux_Spectroscopy: Q6 Evaluate Status ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EVALUATE_STATUS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Status" in result
    print("  ✓")


if __name__ == "__main__":
    test_qubit_flux_spectroscopy_q1_describe()
    test_qubit_flux_spectroscopy_q2_classify()
    test_qubit_flux_spectroscopy_q3_reasoning()
    test_qubit_flux_spectroscopy_q4_assess()
    test_qubit_flux_spectroscopy_q5_extract()
    test_qubit_flux_spectroscopy_q6_status()
    print("\n✓ Qubit_Flux_Spectroscopy tests passed!")
