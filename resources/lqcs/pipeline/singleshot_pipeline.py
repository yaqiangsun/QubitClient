# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/12
########################################################################

"""Single shot readout pipeline with UI storage & cmd args
Usage:
    1. Start UI server first: python -m tests.ui.serve
    2. Example:
        python -m resources.lqcs.pipeline.singleshot_pipeline -q q3lu7 -s ./tmp
"""
import sys
import argparse
import uuid
from datetime import datetime
from pathlib import Path
from PIL import Image
import json

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from qubitclient.storage.result_store import PipelineResultRecord, PipelineResultStore
from qubitclient.storage.storage import StorageBackend
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName
from analysis.inception import singleshot
from analysis.visualization import plot_singleshot

DEFAULT_SAVE_FOLDER = './tmp'

def parse_args():
    parser = argparse.ArgumentParser(description="SingleShot Readout Measurement Pipeline (UI storage sync enabled)")
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q3lu7"],
                        help="Target qubit list, default: q3lu7")
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Plot output directory")
    return parser.parse_args()

def get_singleshot_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = "singleshot"
    pipeline_type = "singleshot_pipeline"
    qubit_name_list = args.qubits
    save_folder = args.save_folder

    try:
        # 1.采集数据
        qubit_ctrl_client = QubitCtrlClient()
        set_params = {
            "qubits": qubit_name_list
        }

        run_record = PipelineResultRecord(
            task_name=task_name,
            task_type=pipeline_type,
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        print(f"[SINGLESHOT] Task started run_id={run_id[:8]}")
        
        data = qubit_ctrl_client.run(CtrlTaskName.SINGLESHOT,
                                       qubits=qubit_name_list)
        data_id = data[0]["text"]
        data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        data = json.loads(data[0]["text"])

        # 2.分析数据
        analysis_result = singleshot(data)

        # 3.绘图
        pure_name = qubit_name_list[0]
        img_save_path = f'{save_folder}/singleshot_{pure_name}.png'
        fig_list = plot_singleshot(data, analysis_result, save_path=img_save_path)

        # 4.接入大模型分析图片
        # resize更小
        # img_small_path = img_save_path.split('.png')[0] + '_small.png'
        # print("img_small_path: ", img_small_path)
        
        # with Image.open(img_save_path) as img:
        #     w, h = img.size
        #     new_w = w // 10
        #     new_h = h // 10
        #     print("size: ", new_w, new_h)
        #     img_small = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        #     img_small.save(img_small_path, dpi=(300, 300))
        
        # test_qubit_spectroscopy_q1_describe(img_small_path)
        # test_qubit_spectroscopy_q2_classify(img_small_path)
        # test_qubit_spectroscopy_q3_reasoning(img_small_path)
        # test_qubit_spectroscopy_q4_assess(img_small_path)
        # test_qubit_spectroscopy_q5_extract(img_small_path)
        # test_qubit_spectroscopy_q6_status(img_small_path)
        # print("\nQubit_Spectroscopy tests passed!")

        # 5.无参数更新
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=[img_save_path],
            completed_at=datetime.now()
        )
        print("Measurement finished, no parameter update")

    except Exception as e:
        err_msg = f"Measure failed: {str(e)}"
        store.update_run(
            run_id=run_id,
            status="failed",
            error=err_msg,
            completed_at=datetime.now()
        )
        print(f"Task failed run_id={run_id[:8]} error: {err_msg}")
        raise

if __name__ == '__main__':
    cli_args = parse_args()
    get_singleshot_hdf5_res(cli_args)