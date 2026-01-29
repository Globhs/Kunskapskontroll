def match_positions(previous, current):
    pairs = []
    used = set()

    for cy in current:
        if not previous:
            continue
            # Tracking logik:Från tidigare positioner välj den som ligger närmast personens nuvarande position
        closest = min(previous, key=lambda py: abs(py - cy))
        if closest not in used:
            used.add(closest)
            pairs.append((closest, cy))

    return pairs