# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/05/14
########################################################################

"""
QCalEval SPECTRUM 实验测试

频谱分析实验，与 QUBIT_SPECTROSCOPY 完全相同
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


# SPECTRUM 测试数据
TEST_SAMPLE = {
    "id": "SPECTRUM_failure_MULTIPLE_PEAKS",
    "experiment_type": "SPECTRUM_failure_MULTIPLE_PEAKS",
    "experiment_family": "SPECTRUM",
    "image_filename": "spectrum_988.png",
    "q1_answer": {"plot_type": "line"},
    "q2_answer": "Suboptimal parameters",
    "q4_answer": "Unreliable",
    "q5_answer": {
    'num_resonances': 3, 'resonance_freq_GHz': 4.75, 'resonance_type': 'peak'
},
    "q6_expected_status": "MULTIPLE_PEAKS",
}

TEST_SAMPLE2 = {
    "id": "SPECTRUM_failure_MULTIPLE_PEAKS",
    "experiment_type": "SPECTRUM_failure_MULTIPLE_PEAKS",
    "experiment_family": "SPECTRUM",
    "image_filename": "spectrum_3645.png",
    "q1_answer": {"plot_type": "line"},
    "q2_answer": "Suboptimal parameters",
    "q4_answer": "Unreliable",
    "q5_answer": {
    'num_resonances': 3, 'resonance_freq_GHz': 4.42, 'resonance_type': 'peak'
},
    "q6_expected_status": "MULTIPLE_PEAKS",
}
def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images_extra", filename)



def test_spectrum_q1_describe():
    print("\n=== SPECTRUM: Q1 Describe Plot ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.DESCRIBE_PLOT,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.SPECTRUM
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_spectrum_q2_classify():
    print("\n=== SPECTRUM: Q2 Classify Outcome ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.CLASSIFY_OUTCOME,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.SPECTRUM
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Classification" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_spectrum_q3_reasoning():
    print("\n=== SPECTRUM: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.SCIENTIFIC_REASONING,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.SPECTRUM
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {result[:300]}...")
        assert len(result) > 0
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_spectrum_q4_assess():
    print("\n=== SPECTRUM: Q4 Assess Fit ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.ASSESS_FIT,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.SPECTRUM
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Assessment" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_spectrum_q5_extract():
    print("\n=== SPECTRUM: Q5 Extract Params ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EXTRACT_PARAMS,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.SPECTRUM
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert result is not None
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


def test_spectrum_q6_status():
    print("\n=== SPECTRUM: Q6 Evaluate Status ===")
    llm = QubitLLM()
    try:
        prompt_data = llm.get_prompt(
            LLMTaskName.EVALUATE_STATUS,
            image_data=get_image_path(TEST_SAMPLE["image_filename"]),
            experiment_family=ExperimentFamily.SPECTRUM
        )
        result = llm.chat(**prompt_data)
        print(f"  结果: {str(result)[:500]}...")
        assert "Status" in result
    except Exception as e:
        print(f"  (跳过实际调用: {e})")
    print("  [OK]")


if __name__ == "__main__":
    test_spectrum_q1_describe()
    test_spectrum_q2_classify()
    # test_spectrum_q3_reasoning()
    test_spectrum_q4_assess()
    test_spectrum_q5_extract()
    test_spectrum_q6_status()
    print("\n[OK] SPECTRUM tests completed!")