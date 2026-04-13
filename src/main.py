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
from tabulate import tabulate


def print_recommendations(
    profile_name: str,
    user_prefs: dict,
    songs: list,
    k: int = 5,
    mode: str = "balanced",
    diversity_penalty: bool = False,
) -> None:
    """Print formatted recommendations for a user profile using tabulate."""
    recs = recommend_songs(user_prefs, songs, k=k, mode=mode, diversity_penalty=diversity_penalty)

    flags = f"mode={mode}"
    if diversity_penalty:
        flags += " | diversity=on"

    print(f"\n{'=' * 72}")
    print(f"  {profile_name}")
    print(f"  Prefs: {user_prefs['genre']} | {user_prefs['mood']} | "
          f"energy={user_prefs['energy']}")
    print(f"  [{flags}]")
    print(f"{'=' * 72}")

    # Build table rows
    rows = []
    for i, (song, score, explanation) in enumerate(recs, 1):
        reasons = "\n".join(f"  {r}" for r in explanation.split("; "))
        rows.append([i, song["title"], song["artist"], f"{score:.2f}", reasons])

    print(tabulate(
        rows,
        headers=["#", "Title", "Artist", "Score", "Reasons"],
        tablefmt="grid",
        colalign=("right", "left", "left", "right", "left"),
    ))
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
            "target_popularity": 60,
            "preferred_decade": "2010s",
            "mood_tags": ["aggressive"],
            "target_instrumentalness": 0.15,
            "target_liveness": 0.35,
        },
        "Profile B: Lofi Chill Listener": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "likes_acoustic": True,
            "valence": 0.60,
            "danceability": 0.55,
            "target_popularity": 40,
            "preferred_decade": "2020s",
            "mood_tags": ["nostalgic", "dreamy"],
            "target_instrumentalness": 0.70,
            "target_liveness": 0.05,
        },
        "Profile C: Pop Dancer": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.80,
            "likes_acoustic": False,
            "valence": 0.85,
            "danceability": 0.88,
            "target_popularity": 80,
            "preferred_decade": "2020s",
            "mood_tags": ["euphoric"],
            "target_instrumentalness": 0.05,
            "target_liveness": 0.15,
        },
        # --- Edge-case / adversarial profiles ---
        "Profile D: Contradictory (high energy + sad mood)": {
            "genre": "pop",
            "mood": "melancholy",
            "energy": 0.95,
            "likes_acoustic": False,
            "valence": 0.20,
            "danceability": 0.80,
            "target_popularity": 50,
            "preferred_decade": "2020s",
            "mood_tags": ["nostalgic"],
            "target_instrumentalness": 0.10,
            "target_liveness": 0.20,
        },
        "Profile E: Genre Ghost (genre not in catalog)": {
            "genre": "reggaeton",
            "mood": "happy",
            "energy": 0.70,
            "likes_acoustic": False,
            "valence": 0.80,
            "danceability": 0.85,
            "target_popularity": 75,
            "preferred_decade": "2020s",
            "mood_tags": ["euphoric"],
            "target_instrumentalness": 0.05,
            "target_liveness": 0.20,
        },
        "Profile F: Middle of Everything (all 0.5)": {
            "genre": "pop",
            "mood": "chill",
            "energy": 0.50,
            "likes_acoustic": True,
            "valence": 0.50,
            "danceability": 0.50,
            "target_popularity": 50,
            "preferred_decade": "2010s",
            "mood_tags": ["dreamy", "nostalgic"],
            "target_instrumentalness": 0.50,
            "target_liveness": 0.30,
        },
    }

    # --- Balanced mode (default) ---
    print("\n" + "=" * 72)
    print("  SCORING MODE: balanced")
    print("=" * 72)
    for name, prefs in profiles.items():
        print_recommendations(name, prefs, songs, mode="balanced")

    # --- Demonstrate alternative scoring modes (Challenge 2) ---
    demo_profile = profiles["Profile C: Pop Dancer"]
    for mode in ["genre-first", "mood-first", "energy-focused"]:
        print_recommendations(
            f"Profile C: Pop Dancer",
            demo_profile, songs, mode=mode,
        )

    # --- Demonstrate diversity penalty (Challenge 3) ---
    print_recommendations(
        "Profile C: Pop Dancer (with diversity penalty)",
        demo_profile, songs, mode="balanced", diversity_penalty=True,
    )


if __name__ == "__main__":
    main()
