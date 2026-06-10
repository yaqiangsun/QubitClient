# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/17
########################################################################

"""
图像处理工具模块
支持图像编码、缩放、格式转换等功能
"""

import base64
import io
import os
from pathlib import Path
from typing import Union

from PIL import Image


def encode_image_to_base64(
    image_data: Union[str, bytes, Path],
    max_size: int | None = None,
    format: str = "PNG",
) -> str:
    """将图像数据编码为 base64 字符串

    Args:
        image_data: 图像文件路径（str、Path）或 bytes
        max_size: 最大边长（像素），超过此尺寸的图像将被缩放
        format: 输出格式，默认 PNG

    Returns:
        base64 编码的图像字符串（不包含 data URI 前缀）
    """
    # 读取图像
    if isinstance(image_data, (str, Path)):
        if not os.path.exists(image_data):
            raise FileNotFoundError(f"Image file not found: {image_data}")
        image = Image.open(image_data)
    else:
        image = Image.open(io.BytesIO(image_data))

    # 缩放图像（如果超过最大尺寸）
    if max_size is not None:
        width, height = image.size
        if width > max_size or height > max_size:
            # 保持宽高比
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))
            image = image.resize((new_width, new_height), Image.LANCZOS)

    # 转换并编码
    if image.mode == "RGBA":
        image = image.convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format=format.upper())
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def encode_image_to_data_uri(
    image_data: Union[str, bytes, Path],
    max_size: int | None = None,
    mime_type: str = "image/png",
) -> str:
    """将图像数据编码为 data URI 格式

    Args:
        image_data: 图像文件路径或 bytes
        max_size: 最大边长（像素），超过此尺寸的图像将被缩放
        mime_type: MIME 类型

    Returns:
        data URI 格式的图像字符串
    """
    base64_data = encode_image_to_base64(image_data, max_size=max_size)
    return f"data:{mime_type};base64,{base64_data}"


def decode_base64_to_image(base64_str: str) -> Image.Image:
    """将 base64 字符串解码为 PIL Image

    Args:
        base64_str: base64 编码的图像数据（不包含 data URI 前缀）

    Returns:
        PIL Image 对象
    """
    image_bytes = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(image_bytes))


def decode_base64_to_bytes(base64_str: str) -> bytes:
    """将 base64 字符串解码为字节串

    Args:
        base64_str: base64 编码的图像数据（不包含 data URI 前缀）

    Returns:
        图像字节串
    """
    return base64.b64decode(base64_str)


def save_image(
    image_data: Union[str, bytes, Image.Image],
    output_path: Union[str, Path],
) -> Path:
    """保存图像到文件

    Args:
        image_data: 图像数据（路径、bytes 或 PIL Image）
        output_path: 输出文件路径

    Returns:
        输出文件路径
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(image_data, Image.Image):
        image_data.save(output_path)
    elif isinstance(image_data, (str, Path)):
        # 复制文件
        import shutil

        shutil.copy(image_data, output_path)
    else:
        # bytes
        with open(output_path, "wb") as f:
            f.write(image_data)

    return output_path