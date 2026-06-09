import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PIL import Image
import json

from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

# from analysis.inception import pulseshape
# from analysis.visualization import plot_pulseshape

SAVE_PLOT_FOLDER = './tmp'


def get_pulseshape_hdf5_res():
    # 1.采集数据
    qubit_ctrl_client = QubitCtrlClient()
    qubit_name_list = ["q3lu7"]
    
    data = qubit_ctrl_client.run(CtrlTaskName.PULSESHAPE,
                                   qubits=qubit_name_list,
                                   step_height=0.2)
    data_id = data[0]["text"]
    data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

    data = json.loads(data[0]["text"])

    # # 2.分析数据
    # analysis_result = pulseshape(data)

    # # 3.绘图
    # pure_name = qubit_name_list[0]
    # img_save_path = f'{SAVE_PLOT_FOLDER}/pulseshape_{pure_name}.png'
    # fig_list = plot_pulseshape(data, analysis_result, save_path=img_save_path)

    # # 无参数更新


if __name__ == '__main__':
    get_pulseshape_hdf5_res()