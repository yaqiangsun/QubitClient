# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/04/21 13:21:34
########################################################################

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