import os
import re
import random

# ---------- SETTINGS ----------
INPUT_FOLDER = "inputs"
OUTPUT_FOLDER = "adjusted_files"

# Approx words per second (depends on TTS speed)
WORDS_PER_SECOND = 2.5  # adjust if needed
MIN_DURATION = 150  # 2 min 30 sec
MAX_DURATION = 240  # 4 min

# Calculate word range based on duration
MIN_WORDS = int(MIN_DURATION * WORDS_PER_SECOND)
MAX_WORDS = int(MAX_DURATION * WORDS_PER_SECOND)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


def clean_text_logically(text):
    """
    Removes only full sentences that are less important,
    but keeps the conversational flow and filler words.
    """

    # Split by sentences (keeping punctuation)
    sentences = re.split(r'(?<=[.!?]) +', text.strip())

    # If already within range, return as is
    if MIN_WORDS <= len(text.split()) <= MAX_WORDS:
        return text

    # If too long, start removing least important sentences
    while len(" ".join(sentences).split()) > MAX_WORDS and len(sentences) > 3:
        # Randomly remove one sentence that does NOT contain speaker intro or closing
        removable = [s for s in sentences if not s.strip().startswith(("Speaker", "Title", "Closing"))]
        if removable:
            sentence_to_remove = random.choice(removable)
            sentences.remove(sentence_to_remove)
        else:
            break

    return " ".join(sentences)


def process_files():
    for file_name in os.listdir(INPUT_FOLDER):
        if file_name.endswith(".txt"):
            file_path = os.path.join(INPUT_FOLDER, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Process only the main discussion part (not the title/speaker tags)
            adjusted_content = clean_text_logically(content)

            # Save to adjusted_files folder
            output_path = os.path.join(OUTPUT_FOLDER, file_name)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(adjusted_content)

            word_count = len(adjusted_content.split())
            print(f"Processed {file_name} → {word_count} words")

    print(f"\n✅ All adjusted files saved in '{OUTPUT_FOLDER}' folder.")


if __name__ == "__main__":
    process_files()