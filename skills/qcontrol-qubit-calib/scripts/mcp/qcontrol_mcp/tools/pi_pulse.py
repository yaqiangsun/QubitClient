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


def pi_pulse(
    qubit: Annotated[str, "目标量子比特名称"],
    pi_num: Annotated[int, "脉冲数量"] = 1,
    pi_amp: Annotated[any, "脉冲幅度"] = None, # r[0:1:0.02]
    pi_len: Annotated[WithUnit, "脉冲时长"] = 60 * ns,
    z_offset: Annotated[float, "Z偏移量"] = 0.5,
    readout_freq: Annotated[WithUnit, "读取频率"] = 6.164 * GHz,
    readout_power: Annotated[WithUnit, "读取功率"] = -30 * dBm,
    f10: Annotated[WithUnit, "本征频率"] = 3.984 * GHz
) -> str:
    """
    执行 π 脉冲标定
    :param qubit: 目标比特名称
    :param pi_num: 脉冲数量
    :param pi_amp: 脉冲幅度
    :param pi_len: 脉冲时长
    :param z_offset: Z偏移量
    :param readout_freq: 读取频率
    :param readout_power: 读取功率
    :param f10: 比特本征频率
    """
    reload(exp)
    dev_cfg = {
        qubit: {
            "pi_amp": pi_amp,
            "pi_len": pi_len,
            "z_offset": z_offset,
            "readout_freq": readout_freq,
            "readout_power": readout_power,
            "f10": f10,
        }
    }
    raw_data = exp.pi_pulse(
        qubit_configs,
        wiring_configs,
        qubit,
        exp_device_configs=dev_cfg,
        pi_num=pi_num,
        cosine_env=False,
        data_vault_path=data_vault_path,
        description=" ",
        collect=True,
        reps=300,
        read_delay=200 * ns
    )

    return json.dumps(raw_data, ensure_ascii=False)