import face_recognition
import numpy as np

def detect_faces(frame, known_encodings, known_names):
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    results = []

    for encoding, location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        face_distances = face_recognition.face_distance(known_encodings, encoding)

        if matches:
            best_match = np.argmin(face_distances)
            if matches[best_match]:
                name = known_names[best_match].upper()
                results.append((name, location, True))
                continue
        results.append(("UNKNOWN", location, False))

    return results
