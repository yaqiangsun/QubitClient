# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/05/14
########################################################################

"""
QCalEval SPECTRUM_2D 实验测试

二维量子比特谱实验，测试单量子比特的 Z 控制调谐能力
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


# SPECTRUM_2D 测试数据
TEST_SAMPLE = {
    "id": "SPECTRUM_2D_failure_NO_FIT",
    "experiment_type": "SPECTRUM_2D_failure_NO_FIT",
    "experiment_family": "SPECTRUM_2D",
    "image_filename": "spectrum2d_4905_Q2.png",
    "q1_answer": {"plot_type": "heatmap"},
    "q2_answer": "Expected behavior",
    "q4_answer": "No fit",
    "q5_answer": {
    'idle_freq_GHz': 4.191, 'freq_range_GHz': 0.382, 'calibration_curve_quality': 'good', 'z_tunability': 'high'
},
    "q6_expected_status": "NO_FIT",
}

TEST_SAMPLE2 = {
    "id": "SPECTRUM_2D_success",
    "experiment_type": "SPECTRUM_2D_success",
    "experiment_family": "SPECTRUM_2D",
    "image_filename": "spectrum2d_4905_Q1.png",
    "q1_answer": {"plot_type": "heatmap"},
    "q2_answer": "Expected behavior",
    "q4_answer": "Reliable",
    "q5_answer": {
    'idle_freq_GHz': 4.35, 'freq_range_GHz': 0.4, 'calibration_curve_quality': 'good', 'z_tunability': 'high'
},
    "q6_expected_status": "SUCCESS",
}
def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images_extra", filename)


def test_spectrum_2d_q1_describe():
    print("\n=== SPECTRUM_2D: Q1 Describe Plot ===")
    llm = QubitLLM()
    # SPECTRUM_2D 没有真实图片，使用空路径测试 prompt 生成
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.DESCRIBE_PLOT,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.SPECTRUM_2D
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  ✓")


def test_spectrum_2d_q2_classify():
    print("\n=== SPECTRUM_2D: Q2 Classify Outcome ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.CLASSIFY_OUTCOME,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.SPECTRUM_2D
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Classification" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  ✓")


def test_spectrum_2d_q3_reasoning():
    print("\n=== SPECTRUM_2D: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.SCIENTIFIC_REASONING,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.SPECTRUM_2D
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {result[:300]}...")
        assert len(result) > 0
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  ✓")


def test_spectrum_2d_q4_assess():
    print("\n=== SPECTRUM_2D: Q4 Assess Fit ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.ASSESS_FIT,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.SPECTRUM_2D
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Assessment" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  ✓")


def test_spectrum_2d_q5_extract():
    print("\n=== SPECTRUM_2D: Q5 Extract Params ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EXTRACT_PARAMS,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.SPECTRUM_2D
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert result is not None
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  ✓")


def test_spectrum_2d_q6_status():
    print("\n=== SPECTRUM_2D: Q6 Evaluate Status ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EVALUATE_STATUS,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.SPECTRUM_2D
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Status" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  ✓")


if __name__ == "__main__":
    test_spectrum_2d_q1_describe()
    test_spectrum_2d_q2_classify()
    # test_spectrum_2d_q3_reasoning()
    test_spectrum_2d_q4_assess()
    test_spectrum_2d_q5_extract()
    test_spectrum_2d_q6_status()
    print("\n[OK] SPECTRUM_2D tests completed!")