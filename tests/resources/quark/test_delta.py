# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/03/26
########################################################################

import os
import sys
import logging

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from resources.quark.analysis.utils import get_pkl_content
from resources.quark.analysis.inception import delta          
from resources.quark.analysis.visualization import plot_delta  


def test_delta(task_key, base_dir):
    """
    测试 Delta 任务的分析与可视化流程
    与 test_optpipulse.py 保持完全一致的结构和逻辑
    """
    for filename in os.listdir(base_dir):
        pkl_path = os.path.join(base_dir, filename)
        
        # 提取文件名前缀（用于保存图片）
        pure_name = os.path.splitext(os.path.basename(pkl_path))[0]
        
        # 读取 pkl 文件
        data = get_pkl_content(pkl_path)
        if data is None:
            continue
            
        if "meta" not in data.keys():
            continue
            
        if "name" not in data["meta"].keys():
            continue

        # 判断是否为 Delta 相关任务
        if "delta" in data["meta"]["name"].lower():
            if len(data["meta"]["other"].get("qubits", [])) >= 1:
                if task_key in ["delta", "del"]:
                    # 执行 Delta 分析
                    analysis_result = delta(data)
                    
                    # 执行 Delta 可视化（保存为 png）
                    fig_list = plot_delta(
                        data, 
                        analysis_result, 
                        save_path=f'./tmp/vis/delta_{pure_name}.png'
                    )
                    
                    # 可选：显示图像（根据需要取消注释）
                    # if fig_list and len(fig_list) > 0:
                    #     fig_list[0].show()
                    # plt.show(block=True)


def main():
    task_key = "delta"                    # 与 optpipulse 的 task_key 对应
    base_dir = "data/Delta"           # 请根据实际 Delta 数据存放路径修改
    
    test_delta(task_key, base_dir)


if __name__ == "__main__":
    main()