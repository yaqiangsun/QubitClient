# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/01/29 16:46:09
########################################################################

"""
提供了用于捕获和处理函数异常的装饰器以及API调用控制装饰器
"""

import functools
import logging
import traceback

def handle_exceptions(func):
    """
    装饰器函数，为被装饰的函数添加try-except异常处理
    
    Args:
        func: 被装饰的函数
        
    Returns:
        wrapper: 添加了异常处理的包装函数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 记录错误消息
            logging.error(f"Error occurred in {func.__name__}: {str(e)}")
            # 打印完整的错误堆栈跟踪
            logging.error(f"Exception traceback:\n{traceback.format_exc()}")
            # 返回None或者可以根据需要返回默认值
            return None
    return wrapper


def control_api_execution(enable_api):
    """
    装饰器工厂函数，根据配置模块中的ENABLE_API变量决定是否执行函数
    
    Args:
        enable_api: 是否启用API
        
    Returns:
        decorator: 根据ENABLE_API控制函数执行的装饰器
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 检查是否启用API
            if enable_api:
                # 如果启用了API，则执行原函数
                return func(*args, **kwargs)
            else:
                # 如果禁用了API，则不执行函数，返回None或默认值
                logging.info(f"{func.__name__} execution skipped due to ENABLE_API setting.")
                return None
        return wrapper
    return decorator