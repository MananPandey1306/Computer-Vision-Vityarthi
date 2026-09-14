import cv2
import face_recognition
import numpy as np
from database.db import add_student

def process_enrollment(image_bgr, name, roll_no):
    """
    Process an enrollment image.
    Expects image in BGR format (like from OpenCV).
    Returns (success_bool, message)
    """
    if not name or not roll_no:
        return False, "Name and Roll Number cannot be empty."

    # Convert BGR to RGB for face_recognition
    rgb_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    # Detect faces
    face_locations = face_recognition.face_locations(rgb_image)
    
    if len(face_locations) == 0:
        return False, "No face detected in the image."
    elif len(face_locations) > 1:
        return False, "Multiple faces detected. Please ensure only one face is in the frame."
        
    # Get the embedding (128-d vector)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
    
    if not face_encodings:
        return False, "Failed to extract face features."
        
    embedding = face_encodings[0]
    
    # Save to database
    success, msg = add_student(name, roll_no, embedding)
    
    return success, msg
