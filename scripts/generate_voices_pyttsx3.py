import os
import sys
import re
import time
import random
import pyttsx3
from xml.sax.saxutils import escape
from pydub import AudioSegment

# === Duration Limits (in seconds) ===
MIN_TOTAL_SEC = 150  # 2:30 min
MAX_TOTAL_SEC = 215  # 3:35 min

# === Voice Selection (Male → Female → Male with DISTINCT ACCENT) ===
VOICE_SETUP = [
    {"gender": "male", "accent": ["david", "guy", "zira"]},       # Speaker 1: US Male
    {"gender": "female", "accent": ["zira", "jenny", "female"]},  # Speaker 2: US Female
    {"gender": "male", "accent": ["brian", "george", "uk"]}       # Speaker 3: UK Male (Distinct)
]

# === File Selection ===
input_number = sys.argv[1] if len(sys.argv) > 1 else "001"
input_file = f"inputs/input_{input_number}.txt"
print(f"\n📄 Processing file: {input_file}")

# === Read & Clean Text ===
def clean_line(line):
    line = line.strip()
    # ✅ Remove Speaker Titles and Phrases like "As Speaker 1"
    line = re.sub(r"^(Title|Speaker 1|Speaker 2|Speaker 3|Closing Line):", "", line, flags=re.IGNORECASE).strip()
    line = re.sub(r"As Speaker \d+.*", "", line, flags=re.IGNORECASE)
    line = re.sub(r"\[.*?\]", "", line)
    line = re.sub(r"\(.*?\)", "", line)
    return line

with open(input_file, "r", encoding="utf-8") as f:
    cleaned_lines = list(filter(None, [clean_line(line) for line in f.readlines()]))

if len(cleaned_lines) < 4:
    raise ValueError("⚠ File must have: Title + 3 Speaker paragraphs + Closing Line.")

title = cleaned_lines[0]
speaker_texts = [f"{title}. {cleaned_lines[1]}", cleaned_lines[2], cleaned_lines[3]]

# === Adjust Text to Meet Total Duration ===
def adjust_texts_for_duration(texts):
    total_words = sum(len(t.split()) for t in texts)
    est_total_sec = total_words / 2.2

    if est_total_sec > MAX_TOTAL_SEC:
        while est_total_sec > MAX_TOTAL_SEC:
            longest = max(range(len(texts)), key=lambda i: len(texts[i].split()))
            texts[longest] = " ".join(texts[longest].split()[:-5])
            est_total_sec = sum(len(t.split()) for t in texts) / 2.2

    elif est_total_sec < MIN_TOTAL_SEC:
        fillers = [
            "That’s actually a really good point.",
            "I think that makes a lot of sense.",
            "Yeah, that’s true when you think about it carefully."
        ]
        while est_total_sec < MIN_TOTAL_SEC:
            idx = random.randint(0, len(texts)-1)
            texts[idx] += " " + random.choice(fillers)
            est_total_sec = sum(len(t.split()) for t in texts) / 2.2

    print(f"✅ Adjusted Total Estimated Duration ≈ {round(est_total_sec//60)}m {round(est_total_sec%60)}s")
    return texts

speaker_texts = adjust_texts_for_duration(speaker_texts)
os.makedirs("output", exist_ok=True)

# === Generate Speaker Voice ===
def generate_voice(idx, text, out_file):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    selected = None
    for v in voices:
        for accent in VOICE_SETUP[idx]["accent"]:
            if accent.lower() in v.name.lower():
                selected = v.id
                break
        if selected:
            break
    if selected:
        engine.setProperty('voice', selected)

    word_count = len(text.split())
    rate = 150 if 150 <= word_count / 2.0 <= 215 else 160
    engine.setProperty('rate', rate)

    wav_file = out_file.replace(".mp3", ".wav")
    print(f"🎙 Speaker {idx+1} → {wav_file} (Rate: {rate})")

    engine.save_to_file(text, wav_file)
    engine.runAndWait()
    engine.stop()
    time.sleep(1)

    audio = AudioSegment.from_wav(wav_file)
    audio.export(out_file, format="mp3")
    os.remove(wav_file)

    dur = round(audio.duration_seconds)
    print(f"✅ Saved: {out_file} — {dur//60}m {dur%60}s")

# === Main Loop ===
for i, txt in enumerate(speaker_texts):
    generate_voice(i, txt, f"output/speaker{i+1}_{input_number}.mp3")

print("\n🎉 All done! Voices saved in /output folder.")