# -*- coding: utf-8 -*-
# Copyright (c) 2025 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2025/12/06 
########################################################################

"""
配置加载模块
支持多种配置来源，优先级从低到高：
1. 项目默认 config.py（最低优先级）
2. 用户目录下的 qubitclient.json 文件
3. 环境变量
4. 运行目录下的 qubitclient.json 文件
5. 构造函数传递的参数（最高优先级）
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


def get_user_config_path() -> Path:
    """获取用户目录下的配置文件路径"""
    home = Path.home()
    return home / "qubitclient.json"


def get_runtime_config_path() -> Path:
    """获取运行目录下的配置文件路径"""
    return Path.cwd() / "qubitclient.json"


def load_json_config(config_path: Path) -> Dict[str, Any]:
    """从 JSON 文件加载配置"""
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load config from {config_path}: {e}")
            return {}
    return {}


def load_env_config() -> Dict[str, Any]:
    """从环境变量加载配置"""
    config = {}
    
    # 支持的环境变量
    url = os.environ.get('QUBITCLIENT_URL')
    api_key = os.environ.get('QUBITCLIENT_API_KEY')
    
    if url:
        config['url'] = url
    if api_key:
        config['api_key'] = api_key
    
    return config


def load_default_config() -> Dict[str, Any]:
    """
    加载默认配置（从项目 config.py 导入）
    如果存在的话
    """
    try:
        # 尝试从项目根目录导入 config
        from .. import config
        return {
            'url': getattr(config, 'API_URL', None),
            'api_key': getattr(config, 'API_KEY', None)
        }
    except (ImportError, AttributeError):
        return {}


def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并多个配置字典，后面的配置会覆盖前面的配置
    参数顺序应该是从低优先级到高优先级
    """
    result = {}
    for config in configs:
        # 只更新非 None 的值
        for key, value in config.items():
            if value is not None:
                result[key] = value
    return result


def get_config(url: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, str]:
    """
    获取最终配置，按照优先级合并所有配置源
    
    优先级从低到高：
    1. 默认 config.py
    2. 用户目录 qubitclient.json
    3. 环境变量
    4. 运行目录 qubitclient.json
    5. 构造函数参数（最高优先级）
    
    Args:
        url: 构造函数传入的 url 参数
        api_key: 构造函数传入的 api_key 参数
    
    Returns:
        包含 url 和 api_key 的配置字典
    """
    # 按优先级从低到高收集配置
    default_config = load_default_config()  # 优先级 1
    user_config = load_json_config(get_user_config_path())  # 优先级 2
    env_config = load_env_config()  # 优先级 3
    runtime_config = load_json_config(get_runtime_config_path())  # 优先级 4
    
    # 构造函数参数（优先级 5）
    param_config = {}
    if url is not None:
        param_config['url'] = url
    if api_key is not None:
        param_config['api_key'] = api_key
    
    # 合并所有配置（高优先级的会覆盖低优先级的）
    merged = merge_configs(
        default_config,
        user_config,
        env_config,
        runtime_config,
        param_config
    )
    
    # 验证必需的配置项
    if 'url' not in merged or not merged.get('url'):
        raise ValueError(
            "URL configuration is required. Please provide it via:\n"
            "1. Constructor parameter: QubitScopeClient(url='...')\n"
            "2. Runtime config file: ./qubitclient.json\n"
            "3. Environment variable: QUBITCLIENT_URL\n"
            "4. User config file: ~/qubitclient.json\n"
            "5. Default config.py: API_URL"
        )
    
    if 'api_key' not in merged or not merged.get('api_key'):
        raise ValueError(
            "API_KEY configuration is required. Please provide it via:\n"
            "1. Constructor parameter: QubitScopeClient(api_key='...')\n"
            "2. Runtime config file: ./qubitclient.json\n"
            "3. Environment variable: QUBITCLIENT_API_KEY\n"
            "4. User config file: ~/qubitclient.json\n"
            "5. Default config.py: API_KEY"
        )
    
    return merged
