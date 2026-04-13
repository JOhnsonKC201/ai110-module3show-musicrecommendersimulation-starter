# Reflection: Profile Comparisons

## Rock Fan vs. Lofi Chill

These two profiles are basically opposites. The Rock Fan wants high energy (0.9), intense mood, and non-acoustic sounds. The Lofi Chill listener wants low energy (0.35), chill mood, and acoustic vibes. Their top 5 lists have zero overlap, which is exactly what you'd expect. Storm Runner (rock, intense, 0.91 energy) topped the Rock list at 0.99, and Library Rain (lofi, chill, 0.35 energy) topped the Lofi list at a perfect 1.0. The system clearly separates users with opposite tastes, which is a good sign that the scoring logic actually works for straightforward cases.

## Pop Dancer vs. Contradictory Profile

This is where things get interesting. Both profiles have genre set to "pop," but the Pop Dancer wants happy mood while the Contradictory user wants melancholy. You'd think the results would look pretty different since the moods are opposite, but the top 2 songs are actually the same — just in a different order. Gym Hero shows up at #2 for Pop Dancer and #1 for Contradictory. That's because Gym Hero is pop (genre match = +3.0) and has high energy, which both profiles want. The mood mismatch only costs 2.0 points, and Gym Hero makes up for some of that with energy closeness. This is basically the system saying "genre matters more than mood," which feels wrong for someone who specifically asked for sad music. A real person wanting melancholy pop would probably hate getting Gym Hero as their top recommendation.

## Genre Ghost vs. Middle of Everything

Neither of these profiles gets great scores, but for different reasons. The Genre Ghost (reggaeton) can never earn the 3.0 genre bonus because reggaeton isn't in the catalog, so scores cap around 0.66. The Middle of Everything profile can technically match genre (pop) but its neutral 0.5 values on everything else mean no single song is a strong match. What's interesting is that the Middle profile's top song (Midnight Coding at 0.64) is actually lofi, not pop, because the chill mood bonus plus the closeness on all the 0.5 values outweighed the genre match. Meanwhile the Genre Ghost's top songs are all happy-mood tracks because that's the only bonus available to them. Both profiles expose how the system struggles when it can't rely on the genre shortcut.

## Rock Fan vs. Pop Dancer

Both of these users know exactly what they want and the system delivers well for both. Storm Runner dominates for Rock Fan, Sunrise City dominates for Pop Dancer. The interesting comparison is the score gaps. Rock Fan has a 0.36 gap between #1 and #2, while Pop Dancer only has a 0.24 gap. That's because there are two pop songs in the catalog (Sunrise City and Gym Hero) but only one rock song (Storm Runner). So the Rock Fan's results drop off a cliff after #1 since nothing else can get the genre bonus. The Pop Dancer has a smoother curve because there's a second pop song to fill the #2 slot. This shows how catalog size directly affects recommendation quality — if you like a well-represented genre, the system works better for you.

## Lofi Chill vs. Middle of Everything

Both profiles have mood set to "chill" and both prefer acoustic sounds, so you'd expect some overlap. And there is — Midnight Coding and Library Rain appear in both top 5 lists, just in different positions. Library Rain is #1 for Lofi Chill (1.0) but #2 for Middle (0.63). The big difference is that Lofi Chill gets the genre bonus on lofi tracks, which pushes them way ahead. The Middle profile doesn't favor lofi specifically, so those songs only win on mood and numerical closeness. This comparison really shows how much the genre bonus acts as a multiplier. Without it, the scores compress into a narrow band where everything feels roughly equal.

## Why Does Gym Hero Keep Showing Up?

Gym Hero appeared in the top 5 for four out of six profiles. For someone who just wants "Happy Pop," seeing a song called "Gym Hero" with an "intense" mood feels weird. The reason it keeps popping up is that it's one of only two pop songs in the catalog, it has very high energy (0.93) and danceability (0.88), and it's non-acoustic. So for any profile that lists pop as their genre, Gym Hero automatically gets +3.0 points, which is enough to beat most non-pop songs even if their mood and energy are a better match. It also sneaks into non-pop profiles because its extreme numerical values happen to be close to what high-energy users want. The fix would be either adding more pop songs to the catalog so there's actual competition, or reducing the genre weight so mood and energy can override a genre match when they're a better fit.
