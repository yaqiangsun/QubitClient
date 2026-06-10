# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/10
########################################################################
"""Start the pipeline result web UI server.

Usage:
    python -m tests.ui.serve
    # or
    uvicorn qubitclient.ui:app --reload --port 8000

The server will be available at http://localhost:8000
"""

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="QubitClient Pipeline Result Web UI")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind (default: 8000)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    args = parser.parse_args()

    try:
        import uvicorn
        from qubitclient.ui import app

        print(f"Starting QubitClient Pipeline UI at http://{args.host}:{args.port}/")
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            reload=args.reload,
        )
    except ImportError:
        print("Error: fastapi/uvicorn not installed.")
        print("Run: pip install -e '.[ui]'")
        sys.exit(1)


if __name__ == "__main__":
    main()