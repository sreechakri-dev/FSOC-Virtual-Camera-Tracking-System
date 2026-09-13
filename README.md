
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

The following values were obtained from a recorded FSOC tracking telemetry run.

| Metric | Measured Value |
|---|---:|
| Telemetry Records | 21 |
| Average FPS | 2.85 FPS |
| Maximum FPS | 6.50 FPS |
| Minimum FPS | 1.10 FPS |
| Average Horizontal Angular Error | 20.76° |
| Average Vertical Angular Error | 10.62° |
| Horizontal Error Range | −20.68° to +35.18° |
| Vertical Error Range | −3.29° to +21.02° |
| Locked Frames | 0 / 21 |
| Aligning Frames | 21 / 21 |

### Tracking Status

During this recorded run:

```text
Total Telemetry Records : 21
Locked Frames           : 0
Aligning Frames         : 21
Lock Rate               : 0%
