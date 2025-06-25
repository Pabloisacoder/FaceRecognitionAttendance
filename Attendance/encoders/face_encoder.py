import cv2
import os
import face_recognition

def load_and_encode_images(image_dir='images'):
    images = []
    names = []

    for file in os.listdir(image_dir):
        img = cv2.imread(f'{image_dir}/{file}')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            images.append(encodings[0])
            names.append(os.path.splitext(file)[0])

    return names, images

