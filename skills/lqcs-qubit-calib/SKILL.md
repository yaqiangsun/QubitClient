---
name: lqcs-qubit-calib
description: "LQCS (Large Quantum Calibration System) measurement pipeline for qubit calibration, including: (1) S21 multi-tone and peak spectroscopy, (2) Power shift analysis, (3) S21 vs Flux measurement, (4) Spectrum and 2D spectrum, (5) Single-shot readout, (6) Rabi oscillation, (7) PiPulseF10 calibration, (8) Ramsey interferometry, (9) Optimal qubit read frequency, (10) Optimal pi-pulse, (11) TimingXYZ calibration, (12) PulseShape optimization, (13) T1 and T1_2D relaxation, (14) SpinEcho T2, (15) Ramsey T2, and (16) XEB gate fidelity. Full measurement workflow with parameter update support for automated qubit characterization"
license: Proprietary. LICENSE.txt has complete terms
dependencies:
  - name: qubitclient-scope
    description: "Traditional fitting and analysis tasks (peak spectroscopy, power shift, S21 vs Flux, T1, T2, Rabi, etc.)"
  - name: qubitclient-nnscope
    description: "Neural network spectrum analysis tasks (S21 peak fitting, spectrum analysis)"
  - name: qubitclient-vqa-review
    description: "LLM-based analysis and review for quantum calibration results"
  - name: qubitclient-control
    description: "MCP protocol-based real-time measurement control interface"
---