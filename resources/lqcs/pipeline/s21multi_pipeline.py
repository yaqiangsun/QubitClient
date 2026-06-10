import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PIL import Image
import json

from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

from analysis.inception import nns21multi, s21multi
from analysis.visualization import plot_nns21multi, plot_s21multi

SAVE_PLOT_FOLDER = './tmp'

base_freq_dict = {
    'q1lu7': 6.561,
    'q2lu7': 6.759,
    'q3lu7': 6.590,
    'q4lu7': 6.762,
    'q5lu7': 6.539,
    'q6lu7': 6.763,
    'q7lu7': 6.611,
    'q8lu7': 6.803,
    'q9lu7': 6.634,
    'q10lu7': 6.855,
    'q11lu7': 6.666,
    'q12lu7': 6.876,
}

def get_s21multi_hdf5_res():
    # 1.采集数据
    qubit_ctrl_client = QubitCtrlClient()
    qubit_name_list = ["q3lu7"]
    data = qubit_ctrl_client.run(CtrlTaskName.S21MULTI,
                                    qubits=qubit_name_list,
                                    frequency_start=6.5,
                                    frequency_end=6.8,
                                    frequency_sample_rate=0.0002)
    
    data_id = data[0]["text"]
    data = qubit_ctrl_client.run(CtrlTaskName.DATA,rid=data_id)

    data = json.loads(data[0]["text"])

    # 2.分析数据
    analysis_result = s21multi(data)

    # 3.绘图
    pure_name = qubit_name_list[0]
    img_save_path = f'{SAVE_PLOT_FOLDER}/s21multi_{pure_name}.png'
    fig_list = plot_s21multi(data, analysis_result, save_path=img_save_path)


    #  4.更新
    if type(analysis_result)==dict:
        if "results" not in analysis_result.keys():
            analysis_result = analysis_result.get("results")
        elif "result" in analysis_result.keys():
            analysis_result = analysis_result.get("result")
    for result in analysis_result:
        peaks_list = result['peaks']
        confs_list = result['confs']
        freqs_list = result['freqs_list']
        for i in range(len(qubit_name_list)):
            peaks = peaks_list[i]
            confs = confs_list[i]
            freqs = freqs_list[i]
            qname=qubit_name_list[i]
            base_freq = base_freq_dict.get(qname) 
            if(len(freqs)): 
                closest_freq = min(freqs, key=lambda f: abs(f - base_freq))
                print("[INFO] update : ", closest_freq, qname)
                values=str(closest_freq)
                task_type=CtrlTaskName.S21MULTI
                # qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM, 
                #                     qname=qname, 
                #                     task_type=task_type, 
                #                     values=values)
                qubit_ctrl_client.update_param(qname=qname, 
                                    task_type=task_type, 
                                    values=values)
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
    get_s21multi_hdf5_res()