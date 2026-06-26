---
name: qubitclient
description: "Unified quantum calibration analysis package. Aggregates: (1) qubitclient-scope — numerical curve fitting and parameter extraction (S21 peak, T1/T2, Rabi, DRAG, RB, etc.), (2) qubitclient-nnscope — neural network based spectrum analysis (S21 peak, spectrum 2D, S21 vs Flux), (3) qubitclient-vqa-review — LLM-based analysis and review for calibration results, (4) qubitclient-control — MCP protocol-based real-time measurement control. Provides a single entry point for all quantum experiment data analysis tasks."
license: Proprietary. LICENSE.txt has complete terms
includes:
  - name: qubitclient-scope
    description: "Traditional numerical fitting and analysis tasks for quantum calibration"
  - name: qubitclient-nnscope
    description: "Neural network based analysis tasks for spectrum and curve segmentation"
  - name: qubitclient-vqa-review
    description: "LLM-based visual question answering and analysis review"
  - name: qubitclient-control
    description: "Real-time measurement control via MCP protocol"
---

## Overview

`qubitclient` is the unified Python package for quantum calibration data analysis. It combines traditional curve fitting, neural network analysis, LLM review, and real-time measurement control into a single, coherent system.

## Sub-Skills

### qubitclient-scope

Numerical curve fitting and parameter extraction for quantum experiments.

**Key capabilities:**
- S21 peak detection (single/multi-peak)
- T1/T2 relaxation time fitting
- Rabi oscillation analysis
- DRAG pulse optimization
- Randomized Benchmarking (RB)
- Single-shot readout fidelity
- Power shift characterization

### qubitclient-nnscope

Neural network based analysis for spectrum and curve segmentation.

**Key capabilities:**
- S21 peak detection with deep learning
- 2D spectrum segmentation (COSINE, POLY curve types)
- S21 vs Flux parameter curve extraction
- Power shift curve segmentation

### qubitclient-vqa-review

LLM-powered visual question answering for quantum calibration results.

**Key capabilities:**
- Automated analysis review
- Calibration result interpretation
- Visual inspection of measurement data

### qubitclient-control

Real-time measurement control via MCP (Model Context Protocol).

**Key capabilities:**
- Live measurement streaming
- Parameter updates during measurement
- Automated calibration workflows

## Usage

```python
# Scope tasks (numerical fitting)
from qubitclient import QubitScopeClient, TaskName
client = QubitScopeClient()

# NNScope tasks (neural network)
from qubitclient import QubitNNScopeClient, NNTaskName, CurveType
nn_client = QubitNNScopeClient()

# MCP Control tasks
from qubitclient.ctrl import MCPClient
mcp_client = MCPClient()
```

## Task Categories

| Category | Module | Tasks |
|----------|--------|-------|
| Spectroscopy | scope / nnscope | S21PEAK, S21PEAKMULTI, SPECTRUM, SPECTRUM2D |
| Relaxation | scope | T1FIT, T2FIT, SPINECHO, T12DFIT |
| Pulse | scope | OPTPIPULSE, RABICOS, DRAG, TIMINGXYZ |
| Flux | scope / nnscope | S21VSFLUX, POWERSHIFT |
| Readout | scope | SINGLESHOT, OPTREADFREQ |
| Benchmarking | scope | RB, DELTA |
| Control | control | Real-time measurement control |
| Review | vqa-review | LLM-based analysis review |