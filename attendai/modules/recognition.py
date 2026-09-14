import cv2
import face_recognition
import numpy as np

def recognize_faces(image_bgr, known_students, tolerance=0.5):
    """
    Detect faces in the image and match them against known students.
    known_students is a list of tuples: (id, name, roll_no, embedding)
    Returns a list of dictionaries with matching details.
    """
    rgb_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    # Resize frame for faster processing
    small_frame = cv2.resize(rgb_image, (0, 0), fx=0.5, fy=0.5)
    
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)
    
    if not known_students:
        return []

    known_encodings = [s[3] for s in known_students]
    
    results = []
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Scale back up face locations since the frame we detected in was scaled to 1/2 size
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2
        
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=tolerance)
        name = "Unknown"
        student_id = None
        roll_no = None
        confidence = 0.0

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                student = known_students[best_match_index]
                student_id = student[0]
                name = student[1]
                roll_no = student[2]
                distance = face_distances[best_match_index]
                # Convert distance to a pseudo-confidence percentage
                confidence = round((1.0 - distance) * 100, 2)
                
        results.append({
            'student_id': student_id,
            'name': name,
            'roll_no': roll_no,
            'confidence': confidence,
            'box': (top, right, bottom, left)
        })
        
    return results
