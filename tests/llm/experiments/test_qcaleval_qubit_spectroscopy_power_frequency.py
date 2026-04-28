# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:34
########################################################################

# -*- coding: utf-8 -*-
"""QCalEval Qubit_Spectroscopy_Power_Frequency 实验测试"""

import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "..", "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM, ExperimentFamily
from qubitclient.llm.task import LLMTaskName


# Qubit_Spectroscopy_Power_Frequency 测试数据
TEST_SAMPLE = {
    "id": "qubit_spectroscopy_power_frequency_failure_f01_f02half_amp_too_high_a",
    "experiment_type": "qubit_spectroscopy_power_frequency_failure_f01_f02half_amp_too_high",
    "experiment_family": "qubit_spectroscopy_power_frequency",
    "image_filename": "89b2bd50af0f265d.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Suboptimal parameters",
    "q4_answer": "No",
    "q5_answer": {
  "f01_MHz": 5200.0,
  "transitions_visible": "f01_f02half",
  "power_regime": "high",
  "measurement_usable": False
},
    "q6_expected_status": "AMP_TOO_HIGH",
}


def get_image_path(filename: str) -> str:
    return os.path.join(DATASET_DIR, "images", filename)


def test_qubit_spectroscopy_power_frequency_q1_describe():
    print("\n=== Qubit_Spectroscopy_Power_Frequency: Q1 Describe Plot ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.QUBIT_SPECTROSCOPY_POWER_FREQUENCY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert "plot_type" in result
    print("  ✓")


def test_qubit_spectroscopy_power_frequency_q2_classify():
    print("\n=== Qubit_Spectroscopy_Power_Frequency: Q2 Classify Outcome ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.QUBIT_SPECTROSCOPY_POWER_FREQUENCY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert "Classification" in result
    print("  ✓")


def test_qubit_spectroscopy_power_frequency_q3_reasoning():
    print("\n=== Qubit_Spectroscopy_Power_Frequency: Q3 Scientific Reasoning ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.QUBIT_SPECTROSCOPY_POWER_FREQUENCY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {result[:200]}...")
    assert len(result) > 0
    print("  ✓")


def test_qubit_spectroscopy_power_frequency_q4_assess():
    print("\n=== Qubit_Spectroscopy_Power_Frequency: Q4 Assess Fit ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.ASSESS_FIT,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.QUBIT_SPECTROSCOPY_POWER_FREQUENCY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert "Assessment" in result
    print("  ✓")


def test_qubit_spectroscopy_power_frequency_q5_extract():
    print("\n=== Qubit_Spectroscopy_Power_Frequency: Q5 Extract Params ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.QUBIT_SPECTROSCOPY_POWER_FREQUENCY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert result is not None
    print("  ✓")


def test_qubit_spectroscopy_power_frequency_q6_status():
    print("\n=== Qubit_Spectroscopy_Power_Frequency: Q6 Evaluate Status ===")
    llm = QubitLLM()
    prompt_data = llm.get_prompt(
        LLMTaskName.EVALUATE_STATUS,
        image_data=get_image_path(TEST_SAMPLE["image_filename"]),
        experiment_family=ExperimentFamily.QUBIT_SPECTROSCOPY_POWER_FREQUENCY
    )
    result = llm.chat(**prompt_data)
    print(f"  结果: {str(result)[:800]}...")
    assert "Status" in result
    print("  ✓")


if __name__ == "__main__":
    test_qubit_spectroscopy_power_frequency_q1_describe()
    test_qubit_spectroscopy_power_frequency_q2_classify()
    test_qubit_spectroscopy_power_frequency_q3_reasoning()
    test_qubit_spectroscopy_power_frequency_q4_assess()
    test_qubit_spectroscopy_power_frequency_q5_extract()
    test_qubit_spectroscopy_power_frequency_q6_status()
    print("\n✓ Qubit_Spectroscopy_Power_Frequency tests passed!")
