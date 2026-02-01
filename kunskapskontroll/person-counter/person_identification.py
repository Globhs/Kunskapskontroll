class PersonIdentifier:
    """
    Hanterar ID-spårning baserat på position (cx, cy).
    - tracks: id -> {"cx","cy","last_seen"}
    - next_id: nästa tilldelade ID
    - max_distance: max avstånd för att matcha en person
    - max_lost: antal frames en person kan vara borta innan spår tas bort
    """
    def __init__(self, max_distance=50, max_lost=40):
        self.next_id = 0
        self.tracks = {}  # id -> tracking info (dict)
        self.max_distance = max_distance
        self.max_lost = max_lost

    def update(self, current_positions, frame_count):
        updated_tracks = {}
        used_ids = set()

        for cx, cy in current_positions:
            matched_id = None
            min_dist = self.max_distance

            # försök match med redan sedda personer
            for pid, track in self.tracks.items():
                dist = ((track["cx"] - cx) ** 2 + (track["cy"] - cy) ** 2) ** 0.5
                if dist < min_dist and pid not in used_ids:
                    min_dist = dist
                    matched_id = pid

            if matched_id is not None:
                # uppdatera spår
                updated_tracks[matched_id] = {
                    "cx": cx,
                    "cy": cy,
                    "last_seen": frame_count
                }
                used_ids.add(matched_id)
            else:
                # skapa nytt ID
                updated_tracks[self.next_id] = {
                    "cx": cx,
                    "cy": cy,
                    "last_seen": frame_count
                }
                used_ids.add(self.next_id)
                self.next_id += 1

        # behåll spår som är försvunna men inte för länge
        for pid, track in self.tracks.items():
            if pid not in updated_tracks:
                if frame_count - track["last_seen"] <= self.max_lost:
                    updated_tracks[pid] = track

        self.tracks = updated_tracks
        return updated_tracks
