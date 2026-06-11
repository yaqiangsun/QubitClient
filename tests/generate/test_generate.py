# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/06/10
########################################################################

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from qubitclient.generate import QubitGenerate, ImageSize, ResponseFormat


def test_generate_init():
    """测试 QubitGenerate 初始化"""
    gen = QubitGenerate()
    assert gen.model is not None
    assert gen.default_size == ImageSize.SIZE_1024x1024
    print(f"QubitGenerate init: model={gen.model}")


def test_image_generation():
    """测试图像生成（文生图）"""
    gen = QubitGenerate(
        # base_url="http://xx.xx.xx.xx:xx/v1",
        # model="Qwen/Qwen-Image",
    )
    images = gen.generate(
        prompt="A beautiful sunset over mountains, digital art style",
        size="1024x1024",
    )
    assert len(images) > 0
    images[0].save("tmp/generate/generated_image.png")
    print(f"Image saved to tmp/generate/generated_image.png")


def test_image_generation_n2():
    """测试多图生成 n=2"""
    gen = QubitGenerate(
        # base_url="http://xx.xx.xx.xx:xx/v1",
        # model="Qwen/Qwen-Image",
    )
    images = gen.generate(
        prompt="A beautiful sunset over mountains, digital art style",
        size="1024x1024",
        n=2,
    )
    assert len(images) >= 1, f"Expected at least 1 image, got {len(images)}"
    for i, img in enumerate(images):
        img.save(f"tmp/generate/generated_n2_{i}.png")
    print(f"Generated {len(images)} images with n=2")


def test_response_format_enum():
    """测试 ResponseFormat 枚举"""
    assert ResponseFormat.B64_JSON.value == "b64_json"
    print(f"ResponseFormat: {ResponseFormat.B64_JSON.value}")


def test_image_edit():
    """测试单图编辑（需要提供输入图片路径）"""
    input_image = "tmp/generate/generated_image.png"
    if os.path.exists(input_image):
        gen = QubitGenerate(
            # base_url="http://xx.xx.xx.xx:8091/v1",
            # model="Qwen/Qwen-Image-Edit",
        )
        images = gen.generate(
            prompt="Convert to watercolor painting style",
            image=input_image,
            size="1024x1024",
            n=1,
        )
        assert len(images) >= 1, f"Expected at least 1 image, got {len(images)}"
        for i, img in enumerate(images):
            img.save(f"tmp/generate/edited_image_{i}.png")
            print(f"Edited image {i} saved to tmp/generate/edited_image_{i}.png")
    else:
        print("test_image_edit skipped (no input image)")


if __name__ == "__main__":
    # test_generate_init()
    # test_response_format_enum()
    test_image_generation()
    test_image_edit()
    print("All tests passed!")