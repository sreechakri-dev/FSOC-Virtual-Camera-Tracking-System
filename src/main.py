import cv2
import numpy as np
import onnxruntime as ort
import time
import csv
import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize CustomTkinter appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SimpleKalmanTracker:
    """Lightweight constant-velocity state estimator for target tracking and prediction."""
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
        return self.x + self.vx * 0.033, self.y + self.vy * 0.033

class FSOCControlTerminal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Virtual Camera Tracking System for Mobile FSOC Terminals")
        self.geometry("1280x880")
        self.minsize(1100, 780)

        self.is_running = False
        self.cap = None
        self.session = None
        self.mode = "camera"
        self.video_path = ""
        
        self.tracker = SimpleKalmanTracker()
        self.cam_pan_deg = 0.0
        self.cam_tilt_deg = 0.0
        self.fx = 800.0
        self.fy = 800.0

        self.time_history = []
        self.error_history = []
        self.pan_history = []
        self.tilt_history = []
        self.start_wall_time = time.time()

        self.model_path = "yolov8n.onnx"
        if os.path.exists(self.model_path):
            self.session = ort.InferenceSession(self.model_path, providers=["CPUExecutionProvider"])
        
        self.title_label = ctk.CTkLabel(self, text="AI VIRTUAL CAMERA TRACKING SYSTEM FOR MOBILE FSOC TERMINALS", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        self.workspace_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.workspace_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.left_panel = ctk.CTkFrame(self.workspace_frame, width=280, corner_radius=8)
        self.left_panel.pack(side="left", fill="y", padx=5, pady=5)
        self.left_panel.pack_propagate(False)
        
        ctk.CTkLabel(self.left_panel, text="Target & Simulation Controls", font=("Arial", 14, "bold")).pack(anchor="w", padx=15, pady=10)
        
        self.btn_camera = ctk.CTkButton(self.left_panel, text="Start Live Camera", fg_color="#1f538d", command=lambda: self.start_tracking("camera"))
        self.btn_camera.pack(padx=15, pady=6, fill="x")

        self.btn_video = ctk.CTkButton(self.left_panel, text="Select & Run MP4 Simulation", fg_color="#2b8a3e", command=self.select_and_run_video)
        self.btn_video.pack(padx=15, pady=6, fill="x")

        self.btn_stop = ctk.CTkButton(self.left_panel, text="Stop Terminal", fg_color="#c92a2a", state="disabled", command=self.stop_tracking)
        self.btn_stop.pack(padx=15, pady=6, fill="x")

        ctk.CTkLabel(self.left_panel, text="Disturbance Injection Level", font=("Arial", 12, "bold")).pack(anchor="w", padx=15, pady=(20, 5))
        self.dist_slider = ctk.CTkSlider(self.left_panel, from_=0.0, to=100.0, number_of_steps=20)
        self.dist_slider.set(10.0)
        self.dist_slider.pack(padx=15, pady=5, fill="x")
        
        self.dist_label = ctk.CTkLabel(self.left_panel, text="Current Disturbance: 10%", font=("Consolas", 11))
        self.dist_label.pack(anchor="w", padx=15, pady=2)
        self.dist_slider.configure(command=self.update_disturbance_label)

        self.btn_clear_cache = ctk.CTkButton(self.left_panel, text="Clear Session Cache", fg_color="#D9534F", hover_color="#C9302C", command=self.clear_cache_action)
        self.btn_clear_cache.pack(padx=15, pady=(30, 6), fill="x")

        self.right_panel = ctk.CTkFrame(self.workspace_frame, fg_color="transparent")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.video_frame = ctk.CTkFrame(self.right_panel, width=640, height=360, corner_radius=8)
        self.video_frame.pack(pady=5)
        self.video_frame.pack_propagate(False)

        self.video_label = ctk.CTkLabel(self.video_frame, text="[ System Offline - Select Mode to Initialize ]", font=("Arial", 14))
        self.video_label.pack(expand=True, fill="both")

        self.graph_frame = ctk.CTkFrame(self.right_panel, height=200, corner_radius=8)
        self.graph_frame.pack(fill="x", pady=5)
        self.graph_frame.pack_propagate(False)

        self.setup_matplotlib_plots()

        self.status_box = ctk.CTkTextbox(self, height=65, font=("Consolas", 11))
        self.log_message("System Initialized with Corrected NumPy Random Engine.")
        self.status_box.pack(fill="x", padx=20, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_disturbance_label(self, val):
        self.dist_label.configure(text=f"Current Disturbance: {int(val)}%")

    def setup_matplotlib_plots(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(7, 2.0), facecolor="#2b2b2b")
        self.fig.tight_layout(pad=1.2)

        for ax in (self.ax1, self.ax2):
            ax.set_facecolor("#1e1e1e")
            ax.tick_params(colors="white", labelsize=8)
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            for spine in ax.spines.values():
                spine.set_edgecolor("#555555")

        self.ax1.set_title("Angular Tracking Error Magnitude (deg)", fontsize=9, color="cyan", pad=2)
        self.line1, = self.ax1.plot([], [], color="#00ffcc", linewidth=1.5)
        self.ax1.set_ylim(0, 5.0)

        self.ax2.set_title("Virtual Camera Pan / Tilt Angles (°)", fontsize=9, color="magenta", pad=2)
        self.line_pan, = self.ax2.plot([], [], color="#00bfff", label="Pan", linewidth=1.2)
        self.line_tilt, = self.ax2.plot([], [], color="#ff69b4", label="Tilt", linewidth=1.2)
        self.ax2.set_ylim(-20, 20)

        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas_plot.get_tk_widget().pack(fill="both", expand=True)

    def update_telemetry_plot(self, error_deg, pan_val, tilt_val):
        elapsed = time.time() - self.start_wall_time
        self.time_history.append(elapsed)
        self.error_history.append(error_deg)
        self.pan_history.append(pan_val)
        self.tilt_history.append(tilt_val)

        if len(self.time_history) > 50:
            self.time_history.pop(0)
            self.error_history.pop(0)
            self.pan_history.pop(0)
            self.tilt_history.pop(0)

        self.line1.set_data(self.time_history, self.error_history)
        if len(self.time_history) > 1:
            self.ax1.set_xlim(self.time_history[0], self.time_history[-1] + 0.1)

        self.line_pan.set_data(self.time_history, self.pan_history)
        self.line_tilt.set_data(self.time_history, self.tilt_history)
        if len(self.time_history) > 1:
            self.ax2.set_xlim(self.time_history[0], self.time_history[-1] + 0.1)

        self.canvas_plot.draw()

    def apply_disturbances(self, frame, level_pct):
        if level_pct <= 0:
            return frame
        
        factor = level_pct / 100.0
        h, w, _ = frame.shape

        max_shift = int(15 * factor)
        # FIXED: Using np.random.randint instead of np.randint
        shift_x = int(np.random.randint(-max_shift, max_shift + 1)) if max_shift > 0 else 0
        shift_y = int(np.random.randint(-max_shift, max_shift + 1)) if max_shift > 0 else 0
        
        M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
        frame = cv2.warpAffine(frame, M, (w, h))

        noise_sigma = 35.0 * factor
        gauss = np.random.normal(0, noise_sigma, frame.shape).astype(np.int16)
        noisy_frame = np.clip(frame.astype(np.int16) + gauss, 0, 255).astype(np.uint8)

        if factor > 0.4:
            kernel_size = int(5 * factor)
            if kernel_size % 2 == 0:
                kernel_size += 1
            kernel = np.zeros((kernel_size, kernel_size))
            kernel[int(kernel_size//2), :] = 1.0 / kernel_size
            noisy_frame = cv2.filter2D(noisy_frame, -1, kernel)

        return noisy_frame

    def log_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.status_box.insert("end", f"[{timestamp}] {message}\n")
        self.status_box.see("end")

    def select_and_run_video(self):
        file_path = filedialog.askopenfilename(
            title="Select Simulation Video File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv"), ("All Files", "*.*")]
        )
        if file_path:
            self.video_path = file_path
            self.start_tracking("video")

    def start_tracking(self, mode):
        if not self.session:
            messagebox.showerror("Error", "Model file 'yolov8n.onnx' missing in directory!")
            return

        if self.is_running:
            self.stop_tracking()

        self.mode = mode
        self.is_running = True
        self.btn_camera.configure(state="disabled")
        self.btn_video.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.btn_clear_cache.configure(state="disabled")

        if self.mode == "camera":
            self.cap = cv2.VideoCapture(0)
            self.log_message("Initializing live camera feed with disturbance engine...")
        else:
            self.cap = cv2.VideoCapture(self.video_path)
            self.log_message(f"Loaded simulation file: {os.path.basename(self.video_path)}")

        self.thread = threading.Thread(target=self.processing_loop)
        self.thread.daemon = True
        self.thread.start()

    def stop_tracking(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.btn_camera.configure(state="normal")
        self.btn_video.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.btn_clear_cache.configure(state="normal")
        self.video_label.configure(image="", text="[ System Offline - Select Mode to Initialize ]")
        self.log_message("Tracking session terminated by operator.")

    def clear_cache_action(self):
        try:
            if os.path.exists("fsoc_tracking_metrics.csv"):
                os.remove("fsoc_tracking_metrics.csv")

            for root, dirs, files in os.walk(".", topdown=False):
                for name in dirs:
                    if name == "__pycache__":
                        shutil.rmtree(os.path.join(root, name), ignore_errors=True)
                for file in files:
                    if file.endswith(".tmp") or file.endswith(".log"):
                        os.remove(os.path.join(root, file))
                        
            self.log_message("Session cache cleared successfully.")
            messagebox.showinfo("Cache Cleared", "Temporary logs and session data cleared successfully.")
        except Exception as e:
            self.log_message(f"[ERROR] Failed to clear cache: {e}")
            messagebox.showerror("Error", f"Failed to clear cache: {e}")

    def processing_loop(self):
        log_file = "fsoc_tracking_metrics.csv"
        file_exists = os.path.exists(log_file)
        f = open(log_file, mode="a", newline="")
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Mode", "FPS", "Target_X", "Target_Y", "Error_Deg_X", "Error_Deg_Y", "Status"])

        while self.is_running and self.cap.isOpened():
            start_time = time.time()
            ret, frame = self.cap.read()
            if not ret:
                if self.mode == "video":
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                else:
                    self.log_message("Camera signal lost.")
                    break

            current_dist_level = self.dist_slider.get()
            frame = self.apply_disturbances(frame, current_dist_level)

            h, w, _ = frame.shape
            img_resized = cv2.resize(frame, (640, 640))
            blob = cv2.dnn.blobFromImage(img_resized, 1/255.0, (640, 640), swapRB=True, crop=False)
            input_name = self.session.get_inputs()[0].name
            
            outputs = self.session.run(None, {input_name: blob})
            predictions = np.squeeze(outputs[0]).T

            center_screen_x, center_screen_y = w // 2, h // 2
            best_dist = float("inf")
            detected_box = None

            for pred in predictions:
                classes_scores = pred[4:]
                max_score = np.max(classes_scores)
                if max_score > 0.35:
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

            status = "Searching..."
            angular_err_x, angular_err_y = 0.0, 0.0

            if detected_box:
                x1, y1, x2, y2, raw_cx, raw_cy = detected_box
                est_cx, est_cy = self.tracker.update(raw_cx, raw_cy)
                status = "Locked" if best_dist <= 25 else "Aligning"
            else:
                est_cx, est_cy = self.tracker.predict()
                status = "Predictive Coasting"

            pixel_offset_x = est_cx - center_screen_x
            pixel_offset_y = est_cy - center_screen_y

            theta_x = np.arctan(pixel_offset_x / self.fx) * (180.0 / np.pi)
            theta_y = np.arctan(pixel_offset_y / self.fy) * (180.0 / np.pi)
            angular_magnitude = np.sqrt(theta_x**2 + theta_y**2)

            self.cam_pan_deg += theta_x * 0.1  
            self.cam_tilt_deg += theta_y * 0.1

            fps = 1.0 / (time.time() - start_time) if (time.time() - start_time) > 0 else 0

            cv2.line(frame, (center_screen_x - 20, center_screen_y), (center_screen_x + 20, center_screen_y), (0, 255, 0), 2)
            cv2.line(frame, (center_screen_x, center_screen_y - 20), (center_screen_x, center_screen_y + 20), (0, 255, 0), 2)

            if detected_box:
                x1, y1, x2, y2, _, _ = detected_box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.circle(frame, (int(est_cx), int(est_cy)), 6, (255, 0, 255), -1)
                cv2.line(frame, (center_screen_x, center_screen_y), (int(est_cx), int(est_cy)), (255, 255, 0), 2)
                writer.writerow([time.strftime("%H:%M:%S"), self.mode, round(fps, 1), int(est_cx), int(est_cy), round(theta_x, 3), round(theta_y, 3), status])

            self.after(0, lambda e=float(angular_magnitude), p=round(self.cam_pan_deg, 2), t=round(self.cam_tilt_deg, 2): self.update_telemetry_plot(e, p, t))

            cv2.putText(frame, f"Mode: {self.mode.upper()} | FPS: {int(fps)}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"Status: {status}", (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"Angle X: {round(theta_x, 2):+.2f}deg | Y: {round(theta_y, 2):+.2f}deg", (20, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            cv2_image = cv2.cvtColor(cv2.resize(frame, (640, 360)), cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(cv2_image)
            imgtk = ImageTk.PhotoImage(image=pil_img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk, text="")

        if self.cap:
            self.cap.release()
        f.close()

    def on_closing(self):
        self.stop_tracking()
        self.destroy()

if __name__ == "__main__":
    app = FSOCControlTerminal()
    app.mainloop()