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
        confidence_list = result['confidence_list']

        curve_type = result['curve_type']

        params_list = np.array(params_list)
        linepoints_list = np.array(linepoints_list)
        confidence_list = np.array(confidence_list)
        mask = confidence_list >= threshold
        filtered_params_list = params_list[mask].tolist()
        filtered_linepoints_list = linepoints_list[mask].tolist()
        filtered_confidence_list = confidence_list[mask].tolist()


        result_filtered['params_list'] = filtered_params_list
        result_filtered['linepoints_list'] = filtered_linepoints_list
        result_filtered['confidence_list'] = filtered_confidence_list

        result_filtered['curve_type'] = curve_type

        results_filtered.append(result_filtered)

    return results_filtered

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
        class_ids = result['class_ids']
        curve_type = result['curve_type']

        params_list = np.array(params_list)
        linepoints_list = np.array(linepoints_list)
        confidence_list = np.array(confidence_list)
        class_ids = np.array(class_ids)
        curve_type = np.array(curve_type)

        mask = confidence_list >= threshold
        filtered_params_list = params_list[mask].tolist()
        filtered_linepoints_list = linepoints_list[mask].tolist()
        filtered_confidence_list = confidence_list[mask].tolist()
        filtered_class_ids = class_ids[mask].tolist()
        filtered_curve_type = curve_type[mask].tolist()


        result_filtered['params_list'] = filtered_params_list
        result_filtered['linepoints_list'] = filtered_linepoints_list
        result_filtered['confidence_list'] = filtered_confidence_list
        result_filtered['class_ids'] = filtered_class_ids
        result_filtered['curve_type'] = filtered_curve_type

        results_filtered.append(result_filtered)

    return results_filtered


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

    return results_filtered

    


TASK_MAP: Dict[str, Callable] = {
    'spectrum2dnnscope': postprocess_result_spectrum2dnnscope,
    's21vfluxnnscope': postprocess_result_s21vfluxnnscope,
    'powershiftnnscope': postprocess_result_powershiftnnscope
}

def run_postprocess(response, threshold, task_type):
    task_func = TASK_MAP.get(task_type)
    if not task_func:
        raise ValueError(f"未知的任务类型: {task_type}")
    return task_func(response, threshold)
