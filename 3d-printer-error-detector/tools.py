import numpy as np
import os
import time
import cv2
import settings
import color

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

def capture_image():
    while True:
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise Exception("Could not open video device")

            ret, frame = cap.read()

            static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', 'images')
            if not os.path.exists(static_folder):
                os.makedirs(static_folder)

            # Remove old images to only allow a small buffer of images and prevent disk space issues
            files = os.listdir(static_folder)
            files.sort()
            number_of_files = len(files)
            if number_of_files > settings.NUMBER_OF_IMAGES_RETAINED - 1:
                for file in files[:number_of_files - settings.NUMBER_OF_IMAGES_RETAINED + 1]:
                    file_path = os.path.join(static_folder, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

            settings.image_name = str(int(time.time())) + '.jpg'
            image_path = os.path.join(static_folder, settings.image_name)
            cv2.imwrite(image_path, frame)
            settings.image_path = image_path
            cap.release()
            time.sleep(settings.SLEEP_INTERVAL)
        except:
            cap.release()
            settings.current_state = settings.State.ISSUE
            settings.model_thread_running = False
            color.pulsing_light(settings.current_state)
