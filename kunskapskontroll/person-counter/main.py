import cv2
from detector import detect_people
from tracker import match_positions
from counter import update_count
import config

video = cv2.VideoCapture(config.VIDEO_PATH)

people_count = 1
frame_count = 0
last_count_frame = -config.COOLDOWN_FRAMES
previous_positions = []

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    frame_count += 1

    current_positions, boxes = detect_people(frame, config.CONFIDENCE)
    pairs = match_positions(previous_positions, current_positions)

    delta, last_count_frame = update_count(
        pairs,
        config.LINE_Y,
        config.MARGIN,
        frame_count,
        last_count_frame,
        config.COOLDOWN_FRAMES
    )

    people_count += delta
    previous_positions = current_positions.copy()
    
    for (x1, y1, x2, y2) in boxes:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    cv2.line(frame, (0, config.LINE_Y), (frame.shape[1], config.LINE_Y), (255, 0, 0), 2)
    cv2.putText(frame, f"People: {people_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    cv2.imshow("Person Counter", frame)
    
video.release()
cv2.destroyAllWindows()