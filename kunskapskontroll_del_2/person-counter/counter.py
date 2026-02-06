def update_count(pairs, line_y, margin, frame_count, last_count_frame, cooldown):
    """
    Räknar hur många personer som passerar linjen.
    - Gick ner över linjen → delta +1
    - Gick upp över linjen → delta -1
    Cooldown används för att undvika dubbelräkning.
    """
    delta = 0

    for prev, curr in pairs:
        prev_x, prev_y = prev[0], prev[1]
        curr_x, curr_y = curr[0], curr[1]

        if frame_count - last_count_frame < cooldown:
            continue  # cooldown aktiv, hoppa över

        # Gick ner över linjen (in)
        if prev_y < line_y - margin and curr_y > line_y + margin:
            delta += 1
            last_count_frame = frame_count

        # Gick upp över linjen (ut)
        elif prev_y > line_y + margin and curr_y < line_y - margin:
            delta -= 1
            last_count_frame = frame_count

    return delta, last_count_frame
