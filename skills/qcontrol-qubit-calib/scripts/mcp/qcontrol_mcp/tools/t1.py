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

# 全局配置
data_vault_path = ["", "test", "single"]
# set_wiring_configs("wiring_config.json")
# qubit_configs = QConfig("qubit_config.json")


def t1(
    qubit: Annotated[str, "目标量子比特名称"],
    q_states: Annotated[List[str], "量子态列表"] = ["I", "X"],
    delay: Annotated[WithUnit, "延迟时长"] = 100 * us,
    zpa: Annotated[float, "Z轴偏移量"] = None,
    read_delay: Annotated[WithUnit, "读取延迟"] = 100 * ns,
    reps: Annotated[int, "采样次数"] = 3000
) -> str:
    """
    执行 T1 弛豫时间测量
    :param qubit: 目标比特名称
    :param q_states: 量子态列表
    :param delay: 延迟时长
    :param zpa: Z轴偏移量，为空则从配置读取
    :param read_delay: 读取延迟
    :param reps: 采样次数
    """
    
    reload(exp)

    # 未传zpa时，沿用原有逻辑从配置获取
    if zpa is None:
        zpa = qubit_configs[qubit]["z_offset"]

    raw_data = exp.t1(
        qubit_configs,
        wiring_configs,
        qubit,
        q_states=q_states,
        delay=delay,
        data_vault_path=data_vault_path,
        zpa=zpa,
        cosine_env=False,
        read_delay=read_delay,
        reps=reps
    )
    latest_raw_data = raw_data

    return json.dumps(raw_data, ensure_ascii=False)