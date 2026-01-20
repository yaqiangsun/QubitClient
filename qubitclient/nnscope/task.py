
import os
import requests

import io
import numpy as np


from qubitclient.nnscope.utils.data_convert import convert_spectrum_npy2npz,convert_spectrum_dict2npz

# load from npz file path
def load_from_npz_path(file_path_list:list[str]):
    files = []
    npydata = {}
    npydata['id'] = 0
    image_qs = {}
    index = 0
    for file_path in file_path_list:
        if file_path.endswith('.npz'):
            index+=1
            with np.load(file_path, allow_pickle=True) as data:  # 修改：添加 allow_pickle=True 参数
                # file_contents[file_name] = dict(data)  # 将 .npz 文件内容转换为字典
                content = dict(data)  # 将 .npz 文件内容转换为字典
                image_qs[str(index)] = (content['iq_avg'],content['bias'],content['frequency'])
    npydata['image'] = image_qs
    with io.BytesIO() as buffer:
        np.save(buffer, npydata)
        bytes_obj = buffer.getvalue()
    files.append(("request", ("None.npy", bytes_obj, "application/octet-stream")))
    return files
# def load_from_npz_path(file_path_list:list[str]):
#     files = []
#     npydata = {}
#     npydata['id'] = 0
#     index = 0
#     for file_path in file_path_list:
#         if file_path.endswith('.npz'):
#             index+=1
#             with np.load(file_path, allow_pickle=True) as data:  # 修改：添加 allow_pickle=True 参数
#                 # file_contents[file_name] = dict(data)  # 将 .npz 文件内容转换为字典
#                 content = dict(data)  # 将 .npz 文件内容转换为字典
#                 allq = content['image'].item()
#                 allq_downsample={}
#                 for q in allq.keys():
#                     singleq = allq[q]
#                     singleq_downsampe = (singleq[0][::1,::1],singleq[1][::1],singleq[2][::1])
#                     # iq = zoom(singleq[0],(2,1),order=1)
#                     # zero_arr = np.zeros((45,40))
#                     # iq = np.vstack((singleq[0],zero_arr))
#                     # # iq = np.vstack((singleq[0],singleq[0]))
#                     #
#                     # arr_2d = singleq[2].reshape(1,-1)
#                     # arr_zoomed = zoom(arr_2d,(1,2),order=1)
#                     # freq = arr_zoomed.flatten()
#                     #
#                     #
#                     # singleq_downsampe = (iq[::1,::1],singleq[1][::1],freq)
#
#
#                     # singleq_downsampe = (singleq[0],singleq[1],singleq[2])
#
#                     allq_downsample[q] = singleq_downsampe
#                 # allq_downsample  = np.array(allq_downsample,dtype=object).reshape(())
#                 # npydata['image'] = (content['image'])
#                 npydata['image'] = allq_downsample
#     with io.BytesIO() as buffer:
#         np.save(buffer, npydata)
#         bytes_obj = buffer.getvalue()
#     files.append(("request", ("None.npy", bytes_obj, "application/octet-stream")))
#     return files
def load_from_npy_path(file_path_list:list[str]):
    files = []
    for file_path in file_path_list:
        if file_path.endswith('.npy'):
            data = np.load(file_path, allow_pickle=True)
            data = data.item() if isinstance(data, np.ndarray) else data
            with io.BytesIO() as buffer:
                np.save(buffer, data)
                bytes_obj = buffer.getvalue()
            files.append(("request", ("None.npy", bytes_obj, "application/octet-stream")))
    return files
def load_from_npz_dict(dict_list:list[dict]):
    files = []
    npydata = {}
    npydata['id'] = 0
    image_qs = {}
    for index,dict_obj in enumerate(dict_list):
        image_qs[str(index)] = (dict_obj['iq_avg'], dict_obj['bias'], dict_obj['frequency'])
    npydata['image'] = image_qs
    with io.BytesIO() as buffer:
        np.save(buffer, npydata)
        bytes_obj = buffer.getvalue()
    files.append(("request", ("None.npy", bytes_obj, "application/octet-stream")))
    return files
def load_from_npy_dict(dict_list:list[dict]):
    files = []
    for dict_obj in dict_list:
        with io.BytesIO() as buffer:
            np.save(buffer, dict_obj)
            bytes_obj = buffer.getvalue()
        files.append(("request", ("None.npy",bytes_obj, "application/octet-stream")))
    return files
def request_task(files,url,api_key,curve_type:str=None):
    headers = {'Authorization': f'Bearer {api_key}'}  # 添加API密钥到请求头
    data = {
            "curve_type":curve_type.value if curve_type else None
    }
    response = requests.post(url, files=files, headers=headers,data=data)
    return response
def load_files(filepath_list: list[str|dict[str,np.ndarray]|np.ndarray]):
    if len(filepath_list)<=0:
        return []
    else:
        if isinstance(filepath_list[0], dict):
            if "image" in filepath_list[0]:
                return load_from_npy_dict(filepath_list)
            else:
                return load_from_npz_dict(filepath_list)
        elif isinstance(filepath_list[0], np.ndarray):
            filepath_list = [filepath_list[i].item() for i in range(len(filepath_list))]
            return load_files(filepath_list)
        elif isinstance(filepath_list[0], str):
            if filepath_list[0].endswith('.npz'):
                return load_from_npz_path(filepath_list)
            elif filepath_list[0].endswith('.npy'):
                return load_from_npy_path(filepath_list)
            else:
                return []



DEFINED_TASKS = {}
def task_register(func):
    DEFINED_TASKS[func.__name__.lower()] = func
    return func

def run_task(file_list: list[str|dict[str,np.ndarray]|np.ndarray],url,api_key,task_type:str,*args,**kwargs):
    files = load_files(file_list)
    response = DEFINED_TASKS[task_type.value](files,url,api_key,*args,**kwargs)
    return response


@task_register
def test(files):
    
    return "hello"

@task_register
def spectrum2dnnscope(files,url,api_key,curve_type):
    spectrum2d_url = url + "/api/v1/tasks/nnscope/seglines"
    response = request_task(files,spectrum2d_url,api_key,curve_type)
    return response
@task_register
def s21vfluxnnscope(files,url,api_key,curve_type):
    spectrum2d_url = url + "/api/v1/tasks/nnscope/s21vflux"
    response = request_task(files,spectrum2d_url,api_key,curve_type)
    return response

@task_register
def powershiftnnscope(files,url,api_key,curve_type):
    spectrum2d_url = url + "/api/v1/tasks/nnscope/powershift"
    response = request_task(files,spectrum2d_url,api_key,curve_type)
    return response

from enum import Enum, unique
@unique
class NNTaskName(Enum):
    # S21PEAK = "s21peak"
    # OPTPIPULSE = "optpipulse"
    # RABI = "rabi"
    # RABICOS = "rabicos"
    # S21VFLUX = "s21vflux"
    # SINGLESHOT = "singleshot"
    # SPECTRUM = "spectrum"
    # T1FIT = "t1fit"
    # T2FIT = "t2fit"
    SPECTRUM2D = "spectrum2dnnscope"
    S21VFLUX = "s21vfluxnnscope"
    POWERSHIFT = "powershiftnnscope"



