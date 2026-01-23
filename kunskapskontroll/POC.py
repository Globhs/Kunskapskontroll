import cv2
from ultralytics import YOLO

# Ladda förtränad YOLOv8-modell
model = YOLO("yolov8n.pt")

# Läs in video
video = cv2.VideoCapture("Door_Test4.mp4")

# Linje för vart dörren är
line_y = 350

# håll koll på antal personer
people_count = 1
# för att hålla koll på tidigare positioner av personer
previous_positions = []

# Loop körs så länge videon har frames kvar
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    # Skicka till AI modellen
    results = model(frame, conf=0.4)

    current_positions = []


    for r in results:
        for box in r.boxes:
            #filtrera person klassen 0 = personer i detta dataset
            cls = int(box.cls[0])
            if cls == 0:
                #hämtar hörnen för varje ruta
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                current_positions.append(cy)

                # Rita ruta och mittpunkt på personer
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    # Enkel in/ut-logik (ifall personen y>än dörr linjen = personen har gått in, och tvärtom för ut)
    for prev_y, curr_y in zip(previous_positions, current_positions):
        if prev_y < line_y and curr_y > line_y:
            people_count += 1
        elif prev_y > line_y and curr_y < line_y:
            people_count -= 1

    previous_positions = current_positions

    # Visa resultat
    cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (255, 0, 0), 2)
    cv2.putText(frame, f"People: {people_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

    cv2.imshow("POC - Person Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()