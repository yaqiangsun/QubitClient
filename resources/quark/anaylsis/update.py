# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/27 10:13:17
########################################################################
import logging
import numpy as np

from .utils import query_param, update_param

def optpipulse_update(data_converted, result: dict):
    # 分别传入 量子实验后的原始数据 和 分析结果
    for idx, qubit in enumerate(data_converted["image"]):
        params = result["results"][0]["params"][idx]
        if params:
            original_amp = query_param(f"gate.R.{qubit}.params.amp")
            if original_amp is not None:  # 防护空值
                final_amp = original_amp * params[0] # params是比例
                update_param(f"gate.R.{qubit}.params.amp", final_amp)
                logging.info(f"更新{qubit}的AMP参数为：{final_amp}")
            else:
                logging.warning(f"未找到{qubit}的AMP参数")