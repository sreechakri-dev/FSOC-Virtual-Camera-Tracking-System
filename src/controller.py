import time

class SystemController:
    """Coordinates the core closed-loop tracking sequence: detection, state estimation, geometry, and actuation."""
    def __init__(self, detector, tracker, virtual_camera, disturbance_engine, metrics_logger):
        self.detector = detector
        self.tracker = tracker
        self.camera = virtual_camera
        self.disturbances = disturbance_engine
        self.logger = metrics_logger
        self.is_active = False

    def process_frame(self, frame, dist_level):
        start_time = time.time()
        h, w, _ = frame.shape
        center_x, center_y = w // 2, h // 2

        # 1. Inject environmental and platform disturbances
        disturbed_frame = self.disturbances.apply(frame, dist_level)

        # 2. Run object detection via ONNX
        detected_box, _ = self.detector.detect(disturbed_frame)

        # 3. Apply state estimation and prediction
        if detected_box:
            x1, y1, x2, y2, raw_cx, raw_cy = detected_box
            est_cx, est_cy = self.tracker.update(raw_cx, raw_cy)
            status = "Locked"
        else:
            est_cx, est_cy = self.tracker.predict()
            status = "Predictive Coasting"
            x1, y1, x2, y2 = None, None, None, None

        # 4. Calculate optical angular errors (degrees)
        theta_x, theta_y, angular_magnitude = self.camera.calculate_angular_errors(est_cx, est_cy, w, h)

        # 5. Update persistent virtual camera mount dynamics
        pan, tilt = self.camera.update_actuation(theta_x, theta_y)

        # 6. Compute execution metrics
        fps = 1.0 / (time.time() - start_time) if (time.time() - start_time) > 0 else 0.0

        # 7. Log telemetry data if target is active
        if detected_box:
            self.logger.log_row([
                time.strftime("%H:%M:%S"),
                round(fps, 1),
                int(est_cx),
                int(est_cy),
                round(theta_x, 3),
                round(theta_y, 3),
                status
            ])

        return {
            "frame": disturbed_frame,
            "detected_box": (x1, y1, x2, y2) if detected_box else None,
            "estimated_coords": (est_cx, est_cy),
            "theta_x": theta_x,
            "theta_y": theta_y,
            "angular_magnitude": angular_magnitude,
            "pan": pan,
            "tilt": tilt,
            "fps": fps,
            "status": status,
            "center": (center_x, center_y)
        }