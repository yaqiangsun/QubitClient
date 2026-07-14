# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import json
from typing import Dict, Any, Optional, List
from typing import Annotated
from swiftmcp import mcp
from labrad.units import Unit, Value, WithUnit

# 定义物理单位
V, mV, us, ns, GHz, MHz, dBm, rad, uA = [
    Unit(s) for s in ("V", "mV", "us", "ns", "GHz", "MHz", "dBm", "rad", "uA")
]

from qcontrol_mcp.tools import s21 as qcontrol_s21
from qcontrol_mcp.tools import spectroscopy as qcontrol_spectroscopy
from qcontrol_mcp.tools import allxy as qcontrol_allxy
from qcontrol_mcp.tools import spectroscopy_adaptive as qcontrol_spectroscopy_adaptive
from qcontrol_mcp.tools import pi_pulse as qcontrol_pi_pulse
from qcontrol_mcp.tools import pi_pulse_half as qcontrol_pi_pulse_half
from qcontrol_mcp.tools import drag as qcontrol_drag
from qcontrol_mcp.tools import iqraw as qcontrol_iqraw
from qcontrol_mcp.tools import t1 as qcontrol_t1
from qcontrol_mcp.tools import ramsey as qcontrol_ramsey
from qcontrol_mcp.tools import orbit_1q as qcontrol_orbit_1q

# ==================== 全局初始化 ====================
data_vault_path = ["", "test", "single"]

# ------模拟 r数列-----------
class RangeObj:
    def __init__(self, start, stop, step, unit=None):
        self.start = start
        self.stop = stop
        self.step = step
        self.unit = unit

class RangeMaker:
    def __getitem__(self, item):
        if isinstance(item, tuple):
            slice_part, unit = item
        else:
            slice_part = item
            unit = None
        start = slice_part.start
        stop = slice_part.stop
        step = slice_part.step
        return RangeObj(start, stop, step, unit)

r = RangeMaker()

# ==============================================
# 所有参数注解统一改为 Any，绕过 Pydantic 解析
# ==============================================
@mcp.tool
async def s21(
    qubit: Annotated[str, "目标量子比特名称"],
    readout_freq: Annotated[Any, "读取频率"] = r[6.59:6.61:0.0002, GHz],
    readout_power: Annotated[Any, "读取功率"] = -10 * dBm
) -> str:
    return qcontrol_s21(qubit=qubit, readout_freq=readout_freq, readout_power=readout_power)


@mcp.tool
async def spectroscopy(
    qubit: Annotated[str, "目标量子比特名称"],
    f10: Annotated[Any, "比特本征频率"] = r[3.999:4.1:0.0000002, GHz],
    spec_amp: Annotated[Any, "频谱幅度"] = r[2.999:3:0.0000001]
) -> str:
    return qcontrol_spectroscopy(qubit=qubit, f10=f10, spec_amp=spec_amp)

@mcp.tool
async def allxy(qubit: Annotated[str, "目标量子比特名称"]) -> str:
    return qcontrol_allxy(qubit=qubit)


@mcp.tool
async def spectroscopy_adaptive(
    qubit: Annotated[str, "目标量子比特名称"],
    spec_amp: Annotated[Any, "频谱幅度"] = 0.5,
    spec_len: Annotated[Any, "频谱时长"] = 1 * us
) -> str:
    return qcontrol_spectroscopy_adaptive(qubit=qubit, spec_amp=spec_amp, spec_len=spec_len)


@mcp.tool
async def pi_pulse(
    qubit: Annotated[str, "目标量子比特名称"],
    pi_num: Annotated[int, "脉冲数量"] = 1,
    pi_amp: Annotated[Any, "脉冲幅度"] = r[0:1:0.02],
    pi_len: Annotated[Any, "脉冲时长"] = 60 * ns,
    z_offset: Annotated[float, "Z偏移量"] = 0.5,
    readout_freq: Annotated[Any, "读取频率"] = 6.164 * GHz,
    readout_power: Annotated[Any, "读取功率"] = -30 * dBm,
    f10: Annotated[Any, "本征频率"] = 3.984 * GHz
) -> str:
    return qcontrol_pi_pulse(
        qubit=qubit, pi_num=pi_num, pi_amp=pi_amp, pi_len=pi_len,
        z_offset=z_offset, readout_freq=readout_freq,
        readout_power=readout_power, f10=f10
    )


