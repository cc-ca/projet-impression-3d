import os
import cv2

# Spécifie le chemin du dossier contenant les images
dossier_images = "./dataset_colab/bed_not_stick"

# Vérifie si le dossier "mirrored" existe, sinon le crée
dossier_miroir = os.path.join(dossier_images, "mirrored")
if not os.path.exists(dossier_miroir):
    os.makedirs(dossier_miroir)

# Parcours toutes les images du dossier
for fichier_image in os.listdir(dossier_images):
    chemin_image = os.path.join(dossier_images, fichier_image)

    # Vérifie si le fichier est une image
    if os.path.isfile(chemin_image) and fichier_image.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Charge l'image
        image = cv2.imread(chemin_image)

        # Applique l'effet miroir de droite à gauche
        image_miroir = cv2.flip(image, 1)

        # Crée le nom du nouveau fichier miroir
        nom_fichier_miroir = "mirror_" + fichier_image

        # Chemin complet pour sauvegarder l'image miroir
        chemin_image_miroir = os.path.join(dossier_miroir, nom_fichier_miroir)

        # Sauvegarde l'image miroir
        print(chemin_image_miroir)
        cv2.imwrite(chemin_image_miroir, image_miroir)

print("Opération terminée. Les images miroir ont été sauvegardées dans le dossier 'mirrored'.")
