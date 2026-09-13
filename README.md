
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

timestamp,frame_number,fps,beacon_x,beacon_y,tracked_x,tracked_y,tracking_error,pan_angle,tilt_angle,acquisition_time_ms,jitter_x,jitter_y,motion_mode,status
00:00:01.033,1,49.8,320.5,240.0,321.2,241.1,1.45,0.01,0.01,18.76,-3,2,LINEAR,Tracking
