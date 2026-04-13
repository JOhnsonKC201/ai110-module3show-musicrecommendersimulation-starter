"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os, sys

# Allow running as `python -m src.main` from the project root
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print formatted recommendations for a user profile."""
    recs = recommend_songs(user_prefs, songs, k=k)

    print(f"\n{'=' * 60}")
    print(f"  {profile_name}")
    print(f"  Prefs: {user_prefs['genre']} | {user_prefs['mood']} | "
          f"energy={user_prefs['energy']}")
    print(f"{'=' * 60}")
    print(f"  {'#':<4} {'Title':<22} {'Artist':<18} {'Score':>6}")
    print(f"  {'-' * 54}")

    for i, (song, score, explanation) in enumerate(recs, 1):
        print(f"  {i:<4} {song['title']:<22} {song['artist']:<18} {score:>5.2f}")
        reasons = explanation.split("; ")
        for reason in reasons:
            print(f"       -> {reason}")
        print()


def main() -> None:
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
    songs = load_songs(csv_path)

    profiles = {
        "Profile A: Rock Fan": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.90,
            "likes_acoustic": False,
            "valence": 0.45,
            "danceability": 0.65,
        },
        "Profile B: Lofi Chill Listener": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "likes_acoustic": True,
            "valence": 0.60,
            "danceability": 0.55,
        },
        "Profile C: Pop Dancer": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.80,
            "likes_acoustic": False,
            "valence": 0.85,
            "danceability": 0.88,
        },
    }

    for name, prefs in profiles.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
