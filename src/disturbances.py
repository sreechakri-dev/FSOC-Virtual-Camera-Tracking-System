import cv2
import numpy as np

class DisturbanceEngine:
    """Injects simulated real-world environmental disturbances into video frames."""
    def __init__(self):
        pass

    def apply(self, frame, level_pct):
        """Applies random platform vibration jitter, atmospheric Gaussian noise, and motion blur."""
        if level_pct <= 0:
            return frame
        
        factor = level_pct / 100.0
        h, w, _ = frame.shape

        # 1. Random Platform Vibration Jitter
        max_shift = int(15 * factor)
        shift_x = int(np.random.randint(-max_shift, max_shift + 1)) if max_shift > 0 else 0
        shift_y = int(np.random.randint(-max_shift, max_shift + 1)) if max_shift > 0 else 0
        
        M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
        frame = cv2.warpAffine(frame, M, (w, h))

        # 2. Gaussian Noise (Atmospheric Scintillation / Turbulence)
        noise_sigma = 35.0 * factor
        gauss = np.random.normal(0, noise_sigma, frame.shape).astype(np.int16)
        noisy_frame = np.clip(frame.astype(np.int16) + gauss, 0, 255).astype(np.uint8)

        # 3. Motion Blur
        if factor > 0.4:
            kernel_size = int(5 * factor)
            if kernel_size % 2 == 0:
                kernel_size += 1
            kernel = np.zeros((kernel_size, kernel_size))
            kernel[int(kernel_size // 2), :] = 1.0 / kernel_size
            noisy_frame = cv2.filter2D(noisy_frame, -1, kernel)

        return noisy_frame