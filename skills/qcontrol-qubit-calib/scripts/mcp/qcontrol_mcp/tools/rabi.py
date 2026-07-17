from importlib import reload
from typing import Annotated, Optional, List
import json
import numpy as np
from labrad.units import Unit, Value, WithUnit
from qubitclient.ctrl import QubitCtrlClient

# from qcontrol.config import wiring_configs
# from qcontrol.experiment import experiments as exp
# from qcontrol.utils.qconfig import QConfig
# from qcontrol.config.settings import set_wiring_configs
# from qcontrol.experiment.utils.range import Range, r
V, mV, us, ns, GHz, MHz, dBm, rad, uA = [
    Unit(s) for s in ("V", "mV", "us", "ns", "GHz", "MHz", "dBm", "rad", "uA")
]

# 全局配置
data_vault_path = ["", "test", "single"]
# set_wiring_configs("wiring_config.json")
# qubit_configs = QConfig("qubit_config.json")


def rabi(
    qubits: List[str],
    piamp_start:float=0,
    piamp_end:float=2,
    piamp_sample_num:int=16,
    pi_len: float=50.0
) -> str:
    qubit_ctrl_client = QubitCtrlClient()
    qname = qubits[0]

    pi_amp_arr = np.linspace(piamp_start, piamp_end, piamp_sample_num)

    z_offset_star = float(qubit_ctrl_client.query_param(qname=qname, key="z_offset_star"))
    readout_freq_star = float(qubit_ctrl_client.query_param(qname=qname, key="readout_freq_star"))
    readout_power_star = float(qubit_ctrl_client.query_param(qname=qname, key="readout_power_star"))
    f10_star = float(qubit_ctrl_client.query_param(qname=qname, key="f10_star"))

    reload(exp)
    dev_cfg = {
        qname: {
            "pi_amp": pi_amp_arr,
            "pi_len": pi_len,
            "z_offset": z_offset_star,
            "readout_freq": readout_freq_star,
            "readout_power": readout_power_star,
            "f10": f10_star,
        }
    }
    raw_data = exp.pi_pulse(
        qubit_configs,
        wiring_configs,
        qname,
        exp_device_configs=dev_cfg,
        pi_num=1,
        cosine_env=False,
        data_vault_path=data_vault_path,
        description=" ",
        collect=True,
        reps=300,
        read_delay=200 * ns
    )

    # 模拟数据
    # raw_data = np.array([-142.3, -21.8, -19.6, -17.1, -15.4, -18.9])

    data_list = raw_data.tolist()

    return json.dumps(data_list, ensure_ascii=False)