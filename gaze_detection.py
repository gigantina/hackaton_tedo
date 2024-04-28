import cv2
import dlib
import numpy as np

# Load the image and convert it

def get_gaze(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    direction = 'left'

    # Initialize the face detector and the landmark predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    first_eye = []
    second_eye = []

    # Detect faces
    faces = detector(gray)

    # Function to extract eye coordinates
    def get_eye_coords(landmarks, start, end):
        eye_coords = []
        for i in range(start, end+1):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            eye_coords.append((x, y))
        return np.array(eye_coords, dtype=np.int32)

    def draw_eye_rectangle(image, eye_coords):
        x_min = np.min(eye_coords[:, 0])
        x_max = np.max(eye_coords[:, 0])
        y_min = np.min(eye_coords[:, 1])
        y_max = np.max(eye_coords[:, 1])
        #cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        return x_min, y_min, x_max, y_max

    def find_pupil(gray, x_min, y_min, x_max, y_max):
        eye_region = gray[y_min:y_max, x_min:x_max]
        #gray = cv2.cvtColor(eye_region, cv2.COLOR_BGR2GRAY)
        threshold_value = 40  # Примерное значение, подберите под свои условия
        _, thresholded = cv2.threshold(eye_region, threshold_value, 255, cv2.THRESH_BINARY_INV)
        #cv2.imshow("Thresholded Eye", thresholded)
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Находим контур с максимальной площадью
        largest_contour = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(largest_contour)
        # Приведение координат к исходному масштабу изображения
        pupil_rect = (x_min + x, y_min + y, x_min + x + w, y_min + y + h)
        cv2.rectangle(image, (pupil_rect[0], pupil_rect[1]), (pupil_rect[2], pupil_rect[3]), (0, 0, 255), 2)  # Рисуем красный прямоугольник
        return pupil_rect

        shifted_contour = largest_contour + np.array([x_min, y_min])
        cv2.drawContours(image, [shifted_contour], -1, (255, 255, 0), thickness=cv2.FILLED)  # Синий цвет


    for face in faces:
        x1 = face.left()
        x2 = face.right()
        face_center_x = (x1 + x2) // 2
        landmarks = predictor(gray, face)

        # Get eye regions and draw rectangles
        left_eye_coords = get_eye_coords(landmarks, 36, 41)
        right_eye_coords = get_eye_coords(landmarks, 42, 47)
        left_x_min, left_y_min, left_x_max, left_y_max = draw_eye_rectangle(image, left_eye_coords)
        right_x_min, right_y_min, right_x_max, right_y_max = draw_eye_rectangle(image, right_eye_coords)

        # Find pupils within the rectangles
        first_eye = find_pupil(gray, left_x_min, left_y_min, left_x_max, left_y_max)
        second_eye = find_pupil(gray, right_x_min, right_y_min, right_x_max, right_y_max)
        direction = ''
        if first_eye[0] < face_center_x and second_eye[0] < face_center_x:
            direction = 'left'
        elif first_eye[0] > face_center_x and second_eye[0] > face_center_x:
            direction = 'right'
        else:
            direction = 'forward'
        print(direction)

    return direction, first_eye, second_eye


def move_pupil(image, eye_rect, pupil_center, shift_x):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x, y, w, h = eye_rect
    dx = 80  # Сдвиг вправо на 50 пикселей
    shift_matrix = np.float32([[1, 0, dx], [0, 1, 0]])

    # Применение аффинного преобразования
    shifted_image = cv2.warpAffine(image, shift_matrix, (image.shape[1], image.shape[0]))
    return shifted_image
    # Загрузка изображения

def get_no_looking(image):
    direction, first_eye, second_eye = get_gaze(image)
    x1 = first_eye[0] + first_eye[3] // 2 
    y1 = first_eye[1] + first_eye[2] // 2
    first_eye_center = (x1, y1)
    x1 = second_eye[0] + second_eye[3] // 2 
    y1 = second_eye[1] + second_eye[2] // 2
    second_eye_center = (x1, y1)
    shift_x = -40
    result_image = move_pupil(image, first_eye, first_eye_center, shift_x)
    return result_image

def no_looking(path):
    image = cv2.imread(image_path)
    if get_gaze(image)[0] != 'forward':
        return True
    else:
        return False