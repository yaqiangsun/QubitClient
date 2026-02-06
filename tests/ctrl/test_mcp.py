# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/02/06 11:56:43
########################################################################
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from qubitclient.ctrl import MCPClient

def main():
    mcp = MCPClient(mcpServers=None)
    result = mcp.call("s21", {
                        "qubits_use":["Q0","Q1"],
                        "frequency_start":-40e6,
                        "frequency_end":40e6,
                        "frequency_sample_num":101
                    }
            )
    print(result)
if __name__ == "__main__":
    main()