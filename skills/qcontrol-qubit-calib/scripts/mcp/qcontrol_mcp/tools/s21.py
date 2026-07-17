
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


def s21(
    qubits: Annotated[List[str], "目标量子比特名称"],
    frequency_center: Annotated[float, "中心频率，单位GHz"] = 6.5,
    frequency_half_bandwidth: Annotated[float, "频率半带宽，单位GHz"] = 0.0005,
    frequency_sample_num: Annotated[int, "频率采样点数"] = 101,
) -> str:
    
    # qubit_ctrl_client = QubitCtrlClient()
    # qname = qubits[0]

    # frequency_start = frequency_center - frequency_half_bandwidth
    # frequency_end = frequency_center + frequency_half_bandwidth
    # freq = np.linspace(frequency_start, frequency_end, frequency_sample_num)

    # readout_power = float(qubit_ctrl_client.query_param(qname=qname, key="readout_power_star"))

    # reload(exp)
    
    # dev_cfg = {
    #     qubit: {
    #         "readout_freq": freq,
    #         "readout_power": readout_power,
    #     }
    # }
    # raw_data = exp.s21(
    #     qubit_configs,
    #     wiring_configs,
    #     [qname],
    #     exp_device_configs=dev_cfg,
    #     sb_freq=100 * MHz,
    #     data_vault_path=data_vault_path,
    #     collect=True,
    #     reps=300
    # )

    # 模拟数据
    raw_data = np.array([-2.3, -21.8, -19.6, -17.1, -15.4, -18.9])
    data_list = raw_data.tolist()

    return json.dumps(data_list, ensure_ascii=False)