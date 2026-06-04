import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PIL import Image
import json

from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import s21
from analysis.visualization import plot_s21

SAVE_PLOT_FOLDER = './tmp'


def get_s21_hdf5_res():
    # 1.数据采集
    qubit_ctrl_client = QubitCtrlClient()
    qubit_name_list = ["q3lu7"]
    fread = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM, key="fread")

    data = qubit_ctrl_client.run(CtrlTaskName.S21,
                                    qubits=qubit_name_list,
                                    frequency_center=fread,
                                    frequency_half_bandwidth=0.005,
                                    frequency_sample_num=200)

    data_id = data[0]["text"]
    data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)

    data = json.loads(data[0]["text"])

    # 2.分析数据
    analysis_result = s21(data)

    # 3.绘图
    pure_name = qubit_name_list[0]
    img_save_path = f'{SAVE_PLOT_FOLDER}/s21peak_{pure_name}.png'
    fig_list = plot_s21(data, analysis_result, save_path=img_save_path)


    #  4.更新
    qname=qubit_name_list[0]
    task_type=CtrlTaskName.S21
    values="6.590"   
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
    get_s21_hdf5_res()