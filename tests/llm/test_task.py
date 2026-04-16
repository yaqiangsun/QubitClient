# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""Tests for qubitclient.llm.task module."""

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.llm.task import get_task_prompt, LLMTaskName, DEFINED_TASKS


def test_task_names():
    """测试任务名称枚举"""
    assert LLMTaskName.DECIDE_NEXT_ACTION.value == "decide_next_action"
    assert LLMTaskName.DESCRIBE_PLOT.value == "describe_plot"
    assert LLMTaskName.CLASSIFY_OUTCOME.value == "classify_outcome"
    assert LLMTaskName.SCIENTIFIC_REASONING.value == "scientific_reasoning"
    assert LLMTaskName.ASSESS_FIT.value == "assess_fit"
    assert LLMTaskName.EXTRACT_PARAMS.value == "extract_params"
    assert LLMTaskName.EVALUATE_STATUS.value == "evaluate_status"
    print("✓ 任务名称枚举正确")


def test_defined_tasks():
    """测试已定义的任务"""
    expected_tasks = [
        "decide_next_action",
        "describe_plot", "classify_outcome", "scientific_reasoning",
        "assess_fit", "extract_params", "evaluate_status",
    ]
    for task in expected_tasks:
        assert task in DEFINED_TASKS, f"Missing task: {task}"
    print(f"✓ 已定义 {len(DEFINED_TASKS)} 个任务")


def test_decide_next_action_task():
    """测试 decide_next_action 任务"""
    # 基本调用
    result = get_task_prompt("decide_next_action", evaluation_result={"Status": "NO_SIGNAL"})
    assert "messages" in result
    assert "response_schema" in result
    assert "recommended_task" in result["response_schema"]["properties"]
    assert "task_params" in result["response_schema"]["properties"]
    assert "reason" in result["response_schema"]["properties"]
    assert "评估结果" in result["messages"][0]["content"]

    # 带上下文
    result = get_task_prompt(
        "decide_next_action",
        evaluation_result={"Status": "SUCCESS"},
        context={"last_task": "rabi", "qubit_id": "Q1"}
    )
    assert "上下文信息" in result["messages"][0]["content"]

    # 带可用行动
    result = get_task_prompt(
        "decide_next_action",
        evaluation_result={"Status": "SUCCESS"},
        available_actions=["rabi", "t1", "ramsey"]
    )
    assert "rabi" in result["messages"][0]["content"]

    print("✓ decide_next_action 任务正常")


def test_describe_plot_task():
    """测试 describe_plot 任务"""
    # 使用 experiment_family
    result = get_task_prompt("describe_plot", "test.png", experiment_family="drag")
    assert "messages" in result
    assert "images" in result
    assert "response_schema" in result
    assert "plot_type" in result["response_schema"]["properties"]
    assert "DRAG" in result["messages"][0]["content"]

    # 使用不同家族
    result = get_task_prompt("describe_plot", "test.png", experiment_family="t1")
    assert "T1" in result["messages"][0]["content"]

    print("✓ describe_plot 任务正常")


def test_classify_outcome_task():
    """测试 classify_outcome 任务"""
    result = get_task_prompt("classify_outcome", "test.png", experiment_family="rabi")
    assert "messages" in result
    assert "images" in result
    assert "response_schema" in result
    assert "Classification" in result["response_schema"]["properties"]
    assert "Expected behavior" in result["messages"][0]["content"]

    print("✓ classify_outcome 任务正常")


def test_scientific_reasoning_task():
    """测试 scientific_reasoning 任务"""
    result = get_task_prompt("scientific_reasoning", "test.png", experiment_family="t1")
    assert "messages" in result
    assert "images" in result
    assert "T1" in result["messages"][0]["content"]

    print("✓ scientific_reasoning 任务正常")


