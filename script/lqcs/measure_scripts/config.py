from IPython.core.getipython import get_ipython

ipy = get_ipython()
ipy.run_line_magic('load_ext', 'autoreload')
ipy.run_line_magic('autoreload', '2')
ipy.run_line_magic('matplotlib', 'qt')
ipy.run_line_magic('matplotlib', '')

import os
import pathlib
import re
import sys
import time
from importlib import reload

import labrad

# basic
import ray
from labrad.units import GHz, MHz, V, dBm, kHz, mV, ns, rad, us
from lqcs import system_config
from pylab import np, plt

from lqms.data_process import dataAnalysisCore as dc
from lqms.measure import (
    generate_coupler,
    generate_qubit,
)
from lqms.measure.basic import BasicTuner, util
from lqms.measure.tuners import base_experiment as basex
from lqms.measure.tuners import cz_experiment as czx
from lqms.measure.tuners import cz_nodes as czn
from lqms.measure.tuners import smt_experiment
from lqms.measure.tuners import sq_nodes as sq
from lqms.pyle.util import sweeptools as st
from lqms.pyle.workflow import switchSession
from lqms.utils import rect_lattice as rl
from lqms.utils.save_path import get_info_path

# from data_process.device.E125D04 import E125D04 as DEVICE


def get_qobjs(name):
    if isinstance(name, str):
        return globals()[name]
    else:
        return [globals()[_name] for _name in name]


def reboot_devices(device_names=None):
    """
    reboot the device through ethernet commands

    args:
        device_names: list[str],
            the device name list to be rebooted, for example, ['DAC_LQ 1']
            if not provided, reboot all the device connected in device manager
    """
    device_manager = ray.get_actor('Device Manager')
    device_manager.reboot.remote(device_names)


## labrad
cxn = labrad.connect()
util.setWiringInfo(cxn)
user = 'LQHL'
s = switchSession(cxn, user=user)
# print("Registry user: ",user)


# experiment
try:
    info = dc.InfoBase(get_info_path(s))
except Exception:
    info = None
_all_qubits = generate_qubit(globals(), info=info, sample=s)
_all_couplers = generate_coupler(globals(), info=info, sample=s)
# for impa in DEVICE.IMPAS.values():
#     exec(f'{impa} = qubitAuto.Qubit("{impa}")')

auto_config = {
    'stats': 300,
    'correctX': False,
    'correctZ': False,
    'reset': False,
    'apply_21': False,
    'run_mode': 'local',
}
# initialize basic tunner
BasicTuner(**auto_config)
BasicTuner._sample = s
BasicTuner._all_qobjs = _all_qubits | _all_couplers

# ray
HEAD_IP_ADDRESS = system_config.get_ray_head()
NODE_IP_ADDRESS = system_config.get_config()['ip']
RAY_PORT = system_config.get_ray_port()
print('NODE_IP_ADDRESS', NODE_IP_ADDRESS)
if not ray.is_initialized():
    ray.init(
        address=f'{HEAD_IP_ADDRESS}:{RAY_PORT}',
        namespace='main',
        _node_ip_address=NODE_IP_ADDRESS,
        log_to_driver=False,
    )
def export_help_to_file(obj, filename='object_methods.txt'):
    """
    将对象的帮助信息导出到文件，支持中文
    """
    import sys
    from io import StringIO
    
    # 设置标准输出的编码（如果需要）
    if hasattr(sys.stdout, 'encoding'):
        original_encoding = sys.stdout.encoding
    else:
        original_encoding = None
    
    try:
        # 使用utf-8编码打开文件
        with open(filename, 'w', encoding='utf-8') as f:
            # 保存原来的stdout
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            
            # 临时设置stdout的编码（如果可能）
            try:
                if hasattr(sys.stdout, 'reconfigure'):
                    sys.stdout.reconfigure(encoding='utf-8')
            except:
                pass
            
            # 获取帮助信息
            help(obj)
            
            # 恢复stdout并获取内容
            sys.stdout = old_stdout
            help_info = mystdout.getvalue()
            
            # 写入文件
            f.write(help_info)
            
            print(f"帮助信息已保存到: {filename}")
            
    except Exception as e:
        print(f"保存文件时出错: {e}")
    finally:
        # 恢复原来的编码（如果修改过）
        if original_encoding and hasattr(sys.stdout, 'reconfigure'):
            try:
                sys.stdout.reconfigure(encoding=original_encoding)
            except:
                pass
