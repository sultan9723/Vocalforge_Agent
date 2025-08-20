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

def generate_paragraph(topic, speaker_id, words_needed):
    paragraph = [f"As speaker {speaker_id}, I’d like to talk about {topic.lower()}."]
    while len(" ".join(paragraph).split()) < words_needed:
        sentence = random.choice(sentence_templates).format(topic=topic)
        paragraph.append(sentence)
    return " ".join(paragraph)

# === Create input files ===
for i in range(1, 501):
    filename = f"{INPUT_FOLDER}/input_{i:03d}.txt"
    topic = topics[i - 1]
    label, min_words, max_words = durations[i - 1]
    total_words = random.randint(min_words, max_words)

    # Title + Speaker 1 introduction (3 short lines)
    intro_lines = [
        f"{topic}.",
        "(short pause)",
        f"In this recording, three students will discuss about {topic}.",
        "(short pause)"
    ]
    intro = "\n".join(intro_lines)
    intro_word_count = sum(len(line.split()) for line in intro_lines)

    # Divide remaining words among speakers
    remaining = total_words - intro_word_count
    per_speaker = remaining // 3

    speaker1 = generate_paragraph(topic, 1, per_speaker)
    speaker2 = generate_paragraph(topic, 2, per_speaker)
    speaker3 = generate_paragraph(topic, 3, per_speaker)

    # Write to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Title: {topic}\n\n")
        f.write(f"Speaker 1: {intro}\n{speaker1}\n\n")
        f.write(f"Speaker 2: {speaker2}\n\n")
        f.write(f"Speaker 3: {speaker3}\n")

print("✅ All 500 input files generated in 'inputs/' with correct intro line.")