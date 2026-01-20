# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/04/15 10:23:27
########################################################################

import math


def parser_result(result, images):
    import cv2
    result_images = []
    for i in range(len(result)):
        image = images[i]
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        # input_image_reshape = (512, 512)
        input_image_reshape = (image.shape[1]*10,image.shape[0])
        image = cv2.resize(image, input_image_reshape, interpolation=cv2.INTER_NEAREST)
        
        
        image_result = result[i]
        linepoints_list = image_result["linepoints_list"]
        for linepoints in linepoints_list:
            for j in range(len(linepoints) - 1):
                cv2.line(image, tuple([int(linepoints[j][0]*10),int(linepoints[j][1])]), tuple([int(linepoints[j + 1][0]*10),int(linepoints[j + 1][1])]), (0, 255, 0), 2)
        
        result_images.append(image)
    return result_images

def convet_axis(points,x_dim,y_dim):
    reflection_points = []
    for point in points:
        x = point[0]
        y = point[1]

        x_grid_start = x_dim[int(x)]
        x_grid_end = x_dim[min(int(x)+1,len(x_dim)-1)]
        x_refletion = (x_grid_end-x_grid_start)* math.modf(x)[0] + x_grid_start

        
        # y_index = min(max(0,int(y)),len(y_dim)-2)
        y_index = int(y)
        if y_index<0 or y_index>len(y_dim)-2:
            continue
        y_grid_start = y_dim[y_index]
        y_grid_end = y_dim[y_index+1]
        y_refletion = (y_grid_end-y_grid_start)* math.modf(y)[0] + y_grid_start
        reflection_points.append([x_refletion,y_refletion])
        pass
        
    return reflection_points