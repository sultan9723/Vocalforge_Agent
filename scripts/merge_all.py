import os
from pydub import AudioSegment

INPUT_DIR = "output"
FINAL_DIR = "final"
TOTAL_FILES = 500  # Set to 500; it will skip ones not generated

# Create the final output directory if it doesn't exist
os.makedirs(FINAL_DIR, exist_ok=True)

print("🔄 Merging all available speaker voices into final outputs...\n")

for i in range(1, TOTAL_FILES + 1):
    file_number = str(i).zfill(3)
    speaker1_file = os.path.join(INPUT_DIR, f"speaker1_{file_number}.mp3")
    speaker2_file = os.path.join(INPUT_DIR, f"speaker2_{file_number}.mp3")
    speaker3_file = os.path.join(INPUT_DIR, f"speaker3_{file_number}.mp3")
    final_file = os.path.join(FINAL_DIR, f"final_{file_number}.mp3")

    if not (os.path.exists(speaker1_file) and os.path.exists(speaker2_file) and os.path.exists(speaker3_file)):
        print(f"[!] Skipping input_{file_number}: One or more speaker files missing")
        continue

    try:
        s1 = AudioSegment.from_mp3(speaker1_file)
        s2 = AudioSegment.from_mp3(speaker2_file)
        s3 = AudioSegment.from_mp3(speaker3_file)
        pause = AudioSegment.silent(duration=1000)  # 1-second pause

        final = s1 + pause + s2 + pause + s3
        final.export(final_file, format="mp3")
        print(f"✅ Merged: final_{file_number}.mp3")
    except Exception as e:
        print(f"[!] Error with input_{file_number}: {e}")

print("\n✅ Merging completed for all available files.")