from PIL import Image
import numpy as np

def get_good_colors(image):
    """Преобразует теплые цвета изображения в более холодные."""
    # Создаем матрицу преобразования цветов
    transformation_matrix = [
        [1.0, 0.5, 0.5],
        [0.5, 1.0, 0.5],
        [0.5, 0.5, 1.0]
    ]

    # Преобразуем изображение в NumPy массив
    image_array = np.asarray(image)

    # Нормализуем значения массива до диапазона [0, 1]
    image_array = image_array.astype(np.float) / 255.0

    # Применяем матрицу преобразования к каждому каналу RGB
    for i in range(len(transformation_matrix)):
        image_array[:, :, i] = image_array[:, :, i] * transformation_matrix[i]

    # Преобразуем обратно в формат PIL и нормализуем значения до диапазона [0, 255]
    image_array = image_array * 255
    image_array = image_array.astype(np.uint8)
    filtered_image = Image.fromarray(image_array)

    return filtered_image
