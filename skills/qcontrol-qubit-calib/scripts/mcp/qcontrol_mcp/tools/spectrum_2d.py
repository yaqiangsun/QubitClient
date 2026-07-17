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
from qubitclient.ctrl import QubitCtrlClient
# 全局配置
data_vault_path = ["", "test", "single"]
# set_wiring_configs("wiring_config.json")
# qubit_configs = QConfig("qubit_config.json")


def spectrum_2d(
    qubits: Annotated[list[str], "量子比特名称"] = ['Q0', 'Q1'],
    freq_start: Annotated[float, "频率起始值，单位GHz"] = 3.0,
    freq_end: Annotated[float, "频率终止值，单位GHz"] = 5.0,
    freq_sample_num: Annotated[int, "频率采样点数"] = 100,
    zpa_start: Annotated[float, "偏置起始值"] = -1,
    zpa_end: Annotated[float, "偏置终止值"] = 1,
    zpa_sample_num: Annotated[int, "偏置采样点数"] = 100,
    spec_amp: Annotated[float, "驱动脉冲幅值"] = 0.5,
    sb_freq: Annotated[float, "边带频率，单位GHz"] = -0.15
) -> str:
    qubit_ctrl_client = QubitCtrlClient()
    qname = qubits[0]
    
    spec_len_star = float(qubit_ctrl_client.query_param(qname=qname, key="spec_len_star"))

    reload(exp)
    dev_cfg = {
        qubits: {
            "spec_amp": spec_amp,
            "spec_len": spec_len_star,
        }
    }
    freq_arr = np.linspace(freq_start, freq_end, freq_sample_num)
    zpa_arr = np.linspace(zpa_start, zpa_end, zpa_sample_num)

    raw_data = exp.spectroscopy_adaptive(
        qubit_configs,
        wiring_configs,
        qname,
        sb_freq=sb_freq,
        freq_scan=freq_arr,
        zpa_scan=zpa_arr,
        exp_device_configs=dev_cfg,
        data_vault_path=data_vault_path,
        description="",
        collect=True,
        scan_shrink_ratio=0.3,
        reps=300
    )
    # raw_data = np.array([9.3, -21.8, -19.6, -17.1, -15.4, -18.9])

    data_list = raw_data.tolist()

    return json.dumps(data_list, ensure_ascii=False)