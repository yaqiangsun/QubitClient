
import os
import requests

import io
import numpy as np


from qubitclient.nnscope.utils.data_convert import convert_spectrum_npy2npz,convert_spectrum_dict2npz

# load from npz file path
def load_from_npz_path(file_path_list:list[str]):
    files = []
    for file_path in file_path_list:
        if file_path.endswith('.npz'):
            file_name = os.path.basename(file_path)
            files.append(("request", (file_name, open(file_path, "rb"), "image/jpeg")))
    return files
def load_from_npy_path(file_path_list:list[str]):
    files = []
    for file_path in file_path_list:
        if file_path.endswith('.npy'):
            dict_list, name_list = convert_spectrum_npy2npz(file_path)
            for data_dict, filename in zip(dict_list, name_list):
                with io.BytesIO() as buffer:
                    np.savez(buffer, **data_dict)
                    bytes_obj = buffer.getvalue()
                files.append(("request", (filename, bytes_obj, "application/octet-stream")))
    return files
def load_from_npz_dict(dict_list:list[dict]):
    files = []
    for index,dict_obj in enumerate(dict_list):
        with io.BytesIO() as buffer:
            np.savez(buffer, **dict_obj)
            bytes_obj = buffer.getvalue()
        files.append(("request", ("None"+str(index)+".npz", bytes_obj, "application/octet-stream")))
    return files
def load_from_npy_dict(dict_list:list[dict]):
    files = []
    for dict_obj in dict_list:
        qubit_dict_list, name_list = convert_spectrum_dict2npz(dict_obj)
        
        for data_dict, filename in zip(qubit_dict_list, name_list):
            with io.BytesIO() as buffer:
                np.savez(buffer, **data_dict)
                bytes_obj = buffer.getvalue()
            files.append(("request", (filename, bytes_obj, "application/octet-stream")))
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
        # elif isinstance(filepath_list[0], np.ndarray):
        #     return load_from_ndarray(filepath_list)
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
def spectrum2d(files,url,api_key,curve_type):
    spectrum2d_url = url + "/seglines"
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
    SPECTRUM2D = "spectrum2d"




