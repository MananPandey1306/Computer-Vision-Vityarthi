# AttendAI - Real-Time Face Recognition Attendance System

**Author:** Manan Pandey  
**Registration Number:** 24BAI10033  
**Course:** CSE3010 - Computer Vision  

---

## 📖 Introduction
In traditional educational environments, taking attendance manually is a time-consuming process that cuts into valuable instructional time. **AttendAI** is a computer vision-based application designed to automate this process. Using real-time facial recognition and liveness detection, the system seamlessly identifies students as they enter a classroom, logs their presence in a database, and provides intuitive reporting via a Streamlit web interface.

## 🚀 Features
- **Student Enrollment:** Capture a new student's face via webcam or image upload, extract their facial embedding, and store it alongside their name and roll number.
- **Live Recognition:** Process real-time webcam frames to detect and recognize enrolled students.
- **Liveness Detection:** Implements an anti-spoofing check using a Laplacian variance approach to ensure static printed photos cannot be used to fake presence.
- **Attendance Logging:** Records the recognized student's details (date, time, confidence score) and prevents duplicate same-day entries.
- **Reporting Dashboard:** User interface to view daily attendance logs and export them as CSV files.

## 🏗️ System Architecture & Tech Stack
AttendAI follows a modular 3-tier architecture:
- **Presentation Layer (Frontend):** Streamlit-based web application providing a UI for Enrollment, Live Attendance, and Reports. Features custom CSS for a premium glassmorphic aesthetic.
- **Logic Layer (Backend/CV):** Python modules handling computer vision tasks. 
  - *OpenCV:* Used for frame capturing and drawing.
  - *face_recognition (dlib):* Handles 128-d embedding extraction and matching using HOG feature extraction and deep metric learning.
- **Data Layer:** SQLite database (`attendance.db`) storing student profiles, serialized 128-d face embeddings, and attendance logs.

## ⚙️ Prerequisites & Setup
- **Environment:** Python 3.12
- **Key Libraries:** OpenCV, Streamlit, dlib, `face_recognition`
- *Note:* Installing `dlib` and `face_recognition` on Windows requires CMake and Visual Studio C++ Build Tools.

To run the application, ensure your dependencies are installed, then execute:
```bash
streamlit run app.py
```

## 🔮 Future Enhancements
- **Deep-Learning Anti-Spoofing:** Upgrade the liveness detector from a simple blur check to a CNN-based blink detector (using eye aspect ratio) or a texture analyzer for higher security.
- **Multi-threading:** Offload the video capture and face recognition loops to background threads using WebRTC to significantly improve frame rates in the Streamlit UI.
- **Cloud Database Integration:** Migrate from SQLite to PostgreSQL or Firebase to allow multiple classroom cameras to sync attendance to a central server.
