import os
import random

# === Settings ===
INPUT_FOLDER = "inputs"
TOPIC_FILE = "topics.txt"

durations = (
    [("2:30", 375, 400)] * 200 +
    [("3:00", 450, 480)] * 200 +
    [("3:15", 500, 520)] * 100
)
random.shuffle(durations)

os.makedirs(INPUT_FOLDER, exist_ok=True)

# Load topics
with open(TOPIC_FILE, "r", encoding="utf-8") as f:
    topics = [line.strip() for line in f if line.strip()]

if len(topics) < 500:
    raise ValueError(f"❌ Your topics.txt only has {len(topics)} topics. Please add at least 500.")

# === Sentence templates for speaker paragraphs ===
sentence_templates = [
    "One important aspect of {topic} is that it impacts people differently depending on the context.",
    "{topic} has evolved significantly in recent years due to changes in technology and society.",
    "Many experts believe that {topic} plays a critical role in shaping our future.",
    "Some argue that the challenges of {topic} outweigh the benefits, but others disagree.",
    "In many educational discussions, {topic} is used as a case study for understanding modern issues.",
    "When considering global trends, {topic} cannot be ignored.",
    "From a policy perspective, {topic} requires careful planning and strategic thinking.",
    "Individuals often have very personal experiences when it comes to {topic}.",
    "{topic} is also connected to ethical considerations that deserve attention.",
    "Looking ahead, the implications of {topic} could be profound for the next generation."
]

def generate_paragraph(topic, words_needed, include_title=False, end_with_pause=False):
    paragraph = []

    if include_title:
        # Title aloud with 1-second pause
        paragraph.append(f"{topic}. [PAUSE]")

    # Fill with random discussion sentences
    while len(" ".join(paragraph).split()) < words_needed:
        sentence = random.choice(sentence_templates).format(topic=topic)
        paragraph.append(sentence)

    if end_with_pause:
        paragraph.append("[SHORT PAUSE]")  # 1.5 sec pause between speakers

    return " ".join(paragraph)

# === Create input files ===
for i in range(1, 501):
    filename = f"{INPUT_FOLDER}/input_{i:03d}.txt"
    topic = topics[i - 1]
    label, min_words, max_words = durations[i - 1]
    total_words = random.randint(min_words, max_words)

    # Intro sentence word count
    intro = f"{topic}. Now three of us will discuss this in detail."
    remaining = total_words - len(intro.split())
    per_speaker = remaining // 3

    speaker1 = generate_paragraph(topic, per_speaker, include_title=True, end_with_pause=True)
    speaker2 = generate_paragraph(topic, per_speaker)
    speaker3 = generate_paragraph(topic, per_speaker)

    # Write to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Title: {topic}\n\n")
        f.write(f"Speaker 1: {speaker1}\n\n")
        f.write(f"Speaker 2: {speaker2}\n\n")
        f.write(f"Speaker 3: {speaker3}\n")

print("✅ All 500 input files generated in 'inputs/' folder.")