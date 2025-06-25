import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, timedelta
import pandas as pd

# Load known face images
path = 'images'
images = []
names = []
image_list = os.listdir(path)

for file in image_list:
    img = cv2.imread(f'{path}/{file}')
    images.append(img)
    names.append(os.path.splitext(file)[0])

# Encode known faces
def encode_faces(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            encode_list.append(encodings[0])
    return encode_list

known_encodings = encode_faces(images)

# ✅ Mark attendance with only one IN and one OUT
def mark_attendance_io(name):
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')

    folder_path = os.path.join('Attendance', date_str)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, 'attendance.csv')

    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["Name", "IN", "OUT"])
    else:
        df = pd.read_csv(file_path)

    if name in df['Name'].values:
        row_index = df[df['Name'] == name].index[0]
        if pd.isna(df.at[row_index, 'OUT']) or df.at[row_index, 'OUT'] == '':
            try:
                in_time = datetime.strptime(df.at[row_index, 'IN'], '%H:%M:%S')
                now_time = datetime.strptime(time_str, '%H:%M:%S')
                if (now_time - in_time) >= timedelta(seconds=30):
                    df.at[row_index, 'OUT'] = str(time_str)
            except:
                pass
    else:
        df = pd.concat([df, pd.DataFrame([[name, str(time_str), '']], columns=["Name", "IN", "OUT"])], ignore_index=True)

    df.to_csv(file_path, index=False)

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    small_img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)

    faces_curr = face_recognition.face_locations(small_img)
    encodes_curr = face_recognition.face_encodings(small_img, faces_curr)

    for encode_face, face_loc in zip(encodes_curr, faces_curr):
        matches = face_recognition.compare_faces(known_encodings, encode_face)
        face_dist = face_recognition.face_distance(known_encodings, encode_face)

        y1, x2, y2, x1 = [v * 4 for v in face_loc]

        if len(face_dist) > 0:
            match_index = np.argmin(face_dist)

            if matches[match_index]:
                name = names[match_index].upper()
                color = (255, 0, 0)  # 🔵 Blue for known
                mark_attendance_io(name)
            else:
                name = "UNKNOWN"
                color = (0, 255, 0)  # 🟢 Green for unknown
        else:
            name = "UNKNOWN"
            color = (0, 255, 0)

        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, name, (x1 + 6, y2 - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Face Recognition Attendance', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()








