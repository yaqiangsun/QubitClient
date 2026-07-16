from importlib import reload
from typing import Annotated, Optional, List
import json
from qubitclient.ctrl import QubitCtrlClient
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


def singleshot(
    qubits: Annotated[List[str], "目标量子比特名称"],
) -> str:
    """
    执行 IQ 原始数据采集
    :param qubit: 目标比特名称
    """
    reload(exp)
    qubit_configs.refresh()

    qubit_ctrl_client = QubitCtrlClient()
    qname = qubits[0]

    pi_amp_star = float(qubit_ctrl_client.query_param(qname=qname, key="pi_amp_star"))
    pi_len_star = float(qubit_ctrl_client.query_param(qname=qname, key="pi_len_star"))
    z_offset_star = float(qubit_ctrl_client.query_param(qname=qname, key="z_offset_star"))
    readout_freq_star = float(qubit_ctrl_client.query_param(qname=qname, key="readout_freq_star"))

    readout_power_star = float(qubit_ctrl_client.query_param(qname=qname, key="readout_power_star"))
    f10_star = float(qubit_ctrl_client.query_param(qname=qname, key="f10_star"))
    readout_len_star = float(qubit_ctrl_client.query_param(qname=qname, key="readout_len_star"))
    adc_start_delay_star = float(qubit_ctrl_client.query_param(qname=qname, key="adc_start_delay_star"))

    dev_cfg = {
        qname: {
            "pi_amp": pi_amp_star,
            "pi_len": pi_len_star,
            "z_offset": z_offset_star,
            "readout_freq": readout_freq_star,
            "readout_power": readout_power_star,
            "f10": f10_star,
            "readout_len": readout_len_star,
            "adc_start_delay": adc_start_delay_star,
        }
    }
    raw_data = exp.IQraw(
        qubit_configs,
        wiring_configs,
        qname,
        exp_device_configs=dev_cfg,
        reps=3000,
        data_vault_path=data_vault_path,
        cosine_env=False,
        read_delay=100 * ns
    )

    data_list = raw_data.tolist()

    return json.dumps(data_list, ensure_ascii=False)