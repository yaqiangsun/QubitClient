# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.

import asyncio
import json
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from contextlib import asynccontextmanager

from qubitclient.storage.result_store import PipelineResultStore

# ---------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------

_sse_queues: list[asyncio.Queue[bytes]] = []
_seen_ids: set[str] = set()


# ---------------------------------------------------------------------------
# Directory watcher
# ---------------------------------------------------------------------------

async def _watch_directory() -> None:
    """Scan tmp/db/result/pipeline/ every 2s, broadcast new records via SSE."""
    project_root = Path(__file__).parent.parent.parent
    pipeline_dir = project_root / "tmp" / "db" / "result" / "pipeline"
    pipeline_dir.mkdir(parents=True, exist_ok=True)
    print(f"[watcher] scanning: {pipeline_dir}")

    # Seed seen set with existing files
    for f in sorted(pipeline_dir.glob("*.json")):
        _seen_ids.add(f.stem)
    print(f"[watcher] seed {len(_seen_ids)} existing files, queues={len(_sse_queues)}")

    while True:
        for fpath in sorted(pipeline_dir.glob("*.json")):
            if fpath.stem in _seen_ids:
                continue
            _seen_ids.add(fpath.stem)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    record = json.load(f)
                payload = f"data: {json.dumps(record)}\n\n".encode()
                dead = []
                for q in _sse_queues:
                    try:
                        q.put_nowait(payload)
                    except Exception:
                        dead.append(q)
                for q in dead:
                    _sse_queues.remove(q)
                print(f"[watcher] broadcasted: {fpath.stem}, queues={len(_sse_queues)}")
            except Exception as e:
                print(f"[watcher] error: {e}")
        await asyncio.sleep(2)


# ---------------------------------------------------------------------------
# Lifespan — start/stop watcher
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(_: FastAPI):
    task = asyncio.create_task(_watch_directory())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    _sse_queues.clear()


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(title="QubitClient Pipeline UI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the main page."""
    project_root = Path(__file__).parent.parent.parent
    tpl = project_root / "qubitclient" / "ui" / "templates" / "index.html"
    return FileResponse(tpl)


@app.get("/api/runs")
async def list_runs(task_name: str | None = None, limit: int = 100, offset: int = 0):
    """List all run records, newest first."""
    store = PipelineResultStore()
    records, total = store.list_runs(task_name=task_name, limit=limit, offset=offset)
    items = []
    for r in records:
        d = r.model_dump(mode="json")
        if isinstance(d.get("created_at"), datetime):
            d["created_at"] = d["created_at"].isoformat()
        if isinstance(d.get("completed_at"), datetime) and d["completed_at"]:
            d["completed_at"] = d["completed_at"].isoformat()
        items.append(d)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@app.delete("/api/runs/{run_id}")
async def delete_run(run_id: str):
    store = PipelineResultStore()
    if not store.delete_run(run_id):
        raise HTTPException(status_code=404, detail="Not found")
    return {"ok": True}


@app.get("/api/plots/{run_id}/{plot_index}")
async def get_plot(run_id: str, plot_index: int):
    store = PipelineResultStore()
    path = store.get_plot_path(run_id, plot_index)
    if not path:
        raise HTTPException(status_code=404, detail="Plot not found")
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = Path(__file__).parent.parent.parent / path
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="image/png")


@app.get("/api/stream")
async def stream():
    """Server-Sent Events — pushes new records as they appear in tmp/db/result/."""
    q: asyncio.Queue[bytes] = asyncio.Queue()
    _sse_queues.append(q)

    async def gen():
        try:
            while True:
                data = await q.get()
                yield data
        except asyncio.CancelledError:
            _sse_queues.remove(q)
            raise

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/task-names")
async def list_task_names():
    store = PipelineResultStore()
    records, _ = store.list_runs(limit=10000)
    names = sorted({r.task_name for r in records if r.task_name})
    return {"task_names": names}