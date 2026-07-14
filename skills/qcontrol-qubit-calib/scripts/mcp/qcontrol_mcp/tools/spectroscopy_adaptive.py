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


def spectroscopy_adaptive(
    qubit: Annotated[str, "目标量子比特名称"],
    spec_amp: Annotated[float, "频谱幅度"] = 0.5,
    spec_len: Annotated[WithUnit, "频谱时长"] = 1 * us
) -> str:
    """
    执行自适应频谱测量
    :param qubit: 目标比特名称
    :param spec_amp: 频谱幅度
    :param spec_len: 频谱时长
    """
    reload(exp)
    dev_cfg = {
        qubit: {
            "spec_amp": spec_amp,
            "spec_len": spec_len,
        }
    }
    raw_data = exp.spectroscopy_adaptive(
        qubit_configs,
        wiring_configs,
        qubit,
        sb_freq=100 * MHz,
        freq_scan=r[-0.006:0.006:0.0006, GHz],
        zpa_scan=r[-0.8:0.19:0.2],
        exp_device_configs=dev_cfg,
        data_vault_path=data_vault_path,
        description="",
        collect=True,
        scan_shrink_ratio=0.3,
        reps=300
    )

    return json.dumps(raw_data, ensure_ascii=False)