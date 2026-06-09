import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PIL import Image
import json
import numpy as np

from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import pipulsef10
from analysis.visualization import plot_pipulsef10

SAVE_PLOT_FOLDER = './tmp'


def get_pipulsef10_hdf5_res():
    # 1.采集数据
    qubit_ctrl_client = QubitCtrlClient()
    qubit_name_list = ["q3lu7"]
    
    data = qubit_ctrl_client.run(CtrlTaskName.PIPULSEF10,
                                   qubits=qubit_name_list,
                                   df_start=0,
                                   df_end=0.03,
                                   df_sample_num=21)
    data_id = data[0]["text"]
    data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

    data = json.loads(data[0]["text"])

    # 2.分析数据
    analysis_result = pipulsef10(data)

    # 3.绘图
    pure_name = qubit_name_list[0]
    img_save_path = f'{SAVE_PLOT_FOLDER}/pipulsef10_{pure_name}.png'
    fig_list = plot_pipulsef10(data, analysis_result, save_path=img_save_path)

    # 4.更新f10, f21
    
    qname=qubit_name_list[0]
    task_type=CtrlTaskName.PIPULSEF10
    values="3.193120459017055,3.193120459017055"   
    qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)

if __name__ == '__main__':
    get_pipulsef10_hdf5_res()