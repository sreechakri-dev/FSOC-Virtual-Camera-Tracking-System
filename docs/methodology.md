# Technical Methodology: ISRO FSOC Virtual Camera Tracking System

## 1. Problem Definition & Operational Constraints

Free-Space Optical Communications (FSOC) systems rely on ultra-narrow laser beams to establish high-bandwidth, secure communication links between mobile terminals. Tracking high-speed targets (such as fast-moving vehicles or aerial nodes) introduces critical engineering hurdles:

* **Narrow Divergence Angles:** Even fractional misalignments in pointing vectors cause catastrophic link dropouts.
* **Inference and Latency Lag:** Neural network detection and pipeline execution introduce milliseconds of delay. At high velocities, target displacement between frame capture and mechanical actuation results in a permanent trailing error.
* **Environmental Disturbances:** Atmospheric turbulence, platform vibration, and optical blur degrade edge detection and target isolation.

---

## 2. Mathematical Formulation & Coordinate Transformation

To bridge the gap between raw screen pixels and professional aerospace metrics, the system discards pixel-only error tracking in favor of angular error geometry.

Given a detected target centroid at pixel coordinates $(x, y)$, an optical center $(c_x, c_y)$, and virtual camera focal lengths $(f_x, f_y)$, the horizontal and vertical angular errors ($\theta_x, \theta_y$) are computed using inverse trigonometric projection:

$$\theta_x = \tan^{-1}\left(\frac{x - c_x}{f_x}\right) \times \left(\frac{180}{\pi}\right)$$

$$\theta_y = \tan^{-1}\left(\frac{y - c_y}{f_y}\right) \times \left(\frac{180}{\pi}\right)$$

The total angular tracking error magnitude is then defined as:

$$\theta_{\text{mag}} = \sqrt{\theta_x^2 + \theta_y^2}$$

This converts abstract pixel counts into quantifiable physical degrees, mirroring real-world gimbal alignment specifications.

---

## 3. Predictive State Estimation (Latency Compensation)

To overcome the limitations of reactive perception (where the system acts on past coordinates), a constant-velocity kinematic estimator predicts future target states.

* **Alpha-Beta Filtering:** The estimator maintains position and velocity vectors, updating predictions using weighted residuals:
$$\hat{x}_{t\vert{}t} = \hat{x}_{t\vert{}t-1} + \alpha (z_t - \hat{x}_{t\vert{}t-1})$$


$$\hat{v}_{t\vert{}t} = \hat{v}_{t-1\vert{}t-1} + \frac{\beta}{\Delta t} (z_t - \hat{x}_{t\vert{}t-1})$$


* **Predictive Coasting:** When environmental occlusion or motion blur causes YOLOv8 to temporarily miss a detection, the tracker continues extrapolating along the established momentum vector (`predict()`), preventing control loop oscillation or lock loss.

---

## 4. Environmental Disturbance Simulation Framework

To rigorously evaluate tracking resilience, the system incorporates a parameterized disturbance engine (`disturbances.py`) capable of injecting three distinct real-world degradation factors:

1. **Platform Vibration Jitter:** Applies a random affine warp displacement ($\pm \Delta x, \pm \Delta y$) to simulate vehicle or gimbal shaking.
2. **Atmospheric Scintillation:** Adds zero-mean Gaussian noise ($\sigma$) across pixel intensity arrays to replicate signal scattering through turbulent air columns.
3. **Motion Blur:** Applies a directional convolution kernel when disturbance levels exceed critical operational thresholds.