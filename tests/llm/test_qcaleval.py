# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
QCalEval 数据集集成测试 - 测试 LLM 多模态功能
"""

import os
import sys

# 获取测试文件所在目录
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(TEST_DIR, "dataset")

project_root = os.path.abspath(os.path.join(TEST_DIR, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm import QubitLLM
from qubitclient.llm.task import LLMTaskName


# 硬编码测试数据
TEST_SAMPLE = {
    "id": "drag_failure_no_signal_a",
    "experiment_type": "drag_failure_no_signal",
    "experiment_family": "drag",
    "image_filename": "e1e93e18c44bebab.png",
    "q1_answer": {"plot_type": "scatter"},
    "q2_answer": "Apparatus issue",
    "q4_answer": "Unreliable",
    "q5_answer": {"optimal_alpha_inv": "Unreliable", "intersection_clear": False},
    "q6_expected_status": "NO_SIGNAL",
}


def get_image_path(filename: str) -> str:
    """获取测试图像路径"""
    return os.path.join(DATASET_DIR, "images", filename)


def test_q1_describe_plot():
    """测试 Q1: 描述图表"""
    print("\n=== Q1: Describe Plot ===")
    llm = QubitLLM()
    image_path = get_image_path(TEST_SAMPLE["image_filename"])

    print(f"图像: {image_path}")
    print(f"实验家族: {TEST_SAMPLE['experiment_family']}")

    prompt_data = llm.get_prompt(
        LLMTaskName.DESCRIBE_PLOT,
        image_data=image_path,
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)

    print(f"结果: {str(result)[:500]}...")
    assert result is not None
    assert "plot_type" in result
    print("✓ Q1 测试通过")


def test_q2_classify_outcome():
    """测试 Q2: 分类实验结果"""
    print("\n=== Q2: Classify Outcome ===")
    llm = QubitLLM()
    image_path = get_image_path(TEST_SAMPLE["image_filename"])

    prompt_data = llm.get_prompt(
        LLMTaskName.CLASSIFY_OUTCOME,
        image_data=image_path,
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)

    print(f"结果: {str(result)[:300]}...")
    print(f"预期分类: {TEST_SAMPLE['q2_answer']}")
    assert result is not None
    assert "Classification" in result
    print("✓ Q2 测试通过")


def test_q3_scientific_reasoning():
    """测试 Q3: 科学推理"""
    print("\n=== Q3: Scientific Reasoning ===")
    llm = QubitLLM()
    image_path = get_image_path(TEST_SAMPLE["image_filename"])

    prompt_data = llm.get_prompt(
        LLMTaskName.SCIENTIFIC_REASONING,
        image_data=image_path,
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)

    print(f"结果: {result[:300]}...")
    assert result is not None
    assert len(result) > 0
    print("✓ Q3 测试通过")


def test_q4_assess_fit():
    """测试 Q4: 评估拟合"""
    print("\n=== Q4: Assess Fit ===")
    llm = QubitLLM()
    image_path = get_image_path(TEST_SAMPLE["image_filename"])

    prompt_data = llm.get_prompt(
        LLMTaskName.ASSESS_FIT,
        image_data=image_path,
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)

    print(f"结果: {str(result)[:300]}...")
    print(f"预期评估: {TEST_SAMPLE['q4_answer']}")
    assert result is not None
    assert "Assessment" in result
    print("✓ Q4 测试通过")


def test_q5_extract_params():
    """测试 Q5: 提取参数"""
    print("\n=== Q5: Extract Params ===")
    llm = QubitLLM()
    image_path = get_image_path(TEST_SAMPLE["image_filename"])

    prompt_data = llm.get_prompt(
        LLMTaskName.EXTRACT_PARAMS,
        image_data=image_path,
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)

    print(f"结果: {str(result)[:300]}...")
    assert result is not None
    print("✓ Q5 测试通过")


def test_q6_evaluate_status():
    """测试 Q6: 评估实验状态"""
    print("\n=== Q6: Evaluate Status ===")
    llm = QubitLLM()
    image_path = get_image_path(TEST_SAMPLE["image_filename"])

    prompt_data = llm.get_prompt(
        LLMTaskName.EVALUATE_STATUS,
        image_data=image_path,
        experiment_family=TEST_SAMPLE["experiment_family"]
    )
    result = llm.chat(**prompt_data)

    print(f"结果: {str(result)[:300]}...")
    print(f"预期状态: {TEST_SAMPLE['q6_expected_status']}")
    assert result is not None
    assert "Status" in result
    print("✓ Q6 测试通过")


def test_all_tasks_single_image():
    """测试单张图像的所有任务"""
    print("\n=== All Tasks on Single Image ===")
    llm = QubitLLM()
    image_path = get_image_path(TEST_SAMPLE["image_filename"])
    experiment_family = TEST_SAMPLE["experiment_family"]

    print(f"实验类型: {TEST_SAMPLE['experiment_type']}")
    print(f"实验家族: {experiment_family}")

    tasks = [
        ("Q1 Describe", LLMTaskName.DESCRIBE_PLOT),
        ("Q2 Classify", LLMTaskName.CLASSIFY_OUTCOME),
        ("Q3 Reasoning", LLMTaskName.SCIENTIFIC_REASONING),
        ("Q4 Assess Fit", LLMTaskName.ASSESS_FIT),
        ("Q5 Extract", LLMTaskName.EXTRACT_PARAMS),
        ("Q6 Status", LLMTaskName.EVALUATE_STATUS),
    ]

    for name, task in tasks:
        try:
            prompt_data = llm.get_prompt(task, image_data=image_path, experiment_family=experiment_family)
            result = llm.chat(**prompt_data)
            print(f"  {name}: {'✓' if result else '✗'}")
        except Exception as e:
            print(f"  {name}: ✗ ({e})")

    print("✓ All tasks test completed")


if __name__ == "__main__":
    test_q1_describe_plot()
    test_q2_classify_outcome()
    test_q3_scientific_reasoning()
    test_q4_assess_fit()
    test_q5_extract_params()
    test_q6_evaluate_status()
    test_all_tasks_single_image()
    print("\n✓ All QCalEval integration tests passed!")