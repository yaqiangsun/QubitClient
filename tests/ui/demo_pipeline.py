# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.
#########################################################################
# Author: yaqiangsun
# Created Time: 2026/06/10
########################################################################
"""Simulate pipeline runs and stream results to the web UI in real-time.

This script mimics the behaviour of real pipeline tasks: it saves run
parameters/results to qubitclient/storage and pushes each new record to
the SSE stream so any open browser tab updates instantly.

Usage:
    # Start the web server first:
    python -m tests.ui.serve

    # Then in a separate terminal run the demo feeder:
    python -m tests.ui.demo_pipeline
"""

import os
import sys
import time
import uuid
import random
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# ---------------------------------------------------------------------------
# Demo data factories
# ---------------------------------------------------------------------------

_TASK_NAMES = ["t1", "s21multi", "ramsey", "rabi", "drag", "spinecho_t2", "xeb"]
_QUBITS = ["q1lu7", "q2lu7", "q3lu7", "q4lu7", "q5lu7"]
_PIPELINES = ["t1_pipeline", "s21multi_pipeline", "ramsey_pipeline",
              "rabi_pipeline", "drag_pipeline", "spinecho_t2_pipeline", "xeb_pipeline"]


def _make_t1_params():
    return {
        "qubits": random.sample(_QUBITS, random.randint(1, 3)),
        "delay_start": 0,
        "delay_end": random.choice([40000, 80000, 160000]),
        "delay_sample_num": random.randint(9, 21),
    }


def _make_s21multi_params():
    return {
        "qubits": random.sample(_QUBITS, 1),
        "frequency_start": 6.3,
        "frequency_end": 6.9,
        "frequency_sample_rate": 0.0001,
    }


def _make_ramsey_params():
    return {
        "qubits": random.sample(_QUBITS, random.randint(1, 2)),
        "delay_start": 0,
        "delay_end": random.choice([100, 500, 1000]),
        "delay_sample_num": random.randint(20, 100),
        "fringeFreq": round(random.uniform(0.01, 0.2), 3),
    }


def _make_rabi_params():
    return {
        "qubits": random.sample(_QUBITS, random.randint(1, 2)),
        "amp_start": 0,
        "amp_end": round(random.uniform(0.5, 2.0), 2),
        "amp_sample_num": random.randint(12, 24),
    }


def _make_drag_params():
    return {
        "qubits": random.sample(_QUBITS, random.randint(1, 2)),
        "lamb": [-0.5, 0.5],
        "stage": random.randint(1, 3),
        "N_repeat": random.randint(1, 5),
    }


_TASK_PARAM_FACTORIES = {
    "t1": _make_t1_params,
    "s21multi": _make_s21multi_params,
    "ramsey": _make_ramsey_params,
    "rabi": _make_rabi_params,
    "drag": _make_drag_params,
}


def _make_fake_analysis(task_name: str, params: dict) -> dict:
    """Generate a plausible-looking analysis result dict for demo purposes."""
    if task_name == "t1":
        return {"T1": round(random.uniform(1e4, 1e5), 1), "unit": "ns"}
    if task_name == "s21multi":
        n = len(params["qubits"])
        return {
            "results": [{
                "peaks": [[round(random.uniform(6.4, 6.8), 4)] for _ in range(n)],
                "confs": [[round(random.uniform(0.5, 1.0), 3)] for _ in range(n)],
                "freqs_list": [[round(random.uniform(6.3, 6.9), 4)] for _ in range(n)],
            }]
        }
    if task_name == "ramsey":
        return {
            "T2*": round(random.uniform(1e3, 1e4), 1),
            "fringeFreq": params.get("fringeFreq", 0.05),
        }
    if task_name == "rabi":
        return {"rabiFreq": round(random.uniform(10, 200), 2), "unit": "MHz"}
    if task_name == "drag":
        return {"optimal_lamb": round(random.uniform(-1, 1), 3)}
    return {"value": round(random.uniform(0, 1), 4)}


# ---------------------------------------------------------------------------
# Main feeder
# ---------------------------------------------------------------------------


def run_demo(n_runs: int = 20, interval: float = 2.0):
    """Simulate `n_runs` pipeline runs and save records to tmp/db/result/."""
    from qubitclient.storage.result_store import PipelineResultRecord, PipelineResultStore
    from qubitclient.storage.storage import StorageBackend

    store = PipelineResultStore(backend=StorageBackend.LOCAL)
    print(f"[demo] Submitting {n_runs} runs, output → {store._store.root_dir}")

    for i in range(n_runs):
        task_name = random.choice(_TASK_NAMES)
        pipeline = f"{task_name}_pipeline"
        params = _TASK_PARAM_FACTORIES.get(task_name, _make_t1_params)()

        # Create running record first
        record = PipelineResultRecord(
            id=uuid.uuid4().hex,
            task_name=task_name,
            task_type=pipeline,
            qubits=params.get("qubits", []),
            params=params,
            status="running",
            created_at=datetime.now(),
        )
        run_id = store.save_run(record)
        print(f"[{i+1}/{n_runs}] [{task_name}] started  id={run_id[:8]}...")

        # Simulate a short "measurement + analysis" delay
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)

        # Sometimes fail for realism
        if random.random() < 0.1:
            store.update_run(
                run_id,
                status="failed",
                error="Simulated timeout: hardware not responding",
                completed_at=datetime.now(),
            )
            print(f"[{i+1}/{n_runs}] [{task_name}] FAILED   id={run_id[:8]}...")
        else:
            analysis = _make_fake_analysis(task_name, params)
            store.update_run(
                run_id,
                status="completed",
                analysis_result=analysis,
                completed_at=datetime.now(),
            )
            print(f"[{i+1}/{n_runs}] [{task_name}] done      id={run_id[:8]}...")

        time.sleep(max(0, interval - delay))

    print("\n[demo] All runs submitted.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simulate pipeline runs for the web UI demo")
    parser.add_argument("-n", "--runs", type=int, default=20, help="Number of runs to simulate")
    parser.add_argument("-i", "--interval", type=float, default=2.0, help="Seconds between runs")
    args = parser.parse_args()

    run_demo(n_runs=args.runs, interval=args.interval)