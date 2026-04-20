# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
QubitLLM 类 - 整合 LLM/VLM 功能用于量子测量数据分析
"""

import base64
import json
import os
from typing import Generator

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("openai package is required. Install with: pip install openai")

from qubitclient.llm.task import get_task_prompt, LLMTaskName


def get_openai_client(api_key: str | None = None, base_url: str | None = None) -> OpenAI:
    """获取 OpenAI 客户端"""
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("API key is required. Set OPENAI_API_KEY or pass api_key parameter.")
    return OpenAI(api_key=api_key, base_url=base_url)


def _encode_image(image_data: str | bytes) -> str:
    """将图像数据编码为 base64 字符串"""
    if isinstance(image_data, str):
        if not os.path.exists(image_data):
            raise FileNotFoundError(f"Image file not found: {image_data}")
        with open(image_data, "rb") as f:
            image_bytes = f.read()
        return base64.b64encode(image_bytes).decode("utf-8")
    else:
        return base64.b64encode(image_data).decode("utf-8")


class QubitLLM:
    """量子测量 LLM/VLM 助手"""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
    ):
        """
        初始化 QubitLLM

        Args:
            api_key: OpenAI API 密钥，默认从配置文件读取
            base_url: 自定义 API 地址，默认从配置文件读取
            model: 默认使用的模型，默认从配置文件读取
        """
        from qubitclient.utils.env_load import get_llm_config

        config = get_llm_config(api_key=api_key, base_url=base_url, model=model)
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url")
        self.model = config.get("model", "gpt-4o")
        self._client = None

    @property
    def client(self) -> OpenAI:
        """获取 OpenAI 客户端"""
        if self._client is None:
            self._client = get_openai_client(self.api_key, self.base_url)
        return self._client

    # ==================== 任务运行 ====================

    def get_prompt(self, task_type: str | LLMTaskName, *args, **kwargs) -> dict:
        """
        获取 LLM 任务对应的 prompt

        Args:
            task_type: 任务类型（字符串或 LLMTaskName 枚举）
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            包含 messages 和 response_schema 的字典
        """
        return get_task_prompt(task_type, *args, **kwargs)

    def run(self, task_type: str | LLMTaskName, *args, **kwargs) -> dict:
        """
        运行 LLM 任务（获取 prompt 并调用 chat 获取结果）

        Args:
            task_type: 任务类型（字符串或 LLMTaskName 枚举）
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            任务执行结果（dict）
        """
        prompt_data = get_task_prompt(task_type, *args, **kwargs)
        return self.chat(**prompt_data)

    # ==================== 基础对话 ====================

    def chat(
        self,
        messages: list[dict],
        model: str | None = None,
        stream: bool = False,
        images: str | bytes | list[str | bytes] | None = None,
        image_detail: str = "high",
        response_schema: dict | None = None,
        **kwargs
    ) -> str | dict | Generator[str, None, None]:
        """
        统一对话接口

        Args:
            messages: 消息列表
            model: 模型（默认使用 self.model）
            stream: 是否流式返回
            images: 图像（单图/多图），支持路径、bytes 或列表
            image_detail: 图像 detail 级别 ("low", "high", "auto")
            response_schema: 指定则返回 JSON 格式
            **kwargs: 其他 API 参数

        Returns:
            模型回复、JSON 对象或生成器
        """
        # 处理图像
        if images is not None:
            if not isinstance(images, list):
                images = [images]

            image_contents = []
            for image_data in images:
                base64_image = _encode_image(image_data)
                image_contents.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": image_detail
                    }
                })

            # 追加图像到最后一条用户消息
            if messages and messages[-1].get("role") == "user":
                content = messages[-1].get("content", [])
                if isinstance(content, str):
                    content = [{"type": "text", "text": content}]
                content = list(content) + image_contents
                messages = messages[:-1] + [{"role": "user", "content": content}]
            else:
                messages = messages + [{"role": "user", "content": image_contents}]

        # 构建请求参数
        params = {
            "model": model or self.model,
            "messages": messages,
            "stream": stream,
            "temperature": 0.2,
            "max_tokens": 16384,
            **kwargs
        }

        # JSON 格式响应
        if response_schema is not None:
            params["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**params)

        if stream:
            return self._handle_stream(response)

        content = response.choices[0].message.content
        if response_schema is not None:
            # 尝试提取 JSON（去掉思考过程等）
            return self._parse_json_response(content)
        return content

    def _handle_stream(self, response) -> Generator[str, None, None]:
        """处理流式响应"""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    def _parse_json_response(self, content: str) -> dict:
        """解析 JSON 响应，处理思考过程等非 JSON 内容"""
        import re

        # 移除思考内容 (<think>...</think>)
        cleaned = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()

        # 尝试直接解析
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # 尝试提取第一个 JSON 对象
        json_match = re.search(r'\{[\s\S]*\}', cleaned)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        # 尝试查找 ```json ... ``` 块
        json_block_match = re.search(r'```json\s*([\s\S]*?)\s*```', cleaned)
        if json_block_match:
            try:
                return json.loads(json_block_match.group(1))
            except json.JSONDecodeError:
                pass

        raise ValueError(f"Failed to parse JSON from response: {cleaned[:200]}")


__all__ = [
    "QubitLLM",
    "get_openai_client",
]