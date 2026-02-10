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
    # 创建lambda参数数组，参考quark工具中的设置
    lamb_array = (np.linspace(-5, 5, 25) / (250e6)).tolist()
    
    result = qubit_ctrl_client.run(CtrlTaskName.DRAG,
                                   qubits=["Q0", "Q2"],
                                   lamb=lamb_array,
                                   stage=1,
                                   N_repeat=1,
                                   pulsePair=[0, 1]
                                   )
    print(result)

if __name__ == "__main__":
    main()