

from .scope_api.api.defined_tasks import s21peak_api_v1_tasks_scope_s21peak_post
from .scope_api.api.defined_tasks import optpipulse_api_v1_tasks_scope_optpipulse_post
from .scope_api.api.defined_tasks import rabi_api_v1_tasks_scope_rabi_post
from .scope_api.api.defined_tasks import rabicos_api_v1_tasks_scope_rabicospeak_post
from .scope_api.api.defined_tasks import s21vflux_api_v1_tasks_scope_s21vflux_post
from .scope_api.api.defined_tasks import singleshot_api_v1_tasks_scope_singleshot_post
from .scope_api.api.defined_tasks import spectrum_api_v1_tasks_scope_spectrum_post
from .scope_api.api.defined_tasks import t1fit_api_v1_tasks_scope_t1fit_post
from .scope_api.api.defined_tasks import t1fit_api_v1_tasks_scope_t2fit_post
from .scope_api.api.defined_tasks import spectrum2d_api_v1_tasks_scope_spectrum2d_post
from .scope_api.api.defined_tasks import powershift_api_v1_tasks_scope_powershift_post


from .scope_api.models import BodyS21PeakApiV1TasksScopeS21PeakPost
from .scope_api.models import BodyOptpipulseApiV1TasksScopeOptpipulsePost
from .scope_api.models import BodyRabiApiV1TasksScopeRabiPost
from .scope_api.models import BodyRabicosApiV1TasksScopeRabicospeakPost
from .scope_api.models import BodyS21VfluxApiV1TasksScopeS21VfluxPost
from .scope_api.models import BodySingleshotApiV1TasksScopeSingleshotPost
from .scope_api.models import BodySpectrumApiV1TasksScopeSpectrumPost
from .scope_api.models import BodyT1FitApiV1TasksScopeT1FitPost
from .scope_api.models import BodyT1FitApiV1TasksScopeT2FitPost
from .scope_api.models import BodySpectrum2DApiV1TasksScopeSpectrum2DPost
from .scope_api.models import BodyPowershiftApiV1TasksScopePowershiftPost


from .scope_api.types import Response
from .scope_api.types import File

import io
import numpy as np
def load_from_dict(dict_list: list[dict]):
    files = []
    for index, dict_obj in enumerate(dict_list):
        with io.BytesIO() as buffer:
            # np.savez(buffer, **dict_obj) # save xxx.npz
            np.save(buffer, dict_obj)
            bytes_obj = buffer.getvalue()
            # 假设File类定义如下：
            # File(payload=bytes内容, file_name=字符串)
            files.append(File(payload=bytes_obj, file_name=f"file_{index}.npy"))
    return files

def load_from_ndarray(ndarray_list: list[np.ndarray]):
    files = []
    for idx, ndarray_data in enumerate(ndarray_list):
        buffer = io.BytesIO()
        np.save(buffer, ndarray_data)
        buffer.seek(0)
        files.append(File(payload=buffer.read(), file_name=f"file_{idx}.npy"))
    return files

def load_from_path(filepath_list: list[str]):
    files = []
    for file_path in filepath_list:
        with open(file_path, "rb") as f:
            file_content = f.read()
            files.append(File(payload=file_content, file_name=file_path))
    return files
def load_files(filepath_list: list[str|dict[str,np.ndarray]|np.ndarray]):
    if len(filepath_list)<=0:
        return []
    else:
        if isinstance(filepath_list[0], dict):
            return load_from_dict(filepath_list)
        elif isinstance(filepath_list[0], np.ndarray):
            return load_from_ndarray(filepath_list)
        elif isinstance(filepath_list[0], str):
            return load_from_path(filepath_list)
        
DEFINED_TASKS = {}
def task_register(func):
    DEFINED_TASKS[func.__name__.lower()] = func
    return func

def run_task(client,file_list: list[str|dict[str,np.ndarray]|np.ndarray],task_type:str):
    files = load_files(file_list)
    response = DEFINED_TASKS[task_type.value](client,files)
    return response


@task_register
def s21peak(client,files: File):
    body: BodyS21PeakApiV1TasksScopeS21PeakPost = BodyS21PeakApiV1TasksScopeS21PeakPost(files=files)
    response: Response[BodyS21PeakApiV1TasksScopeS21PeakPost] = s21peak_api_v1_tasks_scope_s21peak_post.sync_detailed(client=client,body=body)
    return response
