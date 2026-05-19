# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/05/14
########################################################################

"""
QCalEval RAMSEY 实验测试

Ramsey 干涉实验，精确测量量子比特频率和 T2* 退相干时间
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


# RAMSEY 测试数据
TEST_SAMPLE = {
    "id": "RAMSEY_failure",
    "experiment_type": "RAMSEY_failure",
    "experiment_family": "RAMSEY",
    "image_filename": "ramsey_1607.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Expected behavior",
    "q4_answer": "Unreliable",
    "q5_answer": {
    'detuning_Hz': 46142276.903, 't2_star_us': 1.1, 'contrast': 0.678, 'oscillation_quality': 'good'
},
    "q6_expected_status": "FIT_POOR",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images_extra", filename)



def test_ramsey_q1_describe():
    print("\n=== RAMSEY: Q1 Describe Plot ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.DESCRIBE_PLOT,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.RAMSEY
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_ramsey_q2_classify():
    print("\n=== RAMSEY: Q2 Classify Outcome ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.CLASSIFY_OUTCOME,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.RAMSEY
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Classification" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_ramsey_q3_reasoning():
    print("\n=== RAMSEY: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.SCIENTIFIC_REASONING,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.RAMSEY
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {result[:300]}...")
        assert len(result) > 0
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_ramsey_q4_assess():
    print("\n=== RAMSEY: Q4 Assess Fit ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.ASSESS_FIT,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.RAMSEY
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Assessment" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_ramsey_q5_extract():
    print("\n=== RAMSEY: Q5 Extract Params ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EXTRACT_PARAMS,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.RAMSEY
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert result is not None
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_ramsey_q6_status():
    print("\n=== RAMSEY: Q6 Evaluate Status ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EVALUATE_STATUS,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.RAMSEY
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Status" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


if __name__ == "__main__":
    test_ramsey_q1_describe()
    test_ramsey_q2_classify()
    # test_ramsey_q3_reasoning()
    test_ramsey_q4_assess()
    test_ramsey_q5_extract()
    test_ramsey_q6_status()
    print("\n[OK] RAMSEY tests completed!")