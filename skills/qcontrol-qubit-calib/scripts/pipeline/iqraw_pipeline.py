import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
import asyncio
from labrad.units import Unit
from qcontrol.experiment.utils.range import Range, r
V, mV, us, ns, GHz, MHz, dBm, rad, uA = [
    Unit(s) for s in ("V", "mV", "us", "ns", "GHz", "MHz", "dBm", "rad", "uA")
]

# 指向 swiftmcp 启动的服务端脚本
server_params = StdioServerParameters(
    command="swiftmcp",
    args=["mcp", "mcp_tools.py"],
    env=None
)

async def main():
    # 建立连接
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("连接服务端成功")

            res = await session.call_tool(
                "iqraw",
                arguments={
                    "qubit": "qr2",
                    "pi_amp": 0.446,
                    "pi_len": 30 * ns,
                    "z_offset": 0.5,
                    "readout_freq": 6.6 * GHz,
                    "readout_power": -100 * dBm,
                    "f10": 3.984 * GHz,
                    "readout_len": 2.048 * us,
                    "adc_start_delay": r[620:650:1, ns]
                }
            )

            print(res.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())