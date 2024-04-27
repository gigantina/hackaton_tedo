import cv2
import dlib
import numpy as np

faces_model_path = "shape_predictor_68_face_landmarks.dat"

def load_image(image_path):
    return cv2.imread(image_path)

def find_faces(image):
    detector = dlib.get_frontal_face_detector()
    return detector(image, 1)

def get_landmarks(image, faces):
    predictor = dlib.shape_predictor(faces_model_path)
    landmarks = []
    for face in faces:
        landmarks.append(predictor(image, face))
    return landmarks


def is_looking_at_camera(landmarks):
    for landmark in landmarks:
        left_eye = np.array([landmark.part(36).x, landmark.part(36).y])
        right_eye = np.array([landmark.part(45).x, landmark.part(45).y])
        eye_line = right_eye - left_eye
        angle = np.arctan2(eye_line[1], eye_line[0]) * 180.0 / np.pi
        if abs(angle) < 10:
            return True
    return False

def no_looking(path):
	image = load_image(path)
	faces = find_faces(image)


	landmarks = get_landmarks(image, faces)
	return not is_looking_at_camera(landmarks)


if __name__ == '__main__':
	print(no_looking('C:\\Users\\Eugene\\Documents\\hack\\bad\\dreamstime_m_172552664.jpg'))