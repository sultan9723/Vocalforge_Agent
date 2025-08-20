import os
import re
import random

INPUT_FOLDER = "inputs"
MIN_WORDS = 350
MAX_WORDS = 535  # strict maximum

FILLERS = [
    "That’s actually a really good point, by the way.",
    "I think that makes a lot of sense, honestly.",
    "Yeah, that’s true when you think about it carefully.",
    "I feel like we can definitely agree on that.",
    "That’s a really interesting way to look at it."
]

def get_word_count(text):
    return len(text.split())

def extract_speakers(text):
    parts = re.split(r"(Speaker \d+:|Closing Line:)", text)
    return [p.strip() for p in parts if p.strip()]

def rebuild_text(sections):
    text = ""
    i = 0
    while i < len(sections):
        if sections[i].startswith("Speaker") or sections[i].startswith("Closing"):
            text += sections[i] + " " + sections[i + 1] + "\n"
            i += 2
        else:
            text += sections[i] + "\n"
            i += 1
    return text.strip()

def suggest_sentence_removal(speaker_text):
    sentences = re.split(r'(?<=[.!?]) +', speaker_text)
    long_sentences = [s for s in sentences if len(s.split()) > 8]
    return random.choice(long_sentences) if long_sentences else None

def adjust_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words = get_word_count(text)
    sections = extract_speakers(text)

    for i in range(len(sections)):
        if sections[i].startswith("Speaker"):
            dialogue = sections[i + 1]

            # Trim if too long
            while words > MAX_WORDS:
                to_remove = suggest_sentence_removal(dialogue)
                if not to_remove:
                    break
                dialogue = dialogue.replace(to_remove, "")
                sections[i + 1] = dialogue
                words = get_word_count(rebuild_text(sections))

            # Fill if too short
            while words < MIN_WORDS:
                filler = random.choice(FILLERS)
                dialogue += " " + filler
                sections[i + 1] = dialogue
                words = get_word_count(rebuild_text(sections))

    updated_text = rebuild_text(sections)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated_text)

    duration = round(words / 2.5)
    print(f"✔ {os.path.basename(filepath)} — {words} words ≈ {duration//60}m {duration%60}s")

def main():
    print("📂 Adjusting all files to 350–535 words...")
    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".txt"):
            adjust_file(os.path.join(INPUT_FOLDER, file))
    print("\n✅ All files are now between 350–535 words!")

if __name__== "__main__":
    main()