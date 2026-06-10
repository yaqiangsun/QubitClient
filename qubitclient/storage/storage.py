# -*- coding: utf-8 -*-
# Copyright (c) 2026 yaqiang.sun.
# This source code is licensed under the license found in the LICENSE file
# in the root directory of this source tree.

import json
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class StorageBackend(Enum):
    """Storage backend type."""

    LOCAL = "local"
    MEMORY = "memory"


class DataStore:
    """Data storage client for qubitclient.

    Provides a unified interface for storing and retrieving data using
    different storage backends.
    """

    def __init__(
        self,
        backend: StorageBackend = StorageBackend.LOCAL,
        root_dir: Optional[str] = None,
    ):
        self.backend = backend
        if backend == StorageBackend.LOCAL:
            self.root_dir = Path(root_dir) if root_dir else self._default_root()
        self._cache: dict[str, Any] = {}

    def _default_root(self) -> Path:
        """Get default storage root directory, relative to current working directory."""
        storage_dir = Path.cwd() / "tmp" / "db" / "result"
        storage_dir.mkdir(parents=True, exist_ok=True)
        return storage_dir

    def save(self, key: str, data: Any, fmt: str = "json") -> str:
        """Save data to storage.

        Args:
            key: Storage key (used as filename).
            data: Data to store.
            fmt: Storage format ("json", "text", "binary").

        Returns:
            Path to saved file (for LOCAL backend).
        """
        if self.backend == StorageBackend.MEMORY:
            self._cache[key] = data
            return key

        file_path = self.root_dir / f"{key}.{fmt}"
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if fmt == "json":
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif fmt == "text":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(str(data))
        else:
            with open(file_path, "wb") as f:
                f.write(data if isinstance(data, bytes) else str(data).encode())

        return str(file_path)

    def load(self, key: str, fmt: str = "json") -> Any:
        """Load data from storage.

        Args:
            key: Storage key.
            fmt: Storage format ("json", "text", "binary").

        Returns:
            Stored data.
        """
        if self.backend == StorageBackend.MEMORY:
            return self._cache.get(key)

        file_path = self.root_dir / f"{key}.{fmt}"
        if not file_path.exists():
            return None

        if fmt == "json":
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        elif fmt == "text":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            with open(file_path, "rb") as f:
                return f.read()

    def delete(self, key: str, fmt: str = "json") -> bool:
        """Delete data from storage.

        Args:
            key: Storage key.
            fmt: Storage format.

        Returns:
            True if deleted, False if not found.
        """
        if self.backend == StorageBackend.MEMORY:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

        file_path = self.root_dir / f"{key}.{fmt}"
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def exists(self, key: str, fmt: str = "json") -> bool:
        """Check if data exists in storage."""
        if self.backend == StorageBackend.MEMORY:
            return key in self._cache

        file_path = self.root_dir / f"{key}.{fmt}"
        return file_path.exists()

    def list_keys(self, pattern: str = "*") -> list[str]:
        """List all keys in storage.

        Args:
            pattern: Glob pattern for filtering keys.

        Returns:
            List of keys.
        """
        if self.backend == StorageBackend.MEMORY:
            return list(self._cache.keys())

        keys = []
        for f in self.root_dir.glob(pattern):
            keys.append(f.stem)
        return keys

    def clear(self) -> int:
        """Clear all data from storage.

        Returns:
            Number of items cleared.
        """
        if self.backend == StorageBackend.MEMORY:
            count = len(self._cache)
            self._cache.clear()
            return count

        count = 0
        for f in self.root_dir.glob("*"):
            f.unlink()
            count += 1
        return count