# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from qubitclient.storage.storage import DataStore, StorageBackend


class ParamUpdate(BaseModel):
    """Record of a single parameter update."""

    param_name: str = ""
    old_value: Any = None
    new_value: Any = None


class PipelineResultRecord(BaseModel):
    """Schema for a single pipeline run record."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    task_name: str = ""  # CtrlTaskName.value e.g. "t1", "s21multi"
    task_type: str = ""  # pipeline filename e.g. "t1_pipeline"
    qubits: list[str] = Field(default_factory=list)
    params: dict[str, Any] = Field(default_factory=dict)
    raw_data: Any = None
    raw_data_id: str = ""  # ID of the original raw data
    analysis_result: Any = None
    plot_paths: list[str] = Field(default_factory=list)
    status: str = "running"  # "running" | "completed" | "failed"
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    # Parameter update tracking
    original_params: dict[str, Any] = Field(default_factory=dict)  # params before any update
    param_updates: list[ParamUpdate] = Field(default_factory=list)  # history of param changes


class PipelineResultStore:
    """Storage client for pipeline run results.

    Wraps :class:`DataStore` with a structured schema for pipeline
    parameters, raw data, analysis results, and plot paths.
    """

    def __init__(
        self,
        backend: StorageBackend = StorageBackend.LOCAL,
        root_dir: Optional[str] = None,
    ):
        self._store = DataStore(backend=backend, root_dir=root_dir)

    def _key(self, run_id: str) -> str:
        return f"pipeline/{run_id}"

    def save_run(self, record: PipelineResultRecord) -> str:
        """Save a new pipeline run record.

        Args:
            record: The pipeline result record to save.

        Returns:
            The run_id of the saved record.
        """
        self._store.save(self._key(record.id), record.model_dump(mode="json"), fmt="json")
        return record.id

    def update_run(
        self,
        run_id: str,
        *,
        status: Optional[str] = None,
        raw_data: Any = None,
        raw_data_id: Optional[str] = None,
        analysis_result: Any = None,
        plot_paths: Optional[list[str]] = None,
        error: Optional[str] = None,
        completed_at: Optional[datetime] = None,
        new_params: Optional[dict[str, Any]] = None,
    ) -> bool:
        """Update fields of an existing pipeline run record.

        Args:
            run_id: The run ID to update.
            status: New status value.
            raw_data: New raw data.
            raw_data_id: ID of the original raw data.
            analysis_result: New analysis result.
            plot_paths: New plot paths list.
            error: Error message if failed.
            completed_at: Completion timestamp.
            new_params: New params dict — if provided, diff vs original_params is
                recorded in param_updates.

        Returns:
            True if the record was found and updated, False otherwise.
        """
        record = self.get_run(run_id)
        if record is None:
            return False

        if status is not None:
            record.status = status
        if raw_data is not None:
            record.raw_data = raw_data
        if raw_data_id is not None:
            record.raw_data_id = raw_data_id
        if analysis_result is not None:
            record.analysis_result = analysis_result
        if plot_paths is not None:
            record.plot_paths = plot_paths
        if error is not None:
            record.error = error
        if completed_at is not None:
            record.completed_at = completed_at
        if new_params is not None:
            if not record.original_params:
                record.original_params = dict(record.params)
            for k, new_val in new_params.items():
                old_val = record.params.get(k)
                if old_val != new_val:
                    record.param_updates.append(ParamUpdate(param_name=k, old_value=old_val, new_value=new_val))
            record.params = new_params

        self._store.save(self._key(run_id), record.model_dump(mode="json"), fmt="json")
        return True

    def get_run(self, run_id: str) -> Optional[PipelineResultRecord]:
        """Load a pipeline run record by ID.

        Args:
            run_id: The run ID to load.

        Returns:
            The record if found, None otherwise.
        """
        data = self._store.load(self._key(run_id), fmt="json")
        if data is None:
            return None
        return PipelineResultRecord(**data)

    def list_runs(
        self,
        task_name: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[PipelineResultRecord], int]:
        """List pipeline run records with optional task_name filter.

        Args:
            task_name: If provided, only return runs of this task type.
            limit: Maximum number of records to return.
            offset: Number of records to skip.

        Returns:
            A tuple of (list of records, total count matching filter).
        """
        all_keys = self._store.list_keys(pattern="pipeline/*")
        records: list[PipelineResultRecord] = []
        for key in all_keys:
            # key is like "pipeline/{id}"
            run_id = key.split("/", 1)[1] if "/" in key else key
            record = self.get_run(run_id)
            if record is None:
                continue
            if task_name and record.task_name != task_name:
                continue
            records.append(record)

        # Sort by created_at descending
        records.sort(key=lambda r: r.created_at, reverse=True)

        total = len(records)
        paginated = records[offset : offset + limit]
        return paginated, total

    def delete_run(self, run_id: str) -> bool:
        """Delete a pipeline run record.

        Args:
            run_id: The run ID to delete.

        Returns:
            True if deleted, False if not found.
        """
        return self._store.delete(self._key(run_id), fmt="json")

    def get_plot_path(self, run_id: str, plot_index: int = 0) -> Optional[str]:
        """Get the path to a specific plot file for a run.

        Args:
            run_id: The run ID.
            plot_index: Index of the plot in the plot_paths list.

        Returns:
            Path string if found, None otherwise.
        """
        record = self.get_run(run_id)
        if record is None or plot_index >= len(record.plot_paths):
            return None
        return record.plot_paths[plot_index]