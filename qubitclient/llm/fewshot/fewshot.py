# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
Fewshot 管理模块

用于构建少样本评估的 prompt 和管理示例数据
"""

import json
import os
from pathlib import Path
from typing import Any

# 模块根目录
FEWSHOT_DIR = Path(__file__).parent
FEWSHOT_SAMPLES_DIR = FEWSHOT_DIR / "samples"
FEWSHOT_METADATA_FILE = FEWSHOT_SAMPLES_DIR / "metadata.json"


class FewShotManager:
    """Fewshot 示例管理器"""

    def __init__(self, metadata_path: str | Path | None = None):
        """
        初始化 FewShotManager

        Args:
            metadata_path: 元数据文件路径，默认使用内置的 metadata.json
        """
        self.metadata_path = Path(metadata_path) if metadata_path else FEWSHOT_METADATA_FILE
        self._metadata: dict[str, list[dict]] | None = None

    @property
    def metadata(self) -> dict[str, list[dict]]:
        """加载并缓存元数据"""
        if self._metadata is None:
            if not self.metadata_path.exists():
                raise FileNotFoundError(f"Metadata file not found: {self.metadata_path}")
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                self._metadata = json.load(f)
        return self._metadata

    def get_families(self) -> list[str]:
        """获取所有实验家族列表"""
        return list(self.metadata.keys())

    def get_samples(self, experiment_family: str) -> list[dict]:
        """
        获取指定实验家族的示例

        Args:
            experiment_family: 实验家族名称

        Returns:
            示例列表，每个示例包含 prompt 和 answer
        """
        return self.metadata.get(experiment_family, [])

    def get_sample_images(self, experiment_family: str) -> list[str]:
        """
        获取指定实验家族示例的图片路径

        Args:
            experiment_family: 实验家族名称

        Returns:
            图片路径列表
        """
        samples = self.get_samples(experiment_family)
        images = []
        for sample in samples:
            img_path = FEWSHOT_SAMPLES_DIR / experiment_family / sample["image"]
            if img_path.exists():
                images.append(str(img_path))
        return images

    def get_task_prompt_and_answer(
        self,
        experiment_family: str,
        task_name: str,
        include_images: bool = True,
    ) -> tuple[str, list[str]]:
        """
        获取指定任务的 fewshot prompt 和对应图片

        Args:
            experiment_family: 实验家族名称
            task_name: 任务名称 (q1-q6)
            include_images: 是否包含图片

        Returns:
            (fewshot prompt, 图片路径列表)
        """
        samples = self.get_samples(experiment_family)
        if not samples:
            raise ValueError(f"No samples found for experiment family: {experiment_family}")

        # 构建 fewshot prompt
        prompt_parts = []
        images = []

        prompt_key = f"{task_name}_prompt"
        answer_key = f"{task_name}_answer"

        for i, sample in enumerate(samples, 1):
            # 获取 prompt
            prompt = sample.get(prompt_key, "")
            if not prompt:
                continue

            # 获取 answer
            answer = sample.get(answer_key, "")
            if not answer:
                continue

            # 替换 <image> 占位符
            prompt = prompt.replace("<image>", f"<image>")
            # prompt = prompt.replace("<image>", f"<|image>")

            prompt_parts.append(f"Example {i}:\n{prompt}\n\nAnswer:\n{answer}")

            # 获取图片
            if include_images:
                img_path = FEWSHOT_SAMPLES_DIR / experiment_family / sample["image"]
                if img_path.exists():
                    images.append(str(img_path))

        fewshot_prompt = "\n\n---\n\n".join(prompt_parts)
        return fewshot_prompt, images


# 全局管理器实例
_manager: FewShotManager | None = None


def get_fewshot_manager() -> FewShotManager:
    """获取全局 FewShotManager 实例"""
    global _manager
    if _manager is None:
        _manager = FewShotManager()
    return _manager


def get_fewshot_prompt(
    experiment_family: str,
    task_name: str,
    task_prompt: str,
    include_images: bool = True,
) -> tuple[str, list[str]]:
    """
    构建 fewshot prompt

    将任务 prompt 包装在 fewshot 示例中

    Args:
        experiment_family: 实验家族名称
        task_name: 任务名称 (q1-q6)
        task_prompt: 原始任务 prompt
        include_images: 是否包含示例图片

    Returns:
        (完整的 fewshot prompt, 示例图片路径列表)
    """
    manager = get_fewshot_manager()

    # 获取 fewshot 示例
    fewshot_examples, example_images = manager.get_task_prompt_and_answer(
        experiment_family, task_name, include_images=include_images
    )

    # 组合 final prompt
    if fewshot_examples:
        final_prompt = f"""Below are examples of quantum calibration plot analysis:

{fewshot_examples}

---

Now analyze the following image:

{task_prompt}"""
    else:
        final_prompt = task_prompt

    return final_prompt, example_images


def get_fewshot_images(experiment_family: str) -> list[str]:
    """
    获取指定实验家族的 fewshot 示例图片

    Args:
        experiment_family: 实验家族名称

    Returns:
        图片路径列表
    """
    manager = get_fewshot_manager()
    return manager.get_sample_images(experiment_family)


def list_available_families() -> list[str]:
    """列出所有可用的实验家族"""
    manager = get_fewshot_manager()
    return manager.get_families()


__all__ = [
    "FEWSHOT_DIR",
    "FEWSHOT_SAMPLES_DIR",
    "FEWSHOT_METADATA_FILE",
    "FewShotManager",
    "get_fewshot_prompt",
    "get_fewshot_images",
    "list_available_families",
]