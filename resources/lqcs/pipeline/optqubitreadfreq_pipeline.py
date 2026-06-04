import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PIL import Image
import json

from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import optqubitreadfreq
from analysis.visualization import plot_optqubitreadfreq

SAVE_PLOT_FOLDER = './tmp'


def get_optqubitreadfreq_hdf5_res():
    # 1.采集数据
    qubit_ctrl_client = QubitCtrlClient()
    qubit_name_list = ["q3lu7"]


    qname=qubit_name_list[0]
    task_type=CtrlTaskName.OPTQUBITREADFREQ
    fread = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM,qname=qname, task_type=task_type, key="fread")
    
    data = qubit_ctrl_client.run(CtrlTaskName.OPTQUBITREADFREQ,
                                   qubits=qubit_name_list,
                                   freq_span_center=fread,
                                   freq_span_half_bandwidth=0.0055,
                                   freq_span_sample_num=40)
    data_id = data[0]["text"]
    data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

    data = json.loads(data[0]["text"])

    # 2.分析数据
    analysis_result = optqubitreadfreq(data)

    # 3.绘图
    pure_name = qubit_name_list[0]
    img_save_path = f'{SAVE_PLOT_FOLDER}/optqubitreadfreq_{pure_name}.png'
    fig_list = plot_optqubitreadfreq(data, analysis_result, save_path=img_save_path)

    # 4.更新fread
    qname=qubit_name_list[0]
    task_type=CtrlTaskName.OPTQUBITREADFREQ
    values="6.590"   
    qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)

if __name__ == '__main__':
    get_optqubitreadfreq_hdf5_res()