from ultralytics import YOLO
import cv2

# Ladda förtränad YOLO-modell
model = YOLO("yolov8n.pt")

previous_positions = []
person_count = 1

def detect_people(frame, conf=0.4):

    # Detektera personer i en frame med YOLO och retunera current_poisitions och boxes
    # current_positions: lista med (cx, cy)
    # boxes: lista med (x1, y1, x2, y2)
 
    global previous_positions, person_count

    current_positions = []
    boxes = []

    results = model(frame, conf=conf)

    for r in results:
        for box in r.boxes:
            # Filtrera på personklass (0)
            if int(box.cls[0]) == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                current_positions.append((cx, cy))
                boxes.append((x1, y1, x2, y2))

    return current_positions, boxes
