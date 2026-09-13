
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

# FSOC Virtual Camera Tracker — Telemetry & Performance Metrics Report

This document presents the runtime telemetry logs captured during testing of the ISRO-focused Free Space Optical Communication (FSOC) virtual camera tracking system. The metrics below capture live vision tracking performance, frame rates, targeting coordinates, and angular pointing errors under video feed simulation conditions.

---

### Executive Performance Summary

* **Active Operating Mode:** Video Simulation Feed (`video`)
* **Tracking Status:** Active Target Acquisition & Alignment (`Aligning`)
* **Maximum Captured FPS:** `6.5` FPS
* **Minimum Captured FPS:** `1.1` FPS
* **Total Sample Records:** `21` telemetry entries

---

### Telemetry Data Log

| Timestamp | Mode | FPS | Target X | Target Y | Error Deg X (°) | Error Deg Y (°) | Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `00:43:37` | video | 6.5 | 338 | 314 | -20.682 | -3.291 | Aligning |
| `00:43:41` | video | 3.1 | 804 | 500 | 11.599 | 9.926 | Aligning |
| `00:43:47` | video | 1.2 | 1171 | 659 | 33.577 | 20.530 | Aligning |
| `00:43:48` | video | 1.1 | 1195 | 667 | 34.780 | 21.004 | Aligning |
| `00:43:49` | video | 3.6 | 1203 | 667 | 35.183 | 21.020 | Aligning |
| `00:43:50` | video | 2.2 | 1203 | 662 | 35.159 | 20.727 | Aligning |
| `00:43:50` | video | 2.3 | 1193 | 658 | 34.660 | 20.491 | Aligning |
| `00:43:50` | video | 3.7 | 1193 | 656 | 34.687 | 20.313 | Aligning |
| `00:44:29` | video | 3.2 | 996 | 447 | 24.001 | 6.255 | Aligning |
| `00:44:30` | video | 1.7 | 937 | 451 | 20.410 | 6.551 | Aligning |
| `00:44:30` | video | 2.7 | 906 | 456 | 18.422 | 6.860 | Aligning |
| `00:44:31` | video | 1.9 | 887 | 458 | 17.216 | 7.024 | Aligning |
| `00:44:32` | video | 1.1 | 878 | 461 | 16.596 | 7.213 | Aligning |
| `00:44:32` | video | 2.4 | 886 | 461 | 17.125 | 7.212 | Aligning |
| `00:44:33` | video | 1.8 | 893 | 461 | 17.601 | 7.234 | Aligning |
| `00:44:34` | video | 3.4 | 898 | 461 | 17.927 | 7.246 | Aligning |
| `00:44:34` | video | 2.8 | 901 | 461 | 18.132 | 7.266 | Aligning |
| `00:44:35` | video | 1.9 | 903 | 461 | 18.259 | 7.235 | Aligning |
| `00:44:52` | video | 3.4 | 911 | 463 | 18.760 | 7.361 | Aligning |
| `00:44:52` | video | 3.6 | 884 | 463 | 16.962 | 7.389 | Aligning |
| `00:44:53` | video | 6.3 | 863 | 464 | 15.604 | 7.450 | Aligning |

---

### Technical Observations

1. **Target Convergence:** As recorded between timestamps `00:44:29` and `00:44:53`, the target coordinates stabilize as the pointing error progressively narrows down toward baseline tracking bounds.
2. **Frame Rate Fluctuations:** The processing loop maintains active tracking frames between `1.1 FPS` and `6.5 FPS` depending on resolution load and frame complexity during active YOLOv8 object detection cycles.
3. **Alignment Status:** The tracker continuously outputs `Aligning` status as the control loop adjusts angles to compensate for simulated optical link disturbances.
