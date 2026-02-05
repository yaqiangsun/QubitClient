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

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nnspectrum2d(image):

    client = QubitNNScopeClient(url=API_URL,api_key=API_KEY)
    data_ndarray = image
    # data_dict = data_ndarray.item() if isinstance(data_ndarray, np.ndarray) else data_ndarray
    response = client.request(file_list=[data_ndarray],task_type=NNTaskName.SPECTRUM2D,curve_type=CurveType.COSINE)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def s21(image):
    client = QubitScopeClient(url=API_URL,api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray],task_type=TaskName.S21PEAK)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nnpowershift(image):
    client = QubitNNScopeClient(url=API_URL,api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray],task_type=NNTaskName.POWERSHIFT)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nnspectrum(image):
    client = QubitNNScopeClient(url=API_URL,api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray],task_type=NNTaskName.SPECTRUM)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results


@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def rabi(image):
    client = QubitScopeClient(url=API_URL, api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray], task_type=TaskName.RABICOS)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def ramsey(image):
    client = QubitScopeClient(url=API_URL, api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray], task_type=TaskName.RAMSEY)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def t1fit(image):
    client = QubitScopeClient(url=API_URL, api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray], task_type=TaskName.T1FIT)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def t2fit(image):
    client = QubitScopeClient(url=API_URL, api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray], task_type=TaskName.T2FIT)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def optpipulse(image):
    client = QubitScopeClient(url=API_URL, api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray], task_type=TaskName.OPTPIPULSE)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def spectrum(image):
    client = QubitScopeClient(url=API_URL,api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray],task_type=TaskName.SPECTRUM)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def powershift(image):
    client = QubitScopeClient(url=API_URL,api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray],task_type=TaskName.POWERSHIFT)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def s21vsflux(image):
    client = QubitScopeClient(url=API_URL,api_key=API_KEY)
    data_ndarray = image
    response = client.request(file_list=[data_ndarray],task_type=TaskName.S21VFLUX)
    results = client.get_result(response=response)
    logging.debug(f"results:{results}")
    return results
