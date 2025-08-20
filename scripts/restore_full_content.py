import os

input_dir = "inputs"               # Folder with new format but reduced content
backup_dir = "inputs_backup"       # Folder with full original content
output_dir = "inputs_restored"     # Final fixed version

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if not filename.endswith(".txt"):
        continue

    input_path = os.path.join(input_dir, filename)
    backup_path = os.path.join(backup_dir, filename)
    output_path = os.path.join(output_dir, filename)

    if not os.path.exists(backup_path):
        print(f"Skipping {filename} - no backup found.")
        continue

    with open(input_path, 'r', encoding='utf-8') as f:
        input_lines = f.readlines()

    with open(backup_path, 'r', encoding='utf-8') as f:
        backup_lines = f.readlines()

    # Extract new intro part (up to and including first Speaker 1 line)
    try:
        speaker1_index = input_lines.index("Speaker 1:\n")
    except ValueError:
        print(f"Speaker 1 not found in {filename}")
        continue

    new_intro = input_lines[:speaker1_index + 1]

    # Extract speaker paragraphs from the backup
    try:
        speaker1_index_bk = backup_lines.index("Speaker 1:\n")
        speaker2_index_bk = backup_lines.index("Speaker 2:", speaker1_index_bk)
        speaker3_index_bk = backup_lines.index("Speaker 3:", speaker2_index_bk)

        speaker1_content = backup_lines[speaker1_index_bk + 1:speaker2_index_bk]
        speaker2_content = backup_lines[speaker2_index_bk:speaker3_index_bk]
        speaker3_content = backup_lines[speaker3_index_bk:]
    except ValueError:
        print(f"Format error in backup for {filename}")
        continue

    # Final merge
    final_lines = new_intro + speaker1_content + speaker2_content + speaker3_content

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)

print("✅ All files restored to full content with correct format.")