# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/01/27 17:48:06
########################################################################

from qubitclient import QubitNNScopeClient,QubitScopeClient
from qubitclient import NNTaskName,TaskName
import logging
from qubitclient import handle_exceptions, control_api_execution


from .format import s21_convert,s21vsflux_convert,  ramseyt2_convert, t12dfit_convert, nnspectrum2d_convert, spectrum2d_convert,\
                    singleshot_convert, setpialpha_convert,\
                    nns21vsflux_convert,t1fit_convert,\
                    t2fit_convert,nnspectrum_convert,\
                    spectrum_convert, powershift_convert, s21peakmulti_convert,rb_convert,rabicos_convert, xeb_convert,optreadfreq_convert,\
                    spinecho_convert, timingxyz_convert
ENABLE_API=True
def nnscope_template(image,task_type=NNTaskName.SPECTRUM2D):
    client = QubitNNScopeClient()
    data_ndarray = image
    response = client.request(file_list=[data_ndarray],task_type=task_type)
    # results = client.get_result(response=response)
    threshold = 0.3
    results = client.get_filtered_result(response, threshold, task_type = task_type.value)

    logging.debug(f"results:{results}")
    return results

def scope_template(image, task_type=TaskName.SPECTRUM2D, threshold=0.1):
    client = QubitScopeClient()
    data_ndarray = image
    response = client.request(file_list=[data_ndarray], task_type=task_type)
    # results = client.get_result(response=response)
    results = client.get_filtered_result(response, threshold, task_type=task_type.value)
    logging.debug(f"results:{results}")
    return results

####################################################################################

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nnspectrum2d(image):
    image = nnspectrum2d_convert(image)
    results = nnscope_template(image,task_type=NNTaskName.SPECTRUM2D)
    return results

def spectrum2d(image):
    image = spectrum2d_convert(image)
    results = scope_template(image,task_type=TaskName.SPECTRUM2D)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nnpowershift(image):
    image = powershift_convert(image)
    results = nnscope_template(image,task_type=NNTaskName.POWERSHIFT)
    return results
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nnspectrum(image):
    image = nnspectrum_convert(image)
    results = nnscope_template(image,task_type=NNTaskName.SPECTRUM)
    return results


####################################################################################
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nns21(image):
    image = s21_convert(image)
    results = nnscope_template(image,task_type=NNTaskName.S21PEAK)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def s21(image):
    image = s21_convert(image)
    results = scope_template(image,task_type=TaskName.S21PEAK)
    return results
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def s21peakmulti(image):
    image = s21peakmulti_convert(image)
    results = scope_template(image,task_type=TaskName.S21PEAKMULTI)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def nns21peakmulti(image):
    image = s21peakmulti_convert(image)
    results = nnscope_template(image,task_type=NNTaskName.S21PEAKMULTI)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def rabi(image):
    image = rabicos_convert(image)
    results = scope_template(image,task_type=TaskName.RABICOS)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def ramsey(image):
    image = t2fit_convert(image) # ramsey is the same as t2fit
    results = scope_template(image,task_type=TaskName.RAMSEY)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def ramseyt2(image):
    image = ramseyt2_convert(image)
    results = scope_template(image,task_type=TaskName.RAMSEY)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def t1fit(image):
    image = t1fit_convert(image)
    results = scope_template(image,task_type=TaskName.T1FIT)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def t12dfit(image):
    image = t12dfit_convert(image)
    results = scope_template(image,task_type=TaskName.T12DFIT)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def t2fit(image):
    image = t2fit_convert(image)
    results = scope_template(image,task_type=TaskName.T2FIT)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def setpialpha(image):
    image = setpialpha_convert(image)
    results = scope_template(image,task_type=TaskName.SETPIALPHA)
    return results

# @control_api_execution(enable_api=ENABLE_API)
# @handle_exceptions
# def delta(image):
#     image = delta_convert(image)
#     results = scope_template(image,task_type=TaskName.OPTPIPULSE)
#     return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def spectrum(image):
    image = spectrum_convert(image)
    results = scope_template(image,task_type=TaskName.SPECTRUM)
    return results
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def powershift(image):
    image = powershift_convert(image)
    results = scope_template(image,task_type=TaskName.POWERSHIFT)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def s21vsflux(image):
    image = s21vsflux_convert(image)
    results = scope_template(image,task_type=TaskName.S21VSFLUX)
    return results
def nns21vsflux(image):
    image = nns21vsflux_convert(image)
    results = nnscope_template(image,task_type=NNTaskName.S21VSFLUX)
    return results

# @control_api_execution(enable_api=ENABLE_API)
# @handle_exceptions
# def allxy_drag(image):
#     image = drag_convert(image)
#     results = scope_template(image,task_type=TaskName.DRAG)
#     return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def singleshot(image):
    image = singleshot_convert(image)
    results = scope_template(image,task_type=TaskName.SINGLESHOT)
    return results


@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def rb(image):
    image = rb_convert(image)
    results = scope_template(image,task_type=TaskName.RB)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def xeb(image):
    image = xeb_convert(image)
    results = scope_template(image,task_type=TaskName.XEB)
    return results
@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def optreadfreq(image):
    image = optreadfreq_convert(image)
    results = scope_template(image,task_type=TaskName.OPTREADFREQ)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def spinecho(image):
    image = spinecho_convert(image)
    results = scope_template(image, task_type=TaskName.SPINECHO, threshold=-1)
    return results

@control_api_execution(enable_api=ENABLE_API)
@handle_exceptions
def timingxyz(image):
    image = timingxyz_convert(image)
    results = scope_template(image, task_type=TaskName.TIMINGXYZ, threshold=-1)
    return results