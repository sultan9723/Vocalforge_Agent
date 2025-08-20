from pydub import AudioSegment
import os
import sys

# === Get input number ===
input_number = sys.argv[1] if len(sys.argv) > 1 else "001"
print(f"\n🔀 Merging voices for input {input_number}...")

# === Paths to individual speaker files ===
speaker_files = [
    f"output/speaker1_{input_number}.mp3",
    f"output/speaker2_{input_number}.mp3",
    f"output/speaker3_{input_number}.mp3"
]

# === Output folder ===
os.makedirs("final", exist_ok=True)
final_path = f"final/final_{input_number}.mp3"

# === Create silence between speakers ===
silence = AudioSegment.silent(duration=1000)  # 1 second pause

# === Load and merge files ===
combined = AudioSegment.empty()

for i, file in enumerate(speaker_files):
    if not os.path.exists(file):
        print(f"❌ Missing file: {file}")
        continue

    print(f"✅ Adding: {file}")
    audio = AudioSegment.from_mp3(file)
    combined += audio

    if i < len(speaker_files) - 1:
        combined += silence

# === Export merged file ===
if len(combined) > 0:
    combined.export(final_path, format="mp3")
    print(f"🎧 Merged audio saved to: {final_path}")
else:
    print("❌ No audio files merged. Please check if speaker files exist.")