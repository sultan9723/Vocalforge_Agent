import os
import re

# Configurations
INPUT_DIR = "inputs"
START_INDEX = 1
END_INDEX = 500
TARGET_MIN = 490
TARGET_MAX = 510
HARD_LIMIT = 520

def count_words(text):
    return len(re.findall(r'\w+', text))

def remove_blank_lines(text):
    return "\n".join([line for line in text.splitlines() if line.strip()])

def extract_parts(text):
    """
    Returns title, speaker_blocks, and closing line.
    Keeps the structure safe.
    """
    lines = text.strip().splitlines()
    title = lines[0].strip()

    intro_line_index = 3  # Assuming fixed intro format
    intro_lines = lines[1:intro_line_index + 1]

    speakers = []
    current_speaker = None
    current_body = []

    for line in lines[intro_line_index + 1:]:
        if line.strip().startswith("Speaker"):
            if current_speaker:
                speakers.append((current_speaker, "\n".join(current_body).strip()))
            current_speaker = line.strip()
            current_body = []
        else:
            current_body.append(line)

    # Separate final line
    if current_body and "Thank you for your valuable contributions" in current_body[-1]:
        closing_line = current_body[-1].strip()
        current_body = current_body[:-1]
    else:
        closing_line = "And with that, we are ending the discussion here. Thank you for your valuable contributions and insights."

    speakers.append((current_speaker, "\n".join(current_body).strip()))

    return title, intro_lines, speakers, closing_line

def trim_paragraphs(speaker_blocks, target_total_words):
    full_text = " ".join([body for _, body in speaker_blocks])
    all_words = re.findall(r'\w+', full_text)

    if len(all_words) <= target_total_words:
        return speaker_blocks  # no trimming

    trim_count = len(all_words) - target_total_words
    words_left = all_words[:-trim_count]

    trimmed_blocks = []
    for header, body in speaker_blocks:
        body_words = re.findall(r'\w+', body)
        take_count = min(len(words_left), len(body_words))
        new_body = " ".join(words_left[:take_count])
        words_left = words_left[take_count:]
        trimmed_blocks.append((header, new_body.strip()))

    return trimmed_blocks

def rebuild_text(title, intro_lines, speaker_blocks, closing_line):
    result = [title.strip(), ""]
    result.extend(intro_lines)
    for header, body in speaker_blocks:
        result.append(f"{header}\n{body.strip()}")
    result.append("")
    result.append(closing_line)
    return "\n".join(result)

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    clean_text = remove_blank_lines(content)
    original_word_count = count_words(clean_text)

    if original_word_count <= HARD_LIMIT:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(clean_text)
        print(f"[✓] Cleaned: {os.path.basename(file_path)} ({original_word_count} words)")
        return

    # Need to trim
    title, intro_lines, speaker_blocks, closing_line = extract_parts(clean_text)
    trimmed_blocks = trim_paragraphs(speaker_blocks, TARGET_MAX)
    final_text = rebuild_text(title, intro_lines, trimmed_blocks, closing_line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_text)

    final_word_count = count_words(final_text)
    print(f"[✂] Trimmed: {os.path.basename(file_path)} from {original_word_count} → {final_word_count} words")

def main():
    print("🚀 Cleaning & Trimming Inputs (001–500)...\n")
    for i in range(START_INDEX, END_INDEX + 1):
        filename = f"input_{str(i).zfill(3)}.txt"
        path = os.path.join(INPUT_DIR, filename)
        if os.path.exists(path):
            process_file(path)
    print("\n✅ Done cleaning all inputs.")

if __name__ == "__main__":
    main()