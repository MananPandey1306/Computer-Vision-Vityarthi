import cv2

def is_live(image_bgr, threshold=100.0):
    """
    Perform a simple liveness check based on blur detection.
    Static/printed photos often have lower variance of Laplacian compared to live webcam feed.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    
    # Calculate the variance of the Laplacian
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # If the focus measure is less than the threshold, it is considered "fake" (blurry/printed)
    if fm < threshold:
        return False, fm
    
    return True, fm
