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


def spectrum(
    qubits: Annotated[List[str], "目标量子比特名称"],
    freq_start:float=1.0,
    freq_end:float=3.0,
    freq_sample_num:int=200,
    zpa:float=0,
    spec_amp:float=0.0,
    sb_freq:float=0
) -> str:
    qname = qubits[0]
    qubit_ctrl_client = QubitCtrlClient()

    f10_star = float(qubit_ctrl_client.query_param(qname=qname, key="f10_star"))

    reload(exp)
    dev_cfg = {
        qname: {
            "f10": f10_star,
            "spec_amp": spec_amp,
        }
    }
    raw_data = exp.spectroscopy(
        qubit_configs,
        wiring_configs,
        qubits,
        exp_device_configs=dev_cfg,
        read_delay=50 * ns,
        sb_freq=sb_freq,
        data_vault_path=data_vault_path,
        collect=True,
        reps=100
    )
    data_list = raw_data.tolist()

    return json.dumps(data_list, ensure_ascii=False)