import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from PIL import Image
import json
import numpy as np

from lib.data_read import get_latest_content
from analysis.inception import nns21vsflux
from analysis.visualization import plot_nns21vsflux

from lqms.measure.tuners import sq_nodes as sq
from lqms.measure import (
    generate_coupler,
    generate_qubit,
)
info=None
from sqcommand.lib.backend import s

_all_qubits = generate_qubit(globals(), info=info, sample=s)
_all_couplers = generate_coupler(globals(), info=info, sample=s)

SAVE_PLOT_FOLDER = './tmp'
ROOT_FOLDER = 'D:/DataVault/LQHL.dir/test.dir/20260324.dir/'


def get_s21vflux_hdf5_res():
    # 1.数据采集
    # result = sq.s21_zpa2d(q2lu7, freq=None, zpa=None, freq_span=None, update=False)
    q3lu7.regs.fread = 6.5898 # 设置待测⽐特的频率//  6.539 6.561 6.589
    result = sq.s21_zpa2d(q3lu7)

    # 2.找到最新的指定task_type的hdf5文件内容
    data, pure_name = get_latest_content(ROOT_FOLDER, task_type="zpa")


    # 3.分析数据
    analysis_result = nns21vsflux(data)

    # 4.绘图
    pure_name = 'q2lu7'
    img_save_path = f'{SAVE_PLOT_FOLDER}/nns21vflux_{pure_name}.png'
    fig_list = plot_nns21vsflux(data, analysis_result, save_path=img_save_path)

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


    # 5.接入大模型分析图片
    # test_qubit_spectroscopy_q1_describe(img_small_path)
    # test_qubit_spectroscopy_q2_classify(img_small_path)
    # test_qubit_spectroscopy_q3_reasoning(img_small_path)
    # test_qubit_spectroscopy_q4_assess(img_small_path)
    # test_qubit_spectroscopy_q5_extract(img_small_path)
    # test_qubit_spectroscopy_q6_status(img_small_path)
    # print("\nQubit_Spectroscopy tests passed!")


if __name__ == '__main__':
    get_s21vflux_hdf5_res()