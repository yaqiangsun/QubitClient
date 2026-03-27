# Repository Guidelines

- Repo: https://github.com/yaqiangsun/qubitclient
- In chat replies, file references must be repo-root relative only (example: `qubitclient/scope/s21_peak.py:80`); never absolute paths or `~/...`.

## Project Structure & Module Organization

- Source code: `qubitclient/` (main package)
  - `qubitclient/nnscope/` - Neural network spectrum analysis tasks
  - `qubitclient/scope/` - Traditional fitting and analysis tasks
  - `qubitclient/ctrl/` - MCP protocol-based real-time measurement control
  - `qubitclient/draw/` - Visualization and plotting utilities
  - `qubitclient/utils/` - Common utility functions
  - `qubitclient/wrapper_handler.py` - Main wrapper handler
- Tests: `tests/` directory
- Docs: `docs/` (task documentation, configuration guide)
- Examples: `examples/`

## Build, Test, and Development Commands

- Runtime: Python **3.10+** (keep compatibility with Python 3.10-3.13)
- Install deps: `pip install -e .` or `uv sync`
- Install with full features: `pip install -e .[full]`
- Install with plot features: `pip install -e .[plot]`
- Install with MCP features: `pip install -e .[mcp]`
- Build package: `python -m build` or `uv build`
- Type-check: `python -m mypy qubitclient/` (if installed)
- Format check: `python -m black --check qubitclient/`
- Format fix: `python -m black qubitclient/`
- Lint: `python -m ruff check qubitclient/`
- Run tests:
  ```bash
  python tests/test_nnscope.py
  python tests/test_scope.py
  python tests/test_ctrl_mcp.py
  ```

## Coding Style & Naming Conventions

- Language: Python (PEP 8 style)
- Prefer strict typing; avoid `Any` when possible.
- Use type hints for function signatures and variables.
- Naming: use **snake_case** for functions/variables, **PascalCase** for classes.
- Keep files concise; extract helpers when needed.
- Add brief docstrings for public APIs.
- Use f-strings for string formatting.

## Testing Guidelines

- Test files are in `tests/` directory.
- Follow the existing test patterns in `tests/`.
- When adding new features, add corresponding test cases.

## Commit & Pull Request Guidelines

- Use concise, action-oriented commit messages (e.g., `add: support for T1 fitting task`).
- Group related changes; avoid bundling unrelated refactors.
- PR submission: use GitHub's PR template if available.

## Data & Configuration

- Configuration: edit `config.py` (copy from `config.py.example`)
- Data format: see `docs/` for task-specific data format requirements
- Temporary data: `tmp/` directory (can be cleaned)

## MCP Protocol

- The `ctrl` module uses MCP (Model Context Protocol) for real-time measurement control
- MCP adapters required: install with `pip install -e .[mcp]`

## Optional Dependencies

- `plot` - matplotlib, opencv-python, plotly, scipy (for visualization)
- `mcp` - langchain-mcp-adapters (for MCP protocol support)
- `full` - includes both plot and mcp

## Documentation

- Task documentation: `docs/nnscope/`, `docs/scope/`, `docs/ctrl/`
- Configuration guide: `docs/CONFIG_GUIDE.md`
- README: `README.md` (Chinese), `README.en.md` (English)