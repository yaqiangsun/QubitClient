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


def rabihalf(
    qubits: List[str],
    piamp_half_start:float=0,
    piamp_half_end:float=2,
    piamp_half_sample_num:int=16,
    pi_len_half: float=50.0
) -> str:

    pi_amp_half_arr = np.linspace(piamp_half_start, piamp_half_end, piamp_half_sample_num)
    qname = qubits[0]
    reload(exp)

    raw_data = exp.pi_pulse_half(
        qubit_configs,
        wiring_configs,
        qname,
        exp_device_configs={
            opt_qubits: {
                "pi_amp_half": pi_amp_half_arr,
                # "pi_amp_half": 1, # FIXME:不传pi_len_half吗
            }
        },
        pi_num=1,
        data_vault_path=data_vault_path,
        description=" ",
        collect=False,
        reps=300,
        cosine_env=False,
        read_delay=100 * ns,
    )

    # 模拟数据
    # raw_data = np.array([-22.3, -21.8, -19.6, -17.1, -15.4, -18.9])

    data_list = raw_data.tolist()

    return json.dumps(data_list, ensure_ascii=False)