# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../skills/lqcs-qubit-calib/scripts"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils import get_hdf5_content
from analysis.inception import timingxyz
from analysis.visualization import plot_timingxyz


def test_timingxyz(task_key, base_dir):
    for filename in os.listdir(base_dir):
        if not filename.endswith(".hdf5"):
            continue
        file_path = os.path.join(base_dir, filename)
        pure_name = os.path.splitext(os.path.basename(file_path))[0]

        data = get_hdf5_content(file_path)
        if data is None:
            continue

        if task_key in ["timingxyz", "xyz_timing", "TimingXYZ"]:
            print(f"正在测试 timingxyz 文件：{file_path}")
            analysis_result = timingxyz(data)
            plot_timingxyz(
                data,
                analysis_result,
                save_path=f"./tmp/vis/timingxyz_{pure_name}.png",
            )


def main():
    task_key = "timingxyz"
    base_dir = "data/XYZ_Timing_lqcs"
    test_timingxyz(task_key, base_dir)


if __name__ == "__main__":
    main()
