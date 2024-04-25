import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import tensorflow as tf


model_path = "3d_detection_model_complete.h5" 
model = load_model(model_path)

def is_no_3d(path):
    model = load_model(model_path)
    img = image.load_img(path, target_size=(180, 180))  # Измените размер согласно параметрам, использованным при обучении

    # Преобразование изображения в массив numpy
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Создаем пакет из одного изображения
    img_array /= 255.0  # Нормализация

    # Предсказание
    prediction = model.predict(img_array)
    return prediction[0] >= 0.5