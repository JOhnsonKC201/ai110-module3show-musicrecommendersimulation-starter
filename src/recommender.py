import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.5
    target_danceability: float = 0.5

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, str]:
        """Score a Song object against a UserProfile; returns (score, explanation)."""
        MAX_SCORE = 9.0
        total = 0.0
        reasons = []

        if song.genre == user.favorite_genre:
            total += 3.0
            reasons.append("genre match (+3.0)")

        if song.mood == user.favorite_mood:
            total += 2.0
            reasons.append("mood match (+2.0)")

        energy_pts = round(1.5 * (1.0 - abs(song.energy - user.target_energy)), 3)
        total += energy_pts
        reasons.append(f"energy closeness (+{energy_pts:.2f})")

        valence_pts = round(1.0 * (1.0 - abs(song.valence - user.target_valence)), 3)
        total += valence_pts
        reasons.append(f"valence closeness (+{valence_pts:.2f})")

        acoustic_match = (
            (user.likes_acoustic and song.acousticness > 0.5)
            or (not user.likes_acoustic and song.acousticness <= 0.5)
        )
        if acoustic_match:
            total += 1.0
            reasons.append("acoustic preference match (+1.0)")

        dance_pts = round(0.5 * (1.0 - abs(song.danceability - user.target_danceability)), 3)
        total += dance_pts
        reasons.append(f"danceability closeness (+{dance_pts:.2f})")

        normalized = round(total / MAX_SCORE, 4)
        return normalized, "; ".join(reasons)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs sorted by score descending."""
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why this song was recommended."""
        _, explanation = self._score(user, song)
        return explanation


# ---------------------------------------------------------------------------
# Scoring modes (Challenge 2)
# ---------------------------------------------------------------------------
# Each mode defines the weight for each feature. The keys must match the
# scoring logic in score_song. Switching modes changes what the system
# prioritizes without touching the algorithm itself.

