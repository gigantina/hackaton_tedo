import cv2
import os
import numpy as np
import json

with open('dominant_colors.json', 'r') as f:
    colors_to_check = json.load(f)
palette = []
for _, color in colors_to_check:
    palette.append(color)

def euclidean_distance(color1, color2):
    return np.sqrt(np.sum((color1 - color2) ** 2))

def is_color_close(average_color, palette, threshold=7):
    # Check if the average color is close to any color in the palette
    for color in palette:
        if euclidean_distance(average_color, color) < threshold:
            return True
    return False

def average_color(image_path, threshold=10):
    # Load the image
    img = cv2.imread(image_path)

    # Filter out very dark pixels
    mask = np.all(img > [threshold, threshold, threshold], axis=-1)
    valid_pixels = img[mask]

    # Calculate the mean of valid pixels if any
    if valid_pixels.size > 0:
        average = valid_pixels.mean(axis=0)
    else:
        average = [0, 0, 0]  # Default to black if no valid pixels found

    # Convert to RGB if needed (OpenCV uses BGR by default)
    average_color = np.array(average, dtype=np.uint8)[::-1]

    # Display the average color for verification
    average_image = np.full((100, 100, 3), average_color, dtype=np.uint8)

    return average_color

# Example palette (list of RGB tuples)
#palette = [(0, 44, 98),    (0, 76, 137),
#    (0, 94, 169),    (217, 215, 216),
#    (212, 215, 219),    (127, 172, 191),
#    (131, 152, 174),    (91, 155, 204),
#    (60, 119, 174)]


def process_directory(directory, palette):
    results = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')):
            print(filename)
            image_path = os.path.join(directory, filename)
            avg_color = average_color(image_path)
            close_to_palette = is_color_close(avg_color, palette)
            results.append((filename, avg_color.tolist(), "Close" if close_to_palette else "Not close"))
        else:
            results.append((filename, None, "Failed to load"))
    return results

def is_color_ok(path):
    avg_color = average_color(path)
    close_to_palette = is_color_close(avg_color, palette)
    return close_to_palette