from music21 import converter, instrument, note, chord

# Load your generated music
music = converter.parse("gpt-v3-id-random2 (1).mid")

# Initialize metrics
num_pitches = set()
num_pitch_classes = set()
polyphony_count = 0
empty_bar_count = 0
total_bars = 0

# Analyze the music
for element in music.flat.notes:
    if isinstance(element, note.Note):
        num_pitches.add(element.name)
        num_pitch_classes.add(element.pitch.pitchClass)
    elif isinstance(element, chord.Chord):
        num_pitches.update(element.pitches)
        num_pitch_classes.update([p.pitchClass for p in element.pitches])
        polyphony_count += 1

# Count empty bars
for measure in music.getElementsByClass("Measure"):
    if not measure.notes:
        empty_bar_count += 1
    total_bars += 1

# Calculate metrics
in_scale_ratio = len(num_pitch_classes) / 12  # Assuming a 12-tone scale
empty_bar_rate = empty_bar_count / total_bars if total_bars > 0 else 0

print(f"Unique Pitches: {len(num_pitches)}")
print(f"Unique Pitch Classes: {len(num_pitch_classes)}")
print(f"Polyphony Count: {polyphony_count}")
print(f"Empty Bar Rate: {empty_bar_rate:.2f}")
print(f"In Scale Ratio: {in_scale_ratio:.2f}")
