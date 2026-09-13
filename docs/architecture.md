# System Architecture: ISRO FSOC Virtual Camera Tracking System

## 1. Overview

The **ISRO FSOC Virtual Camera Tracking System** is architected as a modular, high-performance software simulation pipeline designed to solve the tight beam-pointing and latency constraints of Free-Space Optical Communications (FSOC). By decoupling perception, state estimation, control dynamics, and environmental disturbances, the system mirrors real-world aerospace optical tracking frameworks.

---

## 2. Modular Component Breakdown

```
SIH26169/
├── src/
│   ├── main.py              # GUI Control Terminal & Thread Manager
│   ├── detector.py          # ONNX Runtime YOLOv8 Inference Engine
│   ├── tracker.py           # Predictive Kinematic Estimator (Kalman/Alpha-Beta)
│   ├── virtual_camera.py    # Optical Geometry & Pan/Tilt Actuation Dynamics
│   ├── controller.py        # Central Closed-Loop Execution Pipeline
│   ├── disturbances.py      # Real-Time Environmental Noise & Vibration Engine
│   └── metrics.py           # Telemetry Logging & History Buffers

```

* **`main.py`**: Initializes the CustomTkinter operational dashboard, handles thread-safe execution loops, and binds interactive UI controls (live camera or MP4 simulation, disturbance sliders).
* **`detector.py`**: Loads the pre-trained `yolov8n.onnx` model via ONNX Runtime. Preprocesses incoming frames (resizing, normalization, blob conversion) and extracts target bounding boxes with configurable confidence thresholds.
* **`tracker.py`**: Implements a constant-velocity kinematic state estimator. Bridges perception latency and high-speed motion by predicting target trajectories and managing predictive coasting during temporary occlusions.
* **`virtual_camera.py`**: Manages simulated optical parameters (focal lengths $f_x, f_y$) and translates pixel offsets into true angular errors ($\theta_x, \theta_y$ in degrees) using inverse tangent geometry. Maintains persistent pan/tilt mount states.
* **`controller.py`**: Acts as the system coordinator, executing the closed-loop pipeline sequence from frame ingestion to telemetry generation.
* **`disturbances.py`**: Simulates real-world operational stressors including atmospheric Gaussian turbulence, platform vibration jitter, and motion blur controlled via an interactive UI slider.
* **`metrics.py`**: Handles asynchronous CSV telemetry logging (`results/sample_metrics.csv`) and manages rolling history buffers for real-time Matplotlib visualization.

---

## 3. Execution Data Flow

1. **Ingestion**: A raw frame is captured from the active video source or webcam stream.
2. **Disturbance Injection**: The `DisturbanceEngine` applies parameterized noise, jitter, and blur to simulate harsh propagation environments.
3. **Detection**: The `FSOCDetector` runs ONNX inference to locate target coordinates relative to the optical center.
4. **State Estimation**: The `FSOCPredictiveTracker` refines coordinates using velocity extrapolation to compensate for processing lag.
5. **Geometry & Actuation**: The `VirtualCamera` calculates angular pointing errors ($\theta_x, \theta_y$) and updates mount angles.
6. **Logging & Visualization**: `MetricsLogger` writes performance records to disk and updates the live UI telemetry HUD and error charts.