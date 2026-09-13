
# ISRO FSOC Virtual Camera Tracking System

A professional, physics-based simulation and tracking pipeline engineered to address the pointing, latency, and environmental disturbance constraints of Free-Space Optical Communications (FSOC).

---

## Core Architecture

The system decouples **perception**, **state estimation**, and **optical geometry** to maintain a robust tracking lock under high-velocity conditions.

- **Inference (`detector.py`)**  
  Executes ONNX-optimized YOLOv8 inference for high-speed target localization.

- **State Estimation (`tracker.py`)**  
  Employs a constant-velocity kinematic estimator to bridge perception lag and execute predictive coasting during target occlusion.

- **Optical Geometry (`virtual_camera.py`)**  
  Converts pixel offsets into true angular coordinates (`θx`, `θy`) using inverse trigonometric projection.

- **Disturbance Simulation (`disturbances.py`)**  
  Injects parameterized platform vibration jitter, atmospheric scintillation noise, and motion blur.

- **Closed-Loop Control (`controller.py` & `main.py`)**  
  Coordinates the pipeline execution loop inside a responsive CustomTkinter interface with live telemetry logging.

---

## Directory Structure

```text
SIH26169/
├── src/
│   ├── main.py              # GUI Control Terminal & Thread Manager
│   ├── detector.py          # ONNX Runtime YOLOv8 Inference Engine
│   ├── tracker.py           # Predictive Kinematic Estimator
│   ├── virtual_camera.py    # Optical Geometry & Pan/Tilt Dynamics
│   ├── controller.py        # Closed-Loop Execution Pipeline
│   ├── disturbances.py      # Environmental Noise & Vibration Engine
│   └── metrics.py           # Telemetry Logging & History Buffers
│
├── models/
│   └── yolov8n.onnx         # Pre-trained Detection Weights
│
├── simulation/
│   └── sample.mp4           # Default Target Test Video
│
├── results/
│   └── sample_metrics.csv   # Exported Telemetry Logs
│
├── docs/
│   ├── architecture.md      # Detailed System Architecture Guide
│   └── methodology.md       # Mathematical Formulations & Physics Derivations
│
├── requirements.txt         # Project Dependencies
├── README.md                # Project Overview
└── SIH26169.exe             # Compiled Standalone Executable

## Measured Telemetry

## FSOC Tracking Telemetry

| Timestamp | Mode | FPS | Target X | Target Y | Error X (°) | Error Y (°) | Status |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | Tracking | 2.1 |  |  |  |  | Aligning |
| 2 | Tracking | 2.4 |  |  |  |  | Aligning |
| 3 | Tracking | 3.0 |  |  |  |  | Aligning |
| 4 | Tracking | 3.2 |  |  |  |  | Aligning |
| 5 | Tracking | 2.8 |  |  |  |  | Aligning |
| 6 | Tracking | 3.5 |  |  |  |  | Aligning |
| 7 | Tracking | 2.6 |  |  |  |  | Aligning |
| 8 | Tracking | 3.1 |  |  |  |  | Aligning |
| 9 | Tracking | 2.9 |  |  |  |  | Aligning |
| 10 | Tracking | 2.7 |  |  |  |  | Aligning |
| 11 | Tracking | 3.0 |  |  |  |  | Aligning |
| 12 | Tracking | 2.5 |  |  |  |  | Aligning |
| 13 | Tracking | 2.8 |  |  |  |  | Aligning |
| 14 | Tracking | 3.2 |  |  |  |  | Aligning |
| 15 | Tracking | 2.9 |  |  |  |  | Aligning |
| 16 | Tracking | 3.0 |  |  |  |  | Aligning |
| 17 | Tracking | 2.6 |  |  |  |  | Aligning |
| 18 | Tracking | 3.4 |  |  |  |  | Aligning |
| 19 | Tracking | 2.7 |  |  |  |  | Aligning |
| 20 | Tracking | 2.9 |  |  |  |  | Aligning |
| 21 | Tracking | 2.8 |  |  |  |  | Aligning |
