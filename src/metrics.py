import os
import csv
import time

class MetricsLogger:
    """Manages CSV telemetry recording and tracking history buffers for performance analysis."""
    def __init__(self, log_filepath="results/sample_metrics.csv", max_history=50):
        self.log_filepath = log_filepath
        self.max_history = max_history
        
        # Ensure results directory exists
        os.makedirs(os.path.dirname(self.log_filepath), exist_ok=True)
        
        self.file = None
        self.writer = None
        self._initialize_csv()

        # Telemetry History Buffers for Live Plotting
        self.time_history = []
        self.error_history = []
        self.pan_history = []
        self.tilt_history = []
        self.start_time = time.time()

    def _initialize_csv(self):
        file_exists = os.path.exists(self.log_filepath)
        self.file = open(self.log_filepath, mode="a", newline="")
        self.writer = csv.writer(self.file)
        if not file_exists:
            self.writer.writerow(["Timestamp", "FPS", "Target_X", "Target_Y", "Error_Deg_X", "Error_Deg_Y", "Status"])
            self.file.flush()

    def log_row(self, row_data):
        """Appends a telemetry record to the CSV file."""
        if self.writer and self.file:
            self.writer.writerow(row_data)
            self.file.flush()

    def update_buffers(self, error_deg, pan_val, tilt_val):
        """Updates rolling history buffers for real-time visualization."""
        elapsed = time.time() - self.start_time
        self.time_history.append(elapsed)
        self.error_history.append(error_deg)
        self.pan_history.append(pan_val)
        self.tilt_history.append(tilt_val)

        if len(self.time_history) > self.max_history:
            self.time_history.pop(0)
            self.error_history.pop(0)
            self.pan_history.pop(0)
            self.tilt_history.pop(0)

        return self.time_history, self.error_history, self.pan_history, self.tilt_history

    def close(self):
        if self.file:
            self.file.close()