@task_register
def optpipulse(client,files: File):
    body: BodyOptpipulseApiV1TasksScopeOptpipulsePost = BodyOptpipulseApiV1TasksScopeOptpipulsePost(files=files)
    response: Response[BodyOptpipulseApiV1TasksScopeOptpipulsePost] = optpipulse_api_v1_tasks_scope_optpipulse_post.sync_detailed(client=client,body=body)
    return response
@task_register
def rabi(client,files: File):
    body: BodyRabiApiV1TasksScopeRabiPost = BodyRabiApiV1TasksScopeRabiPost(files=files)
    response: Response[BodyRabiApiV1TasksScopeRabiPost] = rabi_api_v1_tasks_scope_rabi_post.sync_detailed(client=client,body=body)
    return response
@task_register
def ramsey(client,files: File):
    body: BodyRabiApiV1TasksScopeRabiPost = BodyRabiApiV1TasksScopeRabiPost(files=files)
    response: Response[BodyRabiApiV1TasksScopeRabiPost] = rabi_api_v1_tasks_scope_rabi_post.sync_detailed(client=client,body=body)
    return response
@task_register
def rabicos(client,files: File):
    body: BodyRabicosApiV1TasksScopeRabicospeakPost = BodyRabicosApiV1TasksScopeRabicospeakPost(files=files)
    response: Response[BodyRabicosApiV1TasksScopeRabicospeakPost] = rabicos_api_v1_tasks_scope_rabicospeak_post.sync_detailed(client=client,body=body)
    return response
@task_register
def s21vfluxscope(client,files: File):
    body: BodyS21VfluxApiV1TasksScopeS21VfluxPost = BodyS21VfluxApiV1TasksScopeS21VfluxPost(files=files)
    response: Response[BodyS21VfluxApiV1TasksScopeS21VfluxPost] = s21vflux_api_v1_tasks_scope_s21vflux_post.sync_detailed(client=client,body=body)
    return response
@task_register
def singleshot(client,files: File):
    body: BodySingleshotApiV1TasksScopeSingleshotPost = BodySingleshotApiV1TasksScopeSingleshotPost(files=files)
    response: Response[BodySingleshotApiV1TasksScopeSingleshotPost] = singleshot_api_v1_tasks_scope_singleshot_post.sync_detailed(client=client,body=body)
    return response
@task_register
def spectrum(client,files: File):
    body: BodySpectrumApiV1TasksScopeSpectrumPost = BodySpectrumApiV1TasksScopeSpectrumPost(files=files)
    response: Response[BodySpectrumApiV1TasksScopeSpectrumPost] = spectrum_api_v1_tasks_scope_spectrum_post.sync_detailed(client=client,body=body)
    return response
@task_register
def t1fit(client,files: File):
    body: BodyT1FitApiV1TasksScopeT1FitPost = BodyT1FitApiV1TasksScopeT1FitPost(files=files)
    response: Response[BodyT1FitApiV1TasksScopeT1FitPost] = t1fit_api_v1_tasks_scope_t1fit_post.sync_detailed(client=client,body=body)
    return response
@task_register
def t2fit(client,files: File):
    body: BodyT1FitApiV1TasksScopeT2FitPost = BodyT1FitApiV1TasksScopeT2FitPost(files=files)
    response: Response[BodyT1FitApiV1TasksScopeT2FitPost] = t1fit_api_v1_tasks_scope_t2fit_post.sync_detailed(client=client,body=body)
    return response

@task_register
def spectrum2dscope(client,files: File):
    body: BodySpectrum2DApiV1TasksScopeSpectrum2DPost = BodySpectrum2DApiV1TasksScopeSpectrum2DPost(files=files)
    response: Response[BodySpectrum2DApiV1TasksScopeSpectrum2DPost] = spectrum2d_api_v1_tasks_scope_spectrum2d_post.sync_detailed(client=client,body=body)
    return response
@task_register
def powershift(client,files: File):
    body: BodyPowershiftApiV1TasksScopePowershiftPost = BodyPowershiftApiV1TasksScopePowershiftPost(files=files)
    response: Response[BodyPowershiftApiV1TasksScopePowershiftPost] = powershift_api_v1_tasks_scope_powershift_post.sync_detailed(client=client,body=body)
    return response

from enum import Enum, unique
@unique
class TaskName(Enum):
    S21PEAK = "s21peak"
    OPTPIPULSE = "optpipulse"
    RABI = "rabi"
    RAMSEY = "ramsey"
    RABICOS = "rabicos"
    S21VFLUX = "s21vfluxscope"
    SINGLESHOT = "singleshot"
    SPECTRUM = "spectrum"
    T1FIT = "t1fit"
    T2FIT = "t2fit"
    SPECTRUM2D = "spectrum2dscope"
    POWERSHIFT = "powershift"




