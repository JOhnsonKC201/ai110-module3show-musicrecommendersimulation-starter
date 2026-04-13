# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

This recommender suggests the top 5 songs from a small catalog based on a user's preferred genre, mood, energy level, and a few other taste preferences. It's built for classroom exploration only, not for real users. It assumes the user knows what genre and mood they want and that those preferences stay constant, which obviously isn't how real people work but it keeps the system simple enough to learn from.

---

## 3. How the Model Works

The system takes your taste profile and compares it against every song in the catalog. For each song, it calculates a score based on how well the song matches what you said you like.

Genre match is the biggest factor — if a song is in your favorite genre, it gets a big boost right away. Mood match is the second biggest. After that, the system looks at numerical traits like energy, valence (how positive the song sounds), danceability, and whether the song is acoustic or electronic. For the number-based traits, it measures how close the song's value is to your target — so if you want energy at 0.8 and a song is at 0.82, that's almost a perfect score on that trait.

All the points get added up and normalized to a 0-to-1 scale. Then every song gets sorted from highest to lowest, and the system gives you the top 5 with an explanation of exactly why each one scored the way it did.

---

## 4. Data

The catalog has 20 songs in `data/songs.csv`. The original starter had 10 and I added 10 more to cover genres that were missing like r&b, electronic, folk, hip-hop, classical, latin, and metal.

Each song has these attributes: genre, mood, energy (0-1), tempo in BPM, valence (0-1), danceability (0-1), and acousticness (0-1). The numerical values were assigned by hand based on how the songs feel, which means they reflect my personal interpretation. Someone else might rate the same songs differently.

There are 14 different genres represented but most only have one song each, so if your taste falls in a less common genre the system has fewer options to pick from. Pop and lofi have the most representation with 2 songs each.

---

## 5. Strengths

- When someone has a clear, mainstream preference (like "pop and happy" or "lofi and chill"), the system nails it. The top recommendations genuinely feel like songs that person would enjoy.
- The explanations are actually useful. You can look at the reasons and understand exactly why a song was recommended, which is more transparency than most real apps give you.
- It handles the "lofi chill" listener particularly well — Library Rain scored a perfect 1.0 because it matches on literally every dimension.
- The system is simple enough that you can predict what it'll do, which makes it a good learning tool even if it's not production-ready.

---

## 6. Limitations and Bias

The genre weight at 3.0 out of 9.0 total points means genre controls about a third of the entire score. In practice this creates a filter bubble — once you say you like pop, the system will almost always recommend pop songs first, even if there's a latin or indie pop track that matches your mood and energy way better. I saw this with the Pop Dancer profile where Gym Hero (pop, intense) ranked #2 despite having the wrong mood, while Fuego Lento (latin, happy) which actually matched the mood got pushed to #3.

The system also has a blind spot for users with niche tastes. If your favorite genre isn't in the 20-song catalog at all (like reggaeton), you can never earn the genre bonus, so your scores are automatically capped lower. That's not because the recommendations are bad, it's just a math problem — the system penalizes you for liking something it doesn't have.

Another issue is that everyone gets treated the same way. Some people care way more about mood than genre, or they want variety instead of five songs that all sound the same. The system has no way to learn that or adapt. It also doesn't understand lyrics, cultural context, or what a song is actually about — two songs can have identical numerical profiles but be completely different experiences.

---

## 7. Evaluation

I tested with six user profiles:

- **Rock Fan** (rock, intense, 0.9 energy): Storm Runner won at 0.99. Felt right — it's literally the only rock song in the catalog and it's intense with high energy. The gap between #1 and #2 was 0.36, which showed how much genre dominates.
- **Lofi Chill** (lofi, chill, 0.35 energy): Library Rain got a perfect 1.0. Also felt right. Both top lofi songs matched perfectly.
- **Pop Dancer** (pop, happy, 0.8 energy): Sunrise City at 0.99. Solid pick. But Gym Hero at #2 felt a bit off since the user wanted "happy" and Gym Hero is "intense."
- **Contradictory** (pop, melancholy, 0.95 energy): This exposed a real weakness. The user wants high energy but sad vibes. The system gave them upbeat pop songs instead of actually sad songs, because genre outweighed mood.
- **Genre Ghost** (reggaeton): No song matched the genre so all scores capped around 0.66. Results were reasonable but the confidence was artificially low.
- **Middle of Everything** (all 0.5): Mood-matched songs beat genre-matched songs because the numerical closeness calculations favored moderate values.

I also ran a weight experiment where I halved genre (3.0 to 1.5) and doubled energy (1.5 to 3.0). The results felt slightly more fair — the gap between same-genre and different-genre songs shrank, and the Genre Ghost profile's scores went from 0.66 to 0.82. But for users with strong genre preferences, the original weights probably feel more right.

The thing that surprised me most was how the contradictory profile exposed the genre-over-mood problem. I expected the system to at least put one melancholy song in the top 3 for someone who specifically asked for melancholy, but it didn't.

---

## 8. Future Work

- Let users set their own weights so someone who cares more about mood than genre can express that.
- Add a diversity penalty so the top 5 aren't all from the same genre or mood. Real recommenders do this on purpose.
- Build in some randomness or "exploration" factor to occasionally suggest songs outside the user's comfort zone.
- Expand the catalog a lot. 20 songs isn't enough to see how the system behaves at scale.
- Add tempo as a scoring factor — right now we track it in the CSV but don't use it in the scoring.
- Support multiple profiles per user so you can have a "workout" profile and a "study" profile.

---

## 9. Personal Reflection

Building this taught me that recommender systems are basically just opinion machines with math on top. Every single choice I made — how much genre should matter, what "energy" means, which songs to include — baked my own biases into the output. The system feels objective because it uses numbers, but those numbers came from subjective decisions.

The thing that stuck with me most is how the contradictory profile handled things. A real person who wants "high energy but sad" is probably thinking of something specific, like intense emo music or aggressive rap about heartbreak. My system can't understand that because it treats each feature independently. It doesn't know that certain combinations of traits map to real subcultures or vibes that people actually experience. That gap between what the numbers describe and what the music actually feels like is where human judgment still matters, no matter how good the algorithm gets.
