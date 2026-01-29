def update_count(pairs, line_y, margin, frame_count, last_count_frame, cooldown):
    delta = 0

    for prev_y, curr_y in pairs:
        if frame_count - last_count_frame < cooldown:
            continue

        if prev_y < line_y - margin and curr_y > line_y + margin:
            delta += 1
            last_count_frame = frame_count

        elif prev_y > line_y + margin and curr_y < line_y - margin:
            delta -= 1
            last_count_frame = frame_count

    return delta, last_count_frame