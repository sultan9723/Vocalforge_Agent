import os

INPUT_FOLDER = "inputs"  # make sure this folder exists in same directory

# Average speaking speed: ~150 words/min (you can adjust)
WORDS_PER_MIN = 150

def estimate_duration(words):
    minutes = words / WORDS_PER_MIN
    total_seconds = minutes * 60
    return int(total_seconds // 60), int(total_seconds % 60)

def check_files(folder):
    if not os.path.exists(folder):
        print(f"❌ Folder '{folder}' not found!")
        return

    for file_name in os.listdir(folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                words = len(f.read().split())
                min_dur, sec_dur = estimate_duration(words)
                print(f"{file_name} — {words} words ≈ {min_dur}m {sec_dur}s")

print("✅ Checking all files...")
check_files(INPUT_FOLDER)