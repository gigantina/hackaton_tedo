import cv2
import numpy as np


def get_blur(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var

def get_noise(image):
    
    # Вычисляем среднее значение и стандартное отклонение
    mean_value = np.mean(image)
    std_deviation = np.std(image)

    # Вычисляем соотношение сигнал/шум в децибелах
    if std_deviation == 0:
        return 0
    snr = 20 * np.log10(mean_value / std_deviation)
    return snr

def get_brightness(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    brightness = hsv[:,:,2].mean()
    return brightness

def is_defective(path, min_blur=100, max_noise=40, min_bright=50, max_bright=200):
    image = cv2.imread(path)
    blur = get_blur(image)
    noise = get_noise(image)
    brightness = get_brightness(image)
    result = dict()
    result['blur'] = True
    result['noise'] = True
    result['brightness'] = True
    result['bokeh'] = True
    if blur < max_blur:
        result['blur'] = False
    if noise >= max_noise:
        result['noise'] = False
    if brightness < min_bright or brightness > max_bright:
        result['brightness'] = False

    for key in result:
        if not result[key]:
            return (True, result)
    return (False, result)




