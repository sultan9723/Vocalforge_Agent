import os
import re
import openai
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()

# === CONFIG ===
openai_key = os.getenv("OPENAI_API_KEY")
INPUT_DIR = "inputs"
TARGETS = {
    "2:30": (450, 470),
    "3:00": (530, 550),
    "3:15": (580, 600)
}

# === Select Target Durations ===
target_distribution = {
    "2:30": 200,
    "3:00": 200,
    "3:15": 100
}

# === Count words ===
def count_words(text):
    return len(re.findall(r'\b\w+\b', text))

# === Expand text using OpenAI ===
def expand_paragraph(paragraph, topic, target_words):
    prompt = f"""
You are an academic discussion assistant. Your job is to rewrite the following paragraph in a more detailed, academic, and natural style, without adding filler or repeating the same points.

Topic: {topic}

Paragraph:
{paragraph}

Expand it to approximately {target_words} words while keeping the meaning, improving flow, and sounding like a human speaker in a discussion.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI Error:", e)
        return paragraph

# === Read all input files ===
input_files = sorted([f for f in os.listdir(INPUT_DIR) if f.startswith("input_") and f.endswith(".txt")])
total_targets = sum(target_distribution.values())

# === Assign target durations ===
assigned_targets = {}
counter = {"2:30": 0, "3:00": 0, "3:15": 0}
for fname in input_files:
    for dur, limit in target_distribution.items():
        if counter[dur] < limit:
            assigned_targets[fname] = dur
            counter[dur] += 1
            break

# === Process files ===
for fname in tqdm(input_files, desc="Expanding Inputs"):
    path = os.path.join(INPUT_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) < 4:
        continue  # Skip incomplete files

    title = re.sub(r'^Title:\s*', '', lines[0], flags=re.I)
    speakers = [re.sub(r'^Speaker \d:\s*', '', l, flags=re.I) for l in lines[1:4]]

    full_text = " ".join(speakers)
    current_words = count_words(full_text)

    target_label = assigned_targets.get(fname)
    if not target_label:
        continue

    min_words, max_words = TARGETS[target_label]
    if current_words >= min_words:
        continue  # Already long enough

    # === Expand each speaker paragraph proportionally ===
    target_total = (min_words + max_words) // 2
    ratio = target_total / current_words
    target_counts = [int(count_words(p) * ratio) for p in speakers]

    expanded = []
    for i, (para, count) in enumerate(zip(speakers, target_counts)):
        expanded.append(expand_paragraph(para, title, count))

    # === Save file back ===
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n")
        for i, para in enumerate(expanded):
            f.write(f"Speaker {i+1}: {para}\n\n")

print("\n✅ Done! All short inputs have been expanded to meet target durations.") 