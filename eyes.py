import cv2
import dlib
import numpy as np
import os

faces_model_path = "C:\\Users\\Eugene\\Documents\\hack\\models\\shape_predictor_68_face_landmarks.dat"

def load_image(path):
    if os.path.exists(path):
        image = cv2.imread(path)
        if image is not None:
            return image
        else:
            print("Image loaded is None. Check file format or permissions.")
            return None
    else:
        print("File does not exist:", path)
        return None

def find_faces(image):
    detector = dlib.get_frontal_face_detector()
    return detector(image, 1)

def get_landmarks(image, faces):
    predictor = dlib.shape_predictor(faces_model_path)
    landmarks = []
    for face in faces:
        landmarks.append(predictor(image, face))
    return landmarks

def head_pose_estimation(image, landmarks):
    size = image.shape
    focal_length = size[1]
    center = (size[1]//2, size[0]//2)
    camera_matrix = np.array([[focal_length, 0, center[0]],
                              [0, focal_length, center[1]],
                              [0, 0, 1]], dtype="double")
    
    # Assuming no lens distortion
    dist_coeffs = np.zeros((4, 1))  

    # 3D points in real world space
    model_points = np.array([
        (0.0, 0.0, 0.0),             # Nose tip
        (0.0, -330.0, -65.0),        # Chin
        (-225.0, 170.0, -135.0),     # Left eye left corner
        (225.0, 170.0, -135.0),      # Right eye right corner
        (-150.0, -150.0, -125.0),    # Left Mouth corner
        (150.0, -150.0, -125.0)      # Right mouth corner
    ])

    # 2D image points. If you change the landmarks, the result will be different
    image_points = np.array([
        (landmarks.part(30).x, landmarks.part(30).y), # Nose tip
        (landmarks.part(8).x, landmarks.part(8).y),   # Chin
        (landmarks.part(36).x, landmarks.part(36).y), # Left eye left corner
        (landmarks.part(45).x, landmarks.part(45).y), # Right eye right corner
        (landmarks.part(48).x, landmarks.part(48).y), # Left Mouth corner
        (landmarks.part(54).x, landmarks.part(54).y)  # Right Mouth corner
    ], dtype="double")

    # Solve for pose
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

    # Project a 3D point (0.0, 0.0, 1000.0) onto the image plane. 
    # We use this to draw a line sticking out of the nose
    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

    # Calculate the angle of this projection to assess the orientation
    p1 = (int(image_points[0][0]), int(image_points[0][1]))
    p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))
    angle = np.arctan2(p2[1] - p1[1], p2[0] - p1[0]) * 180.0 / np.pi

    return abs(angle) < 10  # Adjust the angle threshold as needed

def is_looking_at_camera(landmarks, image):
    return head_pose_estimation(image, landmarks[0])  # Assuming one face per image for simplicity

def gaze_detection(path):
    image = load_image(path)
    faces = find_faces(image)
    landmarks = get_landmarks(image, faces)
    return is_looking_at_camera(landmarks, image)

# Usage
path = "C:\\Users\\Eugene\\Documents\\hack\\not_3d_graphics\\dreamstime_m_27976951.jpg"
print(gaze_detection(path))
