# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/17
########################################################################

"""
图像生成模块 - 整合图像生成和编辑功能
支持文本生成图像、单图像编辑、多图像编辑
"""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Union

from PIL import Image

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("openai package is required. Install with: pip install openai")

from qubitclient.generate.image_utils import (
    encode_image_to_base64,
    encode_image_to_data_uri,
    decode_base64_to_image,
    decode_base64_to_bytes,
    save_image as save_image_to_file,
)
from qubitclient.utils.env_load import get_generate_config


class ImageSize(Enum):
    """图像尺寸枚举"""

    SIZE_256x256 = "256x256"
    SIZE_512x512 = "512x512"
    SIZE_1024x1024 = "1024x1024"
    SIZE_1792x1024 = "1792x1024"
    SIZE_1024x1792 = "1024x1792"


class ResponseFormat(Enum):
    """响应格式枚举"""

    URL = "url"
    B64_JSON = "b64_json"


@dataclass
class GeneratedImage:
    """生成的图像数据"""

    b64_json: str | None = None
    """base64 编码的图像数据"""
    url: str | None = None
    """图像 URL"""
    revised_prompt: str | None = None
    """修订后的提示词"""

    def to_image(self) -> Image.Image:
        """转换为 PIL Image"""
        if self.b64_json:
            return decode_base64_to_image(self.b64_json)
        raise ValueError("No b64_json data available")

    def to_bytes(self) -> bytes:
        """转换为字节串"""
        if self.b64_json:
            return decode_base64_to_bytes(self.b64_json)
        raise ValueError("No b64_json data available")

    def save(self, path: Union[str, os.PathLike]) -> os.PathLike:
        """保存图像到文件"""
        if self.b64_json:
            img_bytes = decode_base64_to_bytes(self.b64_json)
            return save_image_to_file(img_bytes, path)
        raise ValueError("No b64_json data available")


def get_generate_client(api_key: str | None = None, base_url: str | None = None) -> OpenAI:
    """获取 OpenAI 客户端（用于图像生成）"""
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError(
            "API key is required. Set OPENAI_API_KEY or pass api_key parameter."
        )
    return OpenAI(api_key=api_key, base_url=base_url)


class QubitGenerate:
    """图像生成客户端

    支持：
    - 文本生成图像（text-to-image）
    - 单图像编辑（image editing）
    - 多图像编辑（multi-image editing）
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        default_size: ImageSize = ImageSize.SIZE_1024x1024,
        default_n: int = 1,
        max_image_size: int | None = 1024,
    ):
        """
        初始化 QubitGenerate

        Args:
            api_key: OpenAI API 密钥
            base_url: 自定义 API 地址
            model: 默认模型
            default_size: 默认图像尺寸
            default_n: 默认生成数量
            max_image_size: 输入图像最大边长（像素）
        """
        config = get_generate_config(api_key=api_key, base_url=base_url, model=model)
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url")
        self.model = config.get("model", "dall-e-3")
        self.default_size = default_size
        self.default_n = default_n
        self.max_image_size = max_image_size
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        """获取 OpenAI 客户端"""
        if self._client is None:
            self._client = get_generate_client(self.api_key, self.base_url)
        return self._client

    def generate(
        self,
        prompt: str,
        image: Union[str, bytes, list[Union[str, bytes]], None] = None,
        mask: Union[str, bytes, None] = None,
        model: str | None = None,
        size: ImageSize | str = ImageSize.SIZE_1024x1024,
        n: int = 1,
        response_format: ResponseFormat = ResponseFormat.B64_JSON,
        **kwargs,
    ) -> list[GeneratedImage]:
        """统一图像生成/编辑接口

        支持三种模式：
        - 文本生成图像：image=None
        - 单图像编辑：image 为单图
        - 多图像编辑：image 为图像列表

        Args:
            prompt: 图像描述或编辑指令
            image: 输入图像（文件路径或 bytes）
                   - None：纯文本生成
                   - 单图（str/bytes）：单图像编辑
                   - 列表：多图像编辑
            mask: 可选蒙版图像（仅单图模式）
            model: 模型（默认使用 self.model）
            size: 图像尺寸
            n: 生成数量（1-10）
            response_format: 响应格式（url 或 b64_json）
            **kwargs: 其他 API 参数

        Returns:
            生成的图像列表
        """
        if isinstance(size, str):
            size = ImageSize(size)

        params = {
            "model": model or self.model,
            "prompt": prompt,
            "size": size.value,
            "n": min(max(1, n), 10),
            "response_format": response_format.value,
            **kwargs,
        }

        # 根据 image 参数类型决定模式
        if image is None:
            # 纯文本生成
            pass
        elif isinstance(image, list):
            # 多图像编辑：编码图像列表
            encoded_images = []
            for img in image:
                b64 = encode_image_to_base64(img, max_size=self.max_image_size)
                encoded_images.append(f"data:image/png;base64,{b64}")
            params["image"] = encoded_images
        else:
            # 单图像编辑：编码单张图像
            image_b64 = encode_image_to_data_uri(
                image,
                max_size=self.max_image_size,
                mime_type="image/png",
            )
            params["image"] = image_b64

            if mask is not None:
                params["mask"] = encode_image_to_data_uri(
                    mask, max_size=self.max_image_size, mime_type="image/png"
                )

        response = self.client.images.generate(**params)
        return self._parse_response(response)

    def _parse_response(self, response) -> list[GeneratedImage]:
        """解析 API 响应"""
        results = []
        for item in response.data:
            results.append(
                GeneratedImage(
                    b64_json=item.b64_json,
                    url=item.url,
                    revised_prompt=getattr(item, "revised_prompt", None),
                )
            )
        return results


__all__ = [
    "QubitGenerate",
    "GeneratedImage",
    "ImageSize",
    "ResponseFormat",
    "get_generate_client",
    "get_generate_config",
]