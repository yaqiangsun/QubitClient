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
    # 创建频率和偏置参数数组，参考quark工具中的设置
    freq_array = (np.arange(3.6, 4.8, 0.002) * 1e9).tolist()
    bias_array = np.linspace(-0.8, 0.8, 21).tolist()
    
    result = qubit_ctrl_client.run(CtrlTaskName.SPECTRUM_2D,
                                   qubits=["Q0", "Q2"],
                                   drive_amp=0.05,
                                   duration=40e-6,
                                   freq=freq_array,
                                   bias=bias_array,
                                   from_idle=False,
                                   absolute=True
                                   )
    print(result)

if __name__ == "__main__":
    main()