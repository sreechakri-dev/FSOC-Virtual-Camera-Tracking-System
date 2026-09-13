import cv2
import numpy as np
import os
import onnxruntime as ort

class FSOCDetector:
    """Handles ONNX Runtime loading and YOLOv8 inference for target detection."""
    def __init__(self, model_path="models/yolov8n.onnx", conf_threshold=0.35):
        self.conf_threshold = conf_threshold
        self.session = None
        self.input_name = None
        
        if os.path.exists(model_path):
            self.session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
            self.input_name = self.session.get_inputs()[0].name
        else:
            raise FileNotFoundError(f"Model file not found at {model_path}")

    def detect(self, frame):
        """Processes a frame through YOLOv8 ONNX and returns the best matching target box (x1, y1, x2, y2, cx, cy)."""
        if not self.session:
            return None, 0.0

        h, w, _ = frame.shape
        img_resized = cv2.resize(frame, (640, 640))
        blob = cv2.dnn.blobFromImage(img_resized, 1/255.0, (640, 640), swapRB=True, crop=False)
        
        outputs = self.session.run(None, {self.input_name: blob})
        predictions = np.squeeze(outputs[0]).T

        center_screen_x, center_screen_y = w // 2, h // 2
        best_dist = float("inf")
        detected_box = None

        for pred in predictions:
            classes_scores = pred[4:]
            max_score = np.max(classes_scores)
            if max_score > self.conf_threshold:
                x_center, y_center, box_w, box_h = pred[0], pred[1], pred[2], pred[3]
                x1 = int((x_center - box_w / 2) * (w / 640))
                y1 = int((y_center - box_h / 2) * (h / 640))
                x2 = int((x_center + box_w / 2) * (w / 640))
                y2 = int((y_center + box_h / 2) * (h / 640))
                
                obj_cx = (x1 + x2) // 2
                obj_cy = (y1 + y2) // 2
                
                dist = np.sqrt((obj_cx - center_screen_x)**2 + (obj_cy - center_screen_y)**2)
                if dist < best_dist:
                    best_dist = dist
                    detected_box = (x1, y1, x2, y2, obj_cx, obj_cy)

        return detected_box, best_dist