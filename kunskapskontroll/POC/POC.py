import cv2
from ultralytics import YOLO

# Ladda förtränad YOLOv8-modell
model = YOLO("yolov8n.pt")

# Läs in video
video = cv2.VideoCapture("Door_Test4.mp4")

# Vilken frame vi är på
frame_count = 0

# Senaste framen vi räknade en person(sutten till -10 för att undvika cooldown_frames i början av videon)
last_count_frame = -10

# Antal cooldown frames för att undvika dubbelräkningar
cooldown_frames = 10

# Linje för vart dörren är
line_y = 350

# Margin/tröskelvärde för att undvika jitter
margin = 0
# Antal personer i rummet
people_count = 1

# Vart personen var i tidigare frame
previous_positions = []

# Loop körs så länge videon har frames kvar
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break
    
    frame_count += 1
    # Nuvarande position
    current_positions = []

    # Skicka till AI modellen
    results = model(frame, conf=0.4)


    for r in results:
        for box in r.boxes:
            #filtrera person klassen 0 = personer i detta dataset
            cls = int(box.cls[0])
            if cls == 0:
                #hämtar hörnen för varje ruta
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx = int((x1 + x2) / 2)

                # Kopplar y-position(vertikal) till current_position
                cy = int((y1 + y2) / 2)
                current_positions.append(cy)

                # Rita ruta och mittpunkt på personer
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)



    # In/ut-logik (ifall previous_position > current_position när personen passerar dörren = personen har gått in, och tvärtom ifall previous_position < current_position)
    for prev_y, curr_y in zip(previous_positions, current_positions):
        if frame_count - last_count_frame < cooldown_frames:
            continue  # Hoppa över om vi är i cooldown-perioden

        if prev_y < line_y - margin and curr_y > line_y + margin:
            people_count += 1
            last_count_frame = frame_count

        elif prev_y > line_y + margin and curr_y < line_y - margin:
            people_count -= 1
            last_count_frame = frame_count

    previous_positions = current_positions.copy()

    # Visa resultat
    cv2.line(frame, (0, line_y), (frame.shape[1], line_y), (255, 0, 0), 2)
    cv2.putText(frame, f"People: {people_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

    cv2.imshow("POC - Person Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()