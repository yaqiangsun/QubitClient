
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


def drag(
    qubit: Annotated[str, "目标量子比特名称"],
    gate_num: Annotated[int, "门数量"],
    gate_type: Annotated[str, "门类型 X / X/2"],
    alpha: Annotated[any, "DRAG 校正系数扫描区间"] = None,
    pi_amp: Annotated[float, "脉冲幅度"] = None
) -> str:
    """
    执行 DRAG 门标定
    :param qubit: 目标比特名称
    :param gate_num: 门数量
    :param gate_type: 门类型 X / X/2
    :param alpha: DRAG 校正系数扫描区间
    :param pi_amp: 脉冲幅度
    """
    
    reload(exp)

    # 沿用原有默认规则：不传参时按门类型自动赋值
    if alpha is None:
        if gate_type == "X":
            alpha = r[-2:2:0.00001]
        else:
            alpha = r[-1:1:1]

    if pi_amp is None:
        pi_amp = 0.4427

    raw_data = exp.drag(
        qubit_configs,
        wiring_configs,
        qubit,
        pi_amp=pi_amp,
        alpha=alpha,
        gate_num=gate_num,
        data_vault_path=data_vault_path,
        gate_type=gate_type,
        cosine_env=False,
        read_delay=100 * ns
    )
    latest_raw_data = raw_data

    return json.dumps(raw_data, ensure_ascii=False)