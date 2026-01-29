from ultralytics import YOLO

model = YOLO("yolov8n.pt")


previous_positions = []
person_count = 0

def detect_people(frame, conf=0.4):
    global previous_positions, person_count

    current_positions = []
    boxes = []

    results = model(frame, conf=conf)

    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cy = int((y1 + y2) / 2)
                
                current_positions.append(cy)
                boxes.append((x1, y1, x2, y2))

    return current_positions, boxes