import cv2
import os
import csv
import time
import pickle

# Define dataset path
dataset_path = "C:\\Users\\katep\\OneDrive\\Desktop\\face\\dataset"


# Create dataset folder if not exists
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# User data CSV file
csv_file = "users.csv"

# Create CSV file with headers if not exists
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Age", "Gender"])

# Load existing IDs only if their folder still exists
existing_ids = set()
with open(csv_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        folder_path = os.path.join(dataset_path, row["ID"])
        if os.path.exists(folder_path):
            existing_ids.add(row["ID"])

# Input user details
while True:
    user_id = input("Enter unique ID: ").strip()
    if user_id in existing_ids:
        print("❌ ID already exists. Please try a different one.")
    else:
        break

name = input("Enter Name: ").strip()
age = input("Enter Age: ").strip()
gender = input("Enter Gender: ").strip()

# Save user info to CSV
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([user_id, name, age, gender])
print(f"✅ User {name} (ID: {user_id}) added to CSV successfully.")

# Update metadata.pkl file
metadata_file = "metadata.pkl"
if os.path.exists(metadata_file):
    with open(metadata_file, "rb") as f:
        metadata = pickle.load(f)
else:
    metadata = {}

# Add new user metadata
metadata[user_id] = {
    "Name": name,
    "Age": age,
    "Gender": gender
}

# Save metadata
with open(metadata_file, "wb") as f:
    pickle.dump(metadata, f)
print(f"✅ Metadata updated for ID {user_id}.")

# Create folder for user
user_folder = os.path.join(dataset_path, user_id)
os.makedirs(user_folder, exist_ok=True)

# Initialize camera and face detection
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Instructions to show
instructions = [
    "Look Straight 👀",
    "Look Left 👈",
    "Look Right 👉",
    "Smile 🙂",
    "Raise Eyebrows 😲",
    "Close Eyes 😌"
]

instruction_time = 4  # Seconds
img_count = 0
max_images = 60
start_time = time.time()
instruction_index = 0

while img_count < max_images:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    elapsed = time.time() - start_time
    if elapsed > instruction_time:
        instruction_index = (instruction_index + 1) % len(instructions)
        start_time = time.time()

    current_instruction = instructions[instruction_index]
    cv2.putText(frame, f"Instruction: {current_instruction}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.putText(frame, f"Image {img_count}/{max_images}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    for (x, y, w, h) in faces:
        face = gray[y:y + h, x:x + w]
        filename = os.path.join(user_folder, f"{user_id}_{img_count}.jpg")
        cv2.imwrite(filename, face)
        img_count += 1
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        time.sleep(0.2)

    cv2.imshow("Capturing Faces", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print(f"\n✅ Captured {img_count} images for ID {user_id}.")
