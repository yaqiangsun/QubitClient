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


def t1(
    qubits: Annotated[List[str], "目标量子比特名称"],
    delay_start: Annotated[int, "延时起始值，单位纳秒"] = 0,
    delay_end: Annotated[int, "延时终止值，单位纳秒"] = 80000,
    delay_sample_num: Annotated[int, "延时采样点数"] = 17,
    zpa: Annotated[float, "直流偏置值"] = 0.0
) -> str:

    delay_array = np.linspace(delay_start, delay_end, delay_sample_num)
    
    reload(exp)
    qubit = qubits[0]

    if zpa == None:
        zpa = float(qubit_ctrl_client.query_param(qname=qname, key="z_offset_star"))

    raw_data = exp.t1(
        qubit_configs,
        wiring_configs,
        qubits,
        q_states=["I", "X"],
        delay=delay_array,
        data_vault_path=data_vault_path,
        zpa=zpa,
        cosine_env=False,
        read_delay=100 * ns,
        reps=3000
    )

    data_list = raw_data.tolist()

    return json.dumps(data_list, ensure_ascii=False)