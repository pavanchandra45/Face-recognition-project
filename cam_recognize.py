import cv2
import numpy as np
import pickle
import os
import time

# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# Load metadata
metadata_file = "metadata.pkl"
if os.path.exists(metadata_file):
    with open(metadata_file, "rb") as f:
        metadata = pickle.load(f)
else:
    print("Metadata not found!")
    metadata = {}

# Load face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Set confidence threshold
CONFIDENCE_THRESHOLD = 50.0

# Track time for group log print
last_log_time = 0
LOG_DELAY = 5  # seconds

# Start camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    known_faces = 0
    unknown_faces = 0
    current_time = time.time()

    for (x, y, w, h) in faces[:5]:  # Process up to 5 faces
        face_gray = gray[y:y + h, x:x + w]
        user_id, confidence = recognizer.predict(face_gray)
        confidence_percentage = round(100 - confidence, 2)

        if confidence_percentage >= CONFIDENCE_THRESHOLD and str(user_id) in metadata:
            user = metadata[str(user_id)]
            name, age, gender = user["Name"], user["Age"], user["Gender"]
            info = f"{name}, {age} yrs, {gender} ({confidence_percentage}%)"
            rectangle_color = (0, 255, 0)  # Green
            known_faces += 1
        else:
            info = f"Unknown ({confidence_percentage}%)"
            rectangle_color = (0, 0, 255)  # Red
            unknown_faces += 1

        cv2.rectangle(frame, (x, y), (x + w, y + h), rectangle_color, 2)
        cv2.putText(frame, info, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, rectangle_color, 2)

    # Print group detection log with delay
    if current_time - last_log_time >= LOG_DELAY:
        if known_faces >0 and unknown_faces == 0:
            print(f"{known_faces} faces known, {unknown_faces} faces unknown ✅❌")
            print("Door open..Welcome!")
        elif known_faces + unknown_faces > 0:
            print(f"{known_faces} faces known, {unknown_faces} faces unknown ✅❌")
            print("Unknown Person Detected! 🚨 ... Door cannot be opened")
        last_log_time = current_time

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
