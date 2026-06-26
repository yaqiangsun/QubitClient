import labrad
from IPython.core.getipython import get_ipython
from get_help import *
ipy = get_ipython()
ipy.run_line_magic('load_ext', 'autoreload')
ipy.run_line_magic('autoreload', '2')
ipy.run_line_magic('matplotlib', '')
import pathlib
import sys

print('##########################################################')
print('#    Data Process Config in Project ExperimentProcess    #')
print('##########################################################')
import numpy as np
from lqms.data_process import *
from lqms.pyle import registry_wrapper2
from lqms.utils.save_path import get_info_path

# 画图中使用中文
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False

rootPath = str(pathlib.Path(__file__).parent)
sys.path.insert(1, rootPath)

cxn = labrad.connect()
dv = cxn.data_vault


def switch_session(session, info_path=None, dv_type='data_vault'):
    """
    session: (e.g.)['', 'qguo', '20200601_C32A01']
    """
    global s
    global data
    global info
    global qter

    try:
        s = registry_wrapper2.RegistryWrapper(cxn, session)
    except Exception:
        s = None
    try:
        assert dv_type in ['data_vault', 'local_data_vault']
        if dv_type == 'data_vault':
            data = dc.DataLab(session, dv, dv_type=dv_type)
        else:
            data = dc.DataLab(session, dv_type=dv_type)
    except Exception:
        data = None
    try:
        if info_path is None:
            info_path = get_info_path(s)
        info = dc.InfoBase(info_path)
    except Exception:
        info = None
    try:
        qter = QubitUpdater(data, info)
    except Exception:
        qter = None

    print('#' * 20)
    try:
        assert s is not None
        print('sample loaded!!!')
        print('#' * 20)
    except Exception:
        pass
    try:
        assert data is not None
        print('data loaded!!!')
        print('#' * 20)
    except Exception:
        pass
    try:
        assert info is not None
        print('info loaded!!!')
        print('#' * 20)
    except Exception:
        pass
    try:
        assert qter is not None
        print('qter loaded!!!')
        print('#' * 20)
    except Exception:
        pass


def czecho2fid(data, datasets0, datasets1, m=15):
    p0s = []
    p1s = []
    for idx, d0 in enumerate(datasets0):
        d1 = datasets1[idx]
        data.loadDataset(d0)
        p0s.append(np.max(data.get_data(dep_index=0)))
        data.loadDataset(d1)
        p1s.append(np.max(data.get_data(dep_index=0)))
    pmax = np.max(p0s)
    idxs = np.arange(len(datasets0))[np.array(p0s) > pmax - 0.05]
    fids = np.zeros(len(datasets0))
    for idx in idxs:
        fids[idx] = 10 ** (np.log10(p1s[idx] / p0s[idx]) / 15)
    return fids
