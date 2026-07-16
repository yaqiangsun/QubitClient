from importlib import reload
from typing import Annotated, Optional, List
import json
import numpy as np
from qubitclient.ctrl import QubitCtrlClient
from labrad.units import Unit, Value, WithUnit
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


def pi_pulse_half(
    qubits: List[str],
    N_list:list[int]=[1, 3, 5],
    amp_list:list[float]=None
) -> str:
    
    reload(exp)
    qubit_ctrl_client = QubitCtrlClient()
    qname = qubits[0]
    pi_amp_half_star = float(qubit_ctrl_client.query_param(qname=qname, key="pi_amp_half_star"))
    dev_cfg = {
        qubits: {
            "pi_amp_half": pi_amp_half_star,
        }
    }
    raw_data = exp.pi_pulse_half(
        qubit_configs,
        wiring_configs,
        qubits,
        exp_device_configs=dev_cfg,
        pi_num=1,
        data_vault_path=data_vault_path,
        description=" ",
        collect=False,
        reps=300,
        cosine_env=False,
        read_delay=100 * ns
    )

    data_list = raw_data.tolist()

    return json.dumps(data_list, ensure_ascii=False)