import logging
import numpy as np
from typing import Dict, Callable

def postprocess_result_s21vfluxscope(response ,threshold):
    logging.debug("Result: %s", response.parsed)
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

    logging.debug("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []
    for idx, result in enumerate(results):
        result_filtered = {}
        peaks_list = result['peaks']
        confs_list = result['confs']
        freqs_list = result['freqs_list']
        status = result['status']
        peaks_list_filtered = []
        confs_list_filtered = []
        freqs_list_filtered = []

        for i in range(len(peaks_list)):
            peaks = np.array(peaks_list[i])
            confs = np.array(confs_list[i])
            freqs = np.array(freqs_list[i])

            mask = confs >= threshold
            filtered_peaks = peaks[mask].tolist()
            filtered_confs = confs[mask].tolist()
            filtered_freqs = freqs[mask].tolist()

            peaks_list_filtered.append(filtered_peaks)
            confs_list_filtered.append(filtered_confs)
            freqs_list_filtered.append(filtered_freqs)

        result_filtered['peaks'] = peaks_list_filtered
        result_filtered['confs'] = confs_list_filtered
        result_filtered['freqs_list'] = freqs_list_filtered

        result_filtered['status'] = status
        results_filtered.append(result_filtered)
    response_data ={}
    response_data['results'] = results_filtered
    return response_data

def postprocess_result_s21peakmulti(response ,threshold):
    return postprocess_result_s21peak(response, threshold)

def postprocess_result_spectrum2dscope(response, threshold):
    logging.debug("Result: %s", response.parsed)
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
    logging.debug("Result: %s", response.parsed)
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

        # 逐个量子比特（或通道）处理，保持原始顺序和长度
        for i in range(len(peaks_list)):
            peaks = np.array(peaks_list[i]) if peaks_list[i] else np.array([])
            confs = np.array(confs_list[i]) if confs_list[i] else np.array([])

            # 如果原始数据为空，或者所有置信度都低于阈值 → 置为空列表
            if len(confs) == 0 or np.all(confs < threshold):
                peaks_list_filtered.append([])
                confs_list_filtered.append([])
            else:
                # 存在至少一个合格的峰 → 保留过滤后的结果
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
    logging.debug("Result: %s", response.parsed)
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

        # 逐个量子比特（或通道）处理，保持原始顺序和长度
        for i in range(len(params_list)):
            params = np.array(params_list[i]) if params_list[i] else np.array([])
            confs  = np.array(confs_list[i])  if confs_list[i]  else np.array([])

            # 若无数据 或 所有置信度都低于阈值 → 置为空列表
            if len(confs) == 0 or np.all(confs < threshold):
                params_list_filtered.append([])
                confs_list_filtered.append([])
            else:
                # 存在至少一个合格的峰 → 保留过滤后的结果
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
    logging.debug("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []

    for item in results:
        result_filtered = {}
        params_list         = item.get('params_list', [])
        r2_list             = item.get('r2_list', [])
        fit_data_list       = item.get('fit_data_list', [])
        fit_data_dense_list = item.get('fit_data_dense_list', [])  
        x_dense_list        = item.get('x_dense_list', [])         
        status = item.get('status', 'failed')

        filtered_params = []
        filtered_r2 = []
        filtered_fit_data = []
        filtered_fit_data_dense = []   
        filtered_x_dense = []          

        for params, r2, fit_data, fit_data_dense, x_dense in zip(
            params_list, r2_list, fit_data_list, fit_data_dense_list, x_dense_list
        ):
            if r2 >= threshold:
                filtered_params.append(params)
                filtered_r2.append(r2)
                filtered_fit_data.append(fit_data)
                filtered_fit_data_dense.append(fit_data_dense)
                filtered_x_dense.append(x_dense)
            else:
                filtered_params.append([])
                filtered_r2.append([])
                filtered_fit_data.append([])
                filtered_fit_data_dense.append([])
                filtered_x_dense.append([])

        result_filtered['params_list']         = filtered_params
        result_filtered['r2_list']             = filtered_r2
        result_filtered['fit_data_list']       = filtered_fit_data
        result_filtered['fit_data_dense_list'] = filtered_fit_data_dense   
        result_filtered['x_dense_list']        = filtered_x_dense         
        result_filtered['status'] = status if any(filtered_params) else 'failed'
        results_filtered.append(result_filtered)

    response_data = {}
    response_data['results'] = results_filtered
    return response_data


def postprocess_result_t2fit(response, threshold):
    logging.debug("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []

    for item in results:
        result_filtered = {}
        params_list         = item.get('params_list', [])
        r2_list             = item.get('r2_list', [])
        fit_data_list       = item.get('fit_data_list', [])
        fit_data_dense_list = item.get('fit_data_dense_list', [])  
        x_dense_list        = item.get('x_dense_list', [])         
        status = item.get('status', 'failed')

        filtered_params = []
        filtered_r2 = []
        filtered_fit_data = []
        filtered_fit_data_dense = []   
        filtered_x_dense = []          

        for params, r2, fit_data, fit_data_dense, x_dense in zip(
            params_list, r2_list, fit_data_list, fit_data_dense_list, x_dense_list
        ):
            if r2 >= threshold:
                filtered_params.append(params)
                filtered_r2.append(r2)
                filtered_fit_data.append(fit_data)
                filtered_fit_data_dense.append(fit_data_dense)     
                filtered_x_dense.append(x_dense)                   
            else:
                filtered_params.append([])
                filtered_r2.append([])
                filtered_fit_data.append([])
                filtered_fit_data_dense.append([])
                filtered_x_dense.append([])

        result_filtered['params_list']         = filtered_params
        result_filtered['r2_list']             = filtered_r2
        result_filtered['fit_data_list']       = filtered_fit_data
        result_filtered['fit_data_dense_list'] = filtered_fit_data_dense   
        result_filtered['x_dense_list']        = filtered_x_dense         
        result_filtered['status'] = status if any(filtered_params) else 'failed'
        results_filtered.append(result_filtered)

    response_data = {}
    response_data['results'] = results_filtered
    return response_data

def postprocess_result_ramsey(response, threshold):
    """
    对 RAMSEY 结果按 R² 拟合优度进行过滤
    threshold: R² 阈值（如 0.8），低于此值的量子比特拟合结果将被过滤掉
    """
    logging.debug("Result: %s", response.parsed)
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

def postprocess_result_drag(response, threshold):
    logging.debug("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []
    for idx, result in enumerate(results):
        result_filtered = {}
        x_pred_list = result['x_pred_list']
        y0_pred_list = result['y0_pred_list']
        y1_pred_list = result['y1_pred_list']
        intersections_list = result['intersections_list']
        intersections_confs_list = result['intersections_confs_list']
        status = result['status']

        intersections_list_filtered = []
        intersections_confs_list_filtered = []

        for i in range(len(intersections_confs_list)):
            intersections = np.array(intersections_list[i])
            intersections_confs = np.array(intersections_confs_list[i])

            mask = intersections_confs >= threshold

            filtered_intersections = intersections[mask].tolist()
            filtered_intersections_confs = intersections_confs[mask].tolist()


            intersections_list_filtered.append(filtered_intersections)
            intersections_confs_list_filtered.append(filtered_intersections_confs)


        result_filtered['x_pred_list'] = x_pred_list
        result_filtered['y0_pred_list'] = y0_pred_list
        result_filtered['y1_pred_list'] = y1_pred_list

        result_filtered['intersections_list'] = intersections_list_filtered
        result_filtered['intersections_confs_list'] = intersections_confs_list_filtered
        result_filtered['status'] = status
        results_filtered.append(result_filtered)
    response_data = {}
    response_data['results'] = results_filtered
    return response_data

def postprocess_result_singleshot(response, threshold):
    logging.debug("Result: %s", response.parsed)
    result = response.parsed

    return result
def postprocess_result_spectrum(response, threshold):
    logging.debug("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []
    for idx, result in enumerate(results):
        filtered_item = {}
        peaks_list = result.get('peaks_list', [])
        confidences_list = result.get('confidences_list', [])
        mean_cut_widths_list = result.get('mean_cut_widths_list', [])
        filtered_peaks = []
        filtered_confidences = []
        filtered_mean_cut_widths = []
        # 遍历每一组数据（处理二维列表结构）
        for idx, (peaks, confs, widths) in enumerate(zip(peaks_list, confidences_list, mean_cut_widths_list)):
            try:
                # 将置信度转为浮点型数组，用于阈值判断
                confs_arr = np.array(confs, dtype=float)
                # 生成过滤掩码：置信度≥阈值的位置保留
                mask = confs_arr >= threshold
            except (ValueError, TypeError):
                # 置信度无法转为数值时，保留所有数据
                mask = np.ones(len(confs), dtype=bool) if confs else []
            
            # 按掩码过滤当前组的所有字段
            # 处理空列表情况，避免索引错误
            if peaks and mask.size > 0:
                filtered_peak = np.array(peaks, dtype=object)[mask].tolist()
            else:
                filtered_peak = []
                
            if confs and mask.size > 0:
                filtered_conf = confs_arr[mask].tolist() if isinstance(confs_arr, np.ndarray) else confs
            else:
                filtered_conf = []
                
            if widths and mask.size > 0:
                filtered_width = np.array(widths, dtype=object)[mask].tolist()
            else:
                filtered_width = []
            
            filtered_peaks.append(filtered_peak)
            filtered_confidences.append(filtered_conf)
            filtered_mean_cut_widths.append(filtered_width)
        
        # 组装过滤后的结果
        filtered_item['peaks_list'] = filtered_peaks
        filtered_item['confidences_list'] = filtered_confidences
        filtered_item['mean_cut_widths_list'] = filtered_mean_cut_widths
        
        results_filtered.append(filtered_item)
    final_response = {}
    final_response['results'] = results_filtered
    return final_response


def postprocess_result_powershift(response, threshold):
    logging.debug("Result: %s", response.parsed)
    result = response.parsed
    results = result.get("results")
    results_filtered = []
    for idx, result in enumerate(results):
        result_filtered = {}
        q_list = result.get('q_list', [])
        keypoints_list = result.get('keypoints_list', [])
        confs = result.get('confs', [])
        class_num_list = result.get('class_num_list', [])

        keypoints_arr = np.array(keypoints_list, dtype=object)
        class_arr = np.array(class_num_list, dtype=object)
        try:
            confs_arr = np.array(confs, dtype=float)
        except Exception:
            confs_arr = np.array(confs, dtype=object)
        q_arr = np.array(q_list, dtype=object)
        if confs_arr.size > 0 and np.issubdtype(confs_arr.dtype, np.number):
            mask = confs_arr >= threshold
        else:
            mask = np.ones(keypoints_arr.shape, dtype=bool)

        filtered_q = q_arr[mask].tolist() if q_arr.size > 0 else []
        filtered_keypoints = keypoints_arr[mask].tolist() if keypoints_arr.size > 0 else []
        filtered_class = class_arr[mask].tolist() if class_arr.size > 0 else []
        filtered_confs = confs_arr[mask].tolist() if confs_arr.size > 0 and np.issubdtype(confs_arr.dtype, np.number) else []

        result_filtered['q_list'] = filtered_q
        result_filtered['keypoints_list'] = filtered_keypoints
        result_filtered['confs'] = filtered_confs
        result_filtered['class_num_list'] = filtered_class

        results_filtered.append(result_filtered)
    response_data ={}
    response_data['results'] = results_filtered
    return response_data

def postprocess_result_rb(response, threshold):
    result = response.parsed
    results = result.get("results", [])
    results_filtered = []

    for item in results:
        result_filtered = {}
        params_list         = item.get('params_list', [])
        r2_list             = item.get('r2_list', [])
        fit_data_list       = item.get('fit_data_list', [])          
        fit_data_dense_list = item.get('fit_data_dense_list', [])   
        fit_x_dense_list    = item.get('x_dense_list', [])          
        status              = item.get('status', 'failed')

        filtered_params         = []
        filtered_r2             = []
        filtered_fit_data       = []
        filtered_fit_data_dense = []
        filtered_x_dense        = []

        for params, r2, fit_data, fit_data_dense, x_dense in zip(
            params_list,
            r2_list,
            fit_data_list,
            fit_data_dense_list,
            fit_x_dense_list
        ):
            if r2 >= threshold:
                filtered_params.append(params)
                filtered_r2.append(r2)
                filtered_fit_data.append(fit_data)
                filtered_fit_data_dense.append(fit_data_dense)
                filtered_x_dense.append(x_dense)
            else:
                filtered_params.append([])
                filtered_r2.append([])           
                filtered_fit_data.append([])
                filtered_fit_data_dense.append([])
                filtered_x_dense.append([])

        result_filtered['params_list']         = filtered_params
        result_filtered['r2_list']             = filtered_r2
        result_filtered['fit_data_list']       = filtered_fit_data
        result_filtered['fit_data_dense_list'] = filtered_fit_data_dense
        result_filtered['x_dense_list']        = filtered_x_dense
        result_filtered['status'] = status if any(filtered_params) else 'failed'

        results_filtered.append(result_filtered)

    response_data = {}
    response_data['results'] = results_filtered
    return response_data

TASK_MAP: Dict[str, Callable] = {
    's21peak': postprocess_result_s21peak,
    's21peakmulti': postprocess_result_s21peak,
    's21vfluxscope': postprocess_result_s21vfluxscope,
    'spectrum2dscope': postprocess_result_spectrum2dscope,
    # 'spectrum2dnnscope': postprocess_result_spectrum2dnnscope
    'rabicos': postprocess_result_rabicos,
    'optpipulse': postprocess_result_optpipulse,
    't1fit': postprocess_result_t1fit,
    't2fit': postprocess_result_t2fit,
    'ramsey': postprocess_result_ramsey,
    'drag': postprocess_result_drag,
    'singleshot': postprocess_result_singleshot,
    'spectrum': postprocess_result_spectrum,
    'powershift': postprocess_result_powershift,
    'rb': postprocess_result_rb
    
}

def run_postprocess(response, threshold, task_type):
    task_func = TASK_MAP.get(task_type)
    if not task_func:
        raise ValueError(f"未知的任务类型: {task_type}")
    return task_func(response, threshold)
