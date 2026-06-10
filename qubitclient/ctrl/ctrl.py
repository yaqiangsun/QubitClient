# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/06 18:11:37
########################################################################


from .task import run_task
from .task import call_mcp


class QubitCtrlClient(object):
    def __init__(self,*args,**kwargs):
        pass

    def run(self,task_type:str="s21peak",*args,**kwargs):
        return run_task(task_type,*args,**kwargs)

    def query_param(self, *args, **kwargs):
        result = call_mcp("query_param",*args,**kwargs)
        return result
    def update_param(self, *args, **kwargs):
        result = call_mcp("update_param",*args,**kwargs)
        return result
    def get_data(rid, *args, **kwargs):
        result = call_mcp("get_data",
                        rid=rid
                        )
        return result