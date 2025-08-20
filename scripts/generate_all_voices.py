import os
import subprocess
import sys  # ✅ Required to use the correct Python interpreter

INPUT_DIR = "inputs"
TOTAL_FILES = 500

print("🎙 Generating all 500 voice recordings...")

for i in range(1, TOTAL_FILES + 1):
    file_number = str(i).zfill(3)
    input_file = os.path.join(INPUT_DIR, f"input_{file_number}.txt")
    
    if not os.path.exists(input_file):
        print(f"[!] Skipping missing file: {input_file}")
        continue

    print(f"[{file_number}] Generating voice for: {input_file}")
    try:
        # ✅ Use sys.executable to call Python from the correct virtual environment
        subprocess.run([sys.executable, "generate_voices.py", file_number], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error processing input_{file_number}.txt: {e}")

print("✅ All voice generation complete.")