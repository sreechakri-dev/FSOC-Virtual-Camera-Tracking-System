import numpy as np

class VirtualCamera:
    """Manages the virtual camera's optical state, focal geometry, and pan/tilt actuator dynamics."""
    def __init__(self, fx=800.0, fy=800.0):
        self.fx = fx
        self.fy = fy
        self.pan_deg = 0.0
        self.tilt_deg = 0.0

    def calculate_angular_errors(self, est_cx, est_cy, screen_w, screen_h):
        """Computes true horizontal and vertical angular errors using inverse tangent geometry."""
        center_x = screen_w // 2
        center_y = screen_h // 2
        
        pixel_offset_x = est_cx - center_x
        pixel_offset_y = est_cy - center_y

        theta_x = np.arctan(pixel_offset_x / self.fx) * (180.0 / np.pi)
        theta_y = np.arctan(pixel_offset_y / self.fy) * (180.0 / np.pi)
        angular_magnitude = np.sqrt(theta_x**2 + theta_y**2)

        return theta_x, theta_y, angular_magnitude

    def update_actuation(self, theta_x, theta_y, gain=0.1):
        """Updates the persistent pan/tilt orientation of the virtual camera mount."""
        self.pan_deg += theta_x * gain
        self.tilt_deg += theta_y * gain
        return self.pan_deg, self.tilt_deg