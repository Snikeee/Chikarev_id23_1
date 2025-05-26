from celery import Celery
from celery import current_task
import numpy as np
from PIL import Image
import cv2
import base64
from io import BytesIO
from app.tasks.celery_config import app

@app.task(bind=True)
def binarize_image_task(self, image_base64: str, algorithm: str):
    try:
        # Декодирование base64 изображения
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))
        img_array = np.array(image)

        # Конвертация в оттенки серого, если нужно
        if len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        if algorithm.lower() != "sauvola":
            raise ValueError("Поддерживается только алгоритм 'sauvola'")

        # Бинаризация с обновлением прогресса
        window_size = 15
        k = 0.2
        R = 128
        height, width = img_array.shape
        binary = np.zeros((height, width), dtype=np.uint8)
        total_pixels = height * width
        processed_pixels = 0

        for i in range(height):
            for j in range(width):
                i_start = max(0, i - window_size // 2)
                i_end = min(height, i + window_size // 2 + 1)
                j_start = max(0, j - window_size // 2)
                j_end = min(width, j + window_size // 2 + 1)

                window = img_array[i_start:i_end, j_start:j_end]
                mean = np.mean(window)
                variance = np.var(window)
                std = np.sqrt(variance) if variance > 0 else 0
                threshold = mean * (1 + k * (std / R - 1))
                binary[i, j] = 255 if img_array[i, j] > threshold else 0

                # Обновление прогресса
                processed_pixels += 1
                progress = (processed_pixels / total_pixels) * 100
                self.update_state(state='PROGRESS', meta={'progress': round(progress, 2)})

        # Конвертация результата в base64
        binarized_image = Image.fromarray(binary)
        buffered = BytesIO()
        binarized_image.save(buffered, format="PNG")
        binarized_base64 = base64.b64encode(buffered.getvalue()).decode()

        return {
            'status': 'COMPLETED',
            'task_id': self.request.id,
            'binarized_image': binarized_base64
        }
    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise