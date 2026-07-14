
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


def s21(
    qubit: Annotated[str, "目标量子比特名称"],
    readout_freq: Annotated[any, "读取频率"] = None, # r[6.59:6.61:0.0002, GHz]
    readout_power: Annotated[any, "读取功率"] = -10 * dBm
) -> str:
    """
    执行 S21 读取腔测量
    :param qubit: 目标比特名称，如 qr2
    :param readout_freq: 读取频率
    :param readout_power: 读取功率
    """
    # reload(exp)
    
    # dev_cfg = {
    #     qubit: {
    #         "readout_freq": readout_freq,
    #         "readout_power": readout_power,
    #     }
    # }
    # raw_data = exp.s21(
    #     qubit_configs,
    #     wiring_configs,
    #     [qubit],
    #     exp_device_configs=dev_cfg,
    #     sb_freq=100 * MHz,
    #     data_vault_path=data_vault_path,
    #     collect=True,
    #     reps=300
    # )

    # FIXME:模拟数据
    raw_data = np.array([-22.3, -21.8, -19.6, -17.1, -15.4, -18.9])

    return json.dumps(raw_data, ensure_ascii=False)