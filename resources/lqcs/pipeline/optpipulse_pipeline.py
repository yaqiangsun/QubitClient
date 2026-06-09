import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PIL import Image
import json

from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import optpipulse
from analysis.visualization import plot_optpipulse

SAVE_PLOT_FOLDER = './tmp'


def get_opt_pipulse_hdf5_res():
    # 1.采集数据 - X门
    qubit_ctrl_client = QubitCtrlClient()
    qubit_name_list = ["q3lu7"]
    
    data = qubit_ctrl_client.run(CtrlTaskName.OPTPIPULSE,
                                   qubits=qubit_name_list,
                                   N_list=[1,4,8],
                                   amp_list=None)
    data_id = data[0]["text"]
    data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

    data = json.loads(data[0]["text"])

    # 2.分析数据
    analysis_result = optpipulse(data)

    # 3.绘图
    pure_name = qubit_name_list[0]
    img_save_path = f'{SAVE_PLOT_FOLDER}/optpipulse_{pure_name}.png'
    fig_list = optpipulse(data, analysis_result, save_path=img_save_path)

    # 4.更新PiGate.amp和PiGate.alpha
   
    qname=qubit_name_list[0]
    task_type=CtrlTaskName.OPTPIPULSE
    values="3.193120459017055,3.193120459017055"   
    qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)

    # # 4.更新PiHalf.amp和PiHalf.alpha
   
    # qname=qubit_name_list[0]
    # task_type=CtrlTaskName.OPTPIPULSE
    # values="Null,Null,3.193120459017055,3.193120459017055"   
    # qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)

if __name__ == '__main__':
    get_opt_pipulse_hdf5_res()