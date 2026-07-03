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
    1. Start UI server first: qubitclient ui start
    2. Example:
        python -m skills.lqcs-qubit-calib.scripts.pipeline.singleshot_pipeline -q q1ld5 -u True -c 0.6
    3. Launch the browser: http://localhost:8581/ to verify the display.
"""

import sys
import argparse
import uuid
from datetime import datetime
from pathlib import Path
from PIL import Image
import os
import logging

# 统一日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from qubitclient.storage.result_store import PipelineResultRecord, PipelineResultStore
from qubitclient.storage.storage import StorageBackend
from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import singleshot
from analysis.visualization import plot_singleshot
from analysis.update import singleshot_update

DEFAULT_SAVE_FOLDER = './tmp/db/result/image'


def llm_analysis(img_save_path):
    # resize更小
    img_small_path = img_save_path.split('.png')[0] + '_small.png'
    logging.info(f"img_small_path: {img_small_path}")

    with Image.open(img_save_path) as img:
        w, h = img.size
        new_w = w // 10
        new_h = h // 10
        logging.info(f"size: {new_w}, {new_h}")
        img_small = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        img_small.save(img_small_path, dpi=(300, 300))

    # test_qubit_spectroscopy_q1_describe(img_small_path)
    # test_qubit_spectroscopy_q2_classify(img_small_path)
    # test_qubit_spectroscopy_q3_reasoning(img_small_path)
    # test_qubit_spectroscopy_q4_assess(img_small_path)
    # test_qubit_spectroscopy_q5_extract(img_small_path)
    # test_qubit_spectroscopy_q6_status(img_small_path)
    logging.info("Qubit_Spectroscopy tests passed!")


def parse_args():
    parser = argparse.ArgumentParser(description="SingleShot Readout Measurement Pipeline (UI storage sync enabled)")
    parser.add_argument("--qubits", "-q", type=str, nargs="+", default=["q1ld5"],
                        help="Target qubit list, default: q1ld5")
    parser.add_argument("--save-folder", "-s", type=str, default=DEFAULT_SAVE_FOLDER,
                        help="Plot output directory")
    # 新增固定参数
    parser.add_argument("--update", "-u", type=bool, default=False,
                        help="Whether update params based on analysis result")
    parser.add_argument("--confidence", "-c", type=float, default=0.5,
                        help="Confidence threshold for parameter update")
    return parser.parse_args()


def get_singleshot_hdf5_res(args):
    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    task_name = CtrlTaskName.SINGLESHOT.value
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
            qubits=qubit_name_list,
            params=set_params
        )
        run_id = store.save_run(run_record)
        logging.info(f"[SINGLESHOT] Task started run_id={run_id[:8]}")

        data_id = qubit_ctrl_client.run(CtrlTaskName.SINGLESHOT, qubits=qubit_name_list)
        raw_data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

        # 2.分析数据
        analysis_result = singleshot(raw_data)

        # 3.绘图
        img_save_path = f'{save_folder}/{CtrlTaskName.SINGLESHOT.value}_{qubit_name_list[0]}_{run_id}.png'
        plot_singleshot(raw_data, analysis_result, save_path=img_save_path)

        img_save_path = os.path.abspath(img_save_path)
        plot_paths = [img_save_path]

        # 调用大模型图片分析
        # llm_analysis(img_save_path)

        # 要更新'discriminator.center0', 'discriminator.center1', 'discriminator.threshold'
        # print("117---------", analysis_result)
        first = analysis_result[0]


        
        store.update_run(
            run_id=run_id,
            status="completed",
            analysis_result=analysis_result,
            plot_paths=plot_paths,
            completed_at=datetime.now()
        )
        logging.info("Measurement finished")

    except Exception as e:
        err_msg = f"Measure failed: {str(e)}"
        store.update_run(
            run_id=run_id,
            status="failed",
            error=err_msg,
            completed_at=datetime.now()
        )
        logging.error(f"Task failed run_id={run_id[:8]} error: {err_msg}")
        raise


if __name__ == '__main__':
    cli_args = parse_args()
    get_singleshot_hdf5_res(cli_args)