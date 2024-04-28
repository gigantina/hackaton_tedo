from PIL import Image

def is_high_quality(path, min_dpi=220, min_resolution=(1024, 768)):
    try:
        img = Image.open(path)
        dpi = img.info.get("dpi", (0, 0))
        width, height = img.size

        # Проверяем разрешение
        if width <= min_resolution[0] or height < min_resolution[1]:
            return True

        # Проверяем DPI
        if dpi[0] < min_dpi or dpi[1] < min_dpi:
            return True

        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return True

def get_high_quality(path):
    # Define the command and its arguments as a list of strings
    command = [
            'python', 'inference_realesrgan.py',
            '-n', 'RealESRGAN_x4plus',
            '-i', path,
            '--face_enhance'
    ]

    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)