def test_assess_fit_task():
    """测试 assess_fit 任务"""
    result = get_task_prompt("assess_fit", "test.png", experiment_family="ramsey_t2star")
    assert "messages" in result
    assert "images" in result
    assert "response_schema" in result
    assert "Assessment" in result["response_schema"]["properties"]
    assert "Reliable" in result["messages"][0]["content"]

    print("✓ assess_fit 任务正常")


def test_extract_params_task():
    """测试 extract_params 任务"""
    # 使用 experiment_family 自动获取 schema
    result = get_task_prompt("extract_params", "test.png", experiment_family="rabi")
    assert "messages" in result
    assert "images" in result
    assert "response_schema" in result
    schema_props = result["response_schema"]["properties"]
    assert "periods_visible" in schema_props
    assert "amplitude_decay" in schema_props

    # 使用自定义 schema
    custom_schema = {"type": "object", "properties": {"custom_field": {"type": "string"}}}
    result = get_task_prompt("extract_params", "test.png", experiment_family="rabi", params_schema=custom_schema)
    assert "custom_field" in result["response_schema"]["properties"]

    print("✓ extract_params 任务正常")


def test_evaluate_status_task():
    """测试 evaluate_status 任务"""
    result = get_task_prompt("evaluate_status", "test.png", experiment_family="gmm")
    assert "messages" in result
    assert "images" in result
    assert "response_schema" in result
    assert "Status" in result["response_schema"]["properties"]
    assert "SUCCESS" in result["messages"][0]["content"]
    assert "NO_SIGNAL" in result["messages"][0]["content"]

    print("✓ evaluate_status 任务正常")


def test_task_with_enum():
    """测试使用枚举调用任务"""
    result = get_task_prompt(LLMTaskName.DESCRIBE_PLOT, "test.png", experiment_family="drag")
    assert "messages" in result

    result = get_task_prompt(LLMTaskName.EVALUATE_STATUS, "test.png", experiment_family="t1")
    assert "messages" in result

    print("✓ 枚举调用任务正常")


def test_task_with_experiment_family_enum():
    """测试使用 ExperimentFamily 枚举"""
    from qubitclient.llm import ExperimentFamily

    # 使用枚举作为 experiment_family
    result = get_task_prompt("describe_plot", "test.png", experiment_family=ExperimentFamily.DRAG)
    assert "messages" in result
    assert "DRAG" in result["messages"][0]["content"]

    result = get_task_prompt("classify_outcome", "test.png", experiment_family=ExperimentFamily.RABI)
    assert "Expected behavior" in result["messages"][0]["content"]

    result = get_task_prompt("extract_params", "test.png", experiment_family=ExperimentFamily.T1)
    assert "response_schema" in result
    assert "T1_us" in result["response_schema"]["properties"]

    result = get_task_prompt("evaluate_status", "test.png", experiment_family=ExperimentFamily.GMM)
    assert "SUCCESS" in result["messages"][0]["content"]
    assert "NO_SIGNAL" in result["messages"][0]["content"]

    # 使用 LLMTaskName 和 ExperimentFamily 组合
    result = get_task_prompt(LLMTaskName.ASSESS_FIT, "test.png", experiment_family=ExperimentFamily.RAMSEY_T2STAR)
    assert "Reliable" in result["messages"][0]["content"]

    print("✓ ExperimentFamily 枚举调用正常")


def test_task_error_handling():
    """测试错误处理"""
    try:
        get_task_prompt("nonexistent_task", "test.png")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Unknown task" in str(e)

    print("✓ 错误处理正常")


if __name__ == "__main__":
    test_task_names()
    test_defined_tasks()
    test_decide_next_action_task()
    test_describe_plot_task()
    test_classify_outcome_task()
    test_scientific_reasoning_task()
    test_assess_fit_task()
    test_extract_params_task()
    test_evaluate_status_task()
    test_task_with_enum()
    test_task_with_experiment_family_enum()
    test_task_error_handling()
    print("\n✓ All task module tests passed!")