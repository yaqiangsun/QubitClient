import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import math
from PIL import Image
import json

from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import ramsey
from analysis.visualization import plot_ramsey

SAVE_PLOT_FOLDER = './tmp'


def get_ramsey_hdf5_res():
    # 1.采集数据
    qubit_ctrl_client = QubitCtrlClient()
    qubit_name_list = ["q3lu7"]
    fringeFreq= 0.05
    data = qubit_ctrl_client.run(CtrlTaskName.RAMSEY,
                                   qubits=qubit_name_list,
                                   delay_start=0,
                                   delay_end=100,
                                   delay_sample_num=100,
                                   fringeFreq=fringeFreq)
    data_id = data[0]["text"]
    data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

    data = json.loads(data[0]["text"])

    # 2.分析数据
    analysis_result = ramsey(data)

    # 3.绘图
    pure_name = qubit_name_list[0]
    img_save_path = f'{SAVE_PLOT_FOLDER}/ramsey_{pure_name}.png'
    fig_list = plot_ramsey(data, analysis_result, save_path=img_save_path)

    # 4.更新f10, f21
    for result in analysis_result:
            params_list = result['params_list']
            r2_list = result['r2_list']
            fit_data_list = result['fit_data_list']
            for i in range(len(qubit_name_list)):
                params = params_list[i]
                w = params[4]
                qname=qubit_name_list[i]
                task_type=CtrlTaskName.RAMSEY
                f10 = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM,qname=qname, key="f10_star")
                deltaf = w /(2*math.pi)         # 失谐量（Hz）
                if(fringeFreq>f10):
                    target_freq = fringeFreq - deltaf    # 如果 f_measure > f10
                
                else:
                     target_freq = fringeFreq + deltaf    # 如果 f_measure < f10
                non=-0.2
                values=str(target_freq) + ',' + str(target_freq + non)
                task_type=CtrlTaskName.RAMSEY
                qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,qname=qname, task_type=task_type, values=values)
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


    # 4.接入大模型分析图片
    # test_qubit_spectroscopy_q1_describe(img_small_path)
    # test_qubit_spectroscopy_q2_classify(img_small_path)
    # test_qubit_spectroscopy_q3_reasoning(img_small_path)
    # test_qubit_spectroscopy_q4_assess(img_small_path)
    # test_qubit_spectroscopy_q5_extract(img_small_path)
    # test_qubit_spectroscopy_q6_status(img_small_path)
    # print("\nQubit_Spectroscopy tests passed!")


if __name__ == '__main__':
    get_ramsey_hdf5_res()