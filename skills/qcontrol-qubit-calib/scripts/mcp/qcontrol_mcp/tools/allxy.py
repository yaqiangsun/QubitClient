
from importlib import reload
from typing import Annotated, Optional
import json
import numpy as np

# from qcontrol.config import wiring_configs
# from qcontrol.experiment import experiments as exp
# from qcontrol.utils.qconfig import QConfig
# from qcontrol.config.settings import set_wiring_configs
from labrad.units import Unit, Value, WithUnit
# from qcontrol.experiment.utils.range import Range, r
V, mV, us, ns, GHz, MHz, dBm, rad, uA = [
    Unit(s) for s in ("V", "mV", "us", "ns", "GHz", "MHz", "dBm", "rad", "uA")
]

# 全局配置
data_vault_path = ["", "test", "single"]
# set_wiring_configs("wiring_config.json")
# qubit_configs = QConfig("qubit_config.json")

def allxy(qubit: Annotated[str, "目标量子比特名称"]) -> str:
    """
    执行 AllXY 标定测量
    :param qubit: 目标比特名称
    """

    reload(exp)
    raw_data = exp.allxy(
        qubit_configs,
        wiring_configs,
        [qubit],
        data_vault_path=data_vault_path,
        collect=True,
        read_delay=100 * ns,
        start_delay=50 * ns,
        cosine_env=False
    )

    return json.dumps(raw_data, ensure_ascii=False)