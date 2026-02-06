def match_positions(previous, current):
    """
    Kopplar ihop personer mellan frames baserat på närmaste position.
    previous: lista med (cx, cy)
    current: lista med (cx, cy)
    Returnerar en lista av par: (previous, current)
    """
    pairs = []
    used = set()

    for cx, cy in current:
        if not previous:
            continue

        # Välj närmaste tidigare position
        closest = min(
            previous,
            key=lambda p: ((p[0] - cx) ** 2 + (p[1] - cy) ** 2) ** 0.5
        )
        prev_cx, prev_cy = closest

        if (prev_cx, prev_cy) not in used:
            used.add((prev_cx, prev_cy))
            pairs.append((closest, (cx, cy)))

    return pairs
