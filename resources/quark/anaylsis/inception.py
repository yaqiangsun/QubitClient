# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/01/27 17:48:06
########################################################################

from qubitclient import QubitNNScopeClient,QubitScopeClient
from qubitclient import NNTaskName,TaskName,CurveType
from .config import API_URL,API_KEY,ENABLE_API
import logging
from .wrapper_handler import handle_exceptions, control_api_execution
from .format import optpipulse_convert
def nnscope_template(image,task_type=NNTaskName.SPECTRUM2D):

    client = QubitNNScopeClient(url=API_URL,api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray],task_type=task_type,curve_type=CurveType.COSINE)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results
def scope_template(image,task_type=TaskName.SPECTRUM2D):
    client = QubitScopeClient(url=API_URL,api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray],task_type=task_type)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results
####################################################################################

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nnspectrum2d(image):

    results = nnscope_template(image,task_type=NNTaskName.SPECTRUM2D)
    return results
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nnpowershift(image):
    results = nnscope_template(image,task_type=NNTaskName.POWERSHIFT)
    return results
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nnspectrum(image):
    results = nnscope_template(image,task_type=NNTaskName.SPECTRUM)
    return results


####################################################################################
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def s21(image):
    results = scope_template(image,task_type=TaskName.S21PEAK)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def rabi(image):
    results = scope_template(image,task_type=TaskName.RABI)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def ramsey(image):
    results = scope_template(image,task_type=TaskName.RAMSEY)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def t1fit(image):
    results = scope_template(image,task_type=TaskName.T1FIT)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def t2fit(image):
    results = scope_template(image,task_type=TaskName.T2FIT)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def optpipulse(image):
    image = optpipulse_convert(image)
    results = scope_template(image,task_type=TaskName.OPTPIPULSE)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def spectrum(image):
    results = scope_template(image,task_type=TaskName.SPECTRUM)
    return results
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def powershift(image):
    results = scope_template(image,task_type=TaskName.POWERSHIFT)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def s21vsflux(image):
    results = scope_template(image,task_type=TaskName.S21VFLUX)
    return results
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def allxy_drag(image):
    results = scope_template(image,task_type=TaskName.DRAG)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def singleshot(image):
    results = scope_template(image,task_type=TaskName.SINGLESHOT)
    return results