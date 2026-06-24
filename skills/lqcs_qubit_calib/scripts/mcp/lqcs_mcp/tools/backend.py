
import labrad
import matplotlib
matplotlib.rcParams['backend'] = 'Agg'
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
import io
from docx.enum.text import WD_ALIGN_PARAGRAPH
from lqms.data_process import *

from importlib import reload

import labrad
import ray
from lqcs import system_config
from pylab import np, plt

from lqms.data_process import dataAnalysisCore as dc
from lqms.measure.basic import BasicTuner, util
from lqms.pyle.workflow import switchSession

from lqms.measure import (
    generate_coupler,
    generate_qubit,
)


freads = {}
f10s = {}
T1s = {}
fids = {}
cxn = labrad.connect()
util.setWiringInfo(cxn)
user = 'LQHL'
s = switchSession(cxn, user=user)
session = ['', 'LQHL', 'test', '20260324']
dv = cxn.data_vault

data = dc.DataLab(session, dv, dv_type='data_vault')

info = None
_all_qubits = generate_qubit(globals(), info=info, sample=s)
_all_couplers = generate_coupler(globals(), info=info, sample=s)


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

