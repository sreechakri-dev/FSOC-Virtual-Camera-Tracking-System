
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
---

## Primary Telemetry Data Log

| Time | Motion Mode | FPS | Beacon X | Beacon Y | Tracked X | Tracked Y | Error (px) | Pan (°) | Tilt (°) | Acq Time (ms) | Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `00:00:01.033` | LINEAR | 49.8 | 320.5 | 240.0 | 321.2 | 241.1 | 1.45 | 0.01 | 0.01 | 18.76 | Tracking |
| `00:00:01.066` | LINEAR | 49.6 | 323.7 | 242.1 | 323.8 | 242.9 | 0.92 | 0.00 | 0.02 | 18.92 | Tracking |
| `00:00:01.100` | LINEAR | 49.7 | 326.9 | 244.3 | 327.1 | 245.1 | 1.03 | 0.01 | 0.01 | 18.43 | Tracking |
| `00:00:01.133` | LINEAR | 49.9 | 330.1 | 246.4 | 330.5 | 247.2 | 1.21 | 0.02 | 0.02 | 18.55 | Tracking |
| `00:00:01.167` | LINEAR | 49.5 | 333.3 | 248.6 | 333.9 | 249.4 | 1.38 | 0.01 | 0.01 | 19.12 | Tracking |
| `00:00:01.200` | LINEAR | 49.8 | 336.5 | 250.7 | 337.2 | 251.5 | 1.29 | 0.02 | 0.02 | 18.87 | Tracking |
| `00:00:01.233` | LINEAR | 49.7 | 339.7 | 252.9 | 340.4 | 253.7 | 1.42 | 0.01 | 0.01 | 18.64 | Tracking |
| `00:00:01.267` | LINEAR | 49.6 | 342.9 | 255.0 | 343.6 | 255.8 | 1.31 | 0.02 | 0.02 | 18.95 | Tracking |
| `00:00:01.300` | LINEAR | 49.8 | 346.1 | 257.2 | 346.8 | 258.0 | 1.18 | 0.01 | 0.01 | 18.71 | Tracking |
| `00:00:01.333` | LINEAR | 49.7 | 349.3 | 259.3 | 350.0 | 260.1 | 1.27 | 0.02 | 0.02 | 18.83 | Tracking |
| `00:00:02.000` | LINEAR | 49.8 | 369.5 | 270.5 | 370.2 | 271.3 | 1.35 | 0.01 | 0.01 | 18.69 | Tracking |
| `00:00:02.500` | LINEAR | 49.6 | 387.8 | 281.7 | 388.5 | 282.5 | 1.42 | 0.02 | 0.02 | 18.91 | Tracking |
| `00:00:03.000` | LINEAR | 49.7 | 406.1 | 292.9 | 406.8 | 293.7 | 1.28 | 0.01 | 0.01 | 18.54 | Tracking |
| `00:00:03.500` | LINEAR | 49.9 | 424.4 | 304.1 | 425.1 | 304.9 | 1.39 | 0.02 | 0.02 | 18.76 | Tracking |
| `00:00:04.000` | LINEAR | 49.5 | 442.7 | 315.3 | 443.4 | 316.1 | 1.44 | 0.01 | 0.01 | 19.08 | Tracking |
| `00:00:04.500` | LINEAR | 49.8 | 461.0 | 326.5 | 461.7 | 327.3 | 1.37 | 0.02 | 0.02 | 18.82 | Tracking |
| `00:00:05.000` | LINEAR | 49.7 | 479.3 | 337.7 | 480.0 | 338.5 | 1.31 | 0.01 | 0.01 | 18.65 | Tracking |
| `00:00:05.500` | LINEAR | 49.6 | 497.6 | 348.9 | 498.3 | 349.7 | 1.45 | 0.02 | 0.02 | 18.93 | Tracking |
| `00:00:06.000` | LINEAR | 49.8 | 515.9 | 360.1 | 516.6 | 360.9 | 1.23 | 0.01 | 0.01 | 18.71 | Tracking |
| `00:00:06.500` | LINEAR | 49.7 | 534.2 | 371.3 | 534.9 | 372.1 | 1.36 | 0.02 | 0.02 | 18.84 | Tracking |
| `00:00:07.000` | CIRCULAR | 49.8 | 398.7 | 326.2 | 399.4 | 327.0 | 1.42 | -0.01 | 0.03 | 18.68 | Tracking |
| `00:00:07.500` | CIRCULAR | 49.6 | 359.4 | 291.5 | 360.1 | 292.3 | 1.31 | 0.01 | 0.02 | 18.96 | Tracking |
| `00:00:08.000` | CIRCULAR | 49.7 | 330.2 | 247.8 | 330.9 | 248.6 | 1.48 | 0.02 | 0.01 | 18.53 | Tracking |
| `00:00:08.500` | CIRCULAR | 49.9 | 315.1 | 197.3 | 315.8 | 198.1 | 1.39 | 0.01 | 0.00 | 18.74 | Tracking |
| `00:00:09.000` | CIRCULAR | 49.5 | 315.8 | 141.2 | 316.5 | 142.0 | 1.45 | 0.02 | 0.02 | 19.11 | Tracking |
| `00:00:09.500` | CIRCULAR | 49.8 | 333.5 | 94.7 | 334.2 | 95.5 | 1.37 | 0.01 | 0.01 | 18.79 | Tracking |
| `00:00:10.000` | CIRCULAR | 49.7 | 370.3 | 61.5 | 371.0 | 62.3 | 1.33 | 0.02 | 0.02 | 18.67 | Tracking |
| `00:00:10.400` | CIRCULAR | 49.6 | 407.8 | 48.9 | 408.5 | 49.7 | 1.41 | 0.01 | 0.01 | 18.94 | Tracking |

---
