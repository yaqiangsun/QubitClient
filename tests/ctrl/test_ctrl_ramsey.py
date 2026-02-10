import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

def main():
    qubit_ctrl_client = QubitCtrlClient()
    result = qubit_ctrl_client.run(CtrlTaskName.RAMSEY,
                                   qubits=["Q0","Q2"],
                                   delta=20e6,
                                   delay=10e-6,
                                   stage=1,
                                   scale=15
                                   )
    print(result)

if __name__ == "__main__":
    main()