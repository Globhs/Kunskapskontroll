import cv2
import numpy as np

def extract_color_histogram(frame, box):
    x1, y1, x2, y2 = box

    h, w, _ = frame.shape

    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w - 1, x2), min(h, y2)

    person_crop = frame[y1:y2, x1:x2]

    if person_crop.size == 0:
        return None
    
    hsv = cv2.cvtColor(person_crop, cv2.COLOR_BGR2HSV)
    
    hist = cv2.calcHist(
        [hsv], 
        [0, 1], 
        None, 
        [30, 32], 
        [0, 180, 0, 256]
    )

    cv2.normalize(hist, hist)
    return hist