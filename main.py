from detection3d import is_no_3d
from quality import is_high_quality
from gaze_detection import no_looking
from defects import is_defective
from colors import is_color_ok
import os


# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' - отключение всех сообщений от TensorFlow

def is_ok(path):
    graphics_3d = is_no_3d(path)[0]
    low_quality = is_high_quality(path)
    looking_at_camera = no_looking(path)
    defects_values = is_defective(path)
    blur = defects_values['blur']
    noise = defects_values['noise']
    brightness = defects_values['brightness']
    colors = is_color_ok(path)
    criteria = dict()
    criteria['blur'] = blur
    criteria['noise'] = noise
    criteria['brightness'] = brightness
    criteria['colors'] = colors
    criteria['looking'] = looking_at_camera
    criteria['quiality'] = low_quality
    criteria['3d'] = graphics_3d
    res = 0.15 * (brightness + blur + noise + looking_at_camera) + 0.3 * (colors) + 0.1 * (graphics_3d) >= 0.5
    return int(res), criteria


def main():
    folder_path = 'C:\\Users\\Eugene\\Downloads\\Ai\\TedoStyle'

    output_filename = 'output2.txt'

    files = os.listdir(folder_path)

    with open(output_filename, 'w') as file:
        file.write(f"file;result;blur;noise;brightness;colors;looking;quality;3d\n")
        for filename in files:
            try:
                if filename.endswith('.jpg') or filename.endswith('.png'):  # Проверка, что файл является изображением
                    full_path = os.path.join(folder_path, filename)
                    result = is_ok(full_path)
                    string = f'{filename};{result[0]};'
                    for criterium in result[1]:
                        string += str(result[1][criterium]) + ';'
                    file.write(f"{string[:-1]}\n")
            except Exception as e:
                print('!!!')
                print(e)
                print('!!!')

if __name__ == "__main__":
    main()
