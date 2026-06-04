import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PIL import Image
import json

from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import spectrum2d
from analysis.visualization import plot_spectrum2d

SAVE_PLOT_FOLDER = './tmp'


def get_spectrum2d_hdf5_res():
    # 1.采集数据

    # qubit_ctrl_client = QubitCtrlClient()
    # qubit_name_list = ["q2lu7"]

    # power_array = np.linspace(-30, -10, 21).tolist()  # 功率范围
    # freq_array = np.linspace(-50e6, 50e6, 101).tolist()  # 频率范围
    
    # result = qubit_ctrl_client.run(CtrlTaskName.POWERSHIFT,
    #                               qubits=qubit_name_list,
    #                               power=power_array,
    #                               freq=freq_array
    #                               )
    
    # data_id = data[0]["text"]
    # data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)
    # tmp = data[0]["text"]

    # print("type(tmp): ", type(tmp))
    # data = json.loads(data[0]["text"])
    # print("data:",data)
    

    # 2.分析数据
    # analysis_result = spectrum2d(data)

    # 3.绘图
    # qubit_name_list = ['q2lu7']
    # pure_name = qubit_name_list[0]
    # img_save_path = f'{SAVE_PLOT_FOLDER}/spectrum2d_{pure_name}.png'
    # fig_list = plot_spectrum2d(data, analysis_result, save_path=img_save_path)

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
    get_spectrum2d_hdf5_res()