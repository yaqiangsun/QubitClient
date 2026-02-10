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
    # 创建频率参数数组，参考quark工具中的设置
    freq_array = (np.arange(3.8, 4.6, 0.02) * 1e9).tolist()
    
    result = qubit_ctrl_client.run(CtrlTaskName.SPECTRUM,
                                   qubits=["Q0"],
                                   freq=freq_array,
                                   drive_amp=0.04,
                                   duration=40e-6,
                                   from_idle=True,
                                   absolute=True,
                                   signal="iq_avg",
                                   build_dependencies=False
                                   )
    print(result)

if __name__ == "__main__":
    main()