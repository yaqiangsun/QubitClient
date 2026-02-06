import os
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

def main():
    qubit_ctrl_client = QubitCtrlClient()
    result = qubit_ctrl_client.run(CtrlTaskName.S21,
                                    qubits_use=["Q0","Q1"],
                                    frequency_start=-40e6,
                                    frequency_end=40e6,
                                    frequency_sample_num=101
                                   )
    print(result)

if __name__ == "__main__":
    main()