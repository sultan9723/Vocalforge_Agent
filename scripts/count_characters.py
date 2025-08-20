import os

INPUT_DIR = "inputs"
total_chars = 0
file_counts = {}

for file in os.listdir(INPUT_DIR):
    if file.endswith(".txt"):
        file_path = os.path.join(INPUT_DIR, file)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            char_count = len(text)
            total_chars += char_count
            file_counts[file] = char_count

print("\n📊 Character Count Per File:")
for file, count in sorted(file_counts.items()):
    print(f"{file}: {count} characters")

print(f"\n✅ TOTAL CHARACTERS across all files: {total_chars}")
approx_words = total_chars // 6
print(f"≈ Approx total words: {approx_words}")