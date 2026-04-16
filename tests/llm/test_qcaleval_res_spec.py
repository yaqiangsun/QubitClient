# -*- coding: utf-8 -*-
"""QCalEval Res_Spec 实验测试"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM
from qubitclient.llm.task import LLMTaskName


# Res_Spec 测试数据
TEST_SAMPLE = {
    "id": "res_spec_failure_wide_scan_no_signal_a",
    "experiment_type": "res_spec_failure_wide_scan_no_signal",
    "experiment_family": "res_spec",
    "image_filename": "c58aae9d24dbaee1.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Anomalous behavior",
    "q4_answer": "No",
    "q5_answer": {
  "resonance_freq_GHz": "Unreliable",
  "contrast": "Unreliable"
},
    "q6_expected_status": "NO_SIGNAL",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images", filename)


def test_res_spec_q1_describe():
    print("\n=== Res_Spec: Q1 Describe Plot ===")
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


def test_res_spec_q2_classify():
    print("\n=== Res_Spec: Q2 Classify Outcome ===")
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


def test_res_spec_q3_reasoning():
    print("\n=== Res_Spec: Q3 Scientific Reasoning ===")
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


def test_res_spec_q4_assess():
    print("\n=== Res_Spec: Q4 Assess Fit ===")
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


def test_res_spec_q5_extract():
    print("\n=== Res_Spec: Q5 Extract Params ===")
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


def test_res_spec_q6_status():
    print("\n=== Res_Spec: Q6 Evaluate Status ===")
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
    test_res_spec_q1_describe()
    test_res_spec_q2_classify()
    test_res_spec_q3_reasoning()
    test_res_spec_q4_assess()
    test_res_spec_q5_extract()
    test_res_spec_q6_status()
    print("\n✓ Res_Spec tests passed!")
