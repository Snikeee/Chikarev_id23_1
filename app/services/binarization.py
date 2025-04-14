import numpy as np
from PIL import Image
import cv2

def binarize_image(image: Image.Image, algorithm: str = "sauvola") -> Image.Image:
    img_array = np.array(image)
    if len(img_array.shape) == 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    if algorithm.lower() != "sauvola":
        raise ValueError("Поддерживается только алгоритм 'sauvola'")
    window_size = 15
    k = 0.2
    R = 128
    height, width = img_array.shape
    binary = np.zeros((height, width), dtype=np.uint8)
    half_window = window_size // 2
    for i in range(height):
        for j in range(width):
            i_start = max(0, i - half_window)
            i_end = min(height, i + half_window + 1)
            j_start = max(0, j - half_window)
            j_end = min(width, j + half_window + 1)
            window = img_array[i_start:i_end, j_start:j_end]
            mean = np.mean(window)
            variance = np.var(window)
            std = np.sqrt(variance) if variance > 0 else 0
            threshold = mean * (1 + k * (std / R - 1))
            binary[i, j] = 255 if img_array[i, j] > threshold else 0
    return Image.fromarray(binary)