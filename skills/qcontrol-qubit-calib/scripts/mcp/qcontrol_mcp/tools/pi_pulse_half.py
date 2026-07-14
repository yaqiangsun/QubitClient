from importlib import reload
from typing import Annotated, Optional
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


def pi_pulse_half(
    qubit: Annotated[str, "目标量子比特名称"],
    pi_num: Annotated[int, "脉冲数量 1/3/5"],
    pi_amp_half: Annotated[any, "半脉冲幅度"] = None # r[1:1.1:0.000005]
) -> str:
    """
    执行半π脉冲测量
    :param qubit: 目标比特名称
    :param pi_num: 脉冲数量 1/3/5
    :param pi_amp_half: 半脉冲幅度
    """
    
    reload(exp)
    dev_cfg = {
        qubit: {
            "pi_amp_half": pi_amp_half,
        }
    }
    raw_data = exp.pi_pulse_half(
        qubit_configs,
        wiring_configs,
        qubit,
        exp_device_configs=dev_cfg,
        pi_num=pi_num,
        data_vault_path=data_vault_path,
        description=" ",
        collect=False,
        reps=300,
        cosine_env=False,
        read_delay=100 * ns
    )

    return json.dumps(raw_data, ensure_ascii=False)