
import os
import requests

import io
import numpy as np


# load from npz file path
def load_from_ndarray_path(file_path_list:list[str]):
    files = []
    for file_path in file_path_list:
        if file_path.endswith('.npz'):
            file_name = os.path.basename(file_path)
            files.append(("request", (file_name, open(file_path, "rb"), "image/jpeg")))
    return files
def load_from_dict(dict_list:list[dict]):
    files = []
    for index,dict_obj in enumerate(dict_list):
        with io.BytesIO() as buffer:
            np.savez(buffer, **dict_obj)
            bytes_obj = buffer.getvalue()
        files.append(("request", ("None"+str(index)+".npz", bytes_obj, "application/octet-stream")))
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
            return load_from_dict(filepath_list)
        # elif isinstance(filepath_list[0], np.ndarray):
        #     return load_from_ndarray(filepath_list)
        elif isinstance(filepath_list[0], str):
            return load_from_ndarray_path(filepath_list)
        
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




