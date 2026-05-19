# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:34
########################################################################

# -*- coding: utf-8 -*-
"""QCalEval Drag 实验测试"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "..", "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM, ExperimentFamily
from qubitclient.llm.task import LLMTaskName


# Drag 测试数据
TEST_SAMPLE = {
    "id": "drag_success",
    "experiment_type": "drag_success",
    "experiment_family": "drag",
    "image_filename": "drag_16343_Q2.png",
    "q1_answer": {"plot_type": "line"},
    "q2_answer": "Expected behavior",
    "q4_answer": "Reliable",
    "q5_answer": {
    'optimal_alpha_inv': 0.0, 'intersection_clear': True
},
    "q6_expected_status": "SUCCESS",
}

TEST_SAMPLE2 = {
    "id": "drag_success",
    "experiment_type": "drag_success",
    "experiment_family": "drag",
    "image_filename": "drag_22378.png",
    "q1_answer": {"plot_type": "line"},
    "q2_answer": "Expected behavior",
    "q4_answer": "Reliable",
    "q5_answer": {
    'optimal_alpha_inv': 0.0, 'intersection_clear': True
},
    "q6_expected_status": "SUCCESS",
}

TEST_SAMPLE3 = {
    "id": "drag_failure_OPTIMAL_NOT_CENTERED",
    "experiment_type": "drag_failure_OPTIMAL_NOT_CENTERED",
    "experiment_family": "drag",
    "image_filename": "drag_16343.png",
    "q1_answer": {"plot_type": "line"},
    "q2_answer": "Expected behavior",
    "q4_answer": "Unreliable",
    "q5_answer": {
    'optimal_alpha_inv': -1.5, 'intersection_clear': True
},
    "q6_expected_status": "OPTIMAL_NOT_CENTERED",
}

TEST_SAMPLE4 = {
    "id": "drag_failure_OPTIMAL_NOT_CENTERED",
    "experiment_type": "drag_failure_NO_CROSSING",
    "experiment_family": "drag",
    "image_filename": "drag_16343_Q2.png",
    "q1_answer": {"plot_type": "line"},
    "q2_answer": "Expected behavior",
    "q4_answer": "Unreliable",
    "q5_answer": {
    'optimal_alpha_inv': 0.0, 'intersection_clear': False
},
    "q6_expected_status": "NO_CROSSING",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images_extra", filename)


def test_drag_q1_describe():
    print("\n=== Drag: Q1 Describe Plot ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.DRAG
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert "plot_type" in result
    print("  ✓")


def test_drag_q2_classify():
    print("\n=== Drag: Q2 Classify Outcome ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.DRAG
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert "Classification" in result
    print("  ✓")


def test_drag_q3_reasoning():
    print("\n=== Drag: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.DRAG
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {result[:200]}...")
    assert len(result) > 0
    print("  ✓")


def test_drag_q4_assess():
    print("\n=== Drag: Q4 Assess Fit ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.ASSESS_FIT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.DRAG
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert "Assessment" in result
    print("  ✓")


def test_drag_q5_extract():
    print("\n=== Drag: Q5 Extract Params ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.DRAG
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert result is not None
    print("  ✓")


def test_drag_q6_status():
    print("\n=== Drag: Q6 Evaluate Status ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EVALUATE_STATUS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.DRAG
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert "Status" in result
    print("  ✓")


if __name__ == "__main__":
    test_drag_q1_describe()
    test_drag_q2_classify()
    # test_drag_q3_reasoning()
    test_drag_q4_assess()
    test_drag_q5_extract()
    test_drag_q6_status()
    print("\n✓ Drag tests passed!")
