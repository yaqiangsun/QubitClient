# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from qubitclient.llm import QubitLLM, LLMTaskName


def test_chat():
    """测试基础对话"""
    llm = QubitLLM()
    result = llm.chat([{"role": "user", "content": "Say hello in one word"}])
    print(f"chat result: {result}")
    assert result is not None
    assert len(result) > 0


def test_chat_with_model():
    """测试指定模型"""
    llm = QubitLLM(model="MiniMaxAI/MiniMax-M2.5")
    result = llm.chat([{"role": "user", "content": "Say hi"}])
    print(f"chat with model result: {result}")
    assert result is not None


def test_get_prompt():
    """测试获取 prompt"""
    llm = QubitLLM()

    # 测试 vlm_analyze
    prompt_data = llm.get_prompt(LLMTaskName.VLM_ANALYZE, image_data="test.png", prompt="分析这个图像")
    assert "messages" in prompt_data
    assert "images" in prompt_data
    print(f"get_prompt vlm_analyze: {prompt_data}")

    # 测试 evaluate_analysis
    prompt_data = llm.get_prompt(LLMTaskName.EVALUATE_ANALYSIS, analysis_result={"score": 80})
    assert "messages" in prompt_data
    assert "response_schema" in prompt_data
    print(f"get_prompt evaluate_analysis: {prompt_data}")


def test_run():
    """测试运行任务"""
    llm = QubitLLM()

    # 测试 evaluate_analysis
    result = llm.run(LLMTaskName.EVALUATE_ANALYSIS, analysis_result={"score": 80})
    print(f"run evaluate_analysis result: {result}")
    assert isinstance(result, dict)
    assert "score" in result


def test_chat_with_json_response():
    """测试 JSON 响应格式"""
    llm = QubitLLM()
    result = llm.chat(
        [{"role": "user", "content": "返回 JSON: {\"name\": \"test\"}"}],
        response_schema={"type": "object", "properties": {"name": {"type": "string"}}}
    )
    print(f"chat json result: {result}")
    assert isinstance(result, dict)


if __name__ == "__main__":
    test_chat()
    test_chat_with_model()
    test_get_prompt()
    test_run()
    test_chat_with_json_response()
    print("All tests passed!")