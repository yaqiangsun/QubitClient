# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.

"""tests.ui — demo package for the pipeline result web UI.

serve.py   — start the web server (port 8581)
demo_pipeline.py — simulate live pipeline runs feeding into the store + SSE stream

Run:
    python -m tests.ui.serve        # terminal 1: start web UI
    python -m tests.ui.demo_pipeline  # terminal 2: feed simulated data
"""

__all__ = []