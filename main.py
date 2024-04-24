from detection3d import is_3d
from quality import is_low_quality
import os

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' - отключение всех сообщений от TensorFlow

path = 'C:\\Users\\Eugene\\Downloads\\Икусственный интеллект\\Фото в стиле ТеДо\\dreamstime_m_103311834.jpg'

print(is_3d(path)[0])
print(is_low_quality(path))