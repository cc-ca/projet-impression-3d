from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import settings
import cv2

def load_and_preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (255, 255))  # Ensure the size matches the training input size
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def predict_defect(model, image_path):
    img = load_and_preprocess_image(image_path)
    predictions = model.predict(img)
    return '0' if np.argmax(predictions) == 0 else '1'

def capture_image(model):
    try:
        cap = cv2.VideoCapture(0)  # Open default webcam
        ret, frame = cap.read()

        static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', 'images')
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)

        # Remove old images
        files = os.listdir(static_folder)
        for file in files:
            file_path = os.path.join(static_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        settings.image_name = time.time() + '.jpg'
        image_path = os.path.join(static_folder, settings.image_name)
        cv2.imwrite(image_path, frame)
        print("Photo captured successfully.")

        img = Image.open(image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        cap.release()

        return predict_defect(model, image_path)
    finally:
        cap.release()