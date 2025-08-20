import os

# === Settings ===
INPUT_FOLDER = "inputs"
MIN_ACCEPTABLE_WORDS = 375  # Anything below this must be expanded

# === Scan All Input Files ===
files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.endswith(".txt")])

short_files = []

print(f"\n🔍 Scanning {len(files)} input files...\n")

for filename in files:
    path = os.path.join(INPUT_FOLDER, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Count words excluding Speaker and Title
    words = [
        word for word in content.replace("\n", " ").split()
        if not word.strip().lower().startswith("speaker") and not word.strip().lower().startswith("title:")
    ]
    word_count = len(words)

    if word_count < MIN_ACCEPTABLE_WORDS:
        short_files.append((filename, word_count))

# === Output ===
print(f"\n🚨 Files that are too short (< {MIN_ACCEPTABLE_WORDS} words): {len(short_files)} files\n")

for fname, count in short_files:
    print(f"  {fname:20} — {count} words")

# === Save list of short files ===
with open("needs_expansion.txt", "w", encoding="utf-8") as out:
    for fname, _ in short_files:
        out.write(f"{fname}\n")

print("\n✅ Done. Saved list to 'needs_expansion.txt'.\n")