SCORING_MODES = {
    "balanced": {
        "genre": 3.0, "mood": 2.0, "energy": 1.5, "valence": 1.0,
        "acoustic": 1.0, "danceability": 0.5, "popularity": 0.5,
        "decade": 0.5, "mood_tag": 1.0, "instrumentalness": 0.5,
        "liveness": 0.5,
    },
    "genre-first": {
        "genre": 5.0, "mood": 1.5, "energy": 1.0, "valence": 0.5,
        "acoustic": 1.0, "danceability": 0.5, "popularity": 0.5,
        "decade": 0.5, "mood_tag": 0.5, "instrumentalness": 0.25,
        "liveness": 0.25,
    },
    "mood-first": {
        "genre": 1.0, "mood": 4.0, "energy": 1.5, "valence": 1.5,
        "acoustic": 1.0, "danceability": 0.5, "popularity": 0.5,
        "decade": 0.5, "mood_tag": 2.0, "instrumentalness": 0.5,
        "liveness": 0.5,
    },
    "energy-focused": {
        "genre": 1.5, "mood": 1.0, "energy": 4.0, "valence": 1.0,
        "acoustic": 0.5, "danceability": 1.5, "popularity": 0.5,
        "decade": 0.5, "mood_tag": 0.5, "instrumentalness": 0.25,
        "liveness": 0.25,
    },
}


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields converted to int/float."""
    FLOAT_FIELDS = {
        "energy", "tempo_bpm", "valence", "danceability", "acousticness",
        "instrumentalness", "liveness",
    }
    INT_FIELDS = {"id", "popularity"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key in INT_FIELDS:
                if key in row:
                    row[key] = int(row[key])
            for key in FLOAT_FIELDS:
                if key in row:
                    row[key] = float(row[key])
            songs.append(row)

    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, str]:
    """Score a single song against user prefs; returns (normalized_score, explanation)."""
    weights = SCORING_MODES[mode]
    max_score = sum(weights.values())
    total = 0.0
    reasons = []

    # Genre match
    w = weights["genre"]
    if song["genre"] == user_prefs.get("genre"):
        total += w
        reasons.append(f"genre match (+{w:.1f})")

    # Mood match
    w = weights["mood"]
    if song["mood"] == user_prefs.get("mood"):
        total += w
        reasons.append(f"mood match (+{w:.1f})")

    # Energy closeness
    if "energy" in user_prefs:
        w = weights["energy"]
        pts = round(w * (1.0 - abs(song["energy"] - user_prefs["energy"])), 3)
        total += pts
        reasons.append(f"energy closeness (+{pts:.2f})")

    # Valence closeness
    if "valence" in user_prefs:
        w = weights["valence"]
        pts = round(w * (1.0 - abs(song["valence"] - user_prefs["valence"])), 3)
        total += pts
        reasons.append(f"valence closeness (+{pts:.2f})")

    # Acousticness alignment
    if "likes_acoustic" in user_prefs:
        w = weights["acoustic"]
        acoustic_match = (
            (user_prefs["likes_acoustic"] and song["acousticness"] > 0.5)
            or (not user_prefs["likes_acoustic"] and song["acousticness"] <= 0.5)
        )
        if acoustic_match:
            total += w
            reasons.append(f"acoustic preference match (+{w:.1f})")

    # Danceability closeness
    if "danceability" in user_prefs:
        w = weights["danceability"]
        pts = round(w * (1.0 - abs(song["danceability"] - user_prefs["danceability"])), 3)
        total += pts
        reasons.append(f"danceability closeness (+{pts:.2f})")

    # --- Challenge 1: Advanced features ---

    # Popularity bonus: closer to target = more points (0-100 scale)
    if "target_popularity" in user_prefs and "popularity" in song:
        w = weights["popularity"]
        pts = round(w * (1.0 - abs(song["popularity"] - user_prefs["target_popularity"]) / 100), 3)
        total += pts
        reasons.append(f"popularity closeness (+{pts:.2f})")

    # Decade preference: full points if decade matches, half if adjacent
    if "preferred_decade" in user_prefs and "release_decade" in song:
        w = weights["decade"]
        decade_order = ["1990s", "2000s", "2010s", "2020s"]
        pref_idx = decade_order.index(user_prefs["preferred_decade"]) if user_prefs["preferred_decade"] in decade_order else -1
        song_idx = decade_order.index(song["release_decade"]) if song["release_decade"] in decade_order else -1
        if pref_idx >= 0 and song_idx >= 0:
            gap = abs(pref_idx - song_idx)
            if gap == 0:
                total += w
                reasons.append(f"decade match (+{w:.1f})")
            elif gap == 1:
                pts = round(w * 0.5, 2)
                total += pts
                reasons.append(f"adjacent decade (+{pts:.2f})")

    # Mood tag match: euphoric, nostalgic, aggressive, dreamy
    if "mood_tags" in user_prefs and "mood_tag" in song:
        w = weights["mood_tag"]
        if song["mood_tag"] in user_prefs["mood_tags"]:
            total += w
            reasons.append(f"mood tag '{song['mood_tag']}' match (+{w:.1f})")

    # Instrumentalness closeness
    if "target_instrumentalness" in user_prefs and "instrumentalness" in song:
        w = weights["instrumentalness"]
        pts = round(w * (1.0 - abs(song["instrumentalness"] - user_prefs["target_instrumentalness"])), 3)
        total += pts
        reasons.append(f"instrumentalness closeness (+{pts:.2f})")

    # Liveness closeness
    if "target_liveness" in user_prefs and "liveness" in song:
        w = weights["liveness"]
        pts = round(w * (1.0 - abs(song["liveness"] - user_prefs["target_liveness"])), 3)
        total += pts
        reasons.append(f"liveness closeness (+{pts:.2f})")

    normalized = round(total / max_score, 4)
    explanation = "; ".join(reasons)
    return normalized, explanation


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversity_penalty: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort descending, and return the top k results."""
    scored = []
    for song in songs:
        score, explanation = score_song(user_prefs, song, mode=mode)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)

    if not diversity_penalty:
        return scored[:k]

    # --- Challenge 3: Diversity penalty ---
    # Walk the sorted list and penalize songs whose artist or genre
    # already appears in the picks so far. This pushes variety into
    # the top results without removing songs entirely.
    selected = []
    seen_artists = set()
    seen_genres = set()

    for song, score, explanation in scored:
        penalty = 0.0
        penalty_reasons = []
        if song["artist"] in seen_artists:
            penalty += 0.15
            penalty_reasons.append("repeat artist (-0.15)")
        if song["genre"] in seen_genres:
            penalty += 0.10
            penalty_reasons.append("repeat genre (-0.10)")

        adjusted = round(max(score - penalty, 0), 4)
        if penalty_reasons:
            explanation += "; " + "; ".join(penalty_reasons)

        selected.append((song, adjusted, explanation))
        seen_artists.add(song["artist"])
        seen_genres.add(song["genre"])

    selected.sort(key=lambda x: x[1], reverse=True)
    return selected[:k]
