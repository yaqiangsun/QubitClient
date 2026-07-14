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


def spectroscopy(
    qubit: Annotated[str, "目标量子比特名称"],
    f10: Annotated[any, "比特本征频率"] = None, # r[3.999:4.1:0.0000002, GHz]
    spec_amp: Annotated[any, "频谱幅度"] = None # r[2.999:3:0.0000001]
) -> str:
    """
    执行比特频谱测量
    :param qubit: 目标比特名称
    :param f10: 比特本征频率
    :param spec_amp: 频谱幅度
    """

    # reload(exp)
    # dev_cfg = {
    #     qubit: {
    #         "f10": f10,
    #         "spec_amp": spec_amp,
    #     }
    # }
    # raw_data = exp.spectroscopy(
    #     qubit_configs,
    #     wiring_configs,
    #     qubit,
    #     exp_device_configs=dev_cfg,
    #     read_delay=50 * ns,
    #     sb_freq=100 * MHz,
    #     data_vault_path=data_vault_path,
    #     collect=True,
    #     reps=100
    # )
    raw_data = []


    return json.dumps(raw_data, ensure_ascii=False)