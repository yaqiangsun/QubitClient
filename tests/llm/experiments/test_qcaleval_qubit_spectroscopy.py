# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:34
########################################################################

# -*- coding: utf-8 -*-
"""QCalEval Qubit_Spectroscopy 实验测试"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "..", "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM, ExperimentFamily
from qubitclient.llm.task import LLMTaskName


# Qubit_Spectroscopy 测试数据
TEST_SAMPLE = {
    "id": "qubit_spectroscopy_failure_multiple_peaks_a",
    "experiment_type": "qubit_spectroscopy_failure_multiple_peaks",
    "experiment_family": "qubit_spectroscopy",
    "image_filename": "0d40473dd5401240.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Anomalous behavior",
    "q4_answer": "Unreliable",
    "q5_answer": {
  "num_resonances": 3,
  "resonance_freq_GHz": "Unreliable",
  "resonance_type": "dip"
},
    "q6_expected_status": "MULTIPLE_PEAKS",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images", filename)


def test_qubit_spectroscopy_q1_describe():
    print("\n=== Qubit_Spectroscopy: Q1 Describe Plot ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.QUBIT_SPECTROSCOPY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "plot_type" in result
    print("  ✓")


def test_qubit_spectroscopy_q2_classify():
    print("\n=== Qubit_Spectroscopy: Q2 Classify Outcome ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.QUBIT_SPECTROSCOPY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Classification" in result
    print("  ✓")


def test_qubit_spectroscopy_q3_reasoning():
    print("\n=== Qubit_Spectroscopy: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.QUBIT_SPECTROSCOPY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {result[:200]}...")
    assert len(result) > 0
    print("  ✓")


def test_qubit_spectroscopy_q4_assess():
    print("\n=== Qubit_Spectroscopy: Q4 Assess Fit ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.ASSESS_FIT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.QUBIT_SPECTROSCOPY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Assessment" in result
    print("  ✓")


def test_qubit_spectroscopy_q5_extract():
    print("\n=== Qubit_Spectroscopy: Q5 Extract Params ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.QUBIT_SPECTROSCOPY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert result is not None
    print("  ✓")


def test_qubit_spectroscopy_q6_status():
    print("\n=== Qubit_Spectroscopy: Q6 Evaluate Status ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EVALUATE_STATUS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.QUBIT_SPECTROSCOPY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:200]}...")
    assert "Status" in result
    print("  ✓")


if __name__ == "__main__":
    test_qubit_spectroscopy_q1_describe()
    test_qubit_spectroscopy_q2_classify()
    test_qubit_spectroscopy_q3_reasoning()
    test_qubit_spectroscopy_q4_assess()
    test_qubit_spectroscopy_q5_extract()
    test_qubit_spectroscopy_q6_status()
    print("\n✓ Qubit_Spectroscopy tests passed!")
