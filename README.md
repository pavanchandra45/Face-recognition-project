# Face-recognition-project
A smart IoT-based security system that unlocks doors using facial recognition. Built with Raspberry Pi, OpenCV, and Python to ensure safe, automated access for authorized users.
# 🔓 Face Detection-Based Automatic Door Unlocking System

A smart IoT-based security system that uses facial recognition to automatically unlock a door. Built using Raspberry Pi, OpenCV, and Python, this system ensures secure access by identifying authorized individuals in real-time.

---

## 📸 Demo
![Face Detection Demo](demo.gif) <!-- Optional: Add a .gif or image of the system working -->

---

## 🚀 Features

- Real-time face detection and recognition using OpenCV
- Automatic door unlocking via servo motor on successful match
- Easy enrollment of new users
- Secure local face dataset training
- Compatible with Raspberry Pi and other GPIO-based systems

---

## 🧠 Tech Stack

| Component      | Technology         |
|----------------|--------------------|
| Face Detection | OpenCV (Haar Cascades) |
| Face Recognition | LBPH (Local Binary Patterns Histogram) |
| Hardware       | Raspberry Pi 3, Servo Motor |
| Programming    | Python |
| Control        | RPi.GPIO / GPIO Zero |

---

## 📁 Project Structure

```bash
face-unlock-system/
│
├── dataset/                # Stored face images for each user
├── recognizer.yml          # Trained face model file
├── haarcascade_frontalface_default.xml
│
├── face_data_collection.py        # Script to register a new face
├── train_model.py          # Trains the face recognizer
├── cam_recognize.py               # Main script: runs face recognition + unlocks door
├── delete.py        # Deletes a user data according to the user input
