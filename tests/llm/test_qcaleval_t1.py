# -*- coding: utf-8 -*-
"""QCalEval T1 实验测试"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM
from qubitclient.llm.task import LLMTaskName


# T1 测试数据
TEST_SAMPLE = {
    "id": "t1_good_decay_a",
    "experiment_type": "t1_good_decay",
    "experiment_family": "t1",
    "image_filename": "2dd184dce63f28dd.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Expected behavior",
    "q4_answer": "Reliable",
    "q5_answer": {"T1_us": 10.0},
    "q6_expected_status": "SUCCESS",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images", filename)


def test_t1_q1():
    print("\n=== T1: Q1 Describe ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)
    assert "plot_type" in result
    print("  ✓")


def test_t1_q2():
    print("\n=== T1: Q2 Classify ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)
    assert "Classification" in result
    print("  ✓")


def test_t1_q3():
    print("\n=== T1: Q3 Reasoning ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)
    assert len(result) > 0
    print("  ✓")


def test_t1_q4():
    print("\n=== T1: Q4 Assess ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.ASSESS_FIT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)
    assert "Assessment" in result
    print("  ✓")


def test_t1_q5():
    print("\n=== T1: Q5 Extract ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)
    assert result is not None
    print("  ✓")


def test_t1_q6():
    print("\n=== T1: Q6 Status ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EVALUATE_STATUS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)
    assert "Status" in result
    print("  ✓")


if __name__ == "__main__":
    test_t1_q1()
    test_t1_q2()
    test_t1_q3()
    test_t1_q4()
    test_t1_q5()
    test_t1_q6()
    print("\n✓ T1 tests passed!")