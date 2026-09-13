import time

class FSOCPredictiveTracker:
    """Lightweight constant-velocity state estimator for target tracking, momentum extrapolation, and coasting."""
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.initialized = False
        self.last_time = time.time()

    def update(self, measured_x, measured_y):
        current_time = time.time()
        dt = current_time - self.last_time
        if dt <= 0:
            dt = 0.033

        if not self.initialized:
            self.x = measured_x
            self.y = measured_y
            self.vx = 0.0
            self.vy = 0.0
            self.initialized = True
        else:
            # Alpha-beta kinematic smoothing weights
            alpha = 0.6
            beta = 0.3
            
            pred_x = self.x + self.vx * dt
            pred_y = self.y + self.vy * dt
            
            residual_x = measured_x - pred_x
            residual_y = measured_y - pred_y
            
            self.x = pred_x + alpha * residual_x
            self.y = pred_y + alpha * residual_y
            
            self.vx += (beta * residual_x) / dt
            self.vy += (beta * residual_y) / dt

        self.last_time = current_time
        return self.x, self.y

    def predict(self):
        """Extrapolates position based on current velocity vector when target is missed."""
        return self.x + self.vx * 0.033, self.y + self.vy * 0.033