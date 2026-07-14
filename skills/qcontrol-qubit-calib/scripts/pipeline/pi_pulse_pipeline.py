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
                "pi_pulse",
                arguments={
                    "qubit": "qr2",
                    "pi_num": 2,
                    "pi_amp": r[0.1:0.9:0.02],
                    "pi_len": 55 * ns,
                    "z_offset": 0.4,
                    "readout_freq": 6.16 * GHz,
                    "readout_power": -28 * dBm,
                    "f10": 3.98 * GHz
                }
            )
            print(res.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())