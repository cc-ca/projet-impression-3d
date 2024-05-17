from keras.models import load_model
from PIL import Image 
from tensorflow import keras
from tensorflow.keras import layers

import numpy as np
import matplotlib.pyplot as plt

import os
import cv2
import random
import time
import datetime
#model.save('models/88-83.h5')

model = load_model('model.h5')


def load_and_preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (255, 255))  # Assurez-vous que la taille correspond à celle utilisée lors de l'entraînement
    img = img / 255.0  # Normalisez les valeurs des pixels
    img = np.expand_dims(img, axis=0)  # Ajoutez une dimension pour représenter le lot (batch)

    return img
def predict_defect_multi_class(model, image_path):
    preprocessed_img = load_and_preprocess_image(image_path)
    predictions = model.predict(preprocessed_img)
    #print (model.predict(preprocessed_img))

    # Interprétez les prédictions
    class_labels = [ "0", "1"]
    predicted_class = class_labels[np.argmax(predictions)]

    return predicted_class

def predict(dir):
    resultf=""
    nb_total=0
    nb_positif=0
    for filename in os.listdir(dir):
        #print(filename)
        nb_total+=1

        result = predict_defect_multi_class(model, dir +"/" + filename)
        if result.upper()==dir[4:].upper():
            nb_positif+=1

        resultf= resultf + "prédiction pour"+ filename + " : "+ str(result) +"\n"

    print (resultf)
    print(str((nb_positif*100)/nb_total) + " % de précision")


def capture():
  # Ouvrir la webcam (la webcam par défaut a l'ID 0)
  cap = cv2.VideoCapture(1)

  # Vérifier si la webcam est ouverte correctement
  if not cap.isOpened():
      print("Erreur: Impossible d'ouvrir la webcam.")
      exit()

  # Capturer une image
  time.sleep(0.5)
  ret, frame = cap.read()

  # Sauvegarder l'image capturée
  if ret:
      cv2.imwrite("photo_capturee.jpg", frame)
      print("Photo capturée avec succès.")
      result = predict_defect_multi_class(model, 'photo_capturee.jpg')
      img = Image.open('photo_capturee.jpg')
      #plt.imshow(img)
      plt.axis('off')  # Masquer les axes
      now = datetime.datetime.now().strftime("%H:%M:%S")
      #plt.show()
      print(f"Prédiction pour la capture caméra : {result}")
      print(f"à {now}")
  
  
  else:
      print("Erreur lors de la capture de la photo.")

  # Libérer la webcam
  cap.release()

def capture_boucle():
    try:
        while True:
            # Exécute la fonction capture()
            capture()
            print()            
            # Pause de x secondes
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nInterruption de l'utilisateur. Fin du script.")

capture_boucle()