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
from PIL import Image
import tempfile

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
    prompt_data = llm.get_prompt(LLMTaskName.SCIENTIFIC_REASONING, image_data="tests/llm/dataset/images/0d127bbe75fa7a04.png")
    assert "messages" in prompt_data
    assert "images" in prompt_data
    print(f"get_prompt vlm_analyze: {prompt_data}")


def test_run():
    """测试运行任务"""
    llm = QubitLLM()

    # 测试 evaluate_analysis
    result = llm.run(LLMTaskName.SCIENTIFIC_REASONING, image_data="tests/llm/dataset/images/0d127bbe75fa7a04.png")
    print(f"run evaluate_analysis result: {result}")


def test_chat_with_json_response():
    """测试 JSON 响应格式"""
    llm = QubitLLM()
    result = llm.chat(
        [{"role": "user", "content": "返回 JSON: {\"name\": \"test\"}"}],
        response_schema={"type": "object", "properties": {"name": {"type": "string"}}}
    )
    print(f"chat json result: {result}")
    assert isinstance(result, dict)


def test_encode_image_with_max_size():
    """测试图像尺寸限制"""
    from qubitclient.llm.llm import _encode_image

    # 创建一个大尺寸测试图像 (800x600)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        large_image = Image.new("RGB", (800, 600), color="red")
        large_image.save(f.name)
        large_image_path = f.name

    try:
        # 测试不缩放
        result1 = _encode_image(large_image_path, max_size=None)
        assert result1 is not None
        print(f"Without max_size: got base64 length {len(result1)}")

        # 测试缩放到 200x200
        result2 = _encode_image(large_image_path, max_size=200)
        assert result2 is not None
        print(f"With max_size=200: got base64 length {len(result2)}")

        # 验证：缩放后的 base64 应该更小
        assert len(result2) < len(result1), "Scaled image should be smaller"
        print(f"encode_image test passed - original: 800x600 -> max dimension: 200")
    finally:
        os.unlink(large_image_path)


def test_max_image_size_parameter():
    """测试 max_image_size 参数"""
    llm = QubitLLM(max_image_size=512)
    assert llm.max_image_size == 512
    print("max_image_size parameter test passed")


if __name__ == "__main__":
    test_chat()
    # test_chat_with_model()
    test_get_prompt() 
    test_run()  
    test_chat_with_json_response() 
    test_encode_image_with_max_size()
    test_max_image_size_parameter()
    print("All tests passed!")