import os

# Folder containing input files
input_dir = "inputs"

# Loop through all 500 files
for i in range(1, 501):
    filename = f"input_{i:03}.txt"
    filepath = os.path.join(input_dir, filename)

    # Skip if file does not exist
    if not os.path.exists(filepath):
        print(f"❌ File missing: {filename}")
        continue

    # Read and clean file
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # If enough content, overwrite file
    if len(lines) >= 4:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"✅ Cleaned: {filename}")
    else:
        print(f"⚠ Not enough content (less than 4 lines): {filename}")