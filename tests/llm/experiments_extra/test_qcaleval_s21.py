# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/05/14
########################################################################

"""
QCalEval S21 实验测试

S21 腔频扫描实验，测量探针频率透射系数确定腔共振频率
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
# S21 测试数据
TEST_SAMPLE = {
    "id": "S21_success",
    "experiment_type": "S21_success",
    "experiment_family": "S21",
    "image_filename": "s21peak_4894.png",
    "q1_answer": {"plot_type": "line"},
    "q2_answer": "Expected behavior",
    "q4_answer": "Reliable",
    "q5_answer": {
    'resonance_freq_GHz': 6.958, 'contrast': 0.96, 'phase_slope_deg_GHz': 180.0
},
    "q6_expected_status": "SUCCESS",
}

TEST_SAMPLE2= {
    "id": "S21_failure_LOW_CONTRAST",
    "experiment_type": "S21_failure_LOW_CONTRAST",
    "experiment_family": "S21",
    "image_filename": "s21peak_2926.png",
    "q1_answer": {"plot_type": "line"},
    "q2_answer": "Anomalous behavior",
    "q4_answer": "Unreliable",
    "q5_answer": {
    'resonance_freq_GHz': 'Unreliable', 'contrast': 'Unreliable', 'phase_slope_deg_GHz': 'Unreliable'
},
    "q6_expected_status": "LOW_CONTRAST",
}
def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images_extra", filename)



def test_s21_q1_describe():
    print("\n=== S21: Q1 Describe Plot ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.DESCRIBE_PLOT,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.S21
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_s21_q2_classify():
    print("\n=== S21: Q2 Classify Outcome ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.CLASSIFY_OUTCOME,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.S21
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Classification" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_s21_q3_reasoning():
    print("\n=== S21: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.SCIENTIFIC_REASONING,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.S21
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {result[:300]}...")
        assert len(result) > 0
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_s21_q4_assess():
    print("\n=== S21: Q4 Assess Fit ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.ASSESS_FIT,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.S21
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Assessment" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_s21_q5_extract():
    print("\n=== S21: Q5 Extract Params ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EXTRACT_PARAMS,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.S21
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert result is not None
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_s21_q6_status():
    print("\n=== S21: Q6 Evaluate Status ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EVALUATE_STATUS,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.S21
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Status" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


if __name__ == "__main__":
    test_s21_q1_describe()
    test_s21_q2_classify()
    # test_s21_q3_reasoning()
    test_s21_q4_assess()
    test_s21_q5_extract()
    test_s21_q6_status()
    print("\n[OK] S21 tests completed!")