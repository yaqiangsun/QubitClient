import logging
import numpy as np
from typing import Dict, Callable

def postprocess_result_s21vflux(response ,threshold):
    logging.info("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []
    for idx, result in enumerate(results):
        result_filtered = {}
        coscurves_list = result['coscurves_list']
        cosconfs_list = result['cosconfs_list']
        lines_list = result['lines_list']
        lineconfs_list = result['lineconfs_list']
        status = result['status']
        coscurves_list_filtered = []
        cosconfs_list_filtered = []
        lines_list_filtered = []
        lineconfs_list_filtered = []

        for i in range(len(cosconfs_list)):
            coscurves = np.array(coscurves_list[i])
            cosconfs = np.array(cosconfs_list[i])
            mask = cosconfs >= threshold
            filtered_coscurves = coscurves[mask].tolist()
            filtered_cosconfs = cosconfs[mask].tolist()
            coscurves_list_filtered.append(filtered_coscurves)
            cosconfs_list_filtered.append(filtered_cosconfs)
        for i in range(len(cosconfs_list)):
            lines = np.array(lines_list[i])
            lineconfs = np.array(lineconfs_list[i])
            mask = lineconfs >= threshold
            filtered_lines = lines[mask].tolist()
            filtered_lineconfs = lineconfs[mask].tolist()
            lines_list_filtered.append(filtered_lines)
            lineconfs_list_filtered.append(filtered_lineconfs)
        result_filtered['coscurves_list'] = coscurves_list_filtered
        result_filtered['cosconfs_list'] = cosconfs_list_filtered
        result_filtered['lines_list'] = lines_list_filtered
        result_filtered['lineconfs_list'] = lineconfs_list_filtered
        result_filtered['status'] = status
        results_filtered.append(result_filtered)
    response_data ={}
    response_data['results'] = results_filtered
    return response_data

def postprocess_result_s21peak(response ,threshold):

    logging.info("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []
    for idx, result in enumerate(results):
        result_filtered = {}
        peaks_list = result['peaks']
        confs_list = result['confs']
        status = result['status']
        peaks_list_filtered = []
        confs_list_filtered = []
        for i in range(len(peaks_list)):
            peaks = np.array(peaks_list[i])
            confs = np.array(confs_list[i])
            mask = confs >= threshold
            filtered_peaks = peaks[mask].tolist()
            filtered_confs = confs[mask].tolist()
            peaks_list_filtered.append(filtered_peaks)
            confs_list_filtered.append(filtered_confs)
        result_filtered['peaks'] = peaks_list_filtered
        result_filtered['confs'] = confs_list_filtered
        result_filtered['status'] = status
        results_filtered.append(result_filtered)
    response_data ={}
    response_data['results'] = results_filtered
    return response_data



def postprocess_result_spectrum2dscope(response, threshold):
    logging.info("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []
    for idx, result in enumerate(results):
        result_filtered = {}
        coscurves_list = result['params']
        cosconfs_list = result['confs']
        coscompress_list = result['coscompress_list']

        lines_list = result['lines_list']
        lineconfs_list = result['lineconfs_list']
        status = result['status']
        coscurves_list_filtered = []
        cosconfs_list_filtered = []
        coscompress_list_filtered = []

        lines_list_filtered = []
        lineconfs_list_filtered = []

        for i in range(len(cosconfs_list)):
            coscurves = np.array(coscurves_list[i])
            cosconfs = np.array(cosconfs_list[i])
            coscompress = np.array(coscompress_list[i])

            mask = cosconfs >= threshold
            filtered_coscurves = coscurves[mask].tolist()
            filtered_cosconfs = cosconfs[mask].tolist()
            filtered_coscompress = coscompress[mask].tolist()

            coscurves_list_filtered.append(filtered_coscurves)
            cosconfs_list_filtered.append(filtered_cosconfs)
            coscompress_list_filtered.append(filtered_coscompress)

        for i in range(len(cosconfs_list)):
            lines = np.array(lines_list[i])
            lineconfs = np.array(lineconfs_list[i])
            mask = lineconfs >= threshold
            filtered_lines = lines[mask].tolist()
            filtered_lineconfs = lineconfs[mask].tolist()
            lines_list_filtered.append(filtered_lines)
            lineconfs_list_filtered.append(filtered_lineconfs)
        result_filtered['params'] = coscurves_list_filtered
        result_filtered['confs'] = cosconfs_list_filtered
        result_filtered['coscompress_list'] = coscompress_list_filtered

        result_filtered['lines_list'] = lines_list_filtered
        result_filtered['lineconfs_list'] = lineconfs_list_filtered
        result_filtered['status'] = status
        results_filtered.append(result_filtered)
    response_data = {}
    response_data['results'] = results_filtered
    return response_data

def postprocess_result_rabicos(response, threshold):
    logging.info("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []
    for idx, result_item in enumerate(results):
        result_filtered = {}
        peaks_list = result_item.get('peaks', [])
        confs_list = result_item.get('confs', [])
        status = result_item.get('status', 'failed')

        peaks_list_filtered = []
        confs_list_filtered = []

        for i in range(len(peaks_list)):
            peaks = np.array(peaks_list[i])
            confs = np.array(confs_list[i])
            mask = confs >= threshold
            filtered_peaks = peaks[mask].tolist()
            filtered_confs = confs[mask].tolist()
            peaks_list_filtered.append(filtered_peaks)
            confs_list_filtered.append(filtered_confs)

        result_filtered['peaks'] = peaks_list_filtered
        result_filtered['confs'] = confs_list_filtered
        result_filtered['status'] = status
        results_filtered.append(result_filtered)

    response_data = {}
    response_data['results'] = results_filtered
    return response_data

def postprocess_result_optpipulse(response, threshold):
    logging.info("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []
    for idx, result_item in enumerate(results):
        result_filtered = {}
        params_list = result_item.get('params', [])      
        confs_list  = result_item.get('confs', [])       
        status = result_item.get('status', 'failed')

        params_list_filtered = []
        confs_list_filtered  = []

        for i in range(len(params_list)):
            params = np.array(params_list[i])
            confs  = np.array(confs_list[i])
            mask = confs >= threshold
            filtered_params = params[mask].tolist()
            filtered_confs  = confs[mask].tolist()
            params_list_filtered.append(filtered_params)
            confs_list_filtered.append(filtered_confs)

        result_filtered['params'] = params_list_filtered
        result_filtered['confs']  = confs_list_filtered
        result_filtered['status']  = status
        results_filtered.append(result_filtered)

    response_data = {}
    response_data['results'] = results_filtered
    return response_data

def postprocess_result_t1fit(response, threshold):
    logging.info("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []

    for item in results:
        result_filtered = {}
        params_list = item.get('params_list', [])
        r2_list = item.get('r2_list', [])
        fit_data_list = item.get('fit_data_list', [])
        status = item.get('status', 'failed')

        filtered_params = []
        filtered_fit_data = []
        filtered_r2 = []

        for params, r2, fit_data in zip(params_list, r2_list, fit_data_list):
            if r2 >= threshold:
                filtered_params.append(params)
                filtered_fit_data.append(fit_data)
                filtered_r2.append(r2)

        result_filtered['params_list'] = filtered_params
        result_filtered['r2_list'] = filtered_r2
        result_filtered['fit_data_list'] = filtered_fit_data
        result_filtered['status'] = status if filtered_params else 'failed'
        results_filtered.append(result_filtered)

    response_data = {}
    response_data['results'] = results_filtered
    return response_data
def postprocess_result_t2fit(response, threshold):
    logging.info("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []

    for item in results:
        result_filtered = {}
        params_list = item.get('params_list', [])
        r2_list = item.get('r2_list', [])
        fit_data_list = item.get('fit_data_list', [])
        status = item.get('status', 'failed')

        filtered_params = []
        filtered_fit_data = []
        filtered_r2 = []

        for params, r2, fit_data in zip(params_list, r2_list, fit_data_list):
            if r2 >= threshold:
                filtered_params.append(params)
                filtered_fit_data.append(fit_data)
                filtered_r2.append(r2)

        result_filtered['params_list'] = filtered_params
        result_filtered['r2_list'] = filtered_r2
        result_filtered['fit_data_list'] = filtered_fit_data
        result_filtered['status'] = status if filtered_params else 'failed'
        results_filtered.append(result_filtered)

    response_data = {}
    response_data['results'] = results_filtered
    return response_data

def postprocess_result_ramsey(response, threshold):
    """
    对 RAMSEY 结果按 R² 拟合优度进行过滤
    threshold: R² 阈值（如 0.8），低于此值的量子比特拟合结果将被过滤掉
    """
    logging.info("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []

    for item in results:
        result_filtered = {}
        params_list = item.get('params_list', [])
        r2_list = item.get('r2_list', [])
        fit_data_list = item.get('fit_data_list', [])
        status = item.get('status', 'failed')

        filtered_params = []
        filtered_fit_data = []
        filtered_r2 = []

        for params, r2, fit_data in zip(params_list, r2_list, fit_data_list):
            if r2 >= threshold:
                filtered_params.append(params)
                filtered_fit_data.append(fit_data)
                filtered_r2.append(r2)

        result_filtered['params_list'] = filtered_params
        result_filtered['r2_list'] = filtered_r2
        result_filtered['fit_data_list'] = filtered_fit_data
        result_filtered['status'] = status if filtered_params else 'failed'
        results_filtered.append(result_filtered)

    response_data = {}
    response_data['results'] = results_filtered
    return response_data

TASK_MAP: Dict[str, Callable] = {
    's21peak': postprocess_result_s21peak,
    's21vflux': postprocess_result_s21vflux,
    'spectrum2dscope': postprocess_result_spectrum2dscope,
    # 'spectrum2dnnscope': postprocess_result_spectrum2dnnscope
    'rabicos': postprocess_result_rabicos,
    'optpipulse': postprocess_result_optpipulse,
    't1fit': postprocess_result_t1fit,
    't2fit': postprocess_result_t2fit,
    'ramsey': postprocess_result_ramsey,
}

def run_postprocess(response, threshold, task_type):
    task_func = TASK_MAP.get(task_type)
    if not task_func:
        raise ValueError(f"未知的任务类型: {task_type}")
    return task_func(response, threshold)
