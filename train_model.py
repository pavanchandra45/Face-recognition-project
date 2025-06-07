import cv2
import numpy as np
import os
from PIL import Image
import pickle

dataset_path = "C:\\Users\\katep\\OneDrive\\Desktop\\face\\dataset"
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load metadata
metadata_file = "metadata.pkl"
if os.path.exists(metadata_file):
    with open(metadata_file, "rb") as f:
        metadata = pickle.load(f)
else:
    metadata = {}

# Prepare training data
face_samples = []
ids = []

print("\nScanning dataset folder...")

for subdir in os.listdir(dataset_path):
    subdir_path = os.path.join(dataset_path, subdir)
    
    if os.path.isdir(subdir_path):  # Check if it's a folder
        for filename in os.listdir(subdir_path):
            if filename.endswith(".jpg"):
                image_path = os.path.join(subdir_path, filename)
                gray_image = Image.open(image_path).convert("L")  # Ensure grayscale
                image_np = np.array(gray_image, "uint8")

                if image_np is None:
                    print(f" Error loading {filename} - Skipping!")
                    continue

                user_id = int(subdir)  # Extract ID from folder name

                face_samples.append(image_np)
                ids.append(user_id)

print(f"Found {len(face_samples)} images for training.")

# Ensure at least 2 images for training
if len(face_samples) < 2:
    print("ERROR: Not enough images for training! Capture at least 2 faces per person.")
    exit()

ids = np.array(ids)

# Train model
recognizer.train(face_samples, ids)
recognizer.save("trainer.yml")
print("\n Model Training Complete. Saved as 'trainer.yml'.")
