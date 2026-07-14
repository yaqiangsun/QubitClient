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


def ramsey(
    qubit: Annotated[str, "目标量子比特名称"],
    short_delay: Annotated[bool, "是否使用短延时扫描"] = True,
    delay: Annotated[any, "延迟扫描区间"] = None,
    fringe_freq: Annotated[WithUnit, "条纹频率"] = None,
    opt_couplers: Annotated[Optional[list], "耦合器配置"] = None,
    read_delay: Annotated[WithUnit, "读取延迟"] = 100 * ns,
    simultaneous: Annotated[bool, "同步采集"] = True
) -> str:
    """
    执行 Ramsey 相干时间测量
    :param qubit: 目标比特名称
    :param short_delay: True=短延时扫描, False=长延时扫描
    :param delay: 延迟扫描区间，不传则根据 short_delay 自动赋值
    :param fringe_freq: 条纹频率，不传则根据 short_delay 自动赋值
    :param opt_couplers: 耦合器配置
    :param read_delay: 读取延迟
    :param simultaneous: 同步采集开关
    """
    reload(exp)

    # 未传参时沿用原有默认规则
    if delay is None:
        if short_delay:
            delay = r[0:500:10, ns]
        else:
            delay = r[0:5000:50, ns]

    if fringe_freq is None:
        if short_delay:
            fringe_freq = 10 * MHz
        else:
            fringe_freq = 500 * GHz

    raw_data = exp.ramsey(
        qubit_configs,
        wiring_configs,
        qubit,
        opt_couplers=opt_couplers,
        delay=delay,
        fringe_freq=fringe_freq,
        data_vault_path=data_vault_path,
        cosine_env=False,
        read_delay=read_delay,
        simultaneous=simultaneous
    )

    return json.dumps(raw_data, ensure_ascii=False)