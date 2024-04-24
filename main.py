from detection3d import is_3d
import os

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' - отключение всех сообщений от TensorFlow

path = 'C:\\Users\\Eugene\\Downloads\\istockphoto-1639514565-1024x1024.jpg'

print(is_3d(path)[0])