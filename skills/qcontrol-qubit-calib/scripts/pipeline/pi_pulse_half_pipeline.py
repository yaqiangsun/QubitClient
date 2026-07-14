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
                "pi_pulse_half",
                arguments={
                    "qubit": "qr2",
                    "pi_num": 3,
                    "pi_amp_half": r[1.02:1.12:0.000005]
                }
            )

            print(res.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())