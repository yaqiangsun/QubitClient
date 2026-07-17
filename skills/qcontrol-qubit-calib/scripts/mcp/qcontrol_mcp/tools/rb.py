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


def rb(
    qubits: Annotated[List[str], "目标量子比特名称"],
    couplers:tuple=tuple([]),
    stage:int=3,
    gate:list=['ref'],
    cycle:list=None,
    size:int=11,
    plot:bool=True
) -> str:
    reload(rb)
    qname = qubits[0]
    raw_data = rb.orbit_1q(
        qubit_configs,
        wiring_configs,
        qname,
        data_vault_path=data_vault_path,
        m=r[0:300:20],
        k=20,
        tbuffer=1 * ns,
        gate=gate,
        reps=1200,
        cosine_env=False,
        read_delay=100 * ns
    )
    # raw_data = np.array([32.3, -21.8, -19.6, -17.1, -15.4, -18.9])

    data_list = raw_data.tolist()

    return json.dumps(data_list, ensure_ascii=False)