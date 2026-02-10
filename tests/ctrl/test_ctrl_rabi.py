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
    # 创建drive_amp参数数组，参考quark工具中的设置
    drive_amp_array = np.linspace(0.01, 0.1, 25).tolist()
    
    result = qubit_ctrl_client.run(CtrlTaskName.RABI,
                                   qubits=["Q0", "Q1"],
                                   drive_amp=drive_amp_array,
                                   width=30e-9
                                   )
    print(result)

if __name__ == "__main__":
    main()