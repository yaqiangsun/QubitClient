# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiang.sun
# Created Time: 2026/04/16
########################################################################

"""
Fewshot 模块 - 少样本评估支持

用于在量子校准图表上对 VLM 进行少样本 (few-shot) 评估
"""

from qubitclient.llm.fewshot.fewshot import (
    FEWSHOT_SAMPLES_DIR,
    FEWSHOT_METADATA_FILE,
    FewShotManager,
    get_fewshot_prompt,
    get_fewshot_images,
    list_available_families,
)

__all__ = [
    "FEWSHOT_SAMPLES_DIR",
    "FEWSHOT_METADATA_FILE",
    "FewShotManager",
    "get_fewshot_prompt",
    "get_fewshot_images",
]