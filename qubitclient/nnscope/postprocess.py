import logging
import numpy as np
from typing import Dict, Callable



def postprocess_result_spectrum2dnnscope(response, threshold):
    logging.debug("Result: %s", response.json())
    result = response.json()
    results = result["result"]

    results_filtered = []
    for idx, result in enumerate(results):
        result_filtered = {}
        params_list = result['params_list']
        linepoints_list = result['linepoints_list']
        confidence_list = result['confidences_list']

        class_ids_list = result['class_ids_list']
        curve_type_list = result['curve_type_list']

        status = result['status']

        params_list_filtered = []
        linepoints_list_filtered = []
        confidence_list_filtered = []
        class_ids_list_filtered = []
        curve_type_list_filtered = []

        for i in range(len(confidence_list)):
            params = np.array(params_list[i])
            linepoints = np.array(linepoints_list[i])
            confidence = np.array(confidence_list[i])
            class_ids = np.array(class_ids_list[i])
            if curve_type_list[i] == None:
                curve_type_list[i] = []
            curve_type = np.array(curve_type_list[i])
            # if curve_type==None:
            #     curve_type=[]
            # if isinstance(curve_type, np.ndarray) and curve_type.ndim == 0:
            #     curve_type = np.array([curve_type.item()])

            mask = confidence >= threshold
            filtered_params = params[mask].tolist()
            filtered_linepoints = linepoints[mask].tolist()
            filtered_confidence = confidence[mask].tolist()
            filtered_class_ids = class_ids[mask].tolist()
            filtered_curve_type = curve_type[mask].tolist()
            params_list_filtered.append(filtered_params)
            linepoints_list_filtered.append(filtered_linepoints)
            confidence_list_filtered.append(filtered_confidence)
            class_ids_list_filtered.append(filtered_class_ids)
            curve_type_list_filtered.append(filtered_curve_type)

        result_filtered['params_list'] = params_list_filtered
        result_filtered['linepoints_list'] = linepoints_list_filtered
        result_filtered['confidences_list'] = confidence_list_filtered
        result_filtered['class_ids_list'] = class_ids_list_filtered
        result_filtered['curve_type_list'] = curve_type_list_filtered
        result_filtered['status'] = status

        results_filtered.append(result_filtered)
    response_data = {}
    response_data['result'] = results_filtered
    return response_data


def postprocess_result_s21vfluxnnscope(response, threshold):
    logging.debug("Result: %s", response.json())
    result = response.json()
    results = result["result"]

    results_filtered = []
    for idx, result in enumerate(results):
        result_filtered = {}
        params_list = result['params_list']
        linepoints_list = result['linepoints_list']
        confidence_list = result['confidence_list']

        class_ids_list = result['class_ids']
        curve_type_list = result['curve_type']

        status = result['status']



        params_list_filtered = []
        linepoints_list_filtered = []
        confidence_list_filtered = []
        class_ids_list_filtered = []
        curve_type_list_filtered = []

        for i in range(len(confidence_list)):
            params = np.array(params_list[i])
            linepoints = np.array(linepoints_list[i])
            confidence = np.array(confidence_list[i])
            class_ids = np.array(class_ids_list[i])
            if curve_type_list[i] == None:
                curve_type_list[i] = []
            curve_type = np.array(curve_type_list[i])
            # if curve_type==None:
            #     curve_type=[]
            # if isinstance(curve_type, np.ndarray) and curve_type.ndim == 0:
            #     curve_type = np.array([curve_type.item()])




            mask = confidence >= threshold
            filtered_params = params[mask].tolist()
            filtered_linepoints = linepoints[mask].tolist()
            filtered_confidence = confidence[mask].tolist()
            filtered_class_ids = class_ids[mask].tolist()
            filtered_curve_type = curve_type[mask].tolist()
            params_list_filtered.append(filtered_params)
            linepoints_list_filtered.append(filtered_linepoints)
            confidence_list_filtered.append(filtered_confidence)
            class_ids_list_filtered.append(filtered_class_ids)
            curve_type_list_filtered.append(filtered_curve_type)

        result_filtered['params_list'] = params_list_filtered
        result_filtered['linepoints_list'] = linepoints_list_filtered
        result_filtered['confidence_list'] = confidence_list_filtered
        result_filtered['class_ids'] = class_ids_list_filtered
        result_filtered['curve_type'] = curve_type_list_filtered
        result_filtered['status'] = status

        results_filtered.append(result_filtered)
    response_data = {}
    response_data['result'] = results_filtered
    return response_data


def postprocess_result_powershiftnnscope(response, threshold):
    logging.debug("Result: %s", response.json())
    result = response.json()
    results = result.get("result", [])

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



def postprocess_result_spectrumnnscope(response, threshold):
    logging.debug("before filter: Result: %s", response.json())
    result = response.json()

    results = result.get("result", [])

    results_filtered = []
    for res in results:
        result_filtered = {}

        peaks_list = res.get('peaks_list', [])
        confidences_list = res.get('confidences_list', [])
        peak_start = res.get('peak_start', [])
        peak_end = res.get('peak_end', [])

        filtered_peaks = []
        filtered_confidences = []
        filtered_peak_start = []
        filtered_peak_end = []

        # 遍历每一条曲线（保留[]位置）
        for wave_idx in range(len(confidences_list)):
            wave_peaks = peaks_list[wave_idx] if wave_idx < len(peaks_list) else []
            wave_confs = confidences_list[wave_idx] if wave_idx < len(confidences_list) else []
            wave_starts = peak_start[wave_idx] if wave_idx < len(peak_start) else []
            wave_ends = peak_end[wave_idx] if wave_idx < len(peak_end) else []

            curr_peaks = []
            curr_confs = []
            curr_starts = []
            curr_ends = []

            # 遍历
            for peak_idx, conf in enumerate(wave_confs):
                if isinstance(conf, (int, float)) and conf >= threshold:
                    if peak_idx < len(wave_peaks):
                        curr_peaks.append(wave_peaks[peak_idx])
                    if peak_idx < len(wave_starts):
                        curr_starts.append(wave_starts[peak_idx])
                    if peak_idx < len(wave_ends):
                        curr_ends.append(wave_ends[peak_idx])
                    curr_confs.append(conf)

            # 无论是否为空，都追加到结果
            filtered_peaks.append(curr_peaks)
            filtered_confidences.append(curr_confs)
            filtered_peak_start.append(curr_starts)
            filtered_peak_end.append(curr_ends)

        # 组装
        result_filtered['peaks_list'] = filtered_peaks
        result_filtered['confidences_list'] = filtered_confidences
        result_filtered['peak_start'] = filtered_peak_start
        result_filtered['peak_end'] = filtered_peak_end
        result_filtered['status'] = 'success'

        results_filtered.append(result_filtered)
    response_data = {'results': results_filtered}
    return response_data


def postprocess_result_s21peaknnscope(response ,threshold):
    # result = response.parsed
    result = response.json()

    results = result.get("result")
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


TASK_MAP: Dict[str, Callable] = {
    'spectrum2dnnscope': postprocess_result_spectrum2dnnscope,
    's21vfluxnnscope': postprocess_result_s21vfluxnnscope,
    'powershiftnnscope': postprocess_result_powershiftnnscope,
    'spectrumnnscope': postprocess_result_spectrumnnscope,
    's21peaknnscope': postprocess_result_s21peaknnscope
}

def run_postprocess(response, threshold, task_type):
    task_func = TASK_MAP.get(task_type)
    if not task_func:
        raise ValueError(f"未知的任务类型: {task_type}")
    return task_func(response, threshold)
