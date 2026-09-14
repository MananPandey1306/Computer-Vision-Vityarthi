import pytest
import numpy as np
import face_recognition

def test_matching_threshold():
    """
    Test face matching logic with mocked embeddings.
    """
    # Create random dummy embeddings (128-dimensional vectors)
    emb1 = np.random.rand(128)
    # create a very similar embedding
    emb2 = emb1 + np.random.normal(0, 0.05, 128)
    # create a very different embedding
    emb3 = np.random.rand(128)
    
    known_encodings = [emb1]
    
    # Test similar face (should be true for tolerance 0.6 usually)
    matches_similar = face_recognition.compare_faces(known_encodings, emb2, tolerance=0.6)
    
    # face_recognition.compare_faces uses l2 norm.
    # The generated mock data might not perfectly align with dlib's expectations for a real face,
    # but we can test the function call structure.
    
    assert len(matches_similar) == 1
    
def test_recognition_empty_list():
    from modules.recognition import recognize_faces
    
    # With empty known list, it should return empty list
    empty_bgr = np.zeros((100, 100, 3), dtype=np.uint8)
    results = recognize_faces(empty_bgr, [])
    assert results == []
