import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PIL import Image
import json
import numpy as np

from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import nnspectrum
from analysis.visualization import plot_nnspectrum

SAVE_PLOT_FOLDER = './tmp'


def get_spectrum_hdf5_res():
    # 1.采集数据
    qubit_ctrl_client = QubitCtrlClient()
    qubit_name_list = ["q3lu7"]
    
    data = qubit_ctrl_client.run(CtrlTaskName.SPECTRUM,
                                   qubits=qubit_name_list,
                                   freq_start=-3,
                                   freq_end=3,
                                   freq_sample_num=200,
                                   bias=0,
                                   drive_amp=0.0)
    data_id = data[0]["text"]
    data = qubit_ctrl_client.run(CtrlTaskName.DATA, rid=data_id)

    data = json.loads(data[0]["text"])

    # 2.分析数据
    analysis_result = nnspectrum(data)

    # 3.绘图
    pure_name = qubit_name_list[0]
    img_save_path = f'{SAVE_PLOT_FOLDER}/spectrum_{pure_name}.png'
    fig_list = plot_nnspectrum(data, analysis_result, save_path=img_save_path)

    # 4.更新f10, f21
    # 根据扫描结果更新
    # 4.更新f10, f21
    for result in analysis_result:
        peaks_list = result['peaks_list']
        confidences_list = result['confidences_list']
        for i in range(len(qubit_name_list)):
            peaks = peaks_list[i]
            confidences = confidences_list[i]
            best_idx = confidences.index(max(confidences))
            best_peak = peaks[best_idx]
            target_freq =best_peak
            non=-0.2
            values=str(target_freq) + ',' + str(target_freq + non)
            qname=qubit_name_list[i]
            task_type=CtrlTaskName.SPECTRUM
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
    get_spectrum_hdf5_res()