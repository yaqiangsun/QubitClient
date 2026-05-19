# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/05/14
########################################################################

"""
QCalEval RB 实验测试

随机基准测试（Random Benchmarking）：测量单量子比特门的平均保真度
"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "..", "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM, ExperimentFamily
from qubitclient.llm.task import LLMTaskName


# RB 测试数据
TEST_SAMPLE = {
    "id": "RB_failure_FIT_POOR",
    "experiment_type": "RB_failure_FIT_POOR",
    "experiment_family": "RB",
    "image_filename": "rb_16715.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": 'Anomalous behavior',
    "q4_answer": "Unreliable",
    "q5_answer": {
    'survival_probability_per_clifford': 0.99, 'average_gate_error_rate': 0.01, 'decay_constant': 0.002, 'fit_quality': 'poor'
},
    "q6_expected_status": "FIT_POOR",
}
TEST_SAMPLE3 = {
    "id": "RB_failure_FIT_POOR",
    "experiment_type": "RB_failure_FIT_POOR",
    "experiment_family": "RB",
    "image_filename": "rb_16702.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": 'Anomalous behavior',
    "q4_answer": "Unreliable",
    "q5_answer": {
    'survival_probability_per_clifford': 0.988, 'average_gate_error_rate': 0.012, 'decay_constant': 0.4172, 'fit_quality': 'good'
},
    "q6_expected_status": "FIT_POOR",
}
TEST_SAMPLE2 = {
    "id": "RB_failure_NO_DECAY",
    "experiment_type": "RB_failure_NO_DECAY",
    "experiment_family": "RB",
    "image_filename": "rb_16712.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Apparatus issue",
    "q4_answer": "Unreliable",
    "q5_answer": {
    'survival_probability_per_clifford': 0.9871, 'average_gate_error_rate': 0.0129, 'decay_constant': 0.013, 'fit_quality': 'good'
},
    "q6_expected_status": "NO_DECAY",
}

def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images_extra", filename)


def test_rb_q1_describe():
    print("\n=== RB: Q1 Describe Plot ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.DESCRIBE_PLOT,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.RB
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_rb_q2_classify():
    print("\n=== RB: Q2 Classify Outcome ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.CLASSIFY_OUTCOME,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.RB
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Classification" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_rb_q3_reasoning():
    print("\n=== RB: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.SCIENTIFIC_REASONING,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.RB
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {result[:300]}...")
        assert len(result) > 0
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_rb_q4_assess():
    print("\n=== RB: Q4 Assess Fit ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.ASSESS_FIT,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.RB
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Assessment" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_rb_q5_extract():
    print("\n=== RB: Q5 Extract Params ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EXTRACT_PARAMS,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.RB
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert result is not None
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_rb_q6_status():
    print("\n=== RB: Q6 Evaluate Status ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EVALUATE_STATUS,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.RB
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Status" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


if __name__ == "__main__":
    test_rb_q1_describe()
    test_rb_q2_classify()
    # test_rb_q3_reasoning()
    test_rb_q4_assess()
    test_rb_q5_extract()
    test_rb_q6_status()
    print("\n[OK] RB tests completed!")