from detection3d import is_3d
from quality import is_low_quality
from gaze_detection import gaze_detection
from defects import is_defective
import os

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' - отключение всех сообщений от TensorFlow


path = "C:\\Users\\Eugene\\Downloads\Ai\\TedoStyle\\shutterstock_1798108990.jpg"

graphics_3d = is_3d(path)[0]
low_quality = is_low_quality(path)
looking_at_camera = gaze_detection(path)
has_defectives = is_defective(path)

print(graphics_3d, low_quality, looking_at_camera, has_defectives)