# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/06 18:11:37
########################################################################

import numpy as np

from .task import run_task
import numpy as np


class QubitCtrlClient(object):
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    def run(self,task_type:str="s21peak",*args,**kwargs):
        return run_task(task_type,*args,**kwargs)