@mcp.tool
async def pi_pulse_half(
    qubit: Annotated[str, "目标量子比特名称"],
    pi_num: Annotated[int, "脉冲数量 1/3/5"],
    pi_amp_half: Annotated[Any, "半脉冲幅度"] = r[1:1.1:0.000005]
) -> str:
    return qcontrol_pi_pulse_half(qubit=qubit, pi_num=pi_num, pi_amp_half=pi_amp_half)


@mcp.tool
async def drag(
    qubit: Annotated[str, "目标量子比特名称"],
    gate_num: Annotated[int, "门数量"],
    gate_type: Annotated[str, "门类型 X / X/2"],
    alpha: Annotated[Any, "DRAG 校正系数扫描区间"] = None,
    pi_amp: Annotated[Any, "脉冲幅度"] = None
) -> str:
    return qcontrol_drag(qubit=qubit, gate_num=gate_num, gate_type=gate_type, alpha=alpha, pi_amp=pi_amp)


@mcp.tool
async def iqraw(
    qubit: Annotated[str, "目标量子比特名称"],
    pi_amp: Annotated[Any, "脉冲幅度"] = 0.446,
    pi_len: Annotated[Any, "脉冲时长"] = 30 * ns,
    z_offset: Annotated[float, "Z偏移量"] = 0.5,
    readout_freq: Annotated[Any, "读取频率"] = 6.6 * GHz,
    readout_power: Annotated[Any, "读取功率"] = -100 * dBm,
    f10: Annotated[Any, "本征频率"] = 3.984 * GHz,
    readout_len: Annotated[Any, "读取时长"] = 2.048 * us,
    adc_start_delay: Annotated[Any, "ADC起始延迟区间"] = r[620:650:1, ns]
) -> str:
    return qcontrol_iqraw(
        qubit=qubit, pi_amp=pi_amp, pi_len=pi_len, z_offset=z_offset,
        readout_freq=readout_freq, readout_power=readout_power,
        f10=f10, readout_len=readout_len, adc_start_delay=adc_start_delay
    )


@mcp.tool
async def t1(
    qubit: Annotated[str, "目标量子比特名称"],
    q_states: Annotated[List[str], "量子态列表"] = ["I", "X"],
    delay: Annotated[Any, "延迟时长"] = 100 * us,
    zpa: Annotated[float, "Z轴偏移量"] = None,
    read_delay: Annotated[Any, "读取延迟"] = 100 * ns,
    reps: Annotated[int, "采样次数"] = 3000
) -> str:
    return qcontrol_t1(
        qubit=qubit, q_states=q_states, delay=delay, zpa=zpa,
        read_delay=read_delay, reps=reps
    )


@mcp.tool
async def ramsey(
    qubit: Annotated[str, "目标量子比特名称"],
    short_delay: Annotated[bool, "是否使用短延时扫描"] = True,
    delay: Annotated[Any, "延迟扫描区间"] = None,
    fringe_freq: Annotated[Any, "条纹频率"] = None,
    opt_couplers: Annotated[Optional[list], "耦合器配置"] = None,
    read_delay: Annotated[Any, "读取延迟"] = 100 * ns,
    simultaneous: Annotated[bool, "同步采集"] = True
) -> str:
    return qcontrol_ramsey(
        qubit=qubit, short_delay=short_delay, delay=delay,
        fringe_freq=fringe_freq, opt_couplers=opt_couplers,
        read_delay=read_delay, simultaneous=simultaneous
    )


@mcp.tool
async def orbit_1q(
    qubit: Annotated[str, "目标量子比特名称"],
    gate: Annotated[str, "门类型"] = "reference",
    m: Annotated[Any, "随机序列长度区间"] = r[0:300:20],
    k: Annotated[int, "随机序列数量"] = 20,
    tbuffer: Annotated[Any, "脉冲间隔"] = 10 * ns,
    reps: Annotated[int, "采样次数"] = 1200,
    read_delay: Annotated[Any, "读取延迟"] = 100 * ns
) -> str:
    return qcontrol_orbit_1q(
        qubit=qubit, gate=gate, m=m, k=k,
        tbuffer=tbuffer, reps=reps, read_delay=read_delay
    )

if __name__ == "__main__":
    mcp.run()