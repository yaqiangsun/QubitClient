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


def iqraw(
    qubit: Annotated[str, "目标量子比特名称"],
    pi_amp: Annotated[float, "脉冲幅度"] = 0.446,
    pi_len: Annotated[WithUnit, "脉冲时长"] = 30 * ns,
    z_offset: Annotated[float, "Z偏移量"] = 0.5,
    readout_freq: Annotated[WithUnit, "读取频率"] = 6.6 * GHz,
    readout_power: Annotated[WithUnit, "读取功率"] = -100 * dBm,
    f10: Annotated[WithUnit, "本征频率"] = 3.984 * GHz,
    readout_len: Annotated[WithUnit, "读取时长"] = 2.048 * us,
    adc_start_delay: Annotated[any, "ADC起始延迟区间"] = None # r[620:650:1, ns]
) -> str:
    """
    执行 IQ 原始数据采集
    :param qubit: 目标比特名称
    :param pi_amp: 脉冲幅度
    :param pi_len: 脉冲时长
    :param z_offset: Z偏移量
    :param readout_freq: 读取频率
    :param readout_power: 读取功率
    :param f10: 比特本征频率
    :param readout_len: 读取时长
    :param adc_start_delay: ADC起始延迟区间
    """
    reload(exp)
    qubit_configs.refresh()

    dev_cfg = {
        qubit: {
            "pi_amp": pi_amp,
            "pi_len": pi_len,
            "z_offset": z_offset,
            "readout_freq": readout_freq,
            "readout_power": readout_power,
            "f10": f10,
            "readout_len": readout_len,
            "adc_start_delay": adc_start_delay,
        }
    }
    raw_data = exp.IQraw(
        qubit_configs,
        wiring_configs,
        qubit,
        exp_device_configs=dev_cfg,
        reps=3000,
        data_vault_path=data_vault_path,
        cosine_env=False,
        read_delay=100 * ns
    )

    return json.dumps(raw_data, ensure_ascii=False)