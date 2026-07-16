
from importlib import reload
from typing import Annotated, Optional, List
import json
import numpy as np
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


def drag(
    qubits: Annotated[List[str], "目标量子比特名称"],
    lamb:list[float]=[-0.5, 0.5],
    stage:int=1,
    N_repeat:int=1,
    pulsePair:list[int]=[0, 1],
    signal:str='population'
) -> str:
    
    reload(exp)

    raw_data = exp.drag(
        qubit_configs,
        wiring_configs,
        qubits,
        pi_amp=pi_amp,
        alpha=alpha,
        gate_num=gate_num,
        data_vault_path=data_vault_path,
        gate_type=gate_type,
        cosine_env=False,
        read_delay=100 * ns
    )

    data_list = raw_data.tolist()

    return json.dumps(data_list, ensure_ascii=False)