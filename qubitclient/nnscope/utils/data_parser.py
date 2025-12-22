# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/04/11 17:58:29
########################################################################

import os
import numpy as np



def load_npz_file(file_path):
    with np.load(file_path, allow_pickle=True) as data:
        content = dict(data)
    return content
def convert_data_to_image(npz_content):
    import cv2
    content = npz_content
    iq_avg = content["iq_avg"]
    rows, cols = iq_avg.shape
    if rows < cols:
        iq_avg = iq_avg.T
    iq_avg = np.abs(iq_avg)
    iq_avg_normalized = cv2.normalize(iq_avg, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return iq_avg_normalized

def load_npz_to_image(file_path):
    npz_content = load_npz_file(file_path)
    image = convert_data_to_image(npz_content)
    return image

def load_npz_to_images(file_path_list):
    images = []
    for file_path in file_path_list:
        print(file_path)
        image = load_npz_to_image(file_path)
        images.append(image)
    return images