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


def ramsey(
    qubits: Annotated[List[str], "目标量子比特名称"],
    delay_start:float=0,
    delay_end:float=100,
    delay_sample_num:int=100,
    fringeFreq:float=0.05
) -> str:

    reload(exp)

    delay_array = np.linspace(delay_start, delay_end, delay_sample_num)

    raw_data = exp.ramsey(
        qubit_configs,
        wiring_configs,
        qubits,
        opt_couplers=None,
        delay=delay_array,
        fringe_freq=fringeFreq,
        data_vault_path=data_vault_path,
        cosine_env=False,
        read_delay=100 * ns,
        simultaneous=True
    )

    data_list = raw_data.tolist()

    return json.dumps(data_list, ensure_ascii=False)