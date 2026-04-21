# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:34
########################################################################

# -*- coding: utf-8 -*-
"""Fewshot 模式评估测试 - PingPong 实验"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM, ExperimentFamily
from qubitclient.llm.task import LLMTaskName


# PingPong 测试数据
TEST_SAMPLE = {
    "id": "pingpong_failure_large_error_a",
    "experiment_type": "pingpong_failure_large_error",
    "experiment_family": "pingpong",
    "image_filename": "3b81b57fe995cf71.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Anomalous behavior",
    "q4_answer": "Unreliable",
    "q6_expected_status": "LARGE_ERROR",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images", filename)


def test_pingpong_q1_zeroshot():
    """Q1 Zero-shot 测试"""
    print("\n=== PingPong Q1: Describe Plot (Zero-shot) ===")
    llm = QubitLLM()
    result = llm.run(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.PINGPONG,
        fewshot=False
    )
    print(f"  结果: {str(result)[:200]}...")
    assert "plot_type" in result
    print("  ✓")


def test_pingpong_q1_fewshot():
    """Q1 Few-shot 测试"""
    print("\n=== PingPong Q1: Describe Plot (Few-shot) ===")
    llm = QubitLLM()
    result = llm.run(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.PINGPONG,
        fewshot=True
    )
    print(f"  结果: {str(result)[:200]}...")
    assert "plot_type" in result
    print("  ✓")


def test_pingpong_q2_zeroshot():
    """Q2 Zero-shot 测试"""
    print("\n=== PingPong Q2: Classify Outcome (Zero-shot) ===")
    llm = QubitLLM()
    result = llm.run(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.PINGPONG,
        fewshot=False
    )
    print(f"  结果: {str(result)[:200]}...")
    assert "Classification" in result
    print("  ✓")


def test_pingpong_q2_fewshot():
    """Q2 Few-shot 测试"""
    print("\n=== PingPong Q2: Classify Outcome (Few-shot) ===")
    llm = QubitLLM()
    result = llm.run(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.PINGPONG,
        fewshot=True
    )
    print(f"  结果: {str(result)[:200]}...")
    assert "Classification" in result
    print("  ✓")


def test_pingpong_q3_zeroshot():
    """Q3 Zero-shot 测试"""
    print("\n=== PingPong Q3: Scientific Reasoning (Zero-shot) ===")
    llm = QubitLLM()
    result = llm.run(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.PINGPONG,
        fewshot=False
    )
    print(f"  结果: {result[:200]}...")
    assert len(result) > 0
    print("  ✓")


def test_pingpong_q3_fewshot():
    """Q3 Few-shot 测试"""
    print("\n=== PingPong Q3: Scientific Reasoning (Few-shot) ===")
    llm = QubitLLM()
    result = llm.run(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.PINGPONG,
        fewshot=True
    )
    print(f"  结果: {result[:200]}...")
    assert len(result) > 0
    print("  ✓")


def test_pingpong_q4_zeroshot():
    """Q4 Zero-shot 测试"""
    print("\n=== PingPong Q4: Assess Fit (Zero-shot) ===")
    llm = QubitLLM()
    result = llm.run(
        LLMTaskName.ASSESS_FIT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.PINGPONG,
        fewshot=False
    )
    print(f"  结果: {str(result)[:200]}...")
    assert "Assessment" in result
    print("  ✓")


def test_pingpong_q4_fewshot():
    """Q4 Few-shot 测试"""
    print("\n=== PingPong Q4: Assess Fit (Few-shot) ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.ASSESS_FIT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.PINGPONG,
        fewshot=True
    )
    print(f"  图片数: {len(prompt_data['images'])}")
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Assessment" in result
    print("  ✓")


def test_pingpong_q5_zeroshot():
    """Q5 Zero-shot 测试"""
    print("\n=== PingPong Q5: Extract Params (Zero-shot) ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.PINGPONG,
        fewshot=False
    )
    print(f"  图片数: {len(prompt_data['images'])}")
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert result is not None
    print("  ✓")


def test_pingpong_q5_fewshot():
    """Q5 Few-shot 测试"""
    print("\n=== PingPong Q5: Extract Params (Few-shot) ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.PINGPONG,
        fewshot=True
    )
    print(f"  图片数: {len(prompt_data['images'])}")
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert result is not None
    print("  ✓")


def test_pingpong_q6_zeroshot():
    """Q6 Zero-shot 测试"""
    print("\n=== PingPong Q6: Evaluate Status (Zero-shot) ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EVALUATE_STATUS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.PINGPONG,
        fewshot=False
    )
    print(f"  图片数: {len(prompt_data['images'])}")
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Status" in result
    print(f"  预期: {TEST_SAMPLE['q6_expected_status']}")
    print("  ✓")


def test_pingpong_q6_fewshot():
    """Q6 Few-shot 测试"""
    print("\n=== PingPong Q6: Evaluate Status (Few-shot) ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EVALUATE_STATUS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.PINGPONG,
        fewshot=True
    )
    print(f"  图片数: {len(prompt_data['images'])}")
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Status" in result
    print(f"  预期: {TEST_SAMPLE['q6_expected_status']}")
    print("  ✓")


if __name__ == "__main__":
    # Zero-shot 测试
    test_pingpong_q1_zeroshot()
    test_pingpong_q2_zeroshot()
    test_pingpong_q3_zeroshot()
    test_pingpong_q4_zeroshot()
    test_pingpong_q5_zeroshot()
    test_pingpong_q6_zeroshot()

    # Few-shot 测试
    test_pingpong_q1_fewshot()
    test_pingpong_q2_fewshot()
    test_pingpong_q3_fewshot()
    test_pingpong_q4_fewshot()
    test_pingpong_q5_fewshot()
    test_pingpong_q6_fewshot()

    print("\n✓ PingPong Few-shot tests passed!")