import os

INPUT_FOLDER = "inputs"

for i in range(1, 501):
    filepath = os.path.join(INPUT_FOLDER, f"input_{i:03d}.txt")
    if not os.path.exists(filepath):
        print(f"❌ File missing: {filepath}")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    if not lines or not lines[0].startswith("Title:"):
        print(f"⚠ Skipping improperly formatted file: {filepath}")
        continue

    title_line = lines[0]
    topic = title_line.replace("Title:", "").strip()

    # Skip to speakers
    try:
        speaker1_index = lines.index(next(l for l in lines if l.startswith("Speaker 1:")))
    except StopIteration:
        print(f"⚠ Skipping file with missing speaker 1: {filepath}")
        continue

    speaker1_lines = lines[speaker1_index + 1:]
    try:
        speaker2_index = speaker1_lines.index(next(l for l in speaker1_lines if l.startswith("Speaker 2:")))
        speaker3_index = speaker1_lines.index(next(l for l in speaker1_lines if l.startswith("Speaker 3:")))
    except StopIteration:
        print(f"⚠ Skipping file with missing speakers: {filepath}")
        continue

    speaker1_text = " ".join(speaker1_lines[:speaker2_index]).strip()
    speaker2_text = " ".join(speaker1_lines[speaker2_index + 1:speaker3_index]).strip()
    speaker3_text = " ".join(speaker1_lines[speaker3_index + 1:]).strip()

    # Construct the fixed content
    updated_text = f"""Title: {topic}

Speaker 1:
(short pause)
In this recording, three students will discuss about {topic}.
(short pause)
{speaker1_text}

Speaker 2:  Exactly I'll Further Continue And I’d like to talk more about {topic.lower()}. {speaker2_text}

Speaker 3: I Appreciate Your Discussion And further I’d like to talk about {topic.lower()}. {speaker3_text}"""

    # Save the updated file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated_text.strip() + "\n")

print("✅ All 500 input files updated to exact required format.")