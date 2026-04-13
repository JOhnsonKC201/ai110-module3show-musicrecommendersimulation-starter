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

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields converted to int/float."""
    FLOAT_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    INT_FIELDS = {"id"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key in INT_FIELDS:
                row[key] = int(row[key])
            for key in FLOAT_FIELDS:
                row[key] = float(row[key])
            songs.append(row)

    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Score a single song against user prefs; returns (normalized_score, explanation)."""
    MAX_SCORE = 9.0
    total = 0.0
    reasons = []

    # Genre match: +3.0
    if song["genre"] == user_prefs.get("genre"):
        total += 3.0
        reasons.append("genre match (+3.0)")

    # Mood match: +2.0
    if song["mood"] == user_prefs.get("mood"):
        total += 2.0
        reasons.append("mood match (+2.0)")

    # Energy closeness: up to +1.5
    if "energy" in user_prefs:
        energy_score = 1.0 - abs(song["energy"] - user_prefs["energy"])
        points = round(1.5 * energy_score, 3)
        total += points
        reasons.append(f"energy closeness (+{points:.2f})")

    # Valence closeness: up to +1.0
    if "valence" in user_prefs:
        valence_score = 1.0 - abs(song["valence"] - user_prefs["valence"])
        points = round(1.0 * valence_score, 3)
        total += points
        reasons.append(f"valence closeness (+{points:.2f})")

    # Acousticness alignment: +1.0
    if "likes_acoustic" in user_prefs:
        acoustic_match = (
            (user_prefs["likes_acoustic"] and song["acousticness"] > 0.5)
            or (not user_prefs["likes_acoustic"] and song["acousticness"] <= 0.5)
        )
        if acoustic_match:
            total += 1.0
            reasons.append("acoustic preference match (+1.0)")

    # Danceability closeness: up to +0.5
    if "danceability" in user_prefs:
        dance_score = 1.0 - abs(song["danceability"] - user_prefs["danceability"])
        points = round(0.5 * dance_score, 3)
        total += points
        reasons.append(f"danceability closeness (+{points:.2f})")

    normalized = round(total / MAX_SCORE, 4)
    explanation = "; ".join(reasons)
    return normalized, explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort descending, and return the top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
