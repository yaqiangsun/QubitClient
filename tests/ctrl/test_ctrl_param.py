import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from qubitclient.ctrl import QubitCtrlClient
from qubitclient.ctrl import CtrlTaskName

def main():
    qubit_ctrl_client = QubitCtrlClient()
    value = qubit_ctrl_client.run(CtrlTaskName.QUERY_PARAM,
                                   key="Q1",
                                   )
    print(value)
    result = qubit_ctrl_client.run(CtrlTaskName.UPDATE_PARAM,
                                   key="Q1",
                                   value=value
                                   )
    print(result)

if __name__ == "__main__":
    main()