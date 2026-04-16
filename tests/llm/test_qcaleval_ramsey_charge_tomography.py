# -*- coding: utf-8 -*-
"""QCalEval Ramsey_Charge_Tomography 实验测试"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM
from qubitclient.llm.task import LLMTaskName


# Ramsey_Charge_Tomography 测试数据
TEST_SAMPLE = {
    "id": "ramsey_charge_tomography_clean_a",
    "experiment_type": "ramsey_charge_tomography_clean",
    "experiment_family": "ramsey_charge_tomography",
    "image_filename": "cae1a8d2b58e0837.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Expected behavior",
    "q4_answer": "No",
    "q5_answer": {
  "event_detected": False,
  "jump_count": 0,
  "jump_positions": [],
  "jump_sizes_mV": []
},
    "q6_expected_status": "NO_EVENT",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images", filename)


def test_ramsey_charge_tomography_q1_describe():
    print("\n=== Ramsey_Charge_Tomography: Q1 Describe Plot ===")
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


def test_ramsey_charge_tomography_q2_classify():
    print("\n=== Ramsey_Charge_Tomography: Q2 Classify Outcome ===")
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


def test_ramsey_charge_tomography_q3_reasoning():
    print("\n=== Ramsey_Charge_Tomography: Q3 Scientific Reasoning ===")
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


def test_ramsey_charge_tomography_q4_assess():
    print("\n=== Ramsey_Charge_Tomography: Q4 Assess Fit ===")
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


def test_ramsey_charge_tomography_q5_extract():
    print("\n=== Ramsey_Charge_Tomography: Q5 Extract Params ===")
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


def test_ramsey_charge_tomography_q6_status():
    print("\n=== Ramsey_Charge_Tomography: Q6 Evaluate Status ===")
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
    test_ramsey_charge_tomography_q1_describe()
    test_ramsey_charge_tomography_q2_classify()
    test_ramsey_charge_tomography_q3_reasoning()
    test_ramsey_charge_tomography_q4_assess()
    test_ramsey_charge_tomography_q5_extract()
    test_ramsey_charge_tomography_q6_status()
    print("\n✓ Ramsey_Charge_Tomography tests passed!")
