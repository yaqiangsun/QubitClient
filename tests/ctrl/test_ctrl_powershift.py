import os
import sys
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

def main():
    qubit_ctrl_client = QubitCtrlClient()
    # 创建测试参数，参考quark工具中的设置
    power_array = np.linspace(-30, -10, 21).tolist()  # 功率范围
    freq_array = np.linspace(-50e6, 50e6, 101).tolist()  # 频率范围
    
    result = qubit_ctrl_client.run(CtrlTaskName.POWERSHIFT,
                                  qubits=["Q0", "Q2"],
                                  power=power_array,
                                  freq=freq_array
                                  )
    print(result)

if __name__ == "__main__":
    main()