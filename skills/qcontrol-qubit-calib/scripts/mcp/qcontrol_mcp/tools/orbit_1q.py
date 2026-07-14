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


def orbit_1q(
    qubit: Annotated[str, "目标量子比特名称"],
    gate: Annotated[str, "门类型"] = "reference",
    m: Annotated[any, "随机序列长度区间"] = None, # r[0:300:20]
    k: Annotated[int, "随机序列数量"] = 20,
    tbuffer: Annotated[WithUnit, "脉冲间隔"] = 10 * ns,
    reps: Annotated[int, "采样次数"] = 1200,
    read_delay: Annotated[WithUnit, "读取延迟"] = 100 * ns
) -> str:
    """
    执行单比特随机基准测试 RB
    :param qubit: 目标比特名称
    :param gate: 门类型
    :param m: 随机序列长度区间
    :param k: 随机序列数量
    :param tbuffer: 脉冲间隔
    :param reps: 采样次数
    :param read_delay: 读取延迟
    """
    reload(rb)
    raw_data = rb.orbit_1q(
        qubit_configs,
        wiring_configs,
        qubit,
        data_vault_path=data_vault_path,
        m=m,
        k=k,
        tbuffer=tbuffer,
        gate=gate,
        reps=reps,
        cosine_env=False,
        read_delay=read_delay
    )

    return json.dumps(raw_data, ensure_ascii=False)