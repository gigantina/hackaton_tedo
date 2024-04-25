import pathlib
import cv2
import cv2.typing
import numpy as np


def count_acceptable_colors_percent_in_buffer(img_bgr: cv2.typing.MatLike, percent: int) -> float:
    ''' Вычисление доли подходящих цветов в буфере bgr '''

    hsv: cv2.typing.MatLike = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # black
    hsv_black_lower = np.array([0, 0, 0])
    hsv_black_upper = np.array([0, 0, 5])
    mask = cv2.inRange(hsv, hsv_black_lower, hsv_black_upper)
    count_black = cv2.countNonZero(mask)

    hue_delta22 = int(360 * percent / 400)

    # red = hsv(0, 255, 255), h: 0-179
    hsv_red_lower1 = np.array([int(360 / 2) - 1 - hue_delta22, 0, 20])
    hsv_red_upper1 = np.array([int(360 / 2) - 1, 255, 255])
    mask = cv2.inRange(hsv, hsv_red_lower1, hsv_red_upper1)
    count_red = cv2.countNonZero(mask)

    hsv_red_lower2 = np.array([0, 0, 20])
    hsv_red_upper2 = np.array([0 + hue_delta22, 255, 255])
    mask = cv2.inRange(hsv, hsv_red_lower2, hsv_red_upper2)
    count_red += cv2.countNonZero(mask)

    # blue = hsv(240, 255, 255)
    hsv_blue_lower = np.array([int(240 / 2) - hue_delta22, 0, 20])
    hsv_blue_upper = np.array([int(240 / 2) + hue_delta22, 255, 255])
    mask = cv2.inRange(hsv, hsv_blue_lower, hsv_blue_upper)
    count_blue = cv2.countNonZero(mask)

    # yellow = hsv(57, 255, 255)
    hsv_yellow_lower = np.array([int(57 / 2) - hue_delta22, 0, 20])
    hsv_yellow_upper = np.array([int(57 / 2) + hue_delta22, 255, 255])
    mask = cv2.inRange(hsv, hsv_yellow_lower, hsv_yellow_upper)
    count_yellow = cv2.countNonZero(mask)

    return (count_red + count_blue + count_yellow) / (hsv.shape[0] * hsv.shape[1] - count_black)


def count_acceptable_colors_percent_in_file(filepath: pathlib.Path, percent: int = 20) -> float:
    """
    Вычисление доли подходящих цветов в файле

    Args:
        filepath (pathlib.Path): Путь к файлу с изображением
        percent (int): "Ширина" hue подходящих цветов (по умолчанию 20%). Если значение равно 0, то используется только сам цвет и его оттенки.

    Returns:
        float: Доля подходящих цветов в файле
    """
    img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    return count_acceptable_colors_percent_in_buffer(img, percent)


def main():
    images_dir = pathlib.Path(r"data\Фото в стиле ТеДо")
    for fs_item in images_dir.iterdir():
        if fs_item.is_file():
            try:
                r = count_acceptable_colors_percent_in_file(fs_item, 20)
                if 0.70 <= r <= 0.95:
                    print(f"{r:4.3f} | {fs_item}")
            except cv2.error:
                continue

def is_color_ok(path):
    r = count_acceptable_colors_percent_in_file(path)
    return 0.70 <= r <= 0.95


if __name__ == "__main__":
    main()
